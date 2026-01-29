#!/usr/bin/env python3
"""
Custom Agent Template - Multi-Agent Consensus Framework

Template for creating custom agents with BLP properties.

@REQ-DEMO-002: Custom agent template
@BLP: Self-Replication (BLP-5)
"""

import asyncio
import json
import traceback
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, List, Optional
from enum import Enum


class BLPCategory(Enum):
    """Base Level Property categories."""
    ALIGNMENT = "BLP-1"
    AUTONOMY = "BLP-2"
    DURABILITY = "BLP-3"
    SELF_IMPROVEMENT = "BLP-4"
    SELF_REPLICATION = "BLP-5"
    SELF_ORGANIZATION = "BLP-6"


@dataclass
class AgentMetrics:
    """Metrics tracking for compute advantage calculation."""
    tasks_completed: int = 0
    tasks_failed: int = 0
    total_execution_time: float = 0.0
    total_cost: float = 0.0
    self_recoveries: int = 0
    escalations: int = 0

    @property
    def success_rate(self) -> float:
        total = self.tasks_completed + self.tasks_failed
        return self.tasks_completed / total if total > 0 else 0.0

    @property
    def avg_execution_time(self) -> float:
        return self.total_execution_time / self.tasks_completed if self.tasks_completed > 0 else 0.0


@dataclass
class AgentConfig:
    """Configuration for custom agents."""
    agent_id: str
    agent_type: str
    blp_focus: List[BLPCategory]
    model_preference: str = "gpt-4o"
    max_retries: int = 3
    timeout_seconds: int = 120
    enable_monitoring: bool = True
    enable_self_healing: bool = True


class BaseAgent(ABC):
    """
    Base class for all custom agents.

    @REQ-BASE-001: Base agent implementation
    @BLP: Alignment (BLP-1)
    @COMPUTE-ADVANTAGE: Foundation for all agent compute advantage
    """

    def __init__(self, config: AgentConfig):
        self.config = config
        self.metrics = AgentMetrics()
        self.state: Dict[str, Any] = {}
        self._initialized = False

    async def initialize(self) -> bool:
        """Initialize the agent."""
        try:
            await self._setup()
            self._initialized = True
            self._log_success("Agent initialized", {"agent_id": self.config.agent_id})
            return True
        except Exception as e:
            self._log_error("Initialization failed", e)
            return False

    @abstractmethod
    async def _setup(self) -> None:
        """Subclass-specific setup. Override in custom agents."""
        pass

    @abstractmethod
    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a task. Override in custom agents."""
        pass

    async def run_with_monitoring(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run task with full monitoring and self-healing.

        @REQ-MON-001: Task execution with monitoring
        @BLP: Autonomy (BLP-2), Self-Improvement (BLP-4)
        """
        start_time = datetime.utcnow()

        for attempt in range(self.config.max_retries):
            try:
                # Execute task
                result = await self.execute_task(task)

                # Record success metrics
                duration = (datetime.utcnow() - start_time).total_seconds()
                self.metrics.tasks_completed += 1
                self.metrics.total_execution_time += duration

                self._log_success("Task completed", {
                    "task": task.get("task_id", "unknown"),
                    "duration": duration,
                    "attempt": attempt + 1
                })

                return result

            except Exception as e:
                if attempt < self.config.max_retries - 1:
                    # Attempt self-healing
                    if self.config.enable_self_healing:
                        healed = await self._attempt_self_healing(e, task)
                        if healed:
                            self.metrics.self_recoveries += 1
                            continue

                    self._log_warning(f"Retrying task (attempt {attempt + 2})", e)
                else:
                    # Final failure
                    self.metrics.tasks_failed += 1
                    self._log_error("Task failed after all retries", e)
                    raise

    async def _attempt_self_healing(self, error: Exception, task: Dict) -> bool:
        """
        Attempt to self-heal from an error.

        @REQ-HEAL-001: Self-healing mechanism
        @BLP: Durability (BLP-3)
        """
        error_type = type(error).__name__

        # Common healing strategies
        healing_strategies = {
            "TimeoutError": self._heal_timeout,
            "ConnectionError": self._heal_connection,
            "RateLimitError": self._heal_rate_limit,
            "ValidationError": self._heal_validation,
        }

        if error_type in healing_strategies:
            return await healing_strategies[error_type](error, task)

        return False

    async def _heal_timeout(self, error: Exception, task: Dict) -> bool:
        """Heal from timeout by reducing complexity."""
        self._log_info("Self-healing: Reducing task complexity for timeout")
        # Simplify task or increase timeout
        self.config.timeout_seconds *= 1.5
        return True

    async def _heal_connection(self, error: Exception, task: Dict) -> bool:
        """Heal from connection error by waiting and retrying."""
        self._log_info("Self-healing: Waiting for connection recovery")
        await asyncio.sleep(5)
        return True

    async def _heal_rate_limit(self, error: Exception, task: Dict) -> bool:
        """Heal from rate limit by backing off."""
        self._log_info("Self-healing: Backing off for rate limit")
        await asyncio.sleep(60)
        return True

    async def _heal_validation(self, error: Exception, task: Dict) -> bool:
        """Heal from validation error by cleaning input."""
        self._log_info("Self-healing: Cleaning input for validation")
        # Clean/sanitize task input
        return True

    def calculate_compute_advantage(self) -> float:
        """
        Calculate compute advantage for this agent.

        @REQ-CA-001: Compute advantage calculation
        @BLP: Self-Improvement (BLP-4)
        """
        # Compute Advantage = (Compute Scaling × Autonomy) / (Time + Effort + Cost)

        # Compute Scaling: Based on parallel capability and throughput
        compute_scaling = min(10.0, self.metrics.tasks_completed / 10)

        # Autonomy: Based on self-recovery rate and low escalation
        if self.metrics.tasks_completed > 0:
            autonomy = (
                self.metrics.success_rate * 0.5 +
                (self.metrics.self_recoveries / max(1, self.metrics.tasks_failed)) * 0.3 +
                (1 - self.metrics.escalations / max(1, self.metrics.tasks_completed)) * 0.2
            )
        else:
            autonomy = 0.5

        # Denominators
        time_factor = max(0.1, self.metrics.avg_execution_time / 10)  # Normalized
        effort_factor = 0.5  # Base effort
        cost_factor = max(0.1, self.metrics.total_cost / 10)  # Normalized

        compute_advantage = (compute_scaling * autonomy) / (time_factor + effort_factor + cost_factor)

        return round(compute_advantage, 2)

    # Logging methods following Standard I/O pattern
    def _log_success(self, message: str, data: Optional[Dict] = None):
        """Log success message."""
        log_entry = {
            "status": "success",
            "agent_id": self.config.agent_id,
            "message": message,
            "data": data or {},
            "timestamp": datetime.utcnow().isoformat()
        }
        print(f"SUCCESS: {json.dumps(log_entry)}")

    def _log_error(self, message: str, error: Exception):
        """Log error message with full details."""
        log_entry = {
            "status": "error",
            "agent_id": self.config.agent_id,
            "message": message,
            "exception_type": type(error).__name__,
            "exception_message": str(error),
            "traceback": traceback.format_exc(),
            "timestamp": datetime.utcnow().isoformat()
        }
        print(f"ERROR: {json.dumps(log_entry, indent=2)}")

    def _log_warning(self, message: str, error: Optional[Exception] = None):
        """Log warning message."""
        log_entry = {
            "status": "warning",
            "agent_id": self.config.agent_id,
            "message": message,
            "timestamp": datetime.utcnow().isoformat()
        }
        if error:
            log_entry["error"] = str(error)
        print(f"WARNING: {json.dumps(log_entry)}")

    def _log_info(self, message: str):
        """Log info message."""
        log_entry = {
            "status": "info",
            "agent_id": self.config.agent_id,
            "message": message,
            "timestamp": datetime.utcnow().isoformat()
        }
        print(f"INFO: {json.dumps(log_entry)}")


# ============================================================================
# Example: Custom Research Agent
# ============================================================================

class ResearchAgent(BaseAgent):
    """
    Example custom agent for research tasks.

    @REQ-RESEARCH-001: Research agent implementation
    @BLP: Alignment (BLP-1), Self-Improvement (BLP-4)
    """

    async def _setup(self) -> None:
        """Setup research agent."""
        self.state["research_history"] = []
        self.state["knowledge_base"] = {}

    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a research task."""
        topic = task.get("topic", "")
        depth = task.get("depth", "standard")

        # Simulate research (in production, this would call LLM APIs)
        research_result = {
            "topic": topic,
            "depth": depth,
            "findings": [
                f"Finding 1 about {topic}",
                f"Finding 2 about {topic}",
                f"Finding 3 about {topic}"
            ],
            "confidence": 0.85,
            "sources": ["source1.com", "source2.org", "source3.edu"],
            "recommendations": [
                f"Recommendation based on {topic} research"
            ]
        }

        # Store in knowledge base for learning
        self.state["research_history"].append({
            "topic": topic,
            "timestamp": datetime.utcnow().isoformat()
        })

        return research_result


# ============================================================================
# Example: Custom Validation Agent
# ============================================================================

class ValidationAgent(BaseAgent):
    """
    Example custom agent for validation tasks.

    @REQ-VALIDATE-001: Validation agent implementation
    @BLP: Alignment (BLP-1), Durability (BLP-3)
    """

    async def _setup(self) -> None:
        """Setup validation agent."""
        self.state["validation_rules"] = []
        self.state["validation_history"] = []

    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a validation task."""
        data = task.get("data", {})
        rules = task.get("rules", [])

        # Perform validation
        validation_results = []
        all_passed = True

        for rule in rules:
            passed = self._check_rule(data, rule)
            validation_results.append({
                "rule": rule["name"],
                "passed": passed,
                "details": rule.get("description", "")
            })
            if not passed:
                all_passed = False

        result = {
            "valid": all_passed,
            "results": validation_results,
            "rules_checked": len(rules),
            "rules_passed": sum(1 for r in validation_results if r["passed"])
        }

        return result

    def _check_rule(self, data: Dict, rule: Dict) -> bool:
        """Check a single validation rule."""
        # Simplified validation logic
        field = rule.get("field", "")
        condition = rule.get("condition", "exists")

        if condition == "exists":
            return field in data
        elif condition == "not_empty":
            return bool(data.get(field))
        elif condition == "min_length":
            return len(str(data.get(field, ""))) >= rule.get("value", 0)

        return True


# ============================================================================
# Usage Example
# ============================================================================

async def main():
    """Demonstrate custom agent usage."""
    print("\n" + "="*60)
    print("Custom Agent Template - Demonstration")
    print("="*60 + "\n")

    # Create a research agent
    research_config = AgentConfig(
        agent_id="research_001",
        agent_type="research",
        blp_focus=[BLPCategory.ALIGNMENT, BLPCategory.SELF_IMPROVEMENT],
        model_preference="gpt-4o",
        enable_monitoring=True,
        enable_self_healing=True
    )

    research_agent = ResearchAgent(research_config)
    await research_agent.initialize()

    # Execute a research task
    research_task = {
        "task_id": "research_001",
        "topic": "Multi-agent consensus algorithms",
        "depth": "comprehensive"
    }

    result = await research_agent.run_with_monitoring(research_task)

    print("\nResearch Result:")
    print(json.dumps(result, indent=2))

    # Calculate compute advantage
    ca = research_agent.calculate_compute_advantage()
    print(f"\nCompute Advantage: {ca}")

    # Create a validation agent
    validation_config = AgentConfig(
        agent_id="validation_001",
        agent_type="validation",
        blp_focus=[BLPCategory.ALIGNMENT, BLPCategory.DURABILITY]
    )

    validation_agent = ValidationAgent(validation_config)
    await validation_agent.initialize()

    # Execute a validation task
    validation_task = {
        "task_id": "validate_001",
        "data": {
            "name": "Test Agent",
            "version": "1.0.0",
            "config": {"enabled": True}
        },
        "rules": [
            {"name": "name_exists", "field": "name", "condition": "exists"},
            {"name": "version_exists", "field": "version", "condition": "not_empty"},
            {"name": "config_exists", "field": "config", "condition": "exists"}
        ]
    }

    validation_result = await validation_agent.run_with_monitoring(validation_task)

    print("\nValidation Result:")
    print(json.dumps(validation_result, indent=2))

    print("\n" + "="*60)
    print("Custom agent demonstration complete!")
    print("="*60 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
