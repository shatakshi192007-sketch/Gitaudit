# GitAudit 🛡️

GitAudit is a local, automated pre-commit security guardian built in Python. It scans code patches for exposed secrets, API keys, and private tokens **locally** before they ever leave your machine, preventing high-risk credential leaks to remote repositories.

## 🤝 Contributing

GitAudit is open-source and loves community contributions! Whether you want to add new credential regex signatures, optimize the Windows terminal pipeline, or improve documentation, your help is welcome.

To get started:
1. **Fork** the repository.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Open a **Pull Request** and let's collaborate!

If you have feature ideas or want to discuss improvements, feel free to open a new **Issue**!



## 🚀 Features
- **Zero-Leak Pipeline:** Integrates natively with Git Hooks to automatically halt insecure commits.
- **Delta Scans:** Utilizes `git diff --cached` to lightning-scan only incoming text line modifications instead of scanning slow, historic codebases.
- **Multi-Signature Regex Engine:** Pre-configured rules mapping AWS access tokens, Slack integrations, generic private cryptographic keys, and high-entropy variable assignments (`api_key`, `secret`, etc.).
- **Cross-Platform Resilient:** Built-in explicit UTF-8 byte stream handlers to bypass standard Windows terminal decoding (`charmap`) crashes.

## 📁 Architecture
```text
gitaudit/
├── core/
│   ├── __init__.py
│   └── git_helper.py    # Interfaces with Git caching commands safely
├── hooks/
│   └── pre-commit       # Native Git automated wrapper script
├── scanner.py           # Core cryptographic token regex signature rules
└── main.py              # CLI entry point and status orchestrator
```

## 🛠️ Installation & Setup

1. **Clone the project workspace:**
   ```bash
   git clone https://github.com
   cd GitAudit
   ```

2. **Initialize Git inside your local workspace:**
   ```bash
   git init
   ```

3. **Install the Pre-Commit Shield:**
   Copy the script logic from your project files into your local hidden configuration directory:
   ```bash
   # On Windows (PowerShell)
   New-Item -Path .git/hooks/pre-commit -ItemType File
   ```
   Paste the wrapper execution shell instructions into `.git/hooks/pre-commit`.

## 🧪 How It Works

When you attempt to make a commit with hardcoded secrets, GitAudit steps in automatically:

```bash
\$ git add test_samples.txt
\$ git commit -m "Deploying app configs"

🔍 GitAudit: Initializing security scan over 1 staged file(s)...

⚠️  [SECURITY LEAK DETECTED IN: test_samples.txt]
============================================================
📍 Match Rule  : AWS Access Key
   Diff Line    : 5
   Exposed Text : aws_key_id = "AKIA1234567890ABCDEF"
------------------------------------------------------------

❌ GitAudit Scan Failed: Found 1 critical leak(s). Action Blocked!
```
The commit is immediately aborted. Once you remove the secret from your file, stage it again, and commit, it passes cleanly!
