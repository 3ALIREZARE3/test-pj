import logging
import yaml
import signal
import time

a = 0
log_level = logging.DEBUG

def set_level(sig, frame):

    global levels
    levels = [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]

    global a
    a += 1
    if a > 4:
        a = 0
    
    global log_level
    log_level = levels[a]
    logging.info(log_level)


def read_config(filename, keylst):

    with open(filename, "r") as f:
        data = yaml.safe_load(f)
        logging.debug(data)

    for i in keylst:
        if i not in data.keys():
            err = f"missing value : {i}"
            return False, err
    result = {}
    for i in data:
        result[i] = data[i]

    return True, result



while True:

    print("=========================================================================================")

    
    signal.signal(signal.SIGINT, set_level)
    logging.basicConfig(filename="test.log", level=log_level, format="%(levelname)s:%(filename)s:%(asctime)s:%(message)s")

    status, names = read_config("test.yml", ["firstName", "lastName"])
    logging.debug(status)
    logging.info(names)

    if status:
        print("DONE!")
        print(f"your name is {names['firstName']} ({names['midName']}) {names['lastName']}")
    else:
        print("ERROR!!!")
        print(f"   :   {names}")
    print(log_level)
    time.sleep(3)