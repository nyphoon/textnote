import os
from flask import Flask, request
from flask import render_template

app = Flask(__name__, instance_relative_config=True)


def create_app(test_config=None):
    # create and configure the app
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'textnote.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    return app


@app.route('/', methods=['GET'])
@app.route('/new', methods=['GET'])
def new():
    return render_template('new.html')


@app.route('/view', methods=['GET'])
def view():
    return render_template('view.html')


@app.route('/edit/<nid>', methods=['GET'])
def edit(nid):
    return render_template('edit.html', nid=nid)


@app.route('/note', methods=['POST'])
def save():
    print(request.data)
    if request.json is None:
        return 'bad syntax', 400
    if 'title' not in request.json or 'note' not in request.json:
        return 'bad format', 400
    return '', 201


@app.route('/note', methods=['GET'])
def list_notes():
    return 'list', 200


@app.route('/note/<nid>', methods=['GET'])
def get(nid):
    return 'note', 200


@app.route('/note/<nid>', methods=['PUT'])
def update(nid):
    return 'updated', 201
