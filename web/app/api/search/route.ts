import { NextRequest, NextResponse } from 'next/server'

// Mock search results - in real app this would query the Neo4j database
const mockSearchResults = [
  {
    id: 'classical-mechanics',
    title: 'Classical Mechanics',
    summary: 'The branch of physics concerned with the motion of macroscopic objects under the influence of forces.',
    domain: 'Physics',
    confidence: 0.95,
    lastModified: '2024-01-15'
  },
  {
    id: 'quantum-mechanics',
    title: 'Quantum Mechanics',
    summary: 'A fundamental theory in physics that describes the physical properties of nature at the scale of atoms.',
    domain: 'Physics',
    confidence: 0.90,
    lastModified: '2024-01-14'
  },
  {
    id: 'theory-of-relativity',
    title: 'Theory of Relativity',
    summary: 'Einstein\'s theory describing the relationship between space and time, and how gravity affects spacetime.',
    domain: 'Physics',
    confidence: 0.98,
    lastModified: '2024-01-13'
  }
]

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams
  const query = searchParams.get('q')
  const limit = parseInt(searchParams.get('limit') || '10')

  if (!query || query.trim().length === 0) {
    return NextResponse.json({ results: [] })
  }

  // Simple mock search - in real app this would use the KnowledgeGraph
  const results = mockSearchResults
    .filter(article =>
      article.title.toLowerCase().includes(query.toLowerCase()) ||
      article.summary.toLowerCase().includes(query.toLowerCase())
    )
    .slice(0, limit)

  return NextResponse.json({ results })
}
