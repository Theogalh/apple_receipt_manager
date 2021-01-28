import datetime
from apple_receipt_manager.transaction import Transaction
from apple_receipt_manager.apple_store_object import AppleStoreBaseObject

RECEIPT_TYPES = [
    'Production',
    'ProductionVPP',
    'ProductionSandbox',
    'ProductionVPPSandbox'
]


class Receipt(AppleStoreBaseObject):
    def __init__(self, receipt_data, logger=None):
        super().__init__(logger=logger)

        # Apple Variables
        self.adam_id = receipt_data.get('adam_id', None)
        self.app_item_id = receipt_data.get('app_item_id', None)
        self.application_version = receipt_data.get('application_version')
        self.bundle_id = receipt_data.get('bundle_id')
        self.download_id = receipt_data.get('download_id')

        self.expiration_date = receipt_data.get('expiration_date')
        self.expiration_date_ms = receipt_data.get('expiration_date_ms')
        self.expiration_date_pst = receipt_data.get('expiration_date_pst')
        self.expiration_datetime = datetime.datetime.fromtimestamp(
            int(self.expiration_date_ms) // 1000
        ) if self.expiration_date_ms else None

        self.original_purchase_date = receipt_data.get('original_purchase_date')
        self.original_purchase_date_ms = receipt_data.get('original_purchase_date_ms')
        self.original_purchase_date_pst = receipt_data.get('original_purchase_date_pst')
        self.original_purchase_datetime = datetime.datetime.fromtimestamp(
            int(self.original_purchase_date_ms) // 1000
        ) if self.original_purchase_date_ms else None

        self.preorder_date = receipt_data.get('preorder_date')
        self.preorder_date_ms = receipt_data.get('preorder_date_ms')
        self.preorder_date_pst = receipt_data.get('preorder_date_pst')
        self.preorder_datetime = datetime.datetime.fromtimestamp(
            int(self.preorder_date_ms) // 1000
        ) if self.preorder_date_ms else None

        self.receipt_creation_date = receipt_data.get('receipt_creation_date')
        self.receipt_creation_date_ms = receipt_data.get('receipt_creation_date_ms')
        self.receipt_creation_date_pst = receipt_data.get('receipt_creation_date_pst')
        self.receipt_creation_datetime = datetime.datetime.fromtimestamp(
            int(self.receipt_creation_date_ms) // 1000
        ) if self.receipt_creation_date_ms else None

        self.request_date = receipt_data.get('request_date')
        self.request_date_ms = receipt_data.get('request_date_ms')
        self.request_date_pst = receipt_data.get('request_date_pst')
        self.request_datetime = datetime.datetime.fromtimestamp(
            int(self.request_date_ms) // 1000
        ) if self.request_date_ms else None

        self.original_application_version = receipt_data.get('original_application_version')

        self.receipt_type = receipt_data.get('receipt_type')
        self.in_app = receipt_data.get('in_app')

        # In sandbox environment, always "0"
        self.version_external_identifier = receipt_data.get('version_external_identifier')

        # Business Variables
        self.expired = self.expiration_datetime < datetime.datetime.utcnow() if self.expiration_datetime else False
        self.transactions = []
        if self.in_app:
            for transaction_data in self.in_app:
                self.transactions.append(Transaction(transaction_data, self.logger))
