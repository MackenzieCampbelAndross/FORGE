"""Security mitigation catalog and OWASP alignment rules."""


class MitigationCatalog:
    """Standard security mitigations mapped to STRIDE and OWASP Top 10."""

    OWASP_RULES: dict[str, str] = {
        "SPOOFING": "OWASP A07:2021-Identification and Authentication Failures",
        "TAMPERING": "OWASP A08:2021-Software and Data Integrity Failures",
        "REPUDIATION": "OWASP A09:2021-Security Logging and Monitoring Failures",
        "INFORMATION_DISCLOSURE": "OWASP A01:2021-Broken Access Control & A02:2021-Cryptographic Failures",
        "DENIAL_OF_SERVICE": "OWASP API4:2023-Unrestricted Resource Consumption",
        "ELEVATION_OF_PRIVILEGE": "OWASP A01:2021-Broken Access Control",
    }

    RECOMMENDED_CONTROLS: dict[str, list[str]] = {
        "SPOOFING": [
            "Implement mTLS for inter-service communication.",
            "Enforce OAuth2 / OIDC with signed JWT verification.",
            "Use hardware-backed API keys or IAM roles.",
        ],
        "TAMPERING": [
            "Implement HMAC or digital signatures on message payloads.",
            "Enforce strict schema validation on all inputs.",
            "Use immutable audit trails with append-only storage.",
        ],
        "REPUDIATION": [
            "Centralize structured audit logs with RFC 5424 compliance.",
            "Cryptographically sign audit trail events.",
            "Enforce strict NTP time synchronization across all nodes.",
        ],
        "INFORMATION_DISCLOSURE": [
            "Enforce AES-256 encryption at rest for all databases and queues.",
            "Enforce TLS 1.3 with strict cipher suites in transit.",
            "Redact PII/PHI in application logs and metrics.",
        ],
        "DENIAL_OF_SERVICE": [
            "Implement token-bucket rate limiting at API gateway.",
            "Apply connection pooling limits and query timeouts.",
            "Deploy ingress behind DDoS mitigation provider (e.g. Cloudflare).",
        ],
        "ELEVATION_OF_PRIVILEGE": [
            "Enforce principle of least privilege in IAM and DB roles.",
            "Implement role-based access control (RBAC) / attribute-based (ABAC).",
            "Validate authorization at every microservice boundary.",
        ],
    }

    @classmethod
    def get_owasp_mapping(cls, stride_category: str) -> str | None:
        return cls.OWASP_RULES.get(stride_category.upper())

    @classmethod
    def get_controls_for_category(cls, stride_category: str) -> list[str]:
        return cls.RECOMMENDED_CONTROLS.get(stride_category.upper(), [])
