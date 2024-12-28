import os
import subprocess


def run_tests():
    failed_result = True
    test_directory = 'tests'
    
    for file in os.listdir(test_directory):
        if file.endswith('.imp'):
            test_path = os.path.join(test_directory, file)
            print(f"Running test {test_path}")
            try:
                subprocess.run(['./imperivm', test_path], check=True, text=True, capture_output=True)
                print("\033[32mOK\033[0m")
                failed_result = False
            except subprocess.CalledProcessError as e:
                print("\033[31mKO\033[0m")
                print(f"Error: {e.stderr}")
                failed_result = True
    
    return failed_result

if __name__ == "__main__":
    failed = run_tests()
    exit(1 if failed else 0)