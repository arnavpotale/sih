import React, { useState, useEffect } from 'react';
import { ClipboardList, Clock, CheckCircle2, ShieldAlert, ArrowRight } from 'lucide-react';
import OfficialInterventionDetailModal from './OfficialInterventionDetailModal';

export default function InterventionCentre({ onSelectProject }) {
  const [interventions, setInterventions] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [filter, setFilter] = useState('All');
  const [selectedIntervention, setSelectedIntervention] = useState(null);

  const fetchInterventions = () => {
    setIsLoading(true);
    fetch('http://localhost:8000/api/interventions/')
      .then(res => res.json())
      .then(data => {
        setInterventions(data);
        setIsLoading(false);
      })
      .catch(err => {
        console.error("Failed to fetch interventions:", err);
        setIsLoading(false);
      });
  };

  useEffect(() => {
    fetchInterventions();
  }, []);

  const filteredInterventions = interventions.filter(i => {
    if (filter === 'All') return true;
    return i.status.replace('_', ' ') === filter;
  });

  return (
    <div style={{ maxWidth: '1200px', margin: '0 auto', paddingTop: '2rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <div>
          <h1 style={{ fontSize: '1.75rem', fontWeight: 800, color: 'var(--gov-navy)', margin: '0 0 4px 0' }}>
            Intervention Centre
          </h1>
          <p style={{ margin: 0, color: '#64748b' }}>Active directive monitoring and response verification</p>
        </div>
      </div>

      <div style={{ display: 'flex', gap: '8px', marginBottom: '1.5rem', overflowX: 'auto', paddingBottom: '10px' }}>
        {['All', 'OPEN', 'IN PROGRESS', 'AWAITING VERIFICATION', 'RESOLVED', 'CLOSED'].map(f => (
          <button 
            key={f} 
            onClick={() => setFilter(f)}
            className={`gov-btn ${filter === f ? 'gov-btn-primary' : 'gov-btn-secondary'}`}
            style={{ fontSize: '0.8rem', padding: '6px 12px', whiteSpace: 'nowrap' }}
          >
            {f}
          </button>
        ))}
      </div>

      <div className="gov-card" style={{ background: '#ffffff', overflow: 'hidden' }}>
        {isLoading ? (
          <div style={{ padding: '2rem', textAlign: 'center', color: '#64748b' }}>Loading interventions...</div>
        ) : filteredInterventions.length === 0 ? (
          <div style={{ padding: '3rem 2rem', textAlign: 'center', color: '#64748b' }}>
            <ShieldAlert size={32} color="#cbd5e1" style={{ marginBottom: '10px' }} />
            <div>No interventions match the selected filter.</div>
          </div>
        ) : (
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.85rem' }}>
            <thead style={{ background: '#f8fafc', borderBottom: '1px solid var(--border-gov)', textAlign: 'left' }}>
              <tr>
                <th style={{ padding: '12px 16px', color: 'var(--gov-navy)' }}>Intervention</th>
                <th style={{ padding: '12px 16px', color: 'var(--gov-navy)' }}>Priority</th>
                <th style={{ padding: '12px 16px', color: 'var(--gov-navy)' }}>Assigned To</th>
                <th style={{ padding: '12px 16px', color: 'var(--gov-navy)' }}>Due Date</th>
                <th style={{ padding: '12px 16px', color: 'var(--gov-navy)' }}>Status</th>
                <th style={{ padding: '12px 16px', color: 'var(--gov-navy)', width: '80px' }}></th>
              </tr>
            </thead>
            <tbody>
              {filteredInterventions.map(inv => (
                <tr key={inv.id} style={{ borderBottom: '1px solid var(--border-light)' }}>
                  <td style={{ padding: '16px' }}>
                    <div style={{ fontWeight: 700, color: 'var(--text-primary)', marginBottom: '4px' }}>{inv.title}</div>
                    <div style={{ color: '#64748b', fontSize: '0.75rem' }}>Project ID: {inv.project_id}</div>
                  </td>
                  <td style={{ padding: '16px' }}>
                    <span className="gov-badge" style={{ 
                      background: inv.priority === 'CRITICAL' ? '#fee2e2' : (inv.priority === 'HIGH' ? '#ffedd5' : '#f1f5f9'),
                      color: inv.priority === 'CRITICAL' ? '#991b1b' : (inv.priority === 'HIGH' ? '#9a3412' : '#334155')
                    }}>
                      {inv.priority}
                    </span>
                  </td>
                  <td style={{ padding: '16px', color: '#475569' }}>{inv.assigned_to}</td>
                  <td style={{ padding: '16px', color: '#475569' }}>{inv.due_date}</td>
                  <td style={{ padding: '16px' }}>
                    <span className="gov-badge" style={{ 
                      background: inv.status === 'CLOSED' ? '#d1fae5' : '#f1f5f9',
                      color: inv.status === 'CLOSED' ? '#065f46' : '#334155'
                    }}>
                      {inv.status.replace('_', ' ')}
                    </span>
                  </td>
                  <td style={{ padding: '16px' }}>
                    <button 
                      onClick={() => setSelectedIntervention(inv)}
                      className="gov-btn gov-btn-secondary"
                      style={{ padding: '4px 10px' }}
                    >
                      View <ArrowRight size={14} />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {selectedIntervention && (
        <OfficialInterventionDetailModal 
          intervention={selectedIntervention}
          onClose={() => {
            setSelectedIntervention(null);
            fetchInterventions();
          }}
        />
      )}
    </div>
  );
}
