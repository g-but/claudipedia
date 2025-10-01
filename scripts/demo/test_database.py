#!/usr/bin/env python3
"""
Interactive demo script to test Claudipedia database functionality.

This script demonstrates:
1. Creating sample physics claims
2. Building reasoning relationships
3. Querying the knowledge graph
4. Identifying knowledge gaps

Run this script to see the system in action!
"""

import sys
import os
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from core.models import Claim, Edge, Gap, ClaimType, ReasoningType, Source
from core.config import config

# Import our database interface
try:
    from core.graph_db import KnowledgeGraph
    DB_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Database interface not available: {e}")
    DB_AVAILABLE = False


def create_sample_physics_data():
    """Create sample physics claims, edges, and gaps."""

    print("📚 Creating sample physics knowledge base...")

    # Sample physics axioms (fundamental truths)
    axioms = [
        Claim(
            statement="Force equals mass times acceleration (F = ma)",
            type=ClaimType.AXIOM,
            domain="physics.classical_mechanics",
            confidence=1.0,
            sources=[
                Source(
                    type="textbook",
                    reference="Newton's Principia Mathematica",
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
            statement="Light travels at constant speed c = 299,792,458 m/s",
            type=ClaimType.AXIOM,
            domain="physics.relativity",
            confidence=1.0,
            sources=[
                Source(
                    type="experiment",
                    reference="Michelson-Morley experiment",
                    credibility=0.95,
                    last_checked=datetime.now()
                )
            ],
            math_expression="c = 299792458\\ \\mathrm{m/s}"
        )
    ]

    # Derived claims (logical consequences)
    derived_claims = [
        Claim(
            statement="Objects in free fall accelerate at constant rate g = 9.8 m/s²",
            type=ClaimType.DERIVED,
            domain="physics.classical_mechanics",
            confidence=0.95,
            sources=[
                Source(
                    type="experiment",
                    reference="Galileo tower experiment",
                    credibility=0.9,
                    last_checked=datetime.now()
                )
            ],
            math_expression="a = g = 9.8\\ \\mathrm{m/s^2}"
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
        )
    ]

    # Knowledge gaps (things we don't understand)
    gaps = [
        Gap(
            question="How does gravity work at the quantum level?",
            blocked_claim_ids=[],  # Will be linked to claims that depend on this
            current_research=["Quantum gravity", "String theory", "Loop quantum gravity"],
            importance=0.9
        ),

        Gap(
            question="What happens to information in black holes?",
            blocked_claim_ids=[],
            current_research=["Black hole information paradox", "Holographic principle"],
            importance=0.85
        ),

        Gap(
            question="Why is the expansion of the universe accelerating?",
            blocked_claim_ids=[],
            current_research=["Dark energy", "Cosmological constant"],
            importance=0.8
        )
    ]

    return axioms, derived_claims, gaps


def demonstrate_database_operations():
    """Demonstrate database operations if available."""

    if not DB_AVAILABLE:
        print("\n⚠️  Database interface not available for live demo")
        print("💡 To enable live demo:")
        print("   1. Start Neo4j: docker compose up -d neo4j")
        print("   2. Ensure .env file has correct database credentials")
        return None

    print("\n🔗 Testing database operations...")

    try:
        # Test connection
        with KnowledgeGraph() as kg:
            print("✅ Connected to Neo4j database")
            # Get initial statistics
            stats = kg.get_statistics()
            print(f"📊 Database stats: {stats}")

            return kg

    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("💡 Make sure Neo4j is running: docker compose up -d neo4j")
        return None


def demonstrate_knowledge_graph_concepts():
    """Show how the knowledge graph concepts work together."""

    print("\n🧠 Claudipedia Knowledge Graph Concepts")
    print("=" * 50)

    axioms, derived_claims, gaps = create_sample_physics_data()

    print("\n📋 SAMPLE AXIOMS (Fundamental Truths):")
    for i, axiom in enumerate(axioms, 1):
        print(f"  {i}. {axiom.statement}")
        print(f"     Domain: {axiom.domain}")
        print(f"     Confidence: {axiom.confidence}")
        print(f"     Math: {axiom.math_expression or 'N/A'}")

    print("\n🔗 SAMPLE DERIVED CLAIMS (Logical Consequences):")
    for i, claim in enumerate(derived_claims, 1):
        print(f"  {i}. {claim.statement}")
        print(f"     Type: {claim.type.value}")
        print(f"     Confidence: {claim.confidence}")

    print("\n❓ SAMPLE KNOWLEDGE GAPS (What We Don't Know):")
    for i, gap in enumerate(gaps, 1):
        print(f"  {i}. {gap.question}")
        print(f"     Importance: {gap.importance}")
        print(f"     Current Research: {', '.join(gap.current_research)}")

    print("\n🔄 HOW THEY CONNECT:")
    print("  • Axioms → Derived Claims (via mathematical derivation)")
    print("  • Claims → Gaps (when gaps block further understanding)")
    print("  • Edges represent reasoning strength and explanation")
    print("  • Sources provide credibility and provenance")

    return axioms, derived_claims, gaps


def show_next_steps():
    """Show what we could build next."""

    print("\n🚀 Next Steps We Could Take:")
    print("=" * 50)

    steps = [
        ("📚 Step 4: Seed Physics Axioms",
         "Load hundreds of physics axioms, laws, and constants into the database",
         "Create scripts/seed_axioms.py with comprehensive physics knowledge"),

        ("🔍 Step 5: Decomposition Engine",
         "Break complex questions into smaller, answerable parts",
         "Use AI to recursively decompose problems like 'Why do objects fall?'"),

        ("✅ Step 6: Verification Engine",
         "Check claims for mathematical consistency and logical validity",
         "Use SymPy to verify equations and detect contradictions"),

        ("🎯 Step 7: Gap Detection",
         "Automatically identify missing knowledge and research opportunities",
         "Find low-confidence areas and contradictions in the knowledge graph"),

        ("🤖 Step 8: Synthesis Engine",
         "Generate natural language answers from the knowledge graph",
         "Combine multiple claims to answer complex questions"),

        ("🌐 Step 9: API Server",
         "Create REST API for querying the knowledge graph",
         "Build /query, /claim/{id}, /gaps endpoints"),

        ("🧪 Step 10: Test Queries",
         "Answer real physics questions to validate the system",
         "Test with questions like 'Why do objects fall?' or 'What are black holes?'")
    ]

    for i, (title, description, implementation) in enumerate(steps, 1):
        print(f"\n  {i}. {title}")
        print(f"     {description}")
        print(f"     💻 {implementation}")

    print("\n💡 Current Status: 30% Complete (Steps 1-3 done)")
    print("🔥 Ready to tackle any of these next steps!")


def main():
    """Main demo function."""

    print("🎯 Claudipedia Interactive Demo")
    print("=" * 50)
    print("Welcome to the Physics Knowledge Graph System!")
    print()

    # Show knowledge graph concepts
    axioms, derived_claims, gaps = demonstrate_knowledge_graph_concepts()

    # Test database operations
    kg = demonstrate_database_operations()

    # Show next steps
    show_next_steps()

    print("\n" + "=" * 50)
    print("✨ Demo Complete!")
    print()
    print("💡 To get started with real functionality:")
    print("   1. Start Neo4j: docker compose up -d neo4j")
    print("   2. Run: python scripts/demo/populate_sample_data.py")
    print("   3. Query: python scripts/demo/query_examples.py")
    print()
    print("🚀 Ready to build something amazing!")


if __name__ == "__main__":
    main()
