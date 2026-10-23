const Event = require('../models/Events');

exports.getAllEvents = (req, res) => {
  Event.getAll((error, results) => {
    if (error) {
      return res.status(500).send({ message: error.message || 'Error occurred while retrieving events' });
    }
    res.send(results);
  });
};

exports.getEventById = (req, res) => {
  Event.getById(req.params.id, (error, results) => {
    if (error) {
      return res.status(500).send({ message: error.message || 'Error occurred while retrieving the events' });
    }
    res.send(results);
  });
};

exports.getEventByName = (req, res) => {
  Event.getByName(req.params.name, (error, results) => {
    if (error) {
      return res.status(500).send({ message: error.message || 'Error occurred while retrieving the events' });
    }
    res.send(results);
  });
};

exports.createEvent = (req, res) => {
  if (!req.body || !req.body.name || !req.body.description || !req.body.startdate || !req.body.enddate) {
    return res.status(400).send({ message: 'Content cannot be empty or missing fields' });
  }

  const newEvent = Event(req.body);

  newEvent.create((error, results) => {
    if (error) {
      return res.status(500).send({ message: error.message || 'Error occurred while creating the event' });
    }
    res.send({ id: results.insertId, ...req.body });
  });
};

exports.updateEvent = (req, res) => {
  if (!req.body || !req.body.name || !req.body.description || !req.body.startdate || !req.body.enddate) {
    return res.status(400).send({ message: 'Content cannot be empty or missing fields' });
  }

  const updatedEvent = Event(req.body);

  updatedEvent.update(req.params.id, (error, results) => {
    if (error) {
      return res.status(500).send({ message: error.message || 'Error occurred while updating the event' });
    }
    res.send({ id: req.params.id, ...req.body });
  });
};

exports.deleteEvent = (req, res) => {
  Event.delete(req.params.id, (error, results) => {
    if (error) {
      return res.status(500).send({ message: error.message || 'Error occurred while deleting the event' });
    }
    res.send(results);
  });
};