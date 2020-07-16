# Fresh-Fyyur
Fresh Fyyur is a musical venue and artist booking site that facilitates the discovery and bookings of shows between local performing artists and venues. At Fresh Fyuur, artists and venue owners can list their profiles and create shows for everyone to discover!

![Fresh Fyyur](./fyyur.png)

All backend code of the project follows the [PEP8 style guideline](https://www.python.org/dev/peps/pep-0008/).
## Getting Started
Developers using this project should have python3 and pip installed on their local environment. Install all dependencies by:
```bash
pip install -r requirements.txt
```

### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Virtual Environment 

It is recommended to work within a vritual environment to keep dependencies for different projects organized and separated.

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql fyyur < fyyur.psql
```

### Running the server

First ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

### Testing
To run the tests, run
```
dropdb fyyur_test
createdb fyyur_test
psql fyyur_test < fyyur.psql
python test_app.py
```

## API Reference
see [Fresh Fyyur API Reference](./API_Reference.md)

## Deployment
The application is deployed using Heroku and live at https://fresh-fyyur.herokuapp.com

## Author
Minjie Lei

## Acknowledgement
Built as part of Udacity's [Full Stack Web Developer Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd0044).