>>>log = client.post('/login', json={'email':'test@gmail.com','password':'123456'})
>>>head_a = 'Bearer '+log.get_json()['access_token']
>>>head_a
'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MTAzNzg1NjAsIm5iZiI6MTYxMDM3ODU2MCwianRpIjoiYjkxNGMyNTMtODg0NS00NzYxLThlNTQtY2JiNGYzZDhiMDU2IiwiZXhwIjoxNjEyNDUyMTYwLCJpZGVudGl0eSI6MSwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.vTDuzjKqVGbBi46ejXWnnzQEbCTZ3lTmEQq5qT0JWfE'
>>>res = client.get('/elements', headers={'Authorization':head_a})
>>>res.get_json()
[{'description': 'POST test', 'id': 1, 'ip_address': '10.0.0.1', 'name': 'Element1', 'user_id': 1}, {'description': 'POST test', 'id': 2, 'ip_address': '10.0.0.2', 'name': 'Element2', 'user_id': 1}, {'description': 'POST test 3', 'id': 3, 'ip_address': '10.0.0.3', 'name': 'Element3', 'user_id': 1}, {'description': 'POST test 23', 'id': 4, 'ip_address': '10.23.0.23', 'name': 'Element2', 'user_id': 1}, {'description': 'POST test 25', 'id': 5, 'ip_address': '10.25.0.25', 'name': 'Element25', 'user_id': 1}, {'description': 'POST test 35', 'id': 6, 'ip_address': '10.35.0.35', 'name': 'Element35', 'user_id': 1}]

