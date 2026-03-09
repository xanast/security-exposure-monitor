def analyze_cookies(response):
    cookies = []

    raw_cookie_headers = response.raw.headers.get_all("Set-Cookie")
    if not raw_cookie_headers:
        raw_cookie_headers = response.headers.get("Set-Cookie")
        if raw_cookie_headers:
            raw_cookie_headers = [raw_cookie_headers]
        else:
            raw_cookie_headers = []

    for raw in raw_cookie_headers:
        cookie_info = {
            "raw": raw,
            "secure": "Secure" in raw,
            "httponly": "HttpOnly" in raw,
            "samesite": "SameSite" in raw
        }
        cookies.append(cookie_info)

    summary = {
        "total": len(cookies),
        "missing_secure": 0,
        "missing_httponly": 0,
        "missing_samesite": 0
    }

    for cookie in cookies:
        if not cookie["secure"]:
            summary["missing_secure"] += 1
        if not cookie["httponly"]:
            summary["missing_httponly"] += 1
        if not cookie["samesite"]:
            summary["missing_samesite"] += 1

    return {
        "cookies": cookies,
        "summary": summary
    }