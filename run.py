from os.path import join, dirname, abspath, exists
from subprocess import run
from time import sleep
from vunit import VUnit

# This is the function to run after the tests. Such a function must have a first argument named output_path.
# output_path is the path to the directory created for the test. This is where the testbench will write
# its data sets. The test fails when it returns False. In this case this happens when a file named fail is found
# in the output directory or if no pass or fail file is found within ten seconds
def post_check(output_path):
    for i in range(10):
        if exists(join(output_path, "pass")):
            return True
        elif exists(join(output_path, "fail")):
            return False

        sleep(1)

    return False

# pre_config is the function to run before the test. This function will call Octave with the script that looks
# for data set files in the output path and visualizes those data sets. For this reason output_path must be passed
# as an argument to the script. In this case I also want to pass a title and the number of sets to the script
# to be used for the Octave generated plot. However, a pre_config function cannot be called with arbitrary
# arguments. VUnit has no knowledge of the title and the number of sets when it calls the function.
# The trick is to have a function make_pre_config that can generate a pre_config function which has been
# "hardcoded" with the desired values
def make_pre_config(plot_title, num_of_data_sets):
    def pre_config(output_path):
        p = run(["octave", join(root, "octave", "visualize.m"), output_path, plot_title, str(num_of_data_sets)])

        return p.returncode == 0

    return pre_config

prj = VUnit.from_argv()

# The array utility is not included by default when VUnit compiles the vunit_lib so it has to be added
prj.add_array_util()

root = dirname(__file__)
lib = prj.add_library("lib")

lib.add_source_files(join(root, "test", "*.vhd"))

# You can get the testbench object using the entity name
tb_octave = lib.entity("tb_octave")

# For this testbench (and all its test cases if it had any) I will add two configurations. One with the
# activate_bug generic set to true and one with the generic set to false.
#
# Each configuration has a name which you see when listing the tests from the command line. The generics
# are listed in a Python dictionary which is a list of key/value pairs. Then I tell what pre_config
# and post_check functions I want. The post_check is common to the configurations but I generate different
# pre_configs to have different titles

size_of_data_set = 10
num_of_data_sets = 10
for name, activate_bug in [("Passing test", False), ("Failing test", True)]:
    tb_octave.add_config(name=name,
                         generics=dict(size_of_data_set=size_of_data_set,
                                       num_of_data_sets=num_of_data_sets,
                                       activate_bug=activate_bug),
                         pre_config=make_pre_config(plot_title=name, num_of_data_sets=num_of_data_sets),
                         post_check=post_check)

prj.main()
