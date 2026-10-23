const db = require('./db');

function Event(data) {
  return {
    name:  data.name,
    description: data.description,
    startdate: data.startdate,
    enddate: data.enddate,

    create(callback) {
      db.query(
        'INSERT INTO events (name, description, startdate, enddate) VALUES (?, ?, ?, ?)',
        [this.name, this.description, this.startdate, this.enddate],
        callback
      );
    },

    update(id, callback) {
      db.query(
        'UPDATE events SET name = ?, description = ?, startdate = ?, enddate = ?  WHERE id = ?',
        [this.name, this.description, this.startdate, this.enddate, id],
        callback
      );
    }
  };
}

Event.getAll = function (callback) {
  db.query('SELECT * FROM events', callback);
};

Event.getById = function (id, callback) {
  db.query('SELECT * FROM events WHERE id = ?', [id], callback);
};

Event.getByName = function (name, callback) {
  db.query('SELECT * FROM events WHERE name = ?', [name], callback);
};

Event.delete = function (id, callback) {
  db.query('DELETE FROM events WHERE id = ?', [id], callback);
};

module.exports = Event;