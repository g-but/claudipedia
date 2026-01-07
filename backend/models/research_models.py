"""
Research models for Claudipedia backend.

This module defines the data models for research profiles, contexts, and sessions
used for truth-seeking and knowledge management.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict
from enum import Enum
from datetime import datetime
import uuid


class ContextType(Enum):
    """Types of research contexts."""
    RESEARCH_PAPER = "research_paper"
    BOOK_EXCERPT = "book_excerpt"
    EXPERIMENTAL_DATA = "experimental_data"
    FIELD_NOTES = "field_notes"
    PERSONAL_INSIGHT = "personal_insight"
    WEB_RESOURCE = "web_resource"
    DATABASE_RECORD = "database_record"


class ResearchStatus(Enum):
    """Status of research activities."""
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ABANDONED = "abandoned"


@dataclass
class ResearchContext:
    """
    A research context uploaded by a user for truth-seeking.

    Attributes:
        id: Unique identifier
        title: Human-readable title for the context
        type: Type of context (paper, book, data, etc.)
        content: The actual context content (text, data, etc.)
        file_path: Path to uploaded file (if applicable)
        metadata: Additional context information (author, date, etc.)
        uploaded_by: User ID who uploaded this context
        uploaded_at: When context was uploaded
        is_verified: Whether context has been verified
        verification_notes: Notes from verification process
    """
    title: str
    type: ContextType
    content: str  # Base64 encoded or text content
    file_path: Optional[str] = None
    metadata: Dict = field(default_factory=dict)
    uploaded_by: str = ""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    uploaded_at: datetime = field(default_factory=datetime.now)
    is_verified: bool = False
    verification_notes: str = ""

    def __post_init__(self):
        if not self.content.strip():
            raise ValueError("Context content cannot be empty")

    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return {
            'id': self.id,
            'title': self.title,
            'type': self.type.value,
            'content': self.content,
            'file_path': self.file_path,
            'metadata': self.metadata,
            'uploaded_by': self.uploaded_by,
            'uploaded_at': self.uploaded_at.isoformat(),
            'is_verified': self.is_verified,
            'verification_notes': self.verification_notes
        }


@dataclass
class ResearchProfile:
    """
    A user's research profile for truth-seeking activities.

    Attributes:
        id: Unique identifier for the profile
        user_id: Associated user ID
        name: Profile name (e.g., "Quantum Physics Research")
        description: Profile description and goals
        domains: Research domains this profile focuses on
        contexts: List of research contexts uploaded to this profile
        status: Current status of research
        created_at: When profile was created
        updated_at: Last update timestamp
        metadata: Additional profile information
    """
    user_id: str
    name: str
    description: str
    domains: List[str] = field(default_factory=list)
    contexts: List[str] = field(default_factory=list)  # Context IDs
    status: ResearchStatus = ResearchStatus.ACTIVE
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    metadata: Dict = field(default_factory=dict)

    def __post_init__(self):
        if not self.name.strip():
            raise ValueError("Profile name cannot be empty")
        if not self.description.strip():
            raise ValueError("Profile description cannot be empty")

    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'description': self.description,
            'domains': self.domains,
            'contexts': self.contexts,
            'status': self.status.value,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'metadata': self.metadata
        }


@dataclass
class ResearchSession:
    """
    A research session where a user explores contexts for truth-seeking.

    Attributes:
        id: Unique session identifier
        profile_id: Associated research profile
        user_id: User conducting the research
        title: Session title
        query: What the user is seeking to understand
        relevant_contexts: Context IDs relevant to this session
        findings: Research findings and insights
        confidence: Confidence in findings (0-1)
        status: Session status
        created_at: Session start time
        completed_at: Session completion time (if completed)
    """
    profile_id: str
    user_id: str
    title: str
    query: str
    relevant_contexts: List[str] = field(default_factory=list)
    findings: str = ""
    confidence: float = 0.0
    status: ResearchStatus = ResearchStatus.ACTIVE
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None

    def __post_init__(self):
        if not self.title.strip():
            raise ValueError("Session title cannot be empty")
        if not self.query.strip():
            raise ValueError("Research query cannot be empty")
        if not 0 <= self.confidence <= 1:
            raise ValueError(f"Confidence must be 0-1, got {self.confidence}")

    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return {
            'id': self.id,
            'profile_id': self.profile_id,
            'user_id': self.user_id,
            'title': self.title,
            'query': self.query,
            'relevant_contexts': self.relevant_contexts,
            'findings': self.findings,
            'confidence': self.confidence,
            'status': self.status.value,
            'created_at': self.created_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }
