import React, { useState } from 'react';
import { X, Send, Paperclip } from 'lucide-react';

export default function ManagerInterventionResponseModal({ intervention, onClose }) {
  const [responseNotes, setResponseNotes] = useState('');
  const [updatedPhysicalProgress, setUpdatedPhysicalProgress] = useState('');
  const [updatedFinancialProgress, setUpdatedFinancialProgress] = useState('');
  const [currentBlocker, setCurrentBlocker] = useState('');
  const [expectedResolutionDate, setExpectedResolutionDate] = useState('');
  const [evidenceFilename, setEvidenceFilename] = useState('');
  
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    // Simulate file upload by just recording the filename if provided
    let finalEvidence = null;
    if (evidenceFilename) {
      finalEvidence = evidenceFilename.split('\\').pop().split('/').pop();
    }

    const payload = {
      status: 'AWAITING_VERIFICATION',
      response_notes: responseNotes,
      updated_physical_progress: updatedPhysicalProgress,
      updated_financial_progress: updatedFinancialProgress,
      current_blocker: currentBlocker,
      expected_resolution_date: expectedResolutionDate,
      evidence_filename: finalEvidence
    };

    try {
      const res = await fetch(`http://localhost:8000/api/interventions/${intervention.id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (!res.ok) throw new Error('Failed to submit response');
      onClose(); // Triggers refresh in parent
    } catch (err) {
      console.error(err);
      alert('Error submitting response.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div style={{
      position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, zIndex: 1000,
      background: 'rgba(0, 0, 0, 0.65)', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '1rem'
    }}>
      <div className="gov-card" style={{
        width: '100%', maxWidth: '800px', maxHeight: '90vh', overflowY: 'auto',
        background: '#ffffff', display: 'flex', flexDirection: 'column'
      }}>
        {/* Header */}
        <div style={{ padding: '1rem 1.5rem', background: 'var(--gov-navy)', color: '#ffffff', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <h2 style={{ fontSize: '1.1rem', margin: 0 }}>Respond to Intervention</h2>
            <div style={{ fontSize: '0.75rem', opacity: 0.8 }}>Project: {intervention.project_id}</div>
          </div>
          <button onClick={onClose} style={{ background: 'transparent', border: 'none', color: '#ffffff', cursor: 'pointer' }}>
            <X size={20} />
          </button>
        </div>

        <div style={{ padding: '1.5rem', display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          
          {/* Official Directive */}
          <div style={{ padding: '15px', background: '#fef2f2', border: '1px solid #fca5a5', borderRadius: '4px', fontSize: '0.85rem' }}>
            <h4 style={{ margin: '0 0 10px 0', fontSize: '0.9rem', color: '#991b1b' }}>Official Directive</h4>
            <div style={{ marginBottom: '10px' }}><strong>Issue:</strong> {intervention.title}</div>
            <div style={{ marginBottom: '10px' }}><strong>Requested Action:</strong> {intervention.description}</div>
            <div style={{ display: 'flex', gap: '20px', color: '#991b1b' }}>
              <span><strong>Priority:</strong> {intervention.priority}</span>
              <span><strong>Due:</strong> {intervention.due_date}</span>
            </div>
            {intervention.response_notes && intervention.response_notes.includes('[OFFICIAL CLARIFICATION REQUEST]') && (
              <div style={{ marginTop: '10px', paddingTop: '10px', borderTop: '1px solid #fca5a5', color: '#b91c1c', fontWeight: 600 }}>
                ⚠️ Official requested further clarification. Please review notes below and update.
              </div>
            )}
          </div>

          <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <h4 style={{ margin: 0, fontSize: '0.9rem', color: 'var(--gov-navy)' }}>Project Response</h4>
            
            <div>
              <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, marginBottom: '4px' }}>Response Notes *</label>
              <textarea 
                rows={4} 
                value={responseNotes} 
                onChange={e => setResponseNotes(e.target.value)} 
                required 
                style={{ width: '100%', padding: '8px', fontSize: '0.85rem', border: '1px solid #cbd5e1' }} 
                placeholder="Detail the actions taken to address the directive..."
              />
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
              <div>
                <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, marginBottom: '4px' }}>Updated Physical Progress (%)</label>
                <input type="number" step="0.1" value={updatedPhysicalProgress} onChange={e => setUpdatedPhysicalProgress(e.target.value)} style={{ width: '100%', padding: '6px', fontSize: '0.85rem', border: '1px solid #cbd5e1' }} />
              </div>
              <div>
                <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, marginBottom: '4px' }}>Updated Financial Progress (%)</label>
                <input type="number" step="0.1" value={updatedFinancialProgress} onChange={e => setUpdatedFinancialProgress(e.target.value)} style={{ width: '100%', padding: '6px', fontSize: '0.85rem', border: '1px solid #cbd5e1' }} />
              </div>
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, marginBottom: '4px' }}>Current Blocker (If any)</label>
              <input type="text" value={currentBlocker} onChange={e => setCurrentBlocker(e.target.value)} style={{ width: '100%', padding: '6px', fontSize: '0.85rem', border: '1px solid #cbd5e1' }} />
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, marginBottom: '4px' }}>Expected Resolution Date</label>
              <input type="date" value={expectedResolutionDate} onChange={e => setExpectedResolutionDate(e.target.value)} style={{ width: '100%', padding: '6px', fontSize: '0.85rem', border: '1px solid #cbd5e1' }} />
            </div>

            <div style={{ padding: '10px', background: '#f8fafc', border: '1px dashed #cbd5e1', borderRadius: '4px' }}>
              <label style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.8rem', fontWeight: 600, marginBottom: '4px', cursor: 'pointer' }}>
                <Paperclip size={16} /> Attach Evidence (PDF/Image)
              </label>
              <input type="file" onChange={e => setEvidenceFilename(e.target.value)} style={{ fontSize: '0.8rem' }} />
              <div style={{ fontSize: '0.7rem', color: '#64748b', marginTop: '4px' }}>* For prototype purposes, this simulates file upload by recording the filename.</div>
            </div>

            <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '10px', marginTop: '10px' }}>
              <button type="button" onClick={onClose} className="gov-btn gov-btn-secondary">Cancel</button>
              <button type="submit" disabled={isSubmitting} className="gov-btn gov-btn-primary">
                {isSubmitting ? 'Submitting...' : <><Send size={14} /> SUBMIT FOR VERIFICATION</>}
              </button>
            </div>
          </form>

        </div>
      </div>
    </div>
  );
}
