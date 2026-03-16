#!/usr/bin/env python3
"""Deploy Streamlit dashboard."""
from __future__ import annotations

import argparse
import subprocess
import sys

from src.utils.logging import get_logger

logger = get_logger(__name__)


def main():
    parser = argparse.ArgumentParser(description="Deploy dashboard")
    parser.add_argument("--port", type=int, default=8501)
    parser.add_argument("--app", type=str, default="streamlit",
                        choices=["streamlit", "dash"])
    args = parser.parse_args()

    if args.app == "streamlit":
        cmd = [
            sys.executable, "-m", "streamlit", "run",
            "dashboards/streamlit/app.py",
            "--server.port", str(args.port),
            "--server.headless", "true",
        ]
    else:
        cmd = [sys.executable, "dashboards/dash/app.py"]

    logger.info(f"Starting {args.app} dashboard on port {args.port}")
    subprocess.run(cmd)


if __name__ == "__main__":
    main()
