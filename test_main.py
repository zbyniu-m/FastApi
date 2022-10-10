from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_all_post():
    response = client.get('/blog/all')
    assert response.status_code == 200


def test_auth_error():
    response = client.post("/token",
                           data={
                               'username' : '',
                               'password': ''
                           }
                           )
    access_tokem = response.json().get('access_token')
    assert access_tokem == None
    message = response.json().get('detail')[0].get('msg')
    assert  message == 'field required'


def test_auth_success():
    response = client.post("/token",
                           data={
                               'username': 'maniek',
                               'password': 'maniek'
                           }
                           )
    access_tokem = response.json().get('access_token')
    assert access_tokem


def test_post_article():
    auth = client.post("/token",
                           data={
                               'username': 'maniek',
                               'password': 'maniek'
                           }
                           )
    access_tokem = auth.json().get('access_token')
    assert access_tokem

    response = client.post(
        "/article/",
        json={
            'title': 'Test article',
              'content': 'Test contetnt',
              'published': True,
              'creator_id': 1
        },
        headers={
            'Authorization': 'bearer ' + access_tokem
        }
    )

    assert response.status_code == 200
    assert response.json().get('title') == 'Test article'
