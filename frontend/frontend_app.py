from flask_swagger_ui import get_swaggerui_blueprint
from flask import Flask, render_template

app = Flask(__name__)

SWAGGER_URL = "/api/docs"  # Swagger UI will be available here
API_URL = "/static/masterblog.json"  # Path to your swagger file

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Masterblog API"}
)

# ✅ Register blueprint BEFORE app.run
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/', methods=['GET'])
def home():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
