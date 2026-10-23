import React from 'react';
import EventItem from './EventItem';
import SearchBar from './SearchBar';

const EventList = ({ 
  events, 
  onEdit, 
  onDelete, 
  searchTerm, 
  setSearchTerm,
  sortOrder,
  setSortOrder
}) => {
  const filteredEvents = events
    .filter(event => 
      event.name.toLowerCase().includes(searchTerm.toLowerCase())
    )
    .sort((a, b) => {
      const dateA = new Date(a.startdate);
      const dateB = new Date(b.startdate);
      return sortOrder === 'asc' ? dateA - dateB : dateB - dateA;
    });

  return (
    <div className="event-list">
      <SearchBar 
        searchTerm={searchTerm}
        setSearchTerm={setSearchTerm}
        sortOrder={sortOrder}
        setSortOrder={setSortOrder}
      />

      {filteredEvents.length > 0 ? (
        <table>
          <thead>
            <tr>
              <th>name</th>
              <th>Start date</th>
              <th>End Date</th>
              <th>operate</th>
            </tr>
          </thead>
          <tbody>
            {filteredEvents.map(event => (
              <EventItem 
                key={event.id} 
                event={event} 
                onEdit={onEdit} 
                onDelete={onDelete} 
              />
            ))}
          </tbody>
        </table>
      ) : (
        <div className="no-events">
          {searchTerm ? 'No matching events found' : 'No event data available'}
        </div>
      )}
    </div>
  );
};

export default EventList;