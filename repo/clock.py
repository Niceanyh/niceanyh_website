from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from focus.auth import login_required
from focus.db import get_db

bp = Blueprint('clock', __name__)

@bp.route('/')
def index():
    db = get_db()
    # posts = db.execute(
    #     'SELECT p.id, title, body, created, author_id, username'
    #     ' FROM post p JOIN user u ON p.author_id = u.id'
    #     ' ORDER BY created DESC'
    # ).fetchall()
    clocks = db.execute(
        'SELECT c.id, title, created,ended ,author_id, username'
        ' FROM clock c JOIN user u ON c.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', clocks=clocks)

@bp.route('/new_focus', methods=('GET', 'POST'))
@login_required
def new_focus():
    db = get_db()
    title = 'a focus'
    db.execute(
                'INSERT INTO clock (author_id,title)'
                ' VALUES (?, ?)',
                (g.user['id'],title)
            )
    db.commit()
    return redirect(url_for('blog.index'))



@bp.route('/end_focus', methods=('GET', 'POST'))
@login_required
def new_focus():
    if request.method == 'POST':
        id = request.form['id']
    db = get_db()
    db.execute(
                'UPDATE clock SET ended = CURRENT_TIMESTAMP WHERE id = ? and author_id = ?',
                ' VALUES (?, ?)',
                (id,g.user['id'])
            )
    db.commit()
    return redirect(url_for('blog.index'))





