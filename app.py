from typing import Optional, Dict

from flask import Flask, jsonify, request

app = Flask(__name__)

client = app.test_client()

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


@app.route('/tutorials', methods=['GET'])
def get_list():
    return jsonify(tutorials)


@app.route('/tutorials', methods=['POST'])
def update_list():
    new_one = request.json
    tutorials.append(new_one)
    return jsonify(tutorials)


@app.route('/tutorials/<int:tutorial_id>', methods=['PUT'])
def update_tutorial(tutorial_id):
    item = next((x for x in tutorials if x['id'] == str(tutorial_id)), None)
    params = request.json
    if not item:
        return {'message': 'No tutorials with this id'}, 400
    item.update(params)
    return item

@app.route('/tutorials/<int:tutorial_id>', methods=['DELETE'])
def delete_tutorial(tutorial_id):
    idx, _ = next((x for x in enumerate(tutorials) if x[1]['id'] == str(tutorial_id)), (None, None))

    if not idx:
        return {'message': 'No tutorials with this id'}, 400
    tutorials.pop(idx)
    return '', 204

if __name__ == '__main__':
    app.run()
# from app import client
# res = client.put('/tutorials/2', json = {'description': 'Put routes update'}) --- PUT test
# res = client.delete('/tutorials/2') --- DELETE test
# res = client.post('/tutorials', json= {'id':'3','title':'video2',"description":'POST test'}) --- POST test
# res = client.get('/tutorials') --- GET test
# res.get_json()