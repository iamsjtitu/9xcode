from fastapi import APIRouter, HTTPException
from datetime import datetime, timezone
import subprocess
import asyncio
import os

router = APIRouter(prefix="/updater", tags=["updater"])

PROJECT_PATH = "/var/www/9xcodes"
SCRIPT_PATH = os.path.join(os.path.dirname(__file__), "..", "update_script.sh")
LOG_FILE = "/tmp/9xcodes_update.log"

# In-memory status tracker
update_status = {
    "is_running": False,
    "last_run": None,
    "last_status": None,
    "logs": [],
    "step": None,
}


async def run_update_script():
    """Run the update shell script in background"""
    update_status["is_running"] = True
    update_status["logs"] = ["[INFO] Starting update..."]
    update_status["step"] = "Running update script..."

    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "update_script.sh")

    # If script doesn't exist, run commands directly
    if not os.path.exists(script_path):
        update_status["logs"].append("[INFO] Running commands directly...")
        commands = [
            ("git stash && git pull origin main", PROJECT_PATH, "Git Pull"),
            (f"{PROJECT_PATH}/backend/venv/bin/pip install -r requirements.txt", f"{PROJECT_PATH}/backend", "Backend Deps"),
            ("NODE_OPTIONS=--max_old_space_size=1024 yarn build", f"{PROJECT_PATH}/frontend", "Frontend Build"),
            ("pm2 restart all", PROJECT_PATH, "PM2 Restart"),
        ]
        all_ok = True
        for cmd, cwd, name in commands:
            update_status["step"] = name
            update_status["logs"].append(f"[INFO] >> {name}")
            try:
                proc = await asyncio.create_subprocess_shell(
                    cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, cwd=cwd
                )
                stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=300)
                if stdout:
                    for line in stdout.decode().strip().split('\n')[:10]:
                        update_status["logs"].append(f"[INFO] {line}")
                if proc.returncode != 0:
                    update_status["logs"].append(f"[ERROR] {name} failed (exit {proc.returncode})")
                    if stderr:
                        for line in stderr.decode().strip().split('\n')[:5]:
                            update_status["logs"].append(f"[ERROR] {line}")
                    if name in ("Git Pull", "Frontend Build"):
                        all_ok = False
                        break
                else:
                    update_status["logs"].append(f"[INFO] {name} done")
            except asyncio.TimeoutError:
                update_status["logs"].append(f"[ERROR] {name} timed out")
                all_ok = False
                break
            except Exception as e:
                update_status["logs"].append(f"[ERROR] {name}: {str(e)}")

        update_status["is_running"] = False
        update_status["last_run"] = datetime.now(timezone.utc).isoformat()
        update_status["last_status"] = "success" if all_ok else "failed"
        update_status["step"] = "Done"
        return

    try:
        process = await asyncio.create_subprocess_exec(
            "bash", script_path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await asyncio.wait_for(process.communicate(), timeout=600)

        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as f:
                lines = f.readlines()
            update_status["logs"] = [l.strip() for l in lines if l.strip()]
            last_line = lines[-1].strip() if lines else ""
            update_status["last_status"] = "success" if "RESULT:success" in last_line else "failed"
        else:
            update_status["last_status"] = "failed"
            update_status["logs"].append("[ERROR] Log file not found")

    except asyncio.TimeoutError:
        update_status["last_status"] = "failed"
        update_status["logs"].append("[ERROR] Update timed out after 10 minutes")
    except Exception as e:
        update_status["last_status"] = "failed"
        update_status["logs"].append(f"[ERROR] {str(e)}")
    finally:
        update_status["is_running"] = False
        update_status["last_run"] = datetime.now(timezone.utc).isoformat()
        update_status["step"] = "Done"


@router.post("/update")
async def trigger_update():
    """Trigger a website update (git pull, build, restart)"""
    if update_status["is_running"]:
        raise HTTPException(status_code=409, detail="Update already in progress")

    if not os.path.isdir(PROJECT_PATH):
        update_status["is_running"] = False
        update_status["last_run"] = datetime.now(timezone.utc).isoformat()
        update_status["last_status"] = "skipped"
        update_status["step"] = "Done"
        update_status["logs"] = [
            f"[INFO] Project path {PROJECT_PATH} not found.",
            "[INFO] This feature works on your VPS where the project is deployed.",
            "[INFO] On VPS: git pull -> pip install -> yarn build -> pm2 restart",
        ]
        return {"message": "Update skipped - not on VPS", "status": "skipped"}

    asyncio.create_task(run_update_script())
    return {"message": "Update started!", "status": "running"}


@router.get("/status")
async def get_update_status():
    """Get current update status and logs"""
    return {
        "is_running": update_status["is_running"],
        "last_run": update_status["last_run"],
        "last_status": update_status["last_status"],
        "current_step": update_status["step"],
        "logs": update_status["logs"],
    }
