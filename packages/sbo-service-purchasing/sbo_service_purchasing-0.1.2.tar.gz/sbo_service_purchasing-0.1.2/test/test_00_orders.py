#! /usr/bin/python3
from sbo_service_purchasing.purchasing import Purchase

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
    purch = Purchase(user, password, company, server)

    action = purch.create_purchase_order(purchase_order)

    purch.logout()

    assert action['success'], action['error_message']


def test_read_purchase_order(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    purch = Purchase(user, password, company, server)

    action = purch.read_purchase_orders()

    purch.logout()

    assert action['success'], action['error_message']


def test_read_purchase_order_by_docentry(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    purch = Purchase(user, password, company, server)

    action = purch.create_purchase_order(purchase_order)

    data = action['data'][0]
    doc_entry = data['DocEntry']

    action = purch.read_purchase_order_by_docentry(doc_entry)

    purch.logout()

    assert action['success'], action['error_message']


def test_read_purchase_order_by_docnum(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    purch = Purchase(user, password, company, server)

    action = purch.create_purchase_order(purchase_order)

    data = action['data'][0]
    doc_num = data['DocNum']

    action = purch.read_purchase_order_by_docnum(doc_num)

    purch.logout()

    assert action['success'], action['error_message']


def test_read_purchase_order_with_filter(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    purch = Purchase(user, password, company, server)

    filter = '(CardCode eq \'V999999999\')'

    action = purch.read_purchase_order_with_filter(filter)

    purch.logout()

    assert action['success'], action['error_message']


def test_update_purchase_order(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    purch = Purchase(user, password, company, server)

    action = purch.create_purchase_order(purchase_order)

    data = action['data'][0]
    doc_entry = data['DocEntry']

    updated_data = {
        'DocEntry': doc_entry,
        'Comments': 'Added a comment'
    }

    action = purch.update_purchase_order(updated_data)

    purch.logout()

    assert action['success'], action['error_message']


def test_close_purchase_order(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    purch = Purchase(user, password, company, server)

    action = purch.create_purchase_order(purchase_order)

    data = action['data'][0]
    doc_entry = data['DocEntry']

    action = purch.close_purchase_order(doc_entry)

    purch.logout()

    assert action['success'], action['error_message']


def test_cancel_purchase_order(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    purch = Purchase(user, password, company, server)

    action = purch.create_purchase_order(purchase_order)

    data = action['data'][0]
    doc_entry = data['DocEntry']

    action = purch.cancel_purchase_order(doc_entry)

    purch.logout()

    assert action['success'], action['error_message']
