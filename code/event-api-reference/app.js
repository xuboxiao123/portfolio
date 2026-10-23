const express = require('express');
const cors = require('cors');
const path = require('path');

const app = express();
const eventRoutes = require('./server/routes/events');

app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'public')));

app.get('/', (req, res) => {
  res.json({ message: 'Welcome to REST Events Test!' });
});

app.use('/events', eventRoutes);

const PORT = 8181;
app.listen(PORT, () => {
  console.log(`CORS enable Express web server is running on port ${PORT}`);
});
