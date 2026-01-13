"""Claude Code CLI bridge."""
import subprocess
import json
from pathlib import Path

def run_claude(prompt: str, cwd: Path = None, timeout: int = 300) -> dict:
    """Run Claude Code CLI with prompt."""
    cwd = cwd or Path.cwd()

    try:
        result = subprocess.run(
            ["claude", "-p", prompt, "--output-format", "json"],
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=timeout
        )

        if result.returncode == 0:
            try:
                return {"success": True, "output": json.loads(result.stdout)}
            except json.JSONDecodeError:
                return {"success": True, "output": result.stdout}
        else:
            return {"success": False, "error": result.stderr or result.stdout}

    except subprocess.TimeoutExpired:
        return {"success": False, "error": "Timeout"}
    except FileNotFoundError:
        return {"success": False, "error": "Claude CLI not found. Install with: npm install -g @anthropic/claude-code"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def run_claude_interactive(prompt: str, cwd: Path = None) -> dict:
    """Run Claude Code in interactive mode (for user interaction)."""
    cwd = cwd or Path.cwd()

    try:
        # Run in foreground for user interaction
        result = subprocess.run(
            ["claude", prompt],
            cwd=str(cwd),
        )
        return {"success": result.returncode == 0}
    except FileNotFoundError:
        return {"success": False, "error": "Claude CLI not found"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def check_claude_available() -> bool:
    """Check if Claude CLI is available."""
    try:
        result = subprocess.run(["claude", "--version"], capture_output=True)
        return result.returncode == 0
    except:
        return False
