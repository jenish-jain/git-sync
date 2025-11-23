#!/usr/bin/env python3
"""
Git Repository Sync Script
Syncs repositories between GitHub and local Git server
With automatic workspace cleanup and log rotation

Author: Jenish Jain
License: MIT
"""

import subprocess
import json
import os
import sys
import logging
import shutil
from pathlib import Path
from typing import List, Dict
from datetime import datetime, timedelta

# Configuration - UPDATE THIS
CONFIG = {
    "github_token": os.environ.get("GITHUB_TOKEN", ""),
    "github_username": "YOUR_GITHUB_USERNAME",  # ⚠️ CHANGE THIS
    "repos_config": os.path.expanduser("~/sync-repos.json"),
    "work_dir": os.path.expanduser("~/sync-workspace"),
    "bare_repos_dir": os.path.expanduser("~/repositories"),
    "log_file": os.path.expanduser("~/git-sync.log"),
    "cleanup_workspace": True,  # Clean workspace after sync
    "log_retention_days": 7     # Keep logs for 7 days
}

# Setup logging with rotation
class LogRotationHandler(logging.FileHandler):
    """Custom handler that rotates logs based on age"""
    def __init__(self, filename, retention_days=7):
        super().__init__(filename, mode='a')
        self.retention_days = retention_days
        self.rotate_logs()
    
    def rotate_logs(self):
        """Remove old log entries"""
        log_file = Path(self.baseFilename)
        if not log_file.exists():
            return
        
        try:
            # Read existing logs
            with open(log_file, 'r') as f:
                lines = f.readlines()
            
            # Filter logs newer than retention period
            cutoff_date = datetime.now() - timedelta(days=self.retention_days)
            new_lines = []
            
            for line in lines:
                # Try to parse timestamp from log line
                try:
                    # Format: 2025-11-23 10:15:30,123 - INFO - ...
                    timestamp_str = line.split(' - ')[0]
                    log_date = datetime.strptime(timestamp_str.split(',')[0], '%Y-%m-%d %H:%M:%S')
                    if log_date > cutoff_date:
                        new_lines.append(line)
                except (ValueError, IndexError):
                    # Keep lines without proper timestamp
                    new_lines.append(line)
            
            # Write back filtered logs
            if len(new_lines) < len(lines):
                with open(log_file, 'w') as f:
                    f.writelines(new_lines)
                removed = len(lines) - len(new_lines)
                print(f"Rotated logs: removed {removed} old entries")
        except Exception as e:
            print(f"Log rotation failed: {e}")

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        LogRotationHandler(CONFIG["log_file"], CONFIG["log_retention_days"]),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class GitSyncManager:
    def __init__(self, config: Dict):
        self.config = config
        self.work_dir = Path(config["work_dir"])
        self.bare_repos_dir = Path(config["bare_repos_dir"])
        self.work_dir.mkdir(parents=True, exist_ok=True)
        self.bare_repos_dir.mkdir(parents=True, exist_ok=True)
        
    def run_command(self, cmd: List[str], cwd: str = None, env: dict = None) -> tuple:
        """Run shell command and return output"""
        try:
            command_env = os.environ.copy()
            if env:
                command_env.update(env)
            
            result = subprocess.run(
                cmd,
                cwd=cwd or self.work_dir,
                capture_output=True,
                text=True,
                timeout=300,
                env=command_env
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            logger.error(f"Command timed out: {' '.join(cmd)}")
            return -1, "", "Command timed out"
        except Exception as e:
            logger.error(f"Command failed: {e}")
            return -1, "", str(e)
    
    def load_repos_config(self) -> List[Dict]:
        """Load repository configuration from JSON file"""
        try:
            with open(self.config["repos_config"], 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Config file not found: {self.config['repos_config']}")
            return []
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in config file: {e}")
            return []
    
    def ensure_bare_repo_exists(self, repo_name: str) -> bool:
        """Create bare repository if it doesn't exist"""
        bare_repo_path = self.bare_repos_dir / f"{repo_name}.git"
        
        if bare_repo_path.exists():
            logger.debug(f"Bare repository already exists: {repo_name}.git")
            return True
        
        logger.info(f"Creating bare repository: {repo_name}.git")
        returncode, stdout, stderr = self.run_command(
            ["git", "init", "--bare", f"{repo_name}.git"],
            cwd=self.bare_repos_dir
        )
        
        if returncode != 0:
            logger.error(f"Failed to create bare repository {repo_name}.git: {stderr}")
            return False
        
        logger.info(f"Successfully created bare repository: {repo_name}.git")
        return True
    
    def update_remote_url(self, repo_name: str, github_url: str, local_url: str) -> bool:
        """Update remote URLs to ensure they have the token"""
        repo_path = self.work_dir / repo_name
        
        if not repo_path.exists():
            return False
        
        logger.debug(f"Updating remote URLs for {repo_name}")
        
        self.run_command(
            ["git", "remote", "set-url", "github", github_url],
            cwd=repo_path
        )
        
        self.run_command(
            ["git", "remote", "set-url", "local", local_url],
            cwd=repo_path
        )
        
        return True
    
    def clone_or_update_repo(self, repo_name: str, github_url: str, local_url: str) -> bool:
        """Clone repository or update if exists"""
        repo_path = self.work_dir / repo_name
        
        if repo_path.exists():
            logger.info(f"Updating existing mirror repo: {repo_name}")
            
            # Check if it's a bare repository
            returncode, stdout, stderr = self.run_command(
                ["git", "rev-parse", "--is-bare-repository"],
                cwd=repo_path
            )
            
            is_bare = stdout.strip() == "true"
            
            if not is_bare:
                logger.warning(f"{repo_name} is not a bare repository, removing and re-cloning...")
                shutil.rmtree(repo_path)
                return self.clone_or_update_repo(repo_name, github_url, local_url)
            
            self.update_remote_url(repo_name, github_url, local_url)
            
            env = {"GIT_TERMINAL_PROMPT": "0"}
            
            self.run_command(["git", "fetch", "github", "--prune"], cwd=repo_path, env=env)
            self.run_command(["git", "fetch", "local", "--prune"], cwd=repo_path, env=env)
        else:
            logger.info(f"Cloning new bare mirror repo: {repo_name}")
            
            env = {"GIT_TERMINAL_PROMPT": "0"}
            
            returncode, stdout, stderr = self.run_command(
                ["git", "clone", "--bare", github_url, repo_name],
                env=env
            )
            
            if returncode != 0:
                logger.error(f"Failed to clone {repo_name}: {stderr}")
                return False
            
            self.run_command(
                ["git", "remote", "add", "local", local_url],
                cwd=repo_path
            )
            
            self.run_command(
                ["git", "remote", "rename", "origin", "github"],
                cwd=repo_path
            )
        
        return True
    
    def sync_repo(self, repo_name: str) -> bool:
        """Sync repository between GitHub and local Git server"""
        repo_path = self.work_dir / repo_name
        
        if not repo_path.exists():
            logger.error(f"Repository not found: {repo_name}")
            return False
        
        logger.info(f"Syncing {repo_name}...")
        
        env = {"GIT_TERMINAL_PROMPT": "0"}
        
        returncode, stdout, stderr = self.run_command(
            ["git", "fetch", "github", "--prune"], 
            cwd=repo_path,
            env=env
        )
        if returncode != 0:
            logger.error(f"Failed to fetch from github: {stderr}")
            return False
        
        self.run_command(["git", "fetch", "local", "--prune"], cwd=repo_path, env=env)
        
        logger.info(f"Pushing to local Git server...")
        returncode, stdout, stderr = self.run_command(
            ["git", "push", "local", "--mirror"],
            cwd=repo_path,
            env=env
        )
        
        if returncode != 0:
            logger.error(f"Failed to push to local: {stderr}")
            return False
        
        logger.info(f"Pushing to GitHub...")
        returncode, stdout, stderr = self.run_command(
            ["git", "push", "github", "--mirror"],
            cwd=repo_path,
            env=env
        )
        
        if returncode != 0:
            logger.error(f"Failed to push to GitHub: {stderr}")
            return False
        
        logger.info(f"✓ Successfully synced {repo_name}")
        return True
    
    def cleanup_workspace(self):
        """Clean up sync workspace to save disk space"""
        if not self.config.get("cleanup_workspace", False):
            logger.info("Workspace cleanup disabled")
            return
        
        logger.info("Cleaning up sync workspace...")
        
        if not self.work_dir.exists():
            logger.info("Workspace already clean")
            return
        
        try:
            # Calculate space before cleanup
            workspace_size = sum(f.stat().st_size for f in self.work_dir.rglob('*') if f.is_file())
            workspace_size_mb = workspace_size / (1024 * 1024)
            
            # Remove workspace
            shutil.rmtree(self.work_dir)
            
            logger.info(f"✓ Cleaned up workspace (freed {workspace_size_mb:.2f} MB)")
        except Exception as e:
            logger.error(f"Failed to cleanup workspace: {e}")
    
    def get_disk_usage_stats(self) -> Dict:
        """Get disk usage statistics"""
        stats = {}
        
        try:
            if self.bare_repos_dir.exists():
                bare_size = sum(f.stat().st_size for f in self.bare_repos_dir.rglob('*') if f.is_file())
                stats['bare_repos_mb'] = bare_size / (1024 * 1024)
            
            if self.work_dir.exists():
                work_size = sum(f.stat().st_size for f in self.work_dir.rglob('*') if f.is_file())
                stats['workspace_mb'] = work_size / (1024 * 1024)
            else:
                stats['workspace_mb'] = 0
            
            stats['total_mb'] = stats.get('bare_repos_mb', 0) + stats.get('workspace_mb', 0)
        except Exception as e:
            logger.warning(f"Could not calculate disk usage: {e}")
        
        return stats
    
    def sync_all(self):
        """Sync all configured repositories"""
        repos = self.load_repos_config()
        
        if not repos:
            logger.warning("No repositories configured")
            return
        
        if not self.config["github_token"]:
            logger.error("GITHUB_TOKEN not set! Please set it as an environment variable.")
            logger.error("Run: export GITHUB_TOKEN='your_token_here'")
            return
        
        # Get initial disk usage
        initial_stats = self.get_disk_usage_stats()
        if initial_stats:
            logger.info(f"Initial disk usage: {initial_stats.get('total_mb', 0):.2f} MB")
        
        logger.info(f"Starting sync for {len(repos)} repositories")
        success_count = 0
        fail_count = 0
        
        for repo in repos:
            repo_name = repo["name"]
            
            github_url = f"https://{self.config['github_token']}@github.com/{self.config['github_username']}/{repo_name}.git"
            local_url = f"{self.bare_repos_dir}/{repo_name}.git"
            
            try:
                if not self.ensure_bare_repo_exists(repo_name):
                    logger.error(f"Failed to ensure bare repo exists: {repo_name}")
                    fail_count += 1
                    continue
                
                if self.clone_or_update_repo(repo_name, github_url, local_url):
                    if self.sync_repo(repo_name):
                        success_count += 1
                    else:
                        fail_count += 1
                else:
                    fail_count += 1
            except Exception as e:
                logger.error(f"Error syncing {repo_name}: {e}")
                fail_count += 1
        
        logger.info(f"Sync complete: {success_count} successful, {fail_count} failed")
        
        # Clean up workspace
        self.cleanup_workspace()
        
        # Get final disk usage
        final_stats = self.get_disk_usage_stats()
        if final_stats:
            logger.info(f"Final disk usage: {final_stats.get('total_mb', 0):.2f} MB")
            if initial_stats:
                saved = initial_stats.get('total_mb', 0) - final_stats.get('total_mb', 0)
                if saved > 0:
                    logger.info(f"💾 Saved {saved:.2f} MB by cleaning workspace")


def main():
    logger.info("="*50)
    logger.info("Git Sync Process Started")
    logger.info("="*50)
    
    sync_manager = GitSyncManager(CONFIG)
    sync_manager.sync_all()
    
    logger.info("Git Sync Process Completed")
    logger.info("="*50)


if __name__ == "__main__":
    main()
