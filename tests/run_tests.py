
import unittest
import os

# Instantiate the test loader.
loader = unittest.TestLoader()
# Instantiate the test runner.
runner = unittest.TextTestRunner(verbosity=2)
# Specify the root dir to start hunting for tests from.
start_dir = 'C:\\Users\\James.Izzard\\Documents\\PyDiet\\tests'
# Change the current directory
os.chdir(start_dir)
# Discover the tests.
suite = loader.discover(start_dir)
# Run the tests.
runner.run(suite)