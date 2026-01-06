import sys
from app import cli

USAGE = """Usage:
  python3 -m app install
  python3 -m app pre-pull
  python3 -m app safe-save
"""

def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(USAGE.strip())
        return 2

    cmd = argv[1]

    if cmd == "install":
        return cli.install(argv[2:])
    if cmd == "pre-pull":
        return cli.pre_pull(argv[2:])
    if cmd == "safe-save":
        return cli.safe_save(argv[2:])

    if cmd in ("-h", "--help", "help"):
        print(USAGE.strip())
        return 0

    print(f"Unknown command: {cmd}\n")
    print(USAGE.strip())
    return 2

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
