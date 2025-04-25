const express = require("express");
const cors = require("cors");
const bodyParser = require("body-parser");
require("dotenv").config();

const app = express();
const db = require("./models");

app.use(cors());
app.use(bodyParser.json());

db.sequelize.sync().then(() => {
  console.log("Baza sinkronizirana.");
});

require("./routes/weather.routes")(app);

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server radi na portu ${PORT}`);
});
