import os
import subprocess

GREEN = "\033[32m"
RED = "\033[31m"
RESET = "\033[0m"


def run_tests():
    failed_result = False
    test_directory = "tests"
    errors = []
    main_class = "src/imperivm.py"

    print("Install dependencies...")
    try:
        subprocess.run("pipenv install")
    except:
        raise

    tests = [os.path.join(test_directory, file) for file in os.listdir(test_directory) if file.endswith(".imp")]
    for test in tests:
        print(f"Running test {test}", end=": ")
        try:
            subprocess.run(
                f"python {main_class} {test}",
                shell=True,
                check=True,
                text=True,
                capture_output=True)
            print(f"{GREEN}OK{RESET}")
        except subprocess.CalledProcessError as e:
            print(f"{RED}KO{RESET}")
            errors.append((test, e.stderr))
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
