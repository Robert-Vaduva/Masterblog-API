"""
Flask application providing a simple blog API with CRUD and search functionality.

This module defines a minimal in-memory API for managing blog posts, supporting:
- Retrieving all posts with optional sorting (`/api/posts`, GET).
- Creating new posts (`/api/posts`, POST).
- Updating posts by ID (`/api/posts/<id>`, PUT).
- Deleting posts by ID (`/api/posts/<id>`, DELETE).
- Searching posts by title, content, author, or date (`/api/posts/search`, GET).

CORS is enabled for all routes, and posts are stored in an in-memory list
for demonstration purposes only.
"""
from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "author": "Robert",
     "content": "This is the first post.", "date": "2023-06-07"},
    {"id": 2, "title": "Second post", "author": "Robert",
     "content": "This is the second post.", "date": "2023-06-07"},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """Retrieve all posts with optional sorting by title, content, author, or date."""
    # get inputs
    sort = request.args.get('sort', 'title')  # default: title
    direction = request.args.get('direction', 'asc')  # default: ascending

    # error handling
    if not sort and not direction:
        return jsonify(POSTS)
    if sort not in ('title', 'content', 'author', 'date'):
        return jsonify({"error": "Can only sort by "
                                 "'title'/'content'/'author'/'date'"}), 400  # 400 = Bad request

    # sort the list
    reverse = direction == "desc"
    new_list = sorted(POSTS, key=lambda x: x[sort].lower(), reverse=reverse)

    return jsonify(new_list)


@app.route('/api/posts', methods=['POST'])
def add_post():
    """Create a new post with title, content, and author."""
    # get inputs
    data = request.get_json()

    # error handling
    if "title" not in data or "content" not in data or "author" not in data:
        return jsonify({"error": "Invalid input"}), 400  # 400 = Bad request
    if data["title"] == "" or data["content"] == "" or data["author"] == "":
        return jsonify({"error": "Invalid input"}), 400  # 400 = Bad request

    # Generate new id and add the data in the list
    new_id = max(post["id"] for post in POSTS) + 1 if POSTS else 1
    new_post = {
        "id": new_id,
        "title": data["title"],
        "content": data["content"],
        "author": data["author"],
        "date": datetime.now().today().strftime("%Y-%m-%d")
    }
    POSTS.append(new_post)

    return jsonify(new_post), 201  # 201 = Created


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """Delete a post by its ID."""
    posts_local = POSTS
    for elem in posts_local:
        if elem["id"] == post_id:
            POSTS.remove(elem)
            return jsonify({"message": f"Post with id {post_id} "
                                       f"has been deleted successfully."}), 200  # 200 = OK
    return jsonify({"error": "Post not found"}), 404


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """Update a post’s title, content, or author by its ID."""
    # get inputs
    data = request.get_json()  # Expecting JSON in request body

    # error handling
    if "title" not in data or "content" not in data or "author" not in data:
        return jsonify({"error": "Invalid input"}), 400  # 400 = Bad request

    # update the requested post
    for index, elem in enumerate(POSTS):
        if elem["id"] == post_id:
            POSTS[index]["title"] = data["title"] if data["title"] \
                else POSTS[index]["title"]
            POSTS[index]["content"] = data["content"] if data["content"] \
                else POSTS[index]["content"]
            POSTS[index]["author"] = data["author"] if data["author"] \
                else POSTS[index]["author"]
            POSTS[index]["date"] = datetime.now().today().strftime("%Y-%m-%d")
            return jsonify({"message": "Post with id <id> "
                                       "has been updated successfully."}), 200  # 200 = OK
    return jsonify({"error": "Post not found"}), 404  # 404 = Not found


@app.route('/api/posts/search', methods=['GET'])
def search_post():
    """Search posts by title, content, author, or date."""
    # get inputs
    title = request.args.get("title", '').lower()
    content = request.args.get("content", '').lower()
    author = request.args.get("author", '').lower()
    date = request.args.get("date", '').lower()

    if not title and not content and not author and not date:
        return jsonify(POSTS)

    # perform search
    search_list = []
    for post in POSTS:
        if ((title in post['title'].lower() and title) or
                (author in post['author'].lower() and author) or
                (date in post['date'].lower() and date) or
                (content in post['content'].lower() and content)):
            search_list.append(post)

    return jsonify(search_list)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
