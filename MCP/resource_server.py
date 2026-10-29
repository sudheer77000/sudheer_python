
from mcp.server.fastmcp import FastMCP
import psutil
import json
from datetime import datetime

mcp = FastMCP("SystemMonitor")

# Resource: returns current system monitoring data
@mcp.resource("system://metrics")
def get_system_metrics() -> str:
    """Get current CPU and memory usage."""

    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()

    metrics = {
        "timestamp": datetime.now().isoformat(),
        "cpu_usage_percent": cpu,
        "memory_usage_percent": memory.percent,
        "available_memory_mb": round(
            memory.available / (1024 * 1024), 2
        )
    }

    return json.dumps(metrics, indent=2)


if __name__ == "__main__":
    mcp.run(transport="stdio")
