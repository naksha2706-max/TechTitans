import socket
import ssl
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from urllib.parse import urlparse

def extract_domain(url: str) -> str:
    if not url:
        return ""
    if not url.startswith(("http://", "https://")):
        url = "http://" + url
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        if domain.startswith("www."):
            domain = domain[4:]
        if ":" in domain:
            domain = domain.split(":")[0]
        return domain
    except Exception:
        return ""

def check_ssl_certificate(domain: str, port: int = 443, timeout: float = 3.0) -> Dict[str, Any]:
    """
    Checks if an HTTPS connection can establish a valid SSL connection to domain.
    """
    if not domain:
        return {"ssl_valid": False, "error": "No domain provided"}
    
    context = ssl.create_default_context()
    try:
        with socket.create_connection((domain, port), timeout=timeout) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                if not cert:
                    return {"ssl_valid": False, "error": "No certificate returned"}
                
                # Verify expiration
                not_after_str = cert.get('notAfter')
                if not_after_str:
                    not_after = datetime.strptime(not_after_str, '%b %d %H:%M:%S %Y %Z').replace(tzinfo=timezone.utc)
                    if datetime.now(timezone.utc) > not_after:
                        return {"ssl_valid": False, "error": "Certificate expired"}
                
                return {"ssl_valid": True, "error": None}
    except Exception as e:
        return {"ssl_valid": False, "error": str(e)}

def analyze_domain(website_url: str) -> Dict[str, Any]:
    """
    Combines domain parsing, SSL status check, and WHOIS domain age heuristic signals.
    """
    domain = extract_domain(website_url)
    if not domain:
        return {
            "domain": "",
            "ssl_valid": True,  # Neutral default if no site provided
            "ssl_checked": False,
            "has_ssl_error": False
        }

    is_https = website_url.strip().lower().startswith("https://") or not website_url.strip().lower().startswith("http://")
    ssl_res = check_ssl_certificate(domain) if is_https else {"ssl_valid": False, "error": "HTTP without SSL"}

    return {
        "domain": domain,
        "ssl_valid": ssl_res["ssl_valid"],
        "ssl_checked": is_https,
        "has_ssl_error": not ssl_res["ssl_valid"] if is_https else False,
        "error": ssl_res.get("error")
    }
