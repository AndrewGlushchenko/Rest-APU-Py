




# You can make tests nn Python console:
# from app import client
# res = client.put('/tutorials/2', json = {'description': 'Put routes update'}) --- PUT test
# res = client.delete('/tutorials/2') --- DELETE test
# res = client.post('/tutorials', json= {'id':'3','title':'video2',"description":'POST test'}) --- POST test
# res = client.get('/tutorials') --- GET test
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