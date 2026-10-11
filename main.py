import sys
from scanner import scan_text
from core import git_helper

get_staged_files = git_helper.get_staged_files
get_staged_file_diff = git_helper.get_staged_file_diff

def run_git_audit():
    """
    Orchestrates the automated scanning pipeline across all staged files.
    """
    staged_files = get_staged_files()
    
    if not staged_files:
        print("✅ GitAudit: No staged changes found to scan.")
        sys.exit(0)
        
    print(f"🔍 GitAudit: Initializing security scan over {len(staged_files)} staged file(s)...")
    total_leaks = 0
    
    for file_path in staged_files:
        # Ignore binary files or lock files that might cause parsing errors
        if file_path.endswith(('.png', '.jpg', '.jpeg', '.lock', '.exe', '.pdf')):
            continue
            
        file_diff_content = get_staged_file_diff(file_path)
        if not file_diff_content.strip():
            continue
            
        threats_found = scan_text(file_diff_content)
        
        if threats_found:
            total_leaks += len(threats_found)
            print(f"\n⚠️  [SECURITY LEAK DETECTED IN: {file_path}]")
            print("=" * 60)
            for issue in threats_found:
                print(f"📍 Match Rule  : {issue['rule']}")
                print(f"   Diff Line    : {issue['line']}")
                print(f"   Exposed Text : {issue['content']}")
                print("-" * 60)

    if total_leaks > 0:
        print(f"\n❌ GitAudit Scan Failed: Found {total_leaks} critical leak(s). Action Blocked!")
        sys.exit(1)
    else:
        print("\n✅ GitAudit Scan Passed: No hardcoded credentials detected in this patch.")
        sys.exit(0)

if __name__ == "__main__":
    run_git_audit()