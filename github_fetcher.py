"""
GitHub Fetcher — reads public repo files via GitHub raw API (no auth needed).
"""

import requests
import re
import base64
from urllib.parse import urlparse

def extract_owner_repo(repo_url: str) -> tuple:
    """Extract (owner, repo_name) from GitHub URL."""
    parsed = urlparse(repo_url.rstrip("/"))
    path_parts = parsed.path.strip("/").split("/")
    if len(path_parts) < 2:
        raise ValueError(f"Invalid GitHub URL: {repo_url}")
    return path_parts[0], path_parts[1]

def fetch_repo_files(repo_url: str) -> dict:
    """
    Fetch key files from a GitHub repo to detect the stack.
    Returns dict: filename -> content.
    """
    owner, repo = extract_owner_repo(repo_url)
    base_raw = f"https://raw.githubusercontent.com/{owner}/{repo}/main"
    
    # Key files to check (in priority order)
    key_files = [
        "package.json",
        "requirements.txt",
        "pyproject.toml",
        "go.mod",
        "Cargo.toml",
        "Gemfile",
        "Dockerfile",
        "docker-compose.yml",
        "nginx.conf",
        "index.html",
        "Makefile",
        "main.py",
        "app.py",
        "server.js",
        "main.go",
        "src/main.rs",
        "config.ru",
        "app.rb",
    ]
    
    files = {}
    
    for filename in key_files:
        try:
            url = f"{base_raw}/{filename}"
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                files[filename] = resp.text
        except Exception:
            pass
    
    # If main branch fails, try master
    if not files:
        base_raw = f"https://raw.githubusercontent.com/{owner}/{repo}/master"
        for filename in key_files:
            try:
                url = f"{base_raw}/{filename}"
                resp = requests.get(url, timeout=10)
                if resp.status_code == 200:
                    files[filename] = resp.text
            except Exception:
                pass
    
    if not files:
        # Try GitHub API for repo contents (public repos, no auth)
        try:
            api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/"
            resp = requests.get(api_url, timeout=10, headers={"Accept": "application/vnd.github.v3+json"})
            if resp.status_code == 200:
                contents = resp.json()
                for item in contents:
                    if item["type"] == "file" and item["name"] in key_files:
                        try:
                            file_resp = requests.get(item["download_url"], timeout=10)
                            if file_resp.status_code == 200:
                                files[item["name"]] = file_resp.text
                        except Exception:
                            pass
        except Exception:
            pass
    
    return files

def fetch_file_content(repo_url: str, filepath: str) -> str:
    """Fetch a single file from a GitHub repo."""
    owner, repo = extract_owner_repo(repo_url)
    for branch in ["main", "master"]:
        url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{filepath}"
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                return resp.text
        except Exception:
            pass
    return ""
