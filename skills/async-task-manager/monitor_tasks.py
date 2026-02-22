#!/usr/bin/env python3
"""
Task Monitor Script - Automatically checks all running tasks and sends notifications
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from task_manager import AsyncTaskManager

def main():
    """Main monitoring function."""
    manager = AsyncTaskManager()
    
    # Get all running tasks
    result = manager.list_tasks(status_filter="running")
    
    if not result["success"]:
        print(f"Error listing tasks: {result.get('error', 'Unknown error')}")
        return
    
    tasks = result["tasks"]
    print(f"Found {len(tasks)} running tasks to monitor")
    
    for task in tasks:
        task_id = task["task_id"]
        
        # Check task status
        status_result = manager.check_task_status(task_id)
        if not status_result["success"]:
            print(f"Error checking status for {task_id}: {status_result.get('error', 'Unknown error')}")
            continue
        
        updated_task = status_result["task_data"]
        status = updated_task["status"]
        
        # Send notification if needed
        if status == "running":
            notify_result = manager.send_notification(task_id)
            if notify_result["success"]:
                print(f"Sent notification for {task_id}")
            else:
                print(f"No notification needed for {task_id}")
        elif status in ["completed", "failed"]:
            # Send final notification for completed/failed tasks
            notify_result = manager.send_notification(task_id, force=True)
            if notify_result["success"]:
                print(f"Sent final notification for {task_id}")
            
            # Clean up completed/failed tasks after sending notification
            task_file = manager.tasks_dir / f"{task_id}.json"
            if task_file.exists():
                task_file.unlink()
                print(f"Cleaned up task file for {task_id}")

if __name__ == "__main__":
    main()