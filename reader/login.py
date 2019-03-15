from os import environ
from flask import Blueprint, session, redirect, request, url_for

bp = Blueprint('/login', __name__, url_prefix='/l')


@bp.route('/', methods=("POST",))
def login():
    pwd = environ.get('password')
    if pwd is None:
        pwd = "weakpassword"
    print(request.form)
    if request.form['input'] is pwd:
        session['authed'] = "value"
        print('set session value?')
        return redirect(url_for('/search.search'))
    else:
        print('redirecting home')
        return redirect(url_for('/home.home'))

