"""
Backend package initialization.
This makes the Backend directory a Python package and allows for proper imports.
"""

from flask import Flask

app = Flask(__name__)

# Import routes after app initialization to avoid circular imports
from controllers.server import configure_routes

# Configure the application routes
configure_routes(app)
