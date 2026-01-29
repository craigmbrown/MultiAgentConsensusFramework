#!/usr/bin/env python3
"""
Quick Start Example - Multi-Agent Consensus Framework

Demonstrates basic usage of the 40-agent consensus system.

@REQ-DEMO-001: Quick start demonstration
@BLP: Alignment (BLP-1)
"""

import asyncio
import os
from dotenv import load_dotenv
from typing import Dict, Any, List

# Load environment variables
load_dotenv()


class SimpleAgent:
    """Simple agent for demonstration purposes."""

    def __init__(self, agent_id: str, specialty: str):
        self.agent_id = agent_id
        self.specialty = specialty
        self.confidence = 0.0

    async def analyze(self, topic: str) -> Dict[str, Any]:
        """Analyze a topic and return response with confidence."""
        # In production, this would call an LLM
        response = {
            'agent_id': self.agent_id,
            'specialty': self.specialty,
            'analysis': f"Analysis of '{topic}' from {self.specialty} perspective",
            'confidence': 0.85,
            'recommendations': [
                f"Recommendation 1 from {self.agent_id}",
                f"Recommendation 2 from {self.agent_id}"
            ]
        }
        return response

    async def vote(self, proposal: Dict) -> Dict[str, Any]:
        """Vote on a proposal."""
        # Simple voting logic - in production this would be more sophisticated
        return {
            'agent_id': self.agent_id,
            'agree': True,
            'confidence': 0.85,
            'reasoning': f"{self.agent_id} agrees based on {self.specialty} analysis"
        }


class ConsensusEngine:
    """Simple consensus engine for demonstration."""

    def __init__(self, threshold: float = 0.75):
        self.threshold = threshold
        self.agents: List[SimpleAgent] = []

    def add_agent(self, agent: SimpleAgent):
        """Add an agent to the consensus group."""
        self.agents.append(agent)
        print(f"Added agent: {agent.agent_id} ({agent.specialty})")

    async def build_consensus(self, topic: str) -> Dict[str, Any]:
        """Build consensus among all agents."""
        print(f"\n{'='*60}")
        print(f"Building consensus on: {topic}")
        print(f"{'='*60}")

        # Phase 1: Gather analyses
        print("\nPhase 1: Gathering agent analyses...")
        analyses = []
        for agent in self.agents:
            analysis = await agent.analyze(topic)
            analyses.append(analysis)
            print(f"  - {agent.agent_id}: confidence {analysis['confidence']:.2f}")

        # Phase 2: Create proposal from analyses
        proposal = self._synthesize_proposal(analyses)
        print(f"\nPhase 2: Synthesized proposal created")

        # Phase 3: Gather votes
        print("\nPhase 3: Gathering votes...")
        votes = []
        for agent in self.agents:
            vote = await agent.vote(proposal)
            votes.append(vote)

        # Phase 4: Calculate consensus
        agree_count = sum(1 for v in votes if v['agree'])
        agreement_rate = agree_count / len(votes)

        consensus_reached = agreement_rate >= self.threshold

        result = {
            'topic': topic,
            'total_agents': len(self.agents),
            'agreement_rate': agreement_rate,
            'consensus_reached': consensus_reached,
            'threshold': self.threshold,
            'proposal': proposal,
            'votes': votes
        }

        # Print result
        print(f"\n{'='*60}")
        print(f"CONSENSUS RESULT")
        print(f"{'='*60}")
        print(f"Agreement Rate: {agreement_rate:.1%}")
        print(f"Threshold: {self.threshold:.1%}")
        print(f"Consensus Reached: {'✅ YES' if consensus_reached else '❌ NO'}")
        print(f"{'='*60}\n")

        return result

    def _synthesize_proposal(self, analyses: List[Dict]) -> Dict[str, Any]:
        """Synthesize a proposal from agent analyses."""
        # Combine all recommendations
        all_recommendations = []
        for analysis in analyses:
            all_recommendations.extend(analysis['recommendations'])

        # Calculate average confidence
        avg_confidence = sum(a['confidence'] for a in analyses) / len(analyses)

        return {
            'summary': f"Synthesized proposal from {len(analyses)} agent analyses",
            'average_confidence': avg_confidence,
            'recommendation_count': len(all_recommendations),
            'top_recommendations': all_recommendations[:5]  # Top 5
        }


async def main():
    """Main demonstration function."""
    print("\n" + "="*60)
    print("Multi-Agent Consensus Framework - Quick Start Demo")
    print("="*60)

    # Create consensus engine
    engine = ConsensusEngine(threshold=0.75)

    # Create agents with different specialties
    specialties = [
        "Design",
        "Implementation",
        "Testing",
        "Deployment",
        "Operations",
        "Security",
        "Performance",
        "Documentation"
    ]

    print("\nCreating agents...")
    for i, specialty in enumerate(specialties):
        agent = SimpleAgent(
            agent_id=f"agent_{i+1:03d}",
            specialty=specialty
        )
        engine.add_agent(agent)

    # Run consensus on a topic
    topic = "Best practices for production AI agent deployment"
    result = await engine.build_consensus(topic)

    # Display detailed results
    print("DETAILED RESULTS")
    print("-"*40)
    print(f"Topic: {result['topic']}")
    print(f"Agents Participating: {result['total_agents']}")
    print(f"Agreement Rate: {result['agreement_rate']:.1%}")
    print(f"Consensus Threshold: {result['threshold']:.1%}")
    print(f"Status: {'CONSENSUS REACHED' if result['consensus_reached'] else 'NO CONSENSUS'}")

    print("\nTop Recommendations:")
    for i, rec in enumerate(result['proposal']['top_recommendations'], 1):
        print(f"  {i}. {rec}")

    print("\n" + "="*60)
    print("Demo complete! See docs/ for full framework documentation.")
    print("="*60 + "\n")

    return result


if __name__ == "__main__":
    asyncio.run(main())
