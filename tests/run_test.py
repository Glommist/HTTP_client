# run_tests.py
import sys
import subprocess


def main():
    use_pytest = True  # 设置为 False 使用 unittest

    if use_pytest:
        cmd = ["pytest", "tests/", "-v"]
    else:
        cmd = [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"]

    subprocess.run(cmd)


if __name__ == "__main__":
    main()
