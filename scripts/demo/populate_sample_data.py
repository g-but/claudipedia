#!/usr/bin/env python3
"""
Populate the Claudipedia database with sample physics data.

This script creates:
1. Fundamental physics axioms
2. Derived claims with reasoning relationships
3. Knowledge gaps
4. Sample queries to demonstrate functionality

Run this after Neo4j is fully started and accessible.
"""

import sys
import os
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from core.models import Claim, Edge, Gap, ClaimType, ReasoningType, Source
from core.graph_db import KnowledgeGraph


def create_physics_axioms():
    """Create fundamental physics axioms."""

    print("📚 Creating physics axioms...")

    axioms = [
        Claim(
            statement="Force equals mass times acceleration (F = ma)",
            type=ClaimType.AXIOM,
            domain="physics.classical_mechanics",
            confidence=1.0,
            sources=[
                Source(
                    type="textbook",
                    reference="Newton's Principia Mathematica (1687)",
                    credibility=1.0,
                    last_checked=datetime.now()
                )
            ],
            math_expression="F = ma"
        ),

        Claim(
            statement="Energy is conserved in closed systems",
            type=ClaimType.AXIOM,
            domain="physics.classical_mechanics",
            confidence=1.0,
            sources=[
                Source(
                    type="law",
                    reference="First Law of Thermodynamics",
                    credibility=1.0,
                    last_checked=datetime.now()
                )
            ]
        ),

        Claim(
            statement="Light travels at constant speed c = 299,792,458 m/s in vacuum",
            type=ClaimType.AXIOM,
            domain="physics.relativity",
            confidence=1.0,
            sources=[
                Source(
                    type="experiment",
                    reference="Michelson-Morley experiment (1887)",
                    credibility=0.95,
                    last_checked=datetime.now()
                )
            ],
            math_expression="c = 299792458\\ \\mathrm{m/s}"
        ),

        Claim(
            statement="Gravity is the curvature of spacetime",
            type=ClaimType.AXIOM,
            domain="physics.relativity",
            confidence=1.0,
            sources=[
                Source(
                    type="theory",
                    reference="General Theory of Relativity (1915)",
                    credibility=0.95,
                    last_checked=datetime.now()
                )
            ]
        ),

        Claim(
            statement="Planck's constant h = 6.626 × 10^-34 J⋅s",
            type=ClaimType.AXIOM,
            domain="physics.quantum_mechanics",
            confidence=1.0,
            sources=[
                Source(
                    type="experiment",
                    reference="Blackbody radiation experiments",
                    credibility=0.95,
                    last_checked=datetime.now()
                )
            ],
            math_expression="h = 6.626 \\times 10^{-34}\\ \\mathrm{J\\cdot s}"
        )
    ]

    return axioms


def create_derived_claims():
    """Create derived claims from axioms."""

    print("🔗 Creating derived claims...")

    derived_claims = [
        Claim(
            statement="Objects in free fall accelerate at constant rate g ≈ 9.81 m/s²",
            type=ClaimType.DERIVED,
            domain="physics.classical_mechanics",
            confidence=0.95,
            sources=[
                Source(
                    type="experiment",
                    reference="Galileo's Leaning Tower of Pisa experiment",
                    credibility=0.9,
                    last_checked=datetime.now()
                )
            ],
            math_expression="a = g \\approx 9.81\\ \\mathrm{m/s^2}"
        ),

        Claim(
            statement="Kinetic energy equals (1/2)mv²",
            type=ClaimType.DERIVED,
            domain="physics.classical_mechanics",
            confidence=0.9,
            sources=[
                Source(
                    type="derivation",
                    reference="Integration of F=ma over distance",
                    credibility=0.95,
                    last_checked=datetime.now()
                )
            ],
            math_expression="KE = \\frac{1}{2}mv^2"
        ),

        Claim(
            statement="E = mc² relates energy and mass",
            type=ClaimType.DERIVED,
            domain="physics.relativity",
            confidence=0.95,
            sources=[
                Source(
                    type="theory",
                    reference="Special Theory of Relativity",
                    credibility=0.9,
                    last_checked=datetime.now()
                )
            ],
            math_expression="E = mc^2"
        ),

        Claim(
            statement="Gravitational time dilation occurs near massive objects",
            type=ClaimType.DERIVED,
            domain="physics.relativity",
            confidence=0.9,
            sources=[
                Source(
                    type="experiment",
                    reference="Pound-Rebka experiment (1959)",
                    credibility=0.85,
                    last_checked=datetime.now()
                )
            ]
        ),

        Claim(
            statement="Photoelectric effect demonstrates particle nature of light",
            type=ClaimType.DERIVED,
            domain="physics.quantum_mechanics",
            confidence=0.9,
            sources=[
                Source(
                    type="experiment",
                    reference="Einstein's explanation (1905)",
                    credibility=0.9,
                    last_checked=datetime.now()
                )
            ]
        )
    ]

    return derived_claims


def create_knowledge_gaps():
    """Create knowledge gaps that need research."""

    print("❓ Creating knowledge gaps...")

    gaps = [
        Gap(
            question="How does gravity work at the quantum level?",
            blocked_claim_ids=[],  # Will be linked to claims that depend on this
            current_research=[
                "Quantum gravity",
                "String theory",
                "Loop quantum gravity",
                "Causal dynamical triangulation"
            ],
            importance=0.95
        ),

        Gap(
            question="What happens to information in black holes?",
            blocked_claim_ids=[],
            current_research=[
                "Black hole information paradox",
                "Holographic principle",
                "Firewall paradox",
                "AMPS paradox"
            ],
            importance=0.9
        ),

        Gap(
            question="Why is the expansion of the universe accelerating?",
            blocked_claim_ids=[],
            current_research=[
                "Dark energy",
                "Cosmological constant",
                "Quintessence",
                "Modified gravity theories"
            ],
            importance=0.85
        ),

        Gap(
            question="What is the fundamental nature of quantum entanglement?",
            blocked_claim_ids=[],
            current_research=[
                "Bell's theorem",
                "Quantum information theory",
                "Many-worlds interpretation",
                "Hidden variables"
            ],
            importance=0.8
        ),

        Gap(
            question="How do we reconcile quantum mechanics and general relativity?",
            blocked_claim_ids=[],
            current_research=[
                "Theory of everything",
                "Grand unified theory",
                "Supersymmetry",
                "Extra dimensions"
            ],
            importance=0.9
        )
    ]

    return gaps


def create_reasoning_edges(axioms, derived_claims):
    """Create edges showing how derived claims follow from axioms."""

    print("🔄 Creating reasoning relationships...")

    edges = [
        # F=ma → g = 9.81 m/s²
        Edge(
            from_claim_id=axioms[0].id,  # F = ma
            to_claim_id=derived_claims[0].id,  # g = 9.81 m/s²
            reasoning_type=ReasoningType.MATHEMATICAL_DERIVATION,
            explanation="In free fall, net force is mg, so a = g by Newton's second law",
            strength=0.95
        ),

        # F=ma → KE = 1/2 mv²
        Edge(
            from_claim_id=axioms[0].id,  # F = ma
            to_claim_id=derived_claims[1].id,  # KE = 1/2 mv²
            reasoning_type=ReasoningType.MATHEMATICAL_DERIVATION,
            explanation="Work-energy theorem: W = ΔKE, and W = ∫F⋅dx = ∫ma⋅dx = ∫mv⋅dv = (1/2)mv²",
            strength=0.9
        ),

        # c = constant → E = mc²
        Edge(
            from_claim_id=axioms[2].id,  # c = constant
            to_claim_id=derived_claims[2].id,  # E = mc²
            reasoning_type=ReasoningType.MATHEMATICAL_DERIVATION,
            explanation="From special relativity, energy-momentum relation derived from constant speed of light",
            strength=0.95
        ),

        # Gravity curvature → time dilation
        Edge(
            from_claim_id=axioms[3].id,  # Gravity is curvature
            to_claim_id=derived_claims[3].id,  # Time dilation
            reasoning_type=ReasoningType.MATHEMATICAL_DERIVATION,
            explanation="Schwarzschild metric predicts time dilation in gravitational fields",
            strength=0.9
        ),

        # Planck's constant → photoelectric effect
        Edge(
            from_claim_id=axioms[4].id,  # h = constant
            to_claim_id=derived_claims[4].id,  # Photoelectric effect
            reasoning_type=ReasoningType.EXPERIMENTAL_SUPPORT,
            explanation="Einstein used Planck's constant to explain photoelectric effect",
            strength=0.9
        )
    ]

    return edges


def populate_database():
    """Populate the database with sample data."""

    print("🚀 Populating Claudipedia database with sample physics data...")

    # Create sample data
    axioms = create_physics_axioms()
    derived_claims = create_derived_claims()
    gaps = create_knowledge_gaps()
    edges = create_reasoning_edges(axioms, derived_claims)

    # Connect to database and populate
    with KnowledgeGraph() as kg:
        print("✅ Connected to database")

        # Create axioms first
        axiom_ids = []
        for axiom in axioms:
            claim_id = kg.create_claim(axiom)
            axiom_ids.append(claim_id)
            print(f"  ✓ Created axiom: {axiom.statement[:50]}...")

        # Create derived claims
        derived_ids = []
        for claim in derived_claims:
            claim_id = kg.create_claim(claim)
            derived_ids.append(claim_id)
            print(f"  ✓ Created derived claim: {claim.statement[:50]}...")

        # Create edges
        for edge in edges:
            edge_id = kg.create_edge(edge)
            print(f"  ✓ Created reasoning edge: {edge.explanation[:50]}...")

        # Create gaps
        for gap in gaps:
            gap_id = kg.create_gap(gap)
            print(f"  ✓ Created knowledge gap: {gap.question[:50]}...")

        # Show statistics
        stats = kg.get_statistics()
        print("
📊 Database Statistics:"        print(f"  • Total claims: {stats['total_claims']}")
        print(f"  • Total edges: {stats['total_edges']}")
        print(f"  • Total gaps: {stats['total_gaps']}")
        print(f"  • Domains: {', '.join([d['domain'] for d in stats['domains'][:3]])}")

    print("\n🎉 Sample data population complete!")
    return axiom_ids, derived_ids, [gap.id for gap in gaps]


def demonstrate_queries(axiom_ids, derived_ids, gap_ids):
    """Demonstrate various database queries."""

    print("\n🔍 Demonstrating database queries...")

    with KnowledgeGraph() as kg:

        # Query 1: Find claims by pattern
        print("\n1️⃣  Searching for 'energy' claims:")
        energy_claims = kg.query_claims("energy", limit=5)
        for claim in energy_claims[:3]:
            print(f"   • {claim.statement} (confidence: {claim.confidence})")

        # Query 2: Get claims by domain
        print("\n2️⃣  Classical mechanics claims:")
        mechanics_claims = kg.get_claims_by_domain("physics.classical_mechanics", min_confidence=0.8)
        print(f"   Found {len(mechanics_claims)} claims in classical mechanics")

        # Query 3: Get supporting claims
        if derived_ids:
            print(f"\n3️⃣  Claims supporting '{derived_claims[0].statement[:30]}...':")
            supporters = kg.get_supporting_claims(derived_ids[0])
            for supporter in supporters[:2]:
                print(f"   • {supporter.statement} (strength: {supporter.metadata.get('supporting_edge', {}).get('strength', 'unknown')})")

        # Query 4: Get gaps
        print("\n4️⃣  High-priority knowledge gaps:")
        important_gaps = kg.query_gaps(min_importance=0.85, limit=3)
        for gap in important_gaps:
            print(f"   • {gap.question} (importance: {gap.importance})")

        # Query 5: Get statistics
        print("\n5️⃣  Database overview:")
        stats = kg.get_statistics()
        print(f"   • Total claims: {stats['total_claims']}")
        print(f"   • High confidence claims: {stats['high_confidence_claims']}")
        print(f"   • Top domains: {[d['domain'] for d in stats['domains'][:3]]}")


def main():
    """Main population script."""

    print("🎯 Claudipedia Sample Data Population")
    print("=" * 60)

    try:
        # Populate database
        axiom_ids, derived_ids, gap_ids = populate_database()

        # Demonstrate queries
        demonstrate_queries(axiom_ids, derived_ids, gap_ids)

        print("\n" + "=" * 60)
        print("✅ Population and demonstration complete!")
        print("\n🚀 Ready for next steps:")
        print("   • Create seed_axioms.py for comprehensive physics data")
        print("   • Build decomposition engine for complex questions")
        print("   • Add verification engine for mathematical consistency")
        print("   • Create API server for web interface")
        print("\n💡 Try: python scripts/demo/query_examples.py")

    except Exception as e:
        print(f"\n❌ Error during population: {e}")
        print("💡 Make sure Neo4j is running: docker compose up -d neo4j")
        sys.exit(1)


if __name__ == "__main__":
    main()

