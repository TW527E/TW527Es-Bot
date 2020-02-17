import logging

def initLogging(logFilename):

    logging.basicConfig(
                        level    = logging.DEBUG,
                        format='%(asctime)s-%(levelname)s-%(message)s',
                        datefmt  = '%y-%m-%d %H:%M',
                        filename = logFilename,
                        filemode = 'w');
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s-%(levelname)s-%(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

initLogging('test.log')
logging.info('just play')
