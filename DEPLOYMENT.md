# Claudipedia Deployment Guide

## 🚀 Quick Start

### Automated Deployment (Recommended)

**Option 1: GitHub Integration (Fully Automated)**
1. **Set up GitHub Secrets** in your repository:
   ```bash
   VERCEL_TOKEN=your_vercel_token
   NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
   NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
   NEXT_PUBLIC_SUPABASE_PREVIEW_URL=your_preview_supabase_url  # Optional
   NEXT_PUBLIC_SUPABASE_PREVIEW_ANON_KEY=your_preview_anon_key  # Optional
   ```

2. **Push to main/develop branches** - deployment happens automatically via GitHub Actions

3. **Monitor deployment** in GitHub Actions tab or Vercel dashboard

**Option 2: Manual CLI Deployment**
```bash
# Login to Vercel (one-time setup)
vercel login

# Deploy to production
cd web && vercel --prod

# Deploy preview version
cd web && vercel
```

## 📋 Prerequisites

### Required Accounts
- **Vercel Account**: https://vercel.com (for hosting)
- **Supabase Account**: https://supabase.com (for database & auth)
- **GitHub Account**: https://github.com (for version control & CI/CD)

### Environment Variables Setup

**For Production (Frontend):**
```bash
NEXT_PUBLIC_API_URL=https://your-backend-api.com  # Backend API URL
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co  # Optional: for auth
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
```

**For Production (Backend):**
```bash
NEO4J_URI=bolt://your-neo4j-instance:7687
NEO4J_USER=your_neo4j_user
NEO4J_PASSWORD=your_neo4j_password
ANTHROPIC_API_KEY=your_claude_api_key
JWT_SECRET=your_jwt_secret
```

**For Preview (Optional):**
```bash
NEXT_PUBLIC_SUPABASE_PREVIEW_URL=https://your-preview-project.supabase.co
NEXT_PUBLIC_SUPABASE_PREVIEW_ANON_KEY=your-preview-anon-key
```

## 🏗️ Architecture Overview

Claudipedia uses a modern decoupled architecture with independent services:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Vercel        │    │   Docker        │    │   GitHub        │
│   (Frontend)    │◄──►│   (Backend)     │    │   (CI/CD)       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │               ┌─────────────────┐       │
         │               │   Neo4j         │       │
         │               │   (Database)    │       │
         │               └─────────────────┘       │
         └───────────────────────────────────────────┘
                                 │
                        ┌─────────────────┐
                        │   Local Dev     │
                        │   Environment   │
                        └─────────────────┘
```

**Key Features:**
- **Decoupled Services**: Frontend and backend can run independently
- **Graceful Degradation**: Frontend works with or without backend
- **Multiple Deployment Options**: Choose what works best for your needs
- **Offline Mode**: Frontend provides mock data when backend is unavailable

## 🔧 Detailed Setup Instructions

### 1. Environment Configuration

**Create environment files:**
```bash
# In web directory
cd web
cp .env.example .env.local
```

**Configure Supabase:**
1. Create a project at https://supabase.com
2. Enable Google OAuth in Authentication > Providers
3. Enable Email (Magic Link) in Authentication > Providers
4. Copy your project URL and anon key to environment variables

### 2. Local Development

**Option A: Full Stack (Frontend + Backend)**
```bash
# Backend (in one terminal)
cd backend && python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Frontend (in another terminal)
cd web && npm install && npm run dev
# Frontend will be at http://localhost:3000
# Backend API will be at http://localhost:8000
```

**Option B: Frontend Only (with mock data)**
```bash
# Frontend with mock data fallback
cd web && npm install && NEXT_PUBLIC_USE_MOCK_DATA=true npm run dev
# Visit http://localhost:3000
```

**Option C: Backend Only**
```bash
# Backend only (for API testing)
cd backend && python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
# API docs at http://localhost:8000/docs
```

### 3. GitHub Integration (CI/CD)

The project includes a comprehensive GitHub Actions workflow (`.github/workflows/ci-cd.yml`) that:

- **Runs tests** on every push/PR
- **Deploys to Vercel** automatically on main/develop branches
- **Runs security scans** before deployment
- **Supports preview deployments** for develop branch

**Required GitHub Secrets:**
- `VERCEL_TOKEN`: Your Vercel access token
- `NEXT_PUBLIC_SUPABASE_URL`: Production Supabase URL
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`: Production Supabase anon key
- `NEXT_PUBLIC_SUPABASE_PREVIEW_URL`: Preview Supabase URL (optional)
- `NEXT_PUBLIC_SUPABASE_PREVIEW_ANON_KEY`: Preview Supabase anon key (optional)

### 4. Vercel Configuration

The `vercel.json` file includes:
- **Build settings** for Next.js
- **Security headers** (CSP, X-Frame-Options, etc.)
- **API route configuration**
- **Environment variable handling**

## 🚀 Deployment Commands

### Production Deployment
```bash
cd web
vercel --prod
```

### Preview Deployment
```bash
cd web
vercel
```

### Using the Deployment Script
```bash
# Make script executable
chmod +x scripts/deployment/deploy.sh

# Deploy to production
./scripts/deployment/deploy.sh

# Deploy to preview
./scripts/deployment/deploy.sh --preview
```

## 🔒 Security & Best Practices

### Environment Variables
- **Never commit** `.env` files to version control
- **Use different** Supabase projects for production/preview
- **Rotate tokens** regularly

### Supabase Configuration
1. **Authentication Providers**: Enable Google OAuth + Email
2. **Redirect URLs**: Add your Vercel domain(s)
3. **CORS Settings**: Configure for your domains
4. **RLS Policies**: Enable Row Level Security

### Vercel Security Headers
- X-Frame-Options: DENY
- X-Content-Type-Options: nosniff
- Referrer-Policy: strict-origin-when-cross-origin

## 📊 Monitoring & Logs

### Vercel Dashboard
- **Deployment status** and logs
- **Function logs** for API routes
- **Performance metrics**
- **Error tracking**

### Supabase Dashboard
- **Database logs**
- **Authentication events**
- **Storage analytics**

### GitHub Actions
- **Build logs** in Actions tab
- **Test results**
- **Security scan reports**

## 🛠️ Troubleshooting

### Common Issues

**Build Failures:**
```bash
# Clear cache and rebuild
cd web && rm -rf .next && npm run build
```

**Environment Variable Issues:**
```bash
# Check if variables are set
vercel env ls

# Pull latest environment
vercel env pull
```

**Permission Issues:**
```bash
# Ensure proper file permissions
chmod +x scripts/deployment/deploy.sh
```

### Getting Help

1. **Check Vercel logs** in dashboard
2. **Review GitHub Actions** logs
3. **Test locally** first
4. **Check environment variables** are correctly set

## 📚 Additional Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Supabase Documentation](https://supabase.com/docs)
- [Next.js Deployment Guide](https://nextjs.org/docs/deployment)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

## 🎯 Features Implemented

### ✅ Core Features
- Clean, modern landing page with "Ask anything" input
- Google OAuth & Email magic link authentication
- User profile page with statistics
- Responsive design (mobile + desktop)
- Dark mode support
- **NEW: Research Profile System** for truth-seeking and knowledge exploration

### ✅ Research & Knowledge Management
- **Research Profiles**: Create organized profiles for different research areas
- **Context Upload**: Upload research papers, books, experimental data, and other sources
- **Research Sessions**: Track research sessions with findings and confidence levels
- **Context Types**: Support for various content types (papers, books, data, notes, etc.)
- **Search & Discovery**: Find relevant contexts across all profiles

### ✅ DevOps & Deployment
- **Decoupled Architecture**: Frontend and backend can deploy independently
- **Graceful Degradation**: Frontend works with or without backend connectivity
- **Multiple Deployment Options**: Docker for backend, Vercel for frontend
- **Offline Mode**: Frontend provides mock data when backend is unavailable
- **Environment Management**: Separate configs for frontend/backend
- **API Documentation**: Interactive API docs at `/docs` endpoint

## 🔮 Next Steps

### Immediate (Ready to Deploy)
- [x] **COMPLETED**: Decoupled architecture with independent frontend/backend
- [x] **COMPLETED**: Research profile system with context management
- [x] **COMPLETED**: Graceful degradation and offline mode
- [ ] Deploy backend to production environment
- [ ] Set up production Neo4j database
- [ ] Configure production environment variables

### Future Enhancements
- [ ] Advanced quest generation system with AI-powered research paths
- [ ] Evidence viewer component for exploring knowledge relationships
- [ ] Social features (comments, sharing, collaboration)
- [ ] Gamification (points, badges, achievements)
- [ ] Real-time collaboration features
- [ ] Advanced search and filtering across all contexts
- [ ] Integration with external knowledge sources (arXiv, PubMed, etc.)
- [ ] Mobile app development
- [ ] Advanced analytics and insights dashboard
