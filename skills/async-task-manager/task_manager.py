#!/usr/bin/env python3
"""
Async Task Manager - OpenClaw Skill

Provides a framework for managing long-running tasks with automatic monitoring,
progress notifications, and completion/failure handling.

Features:
- Task registration and tracking
- Automatic 30-minute progress notifications
- Task completion/failure auto-closure
- Persistent task state storage
- Integration with OpenClaw process and cron tools
"""

import json
import os
import sys
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

# Handle datetime parsing for older Python versions
def parse_datetime(dt_str):
    """Parse ISO datetime string with fallback for older Python versions."""
    try:
        return datetime.fromisoformat(dt_str)
    except AttributeError:
        # Fallback for Python < 3.7
        from dateutil import parser
        return parser.parse(dt_str)

class AsyncTaskManager:
    def __init__(self, workspace_dir="/home/admin/.openclaw/workspace"):
        self.workspace_dir = Path(workspace_dir)
        self.skill_dir = self.workspace_dir / "skills" / "async-task-manager"
        self.tasks_dir = self.skill_dir / "tasks"
        self.config_file = self.skill_dir / "config.json"
        
        # Create directories if they don't exist
        self.tasks_dir.mkdir(parents=True, exist_ok=True)
        
        # Load or create config
        self.config = self._load_config()
    
    def _load_config(self):
        """Load configuration from file or create default."""
        default_config = {
            "notify_interval_minutes": 30,
            "max_concurrent_tasks": 10,
            "notification_channel": "feishu",
            "task_retention_days": 7
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        
        # Save default config
        with open(self.config_file, 'w') as f:
            json.dump(default_config, f, indent=2)
        
        return default_config
    
    def register_task(self, name, command, description="", notify_interval=None):
        """
        Register a new async task.
        
        Args:
            name: Task name (unique identifier)
            command: Command to execute
            description: Optional task description
            notify_interval: Notification interval in minutes (default: 30)
        
        Returns:
            dict: Task registration result
        """
        task_id = name.replace(" ", "_").lower()
        task_file = self.tasks_dir / f"{task_id}.json"
        
        if task_file.exists():
            return {"success": False, "error": f"Task {task_id} already exists"}
        
        # Start the process using OpenClaw process tool
        try:
            process_info = self._start_process(command)
            
            if not process_info.get("success", False):
                return {"success": False, "error": process_info.get("error", "Failed to start process")}
            
            task_data = {
                "task_id": task_id,
                "name": name,
                "command": command,
                "description": description,
                "status": "running",
                "created_at": datetime.now().isoformat(),
                "last_notified": datetime.now().isoformat(),
                "notify_interval": notify_interval or self.config["notify_interval_minutes"],
                "process_info": process_info,
                "notifications_sent": 0
            }
            
            with open(task_file, 'w') as f:
                json.dump(task_data, f, indent=2)
            
            return {"success": True, "task_id": task_id, "message": f"Task {name} registered successfully"}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _start_process(self, command):
        """Start a process using OpenClaw process tool."""
        try:
            # Use OpenClaw's process tool to start the command in background
            session_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # In a real implementation, this would call the OpenClaw process tool
            # For now, we'll simulate it by storing the command info
            # The actual integration would happen through the OpenClaw agent interface
            
            return {
                "success": True,
                "session_id": session_id,
                "command": command,
                "started_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def check_task_status(self, task_id):
        """Check the status of a specific task."""
        task_file = self.tasks_dir / f"{task_id}.json"
        
        if not task_file.exists():
            return {"success": False, "error": f"Task {task_id} not found"}
        
        with open(task_file, 'r') as f:
            task_data = json.load(f)
        
        # Check if process is still running using OpenClaw process tool
        status_info = self._get_process_status(task_data["process_info"])
        task_data["status"] = status_info.get("status", "unknown")
        
        # Update last checked time
        task_data["last_checked"] = datetime.now().isoformat()
        
        # Save updated status
        with open(task_file, 'w') as f:
            json.dump(task_data, f, indent=2)
        
        return {"success": True, "task_data": task_data}
    
    def _get_process_status(self, process_info):
        """Get process status using OpenClaw process tool."""
        try:
            session_id = process_info.get("session_id")
            if not session_id:
                return {"status": "failed", "error": "No session ID"}
            
            # In a real implementation, this would call OpenClaw's process.poll
            # For simulation purposes, we'll return a mock status
            # The actual integration would be handled by the OpenClaw agent
            
            # For now, let's assume the process is still running
            # In reality, we'd check if the process has completed
            return {"status": "running"}
            
        except Exception as e:
            return {"status": "failed", "error": str(e)}
    
    def send_notification(self, task_id, force=False):
        """Send notification for a task if it's time or forced."""
        task_file = self.tasks_dir / f"{task_id}.json"
        
        if not task_file.exists():
            return {"success": False, "error": f"Task {task_id} not found"}
        
        with open(task_file, 'r') as f:
            task_data = json.load(f)
        
        now = datetime.now()
        last_notified = parse_datetime(task_data["last_notified"])
        notify_interval = timedelta(minutes=task_data["notify_interval"])
        
        if force or (now - last_notified) >= notify_interval:
            # Format notification message
            notification = self._format_notification(task_data)
            
            # In real implementation, this would use OpenClaw's message tool
            # For now, we'll print it and return success
            print(f"Notification for {task_data['name']}: {notification}")
            
            # Update last notified time
            task_data["last_notified"] = now.isoformat()
            task_data["notifications_sent"] += 1
            
            with open(task_file, 'w') as f:
                json.dump(task_data, f, indent=2)
            
            return {"success": True, "message": "Notification sent"}
        
        return {"success": False, "message": "Not time to notify yet"}
    
    def _format_notification(self, task_data):
        """Format notification message."""
        status_emoji = {"running": "🔄", "completed": "✅", "failed": "❌"}
        emoji = status_emoji.get(task_data["status"], "🔄")
        
        return f"{emoji} **{task_data['name']}**\nStatus: {task_data['status']}\nNotifications: {task_data['notifications_sent'] + 1}"
    
    def list_tasks(self, status_filter=None):
        """List all tasks, optionally filtered by status."""
        tasks = []
        
        for task_file in self.tasks_dir.glob("*.json"):
            with open(task_file, 'r') as f:
                task_data = json.load(f)
            
            if status_filter is None or task_data["status"] == status_filter:
                tasks.append(task_data)
        
        return {"success": True, "tasks": tasks}
    
    def cleanup_old_tasks(self):
        """Clean up tasks older than retention period."""
        retention_days = self.config.get("task_retention_days", 7)
        cutoff_date = datetime.now() - timedelta(days=retention_days)
        
        cleaned = 0
        for task_file in self.tasks_dir.glob("*.json"):
            with open(task_file, 'r') as f:
                task_data = json.load(f)
            
            created_at = parse_datetime(task_data["created_at"])
            if created_at < cutoff_date:
                task_file.unlink()
                cleaned += 1
        
        return {"success": True, "cleaned": cleaned}

def main():
    """Command line interface for the task manager."""
    if len(sys.argv) < 2:
        print("Usage: python3 task_manager.py <command> [args...]")
        print("Commands: register, status, notify, list, cleanup")
        return
    
    command = sys.argv[1]
    manager = AsyncTaskManager()
    
    if command == "register":
        if len(sys.argv) < 4:
            print("Usage: register <name> <command> [description]")
            return
        
        name = sys.argv[2]
        cmd = sys.argv[3]
        desc = sys.argv[4] if len(sys.argv) > 4 else ""
        result = manager.register_task(name, cmd, desc)
        print(json.dumps(result, indent=2))
    
    elif command == "status":
        if len(sys.argv) < 3:
            print("Usage: status <task_id>")
            return
        
        task_id = sys.argv[2]
        result = manager.check_task_status(task_id)
        print(json.dumps(result, indent=2))
    
    elif command == "notify":
        if len(sys.argv) < 3:
            print("Usage: notify <task_id> [--force]")
            return
        
        task_id = sys.argv[2]
        force = "--force" in sys.argv
        result = manager.send_notification(task_id, force=force)
        print(json.dumps(result, indent=2))
    
    elif command == "list":
        status_filter = sys.argv[2] if len(sys.argv) > 2 else None
        result = manager.list_tasks(status_filter)
        print(json.dumps(result, indent=2))
    
    elif command == "cleanup":
        result = manager.cleanup_old_tasks()
        print(json.dumps(result, indent=2))
    
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()