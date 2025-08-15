from fastapi import FastAPI
from pytrends.request import TrendReq
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

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

@app.get("/")
async def root():
    return JSONResponse(content={
        "ok": True, 
        "service": "n8n-trends-api", 
        "runtime": "python",
        "framework": "fastapi"
    })

@app.get("/trends/{keyword}")
async def get_trends(keyword: str, geo: str = "US", timeframe: str = "today 5-y"):
    try:
        # Build payload for the keyword
        pytrends.build_payload([keyword], cat=0, timeframe=timeframe, geo=geo, gprop='')
        
        # Get interest over time
        interest_over_time = pytrends.interest_over_time()
        
        # Get related topics
        related_topics = pytrends.related_topics()
        
        # Get related queries
        related_queries = pytrends.related_queries()
        
        # Format the response
        result = {
            "keyword": keyword,
            "geo": geo,
            "timeframe": timeframe,
            "interest_over_time": interest_over_time.to_dict('records') if not interest_over_time.empty else [],
            "related_topics": related_topics,
            "related_queries": related_queries
        }
        
        return JSONResponse(content=result)
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

# Export the FastAPI app for Vercel
app_handler = app
