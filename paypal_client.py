import paypalrestsdk
from paypal_config import config as paypal_config




class paypal_client:

	def __init__(self):
		self.configuration = {
			"mode": paypal_config.CONFIG_MODE,
			"client_id": paypal_config.CONFIG_CLIENT_ID,
			"client_secret": paypal_config.CONFIG_CLIENT_SECRET 
		}

	def initialize(self):
		paypalrestsdk.configure(self.configuration)	

	def create_payment(self, return_url, cancel_url, item_price, item_currency, item_quantity, item_name, item_description):
		payment_object = {
			"intent": "sale",
			"payer": 
			{
				"payment_method": "paypal"
			},
			"redirect_urls": 
			{
				"return_url": return_url,
				"cancel_url": cancel_url
			},
			"transactions": [
			{
				"item_list": 
				{
					"items": [
					{
						"name": item_name,
						"sku": "item",
						"price": item_price,
						"currency": item_currency,
						"quantity": item_quantity
					}]
				},
				"amount": {
					"total": str(float(item_price) * item_quantity),
					"currency": item_currency
				},
				"description": item_description
			}
			]
		}
		return payment_object
		
	def send_payment(self, payment_object):
		payment = paypalrestsdk.Payment(payment_object)
		if payment.create():
			return (True, payment)
		else:
			return (False, payment)

	def get_payment_link(self, payment):
		for link in payment.links:
			if link.rel == "approval_url":
				approval_url = str(link.href)
				return approval_url

	def execute_payment(self, payment_id, payer_id):
		payment = paypalrestsdk.Payment.find(payment_id)
		result = payment.execute({"payer_id": payer_id})
		return result

	def fetch_payment(self, payment_id):
		payment_result = paypalrestsdk.Payment.find(payment_id)
		return payment_result

	def get_payment_status(self, payment_result):
		return payment_result["state"]
	
	def display_payment_result(self, payment_result):
		print(payment_result)
		print(payment_result["id"])
		print(payment_result["intent"])
		print(payment_result["state"]) # created or approved
		print(payment_result["cart"])

		print(payment_result["payer"]["payment_method"])
		print(payment_result["payer"]["status"])
		print(payment_result["payer"]["payer_info"]["email"])
		print(payment_result["payer"]["payer_info"]["first_name"])
		print(payment_result["payer"]["payer_info"]["last_name"])
		print(payment_result["payer"]["payer_info"]["payer_id"])
		print(payment_result["payer"]["payer_info"]["shipping_address"]["recipient_name"])
		print(payment_result["payer"]["payer_info"]["shipping_address"]["line1"])
		print(payment_result["payer"]["payer_info"]["shipping_address"]["city"])
		print(payment_result["payer"]["payer_info"]["shipping_address"]["state"])
		print(payment_result["payer"]["payer_info"]["shipping_address"]["postal_code"])
		print(payment_result["payer"]["payer_info"]["shipping_address"]["country_code"])
		if payment_result["state"] == "approved":
			print(payment_result["payer"]["payer_info"]["phone"])
		print(payment_result["payer"]["payer_info"]["country_code"])

	def get_payment_history(self):
		payment_history = paypalrestsdk.Payment.all()
		return payment_history

