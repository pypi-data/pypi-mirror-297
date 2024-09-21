import os
import tempfile
from functools import wraps

def file_operation_checker(test_cases):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                returned_funcs = func(*args, **kwargs)
                all_passed = True
                temp_files = []

                for func_name, cases in test_cases.items():
                    if func_name not in returned_funcs:
                        all_passed = False
                        break
                    
                    test_func = returned_funcs[func_name]
                    
                    for case in cases:
                        try:
                            # Create temporary files
                            for file_key in ['input_file', 'output_file']:
                                if file_key in case:
                                    fd, path = tempfile.mkstemp()
                                    os.close(fd)
                                    temp_files.append(path)
                                    if 'content' in case[file_key]:
                                        with open(path, 'w') as f:
                                            f.write(case[file_key]['content'])
                                    case['input'][file_key.replace('_file', '')] = path

                            # Execute the function
                            result = test_func(**case['input'])

                            # Check the result
                            if 'expected_output' in case:
                                if result != case['expected_output']:
                                    all_passed = False
                                    break

                            # Check file content if needed
                            if 'expected_file_content' in case:
                                with open(case['input']['output'], 'r') as f:
                                    content = f.read()
                                if content != case['expected_file_content']:
                                    all_passed = False
                                    break

                        except Exception as e:
                            print(f"Error in test case: {e}")
                            all_passed = False
                            break

                if all_passed:
                    print("✅ Great job! Exercise completed successfully.")
                else:
                    print("❗ The implementation is incorrect or the exercise was not implemented.")
            except Exception as e:
                print(f"❗ An error occurred: {e}")
            finally:
                # Clean up temporary files
                for path in temp_files:
                    if os.path.exists(path):
                        os.remove(path)

        return wrapper
    return decorator

# Example usage for each function:

check_exercise_246 = file_operation_checker({
    'write_to_file': [
        {
            'input': {'string_value': 'Hello, World!', 'filename': 'output_file'},
            'output_file': {'content': ''},
            'expected_file_content': 'Hello, World!'
        }
    ]
})

check_exercise_247 = file_operation_checker({
    'read_from_file': [
        {
            'input': {'filename': 'input_file'},
            'input_file': {'content': 'Hello, World!'},
            'expected_output': 'Hello, World!'
        }
    ]
})

check_exercise_248 = file_operation_checker({
    'append_to_file': [
        {
            'input': {'filename': 'output_file', 'line': 'New line'},
            'output_file': {'content': 'Existing content\n'},
            'expected_file_content': 'Existing content\nNew line\n'
        }
    ]
})

check_exercise_249 = file_operation_checker({
    'count_lines': [
        {
            'input': {'filename': 'input_file'},
            'input_file': {'content': 'Line 1\nLine 2\nLine 3'},
            'expected_output': 3
        }
    ]
})

check_exercise_250 = file_operation_checker({
    'copy_file': [
        {
            'input': {'source': 'input_file', 'destination': 'output_file'},
            'input_file': {'content': 'File content'},
            'output_file': {'content': ''},
            'expected_file_content': 'File content'
        }
    ]
})

# You can now use these decorators with your exercise functions as before

# Example usage for each function:

check_exercise_246 = file_operation_checker({
    'write_to_file': [
        {
            'input': {'string_value': 'Hello, World!', 'filename': 'output_file'},
            'output_file': {'content': ''},
            'expected_file_content': 'Hello, World!'
        }
    ]
})

check_exercise_247 = file_operation_checker({
    'read_from_file': [
        {
            'input': {'filename': 'input_file'},
            'input_file': {'content': 'Hello, World!'},
            'expected_output': 'Hello, World!'
        }
    ]
})

check_exercise_248 = file_operation_checker({
    'append_to_file': [
        {
            'input': {'filename': 'output_file', 'line': 'New line'},
            'output_file': {'content': 'Existing content\n'},
            'expected_file_content': 'Existing content\nNew line\n'
        }
    ]
})

check_exercise_249 = file_operation_checker({
    'count_lines': [
        {
            'input': {'filename': 'input_file'},
            'input_file': {'content': 'Line 1\nLine 2\nLine 3'},
            'expected_output': 3
        }
    ]
})

check_exercise_250 = file_operation_checker({
    'copy_file': [
        {
            'input': {'source': 'input_file', 'destination': 'output_file'},
            'input_file': {'content': 'File content'},
            'output_file': {'content': ''},
            'expected_file_content': 'File content'
        }
    ]
})
# Create a function called `write_to_file` that takes a string value and a filename, and writes the string to the file.
@check_exercise_246
def exercise_246():
    # This line is mandatory and should not be removed
    ex_stat_init = True
    
    # BELOW GOES YOUR CODE
    def write_to_file(string_value, filename):
        with open(filename, 'w') as file:
            file.write(string_value)
    
    # ABOVE GOES YOUR CODE
    return {"write_to_file": write_to_file}

# Run the exercise
exercise_246()