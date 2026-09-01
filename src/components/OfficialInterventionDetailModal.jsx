import React, { useState } from 'react';
import { X, CheckCircle2, ShieldAlert } from 'lucide-react';

export default function OfficialInterventionDetailModal({ intervention, onClose }) {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [clarificationText, setClarificationText] = useState('');

  const updateStatus = async (status, responseNotesAddendum = '') => {
    setIsSubmitting(true);
    try {
      let notes = intervention.response_notes || '';
      if (responseNotesAddendum) {
        notes += `\n\n[OFFICIAL CLARIFICATION REQUEST]: ${responseNotesAddendum}`;
      }

      const res = await fetch(`http://localhost:8000/api/interventions/${intervention.id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status, response_notes: notes })
      });
      if (!res.ok) throw new Error('Failed to update status');
      onClose(); // Will trigger refresh in parent
    } catch (err) {
      console.error(err);
      alert('Error updating intervention status.');
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
        width: '100%', maxWidth: '700px', maxHeight: '90vh', overflowY: 'auto',
        background: '#ffffff', display: 'flex', flexDirection: 'column'
      }}>
        {/* Header */}
        <div style={{ padding: '1rem 1.5rem', background: 'var(--gov-navy)', color: '#ffffff', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <h2 style={{ fontSize: '1.1rem', margin: 0 }}>Intervention Review</h2>
            <div style={{ fontSize: '0.75rem', opacity: 0.8 }}>ID: {intervention.id} • Project: {intervention.project_id}</div>
          </div>
          <button onClick={onClose} style={{ background: 'transparent', border: 'none', color: '#ffffff', cursor: 'pointer' }}>
            <X size={20} />
          </button>
        </div>

        <div style={{ padding: '1.5rem', display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          
          {/* Intervention Details */}
          <div>
            <h4 style={{ margin: '0 0 10px 0', fontSize: '0.9rem', color: 'var(--gov-navy)' }}>Original Directive</h4>
            <div style={{ padding: '15px', background: '#f8fafc', border: '1px solid var(--border-gov)', borderRadius: '4px', fontSize: '0.85rem' }}>
              <div style={{ marginBottom: '10px' }}><strong>Title:</strong> {intervention.title}</div>
              <div style={{ marginBottom: '10px' }}><strong>Description:</strong> {intervention.description}</div>
              <div style={{ display: 'flex', gap: '20px', color: '#64748b' }}>
                <span><strong>Priority:</strong> {intervention.priority}</span>
                <span><strong>Due Date:</strong> {intervention.due_date}</span>
                <span><strong>Status:</strong> {intervention.status.replace('_', ' ')}</span>
              </div>
            </div>
          </div>

          {/* Manager Response */}
          <div>
            <h4 style={{ margin: '0 0 10px 0', fontSize: '0.9rem', color: 'var(--gov-navy)' }}>Project Manager Response</h4>
            <div style={{ padding: '15px', background: '#f0fdf4', border: '1px solid #bbf7d0', borderRadius: '4px', fontSize: '0.85rem' }}>
              {!intervention.response_notes && intervention.status === 'OPEN' ? (
                <div style={{ color: '#64748b', fontStyle: 'italic' }}>No response submitted yet. Awaiting action from Project Manager.</div>
              ) : (
                <>
                  <div style={{ marginBottom: '10px' }}><strong>Response Notes:</strong><br/>{intervention.response_notes || 'N/A'}</div>
                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px', marginBottom: '10px' }}>
                    <div><strong>Updated Physical Progress:</strong> {intervention.updated_physical_progress || 'N/A'}%</div>
                    <div><strong>Updated Financial Progress:</strong> {intervention.updated_financial_progress || 'N/A'}%</div>
                  </div>
                  <div style={{ marginBottom: '10px' }}><strong>Current Blocker:</strong> {intervention.current_blocker || 'None'}</div>
                  <div style={{ marginBottom: '10px' }}><strong>Expected Resolution:</strong> {intervention.expected_resolution_date || 'N/A'}</div>
                  <div style={{ marginBottom: '10px' }}><strong>Evidence:</strong> {intervention.evidence_filename || 'No evidence attached'}</div>
                </>
              )}
            </div>
          </div>

          {/* Official Actions */}
          {(intervention.status === 'AWAITING_VERIFICATION' || intervention.status === 'IN_PROGRESS') && (
            <div style={{ padding: '15px', borderTop: '1px solid var(--border-gov)', marginTop: '10px' }}>
              <h4 style={{ margin: '0 0 10px 0', fontSize: '0.9rem', color: 'var(--gov-navy)' }}>Official Decision</h4>
              
              <div style={{ marginBottom: '15px' }}>
                <textarea 
                  rows={2} 
                  placeholder="Optional clarification request notes..." 
                  value={clarificationText}
                  onChange={e => setClarificationText(e.target.value)}
                  style={{ width: '100%', padding: '8px', fontSize: '0.85rem', border: '1px solid #cbd5e1', borderRadius: '4px' }}
                />
              </div>

              <div style={{ display: 'flex', gap: '10px' }}>
                <button 
                  onClick={() => updateStatus('IN_PROGRESS', clarificationText)}
                  disabled={isSubmitting || !clarificationText.trim()}
                  className="gov-btn gov-btn-secondary"
                  style={{ flex: 1, justifyContent: 'center' }}
                >
                  <ShieldAlert size={16} /> REQUEST CLARIFICATION
                </button>
                <button 
                  onClick={() => updateStatus('CLOSED')}
                  disabled={isSubmitting}
                  className="gov-btn gov-btn-primary"
                  style={{ flex: 1, justifyContent: 'center', background: '#059669', borderColor: '#059669' }}
                >
                  <CheckCircle2 size={16} /> VERIFY & CLOSE
                </button>
              </div>
            </div>
          )}

        </div>
      </div>
    </div>
  );
}
