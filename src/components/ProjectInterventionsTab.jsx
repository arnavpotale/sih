import React, { useState, useEffect } from 'react';
import { ClipboardList, Clock, CheckCircle2, ShieldAlert } from 'lucide-react';
import CreateInterventionForm from './CreateInterventionForm';

export default function ProjectInterventionsTab({ project, risk }) {
  const [interventions, setInterventions] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [showCreateForm, setShowCreateForm] = useState(false);

  const fetchInterventions = () => {
    setIsLoading(true);
    fetch(`http://localhost:8000/api/interventions/project/${project.id}`)
      .then(res => res.json())
      .then(data => {
        setInterventions(data);
        setIsLoading(false);
      })
      .catch(err => {
        console.error('Failed to fetch interventions:', err);
        setIsLoading(false);
      });
  };

  useEffect(() => {
    fetchInterventions();
  }, [project.id]);

  const handleSuccess = (newIntervention) => {
    setShowCreateForm(false);
    fetchInterventions(); // Refresh list
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
      
      {/* Recommended Action / Create Section */}
      <div style={{ padding: '1rem', background: '#f8fafc', border: '1px solid var(--border-gov)', borderRadius: '4px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <h4 style={{ margin: '0 0 4px 0', fontSize: '0.9rem', color: 'var(--gov-navy-dark)' }}>Recommended Action</h4>
            <p style={{ margin: 0, fontSize: '0.8rem', color: '#64748b' }}>
              {risk.recommendedAction}
            </p>
          </div>
          {!showCreateForm && (
            <button 
              onClick={() => setShowCreateForm(true)}
              className="gov-btn gov-btn-primary"
            >
              CREATE INTERVENTION
            </button>
          )}
        </div>

        {showCreateForm && (
          <CreateInterventionForm 
            project={project} 
            risk={risk} 
            onCancel={() => setShowCreateForm(false)} 
            onSuccess={handleSuccess} 
          />
        )}
      </div>

      {/* Intervention History */}
      <div>
        <h4 style={{ margin: '1rem 0 0.5rem 0', fontSize: '0.9rem', color: 'var(--gov-navy-dark)' }}>Intervention History</h4>
        
        {isLoading ? (
          <div style={{ fontSize: '0.85rem', color: '#64748b' }}>Loading interventions...</div>
        ) : interventions.length === 0 ? (
          <div style={{ fontSize: '0.85rem', color: '#64748b', padding: '1rem', textAlign: 'center', background: '#f8fafc', borderRadius: '4px' }}>
            No interventions recorded for this project.
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            {interventions.map(inv => (
              <div key={inv.id} style={{ 
                padding: '12px', 
                background: '#ffffff', 
                border: '1px solid var(--border-light)', 
                borderLeft: `4px solid ${inv.status === 'CLOSED' ? '#10b981' : (inv.status === 'OPEN' ? '#ef4444' : '#f59e0b')}`,
                borderRadius: '4px'
              }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '6px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                    {inv.status === 'CLOSED' ? <CheckCircle2 size={16} color="#10b981" /> : (inv.status === 'OPEN' ? <ShieldAlert size={16} color="#ef4444" /> : <Clock size={16} color="#f59e0b" />)}
                    <span style={{ fontWeight: 700, fontSize: '0.85rem' }}>{inv.title}</span>
                  </div>
                  <span className={`gov-badge`} style={{ fontSize: '0.7rem', background: inv.status === 'CLOSED' ? '#d1fae5' : '#fee2e2', color: inv.status === 'CLOSED' ? '#065f46' : '#991b1b' }}>
                    {inv.status.replace('_', ' ')}
                  </span>
                </div>
                <div style={{ fontSize: '0.8rem', color: '#64748b', marginBottom: '6px' }}>
                  {inv.description}
                </div>
                <div style={{ display: 'flex', gap: '15px', fontSize: '0.75rem', color: '#94a3b8' }}>
                  <span><strong>Priority:</strong> {inv.priority}</span>
                  <span><strong>Assigned:</strong> {inv.assigned_to}</span>
                  <span><strong>Due:</strong> {inv.due_date}</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

    </div>
  );
}
