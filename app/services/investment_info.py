"""Investment Hub content (static, reviewed by hand).

Tax rules, TDS limits and scheme rates change. Update AS_OF and the facts below
whenever a Union Budget or a quarterly small-savings notification changes them.
No guaranteed-return claims are made for market-linked products.
"""

AS_OF = '28 November 2026'

REVIEW_NOTE = (
    'Compiled on ' + AS_OF + ' from public sources, mainly news and financial-education websites, '
    'not from official tax notifications. Tax laws, TDS limits and scheme rates change (the next Union '
    'Budget is expected in early 2027, and small-savings rates are reviewed every quarter). Please confirm '
    'on incometax.gov.in, the Ministry of Finance or India Post, or with a qualified tax professional '
    'before you act. GrowVest 360 is an educational tool and does not give regulated investment advice.'
)

CALC_SIP = ('SIP calculator', 'calculators.calculator', {'slug': 'sip'})
CALC_FD = ('FD calculator', 'calculators.calculator', {'slug': 'fd'})
CALC_RD = ('RD calculator', 'calculators.calculator', {'slug': 'rd'})
CALC_COMPOUND = ('Compound interest calculator', 'calculators.calculator', {'slug': 'compound'})
CALC_GOLD = ('Gold scenario calculator', 'advanced.gold', {})
CALC_COMPARE = ('Compare options', 'advanced.compare', {})

OPTIONS = [
    {
        'slug': 'mutual-funds',
        'name': 'Mutual Funds and SIP',
        'tagline': 'Pool your money with other investors in a professionally managed fund. A SIP invests a fixed amount every month.',
        'risk': 'High',
        'return_type': 'Market-linked (not guaranteed)',
        'return_note': 'There is no fixed or guaranteed return. Equity fund returns change every year and can be negative over a given period. In the SIP calculator, use a cautious assumed rate and also test a low-return case.',
        'liquidity_level': 'High',
        'liquidity': 'Units can usually be redeemed on any working day. ELSS (tax-saving) funds have a 3-year lock-in, and some funds charge an exit load if you leave early.',
        'duration': 'Equity funds are usually considered for 5 years or more.',
        'description': 'A mutual fund collects money from many people and invests it in shares, bonds or both. With a SIP you invest a fixed amount every month, which spreads your purchases across market ups and downs. Debt funds usually swing less than equity funds, but they are not risk-free.',
        'tax': [
            'Equity-oriented funds (more than 65% in Indian shares): gains from units sold within 12 months are taxed at 20%. Gains after 12 months are taxed at 12.5% on the amount above Rs 1.25 lakh in a financial year.',
            'Debt funds bought after 1 April 2023: gains are taxed at your income-tax slab rate, whatever the holding period.',
            'Budget 2026 left these capital gains rates unchanged for FY 2026-27.',
        ],
        'advantages': [
            'You can start with a small monthly amount.',
            'Professional management and built-in diversification.',
            'A SIP builds a regular saving habit.',
            'Fund value (NAV) is published every day, so it is transparent.',
        ],
        'disadvantages': [
            'The value can fall, especially over short periods.',
            'No guaranteed return.',
            'Fund fees (expense ratio) reduce your returns.',
            'Needs patience, and the large choice of funds can be confusing.',
        ],
        'suitable': [
            'A long time horizon (usually 5 years or more).',
            'You can stay invested when markets fall.',
            'You already have an emergency fund.',
            'You have regular monthly income to invest.',
        ],
        'not_suitable': [
            'Money you need within a few years.',
            'Your emergency fund.',
            'If a market fall would make you panic and sell.',
        ],
        'calculators': [CALC_SIP, CALC_COMPARE],
    },
    {
        'slug': 'gold',
        'name': 'Gold',
        'tagline': 'Buy gold as jewellery, coins, digital gold, a gold ETF or a Sovereign Gold Bond. Your gain depends on the gold price.',
        'risk': 'Medium to High',
        'return_type': 'Price-linked (not guaranteed)',
        'return_note': 'Gold pays no interest on its own, so your gain depends only on the change in gold price. Prices can rise or fall for long periods. Sovereign Gold Bonds also paid 2.5% yearly interest.',
        'liquidity_level': 'Medium',
        'liquidity': 'Gold ETFs trade on exchanges and are easy to sell. Physical gold can be sold, but jewellery loses value through making charges. Sovereign Gold Bonds run for 8 years, and early exit is possible only through RBI redemption windows.',
        'duration': 'Usually held for the long term. Gold prices can stay flat or fall for years.',
        'description': 'Gold has been a familiar store of value for centuries and is often used to diversify a portfolio. You can hold it physically or through paper forms like ETFs and bonds, which avoid storage worries.',
        'tax': [
            'Physical and digital gold: if sold after 24 months, the gain is taxed at 12.5% without indexation. If sold earlier, the gain is added to your income and taxed at your slab rate.',
            'Gold ETFs: if sold after 12 months, the gain is taxed at 12.5% without indexation (the Rs 1.25 lakh equity exemption does not apply). If sold earlier, slab rate.',
            'Sovereign Gold Bonds: from 1 April 2026, the capital gains exemption on redemption applies only to people who subscribed in the original RBI issue and held the bond until the 8-year maturity. The 2.5% yearly interest is taxable.',
            'GST and making charges apply when you buy physical gold.',
        ],
        'advantages': [
            'A different kind of asset that can balance a portfolio.',
            'Easy to understand.',
            'ETFs and bonds avoid storage and purity worries.',
            'You can buy in small amounts.',
        ],
        'disadvantages': [
            'No regular income (except the interest on Sovereign Gold Bonds).',
            'Prices can swing and stay low for years.',
            'Making charges and GST on physical gold reduce your return.',
            'Physical gold needs safe storage.',
        ],
        'suitable': [
            'You want some diversification next to other investments.',
            'A medium to long horizon.',
            'You are comfortable with price swings.',
        ],
        'not_suitable': [
            'You need steady income.',
            'Short-term goals.',
            'Putting all your savings into one asset.',
        ],
        'calculators': [CALC_GOLD, CALC_COMPARE],
    },
    {
        'slug': 'fixed-deposit',
        'name': 'Fixed Deposit (FD)',
        'tagline': 'Deposit a lump sum with a bank for a fixed period and earn interest at a rate fixed when you open the FD.',
        'risk': 'Low',
        'return_type': 'Fixed by the bank when you open the FD',
        'return_note': 'The rate depends on the bank and the tenure and is locked for that FD. Rates for new FDs change over time, so always check the bank current rate.',
        'liquidity_level': 'Medium',
        'liquidity': 'You can usually break an FD early, but banks may charge a penalty or pay a lower rate. Tax-saver FDs have a 5-year lock-in.',
        'duration': 'From a few months to several years, chosen by you.',
        'description': 'An FD is one of the simplest ways to earn a known return. You deposit money for a period you choose, and the bank pays interest at the agreed rate.',
        'tax': [
            'Interest is added to your income and taxed at your slab rate.',
            'The bank deducts 10% TDS if your interest from that bank is more than Rs 50,000 in a financial year (Rs 1 lakh for senior citizens). TDS is not the final tax.',
            'From 1 April 2026, Form 121 replaces Forms 15G and 15H for asking the bank not to deduct TDS, if you are eligible.',
            'A 5-year tax-saver FD can qualify for a Section 80C deduction only in the old tax regime.',
        ],
        'advantages': [
            'A known return, so it is easy to plan.',
            'Low risk, and bank deposits are insured by DICGC up to Rs 5 lakh per depositor per bank.',
            'You choose the tenure.',
            'Very simple to understand and open.',
        ],
        'disadvantages': [
            'Interest is fully taxable.',
            'The return may not beat inflation after tax.',
            'Early withdrawal can cost you a penalty.',
            'If rates fall, you have to reinvest at lower rates later.',
        ],
        'suitable': [
            'A goal with a known date.',
            'You prefer low risk.',
            'Short to medium term goals.',
        ],
        'not_suitable': [
            'Long-term growth where inflation matters a lot.',
            'Money you may need at short notice.',
        ],
        'calculators': [CALC_FD, CALC_COMPOUND],
    },
    {
        'slug': 'recurring-deposit',
        'name': 'Recurring Deposit (RD)',
        'tagline': 'Deposit a fixed amount every month for a fixed period at a rate fixed when you open the RD.',
        'risk': 'Low',
        'return_type': 'Fixed by the bank when you open the RD',
        'return_note': 'The rate depends on the bank and the tenure. Check the current RD rate with your bank before you start.',
        'liquidity_level': 'Medium',
        'liquidity': 'Closing an RD early usually lowers the interest and may carry a penalty. Rules differ by bank.',
        'duration': 'You choose the tenure when you open the RD.',
        'description': 'An RD works like a monthly saving plan with a bank. It suits people who earn monthly and want a disciplined, low-risk way to build a lump sum.',
        'tax': [
            'Interest is added to your income and taxed at your slab rate.',
            'TDS rules similar to FDs apply to RD interest when the interest from a bank crosses the annual limit (Rs 50,000, or Rs 1 lakh for senior citizens).',
        ],
        'advantages': [
            'Builds a regular saving habit with small amounts.',
            'The rate is fixed, so the result is predictable.',
            'Low risk.',
        ],
        'disadvantages': [
            'Interest is taxable.',
            'Returns are modest and may not beat inflation.',
            'Missing instalments can lead to a penalty, depending on the bank.',
            'The rate stays fixed even if market rates rise later.',
        ],
        'suitable': [
            'Regular monthly income and a goal within a few years.',
            'You want a simple, low-risk habit.',
        ],
        'not_suitable': [
            'Long-term wealth building where inflation matters.',
            'Irregular income that may make monthly deposits hard.',
        ],
        'calculators': [CALC_RD, CALC_COMPARE],
    },
    {
        'slug': 'government-schemes',
        'name': 'Government Savings Schemes (PPF, NSC and others)',
        'tagline': 'Savings schemes run by the Government of India, mostly through post offices and banks, with rates notified every quarter.',
        'risk': 'Low',
        'return_type': 'Rate notified by the government every quarter',
        'return_note': 'For October to December 2026 the notified rates are: PPF 7.1%, NSC 7.7%, Sukanya Samriddhi 8.2%, Kisan Vikas Patra 7.5% and Post Office Savings Account 4%. The government reviews these every quarter, so the PPF rate can change after 31 December 2026. NSC and KVP rates are fixed for the certificate when you buy it.',
        'liquidity_level': 'Low',
        'liquidity': 'PPF has a 15-year tenure and NSC has a 5-year lock-in. Early and partial withdrawals follow strict scheme rules, so check the current rules.',
        'duration': 'PPF: 15 years. NSC: 5 years. KVP: matures in 115 months at the current rate.',
        'description': 'These schemes are backed by the government and aimed at long-term, safe saving. PPF is popular for retirement and long-term goals because the interest is compounded every year.',
        'tax': [
            'PPF is widely treated as tax-free on interest and maturity. The investment qualifies for a Section 80C deduction only in the old tax regime.',
            'NSC and KVP interest is generally taxable. Check the current rules before you invest.',
            'Rates and rules can change in the Union Budget or the quarterly rate review.',
        ],
        'advantages': [
            'Government-backed, so very low risk.',
            'Rates are usually higher than a savings account.',
            'PPF interest is compounded every year, which suits long-term goals.',
            'Encourages long-term discipline.',
        ],
        'disadvantages': [
            'Long lock-in periods.',
            'The PPF rate can change every quarter.',
            'There are yearly deposit limits.',
            'Returns may trail equity over very long periods and may not beat inflation by much.',
        ],
        'suitable': [
            'A safe base for long-term goals such as retirement.',
            'You do not need the money for many years.',
        ],
        'not_suitable': [
            'Money you may need soon.',
            'If you want market-linked growth.',
        ],
        'calculators': [CALC_COMPOUND, CALC_COMPARE],
    },
    {
        'slug': 'savings-account',
        'name': 'Savings Account',
        'tagline': 'Keep money in a bank account for everyday needs, with instant access and low interest.',
        'risk': 'Low',
        'return_type': 'Set by the bank (can change anytime)',
        'return_note': 'As reported in September 2026, large banks paid around 2.5% a year and the post office savings account pays 4%. Some small finance banks pay more. Check your own bank.',
        'liquidity_level': 'Very high',
        'liquidity': 'You can usually withdraw the same day, with no lock-in.',
        'duration': 'No fixed period.',
        'description': 'A savings account is the safest and most flexible place for money you may need soon, such as the first part of your emergency fund and your upcoming bills.',
        'tax': [
            'Interest is added to your income and taxed at your slab rate.',
            'A deduction of up to Rs 10,000 on savings interest under Section 80TTA is available only in the old tax regime, for people below 60.',
        ],
        'advantages': [
            'Instant access to your money.',
            'Very low risk, and deposits are insured by DICGC up to Rs 5 lakh per depositor per bank.',
            'No lock-in.',
        ],
        'disadvantages': [
            'The lowest returns, usually below inflation.',
            'Some accounts have minimum balance rules or charges.',
        ],
        'suitable': [
            'Day-to-day money and bills.',
            'The first part of your emergency fund.',
        ],
        'not_suitable': [
            'Long-term growth.',
            'Keeping large amounts idle for years.',
        ],
        'calculators': [CALC_COMPARE],
    },
]

BY_SLUG = {o['slug']: o for o in OPTIONS}