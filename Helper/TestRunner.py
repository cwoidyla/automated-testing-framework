import os, importlib, re, logging, time
from Helper.ConfigFile import ConfigFile
from Helper.Connect import Connect

class TestRunner:
    def __init__(self):
        self.config = ConfigFile()
        self.test_files = self.config.dict['test.files']
        self.test_dir = self.config.dict['test.directory']
        self.test_dir_as_mod = self.test_dir.replace('/','.')
        self.logfile = self.config.dict['test.log.dir'] + self.config.dict['test.log.file']
        print(self.logfile)
        logging.basicConfig(filename=self.logfile,
                            filemode='w',
                            format='%(asctime)s - %(levelname)s - %(message)s')
                            # 2018-07-11 20:12:06,288 - INFO - Begin Test

    def start_connection(self):
        self.conn = Connect(self.config.dict['test.url'])

    def close_connection(self):
        self.conn.close()

    # Selenium automatically prefixes the word "test" in front of test definitions
    # E.g. test_search_p_h_s_document, or test_h_q_r_g_d
    def get_test_def_name(self, instance):
        # set regex to look for the def that starts with test
        r = re.compile("test*.")
        return list(filter(r.match, dir(instance)))[0]

    # Selenium automatically converts module names to class names
    # Python does not like class or module names that begin with numbers
    # TODO: Investigate how to generalize..
    def convert_module_name_to_class_name(self, test_mod_name):
        # Remove beginning two numbers (e.g. 01StartCreatePHS => StartCreatePHS)
        test_class_name = test_mod_name[2:]
        # Selenium removes underscores to convert module names to class names
        test_class_name = test_class_name.replace('_','')
        return test_class_name

    def run_consecutive(self):
        logging.info("Begin Automated Testing")
        at_start = time.time()
        for test in self.test_files:
            logging.info("Begin Test: " + test)
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
                test_start = time.time()
                run.setUp()
                # Pass test definition active Chrome driver
                getattr(run, test_def_name)(self.conn.driver)
                run.tearDown()
                test_end = time.time()
                logging.info("Elapsed time: " + str(test_end - test_start))
                logging.info("End Test: " + test)
            except Exception as e:
                test_end = time.time()
                logging.error(test + " Failed! ")
                logging.error("Exception occurred", exc_info=True)
                logging.info("Elapsed time: " + str(test_end - test_start))
                logging.info("End Test: " + test)
        self.close_connection()
        at_end = time.time()
        logging.info("End Automated Testing")
        logging.info("Total elapsed time: " + str(at_end - at_start))

    def run_parallel(self):
        print("Parallel")

    def calculateStatistics(self):
        logfile = open(self.logfile, 'r')
        for line in logfile:
            log = line.split('-')
            time = log[0]
            level = log[1]
            msg = log[2]

