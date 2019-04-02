#!/usr/bin/env python
# If new configuration file options are added, be sure to
# modify get_test_configs() with new config option and 
# data validation.

from Helper.ConfigFile import ConfigFile
from Helper.TestRunner import TestRunner
from Helper.LoadTest import LoadTest

def main():
    initiate_test()


def initiate_test():
    config = ConfigFile()
    mr_robot = TestRunner()
    if config.dict['test.order'] == 'consecutive':
        mr_robot.start_connection()
        mr_robot.run_consecutive()
    elif config.dict['test.order'] == 'parallel':
        mr_robot.run_parallel()


if __name__ == '__main__':
    main()
