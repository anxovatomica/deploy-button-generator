"""
Deploy Button Generator
A FastAPI web service that analyzes GitHub repos and generates deployment configs.
"""

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn

from stack_detector import detect_stack
from dockerfile_generator import generate_dockerfile
from render_config import generate_render_yaml
from badge_generator import generate_badge
from github_fetcher import fetch_repo_files

app = FastAPI(
    title="Deploy This Button Generator",
    description="Analyze any GitHub repo and get Dockerfile + render.yaml + Deploy badge",
    version="1.0.0"
)

# Templates
templates = Jinja2Templates(directory="templates")

# Pydantic models
class GenerateRequest(BaseModel):
    repo_url: str

class GenerateResponse(BaseModel):
    repo_url: str
    stack: str
    detected_files: list
    dockerfile: str
    render_yaml: str
    badge_markdown: str
    badge_html: str
    build_command: str
    start_command: str

@app.get("/", response_class=HTMLResponse)
async def landing_page(request: Request):
    """Landing page with the web UI form."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/generate")
async def api_generate(request: GenerateRequest):
    """
    API endpoint to generate deployment configs from a GitHub repo URL.
    """
    try:
        result = process_repo(request.repo_url)
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"error": str(e)}
        )

@app.post("/generate")
async def web_generate(request: Request, repo_url: str = Form(...)):
    """
    Web form endpoint — returns the result page.
    """
    try:
        result = process_repo(repo_url)
        return templates.TemplateResponse("result.html", {
            "request": request,
            **result
        })
    except Exception as e:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": str(e)
        })

def process_repo(repo_url: str) -> dict:
    """
    Core processing pipeline: detect stack → generate configs.
    """
    # Normalize URL
    repo_url = repo_url.rstrip("/")
    if not repo_url.startswith("http"):
        repo_url = f"https://github.com/{repo_url}"
    
    # Fetch repo files
    repo_files = fetch_repo_files(repo_url)
    
    # Detect stack
    stack_info = detect_stack(repo_files)
    stack = stack_info["stack"]
    detected_files = stack_info["detected_files"]
    
    # Generate configs
    dockerfile = generate_dockerfile(stack, repo_files, repo_url)
    render_yaml = generate_render_yaml(repo_url, stack, repo_files)
    badge_md, badge_html = generate_badge(repo_url)
    
    return {
        "repo_url": repo_url,
        "stack": stack,
        "detected_files": detected_files,
        "dockerfile": dockerfile,
        "render_yaml": render_yaml,
        "badge_markdown": badge_md,
        "badge_html": badge_html,
        "build_command": stack_info.get("build_command", ""),
        "start_command": stack_info.get("start_command", "")
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
