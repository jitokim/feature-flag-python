"""FastAPI example application using feature-flag-python."""

from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
from typing import Optional, Dict, Any
import os

from feature_flags import (
    initialize_client,
    ais_enabled,
    aget_experiment,
    aget_variant,
    afeature_flag,
    aexperiment_variant,
    cleanup_async_clients,
    ExperimentVariant,
    FeatureFlagError
)

# Initialize FastAPI app
app = FastAPI(
    title="Feature Flags Example API",
    description="Example API demonstrating feature-flag-python usage",
    version="1.0.0"
)


# Mock user authentication
async def get_current_user_id() -> str:
    """Mock function to get current user ID."""
    return "user123"


# Startup and shutdown events
@app.on_event("startup")
async def startup():
    """Initialize feature flag client on startup."""
    # Set default URL if not provided
    if not os.getenv("FEATURE_FLAG_BASE_URL"):
        os.environ["FEATURE_FLAG_BASE_URL"] = "http://localhost:8080"

    initialize_client()
    print("Feature flag client initialized")


@app.on_event("shutdown")
async def shutdown():
    """Cleanup on shutdown."""
    await cleanup_async_clients()
    print("Feature flag client cleaned up")


# Basic feature flag endpoint
@app.get("/api/products/{product_id}")
async def get_product(
        product_id: str,
        user_id: str = Depends(get_current_user_id)
):
    """Get product with feature-flagged enhancements."""
    try:
        # Base product data
        product = {
            "id": product_id,
            "name": f"Product {product_id}",
            "price": 99.99
        }

        # Feature flag: Enhanced product details
        if await ais_enabled("enhanced-product-details", default=False):
            product.update({
                "detailed_description": "Enhanced product description with more details",
                "specifications": {"weight": "1kg", "dimensions": "10x10x10cm"},
                "reviews_summary": {"rating": 4.5, "count": 150}
            })

        # A/B test: Recommendation algorithm
        experiment = await aget_experiment(
            "product-recommendations",
            user_id,
            default_variant=ExperimentVariant.CONTROL
        )

        # Use payload for experiment configuration
        if experiment.variant == ExperimentVariant.TREATMENT:
            # ML-based recommendations
            product["recommendations"] = [
                {"id": "ml-rec-1", "score": 0.95},
                {"id": "ml-rec-2", "score": 0.87}
            ]
            product["recommendation_algorithm"] = experiment.payload["algorithm"] if experiment.payload and "algorithm" in experiment.payload else "ml"
        else:
            # Basic recommendations
            product["recommendations"] = [
                {"id": "basic-rec-1", "score": 0.5},
                {"id": "basic-rec-2", "score": 0.4}
            ]
            product["recommendation_algorithm"] = experiment.payload["algorithm"] if experiment.payload and "algorithm" in experiment.payload else "basic"

        return product

    except FeatureFlagError as e:
        # Feature flag service is down, return basic product
        return {
            "id": product_id,
            "name": f"Product {product_id}",
            "price": 99.99,
            "note": "Basic mode due to feature flag service unavailability"
        }


# Decorator example
@afeature_flag("premium-api", default=False, default_return={"error": "Premium API not available"})
async def premium_analytics(product_id: str) -> Dict[str, Any]:
    """Premium analytics - only available if feature is enabled."""
    return {
        "analytics": {
            "views": 1250,
            "conversion_rate": 0.15,
            "trending_score": 0.87
        },
        "insights": [
            "High conversion rate",
            "Popular among users 25-35"
        ]
    }


@app.get("/api/products/{product_id}/analytics")
async def get_product_analytics(product_id: str):
    """Get product analytics (premium feature)."""
    return await premium_analytics(product_id)


# Experiment decorator example
@aexperiment_variant("pricing-strategy", user_id_key="user_id", default_variant=ExperimentVariant.CONTROL)
async def calculate_pricing(
        base_price: float,
        user_id: str,
        experiment_variant: Optional[ExperimentVariant] = None
) -> Dict[str, Any]:
    """Calculate pricing based on A/B test variant."""
    if experiment_variant == ExperimentVariant.TREATMENT:
        # Dynamic pricing
        discount = 0.15
        final_price = base_price * (1 - discount)
        return {
            "base_price": base_price,
            "final_price": final_price,
            "discount": discount,
            "pricing_strategy": "dynamic"
        }
    else:
        # Standard pricing
        return {
            "base_price": base_price,
            "final_price": base_price,
            "discount": 0.0,
            "pricing_strategy": "standard"
        }


@app.post("/api/pricing")
async def get_pricing(
        data: Dict[str, Any],
        user_id: str = Depends(get_current_user_id)
):
    """Get pricing for items."""
    base_price = data.get("base_price", 100.0)
    return await calculate_pricing(base_price, user_id)


# Search endpoint with multiple feature flags
@app.get("/api/search")
async def search_products(
        query: str,
        user_id: str = Depends(get_current_user_id)
):
    """Search products with feature-flagged enhancements."""
    results = []

    # Feature flag: Enhanced search
    if await ais_enabled("elasticsearch-search", default=False):
        # Simulate Elasticsearch results
        results = [
            {"id": f"es-{i}", "title": f"ES Result {i} for {query}", "score": 0.9 - i * 0.1}
            for i in range(3)
        ]
        search_engine = "elasticsearch"
    else:
        # Basic search
        results = [
            {"id": f"basic-{i}", "title": f"Basic Result {i} for {query}", "score": 0.5 - i * 0.1}
            for i in range(2)
        ]
        search_engine = "basic"

    # A/B test: Result ranking
    variant = await aget_variant("search-ranking", user_id, default_variant=ExperimentVariant.CONTROL)

    if variant == ExperimentVariant.TREATMENT:
        # Personalized ranking
        for result in results:
            result["personalized_score"] = result["score"] * 1.2
        results.sort(key=lambda x: x["personalized_score"], reverse=True)
        ranking_algorithm = "personalized"
    else:
        # Standard ranking
        ranking_algorithm = "standard"

    return {
        "query": query,
        "results": results,
        "search_engine": search_engine,
        "ranking_algorithm": ranking_algorithm,
        "total": len(results)
    }


# Health check with feature flag status
@app.get("/health")
async def health_check():
    """Health check endpoint with feature flag status."""
    try:
        # Check core feature flags
        feature_status = {
            "enhanced_product_details": await ais_enabled("enhanced-product-details", default=False),
            "elasticsearch_search": await ais_enabled("elasticsearch-search", default=False),
            "premium_api": await ais_enabled("premium-api", default=False)
        }

        return {
            "status": "healthy",
            "feature_flags": feature_status,
            "timestamp": "2025-01-01T00:00:00Z"
        }
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Feature flag service unavailable: {str(e)}"
        )


# Global exception handler for feature flag errors
@app.exception_handler(FeatureFlagError)
async def feature_flag_exception_handler(request, exc):
    """Handle feature flag errors gracefully."""
    return JSONResponse(
        status_code=200,  # Don't fail the request
        content={
            "warning": "Feature flag service unavailable, using defaults",
            "error": str(exc)
        }
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
