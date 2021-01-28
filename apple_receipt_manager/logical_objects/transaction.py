import datetime
from apple_receipt_manager.apple_store_base_object import AppleStoreBaseObject

IN_APP_OWNERSHIP_TYPE = {
    'FAMILY_SHARED': 'The transaction belongs to a family member who benefits from service.',
    'PURCHASED': 'The transaction belongs to the purchaser.'
}


class Transaction(AppleStoreBaseObject):
    def __init__(self, transaction_data, logger=None):
        super().__init__(logger=logger)

        # Apple Variables

        # - Cancellation
        self.cancellation_date = transaction_data.get('cancellation_date')
        self.cancellation_date_ms = transaction_data.get('cancellation_date_ms')
        self.cancellation_date_pst = transaction_data.get('cancellation_date_pst')
        self.cancellation_datetime = datetime.datetime.fromtimestamp(
            int(self.cancellation_date_ms)//1000
        ) if self.cancellation_date_ms else None

        self.cancellation_reason = transaction_data.get('cancellation_reason')

        # - Expires
        self.expires_date = transaction_data.get('expires_date')
        self.expires_date_ms = transaction_data.get('expires_date_ms')
        self.expires_date_pst = transaction_data.get('expires_date_pst')
        self.expires_datetime = datetime.datetime.fromtimestamp(
            int(self.expires_date_ms)//1000
        ) if self.expires_date_ms else None

        # - Original Purchase
        self.original_purchase_date = transaction_data.get('original_purchase_date')
        self.original_purchase_date_ms = transaction_data.get('original_purchase_date_ms')
        self.original_purchase_date_pst = transaction_data.get('original_purchase_date_pst')
        self.original_purchase_datetime = datetime.datetime.fromtimestamp(
            int(self.original_purchase_date_ms)//1000
        ) if self.original_purchase_date_ms else None

        # - Purchase
        self.purchase_date = transaction_data.get('purchase_date')
        self.purchase_date_ms = transaction_data.get('purchase_date_ms')
        self.purchase_date_pst = transaction_data.get('purchase_date_pst')
        self.purchase_datetime = datetime.datetime.fromtimestamp(
            int(self.purchase_date_ms)//1000
        ) if self.purchase_date_ms else None

        # - Transaction variables
        self.transaction_id = transaction_data.get("transaction_id")
        self.quantity = transaction_data.get('quantity')
        self.web_order_line_item = transaction_data.get('web_order_line_item')
        self.promotional_offer_id = transaction_data.get('promotional_offer_id')
        self.product_id = transaction_data.get('product_id')
        self.original_transaction_id = transaction_data.get('original_transaction_id')
        self.is_in_intro_offer_period = transaction_data.get('is_in_intro_offer_period')
        self.is_trial_period = transaction_data.get('is_trial_period')
        self.in_app_ownership_type = transaction_data.get('in_app_ownership_type')

        # Business Variables

        self.cancelled = self.cancellation_date is not None
        self.expired = self.expires_datetime < datetime.datetime.utcnow() if self.expires_datetime else False
