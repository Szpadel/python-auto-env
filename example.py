import auto_env
import os

current_file = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file)
auto_env.run_in_venv(
    "%s/.venv" % current_dir, # Path to virtual env
    "%s/requirements.txt" % current_dir, # Path to requirements.txt
    current_file # Path to file to execute
)



import numpy as np;

print("Hello world")
print(np.array([1,2,3]))
