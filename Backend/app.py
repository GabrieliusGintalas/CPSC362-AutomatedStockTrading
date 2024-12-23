from flask import Flask
from controllers.server import configure_routes

app = Flask(__name__)
configure_routes(app)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
