import sys, os

COMMENT = '#'


class ConfigFile:
    def __init__(self):
        self.cfg_file_path = os.getcwd() + "/test.cfg"
        self.dict = self.get_test_configs( self.cfg_file_path )

    def get_test_configs(self, file_name):
        file = open(file_name, 'r')
        cfg = {}
        test_files = []
        for line in file:
            line = line.strip()
            if line.startswith(COMMENT) is not True and len(line) > 0:
                line = line.split('=')
                if len(line) > 2:
                    print('ERROR: "' + line + '" has one too many equal signs!')
                    sys.exit(0)
                elif len(line) < 2:
                    print('ERROR: "' + line + '" is incomplete!')
                    sys.exit(0)

                key = line[0]
                value = line[1]

                if key == 'test.log.dir':
                    cfg['test.log.dir'] = value
                    # Check to see if picture directory exists
                    if os.path.isdir(cfg['test.log.dir']) is False:
                        os.mkdir(cfg['test.log.dir'])

                elif key == 'test.log.file':
                    cfg['test.log.file'] = value

                elif key == 'test.pics.enable':
                    if value == 'true':
                        cfg['test.pics.enable'] = True
                    elif value == 'false':
                        cfg['test.pics.enable'] = False
                    else:
                        print("ERROR: pics.enable value not recognized.")
                        sys.exit(0)

                elif key == 'test.pics.dir':
                    cfg['test.pics.dir'] = os.getcwd() + value
                    # Check to see if picture directory exists
                    if os.path.isdir(cfg['test.pics.dir']) is False:
                        os.mkdir(cfg['test.pics.dir'])

                if key == 'test.headless':
                    if value == 'true':
                        cfg['test.headless'] = True
                    elif value == 'false':
                        cfg['test.headless'] = False
                    else:
                        print("ERROR: test.headless input was misspelled or entered incorrectly.")
                        sys.exit(0)

                elif key == 'test.url':
                    cfg['test.url'] = value

                elif key == 'phs.doc.name':
                    cfg['phs.doc.name'] = value

                elif key == 'phs.doc.number':
                    cfg['phs.doc.number'] = value

                elif key == 'test.files.directory':
                    cfg['test.directory'] = value

                elif key == 'test.files.order':
                    if value == 'consecutive':
                        cfg['test.order'] = 'consecutive'
                    elif value == 'parallel':
                        cfg['test.order'] = 'parallel'
                    else:
                        print("ERROR: test.order input was misspelled or entered incorrectly.")
                        sys.exit(0)

                elif key == 'test.files.begin':
                    line = next(file).strip()
                    while line != 'test.files.end=':
                        if line.startswith("#") or line == '': # if line is not a comment and is not empty
                            line = next(file).strip()
                        elif '#' in line: # else if line contains a trailing comment
                            line = line.split('#')[0] # truncate comment
                            test_files.append(line)
                            line = next(file).strip()
                        else:
                            test_files.append(line)
                            line = next(file).strip()
                    cfg['test.files'] = test_files

        file.close()
        return cfg
