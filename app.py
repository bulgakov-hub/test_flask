from flask import Flask, jsonify, request
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)

client = app.test_client()

engine = create_engine('sqlite:///db.sqlite')

session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = session.query_property()

tasks = [
    {'id': 1, 'name': 'Konst', 'email': 'ya@ya.ru', 'text': 'Drink Coffee', 'status': 'incomplete'},
    {'id': 2, 'name': 'Vasia', 'email': 'ya@ya.ru', 'text': 'Drink Coffee', 'status': 'incomplete'},
    {'id': 3, 'name': 'Petia', 'email': 'ya@ya.ru', 'text': 'Drink Coffee', 'status': 'incomplete'},
    {'id': 4, 'name': 'Ivan', 'email': 'ya@ya.ru', 'text': 'Drink Coffee', 'status': 'incomplete'},
]

@app.route("/tasks", methods=["GET"])
def get_task():
    return jsonify(tasks)

@app.route("/tasks", methods=["POST"])
def update_list():
    new_one =request.json
    tasks.append(new_one)
    return jsonify(tasks)

@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    item = next((x for x in tasks if x['id'] == task_id), None)
    params = request.json
    if not item:
        return {'message': 'No task with this id'}, 400
    item.update(params)
    return item

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    index, _ = next((x for x in enumerate(tasks) 
                        if x[1]['id'] == task_id), (None, None))
    
    tasks.pop(index)
    return '', 204


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()


if __name__== '__main__':
    app.run()