"""Unit tests for model provider abstraction and mock generator."""

import pytest

from forge.core.exceptions import ProviderAuthenticationError
from forge.core.logging import mask_secrets
from forge.core.model_provider import GeminiProvider, MockModelProvider
from forge.schemas.architecture import ArchitectureBlueprint
from forge.schemas.requirements import RequirementsDoc
from forge.schemas.security import ThreatModel


def test_mock_model_provider_schemas():
    provider = MockModelProvider()

    reqs = provider.generate_structured("Generate requirements", RequirementsDoc)
    assert isinstance(reqs, RequirementsDoc)
    assert len(reqs.functional_requirements) > 0

    arch = provider.generate_structured("Generate architecture", ArchitectureBlueprint)
    assert isinstance(arch, ArchitectureBlueprint)
    assert len(arch.components) > 0

    tm = provider.generate_structured("Generate threat model", ThreatModel)
    assert isinstance(tm, ThreatModel)
    assert len(tm.threats) > 0


def test_gemini_provider_auth_failure_without_key():
    with pytest.raises(ProviderAuthenticationError):
        GeminiProvider(api_key="")


def test_mask_secrets():
    raw_log = "Error connecting with api_key='AIzaSyAbCdEf1234567890123456789012345' and password='supersecretpassword'"
    masked = mask_secrets(raw_log)
    assert "AIzaSyAbCdEf" not in masked
    assert "[REDACTED]" in masked
    assert "supersecretpassword" not in masked
