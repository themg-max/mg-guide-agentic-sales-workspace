"""CLI entrypoint: PYTHONPATH=src python3 -m agents.follow_up_planning"""

from .harness import main

if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
