#! /usr/bin/python3
"""
Sales related wrappers
"""

import sbo_service.service as service

import os

from dotenv import load_dotenv


# purchase orders
def create_purchase_order(sbo: service, doc_info):
    e_type = service.entities.get('purchase orders')

    return sbo.create_document(e_type, doc_info)


def read_purchase_orders(sbo: service, skip=None):
    e_type = service.entities.get('purchase orders')

    return sbo.read_documents(e_type, skip)


def read_purchase_order_by_docentry(sbo: service, doc_entry):
    e_type = service.entities.get('purchase orders')

    return sbo.read_documents(e_type, docentry=doc_entry)


def read_purchase_order_by_docnum(sbo: service, doc_num=None):
    e_type = service.entities.get('purchase orders')

    return sbo.read_documents(e_type, docnum=doc_num)


def read_purchase_order_with_filter(sbo: service, filter=None):
    e_type = service.entities.get('purchase orders')

    return sbo.read_documents(e_type, filter=filter)


def update_purchase_order(sbo: service, info):
    e_type = service.entities.get('purchase orders')

    return sbo.update_document(e_type, info, 'DocEntry')


def close_purchase_order(sbo: service, doc_entry=None):
    e_type = service.entities.get('purchase orders')

    return sbo.close_document(e_type, doc_entry)


def cancel_purchase_order(sbo: service, doc_entry=None):
    e_type = service.entities.get('purchase orders')

    return sbo.cancel_document(e_type, doc_entry)


# receipt of goods
def create_goods_receipts(sbo: service, doc_info):
    e_type = service.entities.get('receipt of goods')

    return sbo.create_document(e_type, doc_info)


def read_goods_receipts(sbo: service, skip=None):
    e_type = service.entities.get('receipt of goods')

    return sbo.read_documents(e_type, skip)


def read_goods_receipt_by_docentry(sbo: service, doc_entry):
    e_type = service.entities.get('receipt of goods')

    return sbo.read_documents(e_type, docentry=doc_entry)


def read_goods_receipt_by_docnum(sbo: service, doc_num=None):
    e_type = service.entities.get('receipt of goods')

    filter = f'DocNum eq {doc_num}'

    return sbo.read_documents(e_type, filter=filter)


def read_goods_receipts_with_filter(sbo: service, filter=None):
    e_type = service.entities.get('receipt of goods')

    return sbo.read_documents(e_type, filter=filter)


def update_goods_receipts(sbo: service, info):
    e_type = service.entities.get('receipt of goods')

    return sbo.update_document(e_type, info, 'DocEntry')


def close_goods_receipts(sbo: service, doc_entry=None):
    e_type = service.entities.get('receipt of goods')

    return sbo.close_document(e_type, docentry=doc_entry)


def cancel_goods_receipts(sbo: service, doc_entry=None):
    e_type = service.entities.get('receipt of goods')

    return sbo.cancel_document(e_type, docentry=doc_entry)


# purchase returns
def create_return(sbo: service, doc_info):
    e_type = service.entities.get('purchase returns')

    return sbo.create_document(e_type, doc_info)


def read_returns(sbo: service, skip=None):
    e_type = service.entities.get('purchase returns')

    return sbo.read_documents(e_type, skip)


def read_return_by_docentry(sbo: service, doc_entry):
    e_type = service.entities.get('purchase returns')

    return sbo.read_documents(e_type, docentry=doc_entry)


def read_return_by_docnum(sbo: service, doc_num=None):
    e_type = service.entities.get('purchase returns')

    filter = f'DocNum eq {doc_num}'

    return sbo.read_documents(e_type, filter=filter)


def read_returns_with_filter(sbo: service, filter=None):
    e_type = service.entities.get('purchase returns')

    return sbo.read_documents(e_type, filter=filter)


def update_return(sbo: service, info):
    e_type = service.entities.get('purchase returns')

    return sbo.update_document(e_type, info, 'DocEntry')


def close_return(sbo: service, doc_entry=None):
    e_type = service.entities.get('purchase returns')

    return sbo.close_document(e_type, docentry=doc_entry)


def cancel_return(sbo: service, doc_entry=None):
    e_type = service.entities.get('purchase returns')

    return sbo.cancel_document(e_type, docentry=doc_entry)


# payable invoices
def create_invoice(sbo: service, doc_info):
    e_type = service.entities.get('payable invoices')

    return sbo.create_document(e_type, doc_info)


def read_invoices(sbo: service, skip=None):
    e_type = service.entities.get('payable invoices')

    return sbo.read_documents(e_type, skip)


def read_invoice_by_docentry(sbo: service, doc_entry):
    e_type = service.entities.get('payable invoices')

    return sbo.read_documents(e_type, docentry=doc_entry)


def read_invoice_by_docnum(sbo: service, doc_num=None):
    e_type = service.entities.get('payable invoices')

    filter = f'DocNum eq {doc_num}'

    return sbo.read_documents(e_type, filter=filter)


def read_invoices_with_filter(sbo: service, filter=None):
    e_type = service.entities.get('payable invoices')

    return sbo.read_documents(e_type, filter=filter)


def update_invoice(sbo: service, info):
    e_type = service.entities.get('payable invoices')

    return sbo.update_document(e_type, info, 'DocEntry')


def cancel_invoice(sbo: service, doc_entry=None):
    e_type = service.entities.get('payable invoices')

    return sbo.cancel_document(e_type, docentry=doc_entry)


# purchase credits
def create_credit_note(sbo: service, doc_info, force_log=False):
    e_type = service.entities.get('purchase credits')

    return sbo.create_document(e_type, doc_info, force_log)


def read_credit_notes(sbo: service, skip=None):
    e_type = service.entities.get('purchase credits')

    return sbo.read_documents(e_type, skip=skip)


def read_credit_note_by_docentry(sbo: service, doc_entry):
    e_type = service.entities.get('purchase credits')

    return sbo.read_documents(e_type, docentry=doc_entry)


def read_credit_note_by_docnum(sbo: service, docnum=None):
    e_type = service.entities.get('purchase credits')

    filter = f'DocNum eq {docnum}'

    return sbo.read_documents(e_type, filter=filter)


def read_credit_notes_with_filter(sbo: service, filter=None):
    e_type = service.entities.get('purchase credits')

    return sbo.read_documents(e_type, filter=filter)


def update_credit_note(sbo: service, info):
    e_type = service.entities.get('purchase credits')

    return sbo.update_document(e_type, info, 'DocEntry')


def cancel_credit_note(sbo: service, doc_entry=None):
    e_type = service.entities.get('purchase credits')

    return sbo.cancel_document(e_type, docentry=doc_entry)


# payable down payments
# purchase quotes
# purchase requests
# payable tax invoices


if __name__ == '__main__':
    print('Cannot be run... This is a library')

    document = {
        'DocType': 'dDocumentItems',
        'DocDate': '20230301',
        'DocDueDate': '20230301',
        'CardCode': 'C999999999',
        'NumAtCard': 'test order...should be canceled',
        'DocumentLines': [
            {
                'ItemCode': '7896300',
                'TaxCode': 'EX',
                'Quantity': 10
            }
        ]
    }

    load_dotenv()

    test_user = os.getenv('test_user')
    test_pass = os.getenv('test_pass')
    test_comp = os.getenv('test_comp')
    test_serv = os.getenv('test_serv')

    service.initialize(test_user, test_pass, test_comp, test_serv)

    result = service.login()

    # test creation
    create = create_purchase_order(service, document)

    doc = create['data'][0]
    doc_entry = doc['DocEntry']
    doc_num = doc['DocNum']

    create.pop('data')

    if create['error']:
        print(f'Creation failed: {create["error"]}')
    else:
        print(f'Created {doc_entry} ({doc_num}): {doc}')

    result = service.logout()
