from os import environ
from flask import (Blueprint, render_template,
                   session, url_for, redirect)
from . forms import LoginForm

bp = Blueprint('/home', __name__, url_prefix='/')


@bp.route('/', methods=["GET", "POST"])
def home():
    if 'authed' in session:
        return redirect(url_for('/search.search'))

    pwd = environ.get('password')
    if pwd is None:
        pwd = "asdf"
    form = LoginForm()
    if form.validate_on_submit():
        if form.password.data == pwd:
            session['authed'] = True
            return redirect(url_for('/search.search'))

    return render_template('home.html', form=form)
