# Marketing Copy — Deploy Button Generator

## Tweet Thread (5 tweets)

**Tweet 1/5**
The best open source projects have one thing in common:

A "Deploy to Render" badge in their README.

But writing Dockerfiles and render.yaml sucks.

So I automated it. Paste a GitHub repo → get deploy configs in 30 seconds.

Thread 🧵

**Tweet 2/5**
The workflow before:
1. Clone repo
2. Guess the stack
3. Write Dockerfile (trial and error)
4. Figure out render.yaml
5. Test deploy (fails, repeat)

Total time: 2 hours. Success rate: 50%.

**Tweet 3/5**
The workflow now:
1. Paste repo URL
2. Copy 3 files into your project
3. Users click "Deploy" in your README

Total time: 30 seconds. Success rate: whatever your code is.

**Tweet 4/5**
What it detects:
- Node.js (Next.js, Express, Nuxt)
- Python (FastAPI, Flask, Django)
- Go, Rust, Ruby, Static HTML
- Existing Dockerfiles (pass-through)

What it generates:
- Production Dockerfile
- render.yaml with correct commands
- README badge (markdown + HTML)

**Tweet 5/5**
Built this because I ship a lot of repos and hate writing the same deploy configs over and over.

Free. No auth needed. Works with any public repo.

Try it: github.com/anxovatomica/deploy-button-generator

---

## Dev.to Article Draft

**Title:** "I Automated README Badges Because Manual Deploy Configs Are Boring"

**Intro:**
Every open source maintainer's nightmare: a user DMs you saying "how do I run this?" You have a great project but zero deployment docs. I fixed that with a 30-second tool.

**What it does:**
Deploy Button Generator reads any public GitHub repo, detects the stack, and outputs:
1. A production Dockerfile
2. A render.yaml config
3. A "Deploy to Render" badge for your README

**How it works:**
It scans for package.json, requirements.txt, go.mod, Cargo.toml, etc. Maps them to templates. Generates optimized configs. No guessing.

**Example:**
Paste `github.com/owner/fastapi-app` → get:
- Python multi-stage Dockerfile
- render.yaml with `pip install` + `uvicorn` start command
- Badge markdown ready to copy

**Why it matters:**
Lower friction = more users = more stars = more contributors. One README badge can 10x your project's accessibility.

**Conclusion:**
Free. No signup. 30 seconds. Make your repo deployable today.

---

## Hacker News Launch Post

**Title:** Show HN: Auto-generate "Deploy to Render" badges for any GitHub repo

**Body:**
I got tired of manually writing Dockerfiles and render.yaml for every project. Built a tool that does it automatically — paste a GitHub repo URL, get deploy configs in 30 seconds.

What it detects: Node, Python, Go, Rust, Ruby, Static, Docker
What it outputs: Dockerfile, render.yaml, README badge

Works with any public repo. No auth required.

The dog food test: this tool deploys itself using its own generated config.

Would love feedback from maintainers — what stacks should I add next?

Repo: https://github.com/anxovatomica/deploy-button-generator

---

## Reddit Post (r/webdev)

**Title:** Tool: Auto-generate Dockerfile + Render deploy config from any GitHub repo

**Body:**
Paste a repo URL. Get:
- Dockerfile (production-ready, multi-stage where needed)
- render.yaml (build/start commands auto-detected)
- README badge markdown + HTML

Supports: Node, Python, Go, Rust, Ruby, Static, Docker

I built this because I ship a lot of small projects and writing the same deploy configs felt like Groundhog Day.

Free. No signup. Try it and tell me what stacks I'm missing.

github.com/anxovatomica/deploy-button-generator

---

## Product Hunt Launch Copy

**Tagline:** From GitHub repo to deployable in 30 seconds

**Description:**
Deploy Button Generator auto-creates deployment configurations for any public GitHub repository. No more guessing build commands or writing Dockerfiles from scratch.

**Key features:**
🔍 Auto-detects stack from repo files
🐳 Generates production Dockerfiles
⚙️ Creates render.yaml configs
🏷️ Outputs "Deploy to Render" badge
🌐 Web UI + REST API
🔓 No auth needed for public repos

**Maker comment:**
"I maintain multiple open source projects and got tired of writing the same deploy configs. Now I paste a URL and copy-paste 3 files. Done."

**First comment:**
"Dog food test: this project deploys itself using configs it generated. Recursion is fun."

**Pricing:**
Completely free. Open source. MIT license.
