#!/bin/bash

# Claudipedia Backup Script
# This script creates backups of the database, configuration, and application data

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
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="claudipedia_backup_$DATE"
BACKUP_PATH="$BACKUP_DIR/$BACKUP_NAME"

# Logging
LOG_FILE="$BACKUP_DIR/backup.log"

# Ensure backup directory exists
mkdir -p "$BACKUP_DIR"

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')] $*${NC}" | tee -a "$LOG_FILE"
}

error() {
    echo -e "${RED}[ERROR] $*${NC}" | tee -a "$LOG_FILE"
    exit 1
}

success() {
    echo -e "${GREEN}[SUCCESS] $*${NC}" | tee -a "$LOG_FILE"
}

warning() {
    echo -e "${YELLOW}[WARNING] $*${NC}" | tee -a "$LOG_FILE"
}

# Check if Docker is running
check_docker() {
    log "🔍 Checking Docker status..."
    if ! docker info > /dev/null 2>&1; then
        error "Docker is not running. Please start Docker and try again."
    fi
    success "Docker is running"
}

# Backup Neo4j database
backup_neo4j() {
    log "💾 Backing up Neo4j database..."

    # Create temporary container for backup
    docker run --rm \
        -v claudipedia_neo4j_prod_data:/data \
        -v "$BACKUP_PATH:/backup" \
        -w /backup \
        neo4j:5.12-enterprise \
        neo4j-admin database dump --verbose neo4j --to-path=/backup

    # Compress the backup
    cd "$BACKUP_PATH"
    tar -czf "neo4j_backup_$DATE.tar.gz" neo4j/
    rm -rf neo4j/
    cd - > /dev/null

    success "Neo4j backup completed"
}

# Backup Redis data
backup_redis() {
    log "💾 Backing up Redis data..."

    # Use redis-cli to create RDB backup
    docker exec claudipedia-redis-prod redis-cli SAVE

    # Copy the RDB file
    docker cp claudipedia-redis-prod:/data/dump.rdb "$BACKUP_PATH/redis_dump_$DATE.rdb"

    success "Redis backup completed"
}

# Backup configuration files
backup_config() {
    log "💾 Backing up configuration files..."

    # Create config backup directory
    mkdir -p "$BACKUP_PATH/config"

    # Copy relevant configuration files
    cp "$PROJECT_ROOT/docker-compose.prod.yml" "$BACKUP_PATH/config/" 2>/dev/null || true
    cp "$PROJECT_ROOT/docker/neo4j.prod.conf" "$BACKUP_PATH/config/" 2>/dev/null || true
    cp "$PROJECT_ROOT/docker/prometheus.yml" "$BACKUP_PATH/config/" 2>/dev/null || true

    # Copy environment template (without secrets)
    cp "$PROJECT_ROOT/.env.example" "$BACKUP_PATH/config/" 2>/dev/null || true

    success "Configuration backup completed"
}

# Backup application logs
backup_logs() {
    log "💾 Backing up application logs..."

    mkdir -p "$BACKUP_PATH/logs"

    # Copy recent logs
    cp -r "$PROJECT_ROOT/logs/" "$BACKUP_PATH/logs/" 2>/dev/null || true

    success "Logs backup completed"
}

# Create backup metadata
create_metadata() {
    log "📋 Creating backup metadata..."

    cat > "$BACKUP_PATH/backup_metadata.json" << EOF
{
  "backup_name": "$BACKUP_NAME",
  "created_at": "$(date -Iseconds)",
  "backup_type": "full",
  "version": "1.0.0",
  "components": [
    "neo4j_database",
    "redis_cache",
    "configuration",
    "application_logs"
  ],
  "docker_compose_file": "docker-compose.prod.yml",
  "backup_tool_version": "1.0.0",
  "total_size_mb": "$(du -sm "$BACKUP_PATH" | cut -f1)"
}
EOF

    success "Metadata created"
}

# Cleanup old backups
cleanup_old_backups() {
    log "🧹 Cleaning up old backups..."

    # Keep only the last 7 days of backups
    find "$BACKUP_DIR" -name "claudipedia_backup_*" -type d -mtime +7 -exec rm -rf {} \; 2>/dev/null || true

    success "Old backups cleaned up"
}

# Verify backup integrity
verify_backup() {
    log "🔍 Verifying backup integrity..."

    # Check if backup directory exists and has content
    if [[ ! -d "$BACKUP_PATH" ]]; then
        error "Backup directory not found"
    fi

    # Check for required files
    local required_files=("backup_metadata.json")
    for file in "${required_files[@]}"; do
        if [[ ! -f "$BACKUP_PATH/$file" ]]; then
            error "Required backup file missing: $file"
        fi
    done

    # Calculate total size
    local size_mb=$(du -sm "$BACKUP_PATH" | cut -f1)
    log "📊 Backup size: ${size_mb}MB"

    success "Backup verification completed"
}

# Upload to external storage (optional)
upload_backup() {
    # This is a placeholder for cloud storage integration
    # Uncomment and configure based on your cloud provider

    # Example for AWS S3:
    # if command -v aws &> /dev/null; then
    #     log "☁️ Uploading backup to AWS S3..."
    #     aws s3 cp "$BACKUP_PATH" s3://your-bucket/claudipedia-backups/ --recursive
    #     success "Backup uploaded to S3"
    # fi

    # Example for Google Cloud Storage:
    # if command -v gsutil &> /dev/null; then
    #     log "☁️ Uploading backup to Google Cloud Storage..."
    #     gsutil cp -r "$BACKUP_PATH" gs://your-bucket/claudipedia-backups/
    #     success "Backup uploaded to GCS"
    # fi

    log "☁️ External upload not configured (optional)"
}

# Main backup function
main() {
    log "🚀 Starting Claudipedia backup process..."

    # Pre-backup checks
    check_docker

    # Create backup directory
    mkdir -p "$BACKUP_PATH"

    # Run backup steps
    backup_neo4j
    backup_redis
    backup_config
    backup_logs
    create_metadata

    # Post-backup steps
    cleanup_old_backups
    verify_backup
    upload_backup

    success "🎉 Backup completed successfully!"
    log "📁 Backup location: $BACKUP_PATH"
    log "📊 Backup size: $(du -sh "$BACKUP_PATH" | cut -f1)"

    # Instructions
    echo ""
    echo -e "${GREEN}Backup completed!${NC}"
    echo "Location: $BACKUP_PATH"
    echo "To restore, use: ./scripts/maintenance/restore.sh $BACKUP_NAME"
}

# Run main function
main "$@"
