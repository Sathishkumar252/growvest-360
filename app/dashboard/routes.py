from flask import Blueprint, render_template
from flask_login import login_required, current_user
from ..salary.routes import month_arg
from ..services.dashboard_data import build_dashboard

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard_bp.route('/')
@login_required
def index():
    month = month_arg()
    data = build_dashboard(current_user.id, month, current_user.settings)
    return render_template(
        'dashboard/index.html',
        d=data,
        month_value=month.strftime('%Y-%m'),
        month_label=month.strftime('%B %Y'),
    )