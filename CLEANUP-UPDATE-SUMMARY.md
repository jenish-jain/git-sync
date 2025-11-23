# Git Sync - Cleanup & Log Rotation Update

## 🎯 What's New

We've updated the Git Sync system with two major improvements:

### 1. ✅ Automatic Workspace Cleanup
- Deletes `~/sync-workspace/` after each sync
- **Saves 50% disk space** (from ~5GB to ~2.5GB for typical setup)
- Workspace recreated automatically on next sync

### 2. ✅ Automatic Log Rotation
- Keeps logs for 7 days only
- Limits systemd journal to 100 MB
- Rotates application logs automatically

## 📦 New Files Available

### Main Update
- **sync-with-cleanup.py** - Updated sync script with cleanup
- **setup-log-rotation.sh** - Log rotation setup script

### Documentation
- **CLEANUP-SETUP-GUIDE.md** - Complete setup instructions
- **QUICK-REFERENCE.txt** - Quick reference card

## 🚀 Quick Installation

```bash
# 1. Backup existing script
sudo cp /opt/git-sync/sync.py /opt/git-sync/sync.py.backup

# 2. Install new script
sudo cp sync-with-cleanup.py /opt/git-sync/sync.py

# 3. Update your GitHub username
sudo nano /opt/git-sync/sync.py
# Change: "github_username": "YOUR_GITHUB_USERNAME"

# 4. Setup log rotation
chmod +x setup-log-rotation.sh
./setup-log-rotation.sh

# 5. Restart service
sudo systemctl restart git-sync.service

# 6. Verify
git-sync-status.sh
```

## 💾 Disk Space Savings

### Before
```
~/repositories/     2.5 GB  (bare repos)
~/sync-workspace/   2.5 GB  (mirrors)
Logs:               0.5 GB  (growing indefinitely)
───────────────────────────
Total:              5.5 GB
```

### After
```
~/repositories/     2.5 GB  (bare repos)
~/sync-workspace/   0 MB    (auto-deleted)
Logs:               100 MB  (max, rotated)
───────────────────────────
Total:              2.6 GB  💾 Saved ~3 GB!
```

## ⚡ Performance Impact

### Before Cleanup
- **Sync time**: 30 seconds - 2 minutes
- **Disk usage**: High (duplicated data)
- **Log growth**: Unlimited

### After Cleanup
- **First sync**: 2-30 minutes (re-clones from GitHub)
- **Subsequent syncs**: 30 seconds - 2 minutes (only fetches changes)
- **Disk usage**: Low (50% reduction)
- **Log growth**: Controlled (7 days max)

**Trade-off**: Slightly slower initial sync is worth the disk space savings!

## 🔧 Configuration Options

### In `/opt/git-sync/sync.py`:

```python
CONFIG = {
    # ...
    "cleanup_workspace": True,   # Enable/disable cleanup
    "log_retention_days": 7      # Keep logs for X days
}
```

### Disable Cleanup (if needed)
```bash
sudo nano /opt/git-sync/sync.py
# Change: "cleanup_workspace": False
sudo systemctl restart git-sync.service
```

### Change Log Retention
```bash
sudo nano /opt/git-sync/sync.py
# Change: "log_retention_days": 14  # Keep for 14 days
sudo systemctl restart git-sync.service
```

## 📊 How It Works

### Old Workflow
```
GitHub → sync-workspace → repositories
         (stays forever)   (permanent)
```

### New Workflow
```
GitHub → sync-workspace → repositories → [DELETE workspace]
         (temporary)       (permanent)    (save disk space!)
```

### Next Sync
```
GitHub → [RECREATE workspace] → sync → [DELETE again]
         (clones fresh)
```

## ✅ Verification Steps

After installation, verify everything works:

```bash
# 1. Trigger manual sync
sudo systemctl start git-sync.service

# 2. Check logs for cleanup message
sudo journalctl -u git-sync.service | grep -i cleanup

# Should see:
# "Cleaning up sync workspace..."
# "✓ Cleaned up workspace (freed X MB)"
# "💾 Saved X MB by cleaning workspace"

# 3. Verify workspace is deleted
ls ~/sync-workspace/
# Should output: No such file or directory ✓

# 4. Check disk usage
du -sh ~/repositories/
# Should show only repositories size

# 5. Check log size
sudo journalctl --disk-usage
# Should be under 100 MB
```

## 🆘 Troubleshooting

### Workspace Not Deleted

**Check logs:**
```bash
sudo journalctl -u git-sync.service -n 100 | grep -i cleanup
```

**Check permissions:**
```bash
ls -la ~/ | grep sync-workspace
```

**Manual cleanup:**
```bash
rm -rf ~/sync-workspace/
```

### Sync Taking Too Long

**Increase timeout:**
```bash
sudo nano /etc/systemd/system/git-sync.service
# Change: TimeoutStartSec=1200  # 20 minutes
sudo systemctl daemon-reload
sudo systemctl restart git-sync.service
```

**Or disable cleanup:**
```bash
sudo nano /opt/git-sync/sync.py
# Change: "cleanup_workspace": False
```

### Logs Still Growing

**Verify log rotation:**
```bash
cat /etc/systemd/journald.conf.d/git-sync.conf
```

**Manual cleanup:**
```bash
sudo journalctl --vacuum-time=7d
sudo journalctl --vacuum-size=100M
```

## 🔄 Rollback Instructions

If you want to go back to the old version:

```bash
# Restore backup
sudo cp /opt/git-sync/sync.py.backup /opt/git-sync/sync.py

# Restart service
sudo systemctl restart git-sync.service

# Remove log rotation (optional)
sudo rm /etc/systemd/journald.conf.d/git-sync.conf
sudo systemctl restart systemd-journald
```

## 📈 Benefits Summary

| Aspect | Before | After | Improvement |
|--------|--------|-------|-------------|
| Disk Space | ~5 GB | ~2.5 GB | 50% savings |
| Log Size | Unlimited | 100 MB max | Controlled |
| Sync Time | 1-2 min | 1-2 min* | Same |
| SD Card Life | Lower | Higher | Better |
| Reliability | High | High | Same |

*First sync after cleanup takes longer (acceptable for hourly schedule)

## 🎯 Who Should Use This

### ✅ Recommended For:
- Systems with limited disk space (8-16 GB SD cards)
- Users who want cleaner systems
- Long-term deployments
- Systems that run 24/7

### ⚠️ Consider Original Version If:
- You have plenty of disk space (32+ GB)
- You need fastest possible syncs
- You sync very large repos (>1 GB each)
- You prefer stability over optimization

## 📞 Support

**Documentation:**
- Full guide: `CLEANUP-SETUP-GUIDE.md`
- Quick reference: `QUICK-REFERENCE.txt`

**Commands:**
- Status: `git-sync-status.sh`
- Logs: `sudo journalctl -u git-sync.service -f`
- Disk: `du -sh ~/repositories/`

**Resources:**
- GitHub: https://github.com/jenishjain/git-sync
- Issues: https://github.com/jenishjain/git-sync/issues

## 📝 Changelog

### v1.1.0 (2025-11-23)
- ✅ Added automatic workspace cleanup
- ✅ Added log rotation (7 days)
- ✅ Added disk usage tracking
- ✅ Added cleanup statistics in logs
- ✅ Improved error handling
- 📚 Updated documentation

### v1.0.0 (2025-11-23)
- Initial release
- Basic sync functionality
- Systemd integration

---

**Ready to update?** Follow the Quick Installation steps above!
