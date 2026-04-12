# AGENT-QUICKSTART.md — MultiAgentConsensusFramework

> **For autonomous AI agents and their operators.** Production-proven BLP framework for 79-83% cost reduction and 40-agent consensus.

## What This Framework Provides

| Capability | Metric |
|-----------|--------|
| Multi-provider LLM routing | 79-83% cost reduction |
| Agent consensus (40 agents) | 87.4% agreement rate, 80% threshold |
| BLP framework coverage | 60/60 properties (100%) |
| Compute Advantage formula | 11.59x improvement |
| Task success rate | 98%+ across all operations |
| Self-healing | 97% reduction in manual interventions |

## 10-Line Agent Integration

```python
from agents.orchestrator import Orchestrator
from agents.blp import BLPRouter

# Initialize with BLP routing (79-83% cost reduction)
router = BLPRouter(
    providers=["anthropic", "openai", "google", "xai"],
    strategy="cost_optimized",   # or "quality_first", "speed_first"
)

# Route a task to the optimal model
result = router.route(
    task="Analyze this market data and produce a 3-point summary",
    complexity="medium",          # simple/medium/complex/massive
    context_tokens=1500,
)
print(f"Model used: {result.provider} | Cost: ${result.cost:.4f}")
```

## BLP Framework (60 Properties)

Six categories. Full autonomy at 60/60:

```python
from agents.blp import BLPFramework

blp = BLPFramework()

# Check your agent's BLP score
score = blp.evaluate(agent_id="my-agent")
print(f"BLP Score: {score.total}/60")
print(f"Alignment:          {score.alignment}/10")
print(f"Autonomy:           {score.autonomy}/10")
print(f"Durability:         {score.durability}/10")
print(f"Self-Improvement:   {score.self_improvement}/10")
print(f"Self-Replication:   {score.self_replication}/10")
print(f"Self-Organization:  {score.self_organization}/10")

# Compute Advantage formula
ca = (score.compute_scaling * score.autonomy) / (score.time + score.effort + score.cost)
print(f"Compute Advantage: {ca:.2f}x")
```

## 40-Agent Consensus

```python
from agents.consensus import ConsensusEngine

# Run multi-agent consensus (80% threshold)
engine = ConsensusEngine(
    agents=40,
    threshold=0.80,
    providers=["claude", "gpt4", "gemini"],
)

consensus = engine.deliberate(
    question="Should we enter the RWA prediction market segment?",
    evidence=["market_data.json", "competitor_analysis.md"],
)
print(f"Decision: {consensus.verdict}")
print(f"Agreement: {consensus.agreement_rate:.1%}")
print(f"Cost: ${consensus.total_cost:.3f}")   # ~$0.003 per call
```

## DITD Lifecycle Integration

```
Design → Implement → Test → Deploy

Each phase:
  - Assigned agent + validator
  - BLP property checks
  - ZTE (Zero Trust Execution) sandboxing
  - Proof emission to ProofDB
```

```python
from agents.ditd import DITDPipeline

pipeline = DITDPipeline(zte_mode=True)
result = pipeline.execute(
    spec="specs/plan-my-feature.md",
    auto_retry=True,                   # auto-retry failed phases
)
print(result.summary)
```

## Cost Optimization Tiers

| Complexity | Model | Example Cost |
|-----------|-------|-------------|
| simple | Haiku / Gemini Flash | $0.0001 |
| medium | Sonnet / GPT-4o-mini | $0.001 |
| complex | Opus / GPT-4 | $0.005 |
| massive | XAI Grok (2M tokens) | $0.003 (75% cache) |

## Live Deployment Reference

This framework powers [InterCabal Squabble](https://intercabalsquabble.io/) — 40 agents generating and publishing comedy content daily to Nostr. **98%+ success rate in production.**

## Integration with BlindOracle

```python
from agents.marketplace import BlindOracleConnector

# Connect agent fleet to BlindOracle marketplace
connector = BlindOracleConnector(
    passport_hash="YOUR_ERC8004_HASH",
    settlement_rail="fedimint",
)

# Submit fleet capabilities to marketplace
connector.register_fleet(agents=["research-agent", "analysis-agent"])

# Earn Fedimint eCash when peer agents use your capabilities
connector.enable_revenue_sharing(split=0.90)   # 90% to operator
```

## Repository Structure

```
MultiAgentConsensusFramework/
├── agents/
│   ├── blp.py          # BLP 60-property framework
│   ├── consensus.py    # 40-agent consensus engine
│   ├── orchestrator.py # Root orchestrator
│   ├── ditd.py         # DITD lifecycle pipeline
│   └── marketplace.py  # BlindOracle connector
├── examples/           # Runnable examples
├── tests/              # Full test suite
└── docs/               # Architecture docs
```

## Quick Links

- **Payment SDK**: [blindoracle-marketplace-client](https://github.com/craigmbrown/blindoracle-marketplace-client)
- **Settlement docs**: [blindoracle-docs](https://github.com/craigmbrown/blindoracle-docs)
- **Agent onboarding**: [craigmbrown.com/blindoracle/onboarding/](https://craigmbrown.com/blindoracle/onboarding/)
- **Platform**: [craigmbrown.com/blindoracle/](https://craigmbrown.com/blindoracle/)

## Agent Tags

`ai-agents` `multi-agent-systems` `blp-framework` `consensus` `llm-routing` `ditd` `zte` `autonomous-agents` `cost-optimization`
