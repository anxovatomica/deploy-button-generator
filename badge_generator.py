"""
Badge Generator — creates "Deploy to Render" badge snippets.
"""

from urllib.parse import quote

def generate_badge(repo_url: str) -> tuple:
    """
    Generate Markdown and HTML badge snippets.
    Returns: (markdown, html)
    """
    # Encode URL for query parameter
    encoded_url = quote(repo_url, safe='')
    
    badge_image = "https://render.com/images/deploy-to-render-button.svg"
    deploy_link = f"https://render.com/deploy?repo={encoded_url}"
    
    markdown = f"""[![Deploy to Render]({badge_image})]({deploy_link})"""
    
    html = f"""<p align="center">
  <a href="{deploy_link}">
    <img src="{badge_image}" alt="Deploy to Render" width="180" />
  </a>
</p>"""
    
    return markdown, html
