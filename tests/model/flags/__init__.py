from unittest import mock

import model
from . import fixtures, configs

# Build the global flag list for testing;
# We have to patch the test configs as well as pass them in, because the Flag constructor is going to
# check that the flag name is actually on the list in the configs file.
with mock.patch.dict(model.flags.configs.FLAG_CONFIGS, configs.TEST_FLAG_CONFIGS):
    ALL_TEST_FLAGS = model.flags.build_global_flag_list(configs.TEST_FLAG_CONFIGS)