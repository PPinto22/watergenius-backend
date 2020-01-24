# WaterGenius (Backend)

Homepage: https://watergenius.herokuapp.com

This repository contains the source code for the backend of WaterGenius. WaterGenius was an academic project which aimed at minimizing the amount of water utilized in the irrigation of lands. For that purpose, the system applies an optimization algorithm that calculates the minimum amount of water necessary to keep the plants healthy, according to the humidity of the soil, the type of plants, and the weather forecast.

![High Level Architecture](/img/high-level-architecture.png)

The backend is implemented in Python, with Django. Its purpose is to control the business logic of the application and to interact with the database, while exposing its functionality, via a REST API, to the other sub-systems of WaterGenius (frontend and embedded systems). 

The backend holds information about the users and their lands and spaces, the embedded systems installed on-site, the humidity sensors and their reads, and the irrigation plans and time restrictions:

![Database Schema](/img/dbschema.png)