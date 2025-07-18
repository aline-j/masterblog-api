from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET', 'POST'])
def posts():
    if request.method == 'POST':
        data = request.get_json()

        # Validate fields
        missing_fields = []
        if not data.get('title'):
            missing_fields.append('title')
        if not data.get('content'):
            missing_fields.append('content')

        if missing_fields:
            return jsonify({
                'error': 'Missing required  fields',
                'missing': missing_fields
            }), 400

        # Create new post
        new_post = {
            'id': len(POSTS) + 1,
            'title': data.get('title'),
            'content': data.get('content'),
        }
        POSTS.append(new_post)
        return jsonify(new_post), 201

    else:
        return jsonify(POSTS)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
