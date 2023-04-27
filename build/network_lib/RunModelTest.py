import network_main as nm
import os

# get the current working directory path
cwd = os.getcwd()

# get the directory before the current working directory path
parent_dir = os.path.dirname(cwd)

nm.train_network(parent_dir + "\\assets\\set1_edited")

#nm.run_model_test("saved_models\\trained_model_2023-02-11_13-12-27.h5", "\\data")