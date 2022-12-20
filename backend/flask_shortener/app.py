from flask import Flask, request, abort, jsonify
import bson
import db
from pymongo import ReturnDocument


def create_entry(slug, ios, android, web):
    global existing_keys
    if slug == "":
        slug = str(bson.objectid.ObjectId())
        while slug in existing_keys:
            slug = str(bson.objectid.ObjectId())
        existing_keys.append(slug)
    else:
        if slug in existing_keys:
            abort(422)
    # print("slug:",slug,'\nios:',ios,'\nandroid:',android,'\nweb:', web)
    return {'slug': slug,
            'ios':{
                'primary': ios['primary'],
                'fallback': ios['fallback']
            },
            'android':{
                'primary': android['primary'],
                'fallback': android['fallback'],
            },
            'web': web
            }

app = Flask(__name__)
@app.route('/')
def flask_mongodb_atlas():
    return "flask mongodb atlas!"

#test to insert data to the data base
@app.route('/addtest')
def add_test():
    db.db.collection.insert_one(create_entry("12345", ["ios.primary.com", 'ios.fallback.com'], ['android.primary.com', 'android.fallback.com'], "web.com"))
    return "Added dummy value"

@app.route("/shortlinks", methods=['GET'])
def get_docs():
    res = list(db.db.collection.find(projection={'_id': False}))
    # print((res[0]['_id']))
    return res

@app.route("/shortlinks", methods=['POST'])
def add_doc():
    res = request.get_json()
    try:
        slug = res['slug']
    except:
        slug = ""
    try:
        ios = res['ios']
        android = res['android']
        web = res['web']
    except:
        abort(400)

    entry = create_entry(slug, ios, android, web)
    # print(entry)
    db.db.collection.insert_one(entry)
    del entry['_id']
    return jsonify(entry)

@app.route('/shortlinks/<string:slug>', methods=['PUT'])
def update_doc(slug):
    if slug is None:
        abort(404)
    
    res = request.get_json()
    if res.get('ios',None):
        entry= db.db.collection.find_one_and_update(
                {'slug': slug},
                {'$set': {'ios': res['ios']}},return_document=ReturnDocument.AFTER
                )
    if res.get('android', None):
        entry= db.db.collection.find_one_and_update(
                {'slug': slug},
                {'$set': {'android': res['android']}},return_document=ReturnDocument.AFTER
                )
    if res.get('web', None):
        entry= db.db.collection.find_one_and_update(
                {'slug': slug},
                {'$set': {'web': res['web']}},return_document=ReturnDocument.AFTER
                )
    
    del entry['_id']
    return jsonify(entry)




## Error Handling
'''
Error handling for unprocessable entity
'''
@app.errorhandler(400)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 400,
                    "message": "Your response is missing one or multiple of the required arguments"
                    }), 400

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "Slug already exists"
                    }), 422

@app.errorhandler(404)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "Resource not found"
                    }), 404


if __name__ == '__main__':
    existing_keys = db.db.collection.distinct("slug")
    app.run(port=8000)