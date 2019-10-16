# libpypaypal

libpypaypal demonstrates usage of Paypal's Python SDK for processing online payments.


Integrating <b>Paypal</b> payment gateway is easier than we thought. Paypal provides a Python SDK together with Sandbox accounts to make it easy for developers to integrate and test. 

I tried <b>Stripe</b> but Stripe requires activating account by putting in business name, bank information, SG NRIC/FIN, etc to get an API key. The API key is needed to call the APIs. So I can't experiment with the APIs because I don't have an API key. Paypal is a lot more developer friendly.


### Instructions:

A. Setup Paypal Sandbox accounts
1. Login to https://developer.paypal.com
2. Create a Sandbox Business account (for seller) and a Sandbox Personal account (for test buyer).
3. Create a Sandbox App linked to a Sandbox business account.
   Copy the credentials: Client ID and Secret, to be used in the Paypal Python SDK. 

B. Code flow
1. Initialize Paypal library by providing the App account credentials: Client ID and Secret.
2. Setup payment information to Paypal including a Return URL and Cancel URL callbacks.
   A URL link will be returned pointing to Paypal page that buyer must approve transaction.
   Once customer cancels or approves the payment, the Return URL or Cancel URL will be called.
   If successful, the Return URL is called with the information of PayerID and PaymentID.
3. Execute payment with the specified PayerID and PaymentID.
4. Login to https://sandbox.paypal.com/
   Check Sandbox Business account (for seller) to confirm the transaction and amount is credited.
   Check Sandbox Personal account (for test buyer) to confirm the transaction and amount is debited.

C. Moving from Sandbox to Live:
1. Developer account needs to be upgraded from personal account to business account.
2. Similar as above but replace Sandbox to Live


### Resources:

1. Paypal Python SDK v2 https://github.com/paypal/Checkout-Python-SDK
2. Paypal Python SDK v1 https://github.com/paypal/PayPal-Python-SDK
3. Paypal Server integration https://developer.paypal.com/docs/checkout/reference/server-integration/#use-cases
4. Paypal Developer website https://developer.paypal.com/
5. Paypal Sandbox website https://sandbox.paypal.com/

