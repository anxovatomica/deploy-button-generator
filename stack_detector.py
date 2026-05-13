"""
Stack Detector — analyzes repo file structure to identify the tech stack.
"""

import json
import re

STACK_PRIORITY = [
    "node",      # package.json
    "python",    # requirements.txt / pyproject.toml
    "go",        # go.mod
    "rust",      # Cargo.toml
    "ruby",      # Gemfile
    "docker",    # Dockerfile already exists
    "static",    # index.html at root
]

def detect_stack(repo_files: dict) -> dict:
    """
    Analyze repo files and return detected stack + metadata.
    repo_files: dict of filename -> content
    """
    detected_files = []
    stack = "static"  # default
    build_command = ""
    start_command = ""
    
    # Check each stack indicator
    if "package.json" in repo_files:
        stack = "node"
        detected_files.append("package.json")
        pkg = json.loads(repo_files["package.json"])
        scripts = pkg.get("scripts", {})
        
        # Detect framework
        dependencies = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
        if "next" in dependencies:
            build_command = "npm run build"
            start_command = "npm start"
        elif "nuxt" in dependencies or "nuxt3" in dependencies:
            build_command = "npm run build"
            start_command = "node .output/server/index.mjs"
        elif "express" in dependencies or "fastify" in dependencies or "koa" in dependencies:
            start_command = "npm start"
        elif "vue" in dependencies and "@vue/cli-service" in dependencies:
            build_command = "npm run build"
            start_command = "npx serve -s dist -l 3000"
        elif "react-scripts" in dependencies:
            build_command = "npm run build"
            start_command = "npx serve -s build -l 3000"
        else:
            start_command = scripts.get("start", "npm start")
            build_command = scripts.get("build", "")
    
    elif "requirements.txt" in repo_files or "pyproject.toml" in repo_files:
        stack = "python"
        if "requirements.txt" in repo_files:
            detected_files.append("requirements.txt")
        if "pyproject.toml" in repo_files:
            detected_files.append("pyproject.toml")
        
        # Check for FastAPI, Flask, Django
        req_content = repo_files.get("requirements.txt", "")
        if "fastapi" in req_content.lower():
            start_command = "uvicorn main:app --host 0.0.0.0 --port 8000"
        elif "flask" in req_content.lower():
            start_command = "flask run --host=0.0.0.0 --port=8000"
        elif "django" in req_content.lower():
            start_command = "python manage.py runserver 0.0.0.0:8000"
        else:
            start_command = "python app.py"
    
    elif "go.mod" in repo_files:
        stack = "go"
        detected_files.append("go.mod")
        build_command = "go build -o app ."
        start_command = "./app"
    
    elif "Cargo.toml" in repo_files:
        stack = "rust"
        detected_files.append("Cargo.toml")
        build_command = "cargo build --release"
        start_command = "./target/release/app"
    
    elif "Gemfile" in repo_files:
        stack = "ruby"
        detected_files.append("Gemfile")
        build_command = "bundle install"
        # Check for Rails, Sinatra
        gemfile = repo_files.get("Gemfile", "")
        if "rails" in gemfile.lower():
            start_command = "bundle exec rails server -b 0.0.0.0"
        elif "sinatra" in gemfile.lower():
            start_command = "ruby app.rb"
        else:
            start_command = "ruby app.rb"
    
    elif "Dockerfile" in repo_files:
        stack = "docker"
        detected_files.append("Dockerfile")
    
    elif "index.html" in repo_files:
        stack = "static"
        detected_files.append("index.html")
    
    # Check for additional config files
    for f in ["Dockerfile", "docker-compose.yml", "nginx.conf", "Makefile"]:
        if f in repo_files:
            detected_files.append(f)
    
    return {
        "stack": stack,
        "detected_files": detected_files,
        "build_command": build_command,
        "start_command": start_command
    }
