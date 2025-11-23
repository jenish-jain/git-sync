# Git Sync - Complete Download Package

## 📦 What You Have

This package contains everything you need to set up Git Sync on your Raspberry Pi with two versions:

### Version 1.0 - Original (Basic)
- Standard sync functionality
- Keeps both repositories and workspace
- ~5 GB disk usage

### Version 1.1 - With Cleanup (Recommended)
- Automatic workspace cleanup
- Log rotation (7 days)
- ~2.5 GB disk usage (50% savings!)

## 🚀 Quick Start Guide

### For New Users (Start Here!)

1. **Read this first**: [START_HERE.md](START_HERE.md)
2. **Quick setup**: [QUICKSTART.md](QUICKSTART.md)
3. **Detailed instructions**: [DOWNLOAD_INSTRUCTIONS.txt](DOWNLOAD_INSTRUCTIONS.txt)

### Installation Steps

```bash
# Extract package
tar -xzf git-sync-complete.tar.gz
cd git-sync

# Run setup
chmod +x scripts/setup.sh
./scripts/setup.sh
```

## 🆕 Cleanup & Log Rotation (Recommended)

**Want to save 50% disk space?** Use the updated version with automatic cleanup!

1. **Read update guide**: [CLEANUP-UPDATE-SUMMARY.md](CLEANUP-UPDATE-SUMMARY.md)
2. **Setup instructions**: [CLEANUP-SETUP-GUIDE.md](CLEANUP-SETUP-GUIDE.md)
3. **Quick reference**: [QUICK-REFERENCE.txt](QUICK-REFERENCE.txt)

### Update Steps

```bash
# Install updated script
sudo cp sync-with-cleanup.py /opt/git-sync/sync.py

# Setup log rotation
chmod +x setup-log-rotation.sh
./setup-log-rotation.sh

# Restart
sudo systemctl restart git-sync.service
```

## 📁 Files Reference

### 🎯 Essential Files

| File | Description | When to Use |
|------|-------------|-------------|
| **git-sync-complete.tar.gz** | Main package | First installation |
| **sync-with-cleanup.py** | Updated script | After installation to save space |
| **setup-log-rotation.sh** | Log rotation setup | With cleanup script |

### 📖 Documentation

| File | Description | Audience |
|------|-------------|----------|
| **START_HERE.md** | Master index | Everyone |
| **QUICKSTART.md** | 5-minute guide | Quick setup |
| **README.md** | Package overview | General info |
| **DOWNLOAD_INSTRUCTIONS.txt** | Comprehensive guide | Detailed setup |
| **CLEANUP-UPDATE-SUMMARY.md** | Update overview | Upgrading users |
| **CLEANUP-SETUP-GUIDE.md** | Cleanup instructions | Detailed update guide |
| **QUICK-REFERENCE.txt** | Command reference | Daily use |

### 🔧 Utilities

| File | Description |
|------|-------------|
| **generate-git-sync-project.sh** | Regenerate project |
| **PACKAGE_CONTENTS.txt** | Archive contents list |

## 🎯 Which Version Should I Use?

### Use Version 1.0 (Original) If:
- ✅ You have plenty of disk space (32+ GB SD card)
- ✅ You want fastest syncs
- ✅ You're just testing the system
- ✅ You prefer simplicity

### Use Version 1.1 (Cleanup) If:
- ✅ You have limited disk space (8-16 GB SD card)
- ✅ You want optimal SD card longevity
- ✅ You're running long-term
- ✅ You don't mind slightly slower first syncs

**Recommendation**: Start with 1.0, upgrade to 1.1 after you confirm it works!

## 💾 Disk Space Comparison

| Component | v1.0 | v1.1 | Savings |
|-----------|------|------|---------|
| Repositories | 2.5 GB | 2.5 GB | - |
| Workspace | 2.5 GB | 0 MB | 2.5 GB |
| Logs | Growing | 100 MB max | Variable |
| **Total** | **~5 GB** | **~2.6 GB** | **~2.4 GB (48%)** |

## 🔧 Common Workflows

### Initial Setup

```bash
1. Download git-sync-complete.tar.gz
2. Read START_HERE.md or QUICKSTART.md
3. Extract and run setup.sh
4. Configure repos in ~/sync-repos.json
5. Update username in /opt/git-sync/sync.py
6. Test: python3 /opt/git-sync/sync.py
```

### Upgrade to Cleanup Version

```bash
1. Read CLEANUP-UPDATE-SUMMARY.md
2. Backup: sudo cp /opt/git-sync/sync.py /opt/git-sync/sync.py.backup
3. Install: sudo cp sync-with-cleanup.py /opt/git-sync/sync.py
4. Setup logs: ./setup-log-rotation.sh
5. Restart: sudo systemctl restart git-sync.service
6. Verify: git-sync-status.sh
```

### Daily Operations

```bash
# Check status
git-sync-status.sh

# View logs
sudo journalctl -u git-sync.service -f

# Manual sync
sudo systemctl start git-sync.service

# Check disk usage
du -sh ~/repositories/ ~/sync-workspace/ 2>/dev/null
```

## 📊 Feature Comparison

| Feature | v1.0 | v1.1 |
|---------|------|------|
| Automatic sync | ✅ | ✅ |
| GitHub ↔ Pi bidirectional | ✅ | ✅ |
| Auto-create repos | ✅ | ✅ |
| Systemd service | ✅ | ✅ |
| Status monitoring | ✅ | ✅ |
| Workspace cleanup | ❌ | ✅ |
| Log rotation | ❌ | ✅ |
| Disk usage tracking | ❌ | ✅ |
| Disk space | 5 GB | 2.6 GB |

## 🆘 Getting Help

### Documentation Priority

1. **Quick answer**: Check QUICK-REFERENCE.txt
2. **Setup issues**: Review CLEANUP-SETUP-GUIDE.md or QUICKSTART.md
3. **Comprehensive**: Read DOWNLOAD_INSTRUCTIONS.txt
4. **Online**: Visit https://github.com/jenishjain/git-sync/tree/main/docs

### Common Commands

```bash
# Status
git-sync-status.sh
sudo systemctl status git-sync.service

# Logs
sudo journalctl -u git-sync.service -f
tail -f ~/git-sync.log

# Disk usage
du -sh ~/repositories/
sudo journalctl --disk-usage

# Service control
sudo systemctl start/stop/restart git-sync.timer
```

## 📞 Support Resources

- **GitHub Repository**: https://github.com/jenishjain/git-sync
- **Full Documentation**: https://github.com/jenishjain/git-sync/tree/main/docs
- **Issues/Support**: https://github.com/jenishjain/git-sync/issues
- **GitHub Tokens**: https://github.com/settings/tokens

## ✅ Recommended Reading Order

### For New Users:
1. START_HERE.md ← You are here!
2. QUICKSTART.md
3. Install git-sync-complete.tar.gz
4. Once working, read CLEANUP-UPDATE-SUMMARY.md
5. Upgrade to cleanup version

### For Existing Users:
1. CLEANUP-UPDATE-SUMMARY.md
2. CLEANUP-SETUP-GUIDE.md
3. Install updates
4. Keep QUICK-REFERENCE.txt handy

## 🎉 Ready to Start?

**Complete beginners**: Start with [QUICKSTART.md](QUICKSTART.md)

**Want disk savings**: Read [CLEANUP-UPDATE-SUMMARY.md](CLEANUP-UPDATE-SUMMARY.md)

**Need reference**: Use [QUICK-REFERENCE.txt](QUICK-REFERENCE.txt)

---

**Version**: 1.1.0  
**Last Updated**: 2025-11-23  
**Author**: Jenish Jain  
**License**: MIT  

**Happy syncing! 🚀**
