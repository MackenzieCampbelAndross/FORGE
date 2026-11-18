# FORGE Engineering Benchmark (FEB) v1.0 — Scenario Catalog

Total Scenarios: **100**

The FORGE Engineering Benchmark covers 7 core system design domains with realistic constraints,
expected architectural components, and STRIDE security threats.

## Category Distribution

| Category | Scenarios | Target Focus |
| :--- | :---: | :--- |
| Backend Systems | 20 | High-throughput APIs, streaming, background workers, event-driven pipelines |
| Distributed Systems | 15 | Consensus, partition tolerance, distributed transactions, edge sync |
| AI & ML Systems | 15 | Inference serving, RAG pipelines, training orchestration, vector search |
| Database Systems | 15 | Sharding, multi-model storage, time-series indexing, ACID guarantees |
| Cloud Infrastructure | 15 | Multi-region, Kubernetes topologies, zero-trust VPC, hybrid connectivity |
| Security Critical | 10 | Payment gateways, HSM key managers, auth providers, audit logging |
| General Architecture | 10 | Monolith modularization, legacy migration, plugin extensions |

## Scenario Manifest

| ID | Title | Category | Constraints | Components | Threats | Status |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| `FEB-AIML-001` | Real-Time LLM Inference Gateway | AI and ML systems | 2 | 4 | 3 | Programmatically validated |
| `FEB-AIML-002` | Enterprise Retrieval Augmented Generation (RAG) Engine | AI and ML systems | 2 | 4 | 3 | Programmatically validated |
| `FEB-AIML-003` | Feature Store for Real-Time Fraud Inference | AI and ML systems | 2 | 4 | 3 | Programmatically validated |
| `FEB-AIML-004` | Continuous Model Training & Fine-Tuning Pipeline | AI and ML systems | 2 | 4 | 3 | Programmatically validated |
| `FEB-AIML-005` | Multi-Agent Autonomous Research Orchestrator | AI and ML systems | 2 | 4 | 3 | Programmatically validated |
| `FEB-AIML-006` | Speech-to-Text Audio Streaming Platform | AI and ML systems | 2 | 4 | 3 | Programmatically validated |
| `FEB-AIML-007` | Computer Vision Quality Inspection Pipeline | AI and ML systems | 2 | 4 | 3 | Programmatically validated |
| `FEB-AIML-008` | Personalized Recommendation Engine | AI and ML systems | 2 | 4 | 3 | Programmatically validated |
| `FEB-AIML-009` | AI Guardrails and Content Moderation Gateway | AI and ML systems | 2 | 4 | 3 | Programmatically validated |
| `FEB-AIML-010` | Vector Database Index Sharder | AI and ML systems | 2 | 4 | 3 | Programmatically validated |
| `FEB-AIML-011` | Autonomous Code Review Agent | AI and ML systems | 2 | 4 | 3 | Programmatically validated |
| `FEB-AIML-012` | Document OCR and Table Extraction Pipeline | AI and ML systems | 2 | 4 | 3 | Programmatically validated |
| `FEB-AIML-013` | Distributed Model Serving Mesh | AI and ML systems | 2 | 4 | 3 | Programmatically validated |
| `FEB-AIML-014` | Synthetic Data Generation Platform | AI and ML systems | 2 | 4 | 3 | Programmatically validated |
| `FEB-AIML-015` | Agentic Tool Execution Sandbox | AI and ML systems | 2 | 4 | 3 | Programmatically validated |
| `FEB-BACKEND-001` | High-Throughput Order Ingestion Engine | Backend systems | 2 | 4 | 3 | Programmatically validated |
| `FEB-BACKEND-002` | Real-Time Notification Dispatcher | Backend systems | 2 | 4 | 3 | Programmatically validated |
| `FEB-BACKEND-003` | Financial Ledger Audit Pipeline | Backend systems | 2 | 4 | 3 | Programmatically validated |
| `FEB-BACKEND-004` | Identity and Access Management Broker | Backend systems | 2 | 4 | 3 | Programmatically validated |
| `FEB-BACKEND-005` | Multi-Tenant Subscription Billing System | Backend systems | 2 | 4 | 3 | Programmatically validated |
| `FEB-BACKEND-006` | Global E-Commerce Inventory Synchronizer | Backend systems | 2 | 4 | 3 | Programmatically validated |
| `FEB-BACKEND-007` | Healthcare Patient Data Gateway | Backend systems | 2 | 4 | 3 | Programmatically validated |
| `FEB-BACKEND-008` | Content Management & Delivery Platform | Backend systems | 2 | 4 | 3 | Programmatically validated |
| `FEB-BACKEND-009` | IoT Fleet Telemetry Ingestion Hub | Backend systems | 2 | 4 | 3 | Programmatically validated |
| `FEB-BACKEND-010` | Search Indexing Pipeline | Backend systems | 2 | 4 | 3 | Programmatically validated |
| `FEB-BACKEND-011` | Digital Asset Rights Management API | Backend systems | 2 | 4 | 3 | Programmatically validated |
| `FEB-BACKEND-012` | Ride-Hailing Geospatial Dispatch Hub | Backend systems | 2 | 4 | 3 | Programmatically validated |
| `FEB-BACKEND-013` | API Developer Portal and Gateway Proxy | Backend systems | 2 | 4 | 3 | Programmatically validated |
| `FEB-BACKEND-014` | Automated Compliance Reporting Engine | Backend systems | 2 | 4 | 3 | Programmatically validated |
| `FEB-BACKEND-015` | Cryptographic Key Management Service (KMS) | Backend systems | 2 | 4 | 3 | Programmatically validated |
| `FEB-BACKEND-016` | Digital Wallet Transfer Engine | Backend systems | 2 | 4 | 3 | Programmatically validated |
| `FEB-BACKEND-017` | Flight Booking & GDS Integration Hub | Backend systems | 2 | 4 | 3 | Programmatically validated |
| `FEB-BACKEND-018` | Customer Feedback Sentiment Pipeline | Backend systems | 2 | 4 | 3 | Programmatically validated |
| `FEB-BACKEND-019` | Video Transcoding Job Orchestrator | Backend systems | 2 | 4 | 3 | Programmatically validated |
| `FEB-BACKEND-020` | Energy Grid Smart Meter Ingestion | Backend systems | 2 | 4 | 3 | Programmatically validated |
| `FEB-CLOUD-001` | Multi-Region Kubernetes Traffic Manager | Cloud infrastructure | 2 | 4 | 3 | Programmatically validated |
| `FEB-CLOUD-002` | Automated Cloud Disaster Recovery Coordinator | Cloud infrastructure | 2 | 4 | 3 | Programmatically validated |
| `FEB-CLOUD-003` | Zero Trust Cloud Network Controller | Cloud infrastructure | 2 | 4 | 3 | Programmatically validated |
| `FEB-CLOUD-004` | Serverless Function Autoscaler & Cold Start Mitigator | Cloud infrastructure | 2 | 4 | 3 | Programmatically validated |
| `FEB-CLOUD-005` | Automated Cloud Cost FinOps Optimizer | Cloud infrastructure | 2 | 4 | 3 | Programmatically validated |
| `FEB-CLOUD-006` | Infrastructure-as-Code Drift Detector | Cloud infrastructure | 2 | 4 | 3 | Programmatically validated |
| `FEB-CLOUD-007` | Air-Gapped Container Registry Mirror | Cloud infrastructure | 2 | 4 | 3 | Programmatically validated |
| `FEB-CLOUD-008` | Cloud Log Archiver & Tiering Lifecycle | Cloud infrastructure | 2 | 4 | 3 | Programmatically validated |
| `FEB-CLOUD-009` | Automated TLS Certificate Lifecycle Manager | Cloud infrastructure | 2 | 4 | 3 | Programmatically validated |
| `FEB-CLOUD-010` | Multi-Cloud Secrets Synchronization Agent | Cloud infrastructure | 2 | 4 | 3 | Programmatically validated |
| `FEB-CLOUD-011` | Global Cloud WAN Mesh Router | Cloud infrastructure | 2 | 4 | 3 | Programmatically validated |
| `FEB-CLOUD-012` | Ephemeral Preview Environment Orchestrator | Cloud infrastructure | 2 | 4 | 3 | Programmatically validated |
| `FEB-CLOUD-013` | Cloud Security Posture Management (CSPM) Scanner | Cloud infrastructure | 2 | 4 | 3 | Programmatically validated |
| `FEB-CLOUD-014` | DDoS Scrubber & Dynamic BGP Flowspec Injector | Cloud infrastructure | 2 | 4 | 3 | Programmatically validated |
| `FEB-CLOUD-015` | Distributed Configuration & Feature Flag Broker | Cloud infrastructure | 2 | 4 | 3 | Programmatically validated |
| `FEB-DB-001` | Distributed Key-Value Store with LSM-Trees | Database systems | 2 | 4 | 3 | Programmatically validated |
| `FEB-DB-002` | High-Throughput Time-Series Database | Database systems | 2 | 4 | 3 | Programmatically validated |
| `FEB-DB-003` | Graph Database with Index-Free Adjacency | Database systems | 2 | 4 | 3 | Programmatically validated |
| `FEB-DB-004` | Multi-Master Relational Database Cluster | Database systems | 2 | 4 | 3 | Programmatically validated |
| `FEB-DB-005` | Distributed Analytical Columnar Engine | Database systems | 2 | 4 | 3 | Programmatically validated |
| `FEB-DB-006` | Document Store with Secondary B-Tree Indexing | Database systems | 2 | 4 | 3 | Programmatically validated |
| `FEB-DB-007` | Zero-Knowledge Encrypted Database | Database systems | 2 | 4 | 3 | Programmatically validated |
| `FEB-DB-008` | Spatial-Temporal Geo-Database | Database systems | 2 | 4 | 3 | Programmatically validated |
| `FEB-DB-009` | Transactional Memory Database (VoltDB/H-Store) | Database systems | 2 | 4 | 3 | Programmatically validated |
| `FEB-DB-010` | Distributed CDC (Change Data Capture) Pipeline | Database systems | 2 | 4 | 3 | Programmatically validated |
| `FEB-DB-011` | Cloud-Native Database Storage-Compute Decoupler | Database systems | 2 | 4 | 3 | Programmatically validated |
| `FEB-DB-012` | Blockchain State Storage Engine | Database systems | 2 | 4 | 3 | Programmatically validated |
| `FEB-DB-013` | Distributed Cache Coherency Layer | Database systems | 2 | 4 | 3 | Programmatically validated |
| `FEB-DB-014` | Event Sourcing Event Store | Database systems | 2 | 4 | 3 | Programmatically validated |
| `FEB-DB-015` | Federated Query Engine (Trino/Presto style) | Database systems | 2 | 4 | 3 | Programmatically validated |
| `FEB-DISTRIB-001` | Distributed Lock Service (Chubby/Raft) | Distributed systems | 2 | 3 | 3 | Programmatically validated |
| `FEB-DISTRIB-002` | Globally Distributed Object Storage | Distributed systems | 2 | 4 | 3 | Programmatically validated |
| `FEB-DISTRIB-003` | Distributed Task Scheduler (Celery/Temporal) | Distributed systems | 2 | 4 | 3 | Programmatically validated |
| `FEB-DISTRIB-004` | Global Consistent Cache (Memcached/Redis Cluster) | Distributed systems | 2 | 3 | 3 | Programmatically validated |
| `FEB-DISTRIB-005` | Distributed Log Aggregator (Vector/Fluentd) | Distributed systems | 2 | 4 | 3 | Programmatically validated |
| `FEB-DISTRIB-006` | Distributed Rate Limiter Service | Distributed systems | 2 | 3 | 3 | Programmatically validated |
| `FEB-DISTRIB-007` | Fault-Tolerant Message Broker Cluster | Distributed systems | 2 | 4 | 3 | Programmatically validated |
| `FEB-DISTRIB-008` | Distributed Configuration Management (etcd/Consul) | Distributed systems | 2 | 3 | 3 | Programmatically validated |
| `FEB-DISTRIB-009` | Global Service Mesh Control Plane | Distributed systems | 2 | 4 | 3 | Programmatically validated |
| `FEB-DISTRIB-010` | Distributed Tracing Collector (Jaeger/Zipkin) | Distributed systems | 2 | 4 | 3 | Programmatically validated |
| `FEB-DISTRIB-011` | Cross-Cloud Database Replication Engine | Distributed systems | 2 | 4 | 3 | Programmatically validated |
| `FEB-DISTRIB-012` | Peer-to-Peer Large Artifact Distribution | Distributed systems | 2 | 3 | 3 | Programmatically validated |
| `FEB-DISTRIB-013` | Distributed Deadlock Detector | Distributed systems | 2 | 3 | 3 | Programmatically validated |
| `FEB-DISTRIB-014` | Edge CDN Dynamic Routing & PoP Director | Distributed systems | 2 | 3 | 3 | Programmatically validated |
| `FEB-DISTRIB-015` | Distributed Consensus-Driven Clock Synchronizer | Distributed systems | 2 | 3 | 3 | Programmatically validated |
| `FEB-GEN-001` | Modular Monolith to Microservices Decomposer | General software architecture | 2 | 4 | 3 | Programmatically validated |
| `FEB-GEN-002` | Plugin Architecture for Extensible Desktop Application | General software architecture | 2 | 4 | 3 | Programmatically validated |
| `FEB-GEN-003` | Collaborative Real-Time Canvas Engine (Figma/Miro style) | General software architecture | 2 | 4 | 3 | Programmatically validated |
| `FEB-GEN-004` | Cross-Platform Universal Search & Quick Launcher | General software architecture | 2 | 4 | 3 | Programmatically validated |
| `FEB-GEN-005` | Event-Driven CQRS Architecture for Banking | General software architecture | 2 | 4 | 3 | Programmatically validated |
| `FEB-GEN-006` | Multi-Language Localization (i18n) & Translation Sync | General software architecture | 2 | 4 | 3 | Programmatically validated |
| `FEB-GEN-007` | Automated Database Schema Migration Coordinator | General software architecture | 2 | 4 | 3 | Programmatically validated |
| `FEB-GEN-008` | Cross-Device End-to-End Encrypted Note Synchronizer | General software architecture | 2 | 4 | 3 | Programmatically validated |
| `FEB-GEN-009` | Automated User Onboarding & Feature Tour Engine | General software architecture | 2 | 4 | 3 | Programmatically validated |
| `FEB-GEN-010` | Unified Developer CLI Tool Platform | General software architecture | 2 | 4 | 3 | Programmatically validated |
| `FEB-SEC-001` | Hardware Security Module (HSM) Payment Gateway | Security critical systems | 2 | 4 | 4 | Programmatically validated |
| `FEB-SEC-002` | Zero-Knowledge Identity Verification Platform | Security critical systems | 2 | 4 | 4 | Programmatically validated |
| `FEB-SEC-003` | Air-Gapped Software Signing Authority | Security critical systems | 2 | 4 | 4 | Programmatically validated |
| `FEB-SEC-004` | Enterprise Privileged Access Management (PAM) Vault | Security critical systems | 2 | 4 | 4 | Programmatically validated |
| `FEB-SEC-005` | Automated Dynamic Application Security Testing (DAST) Scanner | Security critical systems | 2 | 4 | 4 | Programmatically validated |
| `FEB-SEC-006` | Security Information & Event Management (SIEM) Correlation Engine | Security critical systems | 2 | 4 | 4 | Programmatically validated |
| `FEB-SEC-007` | Cryptographic Honeypot and Canary Token Platform | Security critical systems | 2 | 4 | 4 | Programmatically validated |
| `FEB-SEC-008` | Automated Threat Intelligence Aggregator & Feed Scraper | Security critical systems | 2 | 4 | 4 | Programmatically validated |
| `FEB-SEC-009` | Confidential Computing Enclave Orchestrator | Security critical systems | 2 | 4 | 4 | Programmatically validated |
| `FEB-SEC-010` | Continuous Software Bill of Materials (SBOM) & Vulnerability Radar | Security critical systems | 2 | 4 | 4 | Programmatically validated |
