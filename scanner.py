import re

# Defined high-risk credential signatures matching industry leak patterns
SCAN_RULES = {
    "AWS Access Key": r"([^A-Z0-9]|^)(AKIA|ASCA|AAAA)[A-Z0-9]{16}([^A-Z0-9]|$)",
    "Generic Private Key": r"-----BEGIN ?(RSA|OPENSSH|DSA|EC)? PRIVATE KEY-----",
    "Slack Token": r"xoxb-[0-9]{11,13}-[a-zA-Z0-9]{24}",
    "Exposed Hardcoded Credential": r"(?i)(api_key|secret|password|token)\s*[:=]\s*['\"][a-zA-Z0-9_\-]{16,}['\"]"
}

def scan_text(payload_text):
    """
    Scans a block of text line by line against regex signatures.
    Returns a list of detected threat dictionary objects.
    """
    found_leaks = []
    lines = payload_text.splitlines()
    
    for line_num, line_content in enumerate(lines, start=1):
        for rule_name, pattern in SCAN_RULES.items():
            if re.search(pattern, line_content):
                found_leaks.append({
                    "rule": rule_name,
                    "line": line_num,
                    "content": line_content.strip()
                })
                
    return found_leaks