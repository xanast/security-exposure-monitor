import requests
from urllib.parse import urljoin


def analyze_robots(base_url):
    robots_url = urljoin(base_url, "/robots.txt")

    try:
        response = requests.get(robots_url, timeout=10)

        if response.status_code != 200:
            return {
                "url": robots_url,
                "found": False,
                "status_code": response.status_code,
                "disallow_entries": [],
                "sitemap_entries": []
            }

        lines = [line.strip() for line in response.text.splitlines() if line.strip()]
        disallow_entries = [line for line in lines if line.lower().startswith("disallow:")]
        sitemap_entries = [line for line in lines if line.lower().startswith("sitemap:")]

        return {
            "url": robots_url,
            "found": True,
            "status_code": response.status_code,
            "disallow_entries": disallow_entries,
            "sitemap_entries": sitemap_entries
        }

    except Exception as e:
        return {
            "url": robots_url,
            "found": False,
            "error": str(e),
            "disallow_entries": [],
            "sitemap_entries": []
        }