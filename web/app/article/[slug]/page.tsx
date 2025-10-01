import { notFound } from 'next/navigation'
import WikipediaLayout from '../../components/WikipediaLayout'
import Article from '../../components/Article'

interface ArticleData {
  title: string
  sections: Array<{
    id: string
    title: string
    content: string
    level: number
  }>
  lastModified: string
  contributors: string[]
  confidence: number
  sources: string[]
}

interface PageProps {
  params: {
    slug: string
  }
}

async function getArticle(slug: string): Promise<ArticleData | null> {
  try {
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3000'}/api/articles/${slug}`, {
      cache: 'no-store' // Always fetch fresh data
    })

    if (!response.ok) {
      return null
    }

    return await response.json()
  } catch (error) {
    console.error('Failed to fetch article:', error)
    return null
  }
}

export default async function ArticlePage({ params }: PageProps) {
  const article = await getArticle(params.slug)

  if (!article) {
    notFound()
  }

  return (
    <WikipediaLayout currentArticle={article.title}>
      <Article
        title={article.title}
        sections={article.sections}
        lastModified={article.lastModified}
        contributors={article.contributors}
        confidence={article.confidence}
        sources={article.sources}
      />
    </WikipediaLayout>
  )
}

export async function generateStaticParams() {
  // For now, return common article slugs
  // In a real app, this would query the database for all articles
  return [
    { slug: 'classical-mechanics' },
    { slug: 'quantum-mechanics' },
    { slug: 'theory-of-relativity' }
  ]
}
