"""
Neo4j graph database interface for Claudipedia knowledge graph.

This module provides the core database operations for storing and querying:
- Claims: Statements of fact with confidence and provenance
- Edges: Reasoning relationships between claims
- Gaps: Identified knowledge gaps blocking progress

The interface handles connection pooling, error handling, and query optimization.
"""

from typing import List, Optional, Dict, Any
from contextlib import contextmanager
from dataclasses import asdict
import logging
from datetime import datetime

from neo4j import GraphDatabase, Driver, Session
from neo4j.exceptions import ServiceUnavailable, Neo4jError

from .config import config
from .models import Claim, Edge, Gap, ClaimType, ReasoningType, Source


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class KnowledgeGraph:
    """
    Neo4j interface for the Claudipedia knowledge graph.

    Handles all database operations for claims, edges, and gaps with:
    - Connection pooling and lifecycle management
    - Error handling and retry logic
    - Query optimization and indexing
    - Data validation and consistency
    """

    def __init__(self, uri: Optional[str] = None, user: Optional[str] = None,
                 password: Optional[str] = None):
        """
        Initialize the knowledge graph database connection.

        Args:
            uri: Neo4j URI (defaults to config.NEO4J_URI)
            user: Neo4j username (defaults to config.NEO4J_USER)
            password: Neo4j password (defaults to config.NEO4J_PASSWORD)
        """
        self._uri = uri or config.NEO4J_URI
        self._user = user or config.NEO4J_USER
        self._password = password or config.NEO4J_PASSWORD
        self._driver: Optional[Driver] = None

        # Connection health tracking
        self._connected = False
        self._last_error: Optional[str] = None

    def connect(self) -> None:
        """
        Establish connection to Neo4j database.

        Raises:
            ServiceUnavailable: If Neo4j is not available
            ValueError: If connection parameters are invalid
        """
        try:
            logger.info(f"Connecting to Neo4j at {self._uri}")

            # Create driver with connection pooling
            self._driver = GraphDatabase.driver(
                self._uri,
                auth=(self._user, self._password),
                # Connection pool settings for reliability
                max_connection_pool_size=10,
                connection_timeout=30
            )

            # Test connection with a simple query
            with self._driver.session() as session:
                result = session.run("RETURN 1 as test")
                result.single()

            self._connected = True
            self._last_error = None
            logger.info("Successfully connected to Neo4j")

            # Initialize database schema if needed
            self._initialize_schema()

        except ServiceUnavailable as e:
            self._connected = False
            self._last_error = f"Neo4j service unavailable: {str(e)}"
            logger.error(f"Failed to connect to Neo4j: {self._last_error}")
            raise ServiceUnavailable(f"Cannot connect to Neo4j at {self._uri}")
        except Exception as e:
            self._connected = False
            self._last_error = f"Connection error: {str(e)}"
            logger.error(f"Unexpected error connecting to Neo4j: {self._last_error}")
            raise

    def disconnect(self) -> None:
        """Close database connection and cleanup resources."""
        if self._driver:
            logger.info("Disconnecting from Neo4j")
            self._driver.close()
            self._driver = None
            self._connected = False

    def is_connected(self) -> bool:
        """Check if database connection is active."""
        return self._connected and self._driver is not None

    @contextmanager
    def session(self):
        """
        Context manager for database sessions.

        Yields:
            Neo4j session object

        Raises:
            RuntimeError: If not connected to database
            Neo4jError: For database operation errors
        """
        if not self.is_connected():
            raise RuntimeError("Not connected to database. Call connect() first.")

        session = self._driver.session()
        try:
            yield session
        except Neo4jError as e:
            logger.error(f"Database error: {str(e)}")
            raise
        finally:
            session.close()

    def _initialize_schema(self) -> None:
        """
        Initialize database schema with required constraints and indexes.

        Creates:
        - Unique constraint on Claim.id
        - Unique constraint on Gap.id
        - Index on Claim.domain for faster queries
        - Index on Claim.confidence for filtering
        - Index on Edge.reasoning_type for relationship queries
        """
        schema_queries = [
            # Constraints for data integrity
            "CREATE CONSTRAINT claim_id_unique IF NOT EXISTS FOR (c:Claim) REQUIRE c.id IS UNIQUE",
            "CREATE CONSTRAINT gap_id_unique IF NOT EXISTS FOR (g:Gap) REQUIRE g.id IS UNIQUE",

            # Indexes for performance
            "CREATE INDEX claim_domain IF NOT EXISTS FOR (c:Claim) ON (c.domain)",
            "CREATE INDEX claim_confidence IF NOT EXISTS FOR (c:Claim) ON (c.confidence)",
            "CREATE INDEX claim_type IF NOT EXISTS FOR (c:Claim) ON (c.type)",
            "CREATE INDEX edge_reasoning_type IF NOT EXISTS FOR ()-[e:Edge]-() ON (e.reasoning_type)",
            "CREATE INDEX gap_importance IF NOT EXISTS FOR (g:Gap) ON (g.importance)",
        ]

        with self.session() as session:
            for query in schema_queries:
                try:
                    session.run(query)
                    logger.debug(f"Executed schema query: {query}")
                except Neo4jError as e:
                    if "already exists" not in str(e):
                        logger.warning(f"Schema query failed: {query} - {str(e)}")

        logger.info("Database schema initialized")

    # Claim Operations

    def create_claim(self, claim: Claim) -> str:
        """
        Create a new claim in the knowledge graph.

        Args:
            claim: Claim object to store

        Returns:
            The claim ID

        Raises:
            Neo4jError: If claim creation fails
            ValueError: If claim data is invalid
        """
        if not isinstance(claim, Claim):
            raise ValueError("claim must be a Claim instance")

        # Convert claim to dictionary for storage
        claim_data = {
            'id': claim.id,
            'statement': claim.statement,
            'type': claim.type.value,
            'domain': claim.domain,
            'confidence': claim.confidence,
            'created_at': claim.created_at.isoformat(),
            'math_expression': claim.math_expression,
            'metadata': claim.metadata
        }

        # Convert sources to dictionaries
        sources_data = []
        for source in claim.sources:
            sources_data.append({
                'type': source.type,
                'reference': source.reference,
                'credibility': source.credibility,
                'last_checked': source.last_checked.isoformat()
            })

        query = """
        MERGE (c:Claim {id: $claim.id})
        ON CREATE SET
            c.statement = $claim.statement,
            c.type = $claim.type,
            c.domain = $claim.domain,
            c.confidence = $claim.confidence,
            c.created_at = $claim.created_at,
            c.math_expression = $claim.math_expression,
            c.metadata = $claim.metadata
        ON MATCH SET
            c.statement = $claim.statement,
            c.domain = $claim.domain,
            c.confidence = $claim.confidence,
            c.math_expression = $claim.math_expression,
            c.metadata = $claim.metadata
        RETURN c.id as claim_id
        """

        with self.session() as session:
            result = session.run(query, claim=claim_data)
            record = result.single()
            claim_id = record["claim_id"]

            # Update or create sources
            self._update_claim_sources(claim_id, sources_data)

        logger.info(f"Created/updated claim: {claim_id}")
        return claim_id

    def get_claim(self, claim_id: str) -> Optional[Claim]:
        """
        Retrieve a claim by ID.

        Args:
            claim_id: Unique claim identifier

        Returns:
            Claim object or None if not found
        """
        query = """
        MATCH (c:Claim {id: $claim_id})
        OPTIONAL MATCH (c)-[:SUPPORTED_BY]->(s:Source)
        RETURN c,
               collect({
                   type: s.type,
                   reference: s.reference,
                   credibility: s.credibility,
                   last_checked: s.last_checked
               }) as sources
        """

        with self.session() as session:
            result = session.run(query, claim_id=claim_id)
            record = result.single()

            if not record:
                return None

            # Reconstruct Claim object
            claim_data = dict(record["c"])
            sources_data = record["sources"]

            # Convert sources back to Source objects
            sources = []
            for source_dict in sources_data:
                sources.append(Source(
                    type=source_dict["type"],
                    reference=source_dict["reference"],
                    credibility=source_dict["credibility"],
                    last_checked=datetime.fromisoformat(source_dict["last_checked"])
                ))

            return Claim(
                id=claim_data["id"],
                statement=claim_data["statement"],
                type=ClaimType(claim_data["type"]),
                domain=claim_data["domain"],
                confidence=claim_data["confidence"],
                sources=sources,
                math_expression=claim_data.get("math_expression"),
                created_at=datetime.fromisoformat(claim_data["created_at"]),
                metadata=claim_data.get("metadata", {})
            )

    def query_claims(self, pattern: str, limit: int = 100) -> List[Claim]:
        """
        Search for claims matching a text pattern.

        Args:
            pattern: Text pattern to search for (case-insensitive)
            limit: Maximum number of results to return

        Returns:
            List of matching Claim objects
        """
        query = """
        MATCH (c:Claim)
        WHERE toLower(c.statement) CONTAINS toLower($pattern)
        OPTIONAL MATCH (c)-[:SUPPORTED_BY]->(s:Source)
        RETURN c,
               collect({
                   type: s.type,
                   reference: s.reference,
                   credibility: s.credibility,
                   last_checked: s.last_checked
               }) as sources
        ORDER BY c.confidence DESC, c.created_at DESC
        LIMIT $limit
        """

        with self.session() as session:
            result = session.run(query, pattern=pattern, limit=limit)
            claims = []

            for record in result:
                claim_data = dict(record["c"])
                sources_data = record["sources"]

                sources = []
                for source_dict in sources_data:
                    sources.append(Source(
                        type=source_dict["type"],
                        reference=source_dict["reference"],
                        credibility=source_dict["credibility"],
                        last_checked=datetime.fromisoformat(source_dict["last_checked"])
                    ))

                claim = Claim(
                    id=claim_data["id"],
                    statement=claim_data["statement"],
                    type=ClaimType(claim_data["type"]),
                    domain=claim_data["domain"],
                    confidence=claim_data["confidence"],
                    sources=sources,
                    math_expression=claim_data.get("math_expression"),
                    created_at=datetime.fromisoformat(claim_data["created_at"]),
                    metadata=claim_data.get("metadata", {})
                )
                claims.append(claim)

        logger.info(f"Found {len(claims)} claims matching pattern: {pattern}")
        return claims

    def get_claims_by_domain(self, domain: str, min_confidence: float = 0.0) -> List[Claim]:
        """
        Get all claims in a specific domain.

        Args:
            domain: Domain to filter by (e.g., "physics.classical_mechanics")
            min_confidence: Minimum confidence threshold

        Returns:
            List of claims in the domain
        """
        query = """
        MATCH (c:Claim {domain: $domain})
        WHERE c.confidence >= $min_confidence
        OPTIONAL MATCH (c)-[:SUPPORTED_BY]->(s:Source)
        RETURN c,
               collect({
                   type: s.type,
                   reference: s.reference,
                   credibility: s.credibility,
                   last_checked: s.last_checked
               }) as sources
        ORDER BY c.confidence DESC, c.created_at DESC
        """

        with self.session() as session:
            result = session.run(query, domain=domain, min_confidence=min_confidence)
            claims = []

            for record in result:
                claim_data = dict(record["c"])
                sources_data = record["sources"]

                sources = []
                for source_dict in sources_data:
                    sources.append(Source(
                        type=source_dict["type"],
                        reference=source_dict["reference"],
                        credibility=source_dict["credibility"],
                        last_checked=datetime.fromisoformat(source_dict["last_checked"])
                    ))

                claim = Claim(
                    id=claim_data["id"],
                    statement=claim_data["statement"],
                    type=ClaimType(claim_data["type"]),
                    domain=claim_data["domain"],
                    confidence=claim_data["confidence"],
                    sources=sources,
                    math_expression=claim_data.get("math_expression"),
                    created_at=datetime.fromisoformat(claim_data["created_at"]),
                    metadata=claim_data.get("metadata", {})
                )
                claims.append(claim)

        return claims

    def get_supporting_claims(self, claim_id: str) -> List[Claim]:
        """
        Get claims that support a given claim through reasoning edges.

        Args:
            claim_id: ID of the claim to find supporters for

        Returns:
            List of supporting claims ordered by edge strength
        """
        query = """
        MATCH (supported:Claim {id: $claim_id})
        MATCH (supporting:Claim)-[e:Edge]->(supported)
        WHERE e.reasoning_type IN ['mathematical_derivation', 'experimental_support', 'logical_inference']
        OPTIONAL MATCH (supporting)-[:SUPPORTED_BY]->(s:Source)
        RETURN supporting,
               e.strength as edge_strength,
               e.reasoning_type as reasoning_type,
               e.explanation as explanation,
               collect({
                   type: s.type,
                   reference: s.reference,
                   credibility: s.credibility,
                   last_checked: s.last_checked
               }) as sources
        ORDER BY e.strength DESC
        """

        with self.session() as session:
            result = session.run(query, claim_id=claim_id)
            claims = []

            for record in result:
                claim_data = dict(record["supporting"])
                sources_data = record["sources"]

                sources = []
                for source_dict in sources_data:
                    sources.append(Source(
                        type=source_dict["type"],
                        reference=source_dict["reference"],
                        credibility=source_dict["credibility"],
                        last_checked=datetime.fromisoformat(source_dict["last_checked"])
                    ))

                claim = Claim(
                    id=claim_data["id"],
                    statement=claim_data["statement"],
                    type=ClaimType(claim_data["type"]),
                    domain=claim_data["domain"],
                    confidence=claim_data["confidence"],
                    sources=sources,
                    math_expression=claim_data.get("math_expression"),
                    created_at=datetime.fromisoformat(claim_data["created_at"]),
                    metadata=claim_data.get("metadata", {})
                )

                # Add edge information to metadata
                claim.metadata['supporting_edge'] = {
                    'strength': record['edge_strength'],
                    'reasoning_type': record['reasoning_type'],
                    'explanation': record['explanation']
                }

                claims.append(claim)

        return claims

    def _update_claim_sources(self, claim_id: str, sources_data: List[Dict]) -> None:
        """Update sources for a claim (helper method)."""
        # First, remove existing sources
        session.run("MATCH (c:Claim {id: $id})-[:SUPPORTED_BY]->(s:Source) DETACH DELETE s",
                   id=claim_id)

        # Add new sources
        for source_data in sources_data:
            query = """
            MATCH (c:Claim {id: $claim_id})
            MERGE (s:Source {
                type: $source.type,
                reference: $source.reference
            })
            ON CREATE SET
                s.credibility = $source.credibility,
                s.last_checked = $source.last_checked
            MERGE (c)-[:SUPPORTED_BY]->(s)
            """

            with self.session() as session:
                session.run(query, claim_id=claim_id, source=source_data)

    # Edge Operations

    def create_edge(self, edge: Edge) -> str:
        """
        Create a reasoning edge between two claims.

        Args:
            edge: Edge object defining the relationship

        Returns:
            The edge ID

        Raises:
            Neo4jError: If edge creation fails
            ValueError: If edge data is invalid
        """
        if not isinstance(edge, Edge):
            raise ValueError("edge must be an Edge instance")

        # Verify that both claims exist
        from_claim = self.get_claim(edge.from_claim_id)
        to_claim = self.get_claim(edge.to_claim_id)

        if not from_claim:
            raise ValueError(f"Source claim not found: {edge.from_claim_id}")
        if not to_claim:
            raise ValueError(f"Target claim not found: {edge.to_claim_id}")

        edge_data = {
            'id': edge.id,
            'from_claim_id': edge.from_claim_id,
            'to_claim_id': edge.to_claim_id,
            'reasoning_type': edge.reasoning_type.value,
            'explanation': edge.explanation,
            'strength': edge.strength,
            'created_at': edge.created_at.isoformat()
        }

        query = """
        MATCH (from:Claim {id: $edge.from_claim_id})
        MATCH (to:Claim {id: $edge.to_claim_id})
        MERGE (from)-[e:Edge {id: $edge.id}]->(to)
        ON CREATE SET
            e.reasoning_type = $edge.reasoning_type,
            e.explanation = $edge.explanation,
            e.strength = $edge.strength,
            e.created_at = $edge.created_at
        ON MATCH SET
            e.reasoning_type = $edge.reasoning_type,
            e.explanation = $edge.explanation,
            e.strength = $edge.strength
        RETURN e.id as edge_id
        """

        with self.session() as session:
            result = session.run(query, edge=edge_data)
            record = result.single()
            edge_id = record["edge_id"]

        logger.info(f"Created/updated edge: {edge_id}")
        return edge_id

    def get_edge(self, edge_id: str) -> Optional[Edge]:
        """Retrieve an edge by ID (not implemented - edges accessed via claims)."""
        # For now, edges are primarily accessed through claim relationships
        # This method could be implemented later if needed for edge-specific queries
        raise NotImplementedError("Edge retrieval by ID not yet implemented")

    def get_gaps_for_claim(self, claim_id: str) -> List[Gap]:
        """
        Get knowledge gaps associated with a claim.

        Args:
            claim_id: ID of the claim to find gaps for

        Returns:
            List of Gap objects
        """
        query = """
        MATCH (c:Claim {id: $claim_id})
        MATCH (g:Gap)-[:BLOCKS]->(c)
        RETURN g
        ORDER BY g.importance DESC
        """

        with self.session() as session:
            result = session.run(query, claim_id=claim_id)
            gaps = []

            for record in result:
                gap_data = dict(record["g"])

                gap = Gap(
                    id=gap_data["id"],
                    question=gap_data["question"],
                    blocked_claim_ids=gap_data.get("blocked_claim_ids", []),
                    current_research=gap_data.get("current_research", ""),
                    importance=gap_data["importance"],
                    created_at=datetime.fromisoformat(gap_data["created_at"]),
                    metadata=gap_data.get("metadata", {})
                )
                gaps.append(gap)

        return gaps

    # Gap Operations

    def create_gap(self, gap: Gap) -> str:
        """
        Create a knowledge gap in the graph.

        Args:
            gap: Gap object to store

        Returns:
            The gap ID

        Raises:
            Neo4jError: If gap creation fails
            ValueError: If gap data is invalid
        """
        if not isinstance(gap, Gap):
            raise ValueError("gap must be a Gap instance")

        gap_data = {
            'id': gap.id,
            'question': gap.question,
            'blocked_claim_ids': gap.blocked_claim_ids,
            'current_research': gap.current_research,
            'importance': gap.importance,
            'created_at': gap.created_at.isoformat(),
            'metadata': gap.metadata
        }

        query = """
        MERGE (g:Gap {id: $gap.id})
        ON CREATE SET
            g.question = $gap.question,
            g.blocked_claim_ids = $gap.blocked_claim_ids,
            g.current_research = $gap.current_research,
            g.importance = $gap.importance,
            g.created_at = $gap.created_at,
            g.metadata = $gap.metadata
        ON MATCH SET
            g.question = $gap.question,
            g.blocked_claim_ids = $gap.blocked_claim_ids,
            g.current_research = $gap.current_research,
            g.importance = $gap.importance,
            g.metadata = $gap.metadata
        RETURN g.id as gap_id
        """

        with self.session() as session:
            result = session.run(query, gap=gap_data)
            record = result.single()
            gap_id = record["gap_id"]

            # Create BLOCKS relationships to claims
            for claim_id in gap.blocked_claim_ids:
                rel_query = """
                MATCH (g:Gap {id: $gap_id})
                MATCH (c:Claim {id: $claim_id})
                MERGE (g)-[:BLOCKS]->(c)
                """
                session.run(rel_query, gap_id=gap_id, claim_id=claim_id)

        logger.info(f"Created/updated gap: {gap_id}")
        return gap_id

    def get_gap(self, gap_id: str) -> Optional[Gap]:
        """
        Retrieve a gap by ID.

        Args:
            gap_id: Unique gap identifier

        Returns:
            Gap object or None if not found
        """
        query = """
        MATCH (g:Gap {id: $gap_id})
        RETURN g
        """

        with self.session() as session:
            result = session.run(query, gap_id=gap_id)
            record = result.single()

            if not record:
                return None

            gap_data = dict(record["g"])

            return Gap(
                id=gap_data["id"],
                question=gap_data["question"],
                blocked_claim_ids=gap_data.get("blocked_claim_ids", []),
                current_research=gap_data.get("current_research", ""),
                importance=gap_data["importance"],
                created_at=datetime.fromisoformat(gap_data["created_at"]),
                metadata=gap_data.get("metadata", {})
            )

    def query_gaps(self, min_importance: float = 0.0, limit: int = 50) -> List[Gap]:
        """
        Query gaps by importance.

        Args:
            min_importance: Minimum importance threshold
            limit: Maximum number of results

        Returns:
            List of Gap objects ordered by importance
        """
        query = """
        MATCH (g:Gap)
        WHERE g.importance >= $min_importance
        RETURN g
        ORDER BY g.importance DESC, g.created_at DESC
        LIMIT $limit
        """

        with self.session() as session:
            result = session.run(query, min_importance=min_importance, limit=limit)
            gaps = []

            for record in result:
                gap_data = dict(record["g"])

                gap = Gap(
                    id=gap_data["id"],
                    question=gap_data["question"],
                    blocked_claim_ids=gap_data.get("blocked_claim_ids", []),
                    current_research=gap_data.get("current_research", ""),
                    importance=gap_data["importance"],
                    created_at=datetime.fromisoformat(gap_data["created_at"]),
                    metadata=gap_data.get("metadata", {})
                )
                gaps.append(gap)

        return gaps

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get database statistics.

        Returns:
            Dictionary with counts of claims, edges, gaps, etc.
        """
        queries = {
            'total_claims': "MATCH (c:Claim) RETURN count(c) as count",
            'total_edges': "MATCH ()-[e:Edge]->() RETURN count(e) as count",
            'total_gaps': "MATCH (g:Gap) RETURN count(g) as count",
            'domains': "MATCH (c:Claim) RETURN c.domain, count(c) as count ORDER BY count DESC",
            'claim_types': "MATCH (c:Claim) RETURN c.type, count(c) as count ORDER BY count DESC",
            'high_confidence_claims': "MATCH (c:Claim) WHERE c.confidence >= 0.8 RETURN count(c) as count"
        }

        stats = {}
        with self.session() as session:
            for key, query in queries.items():
                result = session.run(query)
                if key in ['domains', 'claim_types']:
                    stats[key] = [dict(record) for record in result]
                else:
                    stats[key] = result.single()["count"]

        return stats

    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()

