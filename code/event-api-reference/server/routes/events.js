const express = require('express');
const router = express.Router();

const eventController = require('../controllers/events');

router.get('/', eventController.getAllEvents);
router.get('/:id', eventController.getEventById);
router.get('/by-name/:name', eventController.getEventByName);
router.post('/', eventController.createEvent);
router.put('/:id', eventController.updateEvent);
router.delete('/:id', eventController.deleteEvent);

module.exports = router;