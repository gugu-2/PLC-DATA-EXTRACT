import pytest
from core.domains import domain_manager, DOMAINS


def test_domains_catalog_integrity():
    assert len(DOMAINS) >= 10
    for d in DOMAINS:
        assert d.id
        assert d.name
        assert d.function_block_name.startswith("FB_")
        assert len(d.required_input_units) >= 5
        assert len(d.required_output_units) >= 5
        assert len(d.typical_states) >= 3


def test_domain_manager_sampling():
    sampled = domain_manager.sample(5)
    assert len(sampled) == 5

    single = domain_manager.get_random()
    assert single in DOMAINS
