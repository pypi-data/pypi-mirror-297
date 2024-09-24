#! /usr/bin/python3
import sbo_service.service as service
import sbo_service_purchasing.purchasing as purchasing

import os
from dotenv import load_dotenv
from datetime import date

load_dotenv()

test_user = os.getenv('test_user')
test_pass = os.getenv('test_pass')
test_comp = os.getenv('test_comp')
test_serv = os.getenv('test_serv')

today = date.today()

doc_date = today.strftime('%Y%m%d')

purchase_order = {
    'DoctType': 'dDocument_Items',
    'DocDate': doc_date,
    'DocDueDate': doc_date,
    'CardCode': 'V999999999',
    'DocumentLines': [
        {
            'ItemCode': '7896300',
            'Quantity': 10
        }
    ]
}

failure = {
    'success': False,
    'error_message': 'Test not yet configured'
}


def test_create_purchase_order(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    service.initialize(user, password, company, server)
    service.login()

    action = purchasing.create_purchase_order(service, purchase_order)

    service.logout()

    assert action['success'], action['error_message']


def test_read_purchase_order(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    service.initialize(user, password, company, server)
    service.login()

    action = purchasing.read_purchase_orders(service)

    service.logout()

    assert action['success'], action['error_message']


def test_read_purchase_order_by_docentry(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    service.initialize(user, password, company, server)
    service.login()

    action = purchasing.create_purchase_order(service, purchase_order)

    data = action['data'][0]
    doc_entry = data['DocEntry']

    action = purchasing.read_purchase_order_by_docentry(service, doc_entry)

    service.logout()

    assert action['success'], action['error_message']


def test_read_purchase_order_by_docnum(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    service.initialize(user, password, company, server)
    service.login()

    action = purchasing.create_purchase_order(service, purchase_order)

    data = action['data'][0]
    doc_num = data['DocNum']

    action = purchasing.read_purchase_order_by_docnum(service, doc_num)

    service.logout()

    assert action['success'], action['error_message']


def test_read_purchase_order_with_filter(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    service.initialize(user, password, company, server)
    service.login()

    filter = '(CardCode eq \'V999999999\')'

    action = purchasing.read_purchase_order_with_filter(service, filter)

    service.logout()

    assert action['success'], action['error_message']


def test_update_purchase_order(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    service.initialize(user, password, company, server)
    service.login()

    action = purchasing.create_purchase_order(service, purchase_order)

    data = action['data'][0]
    doc_entry = data['DocEntry']

    updated_data = {
        'DocEntry': doc_entry,
        'Comments': 'Added a comment'
    }

    action = purchasing.update_purchase_order(service, updated_data)

    service.logout()

    assert action['success'], action['error_message']


def test_close_purchase_order(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    service.initialize(user, password, company, server)
    service.login()

    action = purchasing.create_purchase_order(service, purchase_order)

    data = action['data'][0]
    doc_entry = data['DocEntry']

    action = purchasing.close_purchase_order(service, doc_entry)

    service.logout()

    assert action['success'], action['error_message']


def test_cancel_purchase_order(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    service.initialize(user, password, company, server)
    service.login()

    action = purchasing.create_purchase_order(service, purchase_order)

    data = action['data'][0]
    doc_entry = data['DocEntry']

    action = purchasing.cancel_purchase_order(service, doc_entry)

    service.logout()

    assert action['success'], action['error_message']
