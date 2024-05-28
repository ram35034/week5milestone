import pytest
from app1 import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Energy Consumption Monitoring System" in response.data

def test_dashboard(client):
    response = client.get('/dashboard')
    assert response.status_code == 200
    assert b"Dashboard" in response.data

def test_total_consumption(client):
    data = [
        {'source': 'Solar', 'consumption': 100, 'timestamp': '2024-05-28T12:00:00'},
        {'source': 'Wind', 'consumption': 200, 'timestamp': '2024-05-28T12:00:01'},
        {'source': 'Grid', 'consumption': 300, 'timestamp': '2024-05-28T12:00:02'}
    ]
    response = client.post('/api/total_consumption', json=data)
    assert response.status_code == 200
    assert response.json == {'total_consumption': 600}

def test_collect_data(client):
    response = client.get('/api/collect_data')
    assert response.status_code == 200
    data = response.json
    assert len(data) == 3
    assert all(item.get('source') in ['Solar', 'Wind', 'Grid'] for item in data)
    assert all('consumption' in item for item in data)
    assert all('timestamp' in item for item in data)
