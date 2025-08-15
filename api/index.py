from fastapi import FastAPI
from pytrends.request import TrendReq
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI(title="n8n Trends API", description="Google Trends API using PyTrends")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize PyTrends
pytrends = TrendReq(hl='en-US', tz=360)

@app.get("/health")
async def health():
    """Health check endpoint"""
    return JSONResponse(content={
        "status": "healthy",
        "service": "n8n-trends-api",
        "runtime": "python",
        "framework": "fastapi"
    })

@app.get("/trends")
async def trends(keywords: str, geo: str = "US", timeframe: str = "today 5-y"):
    """Get trends data for keywords"""
    try:
        keyword_list = [k.strip() for k in keywords.split(',')]
        pytrends.build_payload(keyword_list, cat=0, timeframe=timeframe, geo=geo, gprop='')
        
        # Get interest over time
        interest_over_time = pytrends.interest_over_time()
        
        result = {
            "keywords": keyword_list,
            "geo": geo,
            "timeframe": timeframe,
            "interest_over_time": interest_over_time.to_dict('records') if not interest_over_time.empty else []
        }
        
        return JSONResponse(content=result)
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

@app.get("/compare")
async def compare(keywords: str, geo: str = "US", timeframe: str = "today 5-y"):
    """Compare multiple keywords"""
    try:
        keyword_list = [k.strip() for k in keywords.split(',')]
        if len(keyword_list) < 2:
            return JSONResponse(
                status_code=400,
                content={"error": "At least 2 keywords required for comparison"}
            )
        
        pytrends.build_payload(keyword_list, cat=0, timeframe=timeframe, geo=geo, gprop='')
        
        # Get interest over time for comparison
        interest_over_time = pytrends.interest_over_time()
        
        result = {
            "keywords": keyword_list,
            "geo": geo,
            "timeframe": timeframe,
            "comparison_data": interest_over_time.to_dict('records') if not interest_over_time.empty else []
        }
        
        return JSONResponse(content=result)
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

@app.get("/related")
async def related(keyword: str, geo: str = "US", timeframe: str = "today 5-y"):
    """Get related topics and queries for a keyword"""
    try:
        pytrends.build_payload([keyword], cat=0, timeframe=timeframe, geo=geo, gprop='')
        
        # Get related topics and queries
        related_topics = pytrends.related_topics()
        related_queries = pytrends.related_queries()
        
        result = {
            "keyword": keyword,
            "geo": geo,
            "timeframe": timeframe,
            "related_topics": related_topics,
            "related_queries": related_queries
        }
        
        return JSONResponse(content=result)
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

# Root endpoint for backwards compatibility
@app.get("/")
async def root():
    return JSONResponse(content={
        "ok": True,
        "service": "n8n-trends-api",
        "runtime": "python",
        "framework": "fastapi",
        "endpoints": ["/health", "/trends", "/compare", "/related"]
    })

# Export the FastAPI app for Vercel
asgi_app = app
