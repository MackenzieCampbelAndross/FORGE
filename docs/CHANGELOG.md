# FORGE Agent Engine Changelog

Multi-agent orchestration, async task DAGs, and memory persistence releases.


- [2026-07-04 10:41:54] fix(scheduler): add structured telemetry event logging for agent tool calls
- [2026-07-07 21:08:50] perf(telemetry): document multi-agent communication protocol and message bus
- [2026-07-09 19:39:10] chore(worker): dynamic registration for custom tool schemas
- **2026-07-13 11:04:00**: `docs(api): add structured telemetry event logging for agent tool calls`
  *Updated specifications and documentation details.*
- [2026-07-13 11:46:45] perf(dag): implement async task DAG scheduler with dependency resolution
- [2026-07-13 13:37:35] fix(subagents): add structured telemetry event logging for agent tool calls
- [2026-07-13 13:53:03] chore(telemetry): update migration scripts for task run state tracking
- [2026-07-13 14:36:18] perf(subagents): add health check endpoint for distributed worker nodes
- [2026-07-13 16:39:30] chore(worker): document multi-agent communication protocol and message bus
- [2026-07-13 17:18:03] chore(telemetry): decouple workflow step execution from state persistence layer
- [2026-07-13 19:36:53] fix(dag): reduce message serialization overhead in agent event stream
- [2026-07-14 09:39:53] fix(subagents): implement vector-backed long-term episodic memory for agents
- **2026-07-14 13:27:04**: `docs(api): update migration scripts for task run state tracking`
  *Updated specifications and documentation details.*
- [2026-07-14 13:28:31] perf(orchestrator): document multi-agent communication protocol and message bus
- [2026-07-14 16:03:11] chore(registry): implement exponential backoff with jitter on API rate limit error
- [2026-07-14 17:00:28] fix(subagents): document multi-agent communication protocol and message bus