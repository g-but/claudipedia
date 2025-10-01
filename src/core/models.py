"""
Core data models for Claudipedia knowledge graph.

This module defines the fundamental data structures:
- Claim: A statement of fact with confidence and provenance
- Edge: A relationship between claims with reasoning
- Gap: An identified knowledge gap blocking progress
- Source: A reference supporting a claim
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict
from enum import Enum
from datetime import datetime
import uuid


class ClaimType(Enum):
    """Types of claims in the knowledge graph."""
    AXIOM = "axiom"              # Fundamental truth (e.g., F=ma)
    LAW = "law"                  # Well-established physical law
    DERIVED = "derived"          # Logically derived from other claims
    EMPIRICAL = "empirical"      # Based on experimental data
    GAP = "gap"                  # Known unknown


class ReasoningType(Enum):
    """Types of reasoning connecting claims."""
    MATHEMATICAL_DERIVATION = "mathematical_derivation"  # Proven via math
    EXPERIMENTAL_SUPPORT = "experimental_support"        # Supported by data
    LOGICAL_INFERENCE = "logical_inference"              # Follows logically
    DEFINITION = "definition"                            # By definition
    CONTRADICTION = "contradiction"                      # Conflicts with


@dataclass
class Source:
    """
    A reference supporting a claim.

    Attributes:
        type: Category of source (textbook, paper, experiment, database)
        reference: Citation or identifier
        credibility: Confidence in this source (0-1)
        last_checked: When this source was last verified
    """
    type: str
    reference: str
    credibility: float
    last_checked: datetime

    def __post_init__(self):
        if not 0 <= self.credibility <= 1:
            raise ValueError(f"Credibility must be 0-1, got {self.credibility}")


@dataclass
class Claim:
    """
    A statement in the knowledge graph.

    Attributes:
        id: Unique identifier
        statement: Natural language statement
        type: Category of claim (axiom, law, derived, empirical, gap)
        domain: Subject area (e.g., "physics.classical_mechanics")
        confidence: How certain we are (0-1)
        sources: Supporting references
        math_expression: LaTeX mathematical formulation (optional)
        created_at: Timestamp
        metadata: Additional structured data
    """
    statement: str
    type: ClaimType
    domain: str
    confidence: float
    sources: List[Source]
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    math_expression: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict = field(default_factory=dict)

    def __post_init__(self):
        if not 0 <= self.confidence <= 1:
            raise ValueError(f"Confidence must be 0-1, got {self.confidence}")

        # Axioms should have confidence 1.0
        if self.type == ClaimType.AXIOM and self.confidence != 1.0:
            raise ValueError("Axioms must have confidence 1.0")

    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return {
            'id': self.id,
            'statement': self.statement,
            'type': self.type.value,
            'domain': self.domain,
            'confidence': self.confidence,
            'sources': [
                {
                    'type': s.type,
                    'reference': s.reference,
                    'credibility': s.credibility,
                    'last_checked': s.last_checked.isoformat()
                } for s in self.sources
            ],
            'math_expression': self.math_expression,
            'created_at': self.created_at.isoformat(),
            'metadata': self.metadata
        }


@dataclass
class Edge:
    """
    A relationship between two claims.

    Represents how one claim supports or relates to another.

    Attributes:
        from_claim_id: Source claim ID
        to_claim_id: Target claim ID
        reasoning_type: How they're related
        explanation: Human-readable description
        strength: Strength of connection (0-1)
        id: Unique identifier
        metadata: Additional structured data
    """
    from_claim_id: str
    to_claim_id: str
    reasoning_type: ReasoningType
    explanation: str
    strength: float
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    metadata: Dict = field(default_factory=dict)

    def __post_init__(self):
        if not 0 <= self.strength <= 1:
            raise ValueError(f"Strength must be 0-1, got {self.strength}")

    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return {
            'id': self.id,
            'from_claim_id': self.from_claim_id,
            'to_claim_id': self.to_claim_id,
            'reasoning_type': self.reasoning_type.value,
            'explanation': self.explanation,
            'strength': self.strength,
            'metadata': self.metadata
        }


@dataclass
class Gap:
    """
    An identified knowledge gap.

    Represents something we don't know that blocks further reasoning.

    Attributes:
        question: What don't we know?
        blocked_claim_ids: Claims that depend on resolving this gap
        current_research: Links to ongoing research
        importance: How critical this gap is (0-1)
        id: Unique identifier
        created_at: When gap was identified
        metadata: Additional structured data
    """
    question: str
    blocked_claim_ids: List[str]
    current_research: List[str]
    importance: float
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict = field(default_factory=dict)

    def __post_init__(self):
        if not 0 <= self.importance <= 1:
            raise ValueError(f"Importance must be 0-1, got {self.importance}")

    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return {
            'id': self.id,
            'question': self.question,
            'blocked_claim_ids': self.blocked_claim_ids,
            'current_research': self.current_research,
            'importance': self.importance,
            'created_at': self.created_at.isoformat(),
            'metadata': self.metadata
        }


# Type hints for collections
ClaimList = List[Claim]
EdgeList = List[Edge]
GapList = List[Gap]
