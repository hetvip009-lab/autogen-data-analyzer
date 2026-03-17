import subprocess
import os
from utils.logger import get_logger

logger = get_logger("executor_agent")

def save_and_run_code(code):
    """Save generated code to file and execute it"""
    try:
        # Save code to temporary file
        with open("temp_code.py", "w") as f:
            f.write(code)
        logger.info("Code saved to temp_code.py")

        # Run the code
        result = subprocess.run(
            ["python", "temp_code.py"],
            capture_output=True,
            text=True,
            timeout=30
        )

        # Check if code ran successfully
        if result.returncode == 0:
            logger.info("Code executed successfully!")
            return {
                "success": True,
                "output": result.stdout,
                "error": None
            }
        else:
            logger.error(f"Code execution failed: {result.stderr}")
            return {
                "success": False,
                "output": None,
                "error": result.stderr
            }

    except subprocess.TimeoutExpired:
        logger.error("Code execution timed out!")
        return {
            "success": False,
            "output": None,
            "error": "Code execution timed out after 30 seconds!"
        }

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return {
            "success": False,
            "output": None,
            "error": str(e)
        }

    finally:
        # Clean up temp file
        if os.path.exists("temp_code.py"):
            os.remove("temp_code.py")
            logger.info("Temp file cleaned up!")