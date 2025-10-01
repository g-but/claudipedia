# Claudipedia Frontend - Quick Setup

## ✅ What's Built (Day 1 MVP)

### Core Features
- 🎨 Modern, clean landing page with gradient design
- 🔍 Prominent "Ask anything" search input
- 🔐 Google OAuth authentication
- 📧 Email magic link authentication
- 👤 User profile page with stats & badges
- 🌓 Dark mode support
- 📱 Fully responsive (mobile & desktop)
- ⚡ Built with Next.js 14 + Turbopack

### Tech Stack
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Auth**: Supabase Auth (Google + Email)
- **Deployment**: Vercel-ready

## 🚀 Quick Start

### 1. Get Supabase Credentials

**Option A: Use existing Supabase project**
1. Go to your Supabase project dashboard
2. Go to Settings > API
3. Copy your project URL and anon key

**Option B: Create new project (or use free tier)**
1. Go to https://supabase.com
2. Create new project (free tier available)
3. Copy URL and anon key from Settings > API

### 2. Configure Environment

```bash
cd web
cp .env.example .env.local
```

Edit `.env.local`:
```env
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key-here
```

### 3. Configure Supabase Auth Providers

In your Supabase dashboard:

**Email Auth:**
1. Go to Authentication > Providers
2. Enable "Email" provider
3. Enable "Confirm email" (optional)

**Google OAuth:**
1. Go to Authentication > Providers
2. Enable "Google" provider
3. Add redirect URL: `http://localhost:3000/auth/callback`

### 4. Run Locally

```bash
npm install
npm run dev
```

Visit http://localhost:3000

## 🌐 Deploy to Vercel

### Quick Deploy

```bash
npm install -g vercel
vercel
```

### Configure for Production

1. Add environment variables in Vercel dashboard:
   - `NEXT_PUBLIC_SUPABASE_URL`
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY`

2. Update Supabase redirect URLs:
   - Go to Authentication > URL Configuration
   - Add: `https://your-app.vercel.app/auth/callback`

## 📝 Next Steps

### Day 2 Features
- [ ] Connect to backend API (FastAPI)
- [ ] Implement quest generation with Claude
- [ ] Add checkpoint/progress tracking
- [ ] Build evidence viewer component

### Future Enhancements
- [ ] Social features (comments, sharing)
- [ ] Gamification system (XP, levels, badges)
- [ ] Knowledge graph visualization
- [ ] Collaborative quests
- [ ] Mobile app (React Native)

## 🎯 Test Checklist

- [ ] Landing page loads
- [ ] Sign in with Google works
- [ ] Sign in with email works
- [ ] Profile page shows user info
- [ ] Sign out works
- [ ] Dark mode toggles properly
- [ ] Mobile responsive layout works
- [ ] Question input is functional (placeholder alert)

## 🐛 Troubleshooting

**Build fails**: Make sure `.env.local` exists (even with placeholder values)

**Auth not working**: Check Supabase redirect URLs match your domain

**Google OAuth fails**: Verify Google provider is enabled in Supabase

## 📂 Project Structure

```
web/
├── app/
│   ├── page.tsx              # Landing page
│   ├── login/page.tsx        # Login page
│   ├── profile/              # Profile pages
│   └── auth/callback/        # Auth callback
├── lib/
│   └── supabase/             # Supabase client utilities
├── middleware.ts             # Auth middleware
└── .env.local                # Environment variables
```
