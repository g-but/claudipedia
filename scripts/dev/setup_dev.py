#!/usr/bin/env python3
"""
Development environment setup script for Claudipedia.

This script helps set up the development environment by:
1. Checking system requirements
2. Setting up environment variables
3. Starting Docker services
4. Running database migrations
5. Creating initial test data
"""

import os
import sys
import subprocess
import argparse
import shutil
from pathlib import Path
from typing import List, Optional


class DevSetup:
    """Development environment setup utilities."""

    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.env_file = self.project_root / '.env'
        self.env_example = self.project_root / '.env.example'

    def check_requirements(self) -> bool:
        """Check if all system requirements are met."""
        print("🔍 Checking system requirements...")

        requirements = [
            ('Docker', self._check_docker),
            ('Docker Compose', self._check_docker_compose),
            ('Python 3.11+', self._check_python),
            ('Git', self._check_git),
        ]

        all_met = True
        for name, check_func in requirements:
            if check_func():
                print(f"✅ {name}")
            else:
                print(f"❌ {name} - not found")
                all_met = False

        return all_met

    def _check_docker(self) -> bool:
        """Check if Docker is installed and running."""
        try:
            result = subprocess.run(['docker', '--version'],
                                  capture_output=True, text=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def _check_docker_compose(self) -> bool:
        """Check if Docker Compose is available."""
        try:
            result = subprocess.run(['docker', 'compose', 'version'],
                                  capture_output=True, text=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            try:
                result = subprocess.run(['docker-compose', '--version'],
                                      capture_output=True, text=True, check=True)
                return True
            except (subprocess.CalledProcessError, FileNotFoundError):
                return False

    def _check_python(self) -> bool:
        """Check if Python 3.11+ is available."""
        try:
            result = subprocess.run([sys.executable, '--version'],
                                  capture_output=True, text=True, check=True)
            version = result.stdout.strip().split()[-1]
            major, minor = map(int, version.split('.')[:2])
            return major >= 3 and minor >= 11
        except (subprocess.CalledProcessError, FileNotFoundError, ValueError):
            return False

    def _check_git(self) -> bool:
        """Check if Git is available."""
        try:
            result = subprocess.run(['git', '--version'],
                                  capture_output=True, text=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def setup_environment(self) -> None:
        """Set up environment variables."""
        print("🔧 Setting up environment...")

        if not self.env_example.exists():
            print("⚠️  No .env.example file found")
            return

        if not self.env_file.exists():
            print("📝 Creating .env file from template...")
            shutil.copy(self.env_example, self.env_file)
            print("✅ .env file created")
        else:
            print("✅ .env file already exists")

        # Check for required API keys
        self._check_api_keys()

    def _check_api_keys(self) -> None:
        """Check for required API keys."""
        if not self.env_file.exists():
            return

        with open(self.env_file, 'r') as f:
            env_content = f.read()

        if 'ANTHROPIC_API_KEY' not in env_content or 'your-api-key-here' in env_content:
            print("⚠️  ANTHROPIC_API_KEY not set in .env file")
            print("   Please set your Anthropic API key to use AI features")

    def start_services(self, background: bool = True) -> None:
        """Start Docker services."""
        print("🚀 Starting Docker services...")

        cmd = ['docker', 'compose', 'up', '-d']

        try:
            result = subprocess.run(cmd, cwd=self.project_root, check=True)
            print("✅ Services started successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to start services: {e}")
            raise

    def wait_for_services(self) -> None:
        """Wait for services to be ready."""
        print("⏳ Waiting for services to be ready...")

        services = [
            ('neo4j', self._check_neo4j_ready),
            ('backend', self._check_backend_ready),
            ('frontend', self._check_frontend_ready),
            ('redis', self._check_redis_ready),
        ]

        for service_name, check_func in services:
            print(f"   Checking {service_name}...", end=' ')
            if check_func():
                print("✅")
            else:
                print("❌")
                raise RuntimeError(f"Service {service_name} is not ready")

    def _check_neo4j_ready(self) -> bool:
        """Check if Neo4j is ready."""
        try:
            # Try to connect to Neo4j HTTP interface
            result = subprocess.run(
                ['curl', '-f', 'http://localhost:7474'],
                capture_output=True, timeout=10
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False

    def _check_redis_ready(self) -> bool:
        """Check if Redis is ready."""
        try:
            result = subprocess.run(
                ['redis-cli', 'ping'],
                capture_output=True, timeout=5
            )
            return result.returncode == 0
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def _check_backend_ready(self) -> bool:
        """Check if backend API is ready."""
        try:
            result = subprocess.run(
                ['curl', '-f', 'http://localhost:8000/health'],
                capture_output=True, timeout=10
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False

    def _check_frontend_ready(self) -> bool:
        """Check if frontend is ready."""
        try:
            result = subprocess.run(
                ['curl', '-f', 'http://localhost:3000'],
                capture_output=True, timeout=10
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False

    def run_tests(self) -> bool:
        """Run the test suite."""
        print("🧪 Running tests...")

        try:
            result = subprocess.run([
                sys.executable, '-m', 'pytest', 'tests/',
                '-v', '--tb=short'
            ], cwd=self.project_root, check=True)

            print("✅ All tests passed")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Tests failed: {e}")
            return False

    def create_test_data(self) -> None:
        """Create some initial test data in the database."""
        print("📊 Creating test data...")

        # This would create some sample claims, edges, and gaps
        # For now, just show that the database is accessible
        try:
            from src.core.graph_db import KnowledgeGraph
            from src.core.config import config

            with KnowledgeGraph() as kg:
                stats = kg.get_statistics()
                print(f"✅ Database accessible - {stats.get('total_claims', 0)} claims loaded")

        except Exception as e:
            print(f"⚠️  Could not create test data: {e}")

    def show_status(self) -> None:
        """Show the current status of services."""
        print("📋 Service Status:")

        try:
            result = subprocess.run([
                'docker', 'compose', 'ps'
            ], cwd=self.project_root, capture_output=True, text=True)

            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"❌ Could not get service status: {e}")

    def run(self, args) -> None:
        """Main setup flow."""
        print("🚀 Claudipedia Development Setup")
        print("=" * 50)

        # Check requirements
        if not self.check_requirements():
            print("❌ Requirements not met. Please install missing dependencies.")
            sys.exit(1)

        # Setup environment
        self.setup_environment()

        # Start services
        if not args.skip_services:
            self.start_services()
            self.wait_for_services()

        # Run tests
        if not args.skip_tests:
            if not self.run_tests():
                print("⚠️  Tests failed, but continuing setup...")

        # Create test data
        if not args.skip_data:
            self.create_test_data()

        # Show final status
        print("\n" + "=" * 50)
        print("✅ Setup complete!")
        print("\n📚 Useful commands:")
        print("   Start services: docker compose up -d")
        print("   Stop services:  docker compose down")
        print("   View logs:      docker compose logs -f")
        print("   Run tests:      python -m pytest tests/")
        print("   Backend API:    http://localhost:8000")
        print("   Frontend:       http://localhost:3000")
        print("   Neo4j browser:  http://localhost:7474")
        print("   API docs:       http://localhost:8000/docs")
        print("   Redis CLI:      redis-cli")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Set up Claudipedia development environment')
    parser.add_argument('--skip-services', action='store_true',
                       help='Skip starting Docker services')
    parser.add_argument('--skip-tests', action='store_true',
                       help='Skip running tests')
    parser.add_argument('--skip-data', action='store_true',
                       help='Skip creating test data')

    args = parser.parse_args()

    # Determine project root
    script_dir = Path(__file__).parent.parent.parent
    setup = DevSetup(script_dir)
    setup.run(args)


if __name__ == '__main__':
    main()
