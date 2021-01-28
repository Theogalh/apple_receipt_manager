import requests

from apple_receipt_manager.exceptions import AppleManagerStatusError, AppleManagerInternalError
from apple_receipt_manager.apple_response import AppleResponse, APPLE_API_STATUS_INFO
from apple_receipt_manager.apple_store_object import AppleStoreBaseObject


class AppleReceiptManager(AppleStoreBaseObject):
    apple_url = "https://sandbox.itunes.apple.com"
    sandbox_url = "https://buy.itunes.apple.com/verifyReceipt"

    def get_response_object(self, receipt_data, password=None, exclude_old_transactions=False):
        response_data = self.get_apple_response_data(receipt_data, password=password, exclude_old_transactions=exclude_old_transactions)
        return AppleResponse(response_data, self.logger)

    def get_apple_response_data(self, receipt, password=None, exclude_old_transactions=False):
        try:
            data = {
                'receipt-data': receipt
            }
            if password:
                if not isinstance(password, str):
                    raise TypeError('password parameter needs to be a Str')
                data['password'] = password
            if exclude_old_transactions:
                if not isinstance(exclude_old_transactions, bool):
                    raise TypeError('exclude_old_transactions parameter needs to be a Bool')
                data['exclude-old-transactions'] = exclude_old_transactions
            response = requests.post(self.apple_url + '/verifyReceipt', json=data)
            response.raise_for_status()
            response_json = response.json()

            # If we get a status 21007, we need call the sandbox URL.
            if response_json['status'] == '21007':
                response = requests.post(self.sandbox_url + '/verifyReceipt', json=data)
                response.raise_for_status()
                response_json = response.json()
            response_status = response_json.get('status')
            if response_status != 0:
                self.logger.warning(self.get_response_status_info(response_status))
        except BaseException as exc:
            self.logger.exception("Apple Manager internal error")
            raise AppleManagerInternalError("Apple Manager internal error") from exc
        return response_json

    @classmethod
    def get_response_status_info(cls, status):
        if not isinstance(status, int):
            raise TypeError('Status must be a integer.')
        if status not in APPLE_API_STATUS_INFO:
            raise AppleManagerStatusError(f'Status {status} is not a Apple valid status.')
        return APPLE_API_STATUS_INFO[status]

    @classmethod
    def sort_list_by_parameter_name(cls, receipt_list, parameter_name, reverse=False):
        if not isinstance(receipt_list, list) or len(receipt_list) == 0:
            raise TypeError('receipt_list parameter needs to be a not empty list object')
        try:
            return sorted(receipt_list, key=lambda receipt: getattr(receipt, parameter_name), reverse=reverse)
        except BaseException as exc:
            raise AppleManagerInternalError('Error during sorts') from exc
