from flask import Flask, request, abort, jsonify
import bson
import db
from pymongo import ReturnDocument
from flask_cors import CORS


# Helper function to create documents while validating the input
def create_entry(slug, ios, android, web):
    # Access global variable to check if slug exists or not
    global existing_keys

    # If no custom slug, create new one using pymongo default generator
    if slug == "":
        slug = str(bson.objectid.ObjectId())
        # Keep generating until not a duplicate
        while slug in existing_keys:
            slug = str(bson.objectid.ObjectId())
        existing_keys.append(slug)

    # If custom slug, make sure it doesn't already exist and if not then continue
    else:
        if slug in existing_keys:
            abort(422)

    # Required schema for application
    return {'slug': slug,
            'ios': {
                'primary': ios['primary'],
                'fallback': ios['fallback']
            },
            'android': {
                'primary': android['primary'],
                'fallback': android['fallback'],
            },
            'web': web
            }


app = Flask(__name__)

# Adding CORS to allow cross application requests
CORS(app)

# Tester endpoint
# @app.route('/')
# def flask_mongodb_atlas():
#     return "flask mongodb atlas!"

# Tester endpoint to add a dummy value
# @app.route('/addtest')
# def add_test():
#     db.db.collection.insert_one(create_entry("12345", ["ios.primary.com", 'ios.fallback.com'], ['android.primary.com', 'android.fallback.com'], "web.com"))
#     return "Added dummy value"

# List all documents
# GET Request
# Gets all documents in collection and retrieves them while removing the mongo _id because it is not JSON serializable by default


@app.route("/shortlinks", methods=['GET'])
def get_docs():
    res = list(db.db.collection.find(projection={'_id': False}))
    return res

# Add new document
# POST request
# Adds new document based on form data it recieves


@app.route("/shortlinks", methods=['POST'])
def add_doc():
    # Get request data
    res = request.get_json()

    # Set slug to empty by default if no custom slug sent
    try:
        slug = res['slug']
    except:
        slug = ""

    # If any of the required arguments are left out, abort with 400 error for bad request
    try:
        ios = res['ios']
        android = res['android']
        web = res['web']
    except:
        abort(400)

    # Create document in correct format and generate new slug if needed
    entry = create_entry(slug, ios, android, web)

    # Insert document into collection and return it
    db.db.collection.insert_one(entry)
    del entry['_id']
    return jsonify(entry)

# Update document
# PUT Request
# Updates existing document based on form data
# Recieves slug in URL


@app.route('/shortlinks/<string:slug>', methods=['PUT'])
def update_doc(slug):
    if slug is None:
        abort(404)

    res = request.get_json()

    # For each major field, check if it is present in the request and if it does, update its corresponding field while returning the newly updated value
    if res.get('ios', None):
        entry = db.db.collection.find_one_and_update(
            {'slug': slug},
            {'$set': {'ios': res['ios']}}, return_document=ReturnDocument.AFTER
        )
    if res.get('android', None):
        entry = db.db.collection.find_one_and_update(
            {'slug': slug},
            {'$set': {'android': res['android']}}, return_document=ReturnDocument.AFTER
        )
    if res.get('web', None):
        entry = db.db.collection.find_one_and_update(
            {'slug': slug},
            {'$set': {'web': res['web']}}, return_document=ReturnDocument.AFTER
        )

    # Slug can't be updated
    if res.get('slug', None):
        abort(403)

    del entry['_id']
    return jsonify(entry)


# Error Handling
'''
Error handling for Bad request
'''
@app.errorhandler(400)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Your request is missing one or multiple of the required arguments"
    }), 400


'''
Error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "Unprocessable i.e. Slug already exists"
    }), 422

'''
Error handling for missing resource
'''
@app.errorhandler(404)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Resource not found"
    }), 404

'''
Error handling for forbidden access
'''
@app.errorhandler(403)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 403,
        "message": "Forbidden"
    }), 403


if __name__ == '__main__':
    # Get existing keys to keep track of them
    existing_keys = db.db.collection.distinct("slug")
    # Run app on port 8000
    app.run(port=8000)
