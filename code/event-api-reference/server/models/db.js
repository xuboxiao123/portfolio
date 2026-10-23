const dbConfig = require("../config/db.config.js");
const mysql = require('mysql2');

const db = mysql.createConnection(dbConfig);

db.connect(err => {
  if (err) {
    throw err;
  }
  console.log('Successfully connected to the database');
});

module.exports = db;
