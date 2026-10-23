import React from 'react';

const SearchBar = ({ searchTerm, setSearchTerm, sortOrder, setSortOrder }) => {
  return (
    <div className="search-controls">
      <input
        type="text"
        placeholder="search event..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        className="search-input"
      />
      
      <div className="sort-controls">
        <label>sort:</label>
        <select 
          value={sortOrder} 
          onChange={(e) => setSortOrder(e.target.value)}
          className="sort-select"
        >
          <option value="asc">Start date (ascending order)</option>
          <option value="desc">Start date (descending order)</option>
        </select>
      </div>
    </div>
  );
};

export default SearchBar;