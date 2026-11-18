"""Unit tests for OWASP and STRIDE mitigation catalog mappings."""

import pytest

from forge.schemas.security import STRIDECategory
from forge.security.mitigation import MitigationCatalog


@pytest.mark.parametrize("category", [c.value for c in STRIDECategory])
def test_all_stride_categories_have_owasp_mappings(category: str) -> None:
    """Verify every STRIDE category has an assigned OWASP reference."""
    mapping = MitigationCatalog.get_owasp_mapping(category)
    assert mapping is not None, f"Category {category} missing OWASP mapping"
    assert "OWASP" in mapping


@pytest.mark.parametrize("category", [c.value for c in STRIDECategory])
def test_all_stride_categories_have_recommended_controls(category: str) -> None:
    """Verify every STRIDE category has at least 3 actionable security controls."""
    controls = MitigationCatalog.get_controls_for_category(category)
    assert len(controls) >= 3, f"Category {category} has fewer than 3 controls"
    for ctrl in controls:
        assert len(ctrl.strip()) > 10


def test_mitigation_catalog_case_insensitivity() -> None:
    """Verify lower-case category queries return correct OWASP mapping."""
    assert MitigationCatalog.get_owasp_mapping("spoofing") == MitigationCatalog.get_owasp_mapping("SPOOFING")
    assert MitigationCatalog.get_controls_for_category("tampering") == MitigationCatalog.get_controls_for_category("TAMPERING")


def test_mitigation_catalog_unknown_category() -> None:
    """Verify unknown category yields None and empty controls."""
    assert MitigationCatalog.get_owasp_mapping("UNKNOWN_CATEGORY") is None
    assert MitigationCatalog.get_controls_for_category("UNKNOWN_CATEGORY") == []
