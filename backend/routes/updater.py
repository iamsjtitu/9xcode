from fastapi import APIRouter, HTTPException
from datetime import datetime, timezone
import asyncio
import json
import os

router = APIRouter(prefix="/updater", tags=["updater"])

PROJECT_PATH = "/var/www/9xcodes"
LOG_FILE = "/tmp/9xcodes_update.log"
STATUS_FILE = "/tmp/9xcodes_update_status.json"

# In-memory flag only for "currently running in this process"
_running_in_process = False


def read_status():
    """Read persisted status from file (survives PM2 restart)"""
    default = {
        "is_running": False,
        "last_run": None,
        "last_status": None,
        "step": None,
    }
    if not os.path.exists(STATUS_FILE):
        return default
    try:
        with open(STATUS_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return default


def write_status(data):
    """Persist status to file"""
    try:
        with open(STATUS_FILE, "w") as f:
            json.dump(data, f)
    except Exception:
        pass


def read_logs():
    """Read logs from the update log file"""
    if not os.path.exists(LOG_FILE):
        return []
    try:
        with open(LOG_FILE, "r") as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    except Exception:
        return []


async def run_update_script():
    """Run the update shell script in background"""
    global _running_in_process
    _running_in_process = True

    write_status({
        "is_running": True,
        "last_run": None,
        "last_status": None,
        "step": "Starting...",
    })

    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "update_script.sh")

    if not os.path.exists(script_path):
        # No shell script — run commands directly with live log updates
        with open(LOG_FILE, "w") as f:
            f.write("[INFO] Running commands directly...\n")

        commands = [
            ("git stash && git pull origin main", PROJECT_PATH, "Git Pull"),
            (f"{PROJECT_PATH}/backend/venv/bin/pip install -r requirements.txt", f"{PROJECT_PATH}/backend", "Backend Deps"),
            ("NODE_OPTIONS=--max_old_space_size=1024 yarn build", f"{PROJECT_PATH}/frontend", "Frontend Build"),
            ("pm2 restart all", PROJECT_PATH, "PM2 Restart"),
        ]
        all_ok = True
        for cmd, cwd, name in commands:
            write_status({"is_running": True, "last_run": None, "last_status": None, "step": name})
            with open(LOG_FILE, "a") as f:
                f.write(f"[INFO] >> {name}\n")
            try:
                proc = await asyncio.create_subprocess_shell(
                    cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, cwd=cwd
                )
                stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=300)
                with open(LOG_FILE, "a") as f:
                    if stdout:
                        for line in stdout.decode().strip().split('\n')[:10]:
                            f.write(f"[INFO] {line}\n")
                    if proc.returncode != 0:
                        f.write(f"[ERROR] {name} failed (exit {proc.returncode})\n")
                        if stderr:
                            for line in stderr.decode().strip().split('\n')[:5]:
                                f.write(f"[ERROR] {line}\n")
                        if name in ("Git Pull", "Frontend Build"):
                            all_ok = False
                            break
                    else:
                        f.write(f"[INFO] {name} done\n")
            except asyncio.TimeoutError:
                with open(LOG_FILE, "a") as f:
                    f.write(f"[ERROR] {name} timed out\n")
                all_ok = False
                break
            except Exception as e:
                with open(LOG_FILE, "a") as f:
                    f.write(f"[ERROR] {name}: {str(e)}\n")

        now = datetime.now(timezone.utc).isoformat()
        status = "success" if all_ok else "failed"
        with open(LOG_FILE, "a") as f:
            f.write(f"RESULT:{status}\n")
        write_status({"is_running": False, "last_run": now, "last_status": status, "step": "Done"})
        _running_in_process = False
        return

    # Shell script exists — run it
    try:
        process = await asyncio.create_subprocess_exec(
            "bash", script_path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await asyncio.wait_for(process.communicate(), timeout=600)

        logs = read_logs()
        last_line = logs[-1] if logs else ""
        status = "success" if "RESULT:success" in last_line else "failed"
        now = datetime.now(timezone.utc).isoformat()
        write_status({"is_running": False, "last_run": now, "last_status": status, "step": "Done"})

    except asyncio.TimeoutError:
        now = datetime.now(timezone.utc).isoformat()
        with open(LOG_FILE, "a") as f:
            f.write("[ERROR] Update timed out after 10 minutes\n")
            f.write("RESULT:failed\n")
        write_status({"is_running": False, "last_run": now, "last_status": "failed", "step": "Done"})
    except Exception as e:
        now = datetime.now(timezone.utc).isoformat()
        with open(LOG_FILE, "a") as f:
            f.write(f"[ERROR] {str(e)}\n")
            f.write("RESULT:failed\n")
        write_status({"is_running": False, "last_run": now, "last_status": "failed", "step": "Done"})
    finally:
        _running_in_process = False


@router.post("/update")
async def trigger_update():
    """Trigger a website update (git pull, build, restart)"""
    status = read_status()
    if status.get("is_running") and _running_in_process:
        raise HTTPException(status_code=409, detail="Update already in progress")

    if not os.path.isdir(PROJECT_PATH):
        now = datetime.now(timezone.utc).isoformat()
        write_status({"is_running": False, "last_run": now, "last_status": "skipped", "step": "Done"})
        with open(LOG_FILE, "w") as f:
            f.write(f"[INFO] Project path {PROJECT_PATH} not found.\n")
            f.write("[INFO] This feature works on your VPS where the project is deployed.\n")
            f.write("[INFO] On VPS: git pull -> pip install -> yarn build -> pm2 restart\n")
            f.write("RESULT:skipped\n")
        return {"message": "Update skipped - not on VPS", "status": "skipped"}

    # Clear old state
    with open(LOG_FILE, "w") as f:
        f.write("[INFO] Starting update...\n")

    asyncio.create_task(run_update_script())
    return {"message": "Update started!", "status": "running"}


@router.get("/status")
async def get_update_status():
    """Get current update status and logs (reads from file, survives restart)"""
    status = read_status()
    logs = read_logs()

    # Auto-detect if script finished but status wasn't updated (e.g. PM2 restart killed the process)
    if status.get("is_running") and not _running_in_process:
        # Process that started the update is gone (PM2 restarted)
        # Check if log file has a RESULT line
        if logs:
            last_line = logs[-1]
            if "RESULT:" in last_line:
                result = "success" if "RESULT:success" in last_line else "failed"
                now = datetime.now(timezone.utc).isoformat()
                status = {"is_running": False, "last_run": now, "last_status": result, "step": "Done"}
                write_status(status)

    return {
        "is_running": status.get("is_running", False),
        "last_run": status.get("last_run"),
        "last_status": status.get("last_status"),
        "current_step": status.get("step"),
        "logs": logs,
    }
