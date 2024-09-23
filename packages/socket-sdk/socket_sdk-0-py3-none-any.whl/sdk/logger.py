import logging

logger = logging.getLogger('SDKLogger')
logger.setLevel(logging.DEBUG)
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler('sdk.log')
c_handler.setLevel(logging.INFO)
f_handler.setLevel(logging.DEBUG)
c_format = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s')
f_format = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)
logger.addHandler(c_handler)
logger.addHandler(f_handler)
