# Git Sync - Quick Start Guide

## What You Downloaded

`git-sync-complete.tar.gz` - Complete Git Sync project with scripts, configs, and documentation

## Installation (5 minutes)

### On Your Raspberry Pi:

```bash
# 1. Extract the archive
tar -xzf git-sync-complete.tar.gz
cd git-sync

# 2. Run setup script (will prompt for GitHub token)
chmod +x scripts/setup.sh
./scripts/setup.sh

# 3. Edit repository list
nano ~/sync-repos.json
```

Add your repositories:
```json
[
  {"name": "repo1"},
  {"name": "repo2"},
  {"name": "repo3"}
]
```

```bash
# 4. Update your GitHub username in the script
nano /opt/git-sync/sync.py
```

Change line:
```python
"github_username": "YOUR_GITHUB_USERNAME",  # Change this to your username
```

```bash
# 5. Test the sync
python3 /opt/git-sync/sync.py

# 6. Check status
git-sync-status.sh
```

Done! The system will now sync automatically every hour.

## What Was Set Up

- ✅ Git server in `~/repositories/`
- ✅ Sync workspace in `~/sync-workspace/`
- ✅ Systemd service (runs hourly)
- ✅ Scripts installed in `/opt/git-sync/`
- ✅ Status command: `git-sync-status.sh`

## Daily Usage

```bash
# Check sync status
git-sync-status.sh

# Manual sync
sudo systemctl start git-sync.service

# View logs
sudo journalctl -u git-sync.service -f

# Clone from your Pi (from any machine)
git clone your-user@raspberrypi-ip:repositories/repo-name.git
```

## Project Structure

```
git-sync/
├── README.md           # Main documentation
├── LICENSE             # MIT License
├── scripts/
│   ├── sync.py         # Main sync script
│   ├── setup.sh        # Automated setup
│   ├── generate-config.py   # Auto-generate repo list
│   └── git-sync-status.sh   # Status dashboard
├── config/
│   ├── sync-repos.example.json  # Example config
│   └── README.md       # Config documentation
├── systemd/
│   ├── git-sync.service    # Systemd service
│   ├── git-sync.timer      # Systemd timer
│   └── git-sync.env.example # Environment template
└── docs/
    ├── README.md       # Docs index
    └── FULL-DOCUMENTATION.md  # Link to full guides
```

## Getting GitHub Token

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Name it: "Raspberry Pi Git Sync"
4. Select scope: **repo** (full control)
5. Generate and copy token (starts with `ghp_`)

## Common Commands

### Service Management
```bash
# Start/stop/restart
sudo systemctl start git-sync.timer
sudo systemctl stop git-sync.timer
sudo systemctl restart git-sync.timer

# Enable/disable auto-start
sudo systemctl enable git-sync.timer
sudo systemctl disable git-sync.timer

# Check status
sudo systemctl status git-sync.service
sudo systemctl status git-sync.timer
```

### Monitoring
```bash
# Dashboard
git-sync-status.sh

# Live logs
sudo journalctl -u git-sync.service -f

# Recent logs
sudo journalctl -u git-sync.service -n 50

# Errors only
sudo journalctl -u git-sync.service -p err
```

### Repository Management
```bash
# List synced repos
ls ~/repositories/

# Add new repo
nano ~/sync-repos.json  # Add repo name
sudo systemctl start git-sync.service  # Sync

# Check repo size
du -sh ~/repositories/*.git
```

## Customization

### Change Sync Frequency

Edit `/etc/systemd/system/git-sync.timer`:

```ini
# Every hour (default)
OnUnitActiveSec=1h

# Every 30 minutes
OnUnitActiveSec=30min

# Daily at 2 AM
OnCalendar=*-*-* 02:00:00
```

Then reload:
```bash
sudo systemctl daemon-reload
sudo systemctl restart git-sync.timer
```

### Auto-Generate Repository List

```bash
export GITHUB_TOKEN="your_token"
python3 scripts/generate-config.py
```

This will create `~/sync-repos.json` with all your GitHub repos (excluding forks and archived).

## Cloning from Your Pi

### From Local Network

```bash
# Standard format
git clone you@raspberry-pi-ip:/home/you/repositories/repo-name.git

# Example
git clone jenishjain@192.168.1.100:/home/jenishjain/repositories/blog-post.git
```

### Set Up SSH Config

Add to `~/.ssh/config` on your laptop:
```
Host raspberrypi
    HostName 192.168.1.100
    User your-username
    IdentityFile ~/.ssh/id_ed25519
```

Then:
```bash
git clone raspberrypi:repositories/repo-name.git
```

## Troubleshooting

### Service Not Running
```bash
sudo systemctl status git-sync.service
sudo journalctl -u git-sync.service -n 50
```

### Authentication Failed
```bash
# Check token
sudo cat /etc/systemd/system/git-sync.env

# Regenerate if needed at: https://github.com/settings/tokens
sudo nano /etc/systemd/system/git-sync.env
sudo systemctl restart git-sync.service
```

### Permission Errors
```bash
sudo chown -R $USER:$USER ~/repositories
sudo chown -R $USER:$USER ~/sync-workspace
```

### Repos Not Syncing
```bash
# Check config
cat ~/sync-repos.json

# Test manually
export GITHUB_TOKEN="your_token"
python3 /opt/git-sync/sync.py
```

## Full Documentation

For comprehensive guides covering every aspect:

📚 **Online Documentation**: https://github.com/jenishjain/git-sync/tree/main/docs

Includes detailed guides on:
- Raspberry Pi setup
- Git server configuration
- Advanced troubleshooting
- Performance optimization
- Security hardening

## Support

- **Issues**: https://github.com/jenishjain/git-sync/issues
- **Logs**: `sudo journalctl -u git-sync.service -f`
- **Status**: `git-sync-status.sh`

## Next Steps

1. ✅ Complete the quick start above
2. 📖 Review full documentation for advanced features
3. 🔐 Set up SSH keys for passwordless access
4. 📊 Monitor with `git-sync-status.sh`
5. 🔄 Enjoy automatic backups!

---

**Author**: Jenish Jain  
**License**: MIT  
**Repository**: https://github.com/jenishjain/git-sync
