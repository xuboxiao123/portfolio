import React from 'react';

const EventItem = ({ event, onEdit, onDelete }) => {
  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-GB', {
      day: 'numeric',
      month: 'short',
      year: 'numeric'
    });
  };

  const getDatePart = (dateString) => {
    return dateString.split(' ')[0];
  };

  return (
    <tr>
      <td>
        <div className="event-name">{event.name}</div>
        <div className="event-description">{event.description.substring(0, 50)}...</div>
      </td>
      <td>
        <div className="event-date">{formatDate(getDatePart(event.startdate))}</div>
      </td>
      <td>
        <div className="event-date">{formatDate(getDatePart(event.enddate))}</div>
      </td>
      <td className="actions">
        <button 
          className="btn-update"
          onClick={() => onEdit(event)}
        >
          Edit
        </button>
        <button 
          className="btn-delete"
          onClick={() => onDelete(event.id)}
        >
          Delete
        </button>
      </td>
    </tr>
  );
};

export default EventItem;