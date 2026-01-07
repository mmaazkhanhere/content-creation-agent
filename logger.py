from datetime import datetime

class Colors:
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    END = "\033[0m"

def log(message: str, level: str = "info"):
    """
    Clean, simple logging function with colored output and timestamps.
    Levels: info, success, warning, error, highlight
    """
    timestamp = datetime.now().strftime("%H:%M:%S")
    prefix = f"[{timestamp}]"
    
    level = level.lower()
    if level == "info":
        print(f"{Colors.BLUE}{prefix}{Colors.END} ℹ️  {message}")
    elif level == "success":
        print(f"{Colors.GREEN}{prefix} ✅ {message}{Colors.END}")
    elif level == "warning":
        print(f"{Colors.YELLOW}{prefix} ⚠️  {message}{Colors.END}")
    elif level == "error":
        print(f"{Colors.RED}{prefix} ❌ {message}{Colors.END}")
    elif level == "highlight":
        print(f"{Colors.BOLD}{Colors.BLUE}{prefix} ✨ {message}{Colors.END}")
    else:
        print(f"{prefix} {message}")
