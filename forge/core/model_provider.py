"""Model provider abstraction and implementations (Gemini & Mock)."""

import json
import random
import time
from abc import ABC, abstractmethod
from typing import Any, TypeVar

from pydantic import BaseModel

from forge.core.config import settings
from forge.core.exceptions import (
    ModelProviderError,
    ProviderAuthenticationError,
    ProviderTimeoutError,
    SchemaValidationError,
)
from forge.core.logging import logger

T = TypeVar("T", bound=BaseModel)


class ProviderResponse(BaseModel):
    """Encapsulated response from a model provider."""

    content: str
    model_name: str
    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    total_tokens: int | None = None
    latency_seconds: float = 0.0
    finish_reason: str | None = None


class ModelProvider(ABC):
    """Abstract base provider for LLM integrations."""

    def __init__(
        self, model_name: str, temperature: float = 0.2, timeout: int = 60, max_retries: int = 3
    ):
        self.model_name = model_name
        self.temperature = temperature
        self.timeout = timeout
        self.max_retries = max_retries

    @abstractmethod
    def generate_text(self, prompt: str, system_instruction: str | None = None) -> ProviderResponse:
        """Generate unstructured text response."""
        pass

    @abstractmethod
    def generate_structured(
        self, prompt: str, response_schema: type[T], system_instruction: str | None = None
    ) -> T:
        """Generate and parse structured response conforming to a Pydantic schema."""
        pass


class MockModelProvider(ModelProvider):
    """Deterministic mock provider for offline testing, benchmarks, and CI/CD."""

    def __init__(self, model_name: str = "mock-forge-v1", temperature: float = 0.0, **kwargs):
        super().__init__(model_name, temperature=temperature, **kwargs)
        self.call_history: list = []

    def generate_text(self, prompt: str, system_instruction: str | None = None) -> ProviderResponse:
        self.call_history.append({"prompt": prompt, "system": system_instruction})
        return ProviderResponse(
            content=f"MOCK_RESPONSE to: {prompt[:40]}...",
            model_name=self.model_name,
            prompt_tokens=len(prompt.split()),
            completion_tokens=20,
            total_tokens=len(prompt.split()) + 20,
            latency_seconds=0.01,
        )

    def generate_structured(
        self, prompt: str, response_schema: type[T], system_instruction: str | None = None
    ) -> T:
        self.call_history.append({"prompt": prompt, "schema": response_schema.__name__})
        schema_name = response_schema.__name__

        # Deterministic generation tailored to schema types
        if schema_name == "RequirementsDoc":
            data: dict[str, Any] = {
                "document_id": "REQ-DOC-MOCK-001",
                "project_id": "PRJ-001",
                "executive_summary": "Synthesized strategy and requirements analysis for target objective.",
                "functional_requirements": [
                    {
                        "requirement_id": "FR-001",
                        "description": "Ingest and process incoming streaming events with schema validation.",
                        "priority": "CRITICAL",
                        "acceptance_criteria": [
                            "Validate against JSON schema",
                            "Reject malformed events",
                        ],
                        "source": "EXPLICIT",
                    },
                    {
                        "requirement_id": "FR-002",
                        "description": "Expose authenticated query API for real-time analytics aggregation.",
                        "priority": "HIGH",
                        "acceptance_criteria": [
                            "Return p99 aggregated metrics",
                            "Enforce role based access control",
                        ],
                        "source": "EXPLICIT",
                    },
                    {
                        "requirement_id": "FR-003",
                        "description": "Persist historical events to durable distributed cold storage.",
                        "priority": "MEDIUM",
                        "acceptance_criteria": [
                            "Write to parquet batches",
                            "Partition by date and tenant",
                        ],
                        "source": "INFERRED",
                    },
                ],
                "non_functional_requirements": [
                    {
                        "requirement_id": "NFR-001",
                        "category": "PERFORMANCE",
                        "description": "API query response latency under peak load.",
                        "measurable_target": "< 150ms p95 latency at 10k QPS",
                        "priority": "HIGH",
                        "source": "EXPLICIT",
                    },
                    {
                        "requirement_id": "NFR-002",
                        "category": "RELIABILITY",
                        "description": "System availability target.",
                        "measurable_target": "99.95% annual uptime",
                        "priority": "CRITICAL",
                        "source": "EXPLICIT",
                    },
                    {
                        "requirement_id": "NFR-003",
                        "category": "SECURITY",
                        "description": "Zero trust inter-service transport encryption.",
                        "measurable_target": "mTLS with AES-256 for all internal links",
                        "priority": "CRITICAL",
                        "source": "EXPLICIT",
                    },
                ],
                "constraints": [
                    {
                        "constraint_id": "CON-001",
                        "category": "TECHNICAL",
                        "description": "Must be deployable on containerized Kubernetes infrastructure.",
                        "mandatory": True,
                        "source": "EXPLICIT",
                    },
                    {
                        "constraint_id": "CON-002",
                        "category": "REGULATORY",
                        "description": "Strict compliance with GDPR and audit trail retention.",
                        "mandatory": True,
                        "source": "EXPLICIT",
                    },
                ],
                "missing_information": ["Target cold-storage backup retention period"],
                "ambiguous_requirements": ["Peak event burst burstiness profile"],
                "contradictions": [],
                "assumptions": ["Underlying cloud infrastructure provides VPC isolation"],
            }
            return response_schema.model_validate(data)

        elif schema_name == "ArchitectureBlueprint":
            arch_data: dict[str, Any] = {
                "architecture_id": "ARCH-MOCK-001",
                "title": "Scalable Event Ingestion & Analytics Architecture",
                "overview": "A distributed, decoupled event streaming platform built with API Gateway, Event Ingestion Bus, Processing Pipeline, and PostgreSQL/Redis storage.",
                "components": [
                    {
                        "component_id": "COMP-001",
                        "name": "API Gateway Service",
                        "responsibility": "Reverse proxy, rate limiting, and client authentication.",
                        "technology": "Envoy / FastAPI",
                        "interfaces": [
                            {
                                "interface_id": "INT-001",
                                "name": "REST Ingestion Endpoint",
                                "protocol": "HTTPS",
                                "description": "Public HTTPS event receiver",
                            }
                        ],
                        "dependencies": ["COMP-002"],
                        "related_requirements": ["FR-001", "NFR-001", "CON-001"],
                    },
                    {
                        "component_id": "COMP-002",
                        "name": "Event Ingestion Bus",
                        "responsibility": "Durable buffer and high-throughput streaming message bus.",
                        "technology": "Apache Kafka",
                        "interfaces": [
                            {
                                "interface_id": "INT-002",
                                "name": "Kafka Producer Topic",
                                "protocol": "Kafka TCP",
                                "description": "Partitioned event topic",
                            }
                        ],
                        "dependencies": [],
                        "related_requirements": ["FR-001", "NFR-002"],
                    },
                    {
                        "component_id": "COMP-003",
                        "name": "Stream Processing Worker",
                        "responsibility": "Consumes raw events, validates schemas, and writes aggregated metrics.",
                        "technology": "Python / Apache Flink",
                        "interfaces": [],
                        "dependencies": ["COMP-002", "COMP-004"],
                        "related_requirements": ["FR-001", "FR-003"],
                    },
                    {
                        "component_id": "COMP-004",
                        "name": "Analytical Database",
                        "responsibility": "Durable ACID storage for aggregated reports and events.",
                        "technology": "PostgreSQL with TimescaleDB",
                        "interfaces": [
                            {
                                "interface_id": "INT-003",
                                "name": "SQL Connection Pool",
                                "protocol": "PostgreSQL Wire Protocol",
                                "description": "Database queries",
                            }
                        ],
                        "dependencies": [],
                        "related_requirements": ["FR-002", "NFR-002", "CON-002"],
                    },
                ],
                "data_flows": [
                    {
                        "flow_id": "FLOW-001",
                        "source_component_id": "COMP-001",
                        "target_component_id": "COMP-002",
                        "protocol": "Kafka TCP",
                        "data_payload": "Validated JSON event payload",
                        "description": "API Gateway publishes raw events to Kafka",
                    },
                    {
                        "flow_id": "FLOW-002",
                        "source_component_id": "COMP-003",
                        "target_component_id": "COMP-004",
                        "protocol": "TCP / SQL",
                        "data_payload": "Processed aggregation records",
                        "description": "Worker writes batch aggregations to PostgreSQL",
                    },
                ],
                "deployment_model": "CONTAINERIZED",
                "technology_choices": [
                    {
                        "technology": "Apache Kafka",
                        "category": "Message Bus",
                        "rationale": "High throughput, partitioned persistence with replayability.",
                        "alternatives_considered": ["RabbitMQ", "AWS SQS"],
                        "tradeoffs": ["Operational complexity in exchange for extreme throughput"],
                    },
                    {
                        "technology": "PostgreSQL / TimescaleDB",
                        "category": "Relational & Time Series Database",
                        "rationale": "Strong consistency, ACID transactions, and fast time-series analytical queries.",
                        "alternatives_considered": ["MongoDB", "Cassandra"],
                        "tradeoffs": [
                            "Horizontal write scaling requires sharding compared to Cassandra"
                        ],
                    },
                ],
                "tradeoffs": [
                    {
                        "dimension": "Consistency vs Latency",
                        "decision": "Eventual consistency for analytics with at-least-once streaming delivery",
                        "pros": ["Extremely high throughput and resilient buffering"],
                        "cons": ["Small reconciliation window before metrics appear in dashboard"],
                    }
                ],
                "assumptions": ["Cluster runs in multi-zone cloud setup"],
                "risks": ["Kafka broker partition skew under abnormal traffic spikes"],
                "requirement_mapping": {
                    "FR-001": ["COMP-001", "COMP-002", "COMP-003"],
                    "FR-002": ["COMP-001", "COMP-004"],
                    "FR-003": ["COMP-003", "COMP-004"],
                    "NFR-001": ["COMP-001"],
                    "NFR-002": ["COMP-002", "COMP-004"],
                    "NFR-003": ["COMP-001", "COMP-002", "COMP-003", "COMP-004"],
                    "CON-001": ["COMP-001"],
                    "CON-002": ["COMP-004"],
                },
            }
            return response_schema.model_validate(arch_data)

        elif schema_name == "ThreatModel":
            tm_data: dict[str, Any] = {
                "threat_model_id": "TM-MOCK-001",
                "project_id": "PRJ-001",
                "threats": [
                    {
                        "threat_id": "THR-001",
                        "category": "DENIAL_OF_SERVICE",
                        "affected_component_id": "COMP-001",
                        "attack_scenario": "Adversary floods public API gateway with volumetric HTTP requests, starving compute resources.",
                        "likelihood": "HIGH",
                        "impact": "HIGH",
                        "severity": "HIGH",
                        "risk_score": 7.5,
                        "mitigation": {
                            "mitigation_id": "MIT-001",
                            "description": "Implement token-bucket rate limiting, IP throttling, and Cloudflare DDoS protection.",
                            "owasp_mapping": "OWASP API4:2023-Unrestricted Resource Consumption",
                            "verification_method": "Load testing with rate-limit assertions",
                        },
                        "residual_risk": "LOW",
                        "owasp_reference": "API4:2023",
                    },
                    {
                        "threat_id": "THR-002",
                        "category": "TAMPERING",
                        "affected_component_id": "COMP-002",
                        "attack_scenario": "Adversary injects malicious forged messages directly into unauthenticated Kafka topic.",
                        "likelihood": "MEDIUM",
                        "impact": "HIGH",
                        "severity": "HIGH",
                        "risk_score": 7.0,
                        "mitigation": {
                            "mitigation_id": "MIT-002",
                            "description": "Enforce SASL/SCRAM authentication, TLS encryption, and ACLs on all Kafka topics.",
                            "owasp_mapping": "OWASP A07:2021-Identification and Authentication Failures",
                            "verification_method": "Broker configuration audit and connection rejection tests",
                        },
                        "residual_risk": "LOW",
                        "owasp_reference": "A07:2021",
                    },
                    {
                        "threat_id": "THR-003",
                        "category": "INFORMATION_DISCLOSURE",
                        "affected_component_id": "COMP-004",
                        "attack_scenario": "SQL injection in query API allows unauthorized exfiltration of customer event logs.",
                        "likelihood": "LOW",
                        "impact": "HIGH",
                        "severity": "MEDIUM",
                        "risk_score": 5.0,
                        "mitigation": {
                            "mitigation_id": "MIT-003",
                            "description": "Use parameterized queries via SQLAlchemy ORM; eliminate raw SQL concatenation.",
                            "owasp_mapping": "OWASP A03:2021-Injection",
                            "verification_method": "Static code analysis (Bandit) and SQLMap penetration test",
                        },
                        "residual_risk": "LOW",
                        "owasp_reference": "A03:2021",
                    },
                ],
                "attack_surfaces": [
                    {
                        "surface_id": "SURF-001",
                        "name": "Public API Ingestion Gateway",
                        "exposure_type": "Public Internet",
                        "description": "HTTPS port 443 accessible to external clients",
                        "protected_by": ["WAF", "TLS 1.3", "Rate Limiter", "JWT Auth"],
                    }
                ],
                "overall_risk_posture": "MEDIUM",
                "recommendations": [
                    "Automate continuous vulnerability scanning of container images in CI/CD pipeline",
                    "Rotate Kafka and database credentials on a 90-day cadence using HashiCorp Vault",
                ],
            }
            return response_schema.model_validate(tm_data)

        # Fallback empty construction
        return response_schema.model_validate({})


class GeminiProvider(ModelProvider):
    """Production provider using Google Gemini API."""

    def __init__(
        self,
        api_key: str | None = None,
        model_name: str | None = None,
        temperature: float | None = None,
        timeout: int | None = None,
        max_retries: int | None = None,
    ):
        key = api_key if api_key is not None else settings.google_api_key
        if not key:
            raise ProviderAuthenticationError(
                "Google API key is missing. Set GOOGLE_API_KEY environment variable or pass explicitly."
            )
        super().__init__(
            model_name=model_name or settings.gemini_model,
            temperature=temperature if temperature is not None else settings.temperature,
            timeout=timeout if timeout is not None else settings.timeout_seconds,
            max_retries=max_retries if max_retries is not None else settings.max_retries,
        )
        self.api_key = key
        self._init_client()

    def _init_client(self):
        try:
            # Modern google-genai SDK
            from google import genai

            self.client = genai.Client(api_key=self.api_key)
            self._use_modern = True
        except (ImportError, Exception):
            # Fallback to google.generativeai
            import google.generativeai as legacy_genai

            legacy_genai.configure(api_key=self.api_key)
            self.client = legacy_genai.GenerativeModel(self.model_name)
            self._use_modern = False

    def generate_text(self, prompt: str, system_instruction: str | None = None) -> ProviderResponse:
        start_time = time.time()
        for attempt in range(self.max_retries):
            try:
                if self._use_modern:
                    config: dict[str, Any] = {"temperature": self.temperature}
                    if system_instruction:
                        config["system_instruction"] = system_instruction
                    response = self.client.models.generate_content(
                        model=self.model_name,
                        contents=prompt,
                        config=config,
                    )
                    content = response.text or ""
                else:
                    response = self.client.generate_content(prompt)
                    content = response.text or ""

                latency = time.time() - start_time
                return ProviderResponse(
                    content=content,
                    model_name=self.model_name,
                    latency_seconds=latency,
                )
            except Exception as e:
                err_str = str(e).lower()
                if "429" in err_str or "quota" in err_str:
                    sleep_time = (2**attempt) + random.uniform(0.5, 1.5)
                    logger.warning(
                        f"Rate limit encountered. Backing off for {sleep_time:.2f}s (attempt {attempt + 1})"
                    )
                    time.sleep(sleep_time)
                elif "timeout" in err_str:
                    if attempt == self.max_retries - 1:
                        raise ProviderTimeoutError(
                            f"Gemini API timed out after {self.max_retries} attempts"
                        ) from e
                    time.sleep(1)
                else:
                    if attempt == self.max_retries - 1:
                        raise ModelProviderError(f"Gemini generation failed: {e}") from e
                    time.sleep(1)

        raise ModelProviderError("Max retries exceeded without successful response")

    def generate_structured(
        self, prompt: str, response_schema: type[T], system_instruction: str | None = None
    ) -> T:
        schema_json = json.dumps(response_schema.model_json_schema(), indent=2)
        structured_prompt = (
            f"{prompt}\n\n"
            f"You MUST output valid, raw JSON strictly conforming to this schema:\n"
            f"{schema_json}\n\n"
            f"Do NOT include markdown formatting, backticks or commentary. Only output valid JSON."
        )
        response = self.generate_text(structured_prompt, system_instruction=system_instruction)
        raw_text = response.content.strip()

        # Clean markdown codeblocks if model inadvertently added them
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:]
        if raw_text.startswith("```"):
            raw_text = raw_text[3:]
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3]
        raw_text = raw_text.strip()

        try:
            parsed = json.loads(raw_text)
            return response_schema.model_validate(parsed)
        except Exception as e:
            logger.error(
                f"Failed to parse structured response into {response_schema.__name__}: {e}"
            )
            raise SchemaValidationError(
                f"Invalid structured schema response: {e}", {"raw": raw_text[:200]}
            ) from e


class FallbackModelProvider(ModelProvider):
    """Resilient provider that automatically falls back to secondary provider upon failure."""

    def __init__(self, primary: ModelProvider, secondary: ModelProvider):
        super().__init__(model_name=f"{primary.model_name}+{secondary.model_name}")
        self.primary = primary
        self.secondary = secondary

    def generate_text(self, prompt: str, system_instruction: str | None = None) -> ProviderResponse:
        try:
            return self.primary.generate_text(prompt, system_instruction=system_instruction)
        except Exception as e:
            logger.warning(
                f"[FallbackModelProvider] Primary {self.primary.model_name} failed ({e}). "
                f"Failing over to {self.secondary.model_name}."
            )
            return self.secondary.generate_text(prompt, system_instruction=system_instruction)

    def generate_structured(
        self, prompt: str, response_schema: type[T], system_instruction: str | None = None
    ) -> T:
        try:
            return self.primary.generate_structured(
                prompt, response_schema=response_schema, system_instruction=system_instruction
            )
        except Exception as e:
            logger.warning(
                f"[FallbackModelProvider] Primary {self.primary.model_name} failed ({e}). "
                f"Failing over to {self.secondary.model_name}."
            )
            return self.secondary.generate_structured(
                prompt, response_schema=response_schema, system_instruction=system_instruction
            )


def get_model_provider(provider_type: str | None = None, **kwargs: Any) -> ModelProvider:
    """Factory to retrieve configured model provider."""
    p_type = (provider_type or settings.model_provider).lower()
    if p_type == "gemini":
        try:
            return GeminiProvider(**kwargs)
        except ProviderAuthenticationError as e:
            logger.warning(
                f"Gemini credentials not available ({e}). Defaulting to MockModelProvider."
            )
            return MockModelProvider()
    elif p_type == "ollama":
        from forge.core.providers.ollama import OllamaProvider
        return OllamaProvider(**kwargs)
    elif p_type == "openai":
        from forge.core.providers.openai import OpenAIProvider
        return OpenAIProvider(**kwargs)
    elif p_type == "anthropic":
        from forge.core.providers.anthropic import AnthropicProvider
        return AnthropicProvider(**kwargs)
    return MockModelProvider(**kwargs)
