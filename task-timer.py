import json
import os
import sys
import time
from datetime import datetime, timedelta

DATA_FILE = "timesheet.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"tasks": [], "current": None}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def start_task(task_name):
    data = load_data()
    if data["current"]:
        print(f"Stopping current task '{data['current']['name']}' before starting new one.")
        stop_task()
        data = load_data()
    data["current"] = {
        "name": task_name,
        "start_time": time.time()
    }
    save_data(data)
    print(f"Started task: {task_name}")

def stop_task():
    data = load_data()
    if not data["current"]:
        print("No task is currently running.")
        return
    task = data["current"]
    end_time = time.time()
    duration = end_time - task["start_time"]
    data["tasks"].append({
        "name": task["name"],
        "start_time": task["start_time"],
        "end_time": end_time,
        "duration": duration
    })
    print(f"Stopped task: {task['name']} (Duration: {str(timedelta(seconds=int(duration)))})")
    data["current"] = None
    save_data(data)

def status():
    data = load_data()
    if not data["current"]:
        print("No task is currently running.")
        return
    task = data["current"]
    duration = time.time() - task["start_time"]
    print(f"Currently running: {task['name']} (Elapsed: {str(timedelta(seconds=int(duration)))})")

def summary():
    data = load_data()
    if not data["tasks"]:
        print("No tasks logged yet.")
        return
    print("\n--- Time Sheet Summary ---")
    total = 0
    for task in data["tasks"]:
        duration = int(task["duration"])
        total += duration
        print(f"Task: {task['name']} | Duration: {str(timedelta(seconds=duration))}")
    print(f"\nTotal Time: {str(timedelta(seconds=total))}\n")

def main():
    if len(sys.argv) < 2:
        print("Usage: python task_timer.py [start <task_name> | stop | status | summary]")
        return
    command = sys.argv[1].lower()

    if command == "start" and len(sys.argv) >= 3:
        task_name = " ".join(sys.argv[2:])
        start_task(task_name)
    elif command == "stop":
        stop_task()
    elif command == "status":
        status()
    elif command == "summary":
        summary()
    else:
        print("Unknown command or missing arguments.")

if __name__ == "__main__":
    main()
