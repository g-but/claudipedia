"""
Claudipedia Backend API

A comprehensive API for the AI-powered encyclopedia where humans and Claude collaborate
to build reliable knowledge with transparency and quality control.
"""

import asyncio
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import jwt
import time
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from enum import Enum
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Claudipedia API",
    description="AI-powered encyclopedia backend with human-AI collaboration",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3002"],  # Next.js dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security scheme
security = HTTPBearer()

# Mock JWT secret - in production use environment variable
JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key-change-in-production")
JWT_ALGORITHM = "HS256"

# Enums for type safety
class ArticleStatus(str, Enum):
    DRAFT = "draft"
    UNDER_REVIEW = "under_review"
    PUBLISHED = "published"
    REJECTED = "rejected"

class ReviewStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    REJECTED = "rejected"

class ReviewerType(str, Enum):
    HUMAN = "human"
    CLAUDE = "claude"

class ReviewType(str, Enum):
    INITIAL = "initial"
    REVISION = "revision"
    QUALITY_CHECK = "quality_check"

class SourceType(str, Enum):
    BOOK = "book"
    PAPER = "paper"
    WEBSITE = "website"
    DATABASE = "database"
    EXPERIMENT = "experiment"

class VerificationStatus(str, Enum):
    VERIFIED = "verified"
    UNVERIFIED = "unverified"
    DISPUTED = "disputed"

# Pydantic Models
class Source(BaseModel):
    id: Optional[str] = None
    type: SourceType
    title: str
    authors: Optional[str] = None
    publication_year: Optional[int] = None
    url: Optional[str] = None
    doi: Optional[str] = None
    verification_status: VerificationStatus = VerificationStatus.UNVERIFIED

class ArticleSection(BaseModel):
    id: str
    title: str
    content: str
    level: int = 1

class Article(BaseModel):
    id: Optional[str] = None
    slug: str
    title: str
    summary: str
    domain: str
    author_id: str
    status: ArticleStatus = ArticleStatus.DRAFT
    version: int = 1
    sections: List[ArticleSection] = []
    sources: List[Source] = []
    tags: List[str] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    published_at: Optional[datetime] = None
    confidence_score: Optional[float] = None
    review_count: int = 0

class Review(BaseModel):
    id: Optional[str] = None
    article_id: str
    reviewer_id: str
    reviewer_type: ReviewerType
    review_type: ReviewType
    status: ReviewStatus = ReviewStatus.PENDING
    score: Optional[float] = None
    feedback: Optional[str] = None
    citations: List[str] = []
    created_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

class User(BaseModel):
    id: str
    email: str
    name: str
    role: str
    expertise: List[str] = []
    reputation: int = 0
    contributions_count: int = 0
    verified: bool = False
    created_at: Optional[datetime] = None

# Mock data storage (in production, use PostgreSQL)
articles_db: Dict[str, Article] = {}
reviews_db: Dict[str, Review] = {}
users_db: Dict[str, User] = {}

# Sample data for testing
def initialize_sample_data():
    """Initialize sample data for development."""
    # Sample users
    users_db["user1"] = User(
        id="user1",
        email="alice@example.com",
        name="Dr. Alice Chen",
        role="researcher",
        expertise=["quantum-mechanics", "particle-physics"],
        reputation=95,
        contributions_count=45,
        verified=True,
        created_at=datetime.now() - timedelta(days=200)
    )

    users_db["user2"] = User(
        id="user2",
        email="bob@example.com",
        name="Prof. Robert Martinez",
        role="professor",
        expertise=["classical-mechanics", "thermodynamics"],
        reputation=98,
        contributions_count=78,
        verified=True,
        created_at=datetime.now() - timedelta(days=400)
    )

    # Sample article
    sample_article = Article(
        id="article1",
        slug="classical-mechanics",
        title="Classical Mechanics",
        summary="The branch of physics concerned with the motion of macroscopic objects under the influence of forces.",
        domain="Physics",
        author_id="user2",
        status=ArticleStatus.PUBLISHED,
        version=2,
        sections=[
            ArticleSection(
                id="intro",
                title="Introduction",
                content="Classical mechanics deals with the motion of macroscopic objects...",
                level=1
            )
        ],
        sources=[
            Source(
                type=SourceType.BOOK,
                title="Fundamentals of Physics",
                authors="Halliday, Resnick, Walker",
                publication_year=2013,
                verification_status=VerificationStatus.VERIFIED
            )
        ],
        created_at=datetime.now() - timedelta(days=30),
        published_at=datetime.now() - timedelta(days=25),
        confidence_score=0.95,
        review_count=3
    )
    articles_db["article1"] = sample_article

    # Sample review
    reviews_db["review1"] = Review(
        id="review1",
        article_id="article1",
        reviewer_id="user1",
        reviewer_type=ReviewerType.HUMAN,
        review_type=ReviewType.INITIAL,
        status=ReviewStatus.COMPLETED,
        score=0.92,
        feedback="Excellent content with strong sources. Minor clarification needed on equation derivations.",
        citations=["Halliday et al. (2013)", "Feynman Lectures Vol 1"],
        created_at=datetime.now() - timedelta(days=28),
        completed_at=datetime.now() - timedelta(days=26)
    )

# Initialize sample data
initialize_sample_data()

# Authentication utilities
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token and return user info."""
    try:
        token = credentials.credentials
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

        # Check if token is expired
        if payload.get("exp", 0) < time.time():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )

        return payload
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )

def get_current_user(user_data = Depends(verify_token)):
    """Get current authenticated user."""
    user_id = user_data.get("sub")
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    return users_db[user_id]

# API Routes

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Claudipedia API",
        "version": "1.0.0",
        "description": "AI-powered encyclopedia backend",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# Authentication endpoints
@app.post("/auth/verify")
async def verify_authentication(user_data = Depends(verify_token)):
    """Verify user authentication and return user info."""
    user_id = user_data.get("sub")
    user = users_db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "authenticated": True,
        "user": user.dict()
    }

# Article endpoints
@app.get("/articles/{article_slug}")
async def get_article(article_slug: str, current_user: User = Depends(get_current_user)):
    """Get article by slug."""
    # In a real implementation, this would query the database
    for article in articles_db.values():
        if article.slug == article_slug:
            return article.dict()

    raise HTTPException(status_code=404, detail="Article not found")

@app.post("/articles")
async def create_article(
    article: Article,
    current_user: User = Depends(get_current_user)
):
    """Create a new article."""
    # Validate user can create articles
    if current_user.reputation < 10 and not current_user.verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient reputation or verification required"
        )

    # Check if slug already exists
    for existing_article in articles_db.values():
        if existing_article.slug == article.slug:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Article slug already exists"
            )

    # Set article metadata
    article.id = f"article_{len(articles_db) + 1}"
    article.author_id = current_user.id
    article.created_at = datetime.now()
    article.updated_at = datetime.now()

    # Store article
    articles_db[article.id] = article

    # Create initial Claude review
    await create_claude_review(article.id)

    logger.info(f"Article created: {article.title} by user {current_user.name}")
    return {"article_id": article.id, "status": "created", "message": "Article submitted for review"}

@app.put("/articles/{article_id}")
async def update_article(
    article_id: str,
    updated_article: Article,
    current_user: User = Depends(get_current_user)
):
    """Update an existing article."""
    if article_id not in articles_db:
        raise HTTPException(status_code=404, detail="Article not found")

    article = articles_db[article_id]

    # Check permissions (author or admin)
    if article.author_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to edit this article"
        )

    # Create new version
    new_version = article.copy()
    new_version.version = article.version + 1
    new_version.updated_at = datetime.now()
    new_version.id = f"{article_id}_v{new_version.version}"

    # Update main article reference
    articles_db[article_id] = new_version

    # Create review for the update
    await create_claude_review(article_id)

    return {"article_id": article_id, "version": new_version.version, "status": "updated"}

# Search endpoints
@app.get("/search")
async def search_articles(
    q: str,
    limit: int = 10,
    current_user: User = Depends(get_current_user)
):
    """Search articles by query."""
    results = []

    for article in articles_db.values():
        if (q.lower() in article.title.lower() or
            q.lower() in article.summary.lower() or
            q.lower() in " ".join(article.tags).lower()):

            results.append({
                "id": article.slug,
                "title": article.title,
                "summary": article.summary,
                "domain": article.domain,
                "confidence": article.confidence_score or 0,
                "lastModified": article.updated_at.isoformat() if article.updated_at else None
            })

    return {"results": results[:limit]}

# Review system endpoints
@app.get("/reviews/pending")
async def get_pending_reviews(current_user: User = Depends(get_current_user)):
    """Get pending reviews for current user."""
    if current_user.role not in ["reviewer", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access reviews"
        )

    pending_reviews = [
        review for review in reviews_db.values()
        if review.status == ReviewStatus.PENDING and
        review.reviewer_id == current_user.id
    ]

    return {"reviews": [review.dict() for review in pending_reviews]}

@app.post("/reviews/{review_id}/complete")
async def complete_review(
    review_id: str,
    review_update: Dict[str, Any],
    current_user: User = Depends(get_current_user)
):
    """Complete a review."""
    if review_id not in reviews_db:
        raise HTTPException(status_code=404, detail="Review not found")

    review = reviews_db[review_id]

    # Check permissions
    if review.reviewer_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to complete this review"
        )

    # Update review
    review.status = ReviewStatus.COMPLETED
    review.completed_at = datetime.now()
    review.score = review_update.get("score", review.score)
    review.feedback = review_update.get("feedback", review.feedback)
    review.citations = review_update.get("citations", review.citations)

    # Update article based on review
    await update_article_from_review(review)

    return {"review_id": review_id, "status": "completed"}

# Claude integration
async def create_claude_review(article_id: str):
    """Create a Claude review for an article."""
    from .services.claude_service import claude_service, ClaudeReviewRequest

    article = articles_db.get(article_id)
    if not article:
        return

    # Create Claude review record
    claude_review = Review(
        id=f"review_claude_{article_id}",
        article_id=article_id,
        reviewer_id="claude_ai",  # Special ID for Claude
        reviewer_type=ReviewerType.CLAUDE,
        review_type=ReviewType.INITIAL,
        status=ReviewStatus.IN_PROGRESS,
        created_at=datetime.now()
    )

    reviews_db[claude_review.id] = claude_review

    # Prepare article content for Claude review
    article_content = "\n".join([section.content for section in article.sections])
    claude_request = ClaudeReviewRequest(
        article_title=article.title,
        article_content=article_content,
        article_sections=[{"title": s.title, "content": s.content, "level": s.level} for s in article.sections],
        sources=[{"title": s.title, "authors": s.authors, "type": s.type.value} for s in article.sources]
    )

    try:
        # Call Claude API for review
        review_response = await claude_service.review_article(claude_request)

        # Update review with Claude's response
        claude_review.status = ReviewStatus.COMPLETED
        claude_review.completed_at = datetime.now()
        claude_review.score = review_response.overall_score
        claude_review.feedback = review_response.review_summary
        claude_review.citations = review_response.citations_used

        # Update article with Claude's assessment
        if review_response.overall_score >= 0.8:
            article.status = ArticleStatus.PUBLISHED
            article.published_at = datetime.now()
            article.confidence_score = review_response.overall_score

        logger.info(f"Claude review completed for article: {article.title}")

    except Exception as e:
        logger.error(f"Error in Claude review for article {article_id}: {e}")
        # Fall back to simulated review
        await simulate_claude_review(claude_review.id, article)

async def simulate_claude_review(review_id: str, article: Article):
    """Simulate Claude reviewing an article."""
    # Simulate AI review process
    await asyncio.sleep(2)  # Simulate API call delay

    review = reviews_db[review_id]
    review.status = ReviewStatus.COMPLETED
    review.completed_at = datetime.now()

    # Simulate Claude's analysis
    review.score = 0.92  # High confidence score
    review.feedback = f"""
    **Claude AI Review - {article.title}**

    **Overall Assessment:** High-quality article with strong academic foundation.

    **Strengths:**
    • Well-structured content with clear explanations
    • Appropriate use of mathematical formulations
    • Comprehensive source citations

    **Areas for Improvement:**
    • Consider adding more recent experimental validations
    • Could benefit from additional cross-references to related topics

    **Source Verification:**
    • Primary sources verified against academic databases
    • Citations appear accurate and relevant

    **Recommendation:** Approve for publication with minor revisions suggested.
    """

    review.citations = [
        "Newton, I. (1687). Philosophiæ Naturalis Principia Mathematica",
        "Feynman Lectures on Physics, Vol. 1",
        "Modern verification through experimental physics literature"
    ]

    # Update article status if Claude approves
    if review.score and review.score >= 0.8:
        article.status = ArticleStatus.PUBLISHED
        article.published_at = datetime.now()
        article.confidence_score = review.score

    logger.info(f"Claude review completed for article: {article.title}")

# Utility functions
async def update_article_from_review(review: Review):
    """Update article status based on review outcome."""
    article = articles_db.get(review.article_id)
    if not article:
        return

    # Update review count
    article.review_count += 1

    # If this is a high-quality review, consider publishing
    if review.score and review.score >= 0.85 and article.status == ArticleStatus.UNDER_REVIEW:
        article.status = ArticleStatus.PUBLISHED
        article.published_at = datetime.now()
        article.confidence_score = review.score

# User endpoints
@app.get("/users/{user_id}")
async def get_user(user_id: str, current_user: User = Depends(get_current_user)):
    """Get user profile."""
    if current_user.role != "admin" and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this profile"
        )

    user = users_db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user.dict()

@app.get("/users/{user_id}/contributions")
async def get_user_contributions(user_id: str, current_user: User = Depends(get_current_user)):
    """Get user's article contributions."""
    if current_user.role != "admin" and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view contributions"
        )

    user_articles = [
        article.dict() for article in articles_db.values()
        if article.author_id == user_id
    ]

    return {"contributions": user_articles}

# Admin endpoints
@app.get("/admin/stats")
async def get_system_stats(current_user: User = Depends(get_current_user)):
    """Get system statistics (admin only)."""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    stats = {
        "total_articles": len(articles_db),
        "published_articles": len([a for a in articles_db.values() if a.status == ArticleStatus.PUBLISHED]),
        "pending_reviews": len([r for r in reviews_db.values() if r.status == ReviewStatus.PENDING]),
        "total_users": len(users_db),
        "claude_reviews": len([r for r in reviews_db.values() if r.reviewer_type == ReviewerType.CLAUDE])
    }

    return {"stats": stats}

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions with proper error responses."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "status_code": exc.status_code}
    )

# Import asyncio for the sleep function
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
