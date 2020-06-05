import os
from flask import Flask, request, render_template, json

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
    # TODO: lock note
    return render_template('edit.html', nid=nid)


@app.route('/note', methods=['POST'])
def save():
    if request.json is None:
        result = {'msg': 'bad syntax'}
        return json.dumps(result), 400
    if 'title' not in request.json or 'note' not in request.json:
        result = {'msg': 'bad format'}
        return json.dumps(result), 400

    result = {'msg': 'saved'}
    return json.dumps(result), 200


@app.route('/note', methods=['GET'])
def list_notes():
    notes = [{'nid': '1',
              'title': 'aaa',
              'note': 'bbb'},
              {'nid': '2',
              'title': 'xxx',
              'note': 'yyy'}]
    return json.dumps(notes), 200


@app.route('/note/<nid>', methods=['GET'])
def get(nid):
    note = {'nid': '1',
            'title': 'aaa',
            'note': 'bbb'}
    return json.dumps(note), 200


@app.route('/note/<nid>', methods=['PUT'])
def update(nid):
    result = {'msg': 'modified'}
    return json.dumps(result), 201
