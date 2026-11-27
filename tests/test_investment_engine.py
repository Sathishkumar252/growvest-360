from decimal import Decimal
from app.services.investment_engine import sip, fd, rd, compound, gold_scenarios


def test_sip_known_value():
    r = sip(5000, 12, 120)
    assert r['invested'] == Decimal('600000.00')
    assert r['future_value'] == Decimal('1161695.38')


def test_sip_zero_rate_equals_invested():
    r = sip(5000, 0, 120)
    assert r['future_value'] == r['invested'] == Decimal('600000.00')


def test_fd_one_year_quarterly():
    assert fd(100000, 7, 12)['future_value'] == Decimal('107185.90')


def test_compound_yearly():
    assert compound(100000, 10, 60, 1)['future_value'] == Decimal('161051.00')


def test_rd_one_year():
    assert rd(5000, '6.5', 12)['future_value'] == Decimal('62143.23')


def test_gold_scenarios_order_and_rates():
    s = gold_scenarios(100000, 8, 120)
    assert [x['scenario'] for x in s] == ['Conservative', 'Base', 'Optimistic']
    assert s[0]['future_value'] < s[1]['future_value'] < s[2]['future_value']
    assert s[1]['future_value'] == Decimal('215892.50')