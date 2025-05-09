from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
from utils.service import get_long_link, MongoDB, LinkShortner

app = FastAPI()

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    # Include both localhost and 127.0.0.1
    allow_origins=["http://localhost:8000", "http://127.0.0.1:8000", "*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# MongoDB connection
conn = MongoClient(
    "mongodb+srv://suvhradipwork:MEy9fVUQvZXhAQ9Q@linkshortnerc1.eap2amc.mongodb.net")


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    responseObj = []
    cursor = (
        conn.linksCollection.linksCollection
        .find({})
        .sort("_id", -1)  # Sort by newest
        .limit(3)         # Only get last 3
    )
    for item in cursor:
        responseObj.append({
            "id": str(item["_id"]),  # Convert ObjectId to string
            "short_link": item["short_link"],
            "long_link": item["long_link"]
        })
    return templates.TemplateResponse("index.html", {"request": request, "responseObj": responseObj})


@app.get("/{short_link}")
async def redirect_origin(short_link: str):
    try:
        long_url = get_long_link(short_link)
        return RedirectResponse(url=long_url)
    except Exception as ex:
        raise HTTPException(
            status_code=500, detail=f"Internal Server Error: {str(ex)}")


@app.post("/shorten/{long_url:path}")
async def shorten_url(long_url: str):
    """
    Generate a short link for the given long URL (provided in the path) and store it in MongoDB.
    """
    try:
        print(f"Received request to shorten URL: {long_url}")  # Debug log

        # Basic validation
        if not long_url.startswith(("http://", "https://")):
            raise HTTPException(
                status_code=400, detail="Invalid URL: Must start with http:// or https://")

        # Generate and store the short link using service functions
        db = MongoDB()
        ins = LinkShortner(long_url, db)
        short_link = ins.deploy_short_link()

        if isinstance(short_link, Exception):
            raise HTTPException(
                status_code=500, detail=f"Failed to generate short link: {str(short_link)}")

        response = {"short_link": short_link}
        print(f"Returning response: {response}")  # Debug log
        return response
    except Exception as ex:
        raise HTTPException(
            status_code=500, detail=f"Internal Server Error: {str(ex)}")


@app.options("/shorten/{long_url:path}")
async def options_shorten():
    """
    Handle CORS preflight requests for the /shorten/{long_url} endpoint.
    """
    print("Handling OPTIONS request for /shorten")  # Debug log
    return {}
