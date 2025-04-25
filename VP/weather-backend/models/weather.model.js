module.exports = (sequelize, DataTypes) => {
    const Weather = sequelize.define("weather", {
      date: {
        type: DataTypes.DATEONLY,
        allowNull: false
      },
      temperature: {
        type: DataTypes.FLOAT,
        allowNull: false
      },
      humidity: {
        type: DataTypes.FLOAT,
        allowNull: false
      },
      wind_speed: {
        type: DataTypes.FLOAT,
        allowNull: false
      }
    });
  
    return Weather;
  };
  