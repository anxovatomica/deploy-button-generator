"""
Render Config Generator — creates render.yaml for Render.com deployment.
"""

import re
from urllib.parse import urlparse

def generate_render_yaml(repo_url: str, stack: str, repo_files: dict) -> str:
    """
    Generate render.yaml content for the detected stack.
    """
    parsed = urlparse(repo_url.rstrip("/"))
    path_parts = parsed.path.strip("/").split("/")
    repo_name = path_parts[1] if len(path_parts) > 1 else "app"
    
    # Sanitize name for Render
    service_name = re.sub(r'[^a-zA-Z0-9-]', '-', repo_name).lower().strip('-')
    
    # Determine port and runtime
    port = "8000"
    if stack == "node":
        port = "3000"
    elif stack == "ruby":
        port = "3000"
    elif stack == "static":
        port = "80"
    elif stack == "go" or stack == "rust":
        port = "8080"
    
    # Build command
    build_cmd = ""
    if stack == "node":
        build_cmd = "npm install"
    elif stack == "python":
        build_cmd = "pip install -r requirements.txt"
    elif stack == "go":
        build_cmd = "go build -o app ."
    elif stack == "rust":
        build_cmd = "cargo build --release"
    elif stack == "ruby":
        build_cmd = "bundle install"
    elif stack == "docker":
        build_cmd = ""
    elif stack == "static":
        build_cmd = ""
    
    # Start command
    start_cmd = ""
    if stack == "node":
        import json
        pkg = json.loads(repo_files.get("package.json", "{}"))
        scripts = pkg.get("scripts", {})
        start_cmd = scripts.get("start", "npm start")
    elif stack == "python":
        req_content = repo_files.get("requirements.txt", "")
        if "fastapi" in req_content.lower():
            start_cmd = "uvicorn main:app --host 0.0.0.0 --port 8000"
        elif "flask" in req_content.lower():
            start_cmd = "flask run --host=0.0.0.0 --port=8000"
        elif "django" in req_content.lower():
            start_cmd = "gunicorn myproject.wsgi:application --bind 0.0.0.0:8000"
        else:
            start_cmd = "python app.py"
    elif stack == "go":
        start_cmd = "./app"
    elif stack == "rust":
        start_cmd = "./target/release/app"
    elif stack == "ruby":
        gemfile = repo_files.get("Gemfile", "")
        if "rails" in gemfile.lower():
            start_cmd = "bundle exec rails server -b 0.0.0.0"
        else:
            start_cmd = "ruby app.rb"
    elif stack == "static":
        start_cmd = "nginx -g 'daemon off;'"
    elif stack == "docker":
        start_cmd = ""
    
    # Generate render.yaml
    yaml_content = f"""services:
  - type: web
    name: {service_name}
    runtime: docker
    repo: {repo_url}
    branch: main
    plan: free
    envVars:
      - key: PORT
        value: {port}
"""
    
    if build_cmd:
        yaml_content += f"    buildCommand: {build_cmd}\n"
    if start_cmd:
        yaml_content += f"    startCommand: {start_cmd}\n"
    
    yaml_content += f"""    healthCheckPath: /
    autoDeploy: true
"""
    
    # Add environment-specific vars for common frameworks
    if stack == "node" and "next" in repo_files.get("package.json", "").lower():
        yaml_content += """      - key: NODE_ENV
        value: production
"""
    
    if stack == "python" and "django" in repo_files.get("requirements.txt", "").lower():
        yaml_content += """      - key: DJANGO_SETTINGS_MODULE
        value: myproject.settings.production
      - key: SECRET_KEY
        generateValue: true
"""
    
    return yaml_content.strip()
