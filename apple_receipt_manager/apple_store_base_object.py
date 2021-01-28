import logging


class AppleStoreBaseObject:
    def __init__(self, logger=None):
        self.logger = logger
        if not self.logger:
            self.logger = logging.getLogger(f'AppleReceiptManager')
