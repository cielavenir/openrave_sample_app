- OpenRAVE app on Django 1.7.11 (jessie)

## Endpoints

- GET /
  - robot list (HTML)
- GET /info.json
  - robot list (JSON)
- POST /add/ROBOT_NAME
  - add robot (file param (collada xml content) is mandatory)
- GET /remove/ROBOT_NAME
  - remove robot

