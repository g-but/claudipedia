'use client'

import { useState } from 'react'

interface ArticleSection {
  id: string
  title: string
  content: string
  level: number
}

interface ArticleProps {
  title: string
  sections: ArticleSection[]
  lastModified: string
  contributors: string[]
  confidence?: number
  sources?: string[]
}

export default function Article({ title, sections, lastModified, contributors, confidence, sources }: ArticleProps) {
  const [showToc, setShowToc] = useState(false)

  return (
    <div className="max-w-4xl mx-auto px-6 py-8">
      {/* Article Header */}
      <header className="mb-8">
        <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
          {title}
        </h1>

        <div className="flex items-center gap-4 text-sm text-gray-600 dark:text-gray-400 mb-4">
          <span>Last modified: {lastModified}</span>
          <span>•</span>
          <span>{contributors.length} contributor{contributors.length !== 1 ? 's' : ''}</span>
          {confidence && (
            <>
              <span>•</span>
              <span className={`px-2 py-1 rounded text-xs ${
                confidence >= 0.9 ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200' :
                confidence >= 0.7 ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200' :
                'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
              }`}>
                {Math.round(confidence * 100)}% Confidence
              </span>
            </>
          )}
        </div>

        {/* Action Buttons */}
        <div className="flex items-center gap-2 mb-6">
          <button className="px-3 py-2 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700">
            Edit Article
          </button>
          <button className="px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-md hover:bg-gray-50 dark:hover:bg-gray-700">
            View History
          </button>
          <button className="px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-md hover:bg-gray-50 dark:hover:bg-gray-700">
            Discuss
          </button>
        </div>

        {/* Table of Contents Toggle */}
        <button
          onClick={() => setShowToc(!showToc)}
          className="text-sm text-blue-600 dark:text-blue-400 hover:underline"
        >
          {showToc ? 'Hide' : 'Show'} Table of Contents
        </button>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
        {/* Table of Contents */}
        {showToc && (
          <aside className="lg:col-span-1">
            <div className="bg-gray-50 dark:bg-gray-800 rounded-lg p-4 sticky top-24">
              <h3 className="font-semibold text-gray-900 dark:text-white mb-3">Contents</h3>
              <nav className="space-y-2">
                {sections.map((section) => (
                  <a
                    key={section.id}
                    href={`#${section.id}`}
                    className={`block text-sm text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 ${
                      section.level > 1 ? `pl-${section.level * 4}` : ''
                    }`}
                  >
                    {section.title}
                  </a>
                ))}
              </nav>
            </div>
          </aside>
        )}

        {/* Article Content */}
        <article className={`${showToc ? 'lg:col-span-3' : 'lg:col-span-4'}`}>
          {sections.map((section) => (
            <section key={section.id} id={section.id} className="mb-8">
              <h2 className={`font-bold text-gray-900 dark:text-white mb-4 ${
                section.level === 1 ? 'text-2xl border-b border-gray-200 dark:border-gray-700 pb-2' :
                section.level === 2 ? 'text-xl' : 'text-lg'
              }`}>
                {section.title}
              </h2>

              <div
                className="prose prose-gray dark:prose-invert max-w-none"
                dangerouslySetInnerHTML={{ __html: section.content }}
              />
            </section>
          ))}

          {/* References */}
          {sources && sources.length > 0 && (
            <section className="mt-12 pt-8 border-t border-gray-200 dark:border-gray-700">
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4">References</h3>
              <ol className="space-y-2">
                {sources.map((source, index) => (
                  <li key={index} className="text-sm text-gray-600 dark:text-gray-400">
                    {source}
                  </li>
                ))}
              </ol>
            </section>
          )}

          {/* Article Actions */}
          <div className="mt-12 pt-8 border-t border-gray-200 dark:border-gray-700">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <button className="px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-md hover:bg-gray-50 dark:hover:bg-gray-700">
                  ← Previous Article
                </button>
                <button className="px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-md hover:bg-gray-50 dark:hover:bg-gray-700">
                  Next Article →
                </button>
              </div>

              <div className="flex items-center gap-2">
                <button className="px-3 py-2 text-sm bg-green-600 text-white rounded-md hover:bg-green-700">
                  Rate Article
                </button>
                <button className="px-3 py-2 text-sm bg-purple-600 text-white rounded-md hover:bg-purple-700">
                  Suggest Improvements
                </button>
              </div>
            </div>
          </div>
        </article>
      </div>
    </div>
  )
}
