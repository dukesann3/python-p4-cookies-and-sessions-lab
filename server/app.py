#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session, request
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
#no CORS?

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():
    all_articles = [article.to_dict() for article in Article.query.all()]
    return make_response(all_articles, 200)

@app.route('/articles/<int:id>', methods=['GET'])
def show_article(id):
    article = Article.query.filter_by(id=id).first().to_dict()
    if not article:
        print("Non existent")
        return make_response({"message": f"ID:{id} does not exist"}, 404)

    session["page_views"] = int(session.get("page_views")) + 1 if session.get("page_views") else 1
    page_views = session.get("page_views")
    print(page_views)

    if page_views <= 3:
        response = make_response(article, 200)
        return response
    else:
        print("error")
        response = make_response({"message": "Maximum pageview limit reached"}, 401)
        return response
    
@app.route('/delete')
def delete_cookie():
    response = make_response("no more cookies")
    response.set_cookie("page_views", 0, expires=0)

    return response


if __name__ == '__main__':
    app.run(port=5555)
