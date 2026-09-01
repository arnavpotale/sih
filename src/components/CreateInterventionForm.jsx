import React, { useState } from 'react';

export default function CreateInterventionForm({ project, risk, onCancel, onSuccess }) {
  const [title, setTitle] = useState(`Review: ${project.primaryDrivers?.[0] || 'Progress Divergence'}`);
  const [description, setDescription] = useState('');
  const [priority, setPriority] = useState(risk.riskLevel === 'Critical' ? 'CRITICAL' : 'HIGH');
  const [assignedTo, setAssignedTo] = useState('Project Manager');
  const [dueDate, setDueDate] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError(null);

    const payload = {
      project_id: project.id,
      title,
      description,
      priority,
      assigned_to: assignedTo,
      due_date: dueDate
    };

    try {
      const res = await fetch('http://localhost:8000/api/interventions/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (!res.ok) throw new Error('Failed to create intervention');
      
      const data = await res.json();
      onSuccess(data);
    } catch (err) {
      console.error(err);
      setError('An error occurred while creating the intervention.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem', marginTop: '1rem' }}>
      <div style={{ padding: '1rem', background: '#f8fafc', border: '1px solid var(--border-gov)', borderRadius: '4px' }}>
        <h4 style={{ margin: '0 0 10px 0', fontSize: '0.9rem', color: 'var(--gov-navy-dark)' }}>Intervention Details</h4>
        
        {error && <div style={{ color: 'red', fontSize: '0.8rem', marginBottom: '10px' }}>{error}</div>}

        <div style={{ marginBottom: '10px' }}>
          <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, marginBottom: '4px' }}>Project (Read Only)</label>
          <input type="text" value={project.name} disabled style={{ width: '100%', padding: '6px', fontSize: '0.85rem' }} />
        </div>

        <div style={{ marginBottom: '10px' }}>
          <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, marginBottom: '4px' }}>Risk / Trigger</label>
          <input type="text" value={`${risk.riskLevel} Risk — ${project.primaryDrivers?.[0] || 'Progress Divergence'}`} disabled style={{ width: '100%', padding: '6px', fontSize: '0.85rem' }} />
        </div>

        <div style={{ marginBottom: '10px' }}>
          <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, marginBottom: '4px' }}>Intervention Title *</label>
          <input type="text" value={title} onChange={e => setTitle(e.target.value)} required style={{ width: '100%', padding: '6px', fontSize: '0.85rem', border: '1px solid #cbd5e1' }} />
        </div>

        <div style={{ marginBottom: '10px' }}>
          <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, marginBottom: '4px' }}>Description & Recommended Action *</label>
          <textarea rows={3} value={description} onChange={e => setDescription(e.target.value)} required style={{ width: '100%', padding: '6px', fontSize: '0.85rem', border: '1px solid #cbd5e1' }} placeholder="Enter the exact directive for the agency..."></textarea>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
          <div>
            <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, marginBottom: '4px' }}>Priority</label>
            <select value={priority} onChange={e => setPriority(e.target.value)} style={{ width: '100%', padding: '6px', fontSize: '0.85rem', border: '1px solid #cbd5e1' }}>
              <option value="CRITICAL">CRITICAL</option>
              <option value="HIGH">HIGH</option>
              <option value="MEDIUM">MEDIUM</option>
              <option value="LOW">LOW</option>
            </select>
          </div>
          <div>
            <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, marginBottom: '4px' }}>Due Date *</label>
            <input type="date" value={dueDate} onChange={e => setDueDate(e.target.value)} required style={{ width: '100%', padding: '6px', fontSize: '0.85rem', border: '1px solid #cbd5e1' }} />
          </div>
        </div>
      </div>

      <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '10px' }}>
        <button type="button" onClick={onCancel} className="gov-btn gov-btn-secondary">Cancel</button>
        <button type="submit" disabled={isSubmitting} className="gov-btn gov-btn-primary">
          {isSubmitting ? 'Submitting...' : 'CREATE INTERVENTION'}
        </button>
      </div>
    </form>
  );
}
