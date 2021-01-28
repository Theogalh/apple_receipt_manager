import datetime
from apple_receipt_manager.apple_store_object import AppleStoreBaseObject

BILLING_RETRIEVAL_PERIOD_INFO = {
    '1': 'The App Store is attempting to renew the subscription.',
    '0': 'The App Store has stopped attempting to renew the subscription.'
}


class PendingRenewal(AppleStoreBaseObject):
    def __init__(self, pending_renewal_data, logger=None):
        super().__init__(logger=logger)

        self.auto_renew_product_id = pending_renewal_data.get('auto_renew_product_id')
        self.auto_renew_status = pending_renewal_data.get('auto_renew_status')
        self.expiration_intent = pending_renewal_data.get('expiration_intent')

        self.grace_period_expires_date = pending_renewal_data.get('grace_period_expires_date')
        self.grace_period_expires_date_ms = pending_renewal_data.get('grace_period_expires_date_ms')
        self.grace_period_expires_date_pst = pending_renewal_data.get('grace_period_expires_date_pst')
        self.grace_period_expires_datetime = datetime.datetime.fromtimestamp(
            int(self.grace_period_expires_date_ms) // 1000
        ) if self.grace_period_expires_date_ms else None

        self.is_in_billing_retry_period = pending_renewal_data.get('is_in_billing_retry_period')
        self.offer_code_ref_name = pending_renewal_data.get('offer_code_ref_name')
        self.original_transaction_id = pending_renewal_data.get('original_transaction_id')
        self.price_consent_status = pending_renewal_data.get('price_consent_status')
        self.product_id = pending_renewal_data.get('product_id')
