# Git Sync - Automatic GitHub to Raspberry Pi Sync

Turn your Raspberry Pi into a private Git server that automatically mirrors your GitHub repositories.

## What is This?

Git Sync creates a **local Git server** on your Raspberry Pi that stays in sync with your GitHub repositories. Think of it as your personal GitHub backup that runs on your home network.

**Why use it?**
- 🔒 **Privacy**: Keep your code on hardware you own
- 💾 **Backup**: Automatic protection against GitHub outages or account issues
- ⚡ **Speed**: Clone/push to your local network (no internet needed)
- 🏠 **Self-hosted**: Full control over your Git infrastructure
- 💰 **Free**: No monthly fees, unlimited private repos

**How it works:**
1. Runs on your Raspberry Pi as a background service
2. Syncs with GitHub every hour (configurable)
3. Creates bare Git repositories you can clone from
4. Bidirectional sync: changes on GitHub → Pi, changes on Pi → GitHub
5. Automatic cleanup saves 50% disk space with log rotation

## 🚀 One-Line Install

```bash
curl -fsSL https://raw.githubusercontent.com/jenish-jain/git-sync/master/install.sh | bash
```

**That's it!** The installer will:
- ✅ Install the sync script and configure systemd
- ✅ Set up log rotation (7-day retention)
- ✅ Prompt for your GitHub username and token
- ✅ Start syncing automatically every hour
- ✅ Create `~/repositories/` for your Git server

## Prerequisites

- Raspberry Pi with Raspbian/Raspberry Pi OS
- Python 3 and Git (pre-installed on Pi OS)
- GitHub Personal Access Token ([get one here](https://github.com/settings/tokens))
  - Required scope: `repo` (full control of private repositories)

## Quick Start

### 1. Configure Repositories

After installation, edit `~/sync-repos.json` to add your repositories:

```bash
nano ~/sync-repos.json
```

```json
[
  {"name": "my-project"},
  {"name": "website"},
  {"name": "scripts"}
]
```

### 2. Verify It's Running

```bash
# Check timer status (should show "active")
sudo systemctl status git-sync.timer

# View recent sync logs
sudo journalctl -u git-sync.service -n 50
```

### 3. Clone from Your Pi

Once synced, clone repositories from your Pi on any device on your network:

```bash
# From your laptop/desktop
git clone pi@raspberrypi.local:repositories/my-project.git

# Or using IP address
git clone pi@192.168.1.100:repositories/my-project.git
```

**Pro tip:** Set up SSH config (`~/.ssh/config`) for easier access:
```
Host pi
    HostName raspberrypi.local
    User pi
```

Then simply: `git clone pi:repositories/my-project.git`

## What Gets Installed

The one-line installer sets up:
- **`/opt/git-sync/sync.py`** - Main sync script
- **`~/sync-repos.json`** - Repository configuration
- **`~/repositories/`** - Your Git server (bare repos)
- **Systemd service + timer** - Runs sync every hour
- **Log rotation** - Keeps logs for 7 days, max 100 MB

## Configuration

### Change Sync Frequency

```bash
# Edit timer configuration
sudo nano /etc/systemd/system/git-sync.timer

# Change OnUnitActiveSec to:
OnUnitActiveSec=30min  # Every 30 minutes
OnUnitActiveSec=6h     # Every 6 hours
OnCalendar=*-*-* 02:00:00  # Daily at 2 AM

# Apply changes
sudo systemctl daemon-reload
sudo systemctl restart git-sync.timer
```

### Update GitHub Token

```bash
# Edit token file
echo 'GITHUB_TOKEN=your_new_token' | sudo tee /etc/systemd/system/git-sync.env
sudo chmod 600 /etc/systemd/system/git-sync.env

# Restart service
sudo systemctl restart git-sync.service
```

### Disable Workspace Cleanup (Optional)

If you have lots of disk space and want faster syncs:

```bash
sudo nano /opt/git-sync/sync.py
# Change line 29: "cleanup_workspace": False

sudo systemctl restart git-sync.service
```

## Common Commands

### Manual Sync

```bash
# Trigger sync now (runs in background)
sudo systemctl start --no-block git-sync.service

# Check if sync is currently running
sudo systemctl is-active git-sync.service
```

### View Logs

```bash
# Recent logs
sudo journalctl -u git-sync.service -n 50

# Follow logs in real-time
sudo journalctl -u git-sync.service -f

# Application log
tail -f ~/git-sync.log
```

### Add New Repository

```bash
# 1. Edit config
nano ~/sync-repos.json
# Add: {"name": "new-repo"}

# 2. Trigger sync
sudo systemctl start --no-block git-sync.service
```

### Service Control

```bash
# Stop syncing
sudo systemctl stop git-sync.timer

# Start syncing
sudo systemctl start git-sync.timer

# Check status
sudo systemctl status git-sync.timer
```

## Monitoring

### Check Disk Usage

```bash
# Repository storage
du -sh ~/repositories/

# Log size
sudo journalctl --disk-usage
```

### Clean Old Logs

```bash
# Clean systemd journal (automatic, but can run manually)
sudo journalctl --vacuum-time=7d
```

## Troubleshooting

### Service Not Running

```bash
sudo systemctl status git-sync.timer
sudo journalctl -u git-sync.service -n 50
```

### Authentication Failed

```bash
# Update GitHub token
echo 'GITHUB_TOKEN=your_new_token' | sudo tee /etc/systemd/system/git-sync.env
sudo chmod 600 /etc/systemd/system/git-sync.env
sudo systemctl restart git-sync.service
```

### Permission Errors

```bash
sudo chown -R $USER:$USER ~/repositories
```

### Out of Disk Space

```bash
# Remove workspace manually
rm -rf ~/sync-workspace/

# Clean old logs
sudo journalctl --vacuum-size=50M
```

## How It Works

Each sync cycle:
1. Creates temporary mirror repos in `~/sync-workspace/`
2. Fetches changes from GitHub and local repos
3. Pushes changes bidirectionally (GitHub ↔ Pi)
4. Deletes `~/sync-workspace/` to save disk space
5. Repeats every hour

**Disk space:** ~2.5 GB (only bare repos kept, workspace deleted)
**Sync time:** 30 seconds - 2 minutes (first sync takes longer)
**Logs:** Auto-rotated, 7-day retention, 100 MB max

## Advanced

### Auto-Generate Repository List

```bash
export GITHUB_TOKEN="your_token"
bash generate-git-sync-project.sh
```

This creates `~/sync-repos.json` with all your GitHub repos (excludes forks and archived).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - Free to use, modify, and distribute.

## Author

**Jenish Jain**
- GitHub: [@jenish-jain](https://github.com/jenish-jain)

---

**Version**: 1.1.0 (with log rotation and cleanup)
**Last Updated**: 2025-11-23

**Happy syncing! 🚀**
