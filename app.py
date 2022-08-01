from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
# import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from flask_jwt_extended import JWTManager
from config import Config
from status_code import *


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config.from_object(Config)

db = SQLAlchemy(app)

from models import *

client = app.test_client()

jwt = JWTManager(app)

# engine = create_engine('sqlite:///db.sqlite')
# session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
# Base = declarative_base()
# Base.query = session.query_property()
# from models import *
# Base.metadata.create_all(bind=engine)

@app.route("/task", methods=["GET"])
def get_task():

    page = request.args.get('page',1, type=int)
    per_page = request.args.get('per_page', app.config['TASKS_PER_PAGE'], type=int)
    
    tasks = Task.query.paginate(page, per_page, True)
    
    data = []
    for task in tasks.items:
        data.append({
            'id': task.id,
            'name': task.name,
            'email': task.email,
            'text': task.text,
            'status': task.status,
        })
    meta = {
        'page': tasks.page,
        'pages': tasks.pages,
        'total_count': tasks.total,
        'prev_page': tasks.prev_num,
        'next_page': tasks.next_num,
        'has_next': tasks.has_next,
        'has_prev': tasks.has_prev,
    }
    return jsonify({'data': data, 'meta': meta}, HTTP_200_OK)


# @app.route("/tasks", methods=["POST"])
# def update_list():
#     new_one =request.json
#     tasks.append(new_one)
#     return jsonify(tasks)


# @app.route("/tasks/<int:task_id>", methods=["PUT"])
# def update_task(task_id):
#     item = next((x for x in tasks if x['id'] == task_id), None)
#     params = request.json
#     if not item:
#         return {'message': 'No task with this id'}, 400
#     item.update(params)
#     return item


# @app.route('/tasks/<int:task_id>', methods=["DELETE"])
# def delete_task(task_id):
#     index, _ = next((x for x in enumerate(tasks) 
#                         if x[1]['id'] == task_id), (None, None))
    
#     tasks.pop(index)
#     return '', 204


# @app.route('/register', methods=["POST"])
# def register():
#     params = request.json
    
#     user = User(**params)
#     session.add(user)
#     session.commit()
#     token = user.get_token()

#     return {'access_token': token}

# @app.route('/login', methods=['POST'])
# def login():
#     params = request.json
#     user = User.authenticate(**params)
#     token = user.get_token()

#     return {'access_token': token}

# @app.teardown_appcontext
# def shutdown_session(exception=None):
#     session.remove()


if __name__== '__main__':
    app.run(debug=True)