# Deploy This Button Generator - Build Spec
## Overview
A web service that analyzes any GitHub repo and generates:
1. Dockerfile (auto-detects stack)
2. `render.yaml` (Render deploy config)
3. One-click "Deploy to Render" badge for README

Users paste a repo URL → get copy-paste ready deploy configs.

## Core Features (MVP)
1. **Stack Detection** — Read package.json, requirements.txt, Cargo.toml, go.mod, Dockerfile, etc. to identify the tech stack
2. **Dockerfile Generator** — Template-based generation per stack (Node, Python, Go, Ruby, static HTML)
3. **Render Config Generator** — Auto-generate `render.yaml` with detected build/start commands
4. **Badge Generator** — Markdown badge + HTML snippet for README
5. **API + Web UI** — Both endpoint and browser form

## Architecture
```
FastAPI app
├── stack_detector.py      # Analyze repo structure
├── dockerfile_generator.py # Templates per stack
├── render_config.py       # Generate render.yaml
├── badge_generator.py     # README snippets
├── github_fetcher.py      # Clone / read repo files (raw GitHub API)
├── main.py                # FastAPI app
└── templates/             # Dockerfile templates
```

## Tech Stack
- Python 3.11 + FastAPI + Jinja2
- SQLite (track generated configs, analytics)
- GitHub raw API (no auth needed for public repos)
- Render deployment ready

## API Contract
```
POST /api/generate
Body: {"repo_url": "https://github.com/owner/repo"}
Response: {
  "dockerfile": "...",
  "render_yaml": "...",
  "badge_markdown": "...",
  "badge_html": "...",
  "stack": "python",
  "detected_files": ["requirements.txt", "main.py"]
}
```

## Stack Detection Logic
1. `package.json` → Node.js (check for Next.js, Express, etc.)
2. `requirements.txt` / `pyproject.toml` → Python
3. `go.mod` → Go
4. `Cargo.toml` → Rust
5. `Gemfile` → Ruby
6. `Dockerfile` already exists → use it, just generate render.yaml
7. `index.html` at root → Static site (nginx)

## Dockerfile Templates
- **Node**: `node:18-alpine`, `npm install`, `npm start` or `node server.js`
- **Python**: `python:3.11-slim`, `pip install -r requirements.txt`, `uvicorn main:app --host 0.0.0.0`
- **Go**: `golang:1.21-alpine`, multi-stage build
- **Static**: `nginx:alpine`, copy files

## render.yaml Template
```yaml
services:
  - type: web
    name: {repo_name}
    runtime: docker
    repo: {repo_url}
    branch: main
    plan: free
```

## Badge Markdown
```
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo={repo_url})
```

## Web UI
Simple one-page form:
- Input: GitHub repo URL
- Button: "Generate Deploy Config"
- Output: Tabs for Dockerfile / render.yaml / Badge
- "Copy" buttons for each

## File Structure
```
deploy-button-generator/
├── main.py
├── stack_detector.py
├── dockerfile_generator.py
├── render_config.py
├── badge_generator.py
├── github_fetcher.py
├── requirements.txt
├── Dockerfile
├── render.yaml
├── templates/
│   ├── node.Dockerfile
│   ├── python.Dockerfile
│   ├── go.Dockerfile
│   ├── static.Dockerfile
│   └── index.html
└── README.md
```

## MUST HAVES
- Works with public repos (no auth needed)
- 5 stack templates minimum
- Clean copy-paste output
- Works on mobile
- No manual config after deploy

## GOD LEVEL REQUIREMENTS
- Single deploy script: `./deploy.sh`
- Auto-provisions on Render
- Self-documenting with examples
- SEO-friendly landing page
- "Deploy THIS project to Render" — eat your own dog food!
