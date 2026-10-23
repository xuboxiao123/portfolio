import React, { useState, useEffect } from 'react';

const EventForm = ({ onSubmit, onCancel, initialData }) => {
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    startdate: '',
    enddate: ''
  });

  useEffect(() => {
    if (initialData) {
      setFormData({
        name: initialData.name,
        description: initialData.description,
        startdate: initialData.startdate.split(' ')[0],
        enddate: initialData.enddate.split(' ')[0]
      });
    }
  }, [initialData]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const formattedData = {
      ...formData,
      startdate: `${formData.startdate} 00:00`,
      enddate: `${formData.enddate} 00:00`
    };
    onSubmit(formattedData);
  };

  return (
    <div className="form-modal">
      <form onSubmit={handleSubmit} className="event-form">
        <h2>{initialData ? 'Update Event' : 'Add New Event'}</h2>
        
        <div className="form-group">
          <label>Event Name:</label>
          <input
            type="text"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
            autoFocus
          />
        </div>

        <div className="form-group">
          <label>Description:</label>
          <textarea
            name="description"
            value={formData.description}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label>Start Date:</label>
          <input
            type="date"
            name="startdate"
            value={formData.startdate}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label>End Date:</label>
          <input
            type="date"
            name="enddate"
            value={formData.enddate}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-actions">
          <button type="submit" className="btn-save">
            {initialData ? 'Update' : 'Save'}
          </button>
          <button type="button" className="btn-cancel" onClick={onCancel}>
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
};

export default EventForm;