import os
from flask import (Flask, request, render_template, json, current_app,
                   send_file)
from .locking import Locking


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'textnote.sqlite'),
        EXPORT=os.path.join(app.instance_path, 'export')
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

    locking = Locking()

    @app.route('/', methods=['GET'])
    @app.route('/new', methods=['GET'])
    def new():
        return render_template('new.html')


    @app.route('/view', methods=['GET'])
    def view():
        return render_template('view.html')


    @app.route('/edit/<nid>', methods=['GET'])
    def edit(nid):
        token = locking.get(nid)
        if token is None:
            return 'This note is using by someone else. Please edit it later.', 200
        return render_template('edit.html', nid=nid, token=token)


    @app.route('/note', methods=['POST'])
    def save():
        note = request.json
        if note is None:
            result = {'msg': 'bad syntax'}
            return json.dumps(result), 400
        if 'title' not in note or 'note' not in note:
            result = {'msg': 'bad format'}
            return json.dumps(result), 400

        conn = db.get_db()
        c = conn.cursor()
        c.execute('INSERT INTO textnote (title, note) VALUES (?, ?)',
                (note['title'], note['note']))
        conn.commit()

        result = {'msg': 'saved'}
        return json.dumps(result), 200


    @app.route('/note', methods=['GET'])
    def list_notes():
        notes = []
        conn = db.get_db()
        c = conn.cursor()
        for row in c.execute('SELECT title, nid FROM textnote'):
            notes.append(dict(row))
        return json.dumps(notes), 200


    @app.route('/note/<nid>', methods=['GET'])
    def get(nid):
        conn = db.get_db()
        c = conn.cursor()
        c.execute('SELECT title, nid, note FROM textnote WHERE nid=?', (nid,))
        row = c.fetchone()
        if row is None:
            result = {'msg': 'note not exist'}
            return json.dumps(result), 404
        note = dict(row)
        return json.dumps(note), 200


    @app.route('/note/<nid>', methods=['PUT'])
    def modify(nid):
        note = request.json
        if note is None:
            result = {'msg': 'bad syntax'}
            return json.dumps(result), 400
        if 'note' not in note or 'token' not in note:
            result = {'msg': 'bad format'}
            return json.dumps(result), 400
        if not locking.verify(nid, note['token']):
            result = {'msg': 'access denied'}
            return json.dumps(result), 403

        conn = db.get_db()
        c = conn.cursor()
        c.execute('UPDATE textnote SET note=? WHERE nid=?',
                  (note['note'], int(nid)))
        conn.commit()

        locking.release(nid, note['token'])
        if c.rowcount == 0:
            result = {'msg': 'no note to modify'}
            return json.dumps(result), 400

        result = {'msg': 'modified'}
        return json.dumps(result), 200


    @app.route('/download/<nid>')
    def download(nid):
        conn = db.get_db()
        c = conn.cursor()
        c.execute('SELECT title, nid, note FROM textnote WHERE nid=?', (nid,))
        row = c.fetchone()
        if row is None:
            result = {'msg': 'note not exist'}
            return json.dumps(result), 404

        note = dict(row)
        export_dir = current_app.config['EXPORT']
        if not os.path.exists(export_dir):
            os.makedirs(export_dir)
        export_path = os.path.join(export_dir, str(note['nid']))
        with open(export_path, 'w') as fp:
            fp.write(note['note'])
        return send_file(export_path, as_attachment=True,
                         attachment_filename=note['title']+'.txt')

    return app
