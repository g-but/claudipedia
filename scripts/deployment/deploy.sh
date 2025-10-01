#!/bin/bash

# Claudipedia Production Deployment Script
# This script handles deployment to Vercel and provides deployment verification

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
REQUIRED_ENV_VARS=("VERCEL_TOKEN" "NEXT_PUBLIC_SUPABASE_URL" "NEXT_PUBLIC_SUPABASE_ANON_KEY")
LOG_FILE="$PROJECT_ROOT/deployment.log"

# Logging function
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

# Pre-deployment checks
pre_deployment_checks() {
    log "🔍 Running pre-deployment checks..."

    # Check if we're in the correct directory
    if [[ ! -f "$FRONTEND_DIR/package.json" ]]; then
        error "Frontend package.json not found. Are you in the correct project directory?"
    fi

    # Check environment variables
    for env_var in "${REQUIRED_ENV_VARS[@]}"; do
        if [[ -z "${!env_var:-}" ]]; then
            error "Required environment variable $env_var is not set"
        fi
    done

    # Check if Vercel CLI is installed
    if ! command -v vercel &> /dev/null; then
        log "📦 Installing Vercel CLI..."
        npm install -g vercel
    fi

    # Check if Node.js version is compatible
    NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
    if [[ "$NODE_VERSION" -lt 18 ]]; then
        warning "Node.js version $NODE_VERSION might not be optimal. Consider using Node.js 18+"
    fi

    success "Pre-deployment checks passed"
}

# Install dependencies
install_dependencies() {
    log "📦 Installing frontend dependencies..."
    cd "$FRONTEND_DIR"

    if [[ -f "package-lock.json" ]]; then
        npm ci
    else
        npm install
    fi

    success "Dependencies installed"
}

# Run tests and linting
run_quality_checks() {
    log "🧪 Running quality checks..."

    cd "$FRONTEND_DIR"

    # Run ESLint
    log "🔍 Running ESLint..."
    if ! npm run lint; then
        error "ESLint checks failed"
    fi

    # Run TypeScript check
    log "🔍 Running TypeScript check..."
    if ! npx tsc --noEmit; then
        error "TypeScript checks failed"
    fi

    # Run build test
    log "🔨 Testing build process..."
    if ! npm run build; then
        error "Build test failed"
    fi

    success "Quality checks passed"
}

# Deploy to Vercel
deploy_to_vercel() {
    log "🚀 Deploying to Vercel..."

    cd "$FRONTEND_DIR"

    # Set environment variables for deployment
    export NEXT_PUBLIC_SUPABASE_URL="${NEXT_PUBLIC_SUPABASE_URL}"
    export NEXT_PUBLIC_SUPABASE_ANON_KEY="${NEXT_PUBLIC_SUPABASE_ANON_KEY}"

    # Deploy to production
    if [[ "${1:-}" == "--preview" ]]; then
        log "🌐 Deploying to preview environment..."
        DEPLOYMENT_URL=$(vercel --token="$VERCEL_TOKEN" --scope="$VERCEL_ORG_ID" 2>/dev/null | grep -o 'https://[^ ]*\.vercel\.app')
        success "Preview deployment completed: $DEPLOYMENT_URL"
    else
        log "🌐 Deploying to production..."
        DEPLOYMENT_URL=$(vercel --prod --token="$VERCEL_TOKEN" --scope="$VERCEL_ORG_ID" 2>/dev/null | grep -o 'https://[^ ]*\.vercel\.app')
        success "Production deployment completed: $DEPLOYMENT_URL"
    fi

    echo "$DEPLOYMENT_URL" > "$PROJECT_ROOT/.last-deployment-url"
}

# Post-deployment verification
post_deployment_verification() {
    local deployment_url
    deployment_url=$(cat "$PROJECT_ROOT/.last-deployment-url" 2>/dev/null || echo "")

    if [[ -z "$deployment_url" ]]; then
        warning "No deployment URL found for verification"
        return
    fi

    log "🔍 Verifying deployment at $deployment_url..."

    # Wait for deployment to be ready
    sleep 10

    # Check if site is accessible
    if curl -f -s "$deployment_url" > /dev/null; then
        success "Deployment verification successful"
    else
        warning "Deployment verification failed - site may not be accessible yet"
    fi
}

# Health check for deployed site
health_check() {
    local deployment_url="$1"

    if [[ -z "$deployment_url" ]]; then
        warning "No deployment URL provided for health check"
        return
    fi

    log "🏥 Running health check for $deployment_url..."

    # Check main page
    if curl -f -s "$deployment_url" | grep -q "Claudipedia"; then
        success "Health check passed - site is responding correctly"
    else
        warning "Health check warning - site may not be fully loaded"
    fi
}

# Rollback function (if needed)
rollback() {
    local deployment_url="$1"

    if [[ -z "$deployment_url" ]]; then
        error "No deployment URL provided for rollback"
    fi

    log "🔄 Rolling back deployment..."

    cd "$FRONTEND_DIR"

    # This would need to be customized based on your rollback strategy
    # For now, just log the rollback
    warning "Rollback functionality needs to be implemented based on your backup strategy"

    # Example rollback command (uncomment and customize):
    # vercel rollback --token="$VERCEL_TOKEN" --scope="$VERCEL_ORG_ID"
}

# Main deployment function
main() {
    local preview=false

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --preview)
                preview=true
                shift
                ;;
            --help)
                echo "Usage: $0 [--preview] [--help]"
                echo ""
                echo "Options:"
                echo "  --preview    Deploy to preview environment instead of production"
                echo "  --help       Show this help message"
                exit 0
                ;;
            *)
                error "Unknown option: $1"
                ;;
        esac
    done

    log "🚀 Starting Claudipedia deployment process..."

    # Run deployment steps
    pre_deployment_checks
    install_dependencies
    run_quality_checks

    if [[ "$preview" == "true" ]]; then
        deploy_to_vercel "--preview"
    else
        deploy_to_vercel
    fi

    # Get the deployment URL for verification
    DEPLOYMENT_URL=$(cat "$PROJECT_ROOT/.last-deployment-url" 2>/dev/null || echo "")

    post_deployment_verification
    health_check "$DEPLOYMENT_URL"

    success "🎉 Deployment completed successfully!"
    log "🌐 Deployment URL: $DEPLOYMENT_URL"

    # Instructions for next steps
    echo ""
    echo -e "${GREEN}Next steps:${NC}"
    echo "1. Verify the deployment at: $DEPLOYMENT_URL"
    echo "2. Check Vercel dashboard for deployment status"
    echo "3. Update any external services with the new URL if needed"
    echo "4. Monitor logs for any issues"
}

# Run main function with all arguments
main "$@"
