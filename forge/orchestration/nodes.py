"""LangGraph node definitions wrapping specialized agents."""

from typing import Any

from forge.agents.architect import ArchitectAgent
from forge.agents.security import SecurityAgent
from forge.agents.strategy import StrategyAgent
from forge.agents.supervisor import SupervisorAgent
from forge.core.logging import logger
from forge.core.model_provider import ModelProvider
from forge.core.state import ForgeState
from forge.schemas.report import RevisionTarget
from forge.schemas.security import ThreatModel


class NodeContainer:
    """Encapsulates agents with injected provider instance."""

    def __init__(self, provider: ModelProvider | None = None):
        self.provider = provider
        self.strategy_agent = StrategyAgent(provider=provider)
        self.architect_agent = ArchitectAgent(provider=provider)
        self.security_agent = SecurityAgent(provider=provider)
        self.supervisor_agent = SupervisorAgent(provider=provider)

    def strategy_node(self, state: ForgeState) -> dict[str, Any]:
        obj = state["objective"]
        rev_hist = state.get("revision_history", [])
        last_rev = (
            rev_hist[-1]
            if (rev_hist and rev_hist[-1].target_agent == RevisionTarget.STRATEGY)
            else None
        )

        req_doc, elapsed = self.strategy_agent.run(obj, revision_request=last_rev)
        metadata = dict(state.get("execution_metadata", {}))
        metadata["strategy_latency_seconds"] = elapsed

        return {
            "requirements": req_doc,
            "current_step": "strategy_done",
            "execution_metadata": metadata,
        }

    def architect_node(self, state: ForgeState) -> dict[str, Any]:
        reqs = state["requirements"]
        if not reqs:
            raise ValueError("Cannot run architect node without validated requirements.")

        rev_hist = state.get("revision_history", [])
        last_rev = (
            rev_hist[-1]
            if (rev_hist and rev_hist[-1].target_agent == RevisionTarget.ARCHITECT)
            else None
        )

        blueprint, elapsed = self.architect_agent.run(reqs, revision_request=last_rev)
        metadata = dict(state.get("execution_metadata", {}))
        metadata["architect_latency_seconds"] = elapsed

        return {
            "architecture": blueprint,
            "current_step": "architect_done",
            "execution_metadata": metadata,
        }

    def security_node(self, state: ForgeState) -> dict[str, Any]:
        blueprint = state.get("architecture")
        if blueprint is None:
            raise ValueError("Architecture cannot be None in security_node.")
        obj = state["objective"]
        ablation = state.get("ablation_config")

        if ablation and not ablation.enable_security_agent:
            logger.info("[SecurityNode] Security agent disabled via ablation config.")
            empty_tm = ThreatModel(
                threat_model_id=f"TM-{obj.project_id}-ABLATED",
                project_id=obj.project_id,
                threats=[],
                attack_surfaces=[],
                recommendations=["Security analysis skipped via ablation config."],
            )
            return {
                "threat_model": empty_tm,
                "current_step": "security_done",
            }

        rev_hist = state.get("revision_history", [])
        last_rev = (
            rev_hist[-1]
            if (rev_hist and rev_hist[-1].target_agent == RevisionTarget.SECURITY)
            else None
        )

        tm, elapsed = self.security_agent.run(
            blueprint, project_id=obj.project_id, revision_request=last_rev
        )
        metadata = dict(state.get("execution_metadata", {}))
        metadata["security_latency_seconds"] = elapsed

        return {
            "threat_model": tm,
            "current_step": "security_done",
            "execution_metadata": metadata,
        }

    def supervisor_node(self, state: ForgeState) -> dict[str, Any]:
        obj = state["objective"]
        reqs = state.get("requirements")
        arch = state.get("architecture")
        tm = state.get("threat_model")
        if reqs is None or arch is None or tm is None:
            raise ValueError("Requirements, Architecture, and ThreatModel must be present before supervisor evaluation.")

        rev_count = state.get("revision_count", 0)
        max_revs = state.get("max_revisions", 3)
        rev_history = list(state.get("revision_history", []))
        ablation = state.get("ablation_config")

        enable_rev = True
        if ablation and not ablation.enable_supervisor_revision:
            enable_rev = False

        rev_request, issues = self.supervisor_agent.evaluate_and_route(
            objective=obj,
            requirements=reqs,
            architecture=arch,
            threat_model=tm,
            revision_count=rev_count,
            max_revisions=max_revs,
            enable_revision=enable_rev,
        )

        if rev_request is not None and enable_rev and rev_count < max_revs:
            rev_history.append(rev_request)
            return {
                "revision_count": rev_count + 1,
                "revision_history": rev_history,
                "validation_issues": issues,
                "next_agent": rev_request.target_agent.value,
                "current_step": f"revision_requested_{rev_request.target_agent.value}",
            }

        # Final report compilation
        report, elapsed = self.supervisor_agent.compile_report(
            objective=obj,
            requirements=reqs,
            architecture=arch,
            threat_model=tm,
            validation_issues=issues,
            revision_history=rev_history,
        )

        metadata = dict(state.get("execution_metadata", {}))
        metadata["supervisor_latency_seconds"] = elapsed

        return {
            "engineering_report": report,
            "validation_issues": issues,
            "revision_history": rev_history,
            "next_agent": RevisionTarget.NONE.value,
            "current_step": "workflow_complete",
            "status": report.final_status.value,
            "execution_metadata": metadata,
        }
