from decimal import Decimal
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from ..extensions import db
from ..models.finance import Income, Expense
from ..salary.routes import month_arg
from ..services.finance_engine import summarize_budget
from ..services.recommendation import build_plan, check_custom
from ..services.investment_info import BY_SLUG
from .forms import PlanForm

plan_bp = Blueprint('plan', __name__, url_prefix='/plan')


@plan_bp.route('/')
@login_required
def index():
    month = month_arg()
    # Read-only calculation, so a GET form is fine (nothing is saved)
    form = PlanForm(formdata=request.args, meta={'csrf': False})
    plan = None
    check = None
    chart = None
    prefill = {}

    form_ok = form.validate() if 'saved' in request.args else False
    # Plan-ku 'saved' correct-ah irundha podhum, adjust box-la thappu irundhaalum plan theriyanum
    if 'saved' in request.args and not form.saved.errors:
        # Ella query-yum current_user.id vechu filter (data isolation)
        incomes = db.session.scalars(
            db.select(Income).filter_by(user_id=current_user.id)).all()
        expenses = db.session.scalars(
            db.select(Expense).filter_by(user_id=current_user.id, month=month)).all()
        summary = summarize_budget(incomes, expenses)

        s = current_user.settings
        plan = build_plan(
            summary['monthly_income'], summary['by_category'], form.saved.data,
            risk=s.risk_tolerance if s else 'medium',
            horizon_years=s.horizon_years if s else 5,
            target_months=s.emergency_target_months if s else 6,
            family_members=s.family_members if s else 1,
        )
        plan['has_profile'] = s is not None

        if plan['status'] == 'ok':
            amounts = {a['key']: a['amount'] for a in plan['allocations']}
            prefill = {
                'emergency': amounts['emergency'],
                'invest': amounts['invest'],
                'buffer': amounts['buffer'],
            }
            chart = {
                'labels': [a['label'] for a in plan['allocations']],
                'values': [float(a['amount']) for a in plan['allocations']],
            }
            if request.args.get('action') == 'adjust':
                if form_ok:
                    zero = Decimal('0')
                    ce = form.custom_emergency.data if form.custom_emergency.data is not None else zero
                    ci = form.custom_invest.data if form.custom_invest.data is not None else zero
                    cb = form.custom_buffer.data if form.custom_buffer.data is not None else zero
                    check = check_custom(plan, ce, ci, cb)
                    prefill = {'emergency': ce, 'invest': ci, 'buffer': cb}
                else:
                    # thappaana value-ah user type panna maadhiriye kaattu, error-oda
                    prefill = {
                        'emergency': request.args.get('custom_emergency', ''),
                        'invest': request.args.get('custom_invest', ''),
                        'buffer': request.args.get('custom_buffer', ''),
                    }

    return render_template(
        'plan/index.html', form=form, plan=plan, check=check, chart=chart, prefill=prefill,
        month_value=month.strftime('%Y-%m'), month_label=month.strftime('%B %Y'),
        hub=BY_SLUG,
    )