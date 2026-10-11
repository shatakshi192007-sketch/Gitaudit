import subprocess
import sys

def get_staged_files():
    """
    Retrieves a list of all staged file names safely using explicit UTF-8 decoding.
    """
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            capture_output=True,
            text=True,
            encoding='utf-8',  # Explicitly force UTF-8 to bypass Windows decoding crashes
            errors='ignore',   # Ignore unreadable formatting bytes
            check=True
        )
        return [f.strip() for f in result.stdout.splitlines() if f.strip()]
    except subprocess.CalledProcessError:
        print("❌ Error: Failed to retrieve staged files. Is this a Git repository?")
        sys.exit(1)

def get_staged_file_diff(file_path):
    """
    Retrieves the incoming changes safely, handling empty states and string decoding.
    """
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", file_path],
            capture_output=True,
            text=True,
            encoding='utf-8',  # Force UTF-8 text processing
            errors='ignore',
            check=True
        )
        
        # Verify the stdout payload is an actual string before parsing
        if not result.stdout:
            return ""
            
        added_lines = []
        for line in result.stdout.splitlines():
            if line.startswith("+") and not line.startswith("+++"):
                added_lines.append(line[1:])
                
        return "\n".join(added_lines)
    except subprocess.CalledProcessError:
        return ""