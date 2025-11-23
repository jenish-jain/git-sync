# Git Sync - Automatic GitHub to Raspberry Pi Sync

Automatically sync your GitHub repositories to your Raspberry Pi as a local Git server with log rotation and automatic cleanup.

## 🚀 One-Line Install

```bash
curl -fsSL https://raw.githubusercontent.com/jenish-jain/git-sync/main/install.sh | bash
```

This will download and set up everything automatically! Or follow the manual installation steps below.

## Features

- ✅ **Automatic bidirectional sync** between GitHub and your Raspberry Pi
- ✅ **Log rotation** - Keeps logs for 7 days (configurable)
- ✅ **Automatic workspace cleanup** - Saves 50% disk space
- ✅ **Hourly synchronization** (customizable)
- ✅ **Auto-creates bare repositories**
- ✅ **Systemd integration** for reliable background operation
- ✅ **Secure token management**
- ✅ **Status monitoring dashboard**

## Disk Space Benefits

### Before Cleanup
```
~/repositories/     2.5 GB  (bare repos)
~/sync-workspace/   2.5 GB  (sync mirrors)
Logs:               Growing indefinitely
───────────────────────────
Total:              ~5.0 GB
```

### After Cleanup (This Version!)
```
~/repositories/     2.5 GB  (bare repos)
~/sync-workspace/   0 MB    (auto-deleted after sync)
Logs:               100 MB max (7-day rotation)
───────────────────────────
Total:              ~2.6 GB  💾 Saved ~2.4 GB!
```

## Quick Start (5 Minutes)

### Prerequisites

1. **Raspberry Pi** with Raspbian/Raspberry Pi OS
2. **GitHub Personal Access Token** - Get it from: https://github.com/settings/tokens
   - Token type: "Personal access token (classic)"
   - Required scope: `repo` (full control of private repositories)
3. **Python 3** (pre-installed on Raspberry Pi OS)
4. **Git** (pre-installed on Raspberry Pi OS)

### Installation

```bash
# 1. Clone this repository
git clone https://github.com/jenishjain/git-sync.git
cd git-sync

# 2. Copy the sync script to system location
sudo mkdir -p /opt/git-sync
sudo cp sync.py /opt/git-sync/
sudo chmod +x /opt/git-sync/sync.py

# 3. Update your GitHub username in the script
sudo nano /opt/git-sync/sync.py
# Change line 24: "github_username": "YOUR_GITHUB_USERNAME"

# 4. Create repository configuration
nano ~/sync-repos.json
```

Add your repositories to `~/sync-repos.json`:
```json
[
  {"name": "repo1"},
  {"name": "repo2"},
  {"name": "your-repo-name"}
]
```

```bash
# 5. Set up log rotation
chmod +x setup-log-rotation.sh
./setup-log-rotation.sh

# 6. Create systemd service file
sudo nano /etc/systemd/system/git-sync.service
```

Paste this configuration:
```ini
[Unit]
Description=Git Sync Service
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
User=YOUR_USERNAME
EnvironmentFile=/etc/systemd/system/git-sync.env
ExecStart=/usr/bin/python3 /opt/git-sync/sync.py
TimeoutStartSec=600

[Install]
WantedBy=multi-user.target
```

Replace `YOUR_USERNAME` with your actual username.

```bash
# 7. Create systemd timer file
sudo nano /etc/systemd/system/git-sync.timer
```

Paste this configuration:
```ini
[Unit]
Description=Git Sync Timer
Requires=git-sync.service

[Timer]
OnBootSec=5min
OnUnitActiveSec=1h
Unit=git-sync.service

[Install]
WantedBy=timers.target
```

```bash
# 8. Create environment file for GitHub token
sudo nano /etc/systemd/system/git-sync.env
```

Add your token:
```
GITHUB_TOKEN=your_github_token_here
```

```bash
# 9. Secure the environment file
sudo chmod 600 /etc/systemd/system/git-sync.env

# 10. Test the sync manually
export GITHUB_TOKEN="your_token_here"
python3 /opt/git-sync/sync.py

# 11. Enable and start the service
sudo systemctl daemon-reload
sudo systemctl enable git-sync.timer
sudo systemctl start git-sync.timer

# 12. Verify it's running
sudo systemctl status git-sync.timer
```

Done! Your repositories will now sync automatically every hour.

## What Gets Installed

- **Script**: `/opt/git-sync/sync.py` - Main sync script
- **Config**: `~/sync-repos.json` - List of repositories to sync
- **Repos**: `~/repositories/` - Bare Git repositories (your Git server)
- **Workspace**: `~/sync-workspace/` - Temporary sync workspace (auto-deleted)
- **Service**: `/etc/systemd/system/git-sync.service` - Systemd service
- **Timer**: `/etc/systemd/system/git-sync.timer` - Hourly timer
- **Token**: `/etc/systemd/system/git-sync.env` - Secure GitHub token storage
- **Logs**: `~/git-sync.log` - Application logs (7-day rotation)

## Configuration

### Main Configuration

Edit `/opt/git-sync/sync.py`:

```python
CONFIG = {
    "github_token": os.environ.get("GITHUB_TOKEN", ""),
    "github_username": "YOUR_GITHUB_USERNAME",  # ⚠️ CHANGE THIS
    "repos_config": os.path.expanduser("~/sync-repos.json"),
    "work_dir": os.path.expanduser("~/sync-workspace"),
    "bare_repos_dir": os.path.expanduser("~/repositories"),
    "log_file": os.path.expanduser("~/git-sync.log"),
    "cleanup_workspace": True,  # Auto-cleanup workspace (recommended)
    "log_retention_days": 7     # Keep logs for 7 days
}
```

### Change Sync Frequency

Edit `/etc/systemd/system/git-sync.timer`:

```ini
# Every hour (default)
OnUnitActiveSec=1h

# Every 30 minutes
OnUnitActiveSec=30min

# Every 6 hours
OnUnitActiveSec=6h

# Daily at 2 AM
OnCalendar=*-*-* 02:00:00
```

Then reload:
```bash
sudo systemctl daemon-reload
sudo systemctl restart git-sync.timer
```

### Disable Workspace Cleanup

If you have plenty of disk space and want faster syncs:

```bash
sudo nano /opt/git-sync/sync.py
# Change: "cleanup_workspace": False
sudo systemctl restart git-sync.service
```

## Daily Usage

### Monitor Sync Status

```bash
# Check service status
sudo systemctl status git-sync.service
sudo systemctl status git-sync.timer

# View recent logs
sudo journalctl -u git-sync.service -n 50

# Follow logs in real-time
sudo journalctl -u git-sync.service -f

# View application log
tail -f ~/git-sync.log
```

### Manual Sync

```bash
# Trigger sync in background (recommended - returns immediately)
sudo systemctl start --no-block git-sync.service

# Or run in foreground (waits until sync completes)
sudo systemctl start git-sync.service

# Test sync with direct command
export GITHUB_TOKEN="your_token"
python3 /opt/git-sync/sync.py

# Check if sync is running
sudo systemctl is-active git-sync.service
```

### Add New Repository

```bash
# Edit config
nano ~/sync-repos.json
# Add: {"name": "new-repo"}

# Trigger sync in background
sudo systemctl start --no-block git-sync.service

# Or wait for next scheduled sync (within 1 hour)
```

### Clone from Your Raspberry Pi

Once synced, you can clone from your Pi over your local network:

```bash
# From another computer on your network
git clone username@raspberry-pi-ip:repositories/repo-name.git

# Example
git clone pi@192.168.1.100:repositories/my-project.git
```

Set up SSH config for easier access (`~/.ssh/config`):
```
Host raspberrypi
    HostName 192.168.1.100
    User pi
    IdentityFile ~/.ssh/id_ed25519
```

Then simply:
```bash
git clone raspberrypi:repositories/my-project.git
```

## Monitoring & Maintenance

### Check Disk Usage

```bash
# Check repository storage
du -sh ~/repositories/

# Check if workspace exists (should not exist after cleanup)
ls ~/sync-workspace/ 2>&1

# Check log size
du -sh ~/git-sync.log
sudo journalctl --disk-usage
```

### Clean Logs Manually

```bash
# Clean systemd journal
sudo journalctl --vacuum-time=7d
sudo journalctl --vacuum-size=100M

# Truncate application log
> ~/git-sync.log
```

## Troubleshooting

### Service Not Running

```bash
# Check status
sudo systemctl status git-sync.service
sudo systemctl status git-sync.timer

# View recent errors
sudo journalctl -u git-sync.service -n 50

# Check if timer is active
sudo systemctl list-timers | grep git-sync
```

### Authentication Failed

```bash
# Verify token
sudo cat /etc/systemd/system/git-sync.env

# Update token
sudo nano /etc/systemd/system/git-sync.env
# Update: GITHUB_TOKEN=your_new_token

# Restart service
sudo systemctl restart git-sync.service
```

### Permission Errors

```bash
# Fix permissions
sudo chown -R $USER:$USER ~/repositories
sudo chown -R $USER:$USER ~/sync-workspace
sudo chmod 755 ~/repositories
```

### Sync Taking Too Long

```bash
# Increase timeout in service file
sudo nano /etc/systemd/system/git-sync.service
# Change: TimeoutStartSec=1200  # 20 minutes

sudo systemctl daemon-reload
sudo systemctl restart git-sync.service
```

### Workspace Not Being Deleted

```bash
# Check cleanup logs
sudo journalctl -u git-sync.service | grep -i cleanup

# Should see:
# "Cleaning up sync workspace..."
# "✓ Cleaned up workspace (freed X MB)"

# Manual cleanup
rm -rf ~/sync-workspace/
```

### Out of Disk Space

```bash
# Emergency cleanup
rm -rf ~/sync-workspace/
sudo journalctl --vacuum-size=50M
> ~/git-sync.log

# Check space
df -h
du -sh ~/repositories/
```

## How It Works

### Sync Workflow

1. **Clone/Update**: Script creates bare mirror repositories in `~/sync-workspace/`
2. **Fetch**: Fetches latest changes from both GitHub and local repositories
3. **Sync**: Pushes changes bidirectionally (GitHub ↔ Local)
4. **Cleanup**: Deletes `~/sync-workspace/` to save disk space
5. **Repeat**: Runs again on next timer trigger (hourly by default)

### Repository Types

- **Bare repositories** (`~/repositories/*.git`): Permanent storage, no working tree
- **Mirror repositories** (`~/sync-workspace/*`): Temporary, used for syncing only

### Log Rotation

- **Application logs**: Rotated based on age (7 days by default)
- **Systemd journal**: Limited to 100 MB with 7-day retention
- **Automatic**: Happens on every sync run

## Performance

### First Sync After Cleanup
- **Time**: 2-30 minutes (needs to re-clone from GitHub)
- **Trade-off**: Worth it for 50% disk space savings

### Subsequent Syncs
- **Time**: 30 seconds - 2 minutes (only fetches new changes)
- **Frequency**: Every hour (default)

## Security

- GitHub token stored in secured file (`/etc/systemd/system/git-sync.env`)
- Service runs as your user (not root)
- SSH key authentication supported for cloning from Pi
- No passwords stored in plain text

## Use Cases

- **Backup**: Automatic GitHub backup to your Raspberry Pi
- **Redundancy**: Protection against GitHub outages
- **Local Development**: Fast local Git server on your network
- **Learning**: Understand Git server operations
- **Privacy**: Keep copies of your code locally
- **Offline Access**: Access your repositories even without internet

## Advanced Usage

### Auto-Generate Repository List

```bash
# Install and run the config generator (requires GitHub token)
export GITHUB_TOKEN="your_token"
python3 generate-git-sync-project.sh
```

This will create `~/sync-repos.json` with all your non-forked, non-archived repositories.

### Multiple GitHub Accounts

Create separate service instances with different usernames and tokens:

```bash
# Copy and modify for second account
sudo cp /etc/systemd/system/git-sync.service /etc/systemd/system/git-sync2.service
sudo cp /etc/systemd/system/git-sync.timer /etc/systemd/system/git-sync2.timer
# Edit files to use different config paths and environment files
```

## Support

- **GitHub Repository**: https://github.com/jenishjain/git-sync
- **Issues/Bugs**: https://github.com/jenishjain/git-sync/issues
- **GitHub Tokens**: https://github.com/settings/tokens

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - Free to use, modify, and distribute.

## Author

**Jenish Jain**
- GitHub: [@jenishjain](https://github.com/jenishjain)

---

**Version**: 1.1.0 (with log rotation and cleanup)
**Last Updated**: 2025-11-23

**Happy syncing! 🚀**
