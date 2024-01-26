import subprocess

def shell(command):

    command = to_list(command)

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

    # Read and print the output in real-time
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())

    # Wait for the process to complete and get the return code
    return_code = process.poll()

    return return_code


def to_list(variable):
    if isinstance(variable, list):
        return variable
    elif variable is None:
        return []
    else:
        # Convert to string and then to list by splitting at whitespaces
        return variable.split()
