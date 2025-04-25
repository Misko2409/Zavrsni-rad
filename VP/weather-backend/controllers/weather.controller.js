const db = require("../models");
const Weather = db.weather;

exports.create = async (req, res) => {
  try {
    const { date, temperature, humidity, wind_speed } = req.body;
    const data = await Weather.create({ date, temperature, humidity, wind_speed });
    res.status(201).json(data);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

exports.findAll = async (req, res) => {
  try {
    const data = await Weather.findAll();
    res.status(200).json(data);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};
