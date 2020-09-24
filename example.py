import auto_env
import os

current_file = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file)
auto_env.run_in_venv(
    os.path.join(current_dir, '.venv'), # Path to virtual env
    os.path.join(current_dir, 'requirements.txt'), # Path to requirements.txt
    current_file # Path to file to execute
)



import numpy as np

print("Hello world")
print(np.array([1,2,3]))
