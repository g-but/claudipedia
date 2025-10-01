"""
Comprehensive tests for the KnowledgeGraph database interface.

Tests cover:
- Connection management and lifecycle
- Claim CRUD operations
- Edge creation and relationships
- Gap management
- Query functionality
- Error handling and edge cases
- Schema initialization
"""

import unittest
import uuid
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock

from src.core.models import Claim, Edge, Gap, ClaimType, ReasoningType, Source
from src.core.graph_db import KnowledgeGraph
from src.core.config import config


class TestKnowledgeGraph(unittest.TestCase):
    """Test suite for KnowledgeGraph database operations."""

    def setUp(self):
        """Set up test fixtures."""
        # Create a mock Neo4j driver for testing
        self.mock_driver = Mock()
        self.mock_session = Mock()
        self.mock_driver.session.return_value = self.mock_session

        # Create test data
        self.test_claim = Claim(
            statement="Force equals mass times acceleration",
            type=ClaimType.AXIOM,
            domain="physics.classical_mechanics",
            confidence=1.0,
            sources=[
                Source(
                    type="textbook",
                    reference="Physics for Scientists and Engineers",
                    credibility=0.9,
                    last_checked=datetime.now()
                )
            ]
        )

        self.test_derived_claim = Claim(
            statement="Objects in free fall accelerate at 9.8 m/s²",
            type=ClaimType.DERIVED,
            domain="physics.classical_mechanics",
            confidence=0.95,
            sources=[
                Source(
                    type="experiment",
                    reference="Galileo tower experiment",
                    credibility=0.85,
                    last_checked=datetime.now()
                )
            ]
        )

        self.test_gap = Gap(
            question="Why does gravity work?",
            blocked_claim_ids=[self.test_derived_claim.id],
            current_research=["Quantum gravity research"],
            importance=0.8
        )

        self.test_edge = Edge(
            from_claim_id=self.test_claim.id,
            to_claim_id=self.test_derived_claim.id,
            reasoning_type=ReasoningType.MATHEMATICAL_DERIVATION,
            explanation="F=ma implies constant acceleration in free fall",
            strength=0.9
        )

    def tearDown(self):
        """Clean up after tests."""
        pass

    @patch('src.core.graph_db.GraphDatabase.driver')
    def test_connect_success(self, mock_driver_class):
        """Test successful database connection."""
        # Setup mock
        mock_driver = Mock()
        mock_driver_class.return_value = mock_driver
        mock_session = Mock()
        mock_driver.session.return_value = mock_session
        mock_session.run.return_value.single.return_value = {'test': 1}

        # Test connection
        kg = KnowledgeGraph()
        kg.connect()

        # Verify connection was established
        self.assertTrue(kg.is_connected())
        mock_driver_class.assert_called_once()
        mock_session.run.assert_called()

    @patch('src.core.graph_db.GraphDatabase.driver')
    def test_connect_failure(self, mock_driver_class):
        """Test connection failure handling."""
        # Setup mock to raise ServiceUnavailable
        mock_driver_class.side_effect = Exception("Connection failed")

        kg = KnowledgeGraph()

        with self.assertRaises(Exception):
            kg.connect()

        self.assertFalse(kg.is_connected())

    def test_disconnect(self):
        """Test database disconnection."""
        kg = KnowledgeGraph()
        kg._driver = Mock()
        kg._connected = True

        kg.disconnect()

        self.assertFalse(kg.is_connected())
        self.assertIsNone(kg._driver)

    def test_context_manager(self):
        """Test context manager functionality."""
        with patch.object(KnowledgeGraph, 'connect'), \
             patch.object(KnowledgeGraph, 'disconnect'):

            with KnowledgeGraph() as kg:
                pass

            # Should have called connect and disconnect
            self.assertTrue(KnowledgeGraph.connect.called)
            self.assertTrue(KnowledgeGraph.disconnect.called)

    @patch('src.core.graph_db.GraphDatabase.driver')
    def test_create_claim(self, mock_driver_class):
        """Test claim creation."""
        # Setup mocks
        mock_driver = Mock()
        mock_driver_class.return_value = mock_driver
        mock_session = Mock()
        mock_driver.session.return_value = mock_session
        mock_session.run.return_value.single.return_value = {'claim_id': self.test_claim.id}

        kg = KnowledgeGraph()
        kg._driver = mock_driver
        kg._connected = True

        # Test claim creation
        result_id = kg.create_claim(self.test_claim)

        self.assertEqual(result_id, self.test_claim.id)
        self.assertEqual(mock_session.run.call_count, 2)  # One for claim, one for sources

    @patch('src.core.graph_db.GraphDatabase.driver')
    def test_create_claim_invalid_type(self, mock_driver_class):
        """Test claim creation with invalid claim object."""
        kg = KnowledgeGraph()

        with self.assertRaises(ValueError) as context:
            kg.create_claim("not a claim object")

        self.assertIn("Claim instance", str(context.exception))

    @patch('src.core.graph_db.GraphDatabase.driver')
    def test_get_claim(self, mock_driver_class):
        """Test claim retrieval."""
        # Setup mock data
        mock_claim_data = {
            'id': self.test_claim.id,
            'statement': self.test_claim.statement,
            'type': self.test_claim.type.value,
            'domain': self.test_claim.domain,
            'confidence': self.test_claim.confidence,
            'created_at': self.test_claim.created_at.isoformat(),
            'math_expression': None,
            'metadata': {}
        }

        mock_sources_data = [{
            'type': 'textbook',
            'reference': 'Physics for Scientists and Engineers',
            'credibility': 0.9,
            'last_checked': datetime.now().isoformat()
        }]

        # Setup mocks
        mock_driver = Mock()
        mock_driver_class.return_value = mock_driver
        mock_session = Mock()
        mock_driver.session.return_value = mock_session

        mock_result = Mock()
        mock_session.run.return_value = mock_result
        mock_result.single.return_value = {
            'c': mock_claim_data,
            'sources': mock_sources_data
        }

        kg = KnowledgeGraph()
        kg._driver = mock_driver
        kg._connected = True

        # Test claim retrieval
        retrieved_claim = kg.get_claim(self.test_claim.id)

        self.assertIsNotNone(retrieved_claim)
        self.assertEqual(retrieved_claim.id, self.test_claim.id)
        self.assertEqual(retrieved_claim.statement, self.test_claim.statement)
        self.assertEqual(len(retrieved_claim.sources), 1)

    @patch('src.core.graph_db.GraphDatabase.driver')
    def test_get_claim_not_found(self, mock_driver_class):
        """Test claim retrieval when claim doesn't exist."""
        # Setup mocks
        mock_driver = Mock()
        mock_driver_class.return_value = mock_driver
        mock_session = Mock()
        mock_driver.session.return_value = mock_session

        mock_result = Mock()
        mock_session.run.return_value = mock_result
        mock_result.single.return_value = None  # Claim not found

        kg = KnowledgeGraph()
        kg._driver = mock_driver
        kg._connected = True

        # Test claim retrieval
        retrieved_claim = kg.get_claim("nonexistent-id")

        self.assertIsNone(retrieved_claim)

    @patch('src.core.graph_db.GraphDatabase.driver')
    def test_query_claims(self, mock_driver_class):
        """Test claim querying by pattern."""
        # Setup mock data
        mock_claim_data = {
            'id': self.test_claim.id,
            'statement': self.test_claim.statement,
            'type': self.test_claim.type.value,
            'domain': self.test_claim.domain,
            'confidence': self.test_claim.confidence,
            'created_at': self.test_claim.created_at.isoformat(),
            'math_expression': None,
            'metadata': {}
        }

        # Setup mocks
        mock_driver = Mock()
        mock_driver_class.return_value = mock_driver
        mock_session = Mock()
        mock_driver.session.return_value = mock_session

        mock_result = Mock()
        mock_session.run.return_value = mock_result
        mock_result.__iter__ = Mock(return_value=iter([{
            'c': mock_claim_data,
            'sources': []
        }]))

        kg = KnowledgeGraph()
        kg._driver = mock_driver
        kg._connected = True

        # Test claim querying
        results = kg.query_claims("force", limit=10)

        self.assertIsInstance(results, list)
        mock_session.run.assert_called_once()

    @patch('src.core.graph_db.GraphDatabase.driver')
    def test_get_claims_by_domain(self, mock_driver_class):
        """Test getting claims by domain."""
        # Setup mock data
        mock_claim_data = {
            'id': self.test_claim.id,
            'statement': self.test_claim.statement,
            'type': self.test_claim.type.value,
            'domain': self.test_claim.domain,
            'confidence': self.test_claim.confidence,
            'created_at': self.test_claim.created_at.isoformat(),
            'math_expression': None,
            'metadata': {}
        }

        # Setup mocks
        mock_driver = Mock()
        mock_driver_class.return_value = mock_driver
        mock_session = Mock()
        mock_driver.session.return_value = mock_session

        mock_result = Mock()
        mock_session.run.return_value = mock_result
        mock_result.__iter__ = Mock(return_value=iter([{
            'c': mock_claim_data,
            'sources': []
        }]))

        kg = KnowledgeGraph()
        kg._driver = mock_driver
        kg._connected = True

        # Test domain filtering
        results = kg.get_claims_by_domain("physics.classical_mechanics", min_confidence=0.5)

        self.assertIsInstance(results, list)
        mock_session.run.assert_called_once()

    @patch('src.core.graph_db.GraphDatabase.driver')
    def test_create_edge(self, mock_driver_class):
        """Test edge creation."""
        # Setup mocks for claim existence checks and edge creation
        mock_driver = Mock()
        mock_driver_class.return_value = mock_driver
        mock_session = Mock()
        mock_driver.session.return_value = mock_session

        # Mock claim existence checks
        mock_claim_result = Mock()
        mock_session.run.return_value = mock_claim_result
        mock_claim_result.single.return_value = {
            'c': {'id': self.test_claim.id},
            'sources': []
        }

        # Mock edge creation result
        mock_edge_result = Mock()
        mock_session.run.return_value = mock_edge_result
        mock_edge_result.single.return_value = {'edge_id': self.test_edge.id}

        kg = KnowledgeGraph()
        kg._driver = mock_driver
        kg._connected = True

        # Mock get_claim method to return test claims
        kg.get_claim = Mock(side_effect=[self.test_claim, self.test_derived_claim])

        # Test edge creation
        result_id = kg.create_edge(self.test_edge)

        self.assertEqual(result_id, self.test_edge.id)

    @patch('src.core.graph_db.GraphDatabase.driver')
    def test_create_edge_missing_claim(self, mock_driver_class):
        """Test edge creation with missing source claim."""
        kg = KnowledgeGraph()
        kg._driver = Mock()
        kg._connected = True

        # Mock get_claim to return None for missing claim
        kg.get_claim = Mock(return_value=None)

        # Create edge with non-existent source claim
        edge = Edge(
            from_claim_id="nonexistent-id",
            to_claim_id=self.test_derived_claim.id,
            reasoning_type=ReasoningType.MATHEMATICAL_DERIVATION,
            explanation="Test edge",
            strength=0.8
        )

        with self.assertRaises(ValueError) as context:
            kg.create_edge(edge)

        self.assertIn("Source claim not found", str(context.exception))

    @patch('src.core.graph_db.GraphDatabase.driver')
    def test_create_gap(self, mock_driver_class):
        """Test gap creation."""
        # Setup mocks
        mock_driver = Mock()
        mock_driver_class.return_value = mock_driver
        mock_session = Mock()
        mock_driver.session.return_value = mock_session

        mock_result = Mock()
        mock_session.run.return_value = mock_result
        mock_result.single.return_value = {'gap_id': self.test_gap.id}

        kg = KnowledgeGraph()
        kg._driver = mock_driver
        kg._connected = True

        # Test gap creation
        result_id = kg.create_gap(self.test_gap)

        self.assertEqual(result_id, self.test_gap.id)
        # Should call run twice: once for gap creation, once for each blocked claim
        self.assertEqual(mock_session.run.call_count, 2)

    @patch('src.core.graph_db.GraphDatabase.driver')
    def test_get_gap(self, mock_driver_class):
        """Test gap retrieval."""
        # Setup mock data
        mock_gap_data = {
            'id': self.test_gap.id,
            'question': self.test_gap.question,
            'blocked_claim_ids': self.test_gap.blocked_claim_ids,
            'current_research': self.test_gap.current_research,
            'importance': self.test_gap.importance,
            'created_at': self.test_gap.created_at.isoformat(),
            'metadata': {}
        }

        # Setup mocks
        mock_driver = Mock()
        mock_driver_class.return_value = mock_driver
        mock_session = Mock()
        mock_driver.session.return_value = mock_session

        mock_result = Mock()
        mock_session.run.return_value = mock_result
        mock_result.single.return_value = {'g': mock_gap_data}

        kg = KnowledgeGraph()
        kg._driver = mock_driver
        kg._connected = True

        # Test gap retrieval
        retrieved_gap = kg.get_gap(self.test_gap.id)

        self.assertIsNotNone(retrieved_gap)
        self.assertEqual(retrieved_gap.id, self.test_gap.id)
        self.assertEqual(retrieved_gap.question, self.test_gap.question)

    @patch('src.core.graph_db.GraphDatabase.driver')
    def test_query_gaps(self, mock_driver_class):
        """Test gap querying by importance."""
        # Setup mock data
        mock_gap_data = {
            'id': self.test_gap.id,
            'question': self.test_gap.question,
            'blocked_claim_ids': self.test_gap.blocked_claim_ids,
            'current_research': self.test_gap.current_research,
            'importance': self.test_gap.importance,
            'created_at': self.test_gap.created_at.isoformat(),
            'metadata': {}
        }

        # Setup mocks
        mock_driver = Mock()
        mock_driver_class.return_value = mock_driver
        mock_session = Mock()
        mock_driver.session.return_value = mock_session

        mock_result = Mock()
        mock_session.run.return_value = mock_result
        mock_result.__iter__ = Mock(return_value=iter([{'g': mock_gap_data}]))

        kg = KnowledgeGraph()
        kg._driver = mock_driver
        kg._connected = True

        # Test gap querying
        results = kg.query_gaps(min_importance=0.5, limit=10)

        self.assertIsInstance(results, list)
        mock_session.run.assert_called_once()

    @patch('src.core.graph_db.GraphDatabase.driver')
    def test_get_gaps_for_claim(self, mock_driver_class):
        """Test getting gaps associated with a claim."""
        # Setup mock data
        mock_gap_data = {
            'id': self.test_gap.id,
            'question': self.test_gap.question,
            'blocked_claim_ids': self.test_gap.blocked_claim_ids,
            'current_research': self.test_gap.current_research,
            'importance': self.test_gap.importance,
            'created_at': self.test_gap.created_at.isoformat(),
            'metadata': {}
        }

        # Setup mocks
        mock_driver = Mock()
        mock_driver_class.return_value = mock_driver
        mock_session = Mock()
        mock_driver.session.return_value = mock_session

        mock_result = Mock()
        mock_session.run.return_value = mock_result
        mock_result.__iter__ = Mock(return_value=iter([{'g': mock_gap_data}]))

        kg = KnowledgeGraph()
        kg._driver = mock_driver
        kg._connected = True

        # Test gaps for claim
        gaps = kg.get_gaps_for_claim(self.test_derived_claim.id)

        self.assertIsInstance(gaps, list)
        mock_session.run.assert_called_once()

    @patch('src.core.graph_db.GraphDatabase.driver')
    def test_get_supporting_claims(self, mock_driver_class):
        """Test getting claims that support another claim."""
        # Setup mock data
        mock_claim_data = {
            'id': self.test_claim.id,
            'statement': self.test_claim.statement,
            'type': self.test_claim.type.value,
            'domain': self.test_claim.domain,
            'confidence': self.test_claim.confidence,
            'created_at': self.test_claim.created_at.isoformat(),
            'math_expression': None,
            'metadata': {}
        }

        # Setup mocks
        mock_driver = Mock()
        mock_driver_class.return_value = mock_driver
        mock_session = Mock()
        mock_driver.session.return_value = mock_session

        mock_result = Mock()
        mock_session.run.return_value = mock_result
        mock_result.__iter__ = Mock(return_value=iter([{
            'supporting': mock_claim_data,
            'sources': [],
            'edge_strength': 0.9,
            'reasoning_type': 'mathematical_derivation',
            'explanation': 'F=ma derivation'
        }]))

        kg = KnowledgeGraph()
        kg._driver = mock_driver
        kg._connected = True

        # Test supporting claims
        supporters = kg.get_supporting_claims(self.test_derived_claim.id)

        self.assertIsInstance(supporters, list)
        mock_session.run.assert_called_once()

    @patch('src.core.graph_db.GraphDatabase.driver')
    def test_get_statistics(self, mock_driver_class):
        """Test database statistics."""
        # Setup mock results for different queries
        mock_session = Mock()

        # Mock total_claims
        mock_result1 = Mock()
        mock_result1.single.return_value = {'count': 42}
        mock_session.run.return_value = mock_result1

        # Mock domains
        mock_result2 = Mock()
        mock_result2.__iter__ = Mock(return_value=iter([
            {'domain': 'physics.classical_mechanics', 'count': 20},
            {'domain': 'physics.quantum_mechanics', 'count': 15}
        ]))

        # Setup driver to return different results for different calls
        mock_driver = Mock()
        mock_driver_class.return_value = mock_driver
        mock_driver.session.return_value = mock_session

        call_count = 0
        def mock_run_side_effect(query):
            nonlocal call_count
            call_count += 1
            if 'MATCH (c:Claim) RETURN count' in query:
                return mock_result1
            elif 'RETURN c.domain, count' in query:
                return mock_result2
            else:
                return Mock()

        mock_session.run.side_effect = mock_run_side_effect

        kg = KnowledgeGraph()
        kg._driver = mock_driver
        kg._connected = True

        # Test statistics
        stats = kg.get_statistics()

        self.assertIsInstance(stats, dict)
        self.assertIn('total_claims', stats)
        self.assertIn('domains', stats)
        self.assertEqual(stats['total_claims'], 42)

    def test_session_context_manager_not_connected(self):
        """Test session context manager when not connected."""
        kg = KnowledgeGraph()

        with self.assertRaises(RuntimeError) as context:
            with kg.session() as session:
                pass

        self.assertIn("Not connected", str(context.exception))

    @patch('src.core.graph_db.GraphDatabase.driver')
    def test_schema_initialization(self, mock_driver_class):
        """Test database schema initialization."""
        # Setup mocks
        mock_driver = Mock()
        mock_driver_class.return_value = mock_driver
        mock_session = Mock()
        mock_driver.session.return_value = mock_session

        # Mock successful connection and schema queries
        mock_result = Mock()
        mock_session.run.return_value = mock_result
        mock_result.single.return_value = {'test': 1}

        kg = KnowledgeGraph()
        kg.connect()

        # Verify schema queries were executed
        self.assertTrue(mock_session.run.called)
        # Should have called for connection test + schema queries
        self.assertGreaterEqual(mock_session.run.call_count, 5)


if __name__ == '__main__':
    unittest.main()

