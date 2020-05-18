from paypal_client import paypal_client
import webbrowser
import argparse
import sys
import json
import time
from datetime import datetime, timedelta



def print_json(json_object, is_json=True, label=None):

	if is_json:
		json_formatted_str = json.dumps(json_object, indent=2)
	else: 
		json_formatted_str = json_object
	if label is None:
		print(json_formatted_str)
	else:
		print("{}\r\n{}".format(label, json_formatted_str))


def test_billing_plan(paypal, billing_plan_id=None):

	############################################################################################################
	# Create billing plan
	############################################################################################################
	print("Create billing plan")
	if billing_plan_id is None:
		cycles = 2
		cost = 10 # 20 USD
		return_url = "http://localhost:8100/#/page_home"
		cancel_url = "http://localhost:8100/#/page_login"
		frequency = "Week"
		billing_plan_id = paypal.create_billing_plan(return_url, cancel_url, cost, cycles, frequency)
	print(billing_plan_id)
	print()


	############################################################################################################
	# Get billing plan
	############################################################################################################
	print("Get billing plan")
	billing_plan = paypal.find_billing_plan(billing_plan_id)
	print(billing_plan)
	print()
	print("id:    {}".format(billing_plan.id))
	print("state: {}".format(billing_plan.state))
	print("name:  {}".format(billing_plan.name))
	print("desc:  {}".format(billing_plan.description))
	print("type:  {}".format(billing_plan.type))
	for index in range(len(billing_plan.payment_definitions)):
		print("paydf: {}".format(billing_plan.payment_definitions[index].id))
		print("       name:   {}".format(billing_plan.payment_definitions[index].name))
		print("       type:   {}".format(billing_plan.payment_definitions[index].type))
		print("       freq:   {}".format(billing_plan.payment_definitions[index].frequency))
		print("       amount: {}".format(billing_plan.payment_definitions[index].amount))
		print("       cycles: {}".format(billing_plan.payment_definitions[index].cycles))
		print("       freqin: {}".format(billing_plan.payment_definitions[index].frequency_interval))

	print("prefs: {}".format(billing_plan.merchant_preferences))
	print("       setupfee: {}".format(billing_plan.merchant_preferences.setup_fee))
	print("       maxfail:  {}".format(billing_plan.merchant_preferences.max_fail_attempts))
	print("       returnurl:{}".format(billing_plan.merchant_preferences.return_url))
	print("       cancelurl:{}".format(billing_plan.merchant_preferences.cancel_url))
	print("       autobill: {}".format(billing_plan.merchant_preferences.auto_bill_amount))
	print("       failact:  {}".format(billing_plan.merchant_preferences.initial_fail_amount_action))

	print("create:{}".format(billing_plan.create_time))
	print("update:{}".format(billing_plan.update_time))
	print("links: {}".format(billing_plan.links[0].href))
#	print_json(json.dumps(billing_plan, default=lambda x: getattr(x, '__dict__', str(x))), is_json=False)
	print()


	############################################################################################################
	# Get billing plans
	############################################################################################################
	print("Get billing plans")
	billing_plans = paypal.get_all_billing_plans()
	print(len(billing_plans.plans))
	print(billing_plans.to_dict().get('plans'))
	print()

	return billing_plan_id


def test_billing_agreement(paypal, billing_plan_id):

	print("Create billing agreement")
	billing_agreement = paypal.create_billing_agreement(billing_plan_id)
	print(billing_agreement.id)
	print()

	print("Get billing agreement approval url")
	approval_url = paypal.get_billing_agreement_link(billing_agreement)
	time.sleep(3)
	print(approval_url)
	print()

	print("Open billing agreement approval url")
	webbrowser.open_new_tab(approval_url)


def test_billing_agreement2(paypal, payment_token):

	print("Execute billing agreement")
	agreement = paypal.execute_billing_agreement(payment_token)
	print(agreement)
	print()
	print('billing_agreement.id:    {}'.format(agreement.id))
	print('billing_agreement.state: {}'.format(agreement.state)) # Active, Expired, Cancelled
	print('agreement_details')
	print('  outstanding_balance:   {}'.format(agreement.agreement_details.outstanding_balance))
	print('  cycles_remaining:      {}'.format(agreement.agreement_details.cycles_remaining))
	print('  cycles_completed:      {}'.format(agreement.agreement_details.cycles_completed))
	print('  next_billing_date:     {}'.format(agreement.agreement_details.next_billing_date))
	print('  final_payment_date:    {}'.format(agreement.agreement_details.final_payment_date))
	print()

	print("Get billing agreement details")
	billing_agreement = paypal.get_billing_agreement(agreement.id)
	print(billing_agreement)
	print()
	print('billing_agreement.id:    {}'.format(billing_agreement.id))
	print('billing_agreement.state: {}'.format(billing_agreement.state)) # Active, Expired, Cancelled
	print('agreement_details')
	print('  outstanding_balance:   {}'.format(billing_agreement.agreement_details.outstanding_balance))
	print('  cycles_remaining:      {}'.format(billing_agreement.agreement_details.cycles_remaining))
	print('  cycles_completed:      {}'.format(billing_agreement.agreement_details.cycles_completed))
	print('  next_billing_date:     {}'.format(billing_agreement.agreement_details.next_billing_date))
	print('  final_payment_date:    {}'.format(billing_agreement.agreement_details.final_payment_date))
	print()

	return agreement.id


def test_billing_agreement3(paypal, billing_agreement_id):

	print("Get billing agreement details")
	billing_agreement = paypal.get_billing_agreement(billing_agreement_id)
	print(billing_agreement)
	print()
	print('billing_agreement.id:    {}'.format(billing_agreement.id))
	print('billing_agreement.state: {}'.format(billing_agreement.state)) # Active, Expired, Cancelled
	print('agreement_details')
	print('  outstanding_balance:   {}'.format(billing_agreement.agreement_details.outstanding_balance))
	print('  cycles_remaining:      {}'.format(billing_agreement.agreement_details.cycles_remaining))
	print('  cycles_completed:      {}'.format(billing_agreement.agreement_details.cycles_completed))
	print('  next_billing_date:     {}'.format(billing_agreement.agreement_details.next_billing_date))
	print('  final_payment_date:    {}'.format(billing_agreement.agreement_details.final_payment_date))
	print()

	return billing_agreement


def main(args):

	# Initialize Paypal library
	paypal = paypal_client()
	paypal.initialize()

	# Test billing plan
	if False:
		billing_plan_id = None
		#billing_plan_id = "P-16M72792HD966615D5U5FR3Y"
		#billing_plan_id = "P-7T749692H6799363N5XYJK6Q"
		billing_plan_id = test_billing_plan(paypal, billing_plan_id)

	if False:
		# Test billing arrangement
		test_billing_agreement(paypal, billing_plan_id)
	elif False:
		# Test execute payment for billing arrangement
		#http://localhost:8100/#/page_home?token=EC-4K4649941E066572A&ba_token=BA-42W12302K1887801T
		#payment_token = 'EC-4K4649941E066572A'

		#http://localhost:8100/#/page_home?token=EC-4LG2625218927020W&ba_token=BA-78M9460303066462A
		#payment_token = 'EC-4LG2625218927020W'
		#payment_token = 'EC-1F794124WR040513S'
		payment_token='EC-70U044870H253582A'
		agreement_id = test_billing_agreement2(paypal, payment_token)
	elif True:
		agreement_id = "I-AFP8LJ3CRFHL"
		billing_agreement = test_billing_agreement3(paypal, agreement_id)
		transactions = paypal.search_transaction_billing_agreement(billing_agreement, "2020-05-06", "2020-05-08")
		print(transactions)
		print()

		agreement_id = "I-HKFTB2F8JJ08"
		billing_agreement = test_billing_agreement3(paypal, agreement_id)
		transactions = paypal.search_transaction_billing_agreement(billing_agreement, "2020-05-06", "2020-05-08")
		print(transactions)
		print()

		agreement_id = "I-SD6X0RDVVHRX"
		billing_agreement = test_billing_agreement3(paypal, agreement_id)
		transactions = paypal.search_transaction_billing_agreement(billing_agreement, "2020-05-06", "2020-05-08")
		print(transactions)
		print()

	if True:
		now = datetime.now()
		utcnow = datetime.utcnow()
		print(now.strftime('%Y-%m-%dT%H:%M:%SZ'))
		print((now+timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%SZ'))

		print(utcnow.strftime('%Y-%m-%dT%H:%M:%SZ'))
		print((utcnow+timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%SZ'))

if __name__ == '__main__':

	main(sys.argv[1:])



