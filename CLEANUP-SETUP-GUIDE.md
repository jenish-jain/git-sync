# Git Sync with Cleanup & Log Rotation - Setup Guide

## What's New

### ✅ Workspace Cleanup
- Automatically deletes `~/sync-workspace/` after each sync
- **Saves ~50% disk space**
- Workspace recreated on next sync (slightly slower first run)

### ✅ Log Rotation
- Keeps logs for only 7 days
- Limits log disk usage to 100 MB
- Automatically rotates old entries

## Setup Instructions

### Step 1: Update the Sync Script

```bash
# Backup existing script
sudo cp /opt/git-sync/sync.py /opt/git-sync/sync.py.backup

# Copy new script with cleanup
sudo cp sync-with-cleanup.py /opt/git-sync/sync.py

# Update GitHub username
sudo nano /opt/git-sync/sync.py
# Change: "github_username": "YOUR_GITHUB_USERNAME"

# Set permissions
sudo chmod +x /opt/git-sync/sync.py
```

### Step 2: Setup Log Rotation

```bash
# Run log rotation setup
chmod +x setup-log-rotation.sh
./setup-log-rotation.sh
```

### Step 3: Test the Changes

```bash
# Test manual sync
export GITHUB_TOKEN="your_token"
python3 /opt/git-sync/sync.py

# You should see:
# - Sync process runs normally
# - "Cleaning up sync workspace..." message
# - "Saved X MB by cleaning workspace" message
# - ~/sync-workspace/ is deleted after completion
```

### Step 4: Verify Workspace Cleanup

```bash
# Check if workspace exists (should NOT exist after sync)
ls ~/sync-workspace/
# Output: ls: cannot access '/home/jenishjain/sync-workspace/': No such file or directory

# Check disk usage
du -sh ~/repositories/
# This is your only Git storage now!
```

### Step 5: Restart Systemd Service

```bash
# Reload and restart
sudo systemctl daemon-reload
sudo systemctl restart git-sync.service

# Check status
sudo systemctl status git-sync.service

# View logs
sudo journalctl -u git-sync.service -n 50
```

## Configuration Options

### Disable Workspace Cleanup (if needed)

Edit `/opt/git-sync/sync.py`:

```python
CONFIG = {
    # ...
    "cleanup_workspace": False,  # Change to False to disable cleanup
    "log_retention_days": 7
}
```

### Change Log Retention Period

Edit `/opt/git-sync/sync.py`:

```python
CONFIG = {
    # ...
    "cleanup_workspace": True,
    "log_retention_days": 14  # Keep logs for 14 days instead of 7
}
```

Or edit systemd journal config:

```bash
sudo nano /etc/systemd/journald.conf.d/git-sync.conf

# Change:
MaxRetentionSec=14day  # Instead of 7day
```

Then restart:
```bash
sudo systemctl restart systemd-journald
```

## Disk Space Comparison

### Before Cleanup

```
~/repositories/     2.5 GB  (bare repos)
~/sync-workspace/   2.5 GB  (mirrors)
Total:              5.0 GB
```

### After Cleanup

```
~/repositories/     2.5 GB  (bare repos)
~/sync-workspace/   0 MB    (deleted after sync)
Total:              2.5 GB
```

**You save 50% disk space! 💾**

## Performance Impact

### First Sync After Cleanup
- **Slower** - needs to clone from GitHub
- Takes 2-5 minutes for small repos
- Takes 10-30 minutes for large repos

### Subsequent Syncs (hourly)
- **Fast** - only fetches new changes
- Takes 30 seconds - 2 minutes

### Trade-off
- **More disk space** ✅ (50% savings)
- **Slightly slower syncs** ⚠️ (acceptable for hourly schedule)

## Monitoring

### Check Disk Usage

```bash
# Repositories only
du -sh ~/repositories/

# Check if workspace exists
ls ~/sync-workspace/ 2>/dev/null || echo "Workspace cleaned ✓"

# Total Git storage
du -sh ~/repositories/ ~/sync-workspace/ 2>/dev/null | awk '{sum+=$1} END {print sum " total"}'
```

### Check Log Size

```bash
# Systemd journal
sudo journalctl --disk-usage

# Application log
du -sh ~/git-sync.log

# View old logs being rotated
tail -100 ~/git-sync.log
```

### Monitor Sync Time

Add to script or check logs:

```bash
# Check last sync duration
sudo journalctl -u git-sync.service | grep "Git Sync Process" | tail -2
```

## Troubleshooting

### Sync Taking Too Long

If syncs take more than 10 minutes after cleanup:

**Option 1: Increase timeout**
```bash
sudo nano /etc/systemd/system/git-sync.service

# Change:
TimeoutStartSec=1200  # 20 minutes instead of 10
```

**Option 2: Disable cleanup for large repos**
```bash
sudo nano /opt/git-sync/sync.py

# Change:
"cleanup_workspace": False,
```

### Workspace Not Being Deleted

Check script output:
```bash
sudo journalctl -u git-sync.service -n 100 | grep -i cleanup
```

Should see:
```
Cleaning up sync workspace...
✓ Cleaned up workspace (freed X MB)
```

If not, check permissions:
```bash
ls -la ~/sync-workspace/
# Should be owned by your user
```

### Logs Still Growing

Check journal settings:
```bash
sudo journalctl --verify
journalctl --disk-usage
```

Manually clean:
```bash
sudo journalctl --vacuum-time=7d
sudo journalctl --vacuum-size=100M
```

### Out of Disk Space

Emergency cleanup:
```bash
# Remove workspace manually
rm -rf ~/sync-workspace/

# Clean logs aggressively
sudo journalctl --vacuum-time=1d
sudo journalctl --vacuum-size=50M

# Clean old logs
> ~/git-sync.log

# Run sync
python3 /opt/git-sync/sync.py
```

## Verification Commands

```bash
# 1. Check script has cleanup enabled
grep "cleanup_workspace" /opt/git-sync/sync.py

# 2. Check log rotation is configured
cat /etc/systemd/journald.conf.d/git-sync.conf

# 3. Run test sync
sudo systemctl start git-sync.service

# 4. Verify workspace is deleted
ls ~/sync-workspace/ 2>&1

# 5. Check disk savings
du -sh ~/repositories/ ~/sync-workspace/ 2>/dev/null
```

## Rollback (if needed)

To go back to the original version:

```bash
# Restore backup
sudo cp /opt/git-sync/sync.py.backup /opt/git-sync/sync.py

# Restart service
sudo systemctl restart git-sync.service

# Remove log rotation config
sudo rm /etc/systemd/journald.conf.d/git-sync.conf
sudo systemctl restart systemd-journald
```

## Benefits Summary

✅ **50% less disk usage** (no duplicate sync-workspace)
✅ **Automatic log cleanup** (only 7 days retained)
✅ **Better SD card longevity** (less writing)
✅ **Cleaner system** (no stale workspace data)
⚠️ **Slightly slower syncs** (acceptable for hourly schedule)

## Next Steps

1. ✅ Update sync script
2. ✅ Setup log rotation
3. ✅ Test manual sync
4. ✅ Verify workspace cleanup
5. ✅ Monitor for a few days
6. ✅ Enjoy the extra disk space!

---

**Questions?** Check logs: `sudo journalctl -u git-sync.service -f`
