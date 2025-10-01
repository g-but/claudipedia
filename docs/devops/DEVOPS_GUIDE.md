# Claudipedia DevOps Guide

## Overview

This guide outlines the DevOps best practices implemented for Claudipedia, a full-stack application with Next.js frontend, FastAPI backend, Neo4j database, and Redis cache.

## Architecture

- **Frontend**: Next.js 15 with TypeScript, deployed on Vercel
- **Backend**: FastAPI with Python, containerized with Docker
- **Database**: Neo4j graph database
- **Cache**: Redis for performance optimization
- **CI/CD**: GitHub Actions with automated testing and deployment
- **Hosting**: Vercel for frontend, containerized backend

## Quick Start

### Prerequisites

1. **GitHub Repository**
   - Fork or clone the repository
   - Enable GitHub Actions in repository settings

2. **Vercel Account**
   - Create account at [vercel.com](https://vercel.com)
   - Install Vercel CLI: `npm i -g vercel`

3. **Environment Variables**
   ```bash
   cp .env.example .env
   # Edit .env with your actual values
   ```

### Local Development

```bash
# Start all services with Docker Compose
docker-compose up -d

# Or run individually:
# Backend
cd backend && python main.py

# Frontend
cd web && npm run dev

# Database (Neo4j Browser)
# Access at http://localhost:7474
```

## CI/CD Pipeline

### GitHub Actions Workflows

The project includes comprehensive CI/CD workflows:

#### `ci-cd.yml`
- **Frontend Testing**: ESLint, TypeScript checks, build verification
- **Backend Testing**: pytest, code formatting, type checking
- **Security Scanning**: npm audit, Python safety checks
- **Deployment**: Automated deployment to Vercel (production/preview)

#### Workflow Triggers
- Push to `main` → Production deployment
- Push to `develop` → Preview deployment
- Pull requests → Run tests without deployment

### Manual Deployment

```bash
# Deploy to production
./scripts/deployment/deploy.sh

# Deploy to preview
./scripts/deployment/deploy.sh --preview
```

## Environment Variables

### Required Variables

| Variable | Description | Required For |
|----------|-------------|--------------|
| `NEO4J_URI` | Neo4j database connection URI | Backend |
| `NEO4J_USER` | Neo4j database username | Backend |
| `NEO4J_PASSWORD` | Neo4j database password | Backend |
| `ANTHROPIC_API_KEY` | Anthropic Claude API key | Backend |
| `JWT_SECRET` | JWT token secret (min 32 chars) | Backend |
| `NEXT_PUBLIC_SUPABASE_URL` | Supabase project URL | Frontend |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Supabase anonymous key | Frontend |
| `VERCEL_TOKEN` | Vercel API token | CI/CD |

### Secrets Management

#### GitHub Repository Secrets

Add these secrets to your GitHub repository (Settings → Secrets and variables → Actions):

```
VERCEL_TOKEN=<your-vercel-token>
NEXT_PUBLIC_SUPABASE_URL=<your-supabase-url>
NEXT_PUBLIC_SUPABASE_ANON_KEY=<your-supabase-anon-key>
```

#### Vercel Environment Variables

In your Vercel project dashboard, add these environment variables:

1. Go to your project dashboard
2. Navigate to Settings → Environment Variables
3. Add the variables for each environment (Production, Preview, Development)

#### Local Environment

```bash
# Copy template
cp .env.example .env

# Edit with your values
nano .env
```

**Security Note**: Never commit `.env` files to version control. The `.gitignore` already excludes them.

## Testing Strategy

### Automated Testing

#### Frontend Tests
```bash
cd web
npm run lint        # ESLint checks
npx tsc --noEmit    # TypeScript compilation check
npm run build       # Build verification
```

#### Backend Tests
```bash
cd backend
python test_backend.py    # Run all tests
pytest -v                 # Verbose test output
pytest --cov=.           # Coverage report
```

#### Manual Testing Checklist
- [ ] User registration/login flows
- [ ] Article creation and editing
- [ ] Search functionality
- [ ] Database connections
- [ ] API endpoints respond correctly
- [ ] Mobile responsiveness
- [ ] Error handling

### Code Quality

#### Linting and Formatting
```bash
# Frontend
cd web && npm run lint

# Backend
cd backend && python test_backend.py  # Includes linting
```

#### Type Checking
```bash
# Frontend
cd web && npx tsc --noEmit

# Backend (if using mypy)
cd backend && python -m mypy .
```

## Deployment Strategy

### Vercel Deployment

#### Automatic Deployment
- Pushes to `main` branch → Production deployment
- Pushes to `develop` branch → Preview deployment
- All deployments include health checks

#### Manual Deployment
```bash
# Production
./scripts/deployment/deploy.sh

# Preview
./scripts/deployment/deploy.sh --preview
```

### Docker Deployment (Alternative)

For self-hosted deployment:

```bash
# Build and start all services
docker-compose up -d --build

# Or build individually
docker build -t claudipedia-backend ./backend
docker build -t claudipedia-frontend ./web
```

## Monitoring and Observability

### Health Checks

#### Application Health
- Backend: `GET /health` endpoint
- Database: Neo4j health checks
- Frontend: Vercel health monitoring

#### Docker Health Checks
All containers include health checks:
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 30s
```

### Logging

#### Application Logs
- Backend: Structured logging with `structlog`
- Frontend: Browser console + Vercel function logs
- Docker: Centralized logging with volume mounts

#### Log Locations
- Application logs: `./logs/` directory
- Docker logs: `docker-compose logs [service-name]`
- Vercel logs: Vercel dashboard

### Error Monitoring

- Frontend errors: Browser console + error boundaries
- Backend errors: Structured logging + error handlers
- Database errors: Neo4j logs + application error handling

## Security Best Practices

### Secrets Management
- ✅ Environment variables for all secrets
- ✅ GitHub repository secrets for CI/CD
- ✅ Vercel environment variables for deployment
- ✅ No hardcoded credentials in code

### Security Headers
```json
{
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Frame-Options", "value": "DENY" },
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "Referrer-Policy", "value": "strict-origin-when-cross-origin" }
      ]
    }
  ]
}
```

### Dependency Security
- ✅ Automated security scanning in CI/CD
- ✅ Regular dependency updates
- ✅ Vulnerability monitoring with npm audit and safety

### Authentication
- ✅ JWT tokens with secure secrets
- ✅ Password hashing with bcrypt
- ✅ OAuth integration with Supabase

## Backup and Recovery

### Database Backups
```bash
# Create Neo4j backup
docker exec claudipedia-neo4j neo4j-admin backup --backup-dir=/backups

# Restore from backup
docker exec claudipedia-neo4j neo4j-admin restore --from=/backups --force
```

### Application Backups
- Git repository serves as code backup
- Environment configuration backed up separately
- Docker volumes for persistent data

## Performance Optimization

### Caching Strategy
- Redis for application caching
- Next.js built-in caching
- Database query optimization

### Docker Optimization
- Multi-stage builds for smaller images
- Non-root user for security
- Proper resource limits

### Monitoring Performance
- Vercel analytics for frontend performance
- Custom metrics for backend performance
- Database query performance monitoring

## Troubleshooting

### Common Issues

#### Deployment Failures
1. Check Vercel dashboard for error logs
2. Verify environment variables are set correctly
3. Check GitHub Actions logs for CI/CD issues

#### Database Connection Issues
1. Verify Neo4j is running: `docker-compose ps`
2. Check connection credentials in environment
3. Review Neo4j logs: `docker-compose logs neo4j`

#### Build Failures
1. Check Node.js version compatibility
2. Verify all dependencies are installed
3. Review build logs for specific errors

### Getting Help

1. Check the logs: `./logs/` directory
2. Review GitHub Actions logs
3. Check Vercel deployment logs
4. Docker logs: `docker-compose logs`

## Maintenance

### Regular Tasks

#### Weekly
- [ ] Review and update dependencies
- [ ] Check security vulnerability reports
- [ ] Review application logs for errors
- [ ] Test backup and recovery procedures

#### Monthly
- [ ] Performance review and optimization
- [ ] Database maintenance and cleanup
- [ ] Security audit and updates
- [ ] Documentation review and updates

### Update Procedures

#### Dependencies
```bash
# Frontend
cd web && npm update

# Backend
cd backend && pip install -r requirements.txt --upgrade
```

#### Docker Images
```bash
# Pull latest images and rebuild
docker-compose pull
docker-compose up -d --build
```

## Contributing

### Development Workflow
1. Create feature branch from `develop`
2. Make changes with tests
3. Run full test suite locally
4. Submit pull request to `develop`
5. Automated tests run on PR
6. Merge to `main` for production deployment

### Code Standards
- Follow existing code style and conventions
- Write tests for new functionality
- Update documentation for changes
- Use meaningful commit messages

## Emergency Procedures

### Rollback Deployment
```bash
# Using Vercel CLI
vercel rollback --token=$VERCEL_TOKEN

# Or via dashboard
# Go to Vercel dashboard → Deployments → Select previous deployment
```

### Database Recovery
1. Stop application services
2. Restore from backup
3. Verify data integrity
4. Restart services

### Service Recovery
```bash
# Restart all services
docker-compose restart

# Restart specific service
docker-compose restart [service-name]

# View service status
docker-compose ps
```

## Support

For issues and questions:
1. Check this documentation first
2. Review existing issues in GitHub
3. Create new issue with detailed information
4. Include relevant logs and error messages

---

**Last Updated**: $(date '+%Y-%m-%d')
**Version**: 1.0.0
