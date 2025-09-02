from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    # get inputs
    sort = request.args.get('sort', 'title')  # default: title
    direction = request.args.get('direction', 'asc')  # default: ascending

    # error handling
    if sort not in ('title', 'content'):
        return jsonify({"error": "Can only sort by 'title' or 'content'"}), 400  # 400 = Bad request

    # sort the list
    reverse = direction == "desc"
    new_list = sorted(POSTS, key=lambda x: x[sort].lower(), reverse=reverse)

    if not sort and not direction:
        return jsonify(POSTS)
    return jsonify(new_list)


@app.route('/api/posts', methods=['POST'])
def add_post():
    # get inputs
    data = request.get_json()

    # error handling
    if ((data["title"] == "" or data["content"] == "") or
            ("title" not in data or "content" not in data)):
        return jsonify({"error": "Invalid input"}), 400  # 400 = Bad request

    # Generate new id and add the data in the list
    new_id = max(post["id"] for post in POSTS) + 1 if POSTS else 1
    new_post = {
        "id": new_id,
        "title": data["title"],
        "content": data["content"]
    }
    POSTS.append(new_post)

    return jsonify(new_post), 201  # 201 = Created


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    global POSTS

    # error handling
    post = None
    for elem in POSTS:
        if elem["id"] == post_id:
            post = elem
    if post is None:
        return jsonify({"error": "Post not found"}), 404

    POSTS.remove(post)
    return jsonify({"message": f"Post with id {post_id} "
                               f"has been deleted successfully."}), 200  # 200 = OK


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    # get inputs
    global POSTS
    data = request.get_json()  # Expecting JSON in request body

    # error handling
    if "title" not in data or "content" not in data:
        return jsonify({"error": "Invalid input"}), 400  # 400 = Bad request

    # update the requested post
    post = None
    for index, elem in enumerate(POSTS):
        if elem["id"] == post_id:
            post = elem
            POSTS[index]["title"] = data["title"] if data["title"] else POSTS[index]["title"]
            POSTS[index]["content"] = data["content"] if data["content"] else POSTS[index]["content"]
            return jsonify({"message": "Post with id <id> has been updated successfully."}), 200  # 200 = OK
    if post is None:
        return jsonify({"error": "Post not found"}), 404  # 404 = Not found


@app.route('/api/posts/search', methods=['GET'])
def search_post():
    # get inputs
    title = request.args.get("title", '').lower()
    content = request.args.get("content", '').lower()

    # perform search
    search_list = []
    for post in POSTS:
        if ((title in post['title'].lower() and title) or
                (content in post['content'].lower() and content)):
            search_list.append(post)
    if not title and not content:
        return jsonify(POSTS)
    return jsonify(search_list)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
