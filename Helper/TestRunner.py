import os, importlib, re
from Helper.ConfigFile import ConfigFile
from Helper.Connect import Connect

class TestRunner:
    def __init__(self):
        self.config = ConfigFile()
        self.test_files = self.config.dict['test.files']
        self.test_dir = self.config.dict['test.directory']
        self.test_dir_as_mod = self.test_dir.replace('/','.')

    def start_connection(self):
        self.conn = Connect(self.config.dict['test.url'])

    def close_connection(self):
        self.conn.close()

    # Selenium automatically prefixes the word "test" in front of test definitions
    # E.g. test_search_document
    def get_test_def_name(self, instance):
        # set regex to look for the def that starts with test
        r = re.compile("test*.")
        return list(filter(r.match, dir(instance)))[0]

    # Selenium automatically converts module names to class names
    # Python does not like class or module names that begin with numbers
    # TODO: Investigate how to generalize..
    def convert_module_name_to_class_name(self, test_mod_name):
        # Remove beginning two numbers (e.g. 01SearchDocument => SearchDocument)
        test_class_name = test_mod_name[2:]
        # Selenium removes underscores to convert module names to class names
        test_class_name = test_class_name.replace('_','')
        return test_class_name

    def run_consecutive(self):
        for test in self.test_files:
            print("Testing " + test)
            # remove '.py' from python file name so file name can be used to import module
            test_mod_name = test.split(".")[0]
            module_path = self.test_dir_as_mod + test_mod_name
            module = importlib.import_module(module_path)
            # clean module name so it can be used to instantiate Selenium test class
            test_class_name = self.convert_module_name_to_class_name(test_mod_name)
            class_ = getattr(module, test_class_name)
            run = class_()
            # Get Selenium test definition to run tests
            test_def_name = self.get_test_def_name(run)
            try:
                run.setUp()
                # Pass test definition active Chrome driver
                getattr(run, test_def_name)(self.conn.driver)
                run.tearDown()
            except Exception as e:
                print("ERROR: " + test + " Failed! ")
                print(e)
        self.close_connection()

    def run_parallel(self):
        print("Parallel")