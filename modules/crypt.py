import subprocess

def encrypt(code):
    """
    Runs the given binary (code) with <image_path> and <key_output_path> as arguments.

    Parameters:
    - code (str): Path to the binary executable.
    - image_path (str): Path to the input image.
    - key_output_path (str): Path to the output key file.

    Returns:
    - result (subprocess.CompletedProcess): The result of the subprocess run.
    """
    try:
        image_path = f"data/{code}/{code}_input.png"
        key_output_path = f"data/{code}"
        result = subprocess.run(
            ["cryptlib/encrypt", image_path, key_output_path],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print("Execution successful.")
        print("Output:", result.stdout)
        return result
    except subprocess.CalledProcessError as e:
        print("Error occurred while executing the binary:")
        print("Return code:", e.returncode)
        print("Error Output:", e.stderr)
        return e

def decrypt(code):
    """
    Runs the given binary (code) with <directory> as the only argument.

    Parameters:
    - code (str): Path to the binary executable.
    - directory (str): Path to the directory to pass as argument.

    Returns:
    - result (subprocess.CompletedProcess): The result of the subprocess run.
    """
    try:
        directory = f"data/{code}"
        result = subprocess.run(
            ["cryptlib/decrypt", directory],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print("Execution successful.")
        print("Output:", result.stdout)
        return result
    except subprocess.CalledProcessError as e:
        print("Error occurred while executing the binary:")
        print("Return code:", e.returncode)
        print("Error Output:", e.stderr)
        return e