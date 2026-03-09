import argparse
from app.scanner import run_scan


def main():
    parser = argparse.ArgumentParser(
        description="Security Exposure Monitor"
    )

    parser.add_argument(
        "target",
        help="Target domain to analyze"
    )

    args = parser.parse_args()

    result = run_scan(args.target)

    print("\nScan finished\n")
    print("Target:", result["target"])
    print("Final URL:", result["final_url"])
    print("Score:", result["summary"]["score"])
    print("Risk level:", result["summary"]["risk_level"])

    print("\nHeaders")
    print("Present:", result["headers"]["present"])
    print("Missing:", result["headers"]["missing"])

    print("\nCookies")
    print("Total:", result["cookies"]["summary"]["total"])
    print("Missing Secure:", result["cookies"]["summary"]["missing_secure"])
    print("Missing HttpOnly:", result["cookies"]["summary"]["missing_httponly"])
    print("Missing SameSite:", result["cookies"]["summary"]["missing_samesite"])

    print("\nRedirects")
    print("Redirected:", result["redirects"]["redirected"])
    print("Hop count:", result["redirects"]["hop_count"])
    print("HTTP to HTTPS:", result["redirects"]["http_to_https"])

    print("\nRobots.txt found:", result["robots"]["found"])
    print("Sitemap found:", result["sitemap"]["found"])

    print("\nTLS")
    if "error" in result["tls"]:
        print("TLS error:", result["tls"]["error"])
    else:
        print("TLS version:", result["tls"]["tls_version"])

    print("\nJSON report saved to:", result["json_report_path"])
    print("HTML report saved to:", result["html_report_path"])


if __name__ == "__main__":
    main()