from decimal import Decimal
from app.services.recommendation import build_plan, check_custom, investing_weights

CATS = {'rent': 8000, 'food': 6000}  # essentials 14,000


def amounts(plan):
    return {a['key']: a['amount'] for a in plan['allocations']}


def test_no_income_and_no_expenses_statuses():
    assert build_plan(0, CATS, 0)['status'] == 'no_income'
    assert build_plan(30000, {}, 0)['status'] == 'no_expenses'


def test_deficit_never_suggests_investing():
    p = build_plan(10000, CATS, 0)
    assert p['status'] == 'deficit'
    assert p['allocations'] == [] and p['invest_split'] == []


def test_tier_a_no_investing_until_first_safety_step():
    p = build_plan(35000, CATS, 0)          # 0 months saved
    a = amounts(p)
    assert p['emergency']['tier'] == 'A'
    assert a['invest'] == Decimal('0.00')
    assert a['emergency'] == Decimal('16800.00')   # 80% of 21,000
    assert a['buffer'] == Decimal('4200.00')
    assert p['invest_split'] == []


def test_tier_b_splits_surplus():
    p = build_plan(35000, CATS, 50000)      # about 3.6 months, target 6 months (84,000)
    a = amounts(p)
    assert p['emergency']['tier'] == 'B'
    assert a['emergency'] == Decimal('8400.00')    # 40%
    assert a['invest'] == Decimal('10500.00')      # 50%
    assert a['buffer'] == Decimal('2100.00')       # 10%


def test_tier_c_when_target_reached():
    p = build_plan(35000, CATS, 84000)
    a = amounts(p)
    assert p['emergency']['tier'] == 'C'
    assert a['emergency'] == Decimal('0.00')
    assert a['invest'] == Decimal('17850.00')      # 85% of 21,000


def test_emergency_allocation_is_capped_at_gap():
    p = build_plan(35000, CATS, 83000)      # gap only 1,000 (tier B)
    a = amounts(p)
    assert a['emergency'] == Decimal('1000.00')
    assert a['invest'] > Decimal('10500.00')       # the excess moves to investing


def test_allocations_always_add_up_to_surplus():
    for saved in (0, 20000, 50000, 83000, 84000, 200000):
        p = build_plan(41234.56, {'rent': 9000, 'food': 5432.1, 'other': 3000}, saved)
        assert sum(a['amount'] for a in p['allocations']) == p['surplus']
        if p['invest_split']:
            invest = [a for a in p['allocations'] if a['key'] == 'invest'][0]['amount']
            assert sum(s['amount'] for s in p['invest_split']) == invest


def test_investing_weights_follow_risk_and_horizon():
    assert investing_weights('medium', 10) == (40, 45, 15)
    assert investing_weights('high', 10) == (20, 65, 15)
    assert investing_weights('high', 4) == (55, 30, 15)
    assert investing_weights('high', 2) == (90, 0, 10)
    for risk in ('low', 'medium', 'high'):
        for h in (1, 3, 5, 20):
            assert sum(investing_weights(risk, h)) == 100


def test_high_emi_warning():
    p = build_plan(30000, {'rent': 5000, 'emi': 14000}, 0)   # 46.67% of income
    assert any('EMI' in w for w in p['warnings'])


def test_check_custom_blocks_overspending_and_warns_early_investing():
    p = build_plan(35000, CATS, 0)
    bad = check_custom(p, 10000, 10000, 5000)       # 25,000 > 21,000
    assert not bad['ok'] and bad['problems']
    warn = check_custom(p, 5000, 5000, 5000)
    assert warn['ok'] and warn['warnings'] and warn['remaining'] == Decimal('6000.00')