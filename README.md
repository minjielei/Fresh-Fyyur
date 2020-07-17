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
The following roles are defined for the API with different permissions

Artist: (JWT: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IktTdmNLM0RiRmRYXzBHdjROTjd6YyJ9.eyJpc3MiOiJodHRwczovL2FtYS1mc25kLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWY3OWVjYmExNWI3YjAwMTM2MWE5OGYiLCJhdWQiOiJmeXl1ciIsImlhdCI6MTU5NDk0MzA0NCwiZXhwIjoxNTk1MDI5NDQ0LCJhenAiOiI5SzY4cDFlNnNWNFZiUXQ2WFV1NHZLU3AxckhoY3ZyaCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsicG9zdDphcnRpc3RzIiwicG9zdDpzaG93cyJdfQ.1stIoc_CFmosDm8M9ZR6F99hiOA9gdBS3gPgCvzzY6oDr9j4wO-0KfFFMET3PHLxWScArUtTTdf8WOvySPPP3z4QZGYlcvursWNw53NLk4BKu3lDN2nx5Ezxe0SI6DJbAIpckHvIPJhzMzbQKBdxMXEIWVr55XESScLtgj14YYTdKm5uLn9t_TKpRuBYEAFA9KMLy0HygyWd3EIE5K7cjF4FQujwkl9nclFufrdaW969l82FlW2cs3oBMZs7ok0cYpy_oE3QFIFN_z7dWlzyI61DEH2lE6s9lzvNUL9pv1_k68bewY-q8dqvt_S_l1UUsUXelBweBn-lgG0LaiyZ3Q)
* post:artists
* post:shows

Venue Owner: (JWT: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IktTdmNLM0RiRmRYXzBHdjROTjd6YyJ9.eyJpc3MiOiJodHRwczovL2FtYS1mc25kLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDExMTg5NzAwNDk3NjgzMjg2Mzg5MyIsImF1ZCI6WyJmeXl1ciIsImh0dHBzOi8vYW1hLWZzbmQudXMuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTU5NDk0MzIyMiwiZXhwIjoxNTk1MDI5NjIyLCJhenAiOiI5SzY4cDFlNnNWNFZiUXQ2WFV1NHZLU3AxckhoY3ZyaCIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJwb3N0OnNob3dzIiwicG9zdDp2ZW51ZXMiXX0.cDGIf9WjHpOdHLNtmKiIstJsA5KKwvhDMGCrpuoQgpQZJhDjHzfyTEHnq1Q_diKnk8573Gcm-8udaau2JJXHVyfWZQAsHV0Qr_61bkO4tbIqi7vQ96ymMVrUG2IR-ZICCRJ2FNeunzOezrUkOtKICiT-an5FJmbQHYGFD6UskcsQe_azAqfrp4u4J0hzpje2rYA06AGQT_uH5IfLVeQ_DDPZ4W6pWOOKmcUQNxHpxbWDbhAPS9zO2x6DK6IM4gdHXAAle_vS8y2ChhW8CCSkzFjR2rozRwUOoI1QFbmHipuYb6g5Rmy1C7zasI66gVxl0BELOnIq1ZYa1NJnZxr1qQ)
* post:venues
* post:shows

Administrator: (JWT: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IktTdmNLM0RiRmRYXzBHdjROTjd6YyJ9.eyJpc3MiOiJodHRwczovL2FtYS1mc25kLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDEwMzAzMDUzNjMxNTEzNDM5MzE2OSIsImF1ZCI6WyJmeXl1ciIsImh0dHBzOi8vYW1hLWZzbmQudXMuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTU5NDk0MzMwNSwiZXhwIjoxNTk1MDI5NzA1LCJhenAiOiI5SzY4cDFlNnNWNFZiUXQ2WFV1NHZLU3AxckhoY3ZyaCIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YXJ0aXN0cyIsImRlbGV0ZTp2ZW51ZXMiLCJwYXRjaDphcnRpc3RzIiwicGF0Y2g6dmVudWVzIl19.XVdhHD2RllqHit1TxYsDW2NE2fcmAZnN2sFto6Mgb2bds-6d34DBa4ZD1zzsdTRZaUWA80DwwusQZlZkG3Kvgaauh45fba0JuVdcKr-UdMNZlc3qsL4oRHA4A4HY55sBEuPgPPEyYddF9SmeBX0bwoTWUKaN3yH6A87IGENmRYnbB8u8aEdt13tRj5d8pJPDsq5LH4LVCmI7_vTE5kfuSUmBre9JobdR0yx7PaoIG820F6hAljXjNqbKTCF3TJZ9BAqzVZ4RJZaymY0ZNZhKoNe7a-SkFpomvTKDmCm3ko_JKk1Ptbv35W8F6MG-MMFOkApkubWeK6z6A1Um1OGrZA)
* patch:artists
* patch:venues
* delete:artists
* delete:venues

Other actions for getting and searching venue, artist, and show information does not require RBAC authorization. 

## Deployment
The application is deployed using Heroku and live at https://fresh-fyyur.herokuapp.com

## Author
Minjie Lei

## Acknowledgement
Built as part of Udacity's [Full Stack Web Developer Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd0044).