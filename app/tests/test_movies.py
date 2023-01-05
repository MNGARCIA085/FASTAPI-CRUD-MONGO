from fastapi.testclient import TestClient
from .conftest import app


"""
# create a new movie
def test_create_movie():
    with TestClient(app) as client:

        data = {
                "title": "Mad Max",
                "genres":['action','drama'],
        }

        response = client.post("/movies/", json=data)
        body = response.json()

        assert response.status_code == 201
        assert body.get("title") == "Mad Max"
        assert body.get("genres") == ['action','drama']
        #assert "_id" in body
"""



# create a new movie (invalid data)
def test_create_movie_missing_data():
    with TestClient(app) as client:

        data = {
                "genres":['action','drama'],
        }

        response = client.post("/movies/", json=data)
        body = response.json()

        assert response.status_code == 422





def test_get_all_movies(add_movie):
    with TestClient(app) as client:
        # given
        
        movie_one = add_movie('nico',['drama'])
        created_movie = app.database["movies"].find_one(
            {"title": 'nico'}
        )
        assert created_movie['title'] == 'nico'
        

        


        # when
        response = client.get("/movies/")
        data = response.json()


        # then
        assert response.status_code == 200
        data[0]['title'] = 'Don Quixote'
        #assert len(data) == 1
        









