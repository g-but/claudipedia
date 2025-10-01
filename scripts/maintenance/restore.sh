#!/bin/bash

# Claudipedia Restore Script
# This script restores the application from a backup

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
BACKUP_DIR="$PROJECT_ROOT/backups"

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')] $*${NC}"
}

error() {
    echo -e "${RED}[ERROR] $*${NC}"
    exit 1
}

success() {
    echo -e "${GREEN}[SUCCESS] $*${NC}"
}

warning() {
    echo -e "${YELLOW}[WARNING] $*${NC}"
}

# Check if Docker is running
check_docker() {
    log "🔍 Checking Docker status..."
    if ! docker info > /dev/null 2>&1; then
        error "Docker is not running. Please start Docker and try again."
    fi
    success "Docker is running"
}

# Validate backup
validate_backup() {
    local backup_name="$1"
    local backup_path="$BACKUP_DIR/$backup_name"

    log "🔍 Validating backup: $backup_name"

    if [[ ! -d "$backup_path" ]]; then
        error "Backup directory not found: $backup_path"
    fi

    if [[ ! -f "$backup_path/backup_metadata.json" ]]; then
        error "Backup metadata not found. This doesn't appear to be a valid backup."
    fi

    success "Backup validation completed"
}

# Stop services
stop_services() {
    log "⏹️ Stopping services..."
    docker-compose -f docker-compose.prod.yml down
    success "Services stopped"
}

# Restore Neo4j database
restore_neo4j() {
    local backup_name="$1"
    local backup_path="$BACKUP_DIR/$backup_name"

    log "💾 Restoring Neo4j database..."

    # Find the Neo4j backup file
    local neo4j_backup=$(find "$backup_path" -name "neo4j_backup_*.tar.gz" | head -1)

    if [[ -z "$neo4j_backup" ]]; then
        warning "No Neo4j backup found. Skipping database restore."
        return
    fi

    # Extract backup
    cd "$backup_path"
    tar -xzf "$(basename "$neo4j_backup")"
    cd - > /dev/null

    # Stop Neo4j service
    docker-compose -f docker-compose.prod.yml stop neo4j

    # Remove existing data
    docker volume rm claudipedia_neo4j_prod_data || true

    # Create new volume and copy data
    docker run --rm \
        -v claudipedia_neo4j_prod_data:/restore \
        -v "$backup_path:/backup" \
        alpine \
        cp -r /backup/neo4j /restore/

    # Start Neo4j
    docker-compose -f docker-compose.prod.yml start neo4j

    # Wait for Neo4j to be ready
    log "⏳ Waiting for Neo4j to start..."
    sleep 30

    success "Neo4j database restored"
}

# Restore Redis data
restore_redis() {
    local backup_name="$1"
    local backup_path="$BACKUP_DIR/$backup_name"

    log "💾 Restoring Redis data..."

    # Find the Redis backup file
    local redis_backup=$(find "$backup_path" -name "redis_dump_*.rdb" | head -1)

    if [[ -z "$redis_backup" ]]; then
        warning "No Redis backup found. Skipping cache restore."
        return
    fi

    # Copy backup file to Redis container
    docker cp "$redis_backup" claudipedia-redis-prod:/data/dump.rdb

    # Restart Redis to load the backup
    docker-compose -f docker-compose.prod.yml restart redis

    success "Redis data restored"
}

# Restore configuration
restore_config() {
    local backup_name="$1"
    local backup_path="$BACKUP_DIR/$backup_name"

    log "💾 Restoring configuration..."

    if [[ -d "$backup_path/config" ]]; then
        # Ask user if they want to restore config files
        read -p "Restore configuration files? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            cp -r "$backup_path/config/"* "$PROJECT_ROOT/" 2>/dev/null || true
            success "Configuration files restored"
        else
            warning "Configuration restore skipped"
        fi
    else
        warning "No configuration backup found"
    fi
}

# Restore logs
restore_logs() {
    local backup_name="$1"
    local backup_path="$BACKUP_DIR/$backup_name"

    log "💾 Restoring application logs..."

    if [[ -d "$backup_path/logs" ]]; then
        # Ask user if they want to restore logs
        read -p "Restore application logs? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            cp -r "$backup_path/logs/"* "$PROJECT_ROOT/logs/" 2>/dev/null || true
            success "Application logs restored"
        else
            warning "Logs restore skipped"
        fi
    else
        warning "No logs backup found"
    fi
}

# Start services
start_services() {
    log "▶️ Starting services..."
    docker-compose -f docker-compose.prod.yml up -d
    success "Services started"
}

# Verify restoration
verify_restoration() {
    log "🔍 Verifying restoration..."

    # Check if services are running
    if docker-compose -f docker-compose.prod.yml ps | grep -q "Up"; then
        success "Services are running"
    else
        warning "Some services may not be running properly"
    fi

    # Check Neo4j health
    if curl -f http://localhost:7474 > /dev/null 2>&1; then
        success "Neo4j is accessible"
    else
        warning "Neo4j may not be fully ready"
    fi

    # Check backend health
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        success "Backend is healthy"
    else
        warning "Backend health check failed"
    fi
}

# Main restore function
main() {
    if [[ $# -ne 1 ]]; then
        echo "Usage: $0 <backup_name>"
        echo ""
        echo "Available backups:"
        ls -la "$BACKUP_DIR" | grep "^d" | awk '{print "  " $9}' | tail -10
        exit 1
    fi

    local backup_name="$1"

    log "🚀 Starting Claudipedia restoration process..."
    warning "This will STOP all services and restore from backup: $backup_name"

    read -p "Are you sure you want to continue? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log "Restoration cancelled"
        exit 0
    fi

    # Run restoration steps
    check_docker
    validate_backup "$backup_name"
    stop_services
    restore_neo4j "$backup_name"
    restore_redis "$backup_name"
    restore_config "$backup_name"
    restore_logs "$backup_name"
    start_services
    verify_restoration

    success "🎉 Restoration completed successfully!"
    log "✅ All services have been restored from backup: $backup_name"

    # Final instructions
    echo ""
    echo -e "${GREEN}Restoration completed!${NC}"
    echo "1. Verify your application is working correctly"
    echo "2. Check logs for any issues: docker-compose logs"
    echo "3. Test key functionality"
    echo "4. Consider running a backup to verify everything works"
}

# Run main function
main "$@"
