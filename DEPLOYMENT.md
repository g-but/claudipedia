# Claudipedia Frontend Deployment Guide

## Prerequisites

1. **Supabase Project**
   - Create a project at https://supabase.com
   - Enable Google OAuth in Authentication > Providers
   - Enable Email (Magic Link) in Authentication > Providers
   - Copy your project URL and anon key

2. **Vercel Account**
   - Sign up at https://vercel.com
   - Install Vercel CLI: `npm i -g vercel`

## Local Setup

1. **Configure environment variables**
   ```bash
   cd web
   cp .env.example .env.local
   ```

2. **Add your Supabase credentials to `.env.local`**
   ```
   NEXT_PUBLIC_SUPABASE_URL=your_supabase_project_url
   NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
   ```

3. **Install dependencies and run**
   ```bash
   npm install
   npm run dev
   ```

4. **Visit http://localhost:3000**

## Vercel Deployment

### Option 1: Deploy via CLI
```bash
cd web
vercel
```

### Option 2: Deploy via GitHub
1. Push to GitHub
2. Import project on Vercel dashboard
3. Add environment variables in Vercel project settings:
   - `NEXT_PUBLIC_SUPABASE_URL`
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY`

### Post-Deployment: Configure Supabase Redirect URLs

In your Supabase project dashboard:
1. Go to Authentication > URL Configuration
2. Add your Vercel URL to:
   - **Site URL**: `https://your-app.vercel.app`
   - **Redirect URLs**:
     - `https://your-app.vercel.app/auth/callback`
     - `http://localhost:3000/auth/callback` (for local dev)

## Features Implemented (Day 1)

- ✅ Clean, modern landing page
- ✅ Prominent "Ask anything" input field
- ✅ Google OAuth authentication
- ✅ Email magic link authentication
- ✅ User profile page with stats
- ✅ Responsive design (mobile + desktop)
- ✅ Dark mode support
- ✅ Ready for Vercel deployment

## Next Steps (Day 2+)

- [ ] Connect to backend API
- [ ] Implement quest generation
- [ ] Add checkpoint/progress tracking
- [ ] Build evidence viewer
- [ ] Add social features (comments, sharing)
- [ ] Implement gamification (points, badges)
