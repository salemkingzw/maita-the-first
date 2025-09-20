from paynow import Paynow
import time

paynow = Paynow(
    'INTEGRATION_ID', 
    'INTEGRATION_KEY',
    'http://google.com', 
    'http://google.com'
    )

payment = paynow.create_payment('Order', 'test@example.com')

payment.add('Payment for stuff', 1)

response = paynow.send_mobile(payment, '0775749445', 'ecocash')


if(response.success):
    poll_url = response.poll_url

    print("Poll Url: ", poll_url)

    status = paynow.check_transaction_status(poll_url)

    time.sleep(30)

    print("Payment Status: ", status.status)
