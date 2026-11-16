"""Generator and manager for the 100 benchmark scenarios of FEB v1.0."""

import os

from forge.benchmark.ground_truth import GroundTruthRules
from forge.schemas.evaluation import BenchmarkCategory, BenchmarkScenario, GroundTruthStatus


def generate_100_feb_scenarios() -> list[BenchmarkScenario]:
    """Generates the full canonical 100 engineering scenarios for FEB v1.0."""
    scenarios: list[BenchmarkScenario] = []

    # 1. BACKEND SYSTEMS (20 scenarios)
    backend_specs = [
        (
            "FEB-BACKEND-001",
            "High-Throughput Order Ingestion Engine",
            "Design a resilient order processing system handling 25,000 orders/sec with zero loss.",
            ["Must use ACID transactional storage", "P99 latency < 100ms"],
            ["Ingest order", "Validate inventory", "Reserve payment"],
            ["API Gateway", "Order Queue", "Order Service", "Database"],
        ),
        (
            "FEB-BACKEND-002",
            "Real-Time Notification Dispatcher",
            "Build a multi-channel notification engine supporting SMS, email, and web push at scale.",
            ["Sub-second delivery", "Rate limit per channel provider"],
            ["Receive alert", "Route to provider", "Log delivery receipts"],
            ["Ingress API", "Priority Queue", "Channel Worker", "Receipt Store"],
        ),
        (
            "FEB-BACKEND-003",
            "Financial Ledger Audit Pipeline",
            "Architect an immutable double-entry financial ledger service.",
            ["Zero ledger discrepancies allowed", "Strict audit trail"],
            ["Record transaction", "Post balance entries", "Generate reconciliation report"],
            ["Ledger API", "Transaction Engine", "Audit DB", "Reconciliation Worker"],
        ),
        (
            "FEB-BACKEND-004",
            "Identity and Access Management Broker",
            "Implement an enterprise IAM broker supporting OAuth2, OIDC, and SAML 2.0 federation.",
            ["Zero trust posture", "Strict session revocation"],
            ["Authenticate user", "Issue JWT tokens", "Validate scopes"],
            ["Auth Gateway", "Token Service", "Directory Store", "Session Cache"],
        ),
        (
            "FEB-BACKEND-005",
            "Multi-Tenant Subscription Billing System",
            "Design a recurring billing engine handling proration, metered usage, and invoice generation.",
            ["PCI-DSS compliance", "Support 10,000 enterprise tenants"],
            ["Calculate usage", "Process recurring billing", "Issue PDF invoices"],
            ["Billing Worker", "Usage Ingestion", "Payment Connector", "Invoice DB"],
        ),
        (
            "FEB-BACKEND-006",
            "Global E-Commerce Inventory Synchronizer",
            "Build an inventory reservation service preventing overselling during flash sales.",
            ["Strict consistency on stock levels", "P95 latency < 50ms"],
            ["Check stock", "Atomically reserve inventory", "Release expired holds"],
            ["Inventory API", "Lock Manager", "Stock Database", "Hold Expiry Worker"],
        ),
        (
            "FEB-BACKEND-007",
            "Healthcare Patient Data Gateway",
            "Architect a HIPAA-compliant FHIR API gateway for electronic medical records.",
            ["End-to-end encryption", "Immutable access logs"],
            ["Query patient records", "Enforce consent policy", "Export FHIR bundle"],
            ["FHIR Gateway", "Consent Engine", "EHR Repository", "Audit Logger"],
        ),
        (
            "FEB-BACKEND-008",
            "Content Management & Delivery Platform",
            "Implement a headless CMS backend with automated image transformation and CDN invalidation.",
            ["99.99% read availability", "Asset rendering < 300ms"],
            ["Publish article", "Optimize media assets", "Purge edge caches"],
            ["CMS Core", "Media Transformer", "Edge CDN Interface", "Content Store"],
        ),
        (
            "FEB-BACKEND-009",
            "IoT Fleet Telemetry Ingestion Hub",
            "Build an ingestion backend processing MQTT streams from 500,000 industrial IoT sensors.",
            ["At-least-once ingestion", "Handle intermittent network loss"],
            ["Ingest sensor packet", "Filter anomaly triggers", "Store time-series metrics"],
            ["MQTT Broker", "Telemetry Processor", "Time-Series Store", "Alerting Worker"],
        ),
        (
            "FEB-BACKEND-010",
            "Search Indexing Pipeline",
            "Design a document indexing and full-text search backend supporting lexical and vector search.",
            ["Near real-time indexing < 2s lag", "P95 search < 80ms"],
            ["Ingest raw document", "Extract embeddings", "Update search index"],
            ["Index Worker", "Embedding Service", "Vector Search Index", "Document Store"],
        ),
        (
            "FEB-BACKEND-011",
            "Digital Asset Rights Management API",
            "Build a licensing backend validating playback rights for encrypted video streams.",
            ["Sub-50ms token issuance", "Strict anti-piracy protections"],
            ["Validate license request", "Issue DRM playback key", "Revoke compromised tokens"],
            ["License API", "DRM Key Vault", "Rights Database", "Audit Cache"],
        ),
        (
            "FEB-BACKEND-012",
            "Ride-Hailing Geospatial Dispatch Hub",
            "Architect a real-time driver-rider spatial matching service.",
            ["P99 geospatial lookup < 30ms", "Continuous driver GPS updates"],
            ["Receive driver coordinates", "Query nearest drivers in geo-hash", "Dispatch ride"],
            ["Location Ingestion", "Spatial Index", "Dispatch Engine", "State Cache"],
        ),
        (
            "FEB-BACKEND-013",
            "API Developer Portal and Gateway Proxy",
            "Design a developer API gateway enforcing per-customer quotas, API keys, and analytics.",
            ["Gateway overhead < 5ms", "Dynamic route reload without downtime"],
            ["Proxy client request", "Enforce rate limit", "Record usage analytics"],
            ["Reverse Proxy", "Rate Limiter", "Analytics Aggregator", "Route Store"],
        ),
        (
            "FEB-BACKEND-014",
            "Automated Compliance Reporting Engine",
            "Build an automated compliance data collector across cloud infrastructures.",
            ["Air-gapped operation support", "Tamper-evident evidence storage"],
            [
                "Collect configuration snapshots",
                "Evaluate CIS benchmarks",
                "Compile PDF audit report",
            ],
            ["Collector Agent", "Rule Evaluator", "Report Generator", "Evidence Store"],
        ),
        (
            "FEB-BACKEND-015",
            "Cryptographic Key Management Service (KMS)",
            "Architect a multi-tenant envelope encryption and key lifecycle management backend.",
            ["FIPS 140-2 Level 3 compliance", "Hardware Security Module integration"],
            ["Generate data encryption key", "Wrap/unwrap customer keys", "Rotate master keys"],
            ["KMS API", "HSM Gateway", "Key Hierarchy Store", "Audit Logger"],
        ),
        (
            "FEB-BACKEND-016",
            "Digital Wallet Transfer Engine",
            "Design a real-time P2P wallet balance transfer system with fraud anomaly screening.",
            ["Strict double-entry bookkeeping", "Zero double-spend"],
            ["Verify wallet balance", "Screen AML rules", "Execute atomic transfer"],
            ["Transfer API", "Fraud Filter", "Ledger Core", "Notification Service"],
        ),
        (
            "FEB-BACKEND-017",
            "Flight Booking & GDS Integration Hub",
            "Build an airline reservation backend integrating with multiple Global Distribution Systems.",
            ["Handle eventual consistency across airlines", "Lock seat hold for 15 mins"],
            ["Search flights", "Hold seat inventory", "Confirm PNR ticket"],
            ["GDS Aggregator", "Hold Manager", "Booking Service", "Ticketing Store"],
        ),
        (
            "FEB-BACKEND-018",
            "Customer Feedback Sentiment Pipeline",
            "Design a customer review ingestion backend triggering automated response workflows.",
            ["Process 5,000 reviews/min", "Support multi-language translation"],
            ["Ingest review", "Score sentiment polarity", "Route negative alerts"],
            ["Review API", "NLP Classifier", "Routing Engine", "CRM Connector"],
        ),
        (
            "FEB-BACKEND-019",
            "Video Transcoding Job Orchestrator",
            "Architect a distributed job queue coordinating adaptive bitrate video encoding.",
            ["Dynamic spot instance utilization", "Fault-tolerant slice re-encoding"],
            ["Split video into chunks", "Queue transcode tasks", "Stitch HLS/DASH manifest"],
            ["Job Controller", "Chunking Worker", "Transcode Pool", "Manifest Builder"],
        ),
        (
            "FEB-BACKEND-020",
            "Energy Grid Smart Meter Ingestion",
            "Build an ingestion backend processing utility meter kilowatt-hour readings across millions of homes.",
            ["Store 5 years historical intervals", "Calculate peak-load pricing"],
            ["Ingest 15-min interval", "Validate meter signature", "Compute dynamic billing"],
            ["Meter Gateway", "Interval Processor", "Timeseries DB", "Billing Aggregator"],
        ),
    ]
    for sid, title, obj, cons, frs, comps in backend_specs:
        scenarios.append(
            BenchmarkScenario(
                scenario_id=sid,
                category=BenchmarkCategory.BACKEND_SYSTEMS,
                title=title,
                objective=obj,
                constraints=cons,
                expected_functional_requirements=frs,
                expected_nfr_categories=["PERFORMANCE", "RELIABILITY", "SECURITY"],
                expected_components=comps,
                expected_threat_categories=["DENIAL_OF_SERVICE", "TAMPERING", "SPOOFING"],
                evaluation_rubric=GroundTruthRules.get_rubric_for_category(
                    BenchmarkCategory.BACKEND_SYSTEMS
                ),
                ground_truth_status=GroundTruthStatus.PROGRAMMATICALLY_VALIDATED,
            )
        )

    # 2. DISTRIBUTED SYSTEMS (15 scenarios)
    dist_specs = [
        (
            "FEB-DISTRIB-001",
            "Distributed Lock Service (Chubby/Raft)",
            "Implement a fault-tolerant distributed locking coordinator with lease renewal.",
            ["Linearizable reads and writes", "Zero split-brain during partitions"],
            ["Acquire named lock", "Renew heartbeat lease", "Release lock"],
            ["Raft Node Cluster", "Lease Manager", "State Machine"],
        ),
        (
            "FEB-DISTRIB-002",
            "Globally Distributed Object Storage",
            "Design an S3-compatible multi-region object store with erasure coding.",
            ["11 nines of durability", "Geo-replication across continents"],
            ["Put object chunk", "Reconstruct erasure shards", "Serve get requests"],
            [
                "Object Gateway",
                "Metadata Coordinator",
                "Storage Storage Node",
                "Replication Daemon",
            ],
        ),
        (
            "FEB-DISTRIB-003",
            "Distributed Task Scheduler (Celery/Temporal)",
            "Architect a durable workflow engine with replayable event histories.",
            ["At-least-once task execution", "Support workflows spanning months"],
            ["Register workflow", "Schedule timed steps", "Replay activity history"],
            ["Workflow Engine", "Task Queue", "History Store", "Worker Pool"],
        ),
        (
            "FEB-DISTRIB-004",
            "Global Consistent Cache (Memcached/Redis Cluster)",
            "Build a multi-region distributed in-memory cache with cache invalidation broadcasts.",
            ["Sub-10ms global reads", "Eventual cache coherency"],
            ["Get cache key", "Set with TTL", "Invalidate cross-region keys"],
            ["Cache Node", "Cluster Proxy", "Invalidation Bus"],
        ),
        (
            "FEB-DISTRIB-005",
            "Distributed Log Aggregator (Vector/Fluentd)",
            "Design an agentless log collection pipeline forwarding server logs to cold storage.",
            ["Zero log dropping during backpressure", "Buffering on disk"],
            ["Collect syslog stream", "Parse structured fields", "Flush batch to S3"],
            ["Log Collector", "Buffer Queue", "Parser Engine", "Storage Sink"],
        ),
        (
            "FEB-DISTRIB-006",
            "Distributed Rate Limiter Service",
            "Implement a global token-bucket rate limiter with sliding window synchronization.",
            ["Decision latency < 2ms", "Resilient to cross-datacenter WAN lag"],
            ["Check rate quota", "Decrement tokens", "Sync window delta"],
            ["Rate Limit Proxy", "Local Redis Cache", "Cross-DC Gossip Sync"],
        ),
        (
            "FEB-DISTRIB-007",
            "Fault-Tolerant Message Broker Cluster",
            "Architect a partitioned, replicated commit-log broker similar to Apache Kafka.",
            ["Strict partition order", "High watermark commit replication"],
            ["Produce message", "Replicate to in-sync replicas", "Consume from offset"],
            ["Broker Node", "Partition Controller", "Commit Log", "Consumer Coordinator"],
        ),
        (
            "FEB-DISTRIB-008",
            "Distributed Configuration Management (etcd/Consul)",
            "Build a strongly consistent key-value configuration tree with watch notifications.",
            ["Raft consensus", "Long polling watch streams"],
            ["Write config key", "Watch prefix updates", "Elect leader"],
            ["Consensus Core", "Prefix Watcher", "Snapshot Engine"],
        ),
        (
            "FEB-DISTRIB-009",
            "Global Service Mesh Control Plane",
            "Design an xDS-compatible control plane distributing dynamic mTLS routing rules to Envoy proxies.",
            ["Update propagation < 1s to 50k sidecars", "Zero traffic interruption"],
            ["Compile routing policies", "Stream xDS updates", "Distribute mTLS certs"],
            ["Control Plane Core", "Policy Engine", "CA Cert Provider", "xDS Streamer"],
        ),
        (
            "FEB-DISTRIB-010",
            "Distributed Tracing Collector (Jaeger/Zipkin)",
            "Architect an OpenTelemetry trace collector sampling billions of spans daily.",
            ["Tail-based sampling", "Bounded memory consumption"],
            ["Ingest OTLP span", "Apply sampling heuristics", "Write trace graph to storage"],
            ["Trace Receiver", "Sampling Worker", "Trace Index", "Storage Adapter"],
        ),
        (
            "FEB-DISTRIB-011",
            "Cross-Cloud Database Replication Engine",
            "Build a CDC replication agent moving changes from AWS Aurora to GCP Cloud SQL in real-time.",
            ["Replication lag < 3s", "Preserve transaction ordering"],
            ["Read binlog/WAL", "Transform datatypes", "Apply changes to target DB"],
            ["WAL Reader", "Transformation Engine", "Buffer Queue", "Target Writer"],
        ),
        (
            "FEB-DISTRIB-012",
            "Peer-to-Peer Large Artifact Distribution",
            "Design a BitTorrent-style distributed distribution network for 50GB container images.",
            ["Maximize internal network transfer", "Limit WAN egress"],
            ["Register artifact chunk", "Discover seed peers", "Verify SHA-256 blocks"],
            ["Tracker Server", "Peer Daemon", "Integrity Verifier"],
        ),
        (
            "FEB-DISTRIB-013",
            "Distributed Deadlock Detector",
            "Architect a distributed transaction manager detecting and resolving wait-for cycles.",
            ["Minimal phantom deadlock false positives", "Fast cycle abort"],
            ["Register resource lock wait", "Build global wait graph", "Abort youngest victim"],
            ["Lock Monitor", "Graph Analyzer", "Transaction Arbiter"],
        ),
        (
            "FEB-DISTRIB-014",
            "Edge CDN Dynamic Routing & PoP Director",
            "Build a Anycast DNS and latency-aware traffic director routing global users to best PoP.",
            ["Sub-50ms DNS response", "Automated failover of dead PoPs"],
            ["Monitor PoP health", "Calculate optimal path", "Respond with geo-routed IP"],
            ["Health Poller", "Routing Engine", "Anycast DNS Daemon"],
        ),
        (
            "FEB-DISTRIB-015",
            "Distributed Consensus-Driven Clock Synchronizer",
            "Implement a hybrid logical clock (HLC) coordination layer for distributed serializability.",
            ["Bounded drift under 100 microseconds", "Monotonicity guarantee"],
            ["Read physical time", "Compute HLC timestamp", "Exchange peer sync messages"],
            ["Clock Daemon", "Peer Sync Bus", "Monotonic Verifier"],
        ),
    ]
    for sid, title, obj, cons, frs, comps in dist_specs:
        scenarios.append(
            BenchmarkScenario(
                scenario_id=sid,
                category=BenchmarkCategory.DISTRIBUTED_SYSTEMS,
                title=title,
                objective=obj,
                constraints=cons,
                expected_functional_requirements=frs,
                expected_nfr_categories=["RELIABILITY", "PERFORMANCE", "SCALABILITY"],
                expected_components=comps,
                expected_threat_categories=[
                    "DENIAL_OF_SERVICE",
                    "TAMPERING",
                    "INFORMATION_DISCLOSURE",
                ],
                evaluation_rubric=GroundTruthRules.get_rubric_for_category(
                    BenchmarkCategory.DISTRIBUTED_SYSTEMS
                ),
                ground_truth_status=GroundTruthStatus.PROGRAMMATICALLY_VALIDATED,
            )
        )

    # 3. AI AND ML SYSTEMS (15 scenarios)
    aiml_specs = [
        (
            "FEB-AIML-001",
            "Real-Time LLM Inference Gateway",
            "Build an LLM reverse proxy with semantic caching, streaming token buffering, and model fallback.",
            ["P95 first-token latency < 400ms", "Zero key exposure"],
            ["Proxy user prompt", "Check semantic vector cache", "Stream response tokens"],
            ["LLM Gateway", "Semantic Cache", "Model Router", "Token Counter"],
        ),
        (
            "FEB-AIML-002",
            "Enterprise Retrieval Augmented Generation (RAG) Engine",
            "Architect a secure RAG pipeline with hybrid dense/sparse search and document ACL filtering.",
            ["Strict document tenant isolation", "Faithful context grounding"],
            ["Chunk document", "Generate embeddings", "Query with ACL filter"],
            ["Document Ingestion", "Embedding Model", "Vector Store", "RAG Generator"],
        ),
        (
            "FEB-AIML-003",
            "Feature Store for Real-Time Fraud Inference",
            "Design an online-offline feature store computing rolling aggregations for credit card transactions.",
            ["Online read latency < 15ms", "Point-in-time correctness"],
            ["Ingest event features", "Update online Redis store", "Write offline Parquet"],
            ["Feature Ingestion", "Online Feature Store", "Offline Lakehouse", "Sync Worker"],
        ),
        (
            "FEB-AIML-004",
            "Continuous Model Training & Fine-Tuning Pipeline",
            "Architect an MLOps pipeline automating dataset validation, LoRA fine-tuning, and model evaluation.",
            ["Automate regression rollback", "Track lineage with MLflow"],
            ["Validate training dataset", "Execute LoRA training", "Evaluate safety benchmarks"],
            ["Data Validator", "Training Cluster", "Model Registry", "Eval Harness"],
        ),
        (
            "FEB-AIML-005",
            "Multi-Agent Autonomous Research Orchestrator",
            "Build a hierarchical multi-agent platform delegating search, synthesis, and code execution tasks.",
            ["Prevent infinite agent loops", "Strict sandbox isolation"],
            ["Decompose user query", "Delegate sub-tasks", "Synthesize findings"],
            ["Supervisor Agent", "Worker Agents", "Tool Sandbox", "Audit Store"],
        ),
        (
            "FEB-AIML-006",
            "Speech-to-Text Audio Streaming Platform",
            "Design a low-latency live audio transcription engine with speaker diarization.",
            ["Audio-to-text latency < 800ms", "Handle 10,000 concurrent calls"],
            ["Ingest audio stream", "Run streaming ASR", "Format diarized transcript"],
            ["Audio Gateway", "ASR Worker Pool", "Diarization Engine", "Egress Streamer"],
        ),
        (
            "FEB-AIML-007",
            "Computer Vision Quality Inspection Pipeline",
            "Architect a high-speed manufacturing visual defect detector on industrial edge hardware.",
            ["Inference time < 50ms per frame", "Offline local operation"],
            ["Capture camera frame", "Run YOLO/TensorRT detector", "Flag defect coordinates"],
            ["Camera Ingest", "Edge Inference Node", "PLC Actuator Interface", "Cloud Sync"],
        ),
        (
            "FEB-AIML-008",
            "Personalized Recommendation Engine",
            "Design a two-stage recommendation platform (candidate generation + ranking model) for 50M items.",
            ["End-to-end latency < 80ms", "Freshness updates < 5 mins"],
            ["Retrieve candidate items", "Score with ranking DNN", "Filter seen items"],
            ["Candidate Retrieval", "Ranking Service", "User Profile Store", "Feedback Collector"],
        ),
        (
            "FEB-AIML-009",
            "AI Guardrails and Content Moderation Gateway",
            "Build a real-time prompt and completion safety filter detecting PII, jailbreaks, and toxicity.",
            ["Filter latency < 50ms", "Zero false-negative on critical safety"],
            ["Scan inbound prompt", "Detect adversarial jailbreaks", "Mask sensitive PII"],
            ["Guardrail Proxy", "Jailbreak Classifier", "PII Masker", "Policy Store"],
        ),
        (
            "FEB-AIML-010",
            "Vector Database Index Sharder",
            "Architect a horizontally scalable HNSW vector database supporting billion-scale vectors.",
            ["Recall > 95% at 50 QPS per shard", "Fast vector insert"],
            ["Index new vector", "Partition across shards", "Execute approximate k-NN"],
            ["Routing Node", "HNSW Shard Cluster", "Index Compactor", "WAL Store"],
        ),
        (
            "FEB-AIML-011",
            "Autonomous Code Review Agent",
            "Design a static analysis and LLM-assisted code review bot with verifiable fix suggestions.",
            ["Integrate with GitHub webhooks", "Zero hallucinated imports"],
            ["Parse Git diff", "Run linter and AST analysis", "Generate PR comments"],
            ["Webhook Receiver", "AST Analyzer", "Review Agent", "GitHub API Adapter"],
        ),
        (
            "FEB-AIML-012",
            "Document OCR and Table Extraction Pipeline",
            "Build an automated financial invoice scanner extracting complex nested tables into JSON.",
            ["Accuracy > 98% on scanned receipts", "Support distorted PDFs"],
            ["Preprocess image", "Run vision layout model", "Map table schema"],
            ["PDF Ingest", "Layout Model", "Table Normalizer", "Export Store"],
        ),
        (
            "FEB-AIML-013",
            "Distributed Model Serving Mesh",
            "Architect a Kubernetes model serving cluster managing vLLM and TensorRT-LLM with autoscaling.",
            ["Dynamic batching optimization", "Scale to zero during idle hours"],
            ["Route request to replica", "Manage continuous batching", "Monitor GPU metrics"],
            ["Model Gateway", "Inference Pods", "GPU Autoscaler", "Telemetry Exporter"],
        ),
        (
            "FEB-AIML-014",
            "Synthetic Data Generation Platform",
            "Design a privacy-preserving synthetic tabular data engine using diffusion models and GANs.",
            ["Differential privacy epsilon < 1.0", "Preserve statistical distributions"],
            ["Profile sensitive dataset", "Train generative model", "Sample synthetic rows"],
            ["Data Profiler", "Generative Engine", "Privacy Evaluator", "Export Pipeline"],
        ),
        (
            "FEB-AIML-015",
            "Agentic Tool Execution Sandbox",
            "Build a secure containerized code execution environment allowing AI agents to run untrusted Python.",
            ["Ephemeral 5-second lifetime", "Zero host network access"],
            ["Receive agent code snippet", "Spin up isolated sandbox", "Return stdout/stderr"],
            ["Sandbox Manager", "MicroVM/Container Pool", "Security Monitor", "Output Sanitizer"],
        ),
    ]
    for sid, title, obj, cons, frs, comps in aiml_specs:
        scenarios.append(
            BenchmarkScenario(
                scenario_id=sid,
                category=BenchmarkCategory.AI_ML_SYSTEMS,
                title=title,
                objective=obj,
                constraints=cons,
                expected_functional_requirements=frs,
                expected_nfr_categories=["PERFORMANCE", "SECURITY", "RELIABILITY"],
                expected_components=comps,
                expected_threat_categories=[
                    "TAMPERING",
                    "INFORMATION_DISCLOSURE",
                    "DENIAL_OF_SERVICE",
                ],
                evaluation_rubric=GroundTruthRules.get_rubric_for_category(
                    BenchmarkCategory.AI_ML_SYSTEMS
                ),
                ground_truth_status=GroundTruthStatus.PROGRAMMATICALLY_VALIDATED,
            )
        )

    # 4. DATABASE SYSTEMS (15 scenarios)
    db_specs = [
        (
            "FEB-DB-001",
            "Distributed Key-Value Store with LSM-Trees",
            "Implement an LSM-tree storage engine with SSTable compaction and write-ahead log.",
            ["Crash consistency via WAL", "Minimize write amplification"],
            ["Append to MemTable", "Flush SSTable to disk", "Run tiered compaction"],
            ["WAL Manager", "MemTable Store", "Compaction Engine", "SSTable Reader"],
        ),
        (
            "FEB-DB-002",
            "High-Throughput Time-Series Database",
            "Design a time-series engine with delta-of-delta timestamp compression and automatic rollups.",
            ["Query million points < 200ms", "Support 10-year retention"],
            ["Write metrics point", "Compress interval block", "Run downsampling rollup"],
            ["Ingestion Core", "Compression Engine", "Rollup Worker", "Storage Engine"],
        ),
        (
            "FEB-DB-003",
            "Graph Database with Index-Free Adjacency",
            "Architect a property graph database executing fast multi-hop graph traversals.",
            ["Sub-100ms 4-hop traversal", "ACID graph mutations"],
            ["Create node/edge", "Traverse neighbor pointers", "Execute Cypher query"],
            ["Graph Storage Engine", "Traversal Planner", "Buffer Pool", "Transaction Log"],
        ),
        (
            "FEB-DB-004",
            "Multi-Master Relational Database Cluster",
            "Design an active-active relational database with conflict-free replicated data types (CRDTs).",
            ["Zero downtime during regional outage", "Deterministic conflict resolution"],
            ["Execute SQL query", "Broadcast replication delta", "Reconcile concurrent writes"],
            ["SQL Frontend", "Storage Engine", "CRDT Resolver", "Replication Broker"],
        ),
        (
            "FEB-DB-005",
            "Distributed Analytical Columnar Engine",
            "Build a Parquet-native vectorized query engine executing parallel SQL scans.",
            ["Process 1TB scan < 5 seconds", "Vectorized AVX-512 execution"],
            ["Parse SQL query", "Plan columnar pushdowns", "Execute parallel scan"],
            ["Query Optimizer", "Vectorized Engine", "Metadata Catalog", "Storage Reader"],
        ),
        (
            "FEB-DB-006",
            "Document Store with Secondary B-Tree Indexing",
            "Architect a JSON document database with dynamic schema indexing and multi-field indexes.",
            ["Consistent secondary index updates", "ACID single-doc operations"],
            ["Insert JSON doc", "Update B-tree index", "Query with range predicate"],
            ["Document Store", "Index Manager", "Query Parser", "Lock Table"],
        ),
        (
            "FEB-DB-007",
            "Zero-Knowledge Encrypted Database",
            "Design an encrypted database allowing homomorphic equality search without decrypting data.",
            ["Zero plaintext on database server", "Resilient to stolen DB dumps"],
            ["Encrypt record client-side", "Search deterministic token", "Return encrypted row"],
            ["Client SDK", "Encrypted Query Proxy", "Storage Engine", "Audit Core"],
        ),
        (
            "FEB-DB-008",
            "Spatial-Temporal Geo-Database",
            "Build a spatial database indexing moving GPS trajectories with R-Trees.",
            ["Sub-50ms polygon containment queries", "Support 1M points/sec update"],
            ["Insert geo-coordinates", "Update R-Tree index", "Query bounding box"],
            ["Spatial Indexer", "Query Planner", "Buffer Manager", "Storage Engine"],
        ),
        (
            "FEB-DB-009",
            "Transactional Memory Database (VoltDB/H-Store)",
            "Design a shared-nothing in-memory relational database executing single-threaded partitioned transactions.",
            ["Sub-millisecond transactions", "Deterministic transaction ordering"],
            ["Route to partition", "Execute stored procedure", "Replicate state to standby"],
            ["Partition Manager", "Execution Engine", "Snapshot Daemon", "Replication Link"],
        ),
        (
            "FEB-DB-010",
            "Distributed CDC (Change Data Capture) Pipeline",
            "Architect a transaction log reader streaming database inserts, updates, and deletes as JSON events.",
            ["Zero performance impact on primary DB", "Exactly-once event delivery"],
            ["Capture WAL changes", "Parse transaction boundary", "Publish to Kafka topic"],
            ["Log Miner", "Transaction Buffer", "Event Publisher", "Offset Tracker"],
        ),
        (
            "FEB-DB-011",
            "Cloud-Native Database Storage-Compute Decoupler",
            "Build a distributed database separating stateless compute nodes from shared storage layer (Aurora style).",
            ["Read replica lag < 10ms", "Instant point-in-time restore"],
            [
                "Execute query on compute node",
                "Write redo log to storage fleet",
                "Serve pages from storage",
            ],
            ["Compute Node", "Storage Fleet", "Log Coordinator", "Backup Manager"],
        ),
        (
            "FEB-DB-012",
            "Blockchain State Storage Engine",
            "Design a verifiable key-value store backed by Sparse Merkle Trees for cryptographic state proofs.",
            ["Fast inclusion/exclusion proofs", "Zero tampering of past blocks"],
            ["Update state trie", "Calculate Merkle root", "Generate proof of state"],
            ["Merkle Trie Engine", "State Cache", "Proof Generator", "Disk Store"],
        ),
        (
            "FEB-DB-013",
            "Distributed Cache Coherency Layer",
            "Architect a write-through and write-behind cache coordinator preserving database consistency.",
            ["Zero stale reads after write commit", "Automatic cache warm up"],
            ["Read cache on hit", "Write through to DB", "Invalidate on rollback"],
            ["Cache Proxy", "Write Behind Queue", "DB Adapter", "Invalidation Broadcaster"],
        ),
        (
            "FEB-DB-014",
            "Event Sourcing Event Store",
            "Design an append-only event store guaranteeing optimistic concurrency control per aggregate.",
            ["Immutable historical records", "Sub-20ms event append"],
            ["Append event to aggregate", "Check expected version", "Stream event to projections"],
            ["Event Log Engine", "Version Checker", "Projection Dispatcher", "Snapshot DB"],
        ),
        (
            "FEB-DB-015",
            "Federated Query Engine (Trino/Presto style)",
            "Build a distributed query coordinator executing cross-database joins between Postgres, Mongo, and S3.",
            ["Minimize data movement", "Cost-based join optimization"],
            [
                "Parse federated SQL query",
                "Generate split plans for connectors",
                "Execute distributed hash join",
            ],
            ["Coordinator Node", "Connector Manager", "Worker Fleet", "Exchange Operator"],
        ),
    ]
    for sid, title, obj, cons, frs, comps in db_specs:
        scenarios.append(
            BenchmarkScenario(
                scenario_id=sid,
                category=BenchmarkCategory.DATABASE_SYSTEMS,
                title=title,
                objective=obj,
                constraints=cons,
                expected_functional_requirements=frs,
                expected_nfr_categories=["RELIABILITY", "PERFORMANCE", "SECURITY"],
                expected_components=comps,
                expected_threat_categories=[
                    "TAMPERING",
                    "INFORMATION_DISCLOSURE",
                    "DENIAL_OF_SERVICE",
                ],
                evaluation_rubric=GroundTruthRules.get_rubric_for_category(
                    BenchmarkCategory.DATABASE_SYSTEMS
                ),
                ground_truth_status=GroundTruthStatus.PROGRAMMATICALLY_VALIDATED,
            )
        )

    # 5. CLOUD INFRASTRUCTURE (15 scenarios)
    cloud_specs = [
        (
            "FEB-CLOUD-001",
            "Multi-Region Kubernetes Traffic Manager",
            "Architect a global GSLB ingress controller routing traffic across 5 Kubernetes clusters.",
            ["Automated failover in < 15 seconds", "Zero dropped active connections"],
            ["Probe cluster health", "Adjust DNS/Anycast weights", "Route HTTP ingress"],
            ["GSLB Director", "Health Poller", "Ingress Controller", "Cert Manager"],
        ),
        (
            "FEB-CLOUD-002",
            "Automated Cloud Disaster Recovery Coordinator",
            "Build an automated RTO/RPO failover orchestration platform for cloud infrastructure.",
            ["RTO < 30 minutes, RPO < 5 minutes", "Validate with automated dry runs"],
            ["Trigger failover runbook", "Promote standby databases", "Switch DNS records"],
            ["DR Orchestrator", "Database Promoter", "DNS Switcher", "Audit Store"],
        ),
        (
            "FEB-CLOUD-003",
            "Zero Trust Cloud Network Controller",
            "Design a software-defined microsegmentation controller enforcing WireGuard overlays between VMs.",
            ["Zero open public ports", "Dynamic peer authorization"],
            [
                "Issue WireGuard peer config",
                "Enforce network firewall rules",
                "Monitor telemetry flows",
            ],
            ["SDN Controller", "WireGuard Daemon", "Policy Engine", "Flow Collector"],
        ),
        (
            "FEB-CLOUD-004",
            "Serverless Function Autoscaler & Cold Start Mitigator",
            "Architect a serverless execution runtime minimizing cold starts through speculative pre-warming.",
            ["Cold start < 50ms", "Zero compute resource waste"],
            ["Predict traffic spikes", "Pre-warm container snapshots", "Dispatch function call"],
            ["Predictive Scaler", "Container Pool", "Function Router", "Metrics Engine"],
        ),
        (
            "FEB-CLOUD-005",
            "Automated Cloud Cost FinOps Optimizer",
            "Build an infrastructure scanner identifying idle cloud resources, orphaned disks, and spot candidates.",
            ["Save estimated 25% compute spend", "Zero disruption to production"],
            [
                "Scan cloud resource metrics",
                "Identify underutilized nodes",
                "Execute rightsizing recommendations",
            ],
            ["FinOps Scanner", "Cost Model Evaluator", "Automation Runner", "Dashboard DB"],
        ),
        (
            "FEB-CLOUD-006",
            "Infrastructure-as-Code Drift Detector",
            "Design a continuous scanner comparing live Terraform state against actual AWS/GCP resources.",
            ["Detect drift within 1 hour", "Automated pull request generation"],
            [
                "Query cloud API inventory",
                "Diff against Terraform state",
                "Alert drift discrepancy",
            ],
            ["State Collector", "Diff Engine", "Alert Notifier", "Remediation Agent"],
        ),
        (
            "FEB-CLOUD-007",
            "Air-Gapped Container Registry Mirror",
            "Architect a secure container image mirror verifying cryptographic Cosign signatures.",
            ["Air-gap network compatibility", "Zero unverified image deployments"],
            ["Sync upstream image", "Verify Cosign signature", "Re-tag into private registry"],
            ["Mirror Daemon", "Signature Verifier", "Private Registry", "Vulnerability Scanner"],
        ),
        (
            "FEB-CLOUD-008",
            "Cloud Log Archiver & Tiering Lifecycle",
            "Build an automated log archiver compressing, encrypting, and transitioning logs from SSD to Glacier.",
            ["Ensure 7-year regulatory retention", "Minimize retrieval costs"],
            [
                "Ingest raw log streams",
                "Compress into Zstandard chunks",
                "Enforce lifecycle storage class",
            ],
            ["Archival Worker", "Compression Engine", "Storage Manager", "Metadata Index"],
        ),
        (
            "FEB-CLOUD-009",
            "Automated TLS Certificate Lifecycle Manager",
            "Design a high-availability certificate authority client renewing 100,000 Let's Encrypt certificates.",
            ["Zero expired production certs", "Automate ACME DNS-01 challenges"],
            ["Request ACME challenge", "Create DNS TXT records", "Distribute certificate bundles"],
            ["ACME Manager", "DNS Provider Interface", "Key Vault", "Distributor Daemon"],
        ),
        (
            "FEB-CLOUD-010",
            "Multi-Cloud Secrets Synchronization Agent",
            "Architect a secrets synchronization bridge mirroring HashiCorp Vault secrets to AWS Secrets Manager.",
            ["Sync latency < 5s", "Zero secret leakage in logs"],
            [
                "Watch Vault secret update",
                "Encrypt secret payload",
                "Push to cloud secrets manager",
            ],
            ["Vault Listener", "Payload Encryptor", "Cloud Sync Worker", "Audit Logger"],
        ),
        (
            "FEB-CLOUD-011",
            "Global Cloud WAN Mesh Router",
            "Build a transit gateway routing encrypted traffic between 20 remote enterprise VPCs.",
            ["Sub-100ms transit overhead", "Automated BGP route healing"],
            ["Establish BGP session", "Propagate routing tables", "Encrypt inter-VPC tunnels"],
            ["Transit Router", "BGP Engine", "Tunnel Manager", "Flow Monitor"],
        ),
        (
            "FEB-CLOUD-012",
            "Ephemeral Preview Environment Orchestrator",
            "Design an automated system spinning up isolated Kubernetes namespaces for every GitHub pull request.",
            ["Startup time < 2 minutes", "Auto-destroy after 3 hours of inactivity"],
            ["Listen to PR event", "Provision helm chart environment", "Teardown on PR close"],
            ["PR Webhook Listener", "K8s Provisioner", "Ingress Router", "Cleanup Reaper"],
        ),
        (
            "FEB-CLOUD-013",
            "Cloud Security Posture Management (CSPM) Scanner",
            "Architect an agentless CSPM platform scanning AWS accounts for misconfigured S3 buckets and IAM roles.",
            ["Scan 500 accounts in < 15 mins", "CIS benchmark mapping"],
            [
                "Assume cross-account IAM role",
                "Inspect security groups & ACLs",
                "Generate risk scorecard",
            ],
            ["Cross-Account Scanner", "Rule Engine", "Remediation Actioner", "Report DB"],
        ),
        (
            "FEB-CLOUD-014",
            "DDoS Scrubber & Dynamic BGP Flowspec Injector",
            "Build an automated anti-DDoS mitigation controller announcing BGP Flowspec rules to border routers.",
            ["Detect flood attack in < 10 seconds", "Mitigate volumetric UDP/SYN floods"],
            [
                "Analyze NetFlow/sFlow packets",
                "Detect threshold anomaly",
                "Inject BGP blackhole / filter rule",
            ],
            ["Flow Analyzer", "Anomaly Detector", "BGP Controller", "Mitigation Log"],
        ),
        (
            "FEB-CLOUD-015",
            "Distributed Configuration & Feature Flag Broker",
            "Architect a globally distributed feature flag daemon propagating toggles to 10,000 server nodes in < 1s.",
            ["Zero network partition lockup", "Local fallback evaluation"],
            [
                "Update flag definition",
                "Broadcast delta over SSE/gRPC",
                "Evaluate targeting rules locally",
            ],
            ["Flag Admin Core", "Distribution Broker", "Local Client SDK", "Audit Store"],
        ),
    ]
    for sid, title, obj, cons, frs, comps in cloud_specs:
        scenarios.append(
            BenchmarkScenario(
                scenario_id=sid,
                category=BenchmarkCategory.CLOUD_INFRASTRUCTURE,
                title=title,
                objective=obj,
                constraints=cons,
                expected_functional_requirements=frs,
                expected_nfr_categories=["RELIABILITY", "SECURITY", "OPERATIONAL"],
                expected_components=comps,
                expected_threat_categories=[
                    "DENIAL_OF_SERVICE",
                    "TAMPERING",
                    "ELEVATION_OF_PRIVILEGE",
                ],
                evaluation_rubric=GroundTruthRules.get_rubric_for_category(
                    BenchmarkCategory.CLOUD_INFRASTRUCTURE
                ),
                ground_truth_status=GroundTruthStatus.PROGRAMMATICALLY_VALIDATED,
            )
        )

    # 6. SECURITY CRITICAL SYSTEMS (10 scenarios)
    sec_specs = [
        (
            "FEB-SEC-001",
            "Hardware Security Module (HSM) Payment Gateway",
            "Design an EMV pin-block translation and payment card verification core.",
            ["Strict PCI-DSS PIN security", "Zero plaintext cardholder data"],
            ["Translate PIN block", "Verify CVV2/dCVV", "Issue payment authorization token"],
            ["HSM Interface", "PIN Translation Engine", "Key Storage Vault", "Audit Controller"],
        ),
        (
            "FEB-SEC-002",
            "Zero-Knowledge Identity Verification Platform",
            "Architect a selective-disclosure identity wallet using zk-SNARK verifiable credentials.",
            ["Zero tracking of user interactions", "Cryptographically sound proofs"],
            [
                "Issue verifiable credential",
                "Generate zk-SNARK proof",
                "Verify proof on-chain or service",
            ],
            ["Issuer Node", "User Wallet Core", "Verifier Engine", "Revocation Registry"],
        ),
        (
            "FEB-SEC-003",
            "Air-Gapped Software Signing Authority",
            "Build an air-gapped code-signing service for firmware updates with multi-person authorization.",
            ["Quorum approval (3 of 5)", "Physical air-gap barrier with QR/USB"],
            ["Upload firmware hash", "Collect cryptographic signatures", "Output signed manifest"],
            ["Signing Ceremony Engine", "Quorum Controller", "HSM Air-Gap Node", "Audit Ledger"],
        ),
        (
            "FEB-SEC-004",
            "Enterprise Privileged Access Management (PAM) Vault",
            "Design a privileged session broker with real-time keystroke recording and credential rotation.",
            ["Zero permanent root passwords", "Kill malicious sessions instantly"],
            [
                "Check out ephemeral root password",
                "Proxy SSH/RDP session",
                "Record screen/keystrokes",
            ],
            ["PAM Proxy", "Password Rotator", "Session Recorder", "Vault Storage"],
        ),
        (
            "FEB-SEC-005",
            "Automated Dynamic Application Security Testing (DAST) Scanner",
            "Architect an automated web application vulnerability scanner simulating authenticated attacks.",
            ["Zero destructive data deletion", "Precise OWASP Top 10 detection"],
            [
                "Crawl application surface",
                "Inject security test vectors",
                "Verify vulnerability payload",
            ],
            ["Crawler Engine", "Payload Injector", "Response Analyzer", "Vulnerability DB"],
        ),
        (
            "FEB-SEC-006",
            "Security Information & Event Management (SIEM) Correlation Engine",
            "Build a high-speed SIEM processing 100,000 security events/sec with sliding-window correlation.",
            ["Detect brute-force/APT patterns", "Latency < 5s from log to alert"],
            [
                "Ingest normalized syslog/CEF",
                "Match Sigma correlation rules",
                "Trigger SOAR incident",
            ],
            ["Log Normalizer", "Correlation Engine", "Rule Matcher", "Incident Dispatcher"],
        ),
        (
            "FEB-SEC-007",
            "Cryptographic Honeypot and Canary Token Platform",
            "Design an intrusion detection system deploying canary API keys, DNS tokens, and database decoy records.",
            ["Immediate notification upon breach attempt", "Zero false positives"],
            ["Deploy canary token", "Monitor trigger endpoints", "Alert SOC team with origin IP"],
            ["Canary Generator", "Trigger Listener", "Alert Engine", "Token Catalog"],
        ),
        (
            "FEB-SEC-008",
            "Automated Threat Intelligence Aggregator & Feed Scraper",
            "Architect a STIX/TAXII threat intel hub deduplicating IOCs (IPs, hashes, domains) with confidence scoring.",
            ["Process 1M IOCs daily", "Real-time firewall feed export"],
            ["Scrape external threat feeds", "Deduplicate and score IOCs", "Export blocklist API"],
            ["Feed Harvester", "Deduplication Engine", "IOC Store", "Distribution API"],
        ),
        (
            "FEB-SEC-009",
            "Confidential Computing Enclave Orchestrator",
            "Build an orchestrator deploying containerized workloads inside AMD SEV-SNP / Intel SGX enclaves.",
            ["Attestation verification before boot", "Encrypted memory hardware enforcement"],
            [
                "Verify enclave attestation",
                "Inject decryption keys into enclave",
                "Run secure computation",
            ],
            ["Attestation Service", "Enclave Manager", "Key Escrow", "Computation Host"],
        ),
        (
            "FEB-SEC-010",
            "Continuous Software Bill of Materials (SBOM) & Vulnerability Radar",
            "Design a real-time SBOM analyzer scanning supply-chain packages for zero-day vulnerabilities.",
            ["Scan 1000 repos in < 10 mins", "Map CVEs to affected microservices"],
            [
                "Extract package lockfiles",
                "Match against OSV/NVD database",
                "Trigger automated patch PR",
            ],
            ["Lockfile Parser", "Vulnerability Matcher", "Impact Graph", "Remediation Engine"],
        ),
    ]
    for sid, title, obj, cons, frs, comps in sec_specs:
        scenarios.append(
            BenchmarkScenario(
                scenario_id=sid,
                category=BenchmarkCategory.SECURITY_CRITICAL,
                title=title,
                objective=obj,
                constraints=cons,
                expected_functional_requirements=frs,
                expected_nfr_categories=["SECURITY", "COMPLIANCE", "RELIABILITY"],
                expected_components=comps,
                expected_threat_categories=[
                    "ELEVATION_OF_PRIVILEGE",
                    "SPOOFING",
                    "TAMPERING",
                    "INFORMATION_DISCLOSURE",
                ],
                evaluation_rubric=GroundTruthRules.get_rubric_for_category(
                    BenchmarkCategory.SECURITY_CRITICAL
                ),
                ground_truth_status=GroundTruthStatus.PROGRAMMATICALLY_VALIDATED,
            )
        )

    # 7. GENERAL SOFTWARE ARCHITECTURE (10 scenarios)
    gen_specs = [
        (
            "FEB-GEN-001",
            "Modular Monolith to Microservices Decomposer",
            "Design an architectural migration path decomposing an e-commerce monolith into decoupled services.",
            ["Zero customer downtime during migration", "Strangler fig pattern adoption"],
            ["Route strangler requests", "Replicate domain data", "Decommission legacy modules"],
            ["API Gateway", "Strangler Router", "Domain Service Pool", "CDC Sync"],
        ),
        (
            "FEB-GEN-002",
            "Plugin Architecture for Extensible Desktop Application",
            "Architect an isolated plugin sandbox supporting third-party extensions in Electron/Python.",
            ["Process isolation prevents crash of main app", "Permission-gated API access"],
            ["Load plugin manifest", "Spawn isolated worker", "Expose IPC capabilities"],
            ["Host Application Core", "Plugin Manager", "IPC Sandbox", "Permission Broker"],
        ),
        (
            "FEB-GEN-003",
            "Collaborative Real-Time Canvas Engine (Figma/Miro style)",
            "Build a real-time collaborative document editor using CRDTs or Operational Transformation (OT).",
            ["Sub-30ms local optimistic updates", "Deterministic multi-user conflict resolution"],
            ["Apply local canvas edit", "Broadcast change vector", "Merge peer operations"],
            ["Canvas Client", "CRDT Sync Server", "Websocket Manager", "Snapshot Store"],
        ),
        (
            "FEB-GEN-004",
            "Cross-Platform Universal Search & Quick Launcher",
            "Design a local desktop quick-launcher searching files, applications, bookmarks, and clipboard history.",
            ["Result query latency < 15ms", "Resource footprint < 50MB RAM"],
            ["Index local desktop filesystem", "Execute fuzzy match", "Launch selected target"],
            ["File Crawler", "Fuzzy Search Engine", "History Store", "Launcher Core"],
        ),
        (
            "FEB-GEN-005",
            "Event-Driven CQRS Architecture for Banking",
            "Architect an event-sourced command-query responsibility segregation (CQRS) banking system.",
            ["Strong auditability", "Read model optimized for high-QPS lookups"],
            ["Execute money command", "Append event to stream", "Project materialized read views"],
            ["Command Service", "Event Store", "Projection Worker", "Query Read DB"],
        ),
        (
            "FEB-GEN-006",
            "Multi-Language Localization (i18n) & Translation Sync",
            "Build a continuous localization backend syncing UI strings from code to translation services.",
            ["Zero missing translation keys", "Automated pseudo-localization testing"],
            [
                "Extract strings from AST",
                "Sync with translation API",
                "Bundle localization catalogs",
            ],
            ["String Extractor", "Translation Sync", "Catalog Compiler", "CDN Exporter"],
        ),
        (
            "FEB-GEN-007",
            "Automated Database Schema Migration Coordinator",
            "Design a database migration runner executing zero-downtime expand-contract migrations.",
            ["Zero table locks on multi-million row tables", "Automated backward rollback"],
            [
                "Validate migration script",
                "Execute background backfill",
                "Switch application to new column",
            ],
            ["Migration Runner", "Lock Inspector", "Backfill Worker", "Schema Registry"],
        ),
        (
            "FEB-GEN-008",
            "Cross-Device End-to-End Encrypted Note Synchronizer",
            "Architect an encrypted personal note sync engine similar to Standard Notes or Signal.",
            ["Zero knowledge server architecture", "Conflict resolution across offline devices"],
            [
                "Encrypt note on device",
                "Sync encrypted ciphertext blobs",
                "Resolve multi-device conflicts",
            ],
            ["Client Encryption SDK", "Sync Server", "Blob Store", "Account Manager"],
        ),
        (
            "FEB-GEN-009",
            "Automated User Onboarding & Feature Tour Engine",
            "Build an embeddable customer onboarding SDK orchestrating step-by-step interactive walkthroughs.",
            ["Zero page load latency degradation", "Real-time user cohort segmentation"],
            [
                "Evaluate tour targeting rules",
                "Render interactive step overlay",
                "Track completion funnels",
            ],
            ["SDK Script", "Targeting Evaluator", "Analytics Receiver", "Config CDN"],
        ),
        (
            "FEB-GEN-010",
            "Unified Developer CLI Tool Platform",
            "Design an extensible enterprise developer CLI with auto-updates, telemetry, and SSO authentication.",
            ["Sub-100ms startup time", "Cross-platform Windows/Mac/Linux support"],
            [
                "Authenticate developer via browser SSO",
                "Execute remote workspace command",
                "Check background auto-updates",
            ],
            ["CLI Core", "Auth Handler", "Plugin Runner", "Update Checker"],
        ),
    ]
    for sid, title, obj, cons, frs, comps in gen_specs:
        scenarios.append(
            BenchmarkScenario(
                scenario_id=sid,
                category=BenchmarkCategory.GENERAL_ARCHITECTURE,
                title=title,
                objective=obj,
                constraints=cons,
                expected_functional_requirements=frs,
                expected_nfr_categories=["USABILITY", "RELIABILITY", "PERFORMANCE"],
                expected_components=comps,
                expected_threat_categories=["TAMPERING", "SPOOFING", "INFORMATION_DISCLOSURE"],
                evaluation_rubric=GroundTruthRules.get_rubric_for_category(
                    BenchmarkCategory.GENERAL_ARCHITECTURE
                ),
                ground_truth_status=GroundTruthStatus.PROGRAMMATICALLY_VALIDATED,
            )
        )

    return scenarios


def save_dataset_to_file(scenarios: list[BenchmarkScenario], output_path: str):
    """Saves scenarios to a JSONL file."""
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        for s in scenarios:
            f.write(s.model_dump_json() + "\n")
