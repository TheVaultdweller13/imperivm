import os
import subprocess

GREEN = "\033[32m"
RED = "\033[31m"
RESET = "\033[0m"


def run_tests():
    failed_result = False
    test_directory = "tests"
    errors = []

    for file in os.listdir(test_directory):
        if file.endswith(".imp"):
            test_path = os.path.join(test_directory, file)
            print(f"Running test {test_path}", end=" ")
            try:
                subprocess.run(["./imperivm", test_path], check=True, text=True, capture_output=True)
                print(f"{GREEN}OK{RESET}")
            except subprocess.CalledProcessError as e:
                print(f"{RED}KO{RESET}")
                errors.append((test_path, e.stderr))
                failed_result = True

    if errors:
        print("\nErrors:")
    for test, error in errors:
        print(f"On {test}")
        print(f"{RED}{error}{RESET}")
        print()

    if errors:
        print("Failed tests:")
    for test, _ in errors:
        print(f"\t{RED}{test}{RESET}")

    return failed_result


if __name__ == "__main__":
    failed = run_tests()
    exit(1 if failed else 0)
