from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, get_jwt
from config import Config
from flask_cors import CORS, cross_origin
from status_code import *
from flask_apispec.extension import FlaskApiSpec
from schemas import TaskSchema, TaskSchemaUpdate, AdminUserSchema, AuthSchema
from flask_apispec import use_kwargs, marshal_with
from datetime import datetime
from datetime import timezone
import os.path


app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

db = SQLAlchemy(app)

client = app.test_client()

jwt = JWTManager(app)

docs = FlaskApiSpec()
docs.init_app(app)

from models import *


@app.route("/api/v1/task", methods=["GET"])
def get_task():
    try:
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
    except Exception as e:
        return make_response(jsonify({'message': str(e)}), HTTP_400_BAD_REQUEST)

    return make_response(jsonify({'task_list': task_list ,'paginate': paginate}), HTTP_200_OK)


@app.route("/api/v1/task", methods=["POST"])
@use_kwargs(TaskSchema)
@marshal_with(TaskSchema)
def create_task(**kwargs):
    
    try:
        new_task = Task(**kwargs)
        db.session.add(new_task)
        db.session.commit()
    
    except Exception as e:
        return make_response(jsonify({'message': str(e)}), HTTP_400_BAD_REQUEST)
    
    return new_task, HTTP_201_CREATED


@app.route("/api/v1/task/<int:task_id>", methods=["PUT"])
@app.route("/api/v1/task/<int:task_id>", methods=["PATCH"])
@jwt_required()
@use_kwargs(TaskSchemaUpdate)
@marshal_with(TaskSchemaUpdate)
def update_task(task_id, **kwargs):
    
    try:
        task = Task.query.filter(Task.id == task_id).first()
        if not task:
            return make_response(jsonify({'message': 'Task not found'}), HTTP_404_NOT_FOUND) 
        
        for key, value in kwargs.items():
            if key == 'admin_edit':
                value = True
            setattr(task, key, value)
        db.session.commit()
    
    except Exception as e:
        return make_response(jsonify({'message': str(e)}), HTTP_400_BAD_REQUEST)
    
    return task, HTTP_200_OK


@app.route('/api/v1/task/<int:task_id>', methods=["DELETE"])
@jwt_required()
@marshal_with(TaskSchema)
def delete_task(task_id):
    
    try:
        task = Task.query.filter(Task.id == task_id).first()
        if not task:
            return make_response(jsonify({'message': 'Task not found'}), HTTP_404_NOT_FOUND) 
        
        db.session.delete(task)
        db.session.commit()
    
    except Exception as e:
        return make_response(jsonify({'message': str(e)}), HTTP_400_BAD_REQUEST)

    return jsonify({}), HTTP_204_NO_CONTENT


@app.route('/api/v1/register', methods=["POST"])
@use_kwargs(AdminUserSchema)
@marshal_with(AdminUserSchema)
def register(**kwargs):
    
    try:
        user = AdminUserTask(**kwargs)
        db.session.add(user)
        db.session.commit()
        token = user.get_token()
    
    except Exception as e:
        return make_response(jsonify({'message': str(e)}), HTTP_400_BAD_REQUEST)


    return jsonify({'access_token': token}), HTTP_201_CREATED


@app.route('/api/v1/login', methods=['POST'])
@use_kwargs(AdminUserSchema(only=('name','password'), partial=True))
@marshal_with(AuthSchema)
def login(**kwargs):
    
    try:
        user = AdminUserTask.authenticate(**kwargs)
        token = user.get_token()
    
    except Exception as e:
        return make_response(jsonify({'message': str(e)}), HTTP_400_BAD_REQUEST)

    return {'access_token': token}


@app.route("/api/v1/logout", methods=["DELETE"])
@jwt_required()
def modify_token():
    try:
        jti = get_jwt()["jti"]
        now = datetime.now(timezone.utc)
        db.session.add(TokenBlocklist(jti=jti, created_at=now))
        db.session.commit()
    
    except Exception as e:
        return make_response(jsonify({'message': str(e)}), HTTP_400_BAD_REQUEST)
    
    return jsonify(message="JWT revoked")


@app.errorhandler(422)
def error_handlers(err):
    
    headers = err.data.get('headers', None)
    messages = err.data.get('messages', ['Invalid request'])
    if headers:
        return make_response(jsonify({'message': messages}), HTTP_400_BAD_REQUEST, headers)
    else:
        return make_response(jsonify({'message': messages}), HTTP_400_BAD_REQUEST)


docs.register(get_task)
docs.register(create_task)
docs.register(update_task)
docs.register(delete_task)
docs.register(register)
docs.register(login)


if __name__== '__main__':
    
    

    app.run(debug=True)