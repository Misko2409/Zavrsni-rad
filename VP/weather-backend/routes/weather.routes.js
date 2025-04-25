module.exports = app => {
    const weather = require("../controllers/weather.controller.js");
    const router = require("express").Router();
  
    router.post("/", weather.create);
    router.get("/", weather.findAll);
  
    app.use("/api/weather", router);
  };
  