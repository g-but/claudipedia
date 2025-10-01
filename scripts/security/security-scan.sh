#!/bin/bash

# Claudipedia Security Scanning Script
# This script runs comprehensive security checks on the application

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
FRONTEND_DIR="$PROJECT_ROOT/web"
BACKEND_DIR="$PROJECT_ROOT/backend"
SECURITY_REPORT="$PROJECT_ROOT/security-report-$(date +%Y%m%d-%H%M%S).json"

# Exit codes
EXIT_SUCCESS=0
EXIT_WARNING=1
EXIT_ERROR=2

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')] $*${NC}"
}

error() {
    echo -e "${RED}[ERROR] $*${NC}"
}

success() {
    echo -e "${GREEN}[SUCCESS] $*${NC}"
}

warning() {
    echo -e "${YELLOW}[WARNING] $*${NC}"
}

# Initialize security report
init_report() {
    cat > "$SECURITY_REPORT" << EOF
{
  "scan_date": "$(date -Iseconds)",
  "scan_version": "1.0.0",
  "project": "claudipedia",
  "findings": []
}
EOF
}

add_finding() {
    local severity="$1"
    local category="$2"
    local title="$3"
    local description="$4"
    local file="${5:-}"

    # Use jq to add finding to JSON report
    if command -v jq &> /dev/null; then
        jq --arg sev "$severity" \
           --arg cat "$category" \
           --arg title "$title" \
           --arg desc "$description" \
           --arg file "$file" \
           '.findings += [{"severity": $sev, "category": $cat, "title": $title, "description": $desc, "file": $file}]' \
           "$SECURITY_REPORT" > tmp.json && mv tmp.json "$SECURITY_REPORT"
    fi

    case "$severity" in
        "HIGH"|"CRITICAL")
            error "🔴 $category: $title - $description"
            return $EXIT_ERROR
            ;;
        "MEDIUM")
            warning "🟡 $category: $title - $description"
            return $EXIT_WARNING
            ;;
        "LOW"|"INFO")
            log "🔵 $category: $title - $description"
            return $EXIT_SUCCESS
            ;;
    esac
}

# Check for secrets in code
check_secrets() {
    log "🔍 Scanning for hardcoded secrets..."

    # Check for common secret patterns
    local secret_patterns=(
        "password.*=.*['\"][^'\"]*['\"]"
        "secret.*=.*['\"][^'\"]*['\"]"
        "key.*=.*['\"][^'\"]*['\"]"
        "token.*=.*['\"][^'\"]*['\"]"
        "api_key.*=.*['\"][^'\"]*['\"]"
    )

    for pattern in "${secret_patterns[@]}"; do
        if grep -r -i "$pattern" "$PROJECT_ROOT" --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=venv --exclude-dir=__pycache__ | grep -v ".env.example" | head -5; then
            add_finding "HIGH" "Secrets" "Hardcoded credentials found" "Potential hardcoded secrets detected in codebase" "multiple"
        fi
    done

    success "No hardcoded secrets found"
}

# Check for insecure configurations
check_insecure_configs() {
    log "🔍 Checking for insecure configurations..."

    # Check for debug mode in production
    if grep -r "DEBUG.*=.*True" "$PROJECT_ROOT" --exclude-dir=.git --exclude-dir=node_modules; then
        add_finding "MEDIUM" "Configuration" "Debug mode enabled" "Debug mode should be disabled in production"
    fi

    # Check for exposed error pages
    if grep -r "error.*detail" "$PROJECT_ROOT" --exclude-dir=.git; then
        add_finding "LOW" "Configuration" "Detailed error pages" "Consider disabling detailed error pages in production"
    fi

    success "Configuration security check completed"
}

# Check frontend dependencies for vulnerabilities
check_frontend_deps() {
    log "🔍 Scanning frontend dependencies..."

    cd "$FRONTEND_DIR"

    # Check for outdated packages
    if command -v npm &> /dev/null; then
        log "📦 Checking npm audit..."
        if npm audit --audit-level moderate; then
            success "No moderate or higher vulnerabilities found"
        else
            add_finding "MEDIUM" "Dependencies" "Vulnerable npm packages" "Outdated or vulnerable npm packages detected"
        fi
    fi

    # Check for security headers in Next.js config
    if [[ -f "next.config.js" || -f "next.config.ts" ]]; then
        if ! grep -q "headers" next.config.*; then
            add_finding "LOW" "Configuration" "Missing security headers" "Consider adding security headers in Next.js config"
        fi
    fi
}

# Check backend dependencies for vulnerabilities
check_backend_deps() {
    log "🔍 Scanning backend dependencies..."

    cd "$BACKEND_DIR"

    # Install safety if not available
    if ! command -v safety &> /dev/null; then
        log "📦 Installing safety tool..."
        pip install safety
    fi

    # Run safety check
    if safety check --file requirements.txt; then
        success "No known security vulnerabilities in Python packages"
    else
        add_finding "HIGH" "Dependencies" "Vulnerable Python packages" "Security vulnerabilities found in Python dependencies"
    fi

    # Check for unsafe patterns in Python code
    if grep -r "eval(" "$BACKEND_DIR" --exclude-dir=.git --exclude-dir=venv; then
        add_finding "HIGH" "Code" "Use of eval() function" "eval() can execute arbitrary code and is dangerous"
    fi

    if grep -r "exec(" "$BACKEND_DIR" --exclude-dir=.git --exclude-dir=venv; then
        add_finding "HIGH" "Code" "Use of exec() function" "exec() can execute arbitrary code and is dangerous"
    fi
}

# Check Docker security
check_docker_security() {
    log "🔍 Checking Docker security..."

    # Check if images run as root
    if grep -r "USER root" "$PROJECT_ROOT" --include="Dockerfile*"; then
        add_finding "HIGH" "Docker" "Container running as root" "Containers should not run as root user"
    fi

    # Check for privileged containers
    if grep -r "privileged" "$PROJECT_ROOT/docker-compose*.yml"; then
        add_finding "HIGH" "Docker" "Privileged container" "Avoid using privileged containers"
    fi

    # Check for exposed ports that shouldn't be
    if grep -r "EXPOSE.*22" "$PROJECT_ROOT" --include="Dockerfile*"; then
        add_finding "MEDIUM" "Docker" "SSH port exposed" "Avoid exposing SSH ports in containers"
    fi

    success "Docker security check completed"
}

# Check file permissions
check_file_permissions() {
    log "🔍 Checking file permissions..."

    # Check for world-writable files
    if find "$PROJECT_ROOT" -type f -perm /002 2>/dev/null | head -5; then
        add_finding "MEDIUM" "Permissions" "World-writable files" "Some files are writable by everyone"
    fi

    # Check for .env files that might be committed
    if git ls-files | grep -q "\.env$"; then
        add_finding "HIGH" "Permissions" ".env file in git" ".env files should never be committed to version control"
    fi

    success "File permissions check completed"
}

# Run comprehensive security scan
run_security_scan() {
    local exit_code=$EXIT_SUCCESS

    log "🚀 Starting comprehensive security scan..."

    # Initialize report
    init_report

    # Run all security checks
    check_secrets || exit_code=$(( exit_code | $? ))
    check_insecure_configs || exit_code=$(( exit_code | $? ))
    check_frontend_deps || exit_code=$(( exit_code | $? ))
    check_backend_deps || exit_code=$(( exit_code | $? ))
    check_docker_security || exit_code=$(( exit_code | $? ))
    check_file_permissions || exit_code=$(( exit_code | $? ))

    # Final report
    log "📊 Security scan completed"
    log "📄 Report saved to: $SECURITY_REPORT"

    if [[ $exit_code -eq $EXIT_ERROR ]]; then
        error "❌ Security scan found critical issues that need immediate attention"
        return $EXIT_ERROR
    elif [[ $exit_code -eq $EXIT_WARNING ]]; then
        warning "⚠️ Security scan found some issues that should be addressed"
        return $EXIT_WARNING
    else
        success "✅ Security scan passed with no issues found"
        return $EXIT_SUCCESS
    fi
}

# Main function
main() {
    run_security_scan
}

# Run main function
main "$@"
