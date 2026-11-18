# FORGE System Design & Architectural Blueprint Cheatsheet

A battle-tested reference guide reflecting the four-agent FORGE engineering methodology (Strategy -> Architect -> Security -> Supervisor).

---

## 1. Phase 1: Requirements & Constraints (Strategy Agent)

### Clarifying Scope
- **Scale**: Read QPS, Write QPS, Storage per year, Network egress bandwidth
- **Latency Targets**: P50, P95, P99 SLA thresholds
- **Consistency vs. Availability**: CAP theorem positioning (CP vs. AP)
- **Data Retention & Compliance**: Hot (30d) vs. Warm (1y) vs. Cold (7y), GDPR / HIPAA / PCI-DSS

### Back-of-the-Envelope Constants
- `1 Day = 86,400 seconds ≈ 10^5 seconds`
- `1 Million requests/day ≈ 12 QPS`
- `1 Billion requests/day ≈ 12,000 QPS`
- Latency Numbers to Know:
  - L1 Cache: `0.5 ns`
  - RAM access: `100 ns`
  - NVMe SSD read: `10-100 µs`
  - Same datacenter round-trip: `0.5 ms`
  - Cross-continental round-trip (e.g. US to EU): `150 ms`

---

## 2. Phase 2: Architecture & Component Decomposition (Architect Agent)

### High-Level Topology Patterns
1. **Edge Tier**: CDN / Anycast BGP -> Reverse Proxy (Envoy/Kong) -> TLS Termination & Rate Limiting
2. **Compute Tier**: Microservices / Stateless API Workers (Kubernetes, gRPC internal, REST external)
3. **Async Streaming Tier**: Kafka / Redpanda / AWS Kinesis for decoupled event-driven ingestion
4. **Caching Tier**: Redis / Memcached (Cache-Aside, Write-Through, Write-Behind)
5. **Storage Tier**:
   - Relational / ACID: PostgreSQL, MySQL, CockroachDB
   - Key-Value / High Write: Cassandra, ScyllaDB, DynamoDB
   - Search & Analytics: Elasticsearch, ClickHouse, Apache Iceberg

---

## 3. Phase 3: STRIDE Security Threat Modeling (Security Agent)

| STRIDE Category | Threat Vector | Mitigation Strategy |
| :--- | :--- | :--- |
| **Spoofing** | Forged client identity / stolen token | Mutual TLS (mTLS), short-lived JWT, OAuth2 OIDC |
| **Tampering** | Payload modification in transit or DB | HMAC signatures, strict Pydantic schema validation, DB audit checksums |
| **Repudiation** | Client denies performing critical action | Append-only immutable audit trail, RFC 5424 structured logging, NTP sync |
| **Information Disclosure** | Data leak across tenant boundaries | AES-256 at rest, TLS 1.3 in transit, PostgreSQL Row-Level Security (RLS) |
| **Denial of Service** | Resource exhaustion / volumetric attack | Distributed token-bucket rate limiter, connection pooling, DDoS scrubbing |
| **Elevation of Privilege** | Horizontal/vertical privilege escalation | Fine-grained RBAC/ABAC (OpenFGA/Zanzibar), least-privilege IAM roles |

---

## 4. Phase 4: Technical Auditing & Validation (Supervisor Agent)

Always verify before finalizing a blueprint:
- **Circular Dependencies**: Topological sort must have zero cycles.
- **Single Point of Failure (SPOF)**: Every component must span at least 3 Availability Zones.
- **Physics Violations**: Sub-millisecond latency claimed over multi-region WAN is physically impossible.
- **Unmapped Requirements**: Every functional and non-functional requirement must trace directly to at least one component.
