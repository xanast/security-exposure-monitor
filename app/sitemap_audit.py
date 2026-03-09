import requests
from urllib.parse import urljoin


def analyze_sitemap(base_url):
    sitemap_url = urljoin(base_url, "/sitemap.xml")

    try:
        response = requests.get(sitemap_url, timeout=10)

        return {
            "url": sitemap_url,
            "found": response.status_code == 200,
            "status_code": response.status_code,
            "content_type": response.headers.get("Content-Type")
        }

    except Exception as e:
        return {
            "url": sitemap_url,
            "found": False,
            "error": str(e)
        }