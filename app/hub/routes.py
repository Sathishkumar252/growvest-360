from flask import Blueprint, render_template, abort
from flask_login import login_required
from ..services.investment_info import OPTIONS, BY_SLUG, AS_OF, REVIEW_NOTE

hub_bp = Blueprint('hub', __name__, url_prefix='/hub')


@hub_bp.route('/')
@login_required
def index():
    return render_template('hub/index.html', options=OPTIONS, as_of=AS_OF, review_note=REVIEW_NOTE)


@hub_bp.route('/<slug>')
@login_required
def detail(slug):
    option = BY_SLUG.get(slug)
    if option is None:
        abort(404)
    return render_template('hub/detail.html', o=option, as_of=AS_OF, review_note=REVIEW_NOTE)