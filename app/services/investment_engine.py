"""Deterministic investment maths (exact Decimal). Inga AI use pannala.

Ella functions-um 'months' vaangum. Ella returns-um ASSUMED / ENTERED rates-ku
estimate, guaranteed values illa.
"""
from decimal import Decimal, ROUND_HALF_UP

D = Decimal
CENT = D('0.01')
ZERO = D('0')


def money(x):
    return D(x).quantize(CENT, rounding=ROUND_HALF_UP)


def _pack(invested, future_value):
    invested = money(invested)
    future_value = money(future_value)
    returns = money(future_value - invested)
    gain_pct = money(returns / invested * 100) if invested > 0 else money(0)
    return {
        'invested': invested,
        'returns': returns,
        'future_value': future_value,
        'gain_pct': gain_pct,
    }


def sip(monthly, annual_rate, months):
    """Monthly SIP. Instalment ovvoru month-oda aarambathula (annuity-due),
    rate / 12 monthly compounding."""
    monthly, annual_rate = D(monthly), D(annual_rate)
    i = annual_rate / 100 / 12
    if i == 0:
        fv = monthly * months
    else:
        fv = monthly * (((1 + i) ** months - 1) / i) * (1 + i)
    return _pack(monthly * months, fv)


def compound(principal, annual_rate, months, freq=1):
    """Lump sum compound interest: A = P (1 + r/n)^(n t)."""
    principal, annual_rate = D(principal), D(annual_rate)
    base = 1 + annual_rate / 100 / freq
    exponent = D(freq) * D(months) / D(12)
    return _pack(principal, principal * base ** exponent)


def fd(principal, annual_rate, months, freq=4):
    """Fixed deposit. Indian banks-la usually quarterly compounding (freq=4)."""
    return compound(principal, annual_rate, months, freq)


def rd(monthly, annual_rate, months, freq=4):
    """Recurring deposit. Ovvoru month-oda aarambathula deposit,
    ovvoru instalment-um maturity varaikkum compound aagum."""
    monthly, annual_rate = D(monthly), D(annual_rate)
    base = 1 + annual_rate / 100 / freq
    total = ZERO
    for k in range(months):
        remaining_years = D(months - k) / D(12)
        total += monthly * base ** (D(freq) * remaining_years)
    return _pack(monthly * months, total)


def gold_lump(amount, annual_growth, months):
    """Gold lump sum, assumed constant yearly price growth."""
    return compound(amount, annual_growth, months, 1)


def gold_scenarios(amount, base_growth, months, spread=3):
    """Conservative / Base / Optimistic: user rate -/+ spread points (illustrative)."""
    base_growth = D(base_growth)
    out = []
    for name, g in (('Conservative', base_growth - spread),
                    ('Base', base_growth),
                    ('Optimistic', base_growth + spread)):
        r = gold_lump(amount, g, months)
        r.update({'scenario': name, 'rate': g})
        out.append(r)
    return out