def analyze_redirects(response):
    chain = []

    for item in response.history:
        chain.append({
            "url": item.url,
            "status_code": item.status_code,
            "location": item.headers.get("Location")
        })

    final_url = response.url
    redirected = len(response.history) > 0

    http_to_https = False
    if redirected and chain:
        first_url = chain[0]["url"]
        if first_url.startswith("http://") and final_url.startswith("https://"):
            http_to_https = True

    return {
        "redirected": redirected,
        "hop_count": len(chain),
        "chain": chain,
        "final_url": final_url,
        "http_to_https": http_to_https
    }