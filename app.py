from flask import Flask, render_template, redirect, url_for, send_from_directory
from auth import app as auth_app, frontend
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__, 
    static_folder='static',
    template_folder='templates'
)

# Configure app
app.config.update(auth_app.config)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-super-secret-key-here')
app.config['WTF_CSRF_ENABLED'] = True
app.config['WTF_CSRF_SECRET_KEY'] = os.getenv('WTF_CSRF_SECRET_KEY', app.config['SECRET_KEY'])

# Serve static files
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

# Register blueprints
app.register_blueprint(frontend, url_prefix='/frontend')

# Root route redirects to frontend index
@app.route('/')
def index():
    return redirect(url_for('frontend.index'))

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('frontend/404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('frontend/500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)
