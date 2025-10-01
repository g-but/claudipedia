# Claudipedia Frontend - Day 1 MVP ✅

**A truth-seeking platform that makes research addictive.**

## 🎉 Day 1 Complete

Beautiful, production-ready landing page with:
- ✨ Prominent "Ask anything" search input
- 🎨 Modern gradient design (purple/blue theme)
- 🌓 Dark mode support
- 📱 Fully responsive
- 🚀 Zero configuration needed - no auth required!

## 🚀 Quick Start

```bash
npm install
npm run dev
```

Visit http://localhost:3000

**That's it!** No database, no auth setup, no environment variables needed.

## 📦 What's Included

- **Landing Page**: Hero section with search input
- **Example Questions**: Click to populate search
- **Feature Pills**: Highlighting key features
- **Status Banner**: Shows current development stage
- **Clean Design**: Glassmorphism effects, smooth transitions

## 🎯 Features

### Current (Day 1)
- Beautiful landing page ✅
- Question input (ready for backend) ✅
- Responsive design ✅
- Dark mode ✅

### Next (Day 2+)
- Connect to backend API
- Generate AI research quests
- Progress tracking
- Evidence viewer

## 🌐 Deploy

### Vercel (Recommended)

```bash
npm install -g vercel
vercel
```

### Other Platforms

Works on any platform that supports Next.js:
- Netlify
- Railway
- Fly.io
- AWS Amplify

## 📂 Structure

```
web/
├── app/
│   ├── page.tsx          # Landing page
│   ├── layout.tsx        # Root layout
│   └── globals.css       # Global styles
├── public/               # Static assets
└── package.json
```

## 🛠 Tech Stack

- **Framework**: Next.js 15 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Runtime**: Turbopack (fast refresh)

## 💡 Next Steps

1. **Backend Integration**: Connect question input to API
2. **Quest Generation**: Implement Claude-powered research quests
3. **User Accounts**: Add auth when needed
4. **Progress System**: Track quest completion

## 📸 What It Looks Like

- **Hero**: "Seek Truth. Unlock Knowledge."
- **Search**: Large, glowing input with "Start Quest ✨" button
- **Examples**: "Why do objects fall?", "How does the internet work?"
- **Status**: "🚧 Currently Building" info box

## 🎨 Design Features

- Gradient backgrounds (purple/blue)
- Glassmorphism (backdrop-blur)
- Smooth hover effects
- Rounded corners (2xl = 16px)
- Shadow depth for elevation

## 🔧 Scripts

```bash
npm run dev        # Start development server
npm run build      # Build for production
npm run start      # Start production server
npm run lint       # Run ESLint
```

---

**Ready to deploy and test TODAY** 🚀
