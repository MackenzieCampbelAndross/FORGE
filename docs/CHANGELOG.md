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
- **2026-07-14 22:03:59**: `docs(dag): enhance subagent output aggregation and summarization pipeline`
  *Updated specifications and documentation details.*
- [2026-07-14 22:21:49] chore(api): update migration scripts for task run state tracking
- [2026-07-16 12:51:42] fix(api): add structured telemetry event logging for agent tool calls
- [2026-07-17 11:45:51] chore(scheduler): validate agent payload schemas with Pydantic v2 models
- [2026-07-17 11:46:53] chore(api): validate agent payload schemas with Pydantic v2 models
- [2026-07-17 15:57:15] chore(memory): implement task execution timeout and cancellation propagation
- [2026-07-17 16:51:29] fix(telemetry): implement async task DAG scheduler with dependency resolution
- [2026-07-17 17:03:38] chore(dag): add health check endpoint for distributed worker nodes
- [2026-07-17 18:22:41] chore(scheduler): add structured telemetry event logging for agent tool calls
- **2026-07-17 21:01:05**: `docs(registry): validate agent payload schemas with Pydantic v2 models`
  *Updated specifications and documentation details.*
- [2026-07-17 21:34:48] chore(scheduler): optimize worker thread pool allocation for parallel tool execution
- [2026-07-17 22:54:38] fix(telemetry): implement vector-backed long-term episodic memory for agents
- **2026-07-21 19:22:40**: `docs(registry): implement vector-backed long-term episodic memory for agents`
  *Updated specifications and documentation details.*
- [2026-07-22 10:00:59] fix(api): validate agent payload schemas with Pydantic v2 models
- [2026-07-22 11:19:05] perf(subagents): reduce message serialization overhead in agent event stream
- [2026-07-22 14:38:49] perf(orchestrator): handle race condition during concurrent subagent dispatch
- [2026-07-22 16:10:17] perf(worker): enhance subagent output aggregation and summarization pipeline
- [2026-07-22 16:17:36] chore(worker): validate agent payload schemas with Pydantic v2 models
- **2026-07-22 18:00:02**: `docs(subagents): implement async task DAG scheduler with dependency resolution`
  *Updated specifications and documentation details.*
- [2026-07-22 19:06:09] fix(api): validate agent payload schemas with Pydantic v2 models
- [2026-07-24 09:52:07] chore(registry): update migration scripts for task run state tracking
- [2026-07-24 10:18:02] perf(api): document multi-agent communication protocol and message bus
- [2026-07-24 10:28:04] fix(subagents): handle race condition during concurrent subagent dispatch
- [2026-07-24 12:41:14] perf(orchestrator): add structured telemetry event logging for agent tool calls
- **2026-07-24 12:53:05**: `docs(orchestrator): add structured telemetry event logging for agent tool calls`
  *Updated specifications and documentation details.*
- [2026-07-24 13:29:33] fix(worker): add health check endpoint for distributed worker nodes
- [2026-07-24 15:18:41] perf(telemetry): validate agent payload schemas with Pydantic v2 models
- [2026-07-24 17:47:52] perf(orchestrator): implement exponential backoff with jitter on API rate limit error
- [2026-07-24 20:16:49] perf(worker): reduce message serialization overhead in agent event stream
- [2026-07-24 20:44:34] fix(orchestrator): optimize worker thread pool allocation for parallel tool execution
- [2026-07-24 22:38:08] perf(worker): implement task execution timeout and cancellation propagation
- **2026-07-24 22:47:39**: `docs(dag): validate agent payload schemas with Pydantic v2 models`
  *Updated specifications and documentation details.*
- [2026-07-25 11:22:34] chore(subagents): validate agent payload schemas with Pydantic v2 models