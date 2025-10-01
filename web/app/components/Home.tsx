'use client'

import Link from 'next/link'
import { useState, useEffect } from 'react'

interface FeaturedArticle {
  id: string
  title: string
  summary: string
  domain: string
  lastModified: string
  confidence: number
  readTime: string
}

export default function Home() {
  const [featuredArticles, setFeaturedArticles] = useState<FeaturedArticle[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchFeaturedArticles = async () => {
      try {
        const response = await fetch('/api/search?q=physics&limit=4')
        const data = await response.json()
        if (data.results) {
          setFeaturedArticles(data.results.map((article: any) => ({
            id: article.id,
            title: article.title,
            summary: article.summary,
            domain: article.domain,
            lastModified: article.lastModified,
            confidence: article.confidence,
            readTime: "12 min read" // Mock for now
          })))
        }
      } catch (error) {
        console.error('Failed to fetch featured articles:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchFeaturedArticles()
  }, [])

  const recentArticles = [
    { title: "Black Holes", domain: "Astrophysics", modified: "2 hours ago" },
    { title: "Quantum Entanglement", domain: "Quantum Physics", modified: "5 hours ago" },
    { title: "Electromagnetism", domain: "Physics", modified: "1 day ago" },
    { title: "String Theory", domain: "Theoretical Physics", modified: "2 days ago" },
    { title: "Nuclear Fusion", domain: "Nuclear Physics", modified: "3 days ago" }
  ]

  const domains = [
    { name: "Classical Mechanics", articles: 45, color: "bg-blue-500" },
    { name: "Quantum Mechanics", articles: 38, color: "bg-blue-600" },
    { name: "Relativity", articles: 32, color: "bg-green-500" },
    { name: "Thermodynamics", articles: 28, color: "bg-orange-500" },
    { name: "Electromagnetism", articles: 41, color: "bg-red-500" },
    { name: "Statistical Mechanics", articles: 24, color: "bg-indigo-500" }
  ]

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="bg-gray-50 dark:bg-gray-900 py-20">
        <div className="max-w-6xl mx-auto px-6 text-center">
          <h1 className="text-5xl font-bold text-gray-900 dark:text-white mb-6">
            Welcome to <span className="text-blue-600 dark:text-blue-400">Claudipedia</span>
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-300 mb-8 max-w-3xl mx-auto">
            The AI-powered encyclopedia where humans and machines collaborate to build comprehensive, reliable knowledge across all domains of physics.
          </p>

          {/* Search Bar */}
          <div className="max-w-2xl mx-auto">
            <div className="relative">
              <input
                type="text"
                placeholder="Search for articles, concepts, or questions..."
                className="w-full px-6 py-4 text-lg rounded-xl border-2 border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder-gray-400 focus:outline-none focus:border-blue-500 dark:focus:border-blue-400"
              />
              <button className="absolute right-3 top-1/2 -translate-y-1/2 px-6 py-3 rounded-lg bg-blue-600 text-white font-medium hover:bg-blue-700 transition-colors">
                Search
              </button>
            </div>
          </div>
        </div>
      </section>

      <div className="max-w-6xl mx-auto px-6 py-12">
        {/* Featured Articles */}
        <section className="mb-16">
          <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-8">Featured Articles</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {loading ? (
              // Loading skeleton
              Array.from({ length: 4 }).map((_, index) => (
                <div key={index} className="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6 border border-gray-200 dark:border-gray-700 animate-pulse">
                  <div className="flex items-center justify-between mb-4">
                    <div className="h-6 bg-gray-200 dark:bg-gray-700 rounded w-20"></div>
                    <div className="h-6 bg-gray-200 dark:bg-gray-700 rounded w-16"></div>
                  </div>
                  <div className="h-6 bg-gray-200 dark:bg-gray-700 rounded mb-3 w-3/4"></div>
                  <div className="space-y-2 mb-4">
                    <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded"></div>
                    <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-5/6"></div>
                  </div>
                  <div className="flex justify-between">
                    <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-16"></div>
                    <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-20"></div>
                  </div>
                </div>
              ))
            ) : (
              featuredArticles.map((article, index) => (
              <article key={index} className="bg-white dark:bg-gray-800 rounded-xl shadow-sm hover:shadow-md transition-shadow p-6 border border-gray-200 dark:border-gray-700">
                <div className="flex items-center justify-between mb-4">
                  <span className="px-3 py-1 text-xs font-medium bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 rounded-full">
                    {article.domain}
                  </span>
                  <span className={`px-2 py-1 text-xs rounded ${
                    article.confidence >= 0.9 ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200' :
                    'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200'
                  }`}>
                    {Math.round(article.confidence * 100)}% Confidence
                  </span>
                </div>

                <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3">
                  <Link href={`/article/${article.id}`} className="hover:text-blue-600 dark:hover:text-blue-400">
                    {article.title}
                  </Link>
                </h3>

                <p className="text-gray-600 dark:text-gray-400 mb-4 line-clamp-3">
                  {article.summary}
                </p>

                <div className="flex items-center justify-between text-sm text-gray-500 dark:text-gray-400">
                  <span>{article.readTime}</span>
                  <span>Modified: {article.lastModified}</span>
                </div>
              </article>
              ))
            )}
          </div>
        </section>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Recent Articles */}
          <section className="lg:col-span-2">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">Recent Articles</h2>
            <div className="space-y-4">
              {recentArticles.map((article, index) => (
                <div key={index} className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-800 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors">
                  <div>
                    <h3 className="font-medium text-gray-900 dark:text-white">
                      <Link href={`/article/${article.title.toLowerCase().replace(/\s+/g, '-')}`} className="hover:text-purple-600 dark:hover:text-purple-400">
                        {article.title}
                      </Link>
                    </h3>
                    <p className="text-sm text-gray-500 dark:text-gray-400">{article.domain}</p>
                  </div>
                  <span className="text-sm text-gray-400">{article.modified}</span>
                </div>
              ))}
            </div>
          </section>

          {/* Physics Domains */}
          <section>
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">Physics Domains</h2>
            <div className="space-y-3">
              {domains.map((domain, index) => (
                <Link
                  key={index}
                  href={`/domain/${domain.name.toLowerCase().replace(/\s+/g, '-')}`}
                  className="block p-4 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 hover:border-purple-300 dark:hover:border-purple-600 transition-colors"
                >
                  <div className="flex items-center justify-between mb-2">
                    <h3 className="font-medium text-gray-900 dark:text-white">{domain.name}</h3>
                    <span className={`w-3 h-3 rounded-full ${domain.color}`}></span>
                  </div>
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    {domain.articles} articles
                  </p>
                </Link>
              ))}
            </div>
          </section>
        </div>

        {/* Stats Section */}
        <section className="mt-16 py-12 bg-gray-50 dark:bg-gray-800 rounded-2xl">
          <div className="text-center">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-8">Claudipedia Statistics</h2>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
              <div>
                <div className="text-3xl font-bold text-purple-600 mb-2">127</div>
                <div className="text-sm text-gray-600 dark:text-gray-400">Articles</div>
              </div>
              <div>
                <div className="text-3xl font-bold text-blue-600 mb-2">8</div>
                <div className="text-sm text-gray-600 dark:text-gray-400">Physics Domains</div>
              </div>
              <div>
                <div className="text-3xl font-bold text-green-600 mb-2">94%</div>
                <div className="text-sm text-gray-600 dark:text-gray-400">Avg Confidence</div>
              </div>
              <div>
                <div className="text-3xl font-bold text-orange-600 mb-2">156</div>
                <div className="text-sm text-gray-600 dark:text-gray-400">Contributors</div>
              </div>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="mt-16 text-center">
          <div className="bg-blue-600 rounded-2xl p-12 text-white">
            <h2 className="text-3xl font-bold mb-4">Help Build the Future of Knowledge</h2>
            <p className="text-lg mb-8 opacity-90">
              Join our community of researchers, students, and AI systems working together to create the most comprehensive and reliable knowledge base.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button className="px-8 py-3 bg-white text-blue-600 font-medium rounded-lg hover:bg-gray-100 transition-colors">
                Create Article
              </button>
              <button className="px-8 py-3 border-2 border-white text-white font-medium rounded-lg hover:bg-white hover:text-blue-600 transition-colors">
                Join Community
              </button>
            </div>
          </div>
        </section>
      </div>
    </div>
  )
}
