import subprocess
import pytest


def compile_cpp():
    compile_command = "g++ test.cpp -o testExecutable"
    subprocess.run(compile_command, check=True, shell=True)


def init():
    compile_command = "g++ test.cpp -o testExecutable"
    subprocess.run(compile_command, check=True, shell=True)

    subprocess.run("python ../main.py -t 'Linux GCC C++'", shell=True, check=True)

    with (open('output.txt', 'r') as file):
        result = [line for line in file.readlines()]
        all_content = file.read()
        result.append(all_content)
        return result


def run_test(input_string):
    with subprocess.Popen(['./testExecutable'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as proc:
        output, errors = proc.communicate(input=input_string)
        return output, errors


@pytest.mark.parametrize("input_string", init())
def test_cpp_executable(input_string):
    output, errors = run_test(input_string)
    assert errors == "", f"Error occurred: {errors}"


def test_cpp_executable_all():
    with (open('output.txt', 'r') as file):
        all_content = file.read()
        output, errors = run_test(all_content)
        assert errors == "", f"Error occurred: {errors}"


def test_valid_simple():
    output, errors = run_test("Hi")
    assert errors == "", f"Error occurred: {errors}"