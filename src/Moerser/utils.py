import logging


def get_morse_alphabet():
    morse_alphabet = {'A': '01', 'B': '1000', 'C': '1010', 'D': '100', 'E': '0', 'F': '0010', 'G': '110', 'H': '0000',
                      'I': '00', 'J': '0111', 'K': '101', 'L': '0100', 'M': '11', 'N': '10', 'O': '111', 'P': '0110',
                      'Q': '1101', 'R': '010', 'S': '000', 'T': '1', 'U': '001', 'V': '0001', 'W': '011', 'X': '1001',
                      'Y': '1011', 'Z': '1100', '0': '11111', '1': '01111', '2': '00111', '3': '00011', '4': '00001',
                      '5': '00000', '6': '10000', '7': '11000', '8': '11100', '9': '11110', ' ': '0000000'}
    return morse_alphabet


def set_logger(name, mode="debug", write_log=False, full_path="./debug.log", write_mode="a"):
    """
        Make Log-File and PrettyPrints. Write mode can be either 'a' (append) or 'w' ((over)write).

        Usage:
            self.log = set_logger(name="log1", mode="info")
            self.log.error("This is wrong")

        Args:
            write_mode:
            full_path:
            write_log:
            name:
            mode:
        """

    if mode == "debug":
        level = logging.DEBUG
    elif mode == "info":
        level = logging.INFO
    elif mode == "warn":
        level = logging.WARN
    elif mode == "error":
        level = logging.ERROR
    else:
        level = logging.INFO

    # create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)

    # create format
    log_format = '[%(name)s][%(asctime)s][%(levelname)-5s][l:%(lineno)d][%(module)s.%(funcName)s()] %(message)s'
    formatter = logging.Formatter(log_format)

    # add format to console handler
    console_handler.setFormatter(formatter)

    # add console handler to logger
    logger.addHandler(console_handler)

    # write log in file
    if write_log is True:
        # create FileHandler
        file_handler = logging.FileHandler(full_path, mode=write_mode)  # write mode is a, w
        file_handler.setLevel(level)

        # add format to console handler
        file_handler.setFormatter(formatter)

        # add Handler to logger
        logger.addHandler(file_handler)

    return logger