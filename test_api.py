from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)
def test_health(): assert client.get('/health').json()['status']=='ok'
def test_home(): assert 'Create Your Comic' in client.get('/').text
def test_generate():
 r=client.post('/generate-comic/json',json={'story_prompt':'fox adventure','character_name':'Luna','setting':'Forest','tone':'Funny','art_style':'Anime'}); assert r.status_code==200 and len(r.json()['panels'])==4
def test_image(): assert client.get('/test-image').status_code==200
