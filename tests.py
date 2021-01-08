from app import *

# NOTES: First element in bd have to use id=11
#AddElements('11','10.10.0.1', 'Element1')

def test_get():
    res = client.get('/elements')
    assert res.status_code == 200
    assert len(res.get_json()) > 0
    assert res.get_json()[0]['id'] == 11

def test_post():
    data = {
        'id': 111,
        'ip_address': '10.10.1.2',
        'name': 'New Element 2',
        'description': 'POST route test'
    }
    res = client.post('/elements', json=data)
    assert res.status_code == 200
    assert res.get_json()['name'] == data['name']

def test_put():
    res = client.put('/elements/111', json={'ip_address': '10.80.1.2'})
    assert res.status_code == 200
    assert NW_Elements.query.get(111).ip_address == '10.80.1.2'

def test_delete():
    res = client.delete('/elements/111')
    assert res.status_code == 204
    assert NW_Elements.query.get(111) is None

