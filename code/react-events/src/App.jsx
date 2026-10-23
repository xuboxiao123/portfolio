import React, { useState, useEffect } from 'react';
import EventList from './components/EventList';
import EventForm from './components/EventForm';
import { getEvents, createEvent, updateEvent, deleteEvent } from './services/api';
import './index.css';

function App() {
  const [events, setEvents] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [sortOrder, setSortOrder] = useState('asc');
  const [editingEvent, setEditingEvent] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState('');

  useEffect(() => {
    const fetchEvents = async () => {
      try {
        setIsLoading(true);
        const data = await getEvents();
        setEvents(data);
        setError(null);
      } catch (err) {
        setError('Unable to load event data, please check API connection');
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    };
    
    fetchEvents();
  }, []);

  const handleSubmit = async (eventData) => {
    try {
      setIsLoading(true);
      
      if (editingEvent) {
        await updateEvent(editingEvent.id, eventData);
        setSuccessMessage('Event updated successfully!');
      } else {
        await createEvent(eventData);
        setSuccessMessage('Event created successfully!');
      }
      
      const updatedEvents = await getEvents();
      setEvents(updatedEvents);
      setShowForm(false);
      setEditingEvent(null);
      
      // Clear success message after 3 seconds
      setTimeout(() => setSuccessMessage(''), 3000);
    } catch (err) {
      setError(editingEvent ? 'Update event failed' : 'Event creation failed');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this event?')) {
      try {
        setIsLoading(true);
        await deleteEvent(id);
        setEvents(events.filter(event => event.id !== id));
        setSuccessMessage('Event deleted successfully!');
        
        // Clear success message after 3 seconds
        setTimeout(() => setSuccessMessage(''), 3000);
      } catch (err) {
        setError('Failed to delete event');
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    }
  };

  return (
    <div className="container">
      <div className="ink-splash ink-splash-1"></div>
      <div className="ink-splash ink-splash-2"></div>
      
      <header>
        <h1>Event Management System</h1>
        <button 
          className="btn-new"
          onClick={() => {
            setEditingEvent(null);
            setShowForm(true);
          }}
        >
          + New Event
        </button>
      </header>

      {error && <div className="error-message">{error}</div>}
      {successMessage && <div className="success-message">{successMessage}</div>}
      
      {isLoading ? (
        <div className="loading">
          <div className="loading-spinner"></div>
          <p>Loading events...</p>
        </div>
      ) : (
        <>
          {showForm && (
            <EventForm 
              onSubmit={handleSubmit} 
              onCancel={() => {
                setShowForm(false);
                setEditingEvent(null);
              }}
              initialData={editingEvent}
            />
          )}

          <EventList 
            events={events}
            onEdit={(event) => {
              setEditingEvent(event);
              setShowForm(true);
            }}
            onDelete={handleDelete}
            searchTerm={searchTerm}
            setSearchTerm={setSearchTerm}
            sortOrder={sortOrder}
            setSortOrder={setSortOrder}
          />
        </>
      )}
    </div>
  );
  
}

export default App;