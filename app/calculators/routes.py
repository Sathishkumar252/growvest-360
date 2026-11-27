from flask import Blueprint, render_template, abort
from flask_login import login_required
from ..services import investment_engine as eng
from .forms import SIPForm, FDForm, RDForm, CompoundForm

calc_bp = Blueprint('calculators', __name__, url_prefix='/calculators')


def run_sip(f):
    return eng.sip(f.monthly_amount.data, f.annual_return.data, f.years.data * 12)


def run_fd(f):
    return eng.fd(f.principal.data, f.annual_rate.data, f.months.data, f.compounding.data)


def run_rd(f):
    return eng.rd(f.monthly_amount.data, f.annual_rate.data, f.months.data, f.compounding.data)


def run_compound(f):
    return eng.compound(f.principal.data, f.annual_rate.data, f.years.data * 12, f.compounding.data)


CALCULATORS = {
    'sip': {
        'title': 'SIP Calculator',
        'blurb': 'Estimate the future value of investing a fixed amount every month in a market-linked fund.',
        'form': SIPForm, 'run': run_sip,
        'value_label': 'Estimated future value',
        'basis': 'Assumed return (not guaranteed)',
        'notes': [
            'Each instalment is invested at the start of the month.',
            'The annual return is divided by 12 and compounded monthly.',
            'Real market returns change every year and can be negative. This is an estimate, not a prediction.',
        ],
    },
    'fd': {
        'title': 'Fixed Deposit Calculator',
        'blurb': 'See the maturity value of a one-time deposit at the interest rate you enter.',
        'form': FDForm, 'run': run_fd,
        'value_label': 'Estimated maturity value',
        'basis': 'Rate entered by you (confirm with your bank)',
        'notes': [
            'Interest is compounded at the frequency you choose. Indian banks commonly use quarterly.',
            'Tax on interest (including TDS) is not deducted here.',
            'Premature withdrawal rules and penalties differ from bank to bank.',
        ],
    },
    'rd': {
        'title': 'Recurring Deposit Calculator',
        'blurb': 'Estimate the maturity value of depositing a fixed amount every month.',
        'form': RDForm, 'run': run_rd,
        'value_label': 'Estimated maturity value',
        'basis': 'Rate entered by you (confirm with your bank)',
        'notes': [
            'Each monthly deposit is made at the start of the month and compounds until maturity.',
            "Quarterly compounding is common for bank RDs. Your bank's own method may differ slightly.",
            'Tax on interest is not deducted here.',
        ],
    },
    'compound': {
        'title': 'Compound Interest Calculator',
        'blurb': 'See how a one-time amount grows when the interest is added back again and again.',
        'form': CompoundForm, 'run': run_compound,
        'value_label': 'Estimated future value',
        'basis': 'Rate entered by you (assumption)',
        'notes': [
            'Formula used: A = P x (1 + r/n)^(n x t).',
            'The result is only as realistic as the rate you enter.',
        ],
    },
}


@calc_bp.route('/')
@login_required
def index():
    return render_template('calculators/index.html', calculators=CALCULATORS)


@calc_bp.route('/<slug>', methods=['GET', 'POST'])
@login_required
def calculator(slug):
    cfg = CALCULATORS.get(slug)
    if cfg is None:
        abort(404)
    form = cfg['form']()
    result = None
    if form.validate_on_submit():
        result = cfg['run'](form)
    return render_template('calculators/calculator.html', cfg=cfg, slug=slug, form=form, result=result)