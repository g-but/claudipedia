'use client'

import { useState, useEffect } from 'react'
import { useSession } from 'next-auth/react'
import Link from 'next/link'
import UserProfile from './UserProfile'

interface SearchResult {
  id: string
  title: string
  summary: string
  domain: string
  confidence: number
  lastModified: string
}

interface WikipediaLayoutProps {
  children: React.ReactNode
  currentArticle?: string
}

export default function WikipediaLayout({ children, currentArticle }: WikipediaLayoutProps) {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')
  const [searchResults, setSearchResults] = useState<SearchResult[]>([])
  const [showResults, setShowResults] = useState(false)
  const [profileOpen, setProfileOpen] = useState(false)
  const { data: session } = useSession()

  // Search functionality
  useEffect(() => {
    const searchArticles = async () => {
      if (searchQuery.trim().length === 0) {
        setSearchResults([])
        setShowResults(false)
        return
      }

      try {
        const response = await fetch(`/api/search?q=${encodeURIComponent(searchQuery)}`)
        const data = await response.json()
        setSearchResults(data.results || [])
        setShowResults(true)
      } catch (error) {
        console.error('Search failed:', error)
        setSearchResults([])
      }
    }

    const debounceTimer = setTimeout(searchArticles, 300)
    return () => clearTimeout(debounceTimer)
  }, [searchQuery])

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (searchQuery.trim()) {
      // In a real app, this would navigate to search results page
      console.log('Searching for:', searchQuery)
    }
  }

  return (
    <div className="min-h-screen bg-white dark:bg-gray-900">
      {/* Header */}
      <header className="fixed top-0 w-full bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Logo */}
            <div className="flex items-center gap-3">
              <button
                onClick={() => setSidebarOpen(!sidebarOpen)}
                className="p-2 rounded-md hover:bg-gray-100 dark:hover:bg-gray-700"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              </button>
              <Link href="/" className="flex items-center gap-2">
                <div className="text-2xl">📚</div>
                <h1 className="text-xl font-bold text-gray-900 dark:text-white">
                  Claudipedia
                </h1>
              </Link>
            </div>

            {/* Search */}
            <div className="flex-1 max-w-lg mx-8 relative">
              <form onSubmit={handleSearchSubmit}>
                <div className="relative">
                  <input
                    type="text"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    placeholder="Search articles..."
                    className="w-full px-4 py-2 pl-10 pr-20 rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <svg className="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                    </svg>
                  </div>
                  <button
                    type="submit"
                    className="absolute right-2 top-1/2 -translate-y-1/2 px-3 py-1 text-sm bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 rounded hover:bg-gray-200 dark:hover:bg-gray-600"
                  >
                    Search
                  </button>
                </div>
              </form>

              {/* Search Results Dropdown */}
              {showResults && searchResults.length > 0 && (
                <div className="absolute top-full left-0 right-0 mt-1 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-md shadow-lg z-50 max-h-96 overflow-y-auto">
                  {searchResults.map((result) => (
                    <Link
                      key={result.id}
                      href={`/article/${result.id}`}
                      className="block p-3 hover:bg-gray-50 dark:hover:bg-gray-700 border-b border-gray-100 dark:border-gray-700 last:border-b-0"
                      onClick={() => {
                        setShowResults(false)
                        setSearchQuery('')
                      }}
                    >
                      <div className="font-medium text-gray-900 dark:text-white">{result.title}</div>
                      <div className="text-sm text-gray-600 dark:text-gray-400 mt-1 line-clamp-2">
                        {result.summary}
                      </div>
                      <div className="flex items-center justify-between mt-2 text-xs text-gray-500 dark:text-gray-400">
                        <span>{result.domain}</span>
                        <span>{Math.round(result.confidence * 100)}% confidence</span>
                      </div>
                    </Link>
                  ))}
                </div>
              )}
            </div>

            {/* Actions */}
            <div className="flex items-center gap-2">
              {session?.user ? (
                <>
                  <Link
                    href="/create"
                    className="px-3 py-2 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700"
                  >
                    Create Article
                  </Link>
                  <button
                    onClick={() => setProfileOpen(!profileOpen)}
                    className="flex items-center gap-2 px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-md hover:bg-gray-50 dark:hover:bg-gray-700"
                  >
                    <div className="w-6 h-6 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-white text-xs font-bold">
                      {session.user.name?.charAt(0).toUpperCase() || 'U'}
                    </div>
                    <span className="hidden sm:inline">{session.user.name}</span>
                  </button>
                </>
              ) : (
                <>
                  <Link
                    href="/auth/signin"
                    className="px-3 py-2 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700"
                  >
                    Sign In
                  </Link>
                  <Link
                    href="/auth/signup"
                    className="px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-md hover:bg-gray-50 dark:hover:bg-gray-700"
                  >
                    Sign Up
                  </Link>
                </>
              )}
            </div>
          </div>
        </div>
      </header>

      <div className="flex pt-16">
        {/* Sidebar */}
        <aside className={`fixed inset-y-0 left-0 pt-16 w-64 bg-gray-50 dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 transform transition-transform duration-300 ease-in-out z-40 ${
          sidebarOpen ? 'translate-x-0' : '-translate-x-full'
        }`}>
          <div className="p-4">
            <nav className="space-y-2">
              <Link
                href="/"
                className="block px-3 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-md"
              >
                🏠 Home
              </Link>

              <div className="pt-4">
                <h3 className="px-3 text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Physics Domains
                </h3>
                <div className="mt-2 space-y-1">
                  {[
                    'Classical Mechanics',
                    'Quantum Mechanics',
                    'Relativity',
                    'Thermodynamics',
                    'Electromagnetism',
                    'Statistical Mechanics',
                    'Nuclear Physics',
                    'Particle Physics'
                  ].map((domain) => (
                    <Link
                      key={domain}
                      href={`/domain/${domain.toLowerCase().replace(/\s+/g, '-')}`}
                      className="block px-3 py-2 text-sm text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-md"
                    >
                      {domain}
                    </Link>
                  ))}
                </div>
              </div>

              <div className="pt-4">
                <h3 className="px-3 text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Community
                </h3>
                <div className="mt-2 space-y-1">
                  <Link href="/recent-changes" className="block px-3 py-2 text-sm text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-md">
                    Recent Changes
                  </Link>
                  <Link href="/discussions" className="block px-3 py-2 text-sm text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-md">
                    Discussions
                  </Link>
                  <Link href="/help" className="block px-3 py-2 text-sm text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-md">
                    Help
                  </Link>
                </div>
              </div>
            </nav>
          </div>
        </aside>

        {/* Overlay for mobile */}
        {sidebarOpen && (
          <div
            className="fixed inset-0 bg-black bg-opacity-50 z-30"
            onClick={() => setSidebarOpen(false)}
          />
        )}

        {/* Main Content */}
        <main className={`flex-1 transition-all duration-300 ${sidebarOpen ? 'ml-64' : 'ml-0'}`}>
          {children}
        </main>
      </div>

      {/* User Profile Dropdown */}
      <UserProfile isOpen={profileOpen} onClose={() => setProfileOpen(false)} />
    </div>
  )
}
