# Git Sync - Download Package

## 📦 What's Included

### 1. `git-sync-complete.tar.gz` (Main Package)
Complete Git Sync system with all scripts, configurations, and documentation.

**Contains:**
- Main sync script (`sync.py`)
- Automated setup script
- Configuration examples
- Systemd service files
- Status monitoring tools
- LICENSE and README

**Size:** ~8 KB

### 2. `QUICKSTART.md` (This File's Companion)
Step-by-step guide to get running in 5 minutes.

### 3. `generate-git-sync-project.sh` (Alternative)
Script to regenerate the entire project structure if needed.

## 🚀 Quick Installation

### On Your Raspberry Pi:

```bash
# 1. Download and extract
tar -xzf git-sync-complete.tar.gz
cd git-sync

# 2. Run setup (will prompt for GitHub token)
chmod +x scripts/setup.sh
./scripts/setup.sh

# 3. Configure repos
nano ~/sync-repos.json

# 4. Update username
nano /opt/git-sync/sync.py
# Change: "github_username": "YOUR_GITHUB_USERNAME"

# 5. Test
python3 /opt/git-sync/sync.py

#  6. Check status
git-sync-status.sh
```

## 📖 Documentation

**Quick Start**: Read `QUICKSTART.md` for immediate setup instructions.

**Full Documentation**: Available online at:
https://github.com/jenishjain/git-sync/tree/main/docs

### Documentation Guides:
1. Raspberry Pi Setup
2. Git Server Setup
3. Script Installation
4. Systemd Configuration
5. Usage Guide
6. Troubleshooting

## ⚙️ What Gets Installed

After running `setup.sh`:

- **Script**: `/opt/git-sync/sync.py`
- **Config**: `~/sync-repos.json`
- **Repos**: `~/repositories/` (bare Git repositories)
- **Workspace**: `~/sync-workspace/` (sync mirrors)
- **Service**: `/etc/systemd/system/git-sync.service`
- **Timer**: `/etc/systemd/system/git-sync.timer`
- **Token**: `/etc/systemd/system/git-sync.env`
- **Status Tool**: `/usr/local/bin/git-sync-status.sh`

## 🔑 GitHub Token

Get your token from: https://github.com/settings/tokens

**Required scope:** `repo` (full control of private repositories)

The setup script will prompt for your token and configure it securely.

## ✅ Verification

After setup, verify everything works:

```bash
# Check service status
sudo systemctl status git-sync.timer
sudo systemctl status git-sync.service

# View dashboard
git-sync-status.sh

# Check logs
sudo journalctl -u git-sync.service -n 20

# List synced repos
ls ~/repositories/
```

## 🔧 Common Tasks

### Add Repository
```bash
nano ~/sync-repos.json  # Add {"name": "new-repo"}
sudo systemctl start git-sync.service
```

### Change Sync Frequency
```bash
sudo nano /etc/systemd/system/git-sync.timer
# Change: OnUnitActiveSec=30min
sudo systemctl daemon-reload
sudo systemctl restart git-sync.timer
```

### Clone from Pi
```bash
git clone your-user@pi-ip:repositories/repo-name.git
```

### View Logs
```bash
sudo journalctl -u git-sync.service -f
```

## 🆘 Troubleshooting

### Quick Fixes

**Service not running:**
```bash
sudo systemctl status git-sync.service
sudo journalctl -u git-sync.service -n 50
```

**Auth failed:**
```bash
sudo nano /etc/systemd/system/git-sync.env
# Update token
sudo systemctl restart git-sync.service
```

**Permission errors:**
```bash
sudo chown -R $USER:$USER ~/repositories
sudo chown -R $USER:$USER ~/sync-workspace
```

## 📊 Features

- ✅ Automatic bidirectional sync (GitHub ↔ Pi)
- ✅ Runs every hour (customizable)
- ✅ Auto-creates bare repositories
- ✅ Comprehensive logging
- ✅ Status monitoring dashboard
- ✅ Secure token management
- ✅ Easy setup and maintenance

## 🔒 Security

- GitHub token stored in secured file (`/etc/systemd/system/git-sync.env`)
- Service runs as your user (not root)
- SSH key authentication supported
- No passwords stored in plain text

## 📝 Project Structure

```
git-sync/
├── README.md              # Main documentation
├── LICENSE               # MIT License
├── scripts/
│   ├── sync.py           # Main sync script ⭐
│   ├── setup.sh          # Automated setup ⭐
│   ├── generate-config.py # Auto-generate repo list
│   └── git-sync-status.sh # Status dashboard
├── config/
│   ├── sync-repos.example.json  # Example config
│   └── README.md         # Config docs
├── systemd/
│   ├── git-sync.service  # Systemd service
│   ├── git-sync.timer    # Systemd timer
│   └── git-sync.env.example # Env template
└── docs/
    ├── README.md         # Docs index
    └── FULL-DOCUMENTATION.md # Link to guides
```

## 🌐 Online Resources

- **Repository**: https://github.com/jenishjain/git-sync
- **Documentation**: https://github.com/jenishjain/git-sync/tree/main/docs
- **Issues**: https://github.com/jenishjain/git-sync/issues
- **GitHub Tokens**: https://github.com/settings/tokens

## 📞 Support

1. Check `QUICKSTART.md`
2. Review logs: `sudo journalctl -u git-sync.service -f`
3. Run status check: `git-sync-status.sh`
4. Check online documentation
5. Open GitHub issue

## 🎯 Use Cases

- **Backup**: Automatic GitHub backup to your Pi
- **Redundancy**: Protection against GitHub outages
- **Local Development**: Fast local Git server
- **Learning**: Understand Git server operations
- **Privacy**: Keep copies of your code locally

## ⚖️ License

MIT License - Free to use, modify, and distribute.

## 👤 Author

**Jenish Jain**
- GitHub: [@jenishjain](https://github.com/jenishjain)

---

**Ready to get started?** Read `QUICKSTART.md` and extract `git-sync-complete.tar.gz`!
