import subprocess    # Used to run external commands and capture their output
import os            # Provides functions for interacting with the operating system
import uuid          # Used to generate a unique filename for each run to avoid conflicts

def run_code(language, code):
    filename = f"temp_{uuid.uuid4()}"
    try:
        # Handle Python code execution
        if language == 'python':
            file = f"{filename}.py"
            with open(file, 'w') as f:
                f.write(code)
            result = subprocess.run(['python', file], capture_output=True, text=True, timeout=5)

         # Handle C code execution
        elif language == 'c':
            c_file = f"{filename}.c"
            exe_file = f"{filename}.exe"
            with open(c_file, 'w') as f:
                f.write(code)
            compile_result = subprocess.run(['gcc', c_file, '-o', exe_file], capture_output=True, text=True)
            if compile_result.returncode != 0:
                return compile_result.stderr
            result = subprocess.run([f"./{exe_file}"], capture_output=True, text=True, timeout=5)

        # Handle Java code execution
        elif language == 'java':
            java_file = f"{filename}.java"
            class_name = filename
            with open(java_file, 'w') as f:
                f.write(code.replace('class Main', f'class {class_name}'))
            compile_result = subprocess.run(['javac', java_file], capture_output=True, text=True)
            if compile_result.returncode != 0:
                return compile_result.stderr
            result = subprocess.run(['java', class_name], capture_output=True, text=True, timeout=5)

        else:
            return "Unsupported Language"

        output = result.stdout
        error = result.stderr
        return output if output else error

    except Exception as e:
        return str(e)

    finally:
        # Clean up all temporary files created during execution
        for ext in ['.py', '.c', '.exe', '.class', '.java']:
            temp_file = f"{filename}{ext}"
            if os.path.exists(temp_file):
                os.remove(temp_file)
