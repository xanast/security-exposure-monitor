SECURITY_HEADERS = [
    "Content-Security-Policy",
    "Strict-Transport-Security",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Referrer-Policy"
]


def analyze_headers(headers):

    present = []
    missing = []

    for header in SECURITY_HEADERS:
        if header in headers:
            present.append(header)
        else:
            missing.append(header)

    return {
        "present": present,
        "missing": missing
    }