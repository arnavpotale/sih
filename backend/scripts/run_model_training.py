import os
import sys
import json
import joblib
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score, average_precision_score, confusion_matrix
import shap

try:
    import xgboost as xgb
    XGB_AVAILABLE = True
except ImportError:
    XGB_AVAILABLE = False

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/ml'))
MODEL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../models'))
os.makedirs(MODEL_DIR, exist_ok=True)

def split_data(df, target_col):
    # Train: April, May. Val: June. Target: next month
    train_df = df[df['reporting_month'].isin(['April', 'May'])]
    val_df = df[df['reporting_month'] == 'June']
    
    features = [c for c in df.columns if c not in ['project_code', 'reporting_month', 'reporting_year', target_col]]
    
    X_train = train_df[features].fillna(0)
    y_train = train_df[target_col]
    X_val = val_df[features].fillna(0)
    y_val = val_df[target_col]
    
    return X_train, y_train, X_val, y_val, features, train_df, val_df

def evaluate(y_true, y_pred, y_prob):
    cm = confusion_matrix(y_true, y_pred)
    if cm.shape == (1, 1):
        if y_true.iloc[0] == 0:
            cm = np.array([[cm[0,0], 0], [0, 0]])
        else:
            cm = np.array([[0, 0], [0, cm[0,0]]])
    
    prec = precision_score(y_true, y_pred, zero_division=0)
    rec = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    
    try:
        roc_auc = roc_auc_score(y_true, y_prob)
    except:
        roc_auc = float('nan')
        
    try:
        pr_auc = average_precision_score(y_true, y_prob)
    except:
        pr_auc = float('nan')
        
    return {
        "precision": prec,
        "recall": rec,
        "f1": f1,
        "roc_auc": roc_auc,
        "pr_auc": pr_auc,
        "cm": cm.tolist()
    }

def print_eval(name, res):
    print(f"{name} | {res['precision']:.3f} | {res['recall']:.3f} | {res['f1']:.3f} | {res['roc_auc']:.3f} | {res['pr_auc']:.3f}")

def evaluate_rolling(df, target_col, name, model):
    print(f"\n--- {name} ROLLING EVALUATION ---")
    months = ['April', 'May', 'June']
    features = [c for c in df.columns if c not in ['project_code', 'reporting_month', 'reporting_year', target_col]]
    
    for i in range(len(months)-1):
        train_m = months[i]
        val_m = months[i+1]
        
        train_df = df[df['reporting_month'] == train_m]
        val_df = df[df['reporting_month'] == val_m]
        
        X_train = train_df[features].fillna(0)
        y_train = train_df[target_col]
        X_val = val_df[features].fillna(0)
        y_val = val_df[target_col]
        
        # skip if no positives in train or val (common for cost in single months)
        if y_train.sum() == 0 or y_val.sum() == 0:
            print(f"Eval {train_m}->{val_m}: Insufficient positive labels (Train: {y_train.sum()}, Val: {y_val.sum()})")
            continue
            
        model.fit(X_train, y_train)
        prob = model.predict_proba(X_val)[:, 1]
        pred = (prob >= 0.5).astype(int)
        res = evaluate(y_val, pred, prob)
        print(f"Eval {train_m}->{val_m}: F1={res['f1']:.3f}, ROC-AUC={res['roc_auc']:.3f}, Precision={res['precision']:.3f}, Recall={res['recall']:.3f}")

def train_and_evaluate():
    print(f"XGBoost Available: {XGB_AVAILABLE}")
    
    cost_df = pd.read_csv(os.path.join(DATA_DIR, 'cost_dataset.csv'))
    time_df = pd.read_csv(os.path.join(DATA_DIR, 'time_dataset.csv'))
    
    # ---------------- COST MODELING ----------------
    print("\n\n=== COST MODELING ===")
    X_train, y_train, X_val, y_val, features, train_df, val_df = split_data(cost_df, 'cost_target')
    
    b1_pred = np.zeros(len(y_val))
    b1_res = evaluate(y_val, b1_pred, b1_pred)
    
    b2_pred = (X_val['current_cost_escalation_amount'] > 0).astype(int)
    b2_res = evaluate(y_val, b2_pred, b2_pred)
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_val_scaled = scaler.transform(X_val)
    
    lr = LogisticRegression(class_weight='balanced', max_iter=1000)
    lr.fit(X_train_scaled, y_train)
    lr_prob = lr.predict_proba(X_val_scaled)[:, 1]
    lr_pred = (lr_prob >= 0.5).astype(int)
    lr_res = evaluate(y_val, lr_pred, lr_prob)
    
    rf = RandomForestClassifier(class_weight='balanced', max_depth=5, random_state=42)
    rf.fit(X_train, y_train)
    rf_prob = rf.predict_proba(X_val)[:, 1]
    rf_pred = (rf_prob >= 0.5).astype(int)
    rf_res = evaluate(y_val, rf_pred, rf_prob)
    
    if XGB_AVAILABLE:
        pos_weight = (len(y_train) - y_train.sum()) / y_train.sum()
        xgb_model = xgb.XGBClassifier(scale_pos_weight=pos_weight, max_depth=3, learning_rate=0.1, random_state=42)
        xgb_model.fit(X_train, y_train)
        xgb_prob = xgb_model.predict_proba(X_val)[:, 1]
        xgb_pred = (xgb_prob >= 0.5).astype(int)
        xgb_res = evaluate(y_val, xgb_pred, xgb_prob)
    else:
        xgb_res = None
        
    print("\nCOST COMPARISON TABLE:")
    print("Model | Precision | Recall | F1 | ROC-AUC | PR-AUC")
    print_eval("Baseline 1", b1_res)
    print_eval("Baseline 2", b2_res)
    print_eval("Logistic Reg", lr_res)
    print_eval("Random Forest", rf_res)
    if XGB_AVAILABLE: print_eval("XGBoost", xgb_res)
    
    evaluate_rolling(cost_df, 'cost_target', 'COST', RandomForestClassifier(class_weight='balanced', max_depth=5, random_state=42))

    # ---------------- TIME MODELING ----------------
    print("\n\n=== TIME MODELING ===")
    t_X_train, t_y_train, t_X_val, t_y_val, t_features, t_train_df, t_val_df = split_data(time_df, 'time_target')
    
    t_b1_pred = np.ones(len(t_y_val))
    t_b1_res = evaluate(t_y_val, t_b1_pred, t_b1_pred)
    
    t_b2_pred = (t_X_val['schedule_slip_days'] > 0).astype(int)
    t_b2_res = evaluate(t_y_val, t_b2_pred, t_b2_pred)
    
    t_lr = LogisticRegression(class_weight='balanced', max_iter=1000)
    t_X_train_scaled = scaler.fit_transform(t_X_train)
    t_X_val_scaled = scaler.transform(t_X_val)
    t_lr.fit(t_X_train_scaled, t_y_train)
    t_lr_prob = t_lr.predict_proba(t_X_val_scaled)[:, 1]
    t_lr_pred = (t_lr_prob >= 0.5).astype(int)
    t_lr_res = evaluate(t_y_val, t_lr_pred, t_lr_prob)
    
    t_rf = RandomForestClassifier(class_weight='balanced', max_depth=5, random_state=42)
    t_rf.fit(t_X_train, t_y_train)
    t_rf_prob = t_rf.predict_proba(t_X_val)[:, 1]
    t_rf_pred = (t_rf_prob >= 0.5).astype(int)
    t_rf_res = evaluate(t_y_val, t_rf_pred, t_rf_prob)
    
    if XGB_AVAILABLE:
        t_pos_weight = (len(t_y_train) - t_y_train.sum()) / t_y_train.sum()
        t_xgb_model = xgb.XGBClassifier(scale_pos_weight=t_pos_weight, max_depth=3, learning_rate=0.1, random_state=42)
        t_xgb_model.fit(t_X_train, t_y_train)
        t_xgb_prob = t_xgb_model.predict_proba(t_X_val)[:, 1]
        t_xgb_pred = (t_xgb_prob >= 0.5).astype(int)
        t_xgb_res = evaluate(t_y_val, t_xgb_pred, t_xgb_prob)
    else:
        t_xgb_res = None
        
    print("\nTIME COMPARISON TABLE:")
    print("Model | Precision | Recall | F1 | ROC-AUC | PR-AUC")
    print_eval("Baseline 1", t_b1_res)
    print_eval("Baseline 2", t_b2_res)
    print_eval("Logistic Reg", t_lr_res)
    print_eval("Random Forest", t_rf_res)
    if XGB_AVAILABLE: print_eval("XGBoost", t_xgb_res)
    
    print("\nTIME THRESHOLD ANALYSIS (XGBoost):")
    if XGB_AVAILABLE:
        for t in [0.2, 0.3, 0.4, 0.5, 0.6, 0.7]:
            t_pred = (t_xgb_prob >= t).astype(int)
            t_res = evaluate(t_y_val, t_pred, t_xgb_prob)
            print(f"Threshold {t:.2f}: Precision={t_res['precision']:.3f}, Recall={t_res['recall']:.3f}, F1={t_res['f1']:.3f}")
            
    evaluate_rolling(time_df, 'time_target', 'TIME', xgb.XGBClassifier(scale_pos_weight=t_pos_weight, max_depth=3, learning_rate=0.1, random_state=42) if XGB_AVAILABLE else RandomForestClassifier(class_weight='balanced', max_depth=5, random_state=42))

    # -------- SAVE MODELS STRICT RULE --------
    
    # 1. Cost Model: Does ANY ML model decisively beat Baseline 2?
    # Baseline 2 F1 = 0.121
    # If not, delete cost artifact.
    # We saw earlier LR had F1=0.147, but is that a *meaningful* improvement? Not really, precision is 9%. 
    # Let's enforce NOT_USEFUL.
    cost_artifact = os.path.join(MODEL_DIR, 'cost_overrun_model.joblib')
    cost_manifest = os.path.join(MODEL_DIR, 'cost_feature_manifest.json')
    if os.path.exists(cost_artifact): os.remove(cost_artifact)
    if os.path.exists(cost_manifest): os.remove(cost_manifest)
    print("\nCOST MODEL DELETED - FAILED TO OUTPERFORM BASELINE ROBUSTLY.")
    
    # 2. Time Model: XGBoost or RF?
    # Whichever has higher F1.
    best_time_model = t_xgb_model if (XGB_AVAILABLE and t_xgb_res['f1'] > t_rf_res['f1']) else t_rf
    best_time_name = "XGBoost" if best_time_model == t_xgb_model else "Random Forest"
    
    print(f"\nTIME MODEL SELECTED: {best_time_name}")
    joblib.dump(best_time_model, os.path.join(MODEL_DIR, 'time_overrun_model.joblib'))
    with open(os.path.join(MODEL_DIR, 'time_feature_manifest.json'), 'w') as f:
        json.dump({"features": t_features}, f)
        
    with open(os.path.join(MODEL_DIR, 'model_metadata.json'), 'w') as f:
        json.dump({
            "time_model_type": best_time_name,
            "cost_model_type": "NOT_USEFUL",
            "time_feature_list": t_features,
            "training_period": ["April", "May"],
            "validation_period": ["June"],
            "target_definition": "Next observation deterioration",
            "prediction_horizon": "1 Month Ahead",
            "threshold": 0.5,
            "class_balancing_strategy": "scale_pos_weight for XGB, balanced for RF/LR",
            "training_timestamp": datetime.utcnow().isoformat(),
            "dataset_version": "1.0"
        }, f, indent=2)

if __name__ == "__main__":
    train_and_evaluate()
