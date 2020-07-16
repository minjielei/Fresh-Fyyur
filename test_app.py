import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Venue, Artist, Show

class FyyurTestCase(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "fyyur_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.artist = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IktTdmNLM0RiRmRYXzBHdjROTjd6YyJ9.eyJpc3MiOiJodHRwczovL2FtYS1mc25kLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWY3OWVjYmExNWI3YjAwMTM2MWE5OGYiLCJhdWQiOiJmeXl1ciIsImlhdCI6MTU5NDkyNDUzOCwiZXhwIjoxNTk0OTMxNzM4LCJhenAiOiI5SzY4cDFlNnNWNFZiUXQ2WFV1NHZLU3AxckhoY3ZyaCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsicG9zdDphcnRpc3RzIiwicG9zdDpzaG93cyJdfQ.p3DurR5Fw50qjcNVNn9zv45KpL6AxVMsth-zy9mYmqIzixigB_q5HAi-yBV1ufjuXfbbkUpnCYW4JmouoTjLgahEJV4Si65jU_aNlQiS1OlJtniVPU_DiPq4wRexApPznz192adyFYvMr7ocdGJybIZuCcM3UiK5MZG7bRaT5d3fLx_3IF67kkirxIv7mn4ujQ7-RhFfUgURp7AA6263qhiNtLS05RbSIUb3sWbQeA4iIw0JTLJcVrc-Nt-rcrKy2yGjO0mtIgzE06wNKb41giGqQ5SRF0tdhQwgH520epd5bSsuflu4D7hNShX_jp-g1BSGoWQv9L7Ufgt1y0VFUQ"
        self.venue_owner = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IktTdmNLM0RiRmRYXzBHdjROTjd6YyJ9.eyJpc3MiOiJodHRwczovL2FtYS1mc25kLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDExMTg5NzAwNDk3NjgzMjg2Mzg5MyIsImF1ZCI6WyJmeXl1ciIsImh0dHBzOi8vYW1hLWZzbmQudXMuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTU5NDkyNDk1NCwiZXhwIjoxNTk0OTMyMTU0LCJhenAiOiI5SzY4cDFlNnNWNFZiUXQ2WFV1NHZLU3AxckhoY3ZyaCIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJwb3N0OnNob3dzIiwicG9zdDp2ZW51ZXMiXX0.Z0Z4A8EZmfFN5qmRrz2c3kiCfcul5iWWT_wG5dqMZPzBGIB8qVEL18NXvQZkshgVRJOIurOubEIbZVPdMkeAoZZymJLgcLiO7AtJb7AxUNrlP53S8nOddaZJVybND9b_C2z_5I1aMtaoaXQMX3pDY_m8uz_7mnH0BEaDKK-3NcoTIgfCaxWJUZ8zrMxNMb0XK6rv0D3xYpJnyN8wLzB2CuB2Wchy09mW7GM6qshXaF_mBnfKj2EpjopjCBdhpLb329RNP4SUVvhoMXH_TCc1Pe10I7Pzlf_m5FeajPzc1zSfnbvov-7uR-tdhVa_oJMM6KIz2sQA3DEi7jwT9FE6lA"
        self.administrator = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IktTdmNLM0RiRmRYXzBHdjROTjd6YyJ9.eyJpc3MiOiJodHRwczovL2FtYS1mc25kLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDEwMzAzMDUzNjMxNTEzNDM5MzE2OSIsImF1ZCI6WyJmeXl1ciIsImh0dHBzOi8vYW1hLWZzbmQudXMuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTU5NDkyNTA2OCwiZXhwIjoxNTk0OTMyMjY4LCJhenAiOiI5SzY4cDFlNnNWNFZiUXQ2WFV1NHZLU3AxckhoY3ZyaCIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YXJ0aXN0cyIsImRlbGV0ZTp2ZW51ZXMiLCJwYXRjaDphcnRpc3RzIiwicGF0Y2g6dmVudWVzIl19.vc_trB3EqB57FYOWdLkutpImqoAYRq_-r4JfM0txm8d5BDSnoYzct8patwriXpFHxBfYBkTKUQGapW1lfS08oYZfH-nZ_7C_kBY6mjzGnAjVWoXAdST9pXyjf86AKhHZXeiHf06jBZ2iGck_CojK52Yx7BCKabnOE4l2FB_iaQni61YG2XA2VansWUYt2W2GDI6S3QhxUXndfRxptKDIG_TKSLiywOPCTaIdS_Fqs68ghTf06MV_p-baFt8CQrLqyfBpSkzQWkpbbC65l_epnWGL9ffLCB2IfI02sjx0oXFHgmUnSNrBr7kj0lOLjutsiFIk6CF_PxNQIKsUXFwhzg"

        self.new_venue = {
            "name": "The East Hop",
            "genres": ["Jazz", "Folk"],
            "address": "1015 Folsom Street",
            "city": "New York",
            "state": "NY",
            "phone": "523-123-1234",
            "website": "https://www.themusicalhop.com",
            "facebook_link": "https://www.facebook.com/TheMusicalHop",
            "seeking_talent": True,
            "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
            "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
        }

        self.new_venue_invalid = {
            "name": "The East Hop",
            "genres": ["Jazz", "Folk"],
            "address": "1015 Folsom Street",
            "city": "New York",
            "state": "NY",
            "phone": "523-123",
            "website": "https://www.themusicalhop.com",
            "facebook_link": "https://www.facebook.com/TheMusicalHop",
            "seeking_talent": True,
            "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
            "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
        }

        self.new_artist = {
            "name": "New Petals",
            "genres": ["Jazz"],
            "city": "San Francisco",
            "state": "CA",
            "phone": "326-123-5000",
            "website": "https://www.gunsnpetalsband.com",
            "facebook_link": "https://www.facebook.com/GunsNPetals",
            "seeking_venue": True,
            "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
            "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
        }

        self.new_artist_invalid = {
            "name": "New Petals",
            "genres": ["Jazz"],
            "city": "San Francisco",
            "state": "CA",
            "phone": "326-123-5000",
            "website": "https://www.gunsnpetalsband.com",
            "facebook_link": "https://www.facebook.com/GunsNPetals",
            "seeking_venue": True,
            "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
            "image_link": "httimages.unsplash.com/"
        }

        self.new_show = {
            "start_time": "2019-05-21 21:30:00",
            "artist_id": 2,
            "venue_id": 2
        }

        self.new_show_invalid = {
            "start_time": "2019-05-21 21:30:00",
            "artist_id": 20,
            "venue_id": 2
        }

    def tearDown(self):
        """execute after each test"""
        pass

    def test_get_venues(self):
        res = self.client().get('/api/venues')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['venues'])
        self.assertTrue(data['total_venues'])

    def test_get_artists(self):
        res = self.client().get('/api/artists')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['artists'])
        self.assertTrue(data['total_artists'])

    def test_get_shows(self):
        res = self.client().get('/api/shows')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['shows'])
        self.assertTrue(data['total_shows'])

    def test_get_venue_by_id(self):
        res = self.client().get('api/venues/2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['venue'])

    def test_404_invalid_venue_id(self):
        res = self.client().get('api/venues/100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_get_artist_by_id(self):
        res = self.client().get('api/artists/2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['artist'])

    def test_404_invalid_artist_id(self):
        res = self.client().get('api/artists/100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_search_venue_by_name(self):
        res = self.client().post('/api/venues/search', json={'searchTerm': 'bar'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['venues']), 1)
        self.assertEqual(data['total_venues'], 1)

    def test_search_venue_by_name_no_results(self):
        res = self.client().post('/api/venues/search', json={'searchTerm': 'mug'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['venues']), 0)
        self.assertEqual(data['total_venues'], 0)

    def test_search_artist_by_name(self):
        res = self.client().post('/api/artists/search', json={'searchTerm': 'band'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['artists']), 1)
        self.assertEqual(data['total_artists'], 1)

    def test_search_artist_by_name_no_results(self):
        res = self.client().post('/api/artists/search', json={'searchTerm': 'mug'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['artists']), 0)
        self.assertEqual(data['total_artists'], 0)

    def test_create_new_venue(self):
        res = self.client().post('/api/venues/create', headers={"Authorization": "Bearer {}".format(self.venue_owner)}, json=self.new_venue)
        data = json.loads(res.data)

        venue = Venue.query.filter(Venue.name == self.new_venue['name']).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(venue.city, self.new_venue['city'])
        self.assertEqual(venue.state, self.new_venue['state'])
        self.assertEqual(venue.address, self.new_venue['address'])
        self.assertEqual(venue.genres, self.new_venue['genres'])
        self.assertEqual(venue.phone, self.new_venue['phone'])
        self.assertEqual(venue.website, self.new_venue['website'])
        self.assertEqual(venue.image_link, self.new_venue['image_link'])
        self.assertEqual(venue.facebook_link, self.new_venue['facebook_link'])
        self.assertEqual(venue.seeking_talent, self.new_venue['seeking_talent'])
        self.assertEqual(venue.seeking_description, self.new_venue['seeking_description'])

    def test_create_venue_with_invalid_phone(self):
        res = self.client().post('/api/venues/create', headers={"Authorization": "Bearer {}".format(self.venue_owner)}, json=self.new_venue_invalid)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Bad request')

    def test_401_create_new_venue_without_permission(self):
        res = self.client().post('/api/venues/create', headers={"Authorization": "Bearer {}".format(self.artist)}, json=self.new_venue_invalid)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], "unathorized")

    def test_create_new_artist(self):
        res = self.client().post('/api/artists/create', headers={"Authorization": "Bearer {}".format(self.artist)}, json=self.new_artist)
        data = json.loads(res.data)

        artist = Artist.query.filter(Artist.name == self.new_artist['name']).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(artist.city, self.new_artist['city'])
        self.assertEqual(artist.state, self.new_artist['state'])
        self.assertEqual(artist.genres, self.new_artist['genres'])
        self.assertEqual(artist.phone, self.new_artist['phone'])
        self.assertEqual(artist.website, self.new_artist['website'])
        self.assertEqual(artist.image_link, self.new_artist['image_link'])
        self.assertEqual(artist.facebook_link, self.new_artist['facebook_link'])
        self.assertEqual(artist.seeking_venue, self.new_artist['seeking_venue'])
        self.assertEqual(artist.seeking_description, self.new_artist['seeking_description'])

    def test_create_artist_with_invalid_url(self):
        res = self.client().post('/api/artists/create', headers={"Authorization": "Bearer {}".format(self.artist)}, json=self.new_artist_invalid)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Bad request')

    def test_create_show(self):
        res = self.client().post('/api/shows/create', headers={"Authorization": "Bearer {}".format(self.artist)}, json=self.new_show)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['venue'])
        self.assertTrue(data['artist'])
        self.assertTrue(data['venue'])

    def test_404_create_show_with_invalid_id(self):
        res = self.client().post('/api/shows/create', headers={"Authorization": "Bearer {}".format(self.venue_owner)}, json=self.new_show_invalid)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_401_create_new_show_without_permission(self):
        res = self.client().post('/api/shows/create', headers={"Authorization": "Bearer {}".format(self.administrator)}, json=self.new_venue_invalid)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], "unathorized")

    def test_edit_venue_by_id(self):
        res = self.client().patch('/api/venues/2/edit', headers={"Authorization": "Bearer {}".format(self.administrator)}, json=self.new_venue)
        data = json.loads(res.data)

        venue = Venue.query.filter(Venue.id == 2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(venue.city, self.new_venue['city'])
        self.assertEqual(venue.state, self.new_venue['state'])
        self.assertEqual(venue.address, self.new_venue['address'])
        self.assertEqual(venue.genres, self.new_venue['genres'])
        self.assertEqual(venue.phone, self.new_venue['phone'])
        self.assertEqual(venue.website, self.new_venue['website'])
        self.assertEqual(venue.image_link, self.new_venue['image_link'])
        self.assertEqual(venue.facebook_link, self.new_venue['facebook_link'])
        self.assertEqual(venue.seeking_talent, self.new_venue['seeking_talent'])
        self.assertEqual(venue.seeking_description, self.new_venue['seeking_description'])

    def test_edit_venue_with_invalid_id(self):
        res = self.client().patch('/api/venues/200/edit', headers={"Authorization": "Bearer {}".format(self.administrator)}, json=self.new_venue)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_401_edit_venue_without_permission(self):
        res = self.client().patch('/api/venues/2/edit', headers={"Authorization": "Bearer {}".format(self.venue_owner)}, json=self.new_venue)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], "unathorized")

    def test_edit_artist_by_id(self):
        res = self.client().patch('/api/artists/1/edit', headers={"Authorization": "Bearer {}".format(self.administrator)}, json=self.new_artist)
        data = json.loads(res.data)

        artist = Artist.query.filter(Artist.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(artist.city, self.new_artist['city'])
        self.assertEqual(artist.state, self.new_artist['state'])
        self.assertEqual(artist.genres, self.new_artist['genres'])
        self.assertEqual(artist.phone, self.new_artist['phone'])
        self.assertEqual(artist.website, self.new_artist['website'])
        self.assertEqual(artist.image_link, self.new_artist['image_link'])
        self.assertEqual(artist.facebook_link, self.new_artist['facebook_link'])
        self.assertEqual(artist.seeking_venue, self.new_artist['seeking_venue'])
        self.assertEqual(artist.seeking_description, self.new_artist['seeking_description'])

    def test_edit_artist_with_invalid_id(self):
        res = self.client().patch('/api/artists/100/edit', headers={"Authorization": "Bearer {}".format(self.administrator)}, json=self.new_artist)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_delete_venue_by_id(self):
        res = self.client().delete('/api/venues/5', headers={"Authorization": "Bearer {}".format(self.administrator)})
        data = json.loads(res.data)

        venue = Venue.query.filter(Venue.id==5).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['delete'])
        self.assertEqual(venue, None)

    def test_delete_venue_invalid_id(self):
        res = self.client().delete('/api/venues/200', headers={"Authorization": "Bearer {}".format(self.administrator)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_delete_artist_by_id(self):
        res = self.client().delete('/api/artists/4', headers={"Authorization": "Bearer {}".format(self.administrator)})
        data = json.loads(res.data)

        artist = Artist.query.filter(Artist.id==4).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['delete'])
        self.assertEqual(artist, None)

    def test_delete_artist_invalid_id(self):
        res = self.client().delete('/api/artists/200', headers={"Authorization": "Bearer {}".format(self.administrator)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_401_delete_artist_without_permission(self):
        res = self.client().delete('/api/artists/4', headers={"Authorization": "Bearer {}".format(self.artist)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], "unathorized")

if __name__ == "__main__":
    unittest.main()