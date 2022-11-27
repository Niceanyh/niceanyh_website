from datetime import timedelta
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from focus.auth import login_required
from focus.db import get_db

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    clocks = db.execute(
        'SELECT c.id, title, created,ended ,author_id, username'
        ' FROM clock c JOIN user u ON c.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    summary = db.execute(
        'SELECT c.id, title, created,ended'
        ' FROM clock c JOIN user u ON c.author_id = u.id WHERE ended IS NOT NULL'
        ' ORDER BY created DESC'
    ).fetchall()
    total_focus = timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)
    for s in summary:
        total_focus = total_focus+ s['ended']- s['created']
    return render_template('blog/index.html', posts=posts,clocks=clocks,total_focus=total_focus)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

@bp.route('/new_focus', methods=('GET', 'POST'))
@login_required
def new_focus():
    db = get_db()
    title = 'a focus'
    focus = get_db().execute(
        'SELECT * FROM clock WHERE author_id = ? and ended IS NULL',(g.user['id'],)).fetchone()

    if focus is not None:
        #abort(404, f"Already exist a focus rigth now.")
        flash("Already exist a focus rigth now.")
        return redirect(url_for('blog.index'))
    else:
        db.execute(
                'INSERT INTO clock (author_id,title)'
                ' VALUES (?, ?)',
                (g.user['id'],title)
            )
    db.commit()
    return redirect(url_for('blog.index'))
    
@bp.route('/<int:id>/end_focus', methods=('POST',))
@login_required
def end_focus(id):
    print(id)
    # if request.method == 'POST':
    #     id = request.form['id']
    db = get_db()
    db.execute(
                'UPDATE clock SET ended = CURRENT_TIMESTAMP WHERE id = ? and author_id = ?',(id,g.user['id'],)
            )
    db.commit()
    print("end_focus")
    return redirect(url_for('blog.index'))


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))