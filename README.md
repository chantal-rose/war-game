# WAR

This repository creates an application that plays the card game War. The rules for this game are followed from [here](https://bicyclecards.com/how-to-play/war/)

## Language and Framework

This application is written in Python and is created using the web framework - [Connexion](https://connexion.readthedocs.io/en/latest/). SQLAlchemy is used for database access to an SQLite backend engine.

## Running the application

### Docker container
Pull the docker image:
```
docker pull chantsdgr/war:v1
docker run -v $(pwd)/db:/app/db -d -p 8000:8000 chantsdgr/war:v1
```
Go to http://localhost:8000/play_game?player1=Alice&player2=Bob

To view the entire game simulation, copy the game ID from the response and send the following request:
http://localhost:8000/get_logs/{game_id}.

To view history of wins for a player, call:
http://localhost:8000/player/{player_name}.

You can also see the leaderboard at http://localhost:8000/ .

There is DB persistence by mounting the db/ directory to the docker container. So if the container is stopped, the data will be retained and can be viewed on the leaderboard once the new container comes back up.

### Development mode

To run the application in development mode, clone this repository and in the root directory, run:
```
python app.py
```
This will start the flask server. You can view the swagger UI at http://localhost:8000/ui/#/

Click on the /play_game endpoint, and then click "Try it out".
Enter two players names, and click on execute. Validate the response in the response body.

Copy the game id from the response and enter it in the text box in the /get_logs/{game_id} endpoint. You will be able see the logs for the associated game.

To check the history of wins for a user, try out the /player/{player_name} endpoint.

You can also access the leaderboard at http://localhost:8000/.


## Testing

All the unit tests can be found in the tests/ folder. The coverage report is created as follows:

```
coverage run -m pytest -v --disable-pytest-warnings
coverage report -m
```

![Coverage Report](images/coverage.png?raw=true "Coverage Report")



