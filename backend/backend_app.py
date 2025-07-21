from flask import Flask, jsonify, request
from flask_cors import CORS
from nltk.toolbox import sort_fields

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


# Posts route
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

    sort_field = request.args.get('sort')
    valid_fields = ['title', 'content']
    if sort_field and sort_field not in valid_fields:
        return jsonify({'error': 'Invalid sort field'}), 400

    sort_direction = request.args.get('direction')
    valid_directions = ['asc', 'desc']
    if sort_direction and sort_direction not in valid_directions:
        return jsonify({'error': 'Invalid sort direction'}), 400

    result_posts = POSTS

    if sort_field:
        reverse = True if sort_direction == 'desc' else False
        result_posts = sorted(POSTS, key=lambda post: post[sort_field].lower(), reverse=reverse)

    return jsonify(result_posts)


# Delete Route
@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete(post_id):
    global POSTS

    filtered_posts = []
    for post in POSTS:
        if post["id"] != post_id:
            filtered_posts.append(post)

    if len(filtered_posts) < len(POSTS):
        POSTS = filtered_posts
        return jsonify({"message": f"Post with id {post_id} has been deleted successfully."}), 200
    else:
        return jsonify({"error": f"No post found with id {post_id}."}), 404


# Update Route
@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update(post_id):
    global POSTS
    data = request.get_json()

    # Search post with matching ID
    for post in POSTS:
        if post["id"] == post_id:
            # Update only if fields have been passed
            post["title"] = data.get("title", post["title"])
            post["content"] = data.get("content", post["content"])
            return jsonify(post), 200

    return jsonify({"error": f"No post found with id {post_id}."}), 404


# Search Route
@app.route('/api/posts/search', methods=['GET'])
def search():
    global POSTS
    title_query = request.args.get('title', '').lower()
    content_query = request.args.get('content', '').lower()

    results = []
    for post in POSTS:
        title_match = title_query in post['title'].lower()
        content_match = content_query in post['content'].lower()
        if title_query and content_query:
            if title_match or content_match:
                results.append(post)
        elif title_query:
            if title_match:
                results.append(post)
        elif content_query:
            if content_match:
                results.append(post)

        return jsonify(results), 200
    return False


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
