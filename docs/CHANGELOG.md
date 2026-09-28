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
- [2026-07-28 17:40:35] chore(orchestrator): update migration scripts for task run state tracking
- [2026-07-28 21:18:18] fix(subagents): validate agent payload schemas with Pydantic v2 models
- [2026-07-29 20:14:05] perf(api): implement async task DAG scheduler with dependency resolution
- [2026-07-30 11:53:01] perf(registry): update migration scripts for task run state tracking
- [2026-07-30 13:30:47] fix(orchestrator): implement task execution timeout and cancellation propagation
- [2026-07-30 13:48:28] chore(subagents): document multi-agent communication protocol and message bus
- **2026-07-30 15:29:02**: `docs(api): validate agent payload schemas with Pydantic v2 models`
  *Updated specifications and documentation details.*
- [2026-07-30 16:06:12] fix(telemetry): handle race condition during concurrent subagent dispatch
- [2026-07-30 17:02:42] chore(worker): update migration scripts for task run state tracking
- **2026-07-30 18:08:41**: `docs(dag): add structured telemetry event logging for agent tool calls`
  *Updated specifications and documentation details.*
- [2026-07-30 20:22:08] chore(subagents): handle race condition during concurrent subagent dispatch
- [2026-07-30 20:51:19] perf(api): reduce message serialization overhead in agent event stream
- [2026-07-30 21:10:46] perf(worker): enhance subagent output aggregation and summarization pipeline
- [2026-08-01 14:08:21] fix(telemetry): reduce message serialization overhead in agent event stream
- [2026-08-01 19:47:43] fix(worker): validate agent payload schemas with Pydantic v2 models
- [2026-08-03 13:58:15] chore(api): add health check endpoint for distributed worker nodes
- [2026-08-04 10:24:05] perf(orchestrator): add structured telemetry event logging for agent tool calls
- [2026-08-04 11:47:58] fix(api): reduce message serialization overhead in agent event stream
- [2026-08-04 14:02:25] perf(registry): handle race condition during concurrent subagent dispatch
- [2026-08-04 14:46:03] fix(telemetry): dynamic registration for custom tool schemas
- **2026-08-04 16:16:08**: `docs(registry): dynamic registration for custom tool schemas`
  *Updated specifications and documentation details.*
- [2026-08-04 16:19:06] chore(subagents): reduce message serialization overhead in agent event stream
- [2026-08-04 17:05:31] chore(subagents): optimize worker thread pool allocation for parallel tool execution
- [2026-08-04 21:12:24] chore(telemetry): handle race condition during concurrent subagent dispatch
- [2026-08-04 22:36:22] perf(telemetry): add health check endpoint for distributed worker nodes
- [2026-08-04 22:59:50] fix(subagents): decouple workflow step execution from state persistence layer
- [2026-08-05 19:51:25] perf(api): document multi-agent communication protocol and message bus
- [2026-08-06 15:06:06] chore(orchestrator): handle race condition during concurrent subagent dispatch
- **2026-08-07 09:45:43**: `docs(registry): document multi-agent communication protocol and message bus`
  *Updated specifications and documentation details.*
- [2026-08-07 09:46:16] chore(memory): handle race condition during concurrent subagent dispatch
- [2026-08-07 10:58:45] perf(api): decouple workflow step execution from state persistence layer
- [2026-08-07 11:04:24] chore(orchestrator): implement async task DAG scheduler with dependency resolution
- [2026-08-07 11:12:11] chore(api): handle race condition during concurrent subagent dispatch
- [2026-08-07 13:44:46] perf(telemetry): dynamic registration for custom tool schemas
- [2026-08-07 13:51:38] fix(subagents): dynamic registration for custom tool schemas
- [2026-08-07 14:27:34] fix(telemetry): update migration scripts for task run state tracking
- [2026-08-07 14:31:55] chore(telemetry): add structured telemetry event logging for agent tool calls
- [2026-08-07 16:11:21] perf(scheduler): validate agent payload schemas with Pydantic v2 models
- [2026-08-07 16:58:43] perf(worker): reduce message serialization overhead in agent event stream
- [2026-08-07 18:20:48] fix(registry): implement exponential backoff with jitter on API rate limit error
- [2026-08-07 19:06:14] fix(memory): implement vector-backed long-term episodic memory for agents
- [2026-08-07 22:07:54] fix(api): handle race condition during concurrent subagent dispatch
- [2026-08-07 22:44:48] perf(orchestrator): add health check endpoint for distributed worker nodes
- [2026-08-11 12:13:11] perf(scheduler): validate agent payload schemas with Pydantic v2 models
- [2026-08-14 09:41:00] perf(dag): update migration scripts for task run state tracking
- [2026-08-14 10:03:54] chore(api): implement exponential backoff with jitter on API rate limit error
- [2026-08-14 10:46:00] chore(worker): implement exponential backoff with jitter on API rate limit error
- [2026-08-14 13:20:29] perf(dag): validate agent payload schemas with Pydantic v2 models
- [2026-08-14 13:24:34] perf(registry): handle race condition during concurrent subagent dispatch
- [2026-08-14 15:15:36] perf(registry): update migration scripts for task run state tracking
- [2026-08-14 15:21:56] perf(scheduler): dynamic registration for custom tool schemas
- [2026-08-14 17:27:12] fix(registry): implement async task DAG scheduler with dependency resolution
- [2026-08-14 17:52:22] perf(memory): add structured telemetry event logging for agent tool calls
- [2026-08-14 18:13:38] fix(orchestrator): optimize worker thread pool allocation for parallel tool execution
- [2026-08-14 18:29:53] fix(memory): reduce message serialization overhead in agent event stream
- [2026-08-14 20:04:02] chore(dag): implement exponential backoff with jitter on API rate limit error
- [2026-08-18 18:12:28] perf(subagents): handle race condition during concurrent subagent dispatch
- [2026-08-19 14:17:34] perf(registry): implement vector-backed long-term episodic memory for agents
- [2026-08-19 16:24:16] fix(worker): decouple workflow step execution from state persistence layer
- [2026-08-26 15:55:04] perf(worker): reduce message serialization overhead in agent event stream
- [2026-08-26 20:49:08] perf(memory): reduce message serialization overhead in agent event stream
- [2026-08-28 11:59:19] chore(api): document multi-agent communication protocol and message bus
- [2026-08-28 12:36:12] chore(telemetry): reduce message serialization overhead in agent event stream
- **2026-08-28 14:43:42**: `docs(telemetry): update migration scripts for task run state tracking`
  *Updated specifications and documentation details.*
- [2026-08-28 17:04:03] fix(memory): implement async task DAG scheduler with dependency resolution
- [2026-08-28 17:42:49] fix(subagents): document multi-agent communication protocol and message bus
- [2026-08-28 17:48:27] perf(subagents): handle race condition during concurrent subagent dispatch
- [2026-08-28 21:44:15] chore(telemetry): add health check endpoint for distributed worker nodes
- [2026-08-28 22:33:18] perf(registry): validate agent payload schemas with Pydantic v2 models
- [2026-09-07 09:43:55] chore(api): dynamic registration for custom tool schemas
- [2026-09-07 21:07:48] chore(scheduler): implement exponential backoff with jitter on API rate limit error
- **2026-09-24 09:51:37**: `docs(subagents): implement vector-backed long-term episodic memory for agents`
  *Updated specifications and documentation details.*
- [2026-09-24 13:12:55] perf(subagents): implement exponential backoff with jitter on API rate limit error
- [2026-09-24 17:49:41] perf(worker): implement async task DAG scheduler with dependency resolution
- [2026-09-25 09:33:01] chore(telemetry): implement task execution timeout and cancellation propagation
- [2026-09-25 20:15:09] fix(subagents): implement task execution timeout and cancellation propagation
- [2026-09-28 20:20:40] chore(scheduler): implement exponential backoff with jitter on API rate limit error
- [2026-09-28 20:44:35] fix(registry): add structured telemetry event logging for agent tool calls