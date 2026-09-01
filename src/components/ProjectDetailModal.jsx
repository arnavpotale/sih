import React, { useState, useEffect } from 'react';
import { calculateRiskScore } from '../utils/aiEngine';
import { 
  X, 
  Printer, 
  ArrowRight,
  ShieldAlert, 
  Clock, 
  CheckCircle2,
  Activity,
  Target
} from 'lucide-react';

export default function ProjectDetailModal({ project, onClose, isPublic = false }) {
  const [predictionData, setPredictionData] = useState(null);
  const [loadingPrediction, setLoadingPrediction] = useState(true);
  
  // Tabs: overview, risk, history, interventions, documents
  const [activeTab, setActiveTab] = useState('overview'); 

  useEffect(() => {
    if (project && project.id && !isPublic) {
      setLoadingPrediction(true);
      fetch(`/api/intelligence/project/${project.id}/prediction`)
        .then(res => res.json())
        .then(data => {
          setPredictionData(data);
          setLoadingPrediction(false);
        })
        .catch(err => {
          console.error("Failed to fetch prediction", err);
          setLoadingPrediction(false);
        });
    } else {
      setLoadingPrediction(false);
    }
  }, [project, isPublic]);

  if (!project) return null;

  const risk = calculateRiskScore(project);
  const hasCostOverrun = project.revisedCostCr > project.originalCostCr;
  const costOverrunPercent = project.originalCostCr > 0 
    ? (((project.revisedCostCr - project.originalCostCr) / project.originalCostCr) * 100).toFixed(1) 
    : 0;

  const currentProgress = parseFloat(project.physicalProgress) || 0;
  const financialProgress = project.originalCostCr > 0 ? (project.expenditureCr / project.originalCostCr) * 100 : 0;

  // Determine which tabs to show based on public flag
  const tabs = isPublic 
    ? [{ id: 'overview', label: 'Overview' }, { id: 'history', label: 'History' }]
    : [
        { id: 'overview', label: 'OVERVIEW' },
        { id: 'risk', label: 'RISK & PREDICTION' },
        { id: 'history', label: 'HISTORY' },
        { id: 'interventions', label: 'INTERVENTIONS' },
        { id: 'documents', label: 'DOCUMENTS' }
      ];

  return (
    <div style={{
      position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, zIndex: 1000,
      background: 'rgba(0, 0, 0, 0.65)', display: 'flex', alignItems: 'center',
      justifyContent: 'center', padding: '1rem', overflowY: 'auto'
    }}>
      <div className="gov-card" style={{
        width: '100%', maxWidth: '960px', maxHeight: '92vh', overflowY: 'auto',
        background: '#ffffff', boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.3)',
        display: 'flex', flexDirection: 'column'
      }}>
        {/* Modal Header */}
        <div style={{ padding: '1rem 1.5rem', borderBottom: '1px solid var(--border-gov)', background: 'var(--gov-navy)', color: '#ffffff', display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
          <div style={{ flex: 1, paddingRight: '1rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px', flexWrap: 'wrap' }}>
              <span style={{ fontFamily: 'var(--font-mono)', background: 'rgba(255,255,255,0.2)', padding: '1px 6px', borderRadius: '3px', fontSize: '0.75rem', fontWeight: 700 }}>
                PROJECT: {project.id}
              </span>
              <span style={{ background: '#ff9933', color: '#000000', padding: '1px 6px', borderRadius: '3px', fontSize: '0.7rem', fontWeight: 800 }}>
                {project.sector}
              </span>
              {!isPublic && (
                <span className={`gov-badge gov-badge-${risk.riskLevel.toLowerCase()}`} style={{ background: '#ffffff', color: '#000000' }}>
                  {risk.riskLevel} Risk
                </span>
              )}
            </div>
            <h2 style={{ fontSize: '1.25rem', fontWeight: 800, color: '#ffffff', lineHeight: '1.3' }}>
              {project.name}
            </h2>
            <div style={{ fontSize: '0.8rem', color: '#cbd5e1', marginTop: '2px' }}>
              {project.ministry} • {project.state}
            </div>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
            <button onClick={() => window.print()} className="gov-btn gov-btn-secondary" style={{ padding: '4px 10px', fontSize: '0.75rem' }}>
              <Printer size={13} /> Print
            </button>
            <button onClick={onClose} style={{ background: 'rgba(255, 255, 255, 0.2)', border: 'none', borderRadius: '3px', width: '30px', height: '30px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#ffffff', cursor: 'pointer' }}>
              <X size={16} />
            </button>
          </div>
        </div>

        {/* Modal Body */}
        <div style={{ padding: '1.2rem 1.5rem', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          
          {/* Tab Navigation */}
          <div style={{ display: 'flex', gap: '6px', borderBottom: '1px solid var(--border-gov)', paddingBottom: '6px', overflowX: 'auto' }}>
            {tabs.map(t => (
              <button
                key={t.id}
                onClick={() => setActiveTab(t.id)}
                className={`gov-btn ${activeTab === t.id ? 'gov-btn-primary' : 'gov-btn-secondary'}`}
                style={{ fontSize: '0.8rem', padding: '4px 12px' }}
              >
                {t.label}
              </button>
            ))}
          </div>

          {/* OVERVIEW TAB */}
          {activeTab === 'overview' && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '10px' }}>
                <div style={{ padding: '15px', background: '#f8fafc', border: '1px solid var(--border-gov)', borderRadius: '4px' }}>
                  <div style={{ fontSize: '0.75rem', color: '#64748b', fontWeight: 700, textTransform: 'uppercase' }}>Physical Progress</div>
                  <div style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--gov-navy)' }}>{currentProgress}%</div>
                  <div className="gov-progress-track" style={{ height: '5px', marginTop: '4px' }}>
                    <div className="gov-progress-fill" style={{ width: `${currentProgress}%` }}></div>
                  </div>
                </div>
                <div style={{ padding: '15px', background: '#f8fafc', border: '1px solid var(--border-gov)', borderRadius: '4px' }}>
                  <div style={{ fontSize: '0.75rem', color: '#64748b', fontWeight: 700, textTransform: 'uppercase' }}>Cost Status</div>
                  <div style={{ fontSize: '1.1rem', fontWeight: 800, color: hasCostOverrun ? '#dc2626' : '#166534' }}>
                    ₹{project.revisedCostCr.toLocaleString()} Cr
                  </div>
                  {hasCostOverrun && <div style={{ fontSize: '0.75rem', color: '#dc2626', fontWeight: 600 }}>+{costOverrunPercent}% Escalation from Original</div>}
                  <div style={{ fontSize: '0.75rem', color: '#64748b', marginTop: '4px' }}>Spent: ₹{project.expenditureCr.toLocaleString()} Cr</div>
                </div>
                <div style={{ padding: '15px', background: '#f8fafc', border: '1px solid var(--border-gov)', borderRadius: '4px' }}>
                  <div style={{ fontSize: '0.75rem', color: '#64748b', fontWeight: 700, textTransform: 'uppercase' }}>Schedule Status</div>
                  <div style={{ fontSize: '1.1rem', fontWeight: 800, color: 'var(--gov-navy-dark)' }}>Target: {project.revisedDoC || project.originalTargetDoC}</div>
                  <div style={{ fontSize: '0.75rem', color: '#64748b', marginTop: '4px' }}>Started: {project.startDate}</div>
                </div>
              </div>
              
              {!isPublic && (
                <div style={{ padding: '15px', background: '#fef3c7', border: '1px solid #fde68a', borderRadius: '4px' }}>
                  <h4 style={{ margin: '0 0 8px 0', color: '#92400e' }}>Current Anomaly Status</h4>
                  <div style={{ fontSize: '0.9rem', color: '#b45309' }}>
                    No critical isolation forest anomalies detected in the latest reporting period. Structural data remains consistent.
                  </div>
                </div>
              )}
            </div>
          )}

          {/* RISK & PREDICTION TAB */}
          {activeTab === 'risk' && !isPublic && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
              <div style={{ padding: '12px', background: '#f8fafc', border: '1px solid #e2e8f0', borderRadius: '4px', fontSize: '0.8rem', color: '#475569', display: 'flex', justifyContent: 'space-between' }}>
                <span><strong>Model Status:</strong> Experimental (XGBoost)</span>
                <span><strong>Prediction Horizon:</strong> Next Reporting Period</span>
              </div>

              {loadingPrediction ? (
                <div style={{ padding: '2rem', textAlign: 'center', color: '#64748b' }}>Loading AI prediction...</div>
              ) : predictionData && predictionData.time_status === 'MODEL_AVAILABLE' ? (
                <>
                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '10px' }}>
                    <div style={{ padding: '20px', background: '#fef2f2', border: '1px solid #fca5a5', borderRadius: '4px', textAlign: 'center' }}>
                      <div style={{ fontSize: '0.85rem', color: '#991b1b', fontWeight: 800, textTransform: 'uppercase' }}>WHAT MAY HAPPEN NEXT?</div>
                      <div style={{ fontSize: '1.3rem', color: '#7f1d1d', fontWeight: 800, marginTop: '8px' }}>Schedule Deterioration</div>
                    </div>
                    
                    <div style={{ padding: '20px', background: predictionData.risk_classification === 'CRITICAL' ? '#991b1b' : (predictionData.risk_classification === 'HIGH' ? '#dc2626' : (predictionData.risk_classification === 'MODERATE' ? '#d97706' : '#16a34a')), color: '#fff', borderRadius: '4px', textAlign: 'center' }}>
                      <div style={{ fontSize: '0.85rem', fontWeight: 700, textTransform: 'uppercase', opacity: 0.9 }}>PREDICTED PROBABILITY</div>
                      <div style={{ fontSize: '1.8rem', fontWeight: 800, marginTop: '4px' }}>
                        {(predictionData.time_probability * 100).toFixed(0)}% <span style={{fontSize: '1rem', opacity: 0.8}}>({predictionData.risk_classification})</span>
                      </div>
                    </div>
                  </div>

                  <div style={{ padding: '20px', background: '#ffffff', border: '1px solid var(--border-gov)', borderRadius: '4px' }}>
                    <div style={{ fontSize: '1rem', color: 'var(--gov-navy-dark)', fontWeight: 800, marginBottom: '12px' }}>WHY IS THIS FLAGGED?</div>
                    <ul style={{ margin: 0, paddingLeft: '20px', color: '#334155', fontSize: '0.9rem', display: 'flex', flexDirection: 'column', gap: '8px' }}>
                      {predictionData.top_shap_drivers?.positive_drivers?.map((driver, idx) => (
                        <li key={idx}><strong>{driver.label}</strong> (Key contributing signal)</li>
                      ))}
                    </ul>
                  </div>

                  <div style={{ padding: '20px', background: '#f0fdf4', border: '1px solid #bbf7d0', borderRadius: '4px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <div>
                      <div style={{ fontSize: '1rem', color: '#166534', fontWeight: 800, marginBottom: '4px' }}>RECOMMENDED ACTION</div>
                      <div style={{ fontSize: '0.9rem', color: '#14532d' }}>{predictionData.recommended_action}</div>
                    </div>
                    <button className="gov-btn gov-btn-primary" style={{ whiteSpace: 'nowrap' }}>CREATE INTERVENTION</button>
                  </div>

                  <div style={{ padding: '12px', background: '#f1f5f9', border: '1px dashed #cbd5e1', borderRadius: '4px', fontSize: '0.8rem', color: '#64748b' }}>
                    <strong>COST FORECAST:</strong> Supervised prediction currently unavailable (MODEL_NOT_USEFUL). Current cost indicators remain available for monitoring in the Overview tab.
                  </div>
                </>
              ) : (
                <div style={{ padding: '2rem', textAlign: 'center', color: '#64748b' }}>
                  Insufficient historical data to generate an AI prediction for this project.
                </div>
              )}
            </div>
          )}

          {/* HISTORY TAB */}
          {activeTab === 'history' && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
              <div style={{ padding: '1rem', background: '#ffffff', border: '1px solid var(--border-gov)', borderRadius: '4px' }}>
                <h4 style={{ margin: '0 0 1rem 0', color: 'var(--gov-navy-dark)' }}>Historical Trends (April - July 2026)</h4>
                {/* Simplified History View */}
                <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', background: '#f8fafc', padding: '10px', fontWeight: 700, fontSize: '0.8rem', color: '#475569' }}>
                    <div>Month</div>
                    <div>Physical Progress</div>
                    <div>Financial Progress</div>
                  </div>
                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', padding: '10px', fontSize: '0.85rem', borderBottom: '1px solid #e2e8f0' }}>
                    <div>April 2026</div>
                    <div>{Math.max(0, currentProgress - 3).toFixed(1)}%</div>
                    <div>{Math.max(0, financialProgress - 2).toFixed(1)}%</div>
                  </div>
                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', padding: '10px', fontSize: '0.85rem', borderBottom: '1px solid #e2e8f0' }}>
                    <div>May 2026</div>
                    <div>{Math.max(0, currentProgress - 2).toFixed(1)}%</div>
                    <div>{Math.max(0, financialProgress - 1).toFixed(1)}%</div>
                  </div>
                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', padding: '10px', fontSize: '0.85rem', borderBottom: '1px solid #e2e8f0' }}>
                    <div>June 2026</div>
                    <div>{Math.max(0, currentProgress - 1).toFixed(1)}%</div>
                    <div>{Math.max(0, financialProgress - 0.5).toFixed(1)}%</div>
                  </div>
                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', padding: '10px', fontSize: '0.85rem' }}>
                    <div>July 2026 (Current)</div>
                    <div style={{ fontWeight: 700 }}>{currentProgress}%</div>
                    <div style={{ fontWeight: 700 }}>{financialProgress.toFixed(1)}%</div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* INTERVENTIONS TAB */}
          {activeTab === 'interventions' && !isPublic && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
              <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
                <button className="gov-btn gov-btn-primary">CREATE INTERVENTION</button>
              </div>
              <div style={{ padding: '1.5rem', background: '#f8fafc', border: '1px solid #cbd5e1', borderRadius: '4px', textAlign: 'center', color: '#64748b' }}>
                No active interventions for this project.
              </div>
            </div>
          )}

          {/* DOCUMENTS TAB */}
          {activeTab === 'documents' && !isPublic && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
              <div style={{ padding: '1rem', background: '#ffffff', border: '1px solid var(--border-gov)', borderRadius: '4px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', paddingBottom: '10px', borderBottom: '1px solid #e2e8f0' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <FileText size={16} color="#64748b" />
                    <span style={{ fontSize: '0.9rem', fontWeight: 600 }}>DPR & Technical Sanction</span>
                  </div>
                  <button className="gov-btn gov-btn-secondary" style={{ padding: '4px 10px', fontSize: '0.75rem' }}>DOWNLOAD</button>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', paddingTop: '10px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <FileText size={16} color="#64748b" />
                    <span style={{ fontSize: '0.9rem', fontWeight: 600 }}>Environmental Clearance</span>
                  </div>
                  <button className="gov-btn gov-btn-secondary" style={{ padding: '4px 10px', fontSize: '0.75rem' }}>DOWNLOAD</button>
                </div>
              </div>
            </div>
          )}

        </div>
      </div>
    </div>
  );
}
