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
		frequency = "WEEK"
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
	print("paydf: {}".format(billing_plan.payment_definitions[0].id))
	print("       name:   {}".format(billing_plan.payment_definitions[0].name))
	print("       type:   {}".format(billing_plan.payment_definitions[0].type))
	print("       freq:   {}".format(billing_plan.payment_definitions[0].frequency))
	print("       amount: {}".format(billing_plan.payment_definitions[0].amount))
	print("       cycles: {}".format(billing_plan.payment_definitions[0].cycles))
	print("       freqin: {}".format(billing_plan.payment_definitions[0].frequency_interval))

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
	print('billing_agreement.id:  {}'.format(agreement.id))
	print('agreement_details')
	print('  outstanding_balance: {}'.format(agreement.agreement_details.outstanding_balance))
	print('  cycles_remaining:    {}'.format(agreement.agreement_details.cycles_remaining))
	print('  cycles_completed:    {}'.format(agreement.agreement_details.cycles_completed))
	print('  next_billing_date:   {}'.format(agreement.agreement_details.next_billing_date))
	print('  final_payment_date:  {}'.format(agreement.agreement_details.final_payment_date))
	print()

	print("Get billing agreement details")
	billing_agreement = paypal.get_billing_agreement_details(agreement.id)
	print(billing_agreement)
	print()
	print('billing_agreement.id:  {}'.format(billing_agreement.id))
	print('agreement_details')
	print('  outstanding_balance: {}'.format(billing_agreement.agreement_details.outstanding_balance))
	print('  cycles_remaining:    {}'.format(billing_agreement.agreement_details.cycles_remaining))
	print('  cycles_completed:    {}'.format(billing_agreement.agreement_details.cycles_completed))
	print('  next_billing_date:   {}'.format(billing_agreement.agreement_details.next_billing_date))
	print('  final_payment_date:  {}'.format(billing_agreement.agreement_details.final_payment_date))
	print()

	return agreement.id


def test_billing_agreement3(paypal, billing_agreement_id):

	print("Get billing agreement details")
	billing_agreement = paypal.get_billing_agreement_details(billing_agreement_id)
	print(billing_agreement)
	print()
	print('billing_agreement.id:  {}'.format(billing_agreement.id))
	print('agreement_details')
	print('  outstanding_balance: {}'.format(billing_agreement.agreement_details.outstanding_balance))
	print('  cycles_remaining:    {}'.format(billing_agreement.agreement_details.cycles_remaining))
	print('  cycles_completed:    {}'.format(billing_agreement.agreement_details.cycles_completed))
	print('  next_billing_date:   {}'.format(billing_agreement.agreement_details.next_billing_date))
	print('  final_payment_date:  {}'.format(billing_agreement.agreement_details.final_payment_date))
	print()

	return billing_agreement


def main(args):

	# Initialize Paypal library
	paypal = paypal_client()
	paypal.initialize()

	# Test billing plan
	if False:
		billing_plan_id = None
		billing_plan_id = test_billing_plan(paypal, billing_plan_id)

	if False:
		# Test billing arrangement
		test_billing_agreement(paypal, billing_plan_id)
	elif False:
		# Test execute payment for billing arrangement
		agreement_id = test_billing_agreement2(paypal, payment_token)
	elif False:
		billing_agreement = test_billing_agreement3(paypal, agreement_id)


if __name__ == '__main__':

	main(sys.argv[1:])



