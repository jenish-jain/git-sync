#!/bin/bash
# Complete Git Sync Project Generator
# Run this script to create the entire project structure with all files

set -e

PROJECT_NAME="git-sync"
echo "Creating Git Sync Project..."

# Create directory structure
mkdir -p "$PROJECT_NAME"/{docs,scripts,config,systemd}
cd "$PROJECT_NAME"

echo "📁 Creating project structure..."

# The documentation files (01-06) and README.md are already created above
# Now create the remaining files

echo "📝 Creating configuration files..."

# config/sync-repos.example.json
cat > config/sync-repos.example.json << 'JSONEOF'
[
  {
    "name": "repository-name-1"
  },
  {
    "name": "repository-name-2"
  },
  {
    "name": "repository-name-3"
  }
]
JSONEOF

# config/README.md
cat > config/README.md << 'CONFIGREADME'
# Configuration

## sync-repos.json

This file contains the list of repositories to sync.

### Format

```json
[
  {
    "name": "repo-name"
  }
]
```

### Setup

1. Copy the example:
   ```bash
   cp sync-repos.example.json ~/sync-repos.json
   ```

2. Edit with your repositories:
   ```bash
   nano ~/sync-repos.json
   ```

3. Or auto-generate from GitHub:
   ```bash
   export GITHUB_TOKEN="your_token"
   python3 ../scripts/generate-config.py
   ```

### Examples

#### Manual Configuration
```json
[
  {"name": "my-project"},
  {"name": "website"},
  {"name": "scripts"}
]
```

#### Exclude Forks and Archived
```bash
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/users/YOUR_USERNAME/repos?per_page=100" | \
  jq '[.[] | select(.fork == false and .archived == false) | {name: .name}]' > ~/sync-repos.json
```
CONFIGREADME

echo "🔧 Creating systemd files..."

# systemd/git-sync.service
cat > systemd/git-sync.service << 'SERVICEEOF'
[Unit]
Description=Git Repository Sync Service
After=network-online.target
Wants=network-online.target
Documentation=https://github.com/jenish-jain/git-sync

[Service]
Type=oneshot
User=jenishjain
Group=jenishjain
WorkingDirectory=/home/jenishjain

# Load environment variables (GitHub token)
EnvironmentFile=/etc/systemd/system/git-sync.env

# Run the sync script
ExecStart=/usr/bin/python3 /opt/git-sync/sync.py

# Logging
StandardOutput=journal
StandardError=journal
SyslogIdentifier=git-sync

# Security hardening
PrivateTmp=yes
NoNewPrivileges=yes
ProtectSystem=strict
ProtectHome=read-only
ReadWritePaths=/home/jenishjain/sync-workspace /home/jenishjain/repositories /home/jenishjain/git-sync.log

# Resource limits
TimeoutStartSec=600
CPUQuota=50%
MemoryMax=512M

# Restart policy
Restart=on-failure
RestartSec=5m

[Install]
WantedBy=multi-user.target
SERVICEEOF

# systemd/git-sync.timer
cat > systemd/git-sync.timer << 'TIMEREOF'
[Unit]
Description=Run Git Sync hourly
Requires=git-sync.service

[Timer]
# Run 5 minutes after boot
OnBootSec=5min

# Run every hour
OnUnitActiveSec=1h

# Run persistently (catch up if system was off)
Persistent=true

Unit=git-sync.service

[Install]
WantedBy=timers.target
TIMEREOF

# systemd/git-sync.env.example
cat > systemd/git-sync.env.example << 'ENVEOF'
GITHUB_TOKEN=ghp_your_github_token_here
ENVEOF

echo "✅ Project structure created successfully!"
echo ""
echo "📍 Location: $(pwd)"
echo ""
echo "Next steps:"
echo "1. Review and customize files in: $(pwd)"
echo "2. Update CONFIG in scripts/sync.py with your GitHub username"
echo "3. Create ~/sync-repos.json with your repositories"
echo "4. Follow the documentation in docs/"
echo ""
echo "To get started:"
echo "  cd $(pwd)"
echo "  cat README.md"
