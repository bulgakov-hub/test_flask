from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config import Config
from status_code import *

from flask_apispec.extension import FlaskApiSpec
from schemas import TaskSchema, AdminUserSchema, AuthSchema
from flask_apispec import use_kwargs, marshal_with


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

client = app.test_client()

jwt = JWTManager(app)

doc = FlaskApiSpec()
doc.init_app(app)

from models import *

@app.route("/task", methods=["GET"])
def get_task():

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', app.config['TASKS_PER_PAGE'], type=int)
    
    tasks = Task.query.paginate(page, per_page, False)
    schema = TaskSchema(many=True)
    task_list = schema.dump(tasks.items)
    paginate = {
        'page': tasks.page,
        'pages': tasks.pages,
        'total_count': tasks.total,
        'prev_page': tasks.prev_num,
        'next_page': tasks.next_num,
        'has_next': tasks.has_next,
        'has_prev': tasks.has_prev,
    }

    return jsonify({'task_list': task_list ,'paginate': paginate})


@app.route("/task", methods=["POST"])
@use_kwargs(TaskSchema)
@marshal_with(TaskSchema)
def create_task(**kwargs):
       
    new_task = Task(**kwargs)
    db.session.add(new_task)
    db.session.commit()

    return new_task


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


@app.route('/register', methods=["POST"])
@use_kwargs(AdminUserSchema)
@marshal_with(AdminUserSchema)
def register(**kwargs):
    
    user = AdminUser(**kwargs)
    db.session.add(user)
    db.session.commit()
    token = user.get_token()

    return {'access_token': token}

@app.route('/login', methods=['POST'])
@use_kwargs(AdminUserSchema(only=('name','password'), partial=True))
@marshal_with(AuthSchema)
def login(**kwargs):
    
    user = AdminUser.authenticate(**kwargs)
    token = user.get_token()

    return {'access_token': token}

# @app.teardown_appcontext
# def shutdown_session(exception=None):
#     session.remove()


if __name__== '__main__':
    app.run(debug=True)