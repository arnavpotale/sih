import React, { useState, useEffect } from 'react';
import { TENDERS_DATA } from '../data/tendersData';
import { 
  HardHat, 
  Building2, 
  Sparkles, 
  CheckCircle2, 
  AlertTriangle, 
  Briefcase, 
  ClipboardList
} from 'lucide-react';
import TendersBiddingPlatform from './TendersBiddingPlatform';
import ManagerInterventionResponseModal from './ManagerInterventionResponseModal';

export default function CompanyBidderPortal({ tenderUser }) {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [selectedTenderForAi, setSelectedTenderForAi] = useState(TENDERS_DATA[0]);
  const [aiEligibilityResult, setAiEligibilityResult] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  // Agency Interventions State
  const [agencyInterventions, setAgencyInterventions] = useState([]);
  const [selectedInterventionToRespond, setSelectedInterventionToRespond] = useState(null);
  const [loadingInterventions, setLoadingInterventions] = useState(false);

  const fetchAgencyInterventions = () => {
    setLoadingInterventions(true);
    fetch('http://localhost:8000/api/interventions/')
      .then(res => res.json())
      .then(data => {
        setAgencyInterventions(data);
        setLoadingInterventions(false);
      })
      .catch(err => {
        console.error("Failed to load interventions:", err);
        setLoadingInterventions(false);
      });
  };

  useEffect(() => {
    fetchAgencyInterventions();
  }, []);

  // Company profile
  const companyProfile = {
    name: tenderUser?.companyName || 'ABC Infrastructure & Engineering Pvt. Ltd.',
    cin: tenderUser?.cin || 'U45200MH2012PTC239841',
    vendorCode: tenderUser?.vendorCode || 'VND-2026-9041',
    annualTurnoverCr: 1120.0,
    solvencyCr: 420.0,
    experienceYears: 9,
    certifications: ['ISO 9001:2015', 'ISO 14001:2015', 'ISO 45001:2018 (Safety)'],
    ongoingProjectsCount: 3,
    completedProjectsCount: 14
  };

  // Run AI Pre-Bid Eligibility Screener
  const runAiEligibilityCheck = (tender) => {
    setSelectedTenderForAi(tender);
    setIsAnalyzing(true);
    setAiEligibilityResult(null);

    setTimeout(() => {
      const req = tender.mandatoryRequirements || {};
      const meetsTurnover = companyProfile.annualTurnoverCr >= (req.minAnnualTurnoverCr || 500);
      const meetsExperience = companyProfile.experienceYears >= (req.minSimilarExperienceYears || 5);
      const meetsSolvency = companyProfile.solvencyCr >= (req.financialSolvencyCr || 200);

      let score = 85;
      if (meetsTurnover) score += 5;
      if (meetsExperience) score += 5;
      if (meetsSolvency) score += 3;
      if (score > 98) score = 98;

      setAiEligibilityResult({
        tenderTitle: tender.title,
        tenderId: tender.id,
        agency: tender.agency,
        score: score,
        isEligible: score >= 75,
        criteriaChecks: [
          { label: `Annual Turnover Requirement (₹${req.minAnnualTurnoverCr || 800} Cr)`, status: meetsTurnover ? 'pass' : 'fail', note: `Company: ₹${companyProfile.annualTurnoverCr} Cr` },
          { label: `Relevant EPC Experience (${req.minSimilarExperienceYears || 7} Years)`, status: meetsExperience ? 'pass' : 'fail', note: `Company: ${companyProfile.experienceYears} Years Track Record` },
          { label: `Bank Financial Solvency (₹${req.financialSolvencyCr || 300} Cr)`, status: meetsSolvency ? 'pass' : 'fail', note: `Company: ₹${companyProfile.solvencyCr} Cr Scheduled Bank Attested` },
          { label: 'Statutory GSTIN & Class-3 DSC Compliance', status: 'pass', note: 'Valid & Verified under CPPP Registry' },
          { label: 'ISO 9001 / ISO 45001 Safety Management System', status: 'pass', note: 'Certified & Uploaded in Document Vault' }
        ],
        missingDocuments: [
          'Joint Venture Power of Attorney (if bidding in Consortium)',
          'Specific Equipment Lease Agreement for Sub-Zero Batching Additives (if applicable)'
        ],
        aiRecommendations: `Strong competitive profile with ${score}% pre-qualification match. Ensure the Appendix-II Bank Guarantee has a 180-day validity to prevent technical disqualification during Stage-1 screening.`
      });
      setIsAnalyzing(false);
    }, 600);
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem', width: '100%', padding: '1rem 0 3rem 0' }}>
      
      {/* Bidder Welcome Banner */}
      <div className="gov-card" style={{
        padding: '1.5rem 2rem',
        background: 'linear-gradient(135deg, #ffffff 0%, #fffbeb 100%)',
        borderLeft: '6px solid #f59e0b',
        borderRadius: '8px'
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}>
              <span className="gov-badge" style={{ background: '#fef3c7', color: '#92400e', border: '1px solid #fcd34d' }}>
                CPPP E-Procurement Desk & Implementing Agency Portal
              </span>
              <span style={{ fontSize: '0.75rem', color: '#b45309', fontWeight: 600 }}>
                Vendor ID: {companyProfile.vendorCode} • Class-1 EPC Verified
              </span>
            </div>
            <h1 style={{ fontSize: '1.6rem', fontWeight: 800, color: '#78350f', margin: 0 }}>
              {companyProfile.name}
            </h1>
            <p style={{ fontSize: '0.85rem', color: '#92400e', marginTop: '4px', margin: 0 }}>
              CIN: {companyProfile.cin} | Financial Capacity: ₹{companyProfile.annualTurnoverCr} Cr | Solvency: ₹{companyProfile.solvencyCr} Cr
            </p>
          </div>

          {/* Navigation Pills */}
          <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
            <button
              onClick={() => setActiveTab('dashboard')}
              style={{
                padding: '8px 16px',
                borderRadius: '6px',
                fontSize: '0.82rem',
                fontWeight: 700,
                border: activeTab === 'dashboard' ? '2px solid #d97706' : '1px solid #cbd5e1',
                background: activeTab === 'dashboard' ? '#fffbeb' : '#ffffff',
                color: activeTab === 'dashboard' ? '#92400e' : '#475569',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '6px'
              }}
            >
              <Building2 size={16} />
              <span>Company Dashboard</span>
            </button>

            <button
              onClick={() => setActiveTab('agency-interventions')}
              style={{
                padding: '8px 16px',
                borderRadius: '6px',
                fontSize: '0.82rem',
                fontWeight: 700,
                border: activeTab === 'agency-interventions' ? '2px solid #d97706' : '1px solid #cbd5e1',
                background: activeTab === 'agency-interventions' ? '#fffbeb' : '#ffffff',
                color: activeTab === 'agency-interventions' ? '#92400e' : '#475569',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '6px'
              }}
            >
              <ClipboardList size={16} color="#d97706" />
              <span>Govt Directives & Interventions ({agencyInterventions.length})</span>
            </button>

            <button
              onClick={() => setActiveTab('ai-screener')}
              style={{
                padding: '8px 16px',
                borderRadius: '6px',
                fontSize: '0.82rem',
                fontWeight: 700,
                border: activeTab === 'ai-screener' ? '2px solid #d97706' : '1px solid #cbd5e1',
                background: activeTab === 'ai-screener' ? '#fffbeb' : '#ffffff',
                color: activeTab === 'ai-screener' ? '#92400e' : '#475569',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '6px'
              }}
            >
              <Sparkles size={16} color="#d97706" />
              <span>AI Pre-Bid Eligibility Screener</span>
            </button>

            <button
              onClick={() => setActiveTab('tenders-platform')}
              style={{
                padding: '8px 16px',
                borderRadius: '6px',
                fontSize: '0.82rem',
                fontWeight: 700,
                border: activeTab === 'tenders-platform' ? '2px solid #d97706' : '1px solid #cbd5e1',
                background: activeTab === 'tenders-platform' ? '#b45309' : '#ffffff',
                color: activeTab === 'tenders-platform' ? '#ffffff' : '#b45309',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '6px',
                boxShadow: '0 2px 6px rgba(180, 83, 9, 0.25)'
              }}
            >
              <Briefcase size={16} />
              <span>Browse Tenders & Submit Bids</span>
            </button>
          </div>
        </div>
      </div>

      {/* ------------------------------------------------------------- */}
      {/* 1. COMPANY DASHBOARD VIEW */}
      {/* ------------------------------------------------------------- */}
      {activeTab === 'dashboard' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem' }}>
            <div className="gov-card" style={{ padding: '1.2rem', borderTop: '4px solid #10b981' }}>
              <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', fontWeight: 600 }}>Active Tenders (Open)</div>
              <div style={{ fontSize: '1.8rem', fontWeight: 800, color: '#065f46', marginTop: '4px' }}>4</div>
              <div style={{ fontSize: '0.72rem', color: '#059669', marginTop: '4px' }}>₹10,050 Cr Total Value</div>
            </div>

            <div className="gov-card" style={{ padding: '1.2rem', borderTop: '4px solid #3b82f6' }}>
              <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', fontWeight: 600 }}>Active Directives</div>
              <div style={{ fontSize: '1.8rem', fontWeight: 800, color: '#1e40af', marginTop: '4px' }}>{agencyInterventions.length}</div>
              <div style={{ fontSize: '0.72rem', color: '#1e40af', marginTop: '4px' }}>From MoSPI Monitoring Desk</div>
            </div>

            <div className="gov-card" style={{ padding: '1.2rem', borderTop: '4px solid #f59e0b' }}>
              <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', fontWeight: 600 }}>Bids Under Evaluation</div>
              <div style={{ fontSize: '1.8rem', fontWeight: 800, color: '#b45309', marginTop: '4px' }}>1</div>
              <div style={{ fontSize: '0.72rem', color: '#b45309', marginTop: '4px' }}>Stage-2 Commercial Bid</div>
            </div>

            <div className="gov-card" style={{ padding: '1.2rem', borderTop: '4px solid #059669' }}>
              <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', fontWeight: 600 }}>Awarded Contracts (L1)</div>
              <div style={{ fontSize: '1.8rem', fontWeight: 800, color: '#059669', marginTop: '4px' }}>1</div>
              <div style={{ fontSize: '0.72rem', color: '#059669', marginTop: '4px' }}>₹740 Cr Sela Pass Package</div>
            </div>
          </div>

          {/* Bid Tracking Table */}
          <div className="gov-card" style={{ padding: '1.5rem', background: '#ffffff' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem', flexWrap: 'wrap', gap: '8px' }}>
              <div>
                <h3 style={{ fontSize: '1.15rem', fontWeight: 800, color: 'var(--gov-navy-dark)', margin: 0 }}>
                  Company Bidding Portfolio & Stage Status
                </h3>
                <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', margin: 0 }}>
                  Track live bid statuses, evaluation stages, and post-award debrief outcomes.
                </p>
              </div>

              <button
                onClick={() => setActiveTab('ai-screener')}
                style={{
                  padding: '6px 14px',
                  borderRadius: '6px',
                  border: '1px solid #f59e0b',
                  background: '#fffbeb',
                  color: '#92400e',
                  fontWeight: 700,
                  fontSize: '0.78rem',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '6px'
                }}
              >
                <Sparkles size={14} color="#d97706" />
                <span>Test Next Bid Eligibility</span>
              </button>
            </div>

            <div style={{ overflowX: 'auto' }}>
              <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.82rem' }}>
                <thead>
                  <tr style={{ background: '#f8fafc', borderBottom: '2px solid #e2e8f0', textAlign: 'left', color: '#475569' }}>
                    <th style={{ padding: '10px 12px' }}>Tender ID & Package</th>
                    <th style={{ padding: '10px 12px' }}>Agency</th>
                    <th style={{ padding: '10px 12px' }}>Value (Cr)</th>
                    <th style={{ padding: '10px 12px' }}>Submitted Date</th>
                    <th style={{ padding: '10px 12px' }}>Evaluation Stage</th>
                    <th style={{ padding: '10px 12px' }}>Status</th>
                  </tr>
                </thead>
                <tbody>
                  <tr style={{ borderBottom: '1px solid #f1f5f9' }}>
                    <td style={{ padding: '12px' }}>
                      <strong>TND-2026-NHAI-0884</strong>
                      <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>6-Lane Vadodara–Mumbai Expressway</div>
                    </td>
                    <td style={{ padding: '12px' }}>NHAI</td>
                    <td style={{ padding: '12px', fontWeight: 700 }}>₹1,850 Cr</td>
                    <td style={{ padding: '12px' }}>2026-04-10</td>
                    <td style={{ padding: '12px' }}>Stage 1 Technical Verification</td>
                    <td style={{ padding: '12px' }}>
                      <span style={{ padding: '3px 8px', borderRadius: '4px', background: '#fef3c7', color: '#92400e', fontWeight: 700, fontSize: '0.72rem' }}>
                        ⏳ Under Evaluation
                      </span>
                    </td>
                  </tr>

                  <tr style={{ borderBottom: '1px solid #f1f5f9' }}>
                    <td style={{ padding: '12px' }}>
                      <strong>TND-2025-NHIDCL-0488</strong>
                      <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Sela Pass High-Altitude Roads</div>
                    </td>
                    <td style={{ padding: '12px' }}>NHIDCL</td>
                    <td style={{ padding: '12px', fontWeight: 700 }}>₹740 Cr</td>
                    <td style={{ padding: '12px' }}>2026-01-15</td>
                    <td style={{ padding: '12px' }}>Contract Executed</td>
                    <td style={{ padding: '12px' }}>
                      <span style={{ padding: '3px 8px', borderRadius: '4px', background: '#dcfce7', color: '#166534', fontWeight: 700, fontSize: '0.72rem' }}>
                        🏆 Awarded (L1)
                      </span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* ------------------------------------------------------------- */}
      {/* 2. AGENCY INTERVENTIONS & DIRECTIVES DESK */}
      {/* ------------------------------------------------------------- */}
      {activeTab === 'agency-interventions' && (
        <div className="gov-card" style={{ padding: '1.5rem', background: '#ffffff' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.2rem', flexWrap: 'wrap', gap: '8px' }}>
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}>
                <span className="gov-badge gov-badge-navy">Implementing Agency Action Queue</span>
                <span style={{ fontSize: '0.75rem', color: '#64748b' }}>Connected to MoSPI Central Database</span>
              </div>
              <h3 style={{ fontSize: '1.25rem', fontWeight: 800, color: 'var(--gov-navy-dark)', margin: 0 }}>
                Official Government Directives & Corrective Actions
              </h3>
              <p style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', margin: '4px 0 0 0' }}>
                Review assigned risk interventions, submit milestone progress, and upload compliance certificates.
              </p>
            </div>
          </div>

          {loadingInterventions ? (
            <div style={{ padding: '3rem', textAlign: 'center', color: '#64748b' }}>Loading active directives...</div>
          ) : agencyInterventions.length === 0 ? (
            <div style={{ padding: '3rem', textAlign: 'center', color: '#64748b' }}>
              <CheckCircle2 size={36} color="#10b981" style={{ marginBottom: '10px' }} />
              <div style={{ fontWeight: 700 }}>No Pending Government Directives</div>
              <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>All monitored project milestones are currently on track.</div>
            </div>
          ) : (
            <div style={{ overflowX: 'auto' }}>
              <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.85rem' }}>
                <thead>
                  <tr style={{ background: '#f8fafc', borderBottom: '2px solid #e2e8f0', textAlign: 'left', color: '#475569' }}>
                    <th style={{ padding: '12px 14px' }}>Directive Title</th>
                    <th style={{ padding: '12px 14px' }}>Project ID</th>
                    <th style={{ padding: '12px 14px' }}>Priority</th>
                    <th style={{ padding: '12px 14px' }}>Due Date</th>
                    <th style={{ padding: '12px 14px' }}>Status</th>
                    <th style={{ padding: '12px 14px' }}>Action</th>
                  </tr>
                </thead>
                <tbody>
                  {agencyInterventions.map((inv) => (
                    <tr key={inv.id} style={{ borderBottom: '1px solid #f1f5f9' }}>
                      <td style={{ padding: '14px' }}>
                        <div style={{ fontWeight: 700, color: 'var(--gov-navy-dark)' }}>{inv.title}</div>
                        <div style={{ fontSize: '0.75rem', color: '#64748b' }}>{inv.description}</div>
                      </td>
                      <td style={{ padding: '14px', fontWeight: 600 }}>{inv.project_id}</td>
                      <td style={{ padding: '14px' }}>
                        <span className="gov-badge" style={{
                          background: inv.priority === 'CRITICAL' ? '#fee2e2' : '#fef3c7',
                          color: inv.priority === 'CRITICAL' ? '#991b1b' : '#92400e'
                        }}>
                          {inv.priority}
                        </span>
                      </td>
                      <td style={{ padding: '14px', color: '#475569' }}>{inv.due_date}</td>
                      <td style={{ padding: '14px' }}>
                        <span className="gov-badge" style={{
                          background: inv.status === 'CLOSED' ? '#dcfce7' : '#f1f5f9',
                          color: inv.status === 'CLOSED' ? '#166534' : '#334155'
                        }}>
                          {inv.status.replace('_', ' ')}
                        </span>
                      </td>
                      <td style={{ padding: '14px' }}>
                        <button
                          onClick={() => setSelectedInterventionToRespond(inv)}
                          className="gov-btn gov-btn-primary"
                          style={{ padding: '6px 12px', fontSize: '0.78rem' }}
                        >
                          <span>Respond & Evidence →</span>
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}

      {/* ------------------------------------------------------------- */}
      {/* 3. AI PRE-BID ELIGIBILITY SCREENER */}
      {/* ------------------------------------------------------------- */}
      {activeTab === 'ai-screener' && (
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1.3fr', gap: '1.5rem' }}>
          <div className="gov-card" style={{ padding: '1.5rem', background: '#ffffff' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '6px' }}>
              <span className="gov-badge" style={{ background: '#fef3c7', color: '#92400e' }}>Automated Pre-Bid AI</span>
              <span style={{ fontSize: '0.75rem', color: '#64748b' }}>GFR 2017 & CPPP Standard Compliance</span>
            </div>
            <h3 style={{ fontSize: '1.2rem', fontWeight: 800, color: '#78350f', margin: '0 0 4px 0' }}>
              Select Tender to Evaluate Eligibility
            </h3>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '1.2rem' }}>
              Our AI evaluates your company turnover, experience, and certifications against mandatory tender clauses.
            </p>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.8rem' }}>
              {TENDERS_DATA.map(t => {
                const isSelected = selectedTenderForAi?.id === t.id;
                return (
                  <div
                    key={t.id}
                    onClick={() => runAiEligibilityCheck(t)}
                    style={{
                      padding: '1rem',
                      borderRadius: '6px',
                      border: isSelected ? '2px solid #d97706' : '1px solid #e2e8f0',
                      background: isSelected ? '#fffbeb' : '#ffffff',
                      cursor: 'pointer',
                      transition: 'all 0.15s ease'
                    }}
                  >
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '4px' }}>
                      <span style={{ fontSize: '0.72rem', fontWeight: 700, color: 'var(--gov-navy)' }}>{t.id}</span>
                      <span style={{ fontSize: '0.72rem', fontWeight: 700, color: '#b45309' }}>₹{t.estimatedCostCr} Cr</span>
                    </div>
                    <h4 style={{ fontSize: '0.88rem', fontWeight: 700, color: '#1e293b', margin: '0 0 4px 0' }}>
                      {t.title}
                    </h4>
                    <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                      🏛️ {t.agency} • Closes: {t.bidClosingDate ? t.bidClosingDate.split('T')[0] : 'Open'}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          <div className="gov-card" style={{ padding: '1.5rem', background: '#ffffff' }}>
            {isAnalyzing ? (
              <div style={{ padding: '3rem', textAlign: 'center', color: '#b45309' }}>
                <Sparkles size={32} style={{ animation: 'spin 2s linear infinite', marginBottom: '12px' }} />
                <h3>Analyzing Mandatory Tender Clauses against Bidder Profile...</h3>
                <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>
                  Cross-referencing turnover, financial solvency, machinery capacity, and statutory compliance.
                </p>
              </div>
            ) : aiEligibilityResult ? (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '1.2rem' }}>
                <div style={{
                  padding: '1.2rem',
                  borderRadius: '8px',
                  background: aiEligibilityResult.score >= 80 ? '#ecfdf5' : '#fffbeb',
                  border: `1.5px solid ${aiEligibilityResult.score >= 80 ? '#10b981' : '#f59e0b'}`,
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  flexWrap: 'wrap',
                  gap: '1rem'
                }}>
                  <div>
                    <span style={{ fontSize: '0.72rem', fontWeight: 700, textTransform: 'uppercase', color: aiEligibilityResult.score >= 80 ? '#065f46' : '#92400e' }}>
                      Eligibility Verdict
                    </span>
                    <h3 style={{ fontSize: '1.3rem', fontWeight: 800, color: aiEligibilityResult.score >= 80 ? '#065f46' : '#78350f', margin: '2px 0 0 0' }}>
                      {aiEligibilityResult.score >= 80 ? '🟢 Highly Qualified to Bid' : '🟡 Moderate Match (Action Required)'}
                    </h3>
                  </div>

                  <div style={{ textAlign: 'right' }}>
                    <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>Overall Match Score</div>
                    <div style={{ fontSize: '2rem', fontWeight: 800, color: aiEligibilityResult.score >= 80 ? '#059669' : '#d97706' }}>
                      {aiEligibilityResult.score}%
                    </div>
                  </div>
                </div>

                <div>
                  <h4 style={{ fontSize: '0.95rem', fontWeight: 700, color: 'var(--gov-navy-dark)', marginBottom: '8px' }}>
                    Mandatory Clause-by-Clause Verification:
                  </h4>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                    {aiEligibilityResult.criteriaChecks.map((check, idx) => (
                      <div
                        key={idx}
                        style={{
                          padding: '10px 12px',
                          borderRadius: '6px',
                          background: '#f8fafc',
                          border: '1px solid #e2e8f0',
                          display: 'flex',
                          alignItems: 'flex-start',
                          gap: '10px'
                        }}
                      >
                        {check.status === 'pass' ? (
                          <CheckCircle2 size={18} color="#16a34a" style={{ flexShrink: 0, marginTop: '2px' }} />
                        ) : (
                          <AlertTriangle size={18} color="#f59e0b" style={{ flexShrink: 0, marginTop: '2px' }} />
                        )}
                        <div>
                          <strong style={{ fontSize: '0.82rem', color: '#1e293b' }}>{check.label}</strong>
                          <div style={{ fontSize: '0.75rem', color: '#64748b', marginTop: '2px' }}>{check.note}</div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                <div style={{ background: '#eff6ff', border: '1px solid #bfdbfe', borderRadius: '6px', padding: '1rem' }}>
                  <div style={{ fontSize: '0.8rem', fontWeight: 700, color: '#1e40af', display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '6px' }}>
                    <Sparkles size={15} color="#2563eb" />
                    <span>AI Strategic Recommendation for this Tender:</span>
                  </div>
                  <p style={{ fontSize: '0.8rem', color: '#1e3a8a', margin: 0, lineHeight: '1.4' }}>
                    {aiEligibilityResult.aiRecommendations}
                  </p>
                </div>

                <button
                  onClick={() => setActiveTab('tenders-platform')}
                  className="gov-btn gov-btn-primary"
                  style={{ padding: '10px', fontSize: '0.88rem', fontWeight: 700 }}
                >
                  Proceed to Online Bid Submission Packet →
                </button>
              </div>
            ) : (
              <div style={{ padding: '3rem', textAlign: 'center', color: 'var(--text-muted)' }}>
                Click on any tender on the left to run an automated AI pre-qualification eligibility check.
              </div>
            )}
          </div>
        </div>
      )}

      {/* ------------------------------------------------------------- */}
      {/* 4. BROWSE TENDERS & SUBMIT BIDS */}
      {/* ------------------------------------------------------------- */}
      {activeTab === 'tenders-platform' && (
        <TendersBiddingPlatform />
      )}

      {/* Modal: Manager Intervention Response */}
      {selectedInterventionToRespond && (
        <ManagerInterventionResponseModal
          intervention={selectedInterventionToRespond}
          onClose={() => {
            setSelectedInterventionToRespond(null);
            fetchAgencyInterventions();
          }}
        />
      )}

    </div>
  );
}
