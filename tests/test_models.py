"""
Unit tests for core data models.

Tests validation, serialization, and edge cases.
"""

import pytest
from datetime import datetime
from src.core.models import (
    Claim, ClaimType, Edge, ReasoningType, Gap, Source
)


class TestSource:
    """Test Source model."""

    def test_create_valid_source(self):
        """Test creating a valid source."""
        source = Source(
            type="textbook",
            reference="Principia Mathematica",
            credibility=1.0,
            last_checked=datetime.now()
        )
        assert source.type == "textbook"
        assert source.credibility == 1.0

    def test_invalid_credibility(self):
        """Test that invalid credibility raises error."""
        with pytest.raises(ValueError):
            Source(
                type="textbook",
                reference="Test",
                credibility=1.5,  # Invalid
                last_checked=datetime.now()
            )


class TestClaim:
    """Test Claim model."""

    def test_create_axiom(self):
        """Test creating an axiom with confidence 1.0."""
        source = Source(
            type="textbook",
            reference="Newton's Principia",
            credibility=1.0,
            last_checked=datetime.now()
        )

        claim = Claim(
            statement="F = ma",
            type=ClaimType.AXIOM,
            domain="physics.classical_mechanics",
            confidence=1.0,
            sources=[source],
            math_expression=r"\vec{F} = m\vec{a}"
        )

        assert claim.type == ClaimType.AXIOM
        assert claim.confidence == 1.0
        assert claim.id is not None
        assert claim.math_expression == r"\vec{F} = m\vec{a}"

    def test_axiom_must_have_confidence_one(self):
        """Test that axioms must have confidence 1.0."""
        source = Source(
            type="textbook",
            reference="Test",
            credibility=1.0,
            last_checked=datetime.now()
        )

        with pytest.raises(ValueError):
            Claim(
                statement="Test axiom",
                type=ClaimType.AXIOM,
                domain="physics.test",
                confidence=0.9,  # Invalid for axiom
                sources=[source]
            )

    def test_derived_claim(self):
        """Test creating a derived claim."""
        source = Source(
            type="paper",
            reference="Physics Review 2023",
            credibility=0.9,
            last_checked=datetime.now()
        )

        claim = Claim(
            statement="Objects fall at 9.8 m/s²",
            type=ClaimType.DERIVED,
            domain="physics.classical_mechanics",
            confidence=0.95,
            sources=[source]
        )

        assert claim.type == ClaimType.DERIVED
        assert 0 < claim.confidence < 1

    def test_claim_to_dict(self):
        """Test serialization to dictionary."""
        source = Source(
            type="textbook",
            reference="Test",
            credibility=1.0,
            last_checked=datetime.now()
        )

        claim = Claim(
            statement="Test claim",
            type=ClaimType.LAW,
            domain="physics.test",
            confidence=0.8,
            sources=[source]
        )

        data = claim.to_dict()
        assert data['statement'] == "Test claim"
        assert data['type'] == "law"
        assert data['confidence'] == 0.8
        assert len(data['sources']) == 1


class TestEdge:
    """Test Edge model."""

    def test_create_edge(self):
        """Test creating a valid edge."""
        edge = Edge(
            from_claim_id="claim1",
            to_claim_id="claim2",
            reasoning_type=ReasoningType.MATHEMATICAL_DERIVATION,
            explanation="Derived via calculus",
            strength=0.9
        )

        assert edge.from_claim_id == "claim1"
        assert edge.reasoning_type == ReasoningType.MATHEMATICAL_DERIVATION
        assert edge.strength == 0.9
        assert edge.id is not None

    def test_invalid_strength(self):
        """Test that invalid strength raises error."""
        with pytest.raises(ValueError):
            Edge(
                from_claim_id="claim1",
                to_claim_id="claim2",
                reasoning_type=ReasoningType.LOGICAL_INFERENCE,
                explanation="Test",
                strength=1.5  # Invalid
            )

    def test_edge_to_dict(self):
        """Test serialization to dictionary."""
        edge = Edge(
            from_claim_id="claim1",
            to_claim_id="claim2",
            reasoning_type=ReasoningType.EXPERIMENTAL_SUPPORT,
            explanation="Confirmed by experiment",
            strength=0.85
        )

        data = edge.to_dict()
        assert data['from_claim_id'] == "claim1"
        assert data['reasoning_type'] == "experimental_support"
        assert data['strength'] == 0.85


class TestGap:
    """Test Gap model."""

    def test_create_gap(self):
        """Test creating a valid gap."""
        gap = Gap(
            question="What is quantum gravity?",
            blocked_claim_ids=["claim1", "claim2"],
            current_research=["https://arxiv.org/..."],
            importance=0.95
        )

        assert gap.question == "What is quantum gravity?"
        assert len(gap.blocked_claim_ids) == 2
        assert gap.importance == 0.95
        assert gap.id is not None

    def test_invalid_importance(self):
        """Test that invalid importance raises error."""
        with pytest.raises(ValueError):
            Gap(
                question="Test?",
                blocked_claim_ids=[],
                current_research=[],
                importance=-0.1  # Invalid
            )

    def test_gap_to_dict(self):
        """Test serialization to dictionary."""
        gap = Gap(
            question="How do bicycles balance?",
            blocked_claim_ids=["claim5"],
            current_research=["paper1", "paper2"],
            importance=0.6
        )

        data = gap.to_dict()
        assert data['question'] == "How do bicycles balance?"
        assert len(data['blocked_claim_ids']) == 1
        assert data['importance'] == 0.6
