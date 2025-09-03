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
from json_helper import read_json_data, write_json_data


app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes
PATH = "../data/blogs.json"


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """Retrieve all posts with optional sorting by title, content, author, or date."""
    # get inputs
    posts_local = read_json_data(PATH)
    sort = request.args.get('sort', 'title')  # default: title
    direction = request.args.get('direction', 'asc')  # default: ascending

    # error handling
    if not sort and not direction:
        return jsonify(posts_local)
    if sort not in ('title', 'content', 'author', 'date'):
        return jsonify({"error": "Can only sort by "
                                 "'title'/'content'/'author'/'date'"}), 400  # 400 = Bad request

    # sort the list
    reverse = direction == "desc"
    new_list = sorted(posts_local, key=lambda x: x[sort].lower(), reverse=reverse)

    return jsonify(new_list)


@app.route('/api/posts', methods=['POST'])
def add_post():
    """Create a new post with title, content, and author."""
    # get inputs
    posts_local = read_json_data(PATH)
    data = request.get_json()

    # error handling
    if "title" not in data or "content" not in data or "author" not in data:
        return jsonify({"error": "Invalid input"}), 400  # 400 = Bad request
    if data["title"] == "" or data["content"] == "" or data["author"] == "":
        return jsonify({"error": "Invalid input"}), 400  # 400 = Bad request

    # Generate new id and add the data in the list
    new_id = max(post["id"] for post in posts_local) + 1 if posts_local else 1
    new_post = {
        "id": new_id,
        "title": data["title"],
        "content": data["content"],
        "author": data["author"],
        "date": datetime.now().today().strftime("%Y-%m-%d")
    }
    posts_local.append(new_post)

    write_json_data(PATH, posts_local)
    return jsonify(new_post), 201  # 201 = Created


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """Delete a post by its ID."""
    posts_local = read_json_data(PATH)
    for elem in posts_local:
        if elem["id"] == post_id:
            posts_local.remove(elem)
            write_json_data(PATH, posts_local)
            return jsonify({"message": f"Post with id {post_id} "
                                       f"has been deleted successfully."}), 200  # 200 = OK
    return jsonify({"error": "Post not found"}), 404


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """Update a post’s title, content, or author by its ID."""
    # get inputs
    posts_local = read_json_data(PATH)
    data = request.get_json()  # Expecting JSON in request body

    # error handling
    if "title" not in data or "content" not in data or "author" not in data:
        return jsonify({"error": "Invalid input"}), 400  # 400 = Bad request

    # update the requested post
    for index, elem in enumerate(posts_local):
        if elem["id"] == post_id:
            posts_local[index]["title"] = data["title"] if data["title"] \
                else posts_local[index]["title"]
            posts_local[index]["content"] = data["content"] if data["content"] \
                else posts_local[index]["content"]
            posts_local[index]["author"] = data["author"] if data["author"] \
                else posts_local[index]["author"]
            posts_local[index]["date"] = datetime.now().today().strftime("%Y-%m-%d")
            write_json_data(PATH, posts_local)
            return jsonify({"message": "Post with id <id> "
                                       "has been updated successfully."}), 200  # 200 = OK
    return jsonify({"error": "Post not found"}), 404  # 404 = Not found


@app.route('/api/posts/search', methods=['GET'])
def search_post():
    """Search posts by title, content, author, or date."""
    # get inputs
    posts_local = read_json_data(PATH)
    title = request.args.get("title", '').lower()
    content = request.args.get("content", '').lower()
    author = request.args.get("author", '').lower()
    date = request.args.get("date", '').lower()

    if not title and not content and not author and not date:
        return jsonify(posts_local)

    # perform search
    search_list = []
    for post in posts_local:
        match_title = title and title in post['title'].lower()
        match_author = author and author in post['author'].lower()
        match_date = date and date in post['date'].lower()
        match_content = content and content in post['content'].lower()

        if match_title or match_author or match_date or match_content:
            search_list.append(post)

    return jsonify(search_list)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
