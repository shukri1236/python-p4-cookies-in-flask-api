
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request, session
from flask_migrate import Migrate

from models import db, Article

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'  # Use one secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

# Route to show session data
@app.route('/sessions/<string:key>', methods=['GET'])
def show_session(key):
    if key in session:
        response = make_response(jsonify({
            'session': {
                'session_key': key,
                'session_value': session[key],
                'session_accessed': session.accessed,
            },
            'cookies': [{cookie: request.cookies[cookie]} for cookie in request.cookies],
        }), 200)
    else:
        response = {'message': f'Session key "{key}" not found'}, 404
    return response

# Route to clear session data
@app.route('/clear')
def clear_session():
    session.clear()  # Clear the entire session
    return {'message': '200: Successfully cleared session data'}, 200

# Route to list all articles
@app.route('/articles')
def index_articles():
    articles = [article.to_dict() for article in Article.query.all()]
    return make_response(jsonify(articles), 200)

# Route to show a specific article and manage page views
@app.route('/articles/<int:id>')
def show_article(id):
    session['page_views'] = session.get('page_views', 0) + 1

    if session['page_views'] <= 3:
        article = Article.query.filter_by(id=id).first()
    