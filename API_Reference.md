# Fresh Fyyur API Reference

## Getting Started
* Base URL: The app is hosted via Heroku at the location `https://fresh-fyyur.herokuapp.com
* Authentication: RBAC authorization policies are enforced for this API with the following roles and permissions:
Artist:
* post:artists
* post:shows
Venue Owner:
* post:venues
* post:shows
Administrator
* patch:artists
* patch:venues
* delete:artists
* delete:venues
Other endpoints for getting and searching venue, artist, and show information does not require RBAC authorization. 

## Error Handling
Errors are returned as JSON objects in the following format
```python
{
    "success": False,
    "error": 404,
    "message": "resource not found"
}
```

The following error types are returned by the API when requests fail:
* 401: Unauthorized
* 404: Resource not found
* 422: Not Processible

## Endpoints
**GET /api/venues**
* General:
    - Returns a list of venues, success value, and total number of venues
* Sample: `curl https://fresh-fyyur.herokuapp.com/api/venues`
```python
{
  "success": true,
  "total_venues": 3,
  "venues": [
    {
      "genres": [
        "Classical",
        "Folk",
        "Jazz",
        "Reggae"
      ],
      "id": 2,
      "name": "The Musical Hop"
    },
    {
      "genres": [
        "Classical",
        "Hip-Hop",
        "R&B"
      ],
      "id": 3,
      "name": "The Dueling Pianos Bar"
    },
    {
      "genres": [
        "Classical",
        "Folk",
        "Jazz",
        "Rock n Roll"
      ],
      "id": 4,
      "name": "Park Square Live Music & Coffee"
    }
  ]
}
```

**GET /api/artists**
* General:
    - Returns a list of artists, success value, and total number of artists
* Sample: `curl https://fresh-fyyur.herokuapp.com/api/artists`
```python
{
  "artists": [
    {
      "genres": [
        "Rock n Roll"
      ],
      "id": 1,
      "name": "Guns N Petals"
    },
    {
      "genres": [
        "Jazz"
      ],
      "id": 2,
      "name": "Matt Quevedo"
    },
    {
      "genres": [
        "Classical",
        "Jazz"
      ],
      "id": 3,
      "name": "The Wild Sax Band"
    }
  ],
  "success": true,
  "total_artists": 3
}
```

**GET /api/shows**
* General:
    - Returns a list of shows, success value, and total number of shows
* Sample: `curl https://fresh-fyyur.herokuapp.com/api/shows`
```python
{
  "shows": [
    {
      "artist_id": 1,
      "id": 2,
      "start_time": "Tue, 21 May 2019 21:30:00 GMT",
      "venue_id": 2
    },
    {
      "artist_id": 2,
      "id": 3,
      "start_time": "Sat, 15 Jun 2019 23:00:00 GMT",
      "venue_id": 4
    },
    {
      "artist_id": 3,
      "id": 4,
      "start_time": "Sun, 01 Apr 2035 20:00:00 GMT",
      "venue_id": 4
    },
    {
      "artist_id": 3,
      "id": 5,
      "start_time": "Sun, 08 Apr 2035 20:00:00 GMT",
      "venue_id": 4
    },
    {
      "artist_id": 3,
      "id": 6,
      "start_time": "Sun, 15 Apr 2035 20:00:00 GMT",
      "venue_id": 4
    }
  ],
  "success": true,
  "total_shows": 5
}
```

**GET /api/venues/2**
* General:
    - Returns the venue with the specific id and success value
* Sample: `curl https://fresh-fyyur.herokuapp.com/api/venues/2`
```python
{
  "success": true,
  "venue": {
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "genres": [
      "Classical",
      "Folk",
      "Jazz",
      "Reggae"
    ],
    "id": 2,
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    "name": "The Musical Hop",
    "phone": "123-123-1234",
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "seeking_talent": true,
    "state": "CA",
    "website": "https://www.themusicalhop.com"
  }
}
```

**GET /api/artists/2**
* General:
    - Returns the artist with the specific id and success value
* Sample: `curl https://fresh-fyyur.herokuapp.com/api/artists/2`
```python
{
  "artist": {
    "city": "New York",
    "facebook_link": "https://www.facebook.com/mattquevedo923251523",
    "genres": [
      "Jazz"
    ],
    "id": 2,
    "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    "name": "Matt Quevedo",
    "phone": "300-400-5000",
    "seeking_description": "",
    "seeking_venue": false,
    "state": "NY",
    "website": "https://www.facebook.com/mattquevedo923251523"
  },
  "success": true
}
```

**Post /api/venues/search**
* General:
    - Returns the venues whose name match the search term, the total number of such venues, and the success value
* Sample: `curl -X POST https://fresh-fyyur.herokuapp.com/api/venues/search --header Content-Type: application/json --data-raw {"searchTerm": "bar"}`
```python
{
  "success": true,
  "total_venues": 1,
  "venues": [
    {
      "genres": [
        "Classical",
        "Hip-Hop",
        "R&B"
      ],
      "id": 3,
      "name": "The Dueling Pianos Bar"
    }
  ]
}
```

**Post /api/artists/search**
* General:
    - Returns the artists whose name match the search term, the total number of such artists, and the success value
* Sample: `curl -X POST https://fresh-fyyur.herokuapp.com/api/artists/search --header Content-Type: application/json --data-raw {"searchTerm": "gun"}`
```python
{
  "artists": [
    {
      "genres": [
        "Rock n Roll"
      ],
      "id": 1,
      "name": "Guns N Petals"
    }
  ],
  "success": true,
  "total_artists": 1
}
```

**Post /api/venues/create**
* General:
    - Returns the success value, artists, and total number of venues after creation
* Sample: `curl -X POST 'https://fresh-fyyur.herokuapp.com/api/venues/create' --header 'Content-Type: application/json' --header 'Authorization: Bearer {{venue_owner_token}} --data-raw {{venue_data}}`
```python
{
  "success": true,
  "total_venues": 4,
  "venues": [
    {
      "genres": [
        "Classical",
        "Folk",
        "Jazz",
        "Reggae"
      ],
      "id": 2,
      "name": "The Musical Hop"
    },
    {
      "genres": [
        "Classical",
        "Hip-Hop",
        "R&B"
      ],
      "id": 3,
      "name": "The Dueling Pianos Bar"
    },
    {
      "genres": [
        "Classical",
        "Folk",
        "Jazz",
        "Rock n Roll"
      ],
      "id": 4,
      "name": "Park Square Live Music & Coffee"
    },
    {
      "genres": [
        "Jazz",
        "Folk"
      ],
      "id": 5,
      "name": "The East Hop"
    }
  ]
}
```

**Post /api/artists/create**
* General:
    - Returns the success value, artists, and total number of artists after creation
* Sample: `curl -X POST 'https://fresh-fyyur.herokuapp.com/api/artists/create' --header 'Content-Type: application/json' --header 'Authorization: Beare{artist_token}} --data-raw {{artist_data}}`
```python
{
  "artists": [
    {
      "genres": [
        "Rock n Roll"
      ],
      "id": 1,
      "name": "Guns N Petals"
    },
    {
      "genres": [
        "Jazz"
      ],
      "id": 2,
      "name": "Matt Quevedo"
    },
    {
      "genres": [
        "Classical",
        "Jazz"
      ],
      "id": 3,
      "name": "The Wild Sax Band"
    },
    {
      "genres": [
        "Jazz"
      ],
      "id": 4,
      "name": "New Petals"
    }
  ],
  "success": true,
  "total_artists": 4
}
```

**Patch /api/venues/2/edit**
* General:
    - Returns the success value, and the edited venue
* Sample: `curl -X PATCH 'https://fresh-fyyur.herokuapp.com/api/venues/2/edit' --header 'Content-Type: application/json' --header 'Authorization: Bearer {{administrator_token}} --data-raw {{venue_data}}`
```python
{
  "success": true,
  "venue": {
    "address": "1015 Folsom Street",
    "city": "New York",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "genres": [
      "Jazz",
      "Folk"
    ],
    "id": 2,
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    "name": "The East Hop",
    "phone": "523-123-1234",
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "seeking_talent": true,
    "state": "NY",
    "website": "https://www.themusicalhop.com"
  }
}
```

**Patch /api/artists/1/edit**
* General:
    - Returns the success value, and the edited artist
* Sample: `curl -X PATCH 'https://fresh-fyyur.herokuapp.com/api/artists/1/edit' --header 'Content-Type: application/json' --header 'Authorization: Beare{adiministrator_token}} --data-raw {{artist_data}}`
```python
{
  "artist": {
    "city": "New York",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "genres": [
      "Jazz",
      "Folk"
    ],
    "id": 1,
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    "name": "The East Hop",
    "phone": "523-123-1234",
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "seeking_venue": false,
    "state": "NY",
    "website": "https://www.themusicalhop.com"
  },
  "success": true
}
```

**Delete /api/venues/5**
* General:
    - Returns the success value, and the deleted venue
* Sample: `curl -X DELETE 'https://fresh-fyyur.herokuapp.com/api/venues/5' --header 'Authorization: Bearer {{administrator_token}}`
```python
{
  "delete": {
    "genres": [
      "Jazz",
      "Folk"
    ],
    "id": 5,
    "name": "The East Hop"
  },
  "success": true
}
```

**Delete /api/artists/4**
* General:
    - Returns the success value, and the deleted artist
* Sample: `curl -X DELETE 'https://fresh-fyyur.herokuapp.com/api/artists/4' --header 'Authorization: Bearer {{administrator_token}}`
```python
{
  "delete": {
    "genres": [
      "Jazz"
    ],
    "id": 4,
    "name": "New Petals"
  },
  "success": true
}
```

