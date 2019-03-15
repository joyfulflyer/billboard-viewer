from flask import (Blueprint, render_template,
                   session, url_for, redirect)

bp = Blueprint('/home', __name__, url_prefix='/')


@bp.route('/', methods=("GET",))
def home():
    if 'authed' in session:
        return redirect(url_for('/search.search'))
    return render_template('home.html')
