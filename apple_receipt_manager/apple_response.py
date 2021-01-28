import logging
from apple_receipt_manager.receipt import Receipt
from apple_receipt_manager.pending_renewal import PendingRenewal
from apple_receipt_manager.apple_store_object import AppleStoreBaseObject

APPLE_API_STATUS_INFO = {
    21000: 'The request to the App Store was not made using the HTTP POST request method.',
    21001: 'This status code is no longer sent by the App Store.',
    21002: 'The data in the receipt-data property was malformed or the service experienced a temporary issue. '
           'Try again',
    21003: 'The receipt could not be authenticated',
    21004: 'The shared secret you profided does not match the shared secret on file for your account',
    21005: 'The receipt server was temporarily unable to provide the receipt. Try again',
    21006: 'This receipt is valid but the subscription has expired. '
           'When this status code is returned to your server, the receipt data is also decoded and '
           'returned as part of the response. '
           'Only returned for iOS 6-style transaction receipts for auto-renewable subscriptions.',
    21007: 'This receipt is from the test environment, but it was sent to the production environment for verification.',
    21008: 'This receipt is from the production environment, but it was sent to the test environment for verification.',
    21009: 'Internal data access error. Try again later.',
    21010: 'The user account cannot be found or has been deleted.',
    0: None
}


class AppleResponse(AppleStoreBaseObject):
    def __init__(self, response_data, logger=None):
        super().__init__(logger=logger)

        self.pending_renewal_info = response_data.get('pending_renewal_info')
        self.status = response_data.get('status')
        self.latest_receipt = response_data.get('latest_receipt')
        self.latest_receipt_info = response_data.get('latest_receipt_info')
        self.receipt = Receipt(response_data.get('receipt'), logger=self.logger) if response_data.get('receipt') else None
        self.environment = response_data.get('environment')
        self.is_retryable = response_data.get('is-retryable')

        # Business objects
        self.logger = logger

        self.pending_renewal_objects = []
        self.latest_receipt_objects = []

        if self.latest_receipt_info:
            for latest_receipt_info in self.latest_receipt_info:
                self.latest_receipt_objects.append(Receipt(latest_receipt_info, logger=self.logger))
        if self.pending_renewal_info:
            for pending_renewal_info in self.pending_renewal_info:
                self.pending_renewal_objects.append(PendingRenewal(pending_renewal_info, logger=self.logger))
