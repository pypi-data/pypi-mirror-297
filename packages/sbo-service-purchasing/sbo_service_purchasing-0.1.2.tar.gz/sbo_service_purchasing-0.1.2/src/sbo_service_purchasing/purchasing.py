#! /usr/bin/python3
"""
Purchase related wrappers
"""
from sbo_service.service import Service


class Purchase(Service):
    def __init__(self,
                 usr=None,
                 pwrd=None,
                 compDB=None,
                 srvr=None,
                 prt=50000):
        Service.__init__(self,
                         usr,
                         pwrd,
                         compDB,
                         srvr,
                         prt)

        self.login()

    # purchase orders
    def create_purchase_order(self,
                              doc_info: dict):
        e_type = self.entity('purchase orders')

        return self.create_document(e_type,
                                    doc_info)

    def read_purchase_orders(self,
                             skip=None):
        e_type = self.entity('purchase orders')

        return self.read_documents(e_type,
                                   skip)

    def read_purchase_order_by_docentry(self,
                                        doc_entry: int):
        e_type = self.entity('purchase orders')

        return self.read_documents(e_type,
                                   docentry=doc_entry)

    def read_purchase_order_by_docnum(self,
                                      doc_num: int = None):
        e_type = self.entity('purchase orders')

        return self.read_documents(e_type,
                                   docnum=doc_num)

    def read_purchase_order_with_filter(self,
                                        filter: str = None):
        e_type = self.entity('purchase orders')

        return self.read_documents(e_type,
                                   filter=filter)

    def update_purchase_order(self,
                              info: dict):
        e_type = self.entity('purchase orders')

        return self.update_document(e_type,
                                    info,
                                    'DocEntry')

    def close_purchase_order(self,
                             doc_entry: int = None):
        e_type = self.entity('purchase orders')

        return self.close_document(e_type,
                                   doc_entry)

    def cancel_purchase_order(self,
                              doc_entry: int = None):
        e_type = self.entity('purchase orders')

        return self.cancel_document(e_type,
                                    doc_entry)

    # receipt of goods
    def create_goods_receipts(self,
                              doc_info: dict):
        e_type = self.entity('receipt of goods')

        return self.create_document(e_type,
                                    doc_info)

    def read_goods_receipts(self,
                            skip=None):
        e_type = self.entity('receipt of goods')

        return self.read_documents(e_type,
                                   skip)

    def read_goods_receipt_by_docentry(self,
                                       doc_entry: int):
        e_type = self.entity('receipt of goods')

        return self.read_documents(e_type,
                                   docentry=doc_entry)

    def read_goods_receipt_by_docnum(self,
                                     doc_num: int = None):
        e_type = self.entity('receipt of goods')

        filter = f'DocNum eq {doc_num}'

        return self.read_documents(e_type,
                                   filter=filter)

    def read_goods_receipts_with_filter(self,
                                        filter: str = None):
        e_type = self.entity('receipt of goods')

        return self.read_documents(e_type,
                                   filter=filter)

    def update_goods_receipts(self,
                              info: dict):
        e_type = self.entity('receipt of goods')

        return self.update_document(e_type,
                                    info,
                                    'DocEntry')

    def close_goods_receipts(self,
                             doc_entry: dict = None):
        e_type = self.entity('receipt of goods')

        return self.close_document(e_type,
                                   docentry=doc_entry)

    def cancel_goods_receipts(self,
                              doc_entry: int = None):
        e_type = self.entity('receipt of goods')

        return self.cancel_document(e_type, docentry=doc_entry)

    # purchase returns
    def create_return(self,
                      doc_info: dict):
        e_type = self.entity('purchase returns')

        return self.create_document(e_type,
                                    doc_info)

    def read_returns(self,
                     skip=None):
        e_type = self.entity('purchase returns')

        return self.read_documents(e_type,
                                   skip)

    def read_return_by_docentry(self,
                                doc_entry: int):
        e_type = self.entity('purchase returns')

        return self.read_documents(e_type,
                                   docentry=doc_entry)

    def read_return_by_docnum(self,
                              doc_num: int = None):
        e_type = self.entity('purchase returns')

        filter = f'DocNum eq {doc_num}'

        return self.read_documents(e_type,
                                   filter=filter)

    def read_returns_with_filter(self,
                                 filter: str = None):
        e_type = self.entity('purchase returns')

        return self.read_documents(e_type,
                                   filter=filter)

    def update_return(self,
                      info: dict):
        e_type = self.entity('purchase returns')

        return self.update_document(e_type,
                                    info,
                                    'DocEntry')

    def close_return(self,
                     doc_entry: int = None):
        e_type = self.entity('purchase returns')

        return self.close_document(e_type,
                                   docentry=doc_entry)

    def cancel_return(self,
                      doc_entry: int = None):
        e_type = self.entity('purchase returns')

        return self.cancel_document(e_type,
                                    docentry=doc_entry)

    # payable invoices
    def create_invoice(self,
                       doc_info: dict):
        e_type = self.entity('payable invoices')

        return self.create_document(e_type,
                                    doc_info)

    def read_invoices(self,
                      skip=None):
        e_type = self.entity('payable invoices')

        return self.read_documents(e_type,
                                   skip)

    def read_invoice_by_docentry(self,
                                 doc_entry: int):
        e_type = self.entity('payable invoices')

        return self.read_documents(e_type,
                                   docentry=doc_entry)

    def read_invoice_by_docnum(self,
                               doc_num: int = None):
        e_type = self.entity('payable invoices')

        filter = f'DocNum eq {doc_num}'

        return self.read_documents(e_type,
                                   filter=filter)

    def read_invoices_with_filter(self,
                                  filter: str = None):
        e_type = self.entity('payable invoices')

        return self.read_documents(e_type,
                                   filter=filter)

    def update_invoice(self,
                       info: dict):
        e_type = self.entity('payable invoices')

        return self.update_document(e_type,
                                    info,
                                    'DocEntry')

    def cancel_invoice(self,
                       doc_entry: int = None):
        e_type = self.entity('payable invoices')

        return self.cancel_document(e_type,
                                    docentry=doc_entry)

    # purchase credits
    def create_credit_note(self,
                           doc_info: dict,
                           force_log=False):
        e_type = self.entity('purchase credits')

        return self.create_document(e_type,
                                    doc_info,
                                    force_log)

    def read_credit_notes(self,
                          skip=None):
        e_type = self.entity('purchase credits')

        return self.read_documents(e_type,
                                   skip=skip)

    def read_credit_note_by_docentry(self,
                                     doc_entry: int):
        e_type = self.entity('purchase credits')

        return self.read_documents(e_type,
                                   docentry=doc_entry)

    def read_credit_note_by_docnum(self,
                                   docnum: int = None):
        e_type = self.entity('purchase credits')

        filter = f'DocNum eq {docnum}'

        return self.read_documents(e_type,
                                   filter=filter)

    def read_credit_notes_with_filter(self,
                                      filter: str = None):
        e_type = self.entity('purchase credits')

        return self.read_documents(e_type,
                                   filter=filter)

    def update_credit_note(self,
                           info: dict):
        e_type = self.entity('purchase credits')

        return self.update_document(e_type,
                                    info,
                                    'DocEntry')

    def cancel_credit_note(self,
                           doc_entry: int = None):
        e_type = self.get('purchase credits')

        return self.cancel_document(e_type,
                                    docentry=doc_entry)

    # payable down payments
    # purchase quotes
    # purchase requests
    # payable tax invoices
