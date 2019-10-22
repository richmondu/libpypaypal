from paypal_client import paypal_client
import webbrowser
import argparse
import sys



# Default configuration values
CONFIG_MODE = 0
CONFIG_RETURN_URL = "http://localhost:8100/#/page_home"
CONFIG_CANCEL_URL = "http://localhost:8100/#/page_home"
CONFIG_PAYMENT_ID = "PAYID-LWPNLEY6MH86403AS8631242"
CONFIG_PAYER_ID   = "KZ93QYTD9WRAY"



def parse_arguments(argv):

	parser = argparse.ArgumentParser()
	parser.add_argument('--USE_MODE',       required=True,  default=0, help='0 for create payment, 1 for execute payment, 2 for check payment history')
	parser.add_argument('--USE_RETURN_URL', required=False, default="None", help='return url to use')
	parser.add_argument('--USE_CANCEL_URL', required=False, default="None", help='cancel url id to use')
	parser.add_argument('--USE_PAYMENT_ID', required=False, default="None", help='payment id to use')
	parser.add_argument('--USE_PAYER_ID',   required=False, default="None", help='payer id to use')
	return parser.parse_args(argv)


def main(args):

	CONFIG_MODE       = int(args.USE_MODE)
	CONFIG_RETURN_URL = args.USE_RETURN_URL
	CONFIG_CANCEL_URL = args.USE_CANCEL_URL
	CONFIG_PAYMENT_ID = args.USE_PAYMENT_ID
	CONFIG_PAYER_ID   = args.USE_PAYER_ID

	# Initialize Paypal library
	paypal = paypal_client()
	paypal.initialize()

	# Initialize payment then open link to paypal
	if CONFIG_MODE == 1:
		return_url = CONFIG_RETURN_URL
		cancel_url = CONFIG_CANCEL_URL
		item_price = "7.00"
		item_currency = "USD"
		item_quantity = 1
		item_name = "Premium Membership"
		item_sku = "CREDITX7USD"
		item_description = "Monthly subscription for premium access"

		payment_object = paypal.create_payment(return_url, cancel_url, item_price, item_currency, item_quantity, item_name, item_sku, item_description)
		#print(payment_object)
		(status, payment) = paypal.send_payment(payment_object)
		if not status:
			print("Payment creation failed! {}".format(payment.error))
			return
		approval_url = paypal.get_payment_link(payment)
		print("\r\nPayment creation successful!\r\n")

		data = {
			"paymentId": payment["id"],
			"token": approval_url[approval_url.find("token=")+len("token="):],
			"create_time": payment["create_time"],
			"sku": item_sku,
		}
		print(data)

		# Open browser
		webbrowser.open_new_tab(approval_url)
		print("\r\nOpening browser for payment approval!\r\n{}".format(approval_url))


	# Once user completes payment, the registered callback URL is called with the Payment ID and Payer ID
	# Ex. http://localhost:8100/#/page_home?paymentId=PAYID-LWPNLEY6MH86403AS8631242&token=EC-6DA33251UW9273633&PayerID=KZ93QYTD9WRAY
	# Parse the PaymentID and PayerID then execute the payment and verify the result
	# Get "paymentID" and "PayerID" parameters from return_url parameter
	# Sample when user cancelled:
	#	URL: http://localhost:8100/#/page_home
	#	Result: http://localhost:8100/#/page_home?token=EC-2PA77635SA4416611
	# Sample when user approved:
	#	URL: http://localhost:8100/#/page_home
	#	Result: http://localhost:8100/#/page_home?paymentId=PAYID-LWPMDPQ1L2215833N9046355&token=EC-2PA77635SA4416611&PayerID=KZ93QYTD9WRAY
	elif CONFIG_MODE == 2:
		payment_id = CONFIG_PAYMENT_ID
		payer_id = CONFIG_PAYER_ID
		result = paypal.execute_payment(payment_id, payer_id)
		if not result:
			print("Payment failed! {}".format(payment.error))
			return

		payment_result = paypal.fetch_payment(payment_id)
		status = paypal.get_payment_status(payment_result)
		if status != "approved":
			print("Payment not yet completed! {}".format(status))
			return

		print("Payment completed successfully!")
		paypal.display_payment_result(payment_result)


	# Get history of successful payment transaction
	elif CONFIG_MODE == 3:
		payment_history = paypal.get_payment_history()
		print(len(payment_history.payments));
		print(payment_history.payments);


if __name__ == '__main__':

	main(parse_arguments(sys.argv[1:]))



