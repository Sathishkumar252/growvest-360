from app.services.investment_info import OPTIONS, BY_SLUG, AS_OF

REQUIRED = ['slug', 'name', 'tagline', 'risk', 'return_type', 'return_note', 'liquidity_level',
            'liquidity', 'duration', 'description', 'tax', 'advantages', 'disadvantages',
            'suitable', 'not_suitable', 'calculators']
RISKS = {'Low', 'Medium', 'Medium to High', 'High'}


def test_every_option_has_all_fields():
    for o in OPTIONS:
        for key in REQUIRED:
            assert o.get(key), f"{o.get('slug')} is missing {key}"


def test_slugs_are_unique_and_indexed():
    slugs = [o['slug'] for o in OPTIONS]
    assert len(slugs) == len(set(slugs))
    assert set(BY_SLUG) == set(slugs)


def test_risk_labels_are_known():
    for o in OPTIONS:
        assert o['risk'] in RISKS


def test_market_linked_options_never_claim_guarantees():
    for slug in ('mutual-funds', 'gold'):
        o = BY_SLUG[slug]
        assert 'not guaranteed' in o['return_type'].lower()


def test_as_of_date_is_set():
    assert AS_OF