
# You can make tests nn Python console:
# from app import client
# res = client.put('/elements/2', json = {'description': 'Put routes update'}) --- PUT test
# res = client.delete('/elements/2') --- DELETE test
# res = client.post('/elements', json= {'id':'3','title':'video2',"description":'POST test'}) --- POST test
# res = client.get('/elements') --- GET test
# res.get_json()

#item = next((x for x in tutorials if x['id'] == str(tutorial_id)), None)



#AddElements('11','10.10.0.1', 'Element1')
#AddElements('12','10.10.0.2', 'Element2')
#AddElements('13','10.10.0.3', 'Element3')
#AddElements('14','10.10.0.4', 'Element4')
#AddElements('15','10.10.0.5', 'Element5')


tutorials = [
    {
        'id': '1',
        'title': 'Video Intro',
        'description': 'GET, POST routes'
    },
    {
        'id': '2',
        'title': 'Video More',
        'description': 'PUT, DELETE rotes'
    }
]

res = client.post('/register', json={'name':'testuser', 'email':'test@gmail.com','password':'123456'})

log = client.post('/login', json={'email':'test@gmail.com','password':'123456'})
head_a = 'Bearer '+log.get_json()['access_token']
log.get_json()
res = client.get('/elements', headers={'Authorization':'Bearer  '})
res.get_json()
res = client.post('/elements', json= {'id':'21','name':'Element21', 'ip_address':'10.21.0.21', 'description':'POST test'}, headers={'Authorization': head_a})

