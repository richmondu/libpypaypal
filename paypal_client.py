import paypalrestsdk
from paypalrestsdk import BillingPlan, BillingAgreement
from paypal_config import config as paypal_config
from datetime import datetime, timedelta




class paypal_client:

	def __init__(self):
		self.configuration = {
			"mode": paypal_config.CONFIG_MODE,
			"client_id": paypal_config.CONFIG_CLIENT_ID,
			"client_secret": paypal_config.CONFIG_CLIENT_SECRET 
		}

	def initialize(self):
		paypalrestsdk.configure(self.configuration)	

	def create_payment(self, return_url, cancel_url, item_price, item_currency, item_quantity, item_name, item_sku, item_description):
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
						"sku": item_sku,
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



	def create_billing_plan(self, return_url, cancel_url, item_price, num_cycles, frequency):
		plan = {
			"description": "Basic Plan subscription",
			"merchant_preferences": {
				"auto_bill_amount": "yes",
				"cancel_url": cancel_url,
				"initial_fail_amount_action": "continue",
				"max_fail_attempts": "2",
				"return_url": return_url,
			},
			"name": "Basic Plan subscription",
			"payment_definitions": [
				{
					"amount": {
						"currency": "USD",
						"value": str(item_price)
					},
					"cycles": str(num_cycles),
					"frequency": frequency,
					"frequency_interval": "1",
					"name": "REGULAR 1",
					"type": "REGULAR"
				}
			],
			"type": "FIXED"
		}
		billing_plan = BillingPlan(plan)
		if billing_plan.create():
			#print("Billing Plan {} creation successful!".format(billing_plan.id))
			if billing_plan.activate():
				#print("Billing Plan {} activation successful {}".format(billing_plan.id, billing_plan.state))
				pass
			else:
				print("Billing Plan activation failed! {}".format(billing_plan.error))
		else:
			print("Billing Plan creation failed!".format(billing_plan.error))
		return billing_plan.id

	def find_billing_plan(self, billing_plan_id):
		billing_plan = BillingPlan.find(billing_plan_id)
		return billing_plan

	def get_all_billing_plans(self):
		history = BillingPlan.all({"status": "ACTIVE", "sort_order": "DESC"})
		#if history:
		#	for plan in history.plans:
		#		print("{}".format(plan.id))
		return history



	def create_billing_agreement(self, billing_plan_id):
		agreement = {
			"name": "Agreement for Basic Plan subscription",
			"description": "Agreement for Basic Plan subscription",
			"start_date": (datetime.now()+timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%SZ'),
			"plan": {
				"id": billing_plan_id
			},
			"payer": {
				"payment_method": "paypal"
			},
		}
		billing_agreement = BillingAgreement(agreement)
		if billing_agreement.create():
			print("Billing Agreement creation successful! {}".format(billing_agreement.id))
			print(billing_agreement)
			for link in billing_agreement.links:
				print(link.rel)
				print(link.href)
				if link.rel == "approval_url":
					approval_url = link.href
					print(approval_url)
		else:
			print("Billing Agreement creation failed! {}".format(billing_agreement.error))
		return billing_agreement

	def get_billing_agreement_link(self, billing_agreement):
		for link in billing_agreement.links:
			if link.rel == "approval_url":
				return link.href
		return None

	def execute_billing_agreement(self, payment_token):
		billing_agreement_response = BillingAgreement.execute(payment_token)
		print(billing_agreement_response)
		print(billing_agreement_response.id)
		return billing_agreement_response

	def get_billing_agreement(self, agreement_id):
		billing_agreement = BillingAgreement.find(agreement_id)
		return billing_agreement

	def cancel_billing_agreement(self, billing_agreement):
		note = {"note": "Canceling the agreement"}
		if billing_agreement.cancel(note):
			# Would expect status has changed to Cancelled
			billing_agreement = BillingAgreement.find(billing_agreement.id)
			print("Billing Agreement cancellation successful! {} {}".format(billing_agreement.id, billing_agreement.state))
		else:
			print("Billing Agreement cancellation failed! {}".format(billing_agreement.error))

	def suspend_billing_agreement(self, billing_agreement):
		note = {"note": "Suspending the agreement"}
		if billing_agreement.suspend(note):
			# Would expect status has changed to Suspended
			billing_agreement = BillingAgreement.find(billing_agreement.id)
			print("Billing Agreement suspension successful! {} {}".format(billing_agreement.id, billing_agreement.state))
		else:
			print("Billing Agreement suspension failed! {}".format(billing_agreement.error))

	def reactivate_billing_agreement(self, billing_agreement):
		note = {"note": "Reactivating the agreement"}
		if billing_agreement.reactivate(note):
			# Would expect status has changed to Active
			billing_agreement = BillingAgreement.find(billing_agreement.id)
			print("Billing Agreement reactivation successful! {} {}".format(billing_agreement.id, billing_agreement.state))
		else:
			print("Billing Agreement reactivation failed! {}".format(billing_agreement.error))

	def set_and_bill_balance_billing_agreement(self, billing_agreement):
		outstanding_amount = {
			"value": "10",
			"currency": "USD"
		}
		if billing_agreement.set_balance(outstanding_amount):
			billing_agreement = BillingAgreement.find(billing_agreement.id)
			print("Billing Agreement set_balance successful! {} {}".format(billing_agreement.id, billing_agreement.outstanding_balance.value))

			outstanding_amount_note = {
				"note": "Billing Balance Amount",
				"amount": outstanding_amount
			}

			if billing_agreement.bill_balance(outstanding_amount_note):
				billing_agreement = BillingAgreement.find(billing_agreement.id)
				print("Billing Agreement bill_balance successful! {}".format(billing_agreement.outstanding_balance.value))
			else:
				print("Billing Agreement bill_balance failed! {}".format(billing_agreement.error))
		else:
			print("Billing Agreement set_balance failed! {}".format(billing_agreement.error))

	def search_transaction_billing_agreement(self, billing_agreement, start_date, end_date):
		#start_date = "2014-07-01"
		#end_date = "2014-07-20"
		transactions = billing_agreement.search_transactions(start_date, end_date)
		for transaction in transactions.agreement_transaction_list:
			print("  -> Transaction[%s]" % (transaction.transaction_id))

		return transactions
