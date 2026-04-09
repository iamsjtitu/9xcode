from fastapi import APIRouter, HTTPException
from datetime import datetime, timezone
import subprocess
import asyncio
import os

router = APIRouter(prefix="/updater", tags=["updater"])

PROJECT_PATH = "/var/www/9xcodes"

# In-memory status tracker
update_status = {
    "is_running": False,
    "last_run": None,
    "last_status": None,  # "success" | "failed"
    "logs": [],
    "step": None,
}


def reset_status():
    update_status["is_running"] = True
    update_status["logs"] = []
    update_status["step"] = "Starting..."
    update_status["last_status"] = None


def add_log(msg, is_error=False):
    prefix = "ERROR" if is_error else "INFO"
    update_status["logs"].append(f"[{prefix}] {msg}")


async def run_command(cmd, cwd=None, step_name=""):
    """Run a shell command and capture output"""
    update_status["step"] = step_name
    add_log(f">> {step_name}: {cmd}")

    try:
        process = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=cwd or PROJECT_PATH,
        )
        stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=300)

        stdout_text = stdout.decode().strip()
        stderr_text = stderr.decode().strip()

        if stdout_text:
            for line in stdout_text.split('\n')[:20]:
                add_log(line)
        if stderr_text and process.returncode != 0:
            for line in stderr_text.split('\n')[:10]:
                add_log(line, is_error=True)

        if process.returncode != 0:
            add_log(f"{step_name} failed with exit code {process.returncode}", is_error=True)
            return False
        
        add_log(f"{step_name} completed successfully")
        return True
    except asyncio.TimeoutError:
        add_log(f"{step_name} timed out after 5 minutes", is_error=True)
        return False
    except Exception as e:
        add_log(f"{step_name} exception: {str(e)}", is_error=True)
        return False


async def do_update():
    """Run the full update pipeline"""
    reset_status()

    VENV_PIP = f"{PROJECT_PATH}/backend/venv/bin/pip"

    steps = [
        ("git pull origin main", PROJECT_PATH, "Git Pull"),
        (f"{VENV_PIP} install -r requirements.txt", f"{PROJECT_PATH}/backend", "Backend Dependencies"),
        ("NODE_OPTIONS=--max_old_space_size=512 yarn build", f"{PROJECT_PATH}/frontend", "Frontend Build"),
        ("pm2 restart all", PROJECT_PATH, "PM2 Restart"),
    ]

    all_ok = True
    for cmd, cwd, name in steps:
        success = await run_command(cmd, cwd, name)
        if not success:
            # Git pull and build are critical - stop on failure
            if name in ("Git Pull", "Frontend Build"):
                all_ok = False
                break
            # Dependencies and restart - log but continue
            if name == "PM2 Restart":
                all_ok = False

    update_status["is_running"] = False
    update_status["last_run"] = datetime.now(timezone.utc).isoformat()
    update_status["last_status"] = "success" if all_ok else "failed"
    update_status["step"] = "Done" if all_ok else "Failed"
    add_log(f"Update {'completed successfully' if all_ok else 'failed'}!")


@router.post("/update")
async def trigger_update():
    """Trigger a website update (git pull, build, restart)"""
    if update_status["is_running"]:
        raise HTTPException(status_code=409, detail="Update already in progress")

    # Check if project path exists
    if not os.path.isdir(PROJECT_PATH):
        # On preview/dev environment, just simulate
        update_status["is_running"] = False
        update_status["last_run"] = datetime.now(timezone.utc).isoformat()
        update_status["last_status"] = "skipped"
        update_status["step"] = "Done"
        update_status["logs"] = [
            f"[INFO] Project path {PROJECT_PATH} not found.",
            "[INFO] This feature works on your VPS where the project is deployed.",
            "[INFO] On VPS, it will run: git pull -> install deps -> yarn build -> pm2 restart",
        ]
        return {"message": "Update skipped - not on VPS", "status": "skipped"}

    # Run update in background
    asyncio.create_task(do_update())
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
