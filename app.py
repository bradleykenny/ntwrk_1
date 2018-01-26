# A SOCIAL NETWORK VERSION 1.0
# BY BRADLEY KENNY

# THIS IS THE APP THAT SHOULD BE RUN WHEN TRYING TO RUN PROGRAM
# OPEN CMD AND RUN > PYTHON APP.PY

# REQUIRES PIP INSTALL [FLASK, PEEWEE, FLASK-BCRYPT, FLASK-LOGIN, WTFORMS]

from flask import Flask, g, render_template, flash, redirect, url_for, abort
from flask_bcrypt import check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

import forms
import models

# FOR RUNNING APP (WHAT TO RUN ON); USED AS VARIABLES IN END
DEBUG = False # CHANGE TO FALSE WHEN COMPLETE (WHEN FALSE, CHANGES TO CODE DONT DISPLAY ON REFRESH)
PORT = 2000
HOST = '127.0.0.1'

app = Flask(__name__)
app.secret_key = 'qins.snlqsnoqsunbqy7qs.nqsnqb!abdak0,ashdbaa1'    # CAN CHANGE TO ANYTHING

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(userid):
	try:
		return models.User.get(models.User.id == userid)
	except models.DoesNotExist:
		return None

@app.before_request
def before_request():
    g.db = models.DATABASE
    g.db.connect()     # OPEN CONNECTION TO DATABASE
    g.user = current_user

@app.after_request
def after_request(response):
	g.db.close()   # CLOSE DATABASE CONNECTION
	return response

@app.route('/')
def index():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=('GET', 'POST'))
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash("You're now registered on Lorem.", "success")
        models.User.create_user(
            username = form.username.data,
            email = form.email.data,
            password = form.password.data
        )
        return redirect(url_for('index'))
    return render_template('register.html', form=form)

# LOG IN PAGE SHOULD BE FIRST PAGE SO ANYONE WITHOUT PASSWORD CANT SEE CONTENT
# I HAVE DONE THIS IN APP.ROUTE('/')
@app.route('/login', methods= ('GET', 'POST'))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash("Email doesn't match.", "error")

        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('stream'))
            else:
                flash("Email or password isn't correct.", "error")
    return render_template('login.html', form = form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out", "success")
    return redirect(url_for('index'))

@app.route('/new_post', methods=('GET', 'POST'))
@login_required
def post():
    form = forms.PostForm()
    if form.validate_on_submit():
        models.Post.create(user=g.user.id,
                           content=form.content.data.strip())
        flash("Message posted", "success")
        return redirect(url_for('stream'))
    return render_template('post.html', form=form)

@app.route('/all')
def all():
    stream = models.Post.select().limit(100)
    return render_template('stream.html', stream=stream)

@app.route('/stream')
@app.route('/stream/<username>')
@login_required
def stream(username=None):
    template = 'stream.html'
    if username and username != current_user.username:
        try:
            user = models.User.select().where(
                models.User.username**username).get()
        except models.DoesNotExist:
            abort(404)
        else:
            stream = user.posts.limit(100)
    else:
        stream = current_user.get_stream().limit(100)
        user = current_user
    if username:
        template = 'user_stream.html'
    return render_template(template, stream=stream, user=user)


@app.route('/post/<int:post_id>')
def view_post(post_id):
    posts = models.Post.select().where(models.Post.id == post_id)
    if posts.count() == 0:
        abort(404)
    return render_template('stream.html', stream=posts)

@app.route('/delete_post/<int:post_id>')
def delete_post(post_id):
    try:
        post = models.Post.select().where(models.Post.id == post_id).get()
    except models.Post.DoesNotExist:
        abort(404)

    post.delete_instance()
    flash("This post has successfully been deleted", "success")
    return redirect(url_for('stream', stream = stream))

@app.route('/edit_post/<int:post_id>', methods=('GET', 'POST'))
@login_required
def edit_post(post_id):
    edit = models.Post.select().where(models.Post.id == post_id).get()
    form = forms.PostForm(obj=edit)
    form.populate_obj(edit)
    if form.validate_on_submit():
        new_content = form.content.data.strip()
        q = models.Post.update(content=new_content).where(models.Post.id == post_id)
        q.execute()
        flash("Post updated.", "success")
        return redirect(url_for('all'))
    return render_template('post.html', form=form)

@app.route('/follow/<username>')
@login_required
def follow(username):
    try:
        to_user = models.User.get(models.User.username**username)
    except models.DoesNotExist:
        abort(404)
    else:
        try:
            models.Relationship.create(
                from_user=g.user._get_current_object(),
                to_user=to_user
            )
        except models.IntegrityError:
            pass
        else:
            flash("You're now following {}.".format(to_user.username), "success")
    return redirect(url_for('stream', username=to_user.username))

@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    try:
        to_user = models.User.get(models.User.username**username)
    except models.DoesNotExist:
        abort(404)
    else:
        try:
            models.Relationship.get(
                from_user=g.user._get_current_object(),
                to_user=to_user
            ).delete_instance()
        except models.IntegrityError:
            pass
        else:
            flash("You've unfollowed {}.".format(to_user.username), "success")
    return redirect(url_for('stream', username=to_user.username))

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def not_found(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    models.initialize()
    try:
        models.User.create_user(
            username='bradleykenny',
            email='bradleykenny@gmail.com',
            password='bradley123'
        )
    except ValueError:
        pass
    app.run(debug=DEBUG, host=HOST, port=PORT)     # VALUES STEM FROM BEGINNING OF CODE
