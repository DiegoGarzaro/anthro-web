import logging

class Logger:
    def __init__(self, name='app_logger', log_file='app.log', level=logging.INFO):
        """
        Initialize the logger.

        Args:
            name (str): Name of the logger.
            log_file (str): Path to the log file.
            level (int): Logging level.
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Create handlers
        file_handler = logging.FileHandler(log_file)
        console_handler = logging.StreamHandler()

        # Set level for handlers
        file_handler.setLevel(level)
        console_handler.setLevel(level)

        # Create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)

    def debug(self, message):
        self.logger.debug(message)

    def warning(self, message):
        self.logger.warning(message)

    def critical(self, message):
        self.logger.critical(message)
