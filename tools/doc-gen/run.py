from pathlib import Path
import argparse


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["preview", "release"], default="preview")
    args = parser.parse_args()
    output = Path("build")
    output.mkdir(exist_ok=True)
    print(f"doc-gen sample executed: mode={args.mode}")


if __name__ == "__main__":
    main()
