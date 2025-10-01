"""
Configuration management for Claudipedia.

Loads settings from environment variables with sensible defaults.
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load .env file if it exists
load_dotenv()


class Config:
    """Application configuration."""

    # Neo4j Database
    NEO4J_URI: str = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    NEO4J_USER: str = os.getenv("NEO4J_USER", "neo4j")
    NEO4J_PASSWORD: str = os.getenv("NEO4J_PASSWORD", "claudipedia")

    # Anthropic API
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY")

    # API Server
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))

    # System Parameters
    DEFAULT_CONFIDENCE_THRESHOLD: float = 0.3
    MAX_DECOMPOSITION_DEPTH: int = 10
    AXIOM_CONFIDENCE: float = 1.0

    # Physics domains
    PHYSICS_DOMAINS = [
        "physics.classical_mechanics",
        "physics.thermodynamics",
        "physics.electromagnetism",
        "physics.quantum_mechanics",
        "physics.relativity",
        "physics.statistical_mechanics",
        "physics.optics",
        "physics.nuclear",
        "physics.particle",
        "physics.condensed_matter",
    ]

    # Known physics constants (for validation)
    PHYSICS_CONSTANTS = {
        "speed_of_light": 299792458,  # m/s
        "gravitational_constant": 6.674e-11,  # m³/kg·s²
        "planck_constant": 6.62607015e-34,  # J·s
        "boltzmann_constant": 1.380649e-23,  # J/K
        "elementary_charge": 1.602176634e-19,  # C
        "electron_mass": 9.1093837015e-31,  # kg
        "proton_mass": 1.67262192369e-27,  # kg
        "avogadro_number": 6.02214076e23,  # mol⁻¹
    }

    @classmethod
    def validate(cls) -> bool:
        """
        Validate configuration.

        Returns:
            True if configuration is valid

        Raises:
            ValueError if critical settings are missing
        """
        if not cls.ANTHROPIC_API_KEY:
            raise ValueError(
                "ANTHROPIC_API_KEY not set. "
                "Please set it in .env or environment variables."
            )

        if not cls.NEO4J_URI:
            raise ValueError("NEO4J_URI not set")

        return True


# Singleton instance
config = Config()
