"""Rule-based budget recommendation engine (deterministic, no AI).

Output is a rule-of-thumb starting split of your monthly surplus. It is educational,
not regulated investment advice. Essential spending and the emergency fund come first.
"""
from decimal import Decimal, ROUND_HALF_UP

D = Decimal
CENT = D('0.01')
ZERO = D('0')

ESSENTIAL_CATEGORIES = {'rent', 'food', 'transport', 'utilities', 'education', 'emi', 'family'}

# Surplus split by emergency-fund stage: (emergency %, investing %, wants/flexibility %)
TIER_PCT = {'A': (80, 0, 20), 'B': (40, 50, 10), 'C': (0, 85, 15)}

# Investing split by risk comfort: (safe deposits %, equity SIP %, gold %)
RISK_BASE = {'low': (75, 15, 10), 'medium': (40, 45, 15), 'high': (20, 65, 15)}

INVEST_BUCKETS = {
    'safe': {'label': 'Safe deposits (RD, FD, PPF)', 'hub': ['recurring-deposit', 'fixed-deposit', 'government-schemes']},
    'equity': {'label': 'Equity mutual fund SIP', 'hub': ['mutual-funds']},
    'gold': {'label': 'Gold', 'hub': ['gold']},
}


def money(x):
    return D(x).quantize(CENT, rounding=ROUND_HALF_UP)


def rs(x):
    return 'Rs {:,.2f}'.format(money(x))


def investing_weights(risk, horizon_years):
    """(safe, equity, gold) whole percentages that add up to 100."""
    safe, equity, gold = RISK_BASE.get(risk, RISK_BASE['medium'])
    if horizon_years < 3:
        equity_cap, gold_cap = 0, 10
    elif horizon_years < 5:
        equity_cap, gold_cap = 30, 100
    else:
        equity_cap, gold_cap = 100, 100
    if equity > equity_cap:
        safe += equity - equity_cap
        equity = equity_cap
    if gold > gold_cap:
        safe += gold - gold_cap
        gold = gold_cap
    return safe, equity, gold


def _tier(saved, base, target_months):
    """A: below the first safety step, B: building towards target, C: target reached."""
    target = money(base * target_months)
    first_step = money(base * min(D(3), D(target_months)))
    if saved < first_step:
        return 'A', target
    if saved < target:
        return 'B', target
    return 'C', target


def build_plan(income, by_category, saved_emergency, risk='medium', horizon_years=5,
               target_months=6, family_members=1):
    income = money(income)
    saved = money(saved_emergency)
    by_category = {k: money(v) for k, v in by_category.items()}

    essentials = money(sum((v for k, v in by_category.items() if k in ESSENTIAL_CATEGORIES), ZERO))
    flexible = money(sum((v for k, v in by_category.items() if k not in ESSENTIAL_CATEGORIES), ZERO))
    expenses = money(essentials + flexible)
    surplus = money(income - expenses)
    emi = by_category.get('emi', ZERO)

    plan = {
        'status': 'ok', 'income': income, 'expenses': expenses, 'essentials': essentials,
        'flexible': flexible, 'surplus': surplus, 'saved': saved,
        'risk': risk, 'horizon_years': horizon_years, 'target_months': target_months,
        'emergency': None, 'allocations': [], 'invest_split': [], 'warnings': [],
    }

    if income <= 0:
        plan['status'] = 'no_income'
        return plan
    if expenses <= 0:
        plan['status'] = 'no_expenses'
        return plan

    base = essentials if essentials > 0 else expenses
    months_saved = (saved / base).quantize(D('0.1'), rounding=ROUND_HALF_UP)
    tier, target = _tier(saved, base, target_months)
    gap = money(max(ZERO, target - saved))
    plan['emergency'] = {'target': target, 'saved': saved, 'gap': gap, 'months_saved': months_saved,
                         'target_months': target_months, 'tier': tier, 'base': base}

    emi_pct = money(emi / income * 100)
    if emi_pct >= 40:
        plan['warnings'].append(
            'Your EMIs are about {}% of your income. Many lenders and planners treat 40% or more as a high EMI burden.'.format(emi_pct))
    if family_members >= 3 and target_months < 6:
        plan['warnings'].append(
            'You support {} people. Many planners suggest an emergency fund at the higher end (6 months) for families.'.format(family_members))
    if risk == 'high' and horizon_years < 5:
        plan['warnings'].append(
            'Your investment horizon is under 5 years, so the equity share is reduced even though your risk comfort is high.')

    if surplus <= 0:
        plan['status'] = 'deficit'
        return plan

    e_pct, i_pct, b_pct = TIER_PCT[tier]
    emergency_amt = min(gap, money(surplus * e_pct / 100))
    excess = money(surplus * e_pct / 100 - emergency_amt)
    invest_amt = money(surplus * i_pct / 100 + (excess if tier != 'A' else ZERO))
    buffer_amt = money(surplus - emergency_amt - invest_amt)

    if tier == 'A':
        e_why = ('Your emergency fund covers about {} months of essential spending. Building it to at least '
                 '{} months comes first, so nothing is suggested for investing yet.').format(
                     months_saved, min(3, target_months))
        i_why = 'Investing waits until your emergency fund reaches the first safety step.'
    elif tier == 'B':
        e_why = ('Your emergency fund covers about {} months. A target of {} months is {} away, so a large part '
                 'of your surplus keeps topping it up.').format(months_saved, target_months, rs(gap))
        i_why = 'The first safety step is done, so part of the surplus can start working for your longer-term goals.'
    else:
        e_why = 'Your emergency fund has reached its {}-month target, so you only need to keep it topped up as expenses grow.'.format(target_months)
        i_why = 'Your essentials and emergency fund are covered, so most of the surplus can go towards your goals.'
    b_why = 'Money for wants and flexibility keeps the plan realistic. A plan that feels too strict is hard to follow.'

    def pct_of_surplus(amount):
        return money(amount / surplus * 100)

    plan['allocations'] = [
        {'key': 'emergency', 'label': 'Emergency fund', 'amount': emergency_amt, 'pct': pct_of_surplus(emergency_amt), 'why': e_why},
        {'key': 'invest', 'label': 'Investing for goals', 'amount': invest_amt, 'pct': pct_of_surplus(invest_amt), 'why': i_why},
        {'key': 'buffer', 'label': 'Wants and flexibility', 'amount': buffer_amt, 'pct': pct_of_surplus(buffer_amt), 'why': b_why},
    ]

    if invest_amt > 0:
        w_safe, w_equity, w_gold = investing_weights(risk, horizon_years)
        whys = {
            'safe': 'Steady, lower-risk options for money you may need sooner or want to protect.',
            'equity': 'Market-linked growth over the long term, with no guaranteed return and real chances of falls.',
            'gold': 'A smaller share to diversify. Gold prices can swing and can stay flat for years.',
        }
        if horizon_years < 3:
            whys['equity'] = 'Equity is not suggested for a horizon under 3 years because short-term falls are common.'
        elif horizon_years < 5:
            whys['equity'] = 'Equity share is capped at 30% because your horizon is under 5 years.'
        parts = []
        used = ZERO
        keys = ['safe', 'equity', 'gold']
        for idx, (key, w) in enumerate(zip(keys, (w_safe, w_equity, w_gold))):
            amount = money(invest_amt - used) if idx == len(keys) - 1 else money(invest_amt * w / 100)
            used += amount
            parts.append({'key': key, 'label': INVEST_BUCKETS[key]['label'], 'weight': w, 'amount': amount,
                          'why': whys[key], 'hub': INVEST_BUCKETS[key]['hub']})
        plan['invest_split'] = parts
    return plan


def check_custom(plan, emergency, invest, buffer):
    """Validate a split the user adjusted by hand."""
    emergency, invest, buffer = money(emergency), money(invest), money(buffer)
    total = money(emergency + invest + buffer)
    surplus = plan['surplus']
    problems, warnings = [], []
    if total > surplus:
        problems.append(
            'Your split adds up to {}, which is {} more than your monthly surplus of {}. '
            'Money needed for essential expenses should not be invested.'.format(rs(total), rs(total - surplus), rs(surplus)))
    em = plan['emergency']
    if invest > 0 and em and em['tier'] == 'A':
        warnings.append(
            'You are investing while your emergency fund is below the first safety step. '
            'Many planners suggest building the emergency fund first.')
    if em and emergency > em['gap'] > 0:
        warnings.append('You are putting {} into the emergency fund, which is more than the {} still needed to reach your target.'.format(rs(emergency), rs(em['gap'])))
    return {'total': total, 'remaining': money(surplus - total), 'problems': problems,
            'warnings': warnings, 'ok': not problems}