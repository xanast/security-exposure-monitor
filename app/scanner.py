import json
from pathlib import Path

import requests

from app.headers_audit import analyze_headers
from app.tls_checks import check_tls
from app.cookies_audit import analyze_cookies
from app.robots_audit import analyze_robots
from app.sitemap_audit import analyze_sitemap
from app.redirects_audit import analyze_redirects
from app.report_html import save_html_report


def save_json_report(report_data, filename="outputs/report.json"):
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(report_data, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    return str(path)


def run_scan(target):
    if not target.startswith("http"):
        target = "https://" + target

    response = requests.get(
        target,
        timeout=10,
        allow_redirects=True,
        headers={"User-Agent": "SecurityExposureMonitor/1.0"}
    )

    headers_result = analyze_headers(response.headers)
    tls_result = check_tls(target)
    cookies_result = analyze_cookies(response)
    robots_result = analyze_robots(target)
    sitemap_result = analyze_sitemap(target)
    redirects_result = analyze_redirects(response)

    score = 100
    score -= len(headers_result["missing"]) * 5
    score -= cookies_result["summary"]["missing_secure"] * 3
    score -= cookies_result["summary"]["missing_httponly"] * 3
    score -= cookies_result["summary"]["missing_samesite"] * 2

    if not robots_result["found"]:
        score -= 2

    if not sitemap_result["found"]:
        score -= 2

    if redirects_result["redirected"] and not redirects_result["http_to_https"]:
        score -= 3

    score = max(score, 0)

    summary = {
        "score": score,
        "risk_level": "low" if score > 80 else "medium" if score > 50 else "high"
    }

    report = {
        "target": target,
        "final_url": redirects_result["final_url"],
        "headers": headers_result,
        "tls": tls_result,
        "cookies": cookies_result,
        "robots": robots_result,
        "sitemap": sitemap_result,
        "redirects": redirects_result,
        "summary": summary
    }

    json_report_path = save_json_report(report)
    html_report_path = save_html_report(report)

    return {
        **report,
        "json_report_path": json_report_path,
        "html_report_path": html_report_path
    }