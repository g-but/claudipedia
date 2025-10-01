'use client'

import { useState } from 'react'
import { useSession } from 'next-auth/react'
import { useRouter } from 'next/navigation'
import WikipediaLayout from '../components/WikipediaLayout'

interface ArticleSection {
  id: string
  title: string
  content: string
  level: number
}

export default function CreateArticle() {
  const { data: session, status } = useSession()
  const router = useRouter()
  const [loading, setLoading] = useState(false)
  const [formData, setFormData] = useState({
    title: '',
    summary: '',
    domain: 'Physics',
    sections: [
      { id: '1', title: 'Introduction', content: '', level: 1 }
    ] as ArticleSection[],
    sources: [''],
    tags: [] as string[]
  })

  // Redirect if not authenticated
  if (status === 'loading') {
    return (
      <WikipediaLayout>
        <div className="max-w-4xl mx-auto px-6 py-8">
          <div className="animate-pulse space-y-4">
            <div className="h-8 bg-gray-200 dark:bg-gray-700 rounded w-1/3"></div>
            <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-1/2"></div>
            <div className="h-32 bg-gray-200 dark:bg-gray-700 rounded"></div>
          </div>
        </div>
      </WikipediaLayout>
    )
  }

  if (!session) {
    router.push('/auth/signin')
    return null
  }

  const handleInputChange = (field: string, value: string | string[]) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }))
  }

  const addSection = () => {
    const newSection: ArticleSection = {
      id: Date.now().toString(),
      title: '',
      content: '',
      level: 1
    }
    setFormData(prev => ({
      ...prev,
      sections: [...prev.sections, newSection]
    }))
  }

  const updateSection = (id: string, field: 'title' | 'content' | 'level', value: string | number) => {
    setFormData(prev => ({
      ...prev,
      sections: prev.sections.map(section =>
        section.id === id ? { ...section, [field]: value } : section
      )
    }))
  }

  const removeSection = (id: string) => {
    if (formData.sections.length > 1) {
      setFormData(prev => ({
        ...prev,
        sections: prev.sections.filter(section => section.id !== id)
      }))
    }
  }

  const addSource = () => {
    setFormData(prev => ({
      ...prev,
      sources: [...prev.sources, '']
    }))
  }

  const updateSource = (index: number, value: string) => {
    setFormData(prev => ({
      ...prev,
      sources: prev.sources.map((source, i) => i === index ? value : source)
    }))
  }

  const removeSource = (index: number) => {
    if (formData.sources.length > 1) {
      setFormData(prev => ({
        ...prev,
        sources: prev.sources.filter((_, i) => i !== index)
      }))
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    try {
      // In a real app, this would submit to the backend
      console.log('Creating article:', formData)

      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 2000))

      // Redirect to the new article
      router.push(`/article/${formData.title.toLowerCase().replace(/\s+/g, '-')}`)
    } catch (error) {
      console.error('Failed to create article:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <WikipediaLayout>
      <div className="max-w-4xl mx-auto px-6 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">Create New Article</h1>
          <p className="text-gray-600 dark:text-gray-400">
            Share your knowledge with the world. All contributions are reviewed by our community and AI systems.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-8">
          {/* Basic Information */}
          <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border border-gray-200 dark:border-gray-700">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">Article Information</h2>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label htmlFor="title" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Article Title
                </label>
                <input
                  type="text"
                  id="title"
                  value={formData.title}
                  onChange={(e) => handleInputChange('title', e.target.value)}
                  className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="e.g., Quantum Mechanics"
                  required
                />
              </div>

              <div>
                <label htmlFor="domain" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Domain/Category
                </label>
                <select
                  id="domain"
                  value={formData.domain}
                  onChange={(e) => handleInputChange('domain', e.target.value)}
                  className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option>Physics</option>
                  <option>Mathematics</option>
                  <option>Chemistry</option>
                  <option>Biology</option>
                  <option>Computer Science</option>
                  <option>Philosophy</option>
                </select>
              </div>
            </div>

            <div className="mt-6">
              <label htmlFor="summary" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Brief Summary
              </label>
              <textarea
                id="summary"
                value={formData.summary}
                onChange={(e) => handleInputChange('summary', e.target.value)}
                rows={3}
                className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Provide a brief overview of what this article covers..."
                required
              />
            </div>
          </div>

          {/* Article Content */}
          <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border border-gray-200 dark:border-gray-700">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold text-gray-900 dark:text-white">Article Content</h2>
              <button
                type="button"
                onClick={addSection}
                className="px-3 py-2 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700"
              >
                Add Section
              </button>
            </div>

            <div className="space-y-6">
              {formData.sections.map((section, index) => (
                <div key={section.id} className="border border-gray-200 dark:border-gray-600 rounded-lg p-4">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="font-medium text-gray-900 dark:text-white">Section {index + 1}</h3>
                    {formData.sections.length > 1 && (
                      <button
                        type="button"
                        onClick={() => removeSection(section.id)}
                        className="text-red-600 hover:text-red-700 text-sm"
                      >
                        Remove
                      </button>
                    )}
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                        Section Title
                      </label>
                      <input
                        type="text"
                        value={section.title}
                        onChange={(e) => updateSection(section.id, 'title', e.target.value)}
                        className="w-full px-3 py-2 rounded border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                        placeholder="Introduction"
                        required
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                        Heading Level
                      </label>
                      <select
                        value={section.level}
                        onChange={(e) => updateSection(section.id, 'level', parseInt(e.target.value))}
                        className="w-full px-3 py-2 rounded border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                      >
                        <option value={1}>H1 (Main Section)</option>
                        <option value={2}>H2 (Subsection)</option>
                        <option value={3}>H3 (Sub-subsection)</option>
                      </select>
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      Content (Markdown supported)
                    </label>
                    <textarea
                      value={section.content}
                      onChange={(e) => updateSection(section.id, 'content', e.target.value)}
                      rows={6}
                      className="w-full px-3 py-2 rounded border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="Write your section content here..."
                      required
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Sources */}
          <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border border-gray-200 dark:border-gray-700">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold text-gray-900 dark:text-white">Sources & References</h2>
              <button
                type="button"
                onClick={addSource}
                className="px-3 py-2 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700"
              >
                Add Source
              </button>
            </div>

            <div className="space-y-4">
              {formData.sources.map((source, index) => (
                <div key={index} className="flex gap-2">
                  <input
                    type="text"
                    value={source}
                    onChange={(e) => updateSource(index, e.target.value)}
                    className="flex-1 px-3 py-2 rounded border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="e.g., Einstein, A. (1905). On the Electrodynamics of Moving Bodies."
                    required
                  />
                  {formData.sources.length > 1 && (
                    <button
                      type="button"
                      onClick={() => removeSource(index)}
                      className="px-3 py-2 text-red-600 hover:text-red-700"
                    >
                      Remove
                    </button>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Submit Actions */}
          <div className="flex items-center justify-between pt-6 border-t border-gray-200 dark:border-gray-700">
            <div className="text-sm text-gray-600 dark:text-gray-400">
              <p>Your article will be reviewed by our community and AI systems before publication.</p>
            </div>

            <div className="flex space-x-3">
              <button
                type="button"
                onClick={() => router.back()}
                className="px-6 py-2 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={loading}
                className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? (
                  <div className="flex items-center">
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
                    Creating...
                  </div>
                ) : (
                  'Create Article'
                )}
              </button>
            </div>
          </div>
        </form>
      </div>
    </WikipediaLayout>
  )
}

