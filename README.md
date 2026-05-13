# 🚀 Deploy This Button Generator

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/anxovatomica/deploy-button-generator)

Paste a GitHub repo URL → get `Dockerfile` + `render.yaml` + a one-click **"Deploy to Render"** badge.

**🌐 Live Demo:** http://43.98.167.138:8002

No auth. No config. Just paste and copy-paste.

---

## What It Does

| Input | Output |
|-------|--------|
| `github.com/owner/repo` | `Dockerfile` (auto-detected stack) |
| | `render.yaml` (Render.com deploy config) |
| | Markdown + HTML badge for README |

**Supported stacks:** Node.js · Python · Go · Rust · Ruby · Static HTML

---

## Quick Start

### Local

```bash
git clone https://github.com/anxovatomica/deploy-button-generator
cd deploy-button-generator
chmod +x deploy.sh
./deploy.sh
```

Then open [http://localhost:8000](http://localhost:8000)

### API

```bash
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{"repo_url": "https://github.com/owner/repo"}'
```

**Response:**
```json
{
  "repo_url": "https://github.com/owner/repo",
  "stack": "python",
  "detected_files": ["requirements.txt"],
  "dockerfile": "...",
  "render_yaml": "...",
  "badge_markdown": "...",
  "badge_html": "..."
}
```

---

## Deploy to Render

Click this button to deploy THIS project:

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/anxovatomica/deploy-button-generator)

Or use the `render.yaml` in this repo.

---

## How Stack Detection Works

| File Detected | Stack | Dockerfile Template |
|---------------|-------|---------------------|
| `package.json` | Node.js | `node:18-alpine`, multi-stage if build script |
| `requirements.txt` / `pyproject.toml` | Python | `python:3.11-slim`, FastAPI/Flask/Django aware |
| `go.mod` | Go | `golang:1.21-alpine`, multi-stage |
| `Cargo.toml` | Rust | `rust:1.75-slim`, multi-stage |
| `Gemfile` | Ruby | `ruby:3.2-slim`, Rails/Sinatra aware |
| `Dockerfile` exists | Docker | Use existing, generate render.yaml only |
| `index.html` at root | Static | `nginx:alpine` |

---

## Tech Stack

- **Backend:** FastAPI + Uvicorn
- **Templates:** Jinja2
- **Fetcher:** GitHub Raw API (no auth needed for public repos)
- **Deployment:** Docker + Render.com

---

## File Structure

```
deploy-button-generator/
├── main.py                  # FastAPI app
├── stack_detector.py        # Detect tech stack from repo files
├── dockerfile_generator.py  # Generate Dockerfile per stack
├── render_config.py         # Generate render.yaml
├── badge_generator.py       # README badge snippets
├── github_fetcher.py        # Read GitHub repo files
├── requirements.txt         # Python deps
├── Dockerfile               # This app's container
├── render.yaml              # Deploy THIS app to Render
├── deploy.sh                # One-shot local deploy
├── README.md                # This file
└── templates/
    ├── index.html           # Landing page
    ├── result.html          # Generated output
    └── error.html           # Error page
```

---

## License

MIT — use it, fork it, deploy it.

Built for builders who just want to ship. 🏁
