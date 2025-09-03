"""
Flask application providing a homepage and Swagger UI for the Masterblog API.

This module sets up a simple Flask server with the following:
- Swagger UI available at `/api/docs` to explore and test the API defined in
  `static/masterblog.json`.
- A homepage route (`/`) that renders `index.html`.
- Configured to run on host `0.0.0.0` and port `5001` in debug mode.

Intended as a lightweight entry point for serving the Masterblog API
documentation and a landing page.
"""
from flask_swagger_ui import get_swaggerui_blueprint
from flask import Flask, render_template


app = Flask(__name__)
SWAGGER_URL = "/api/docs"
API_URL = "/static/masterblog.json"
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Masterblog API"}
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)


@app.route('/', methods=['GET'])
def home():
    """Render the homepage template."""
    return render_template("index.html")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
