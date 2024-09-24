#! /usr/bin/python3
"""
Sales related wrappers
"""
from sbo_service.service import Service


class Sales(Service):
    svc = None

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

    def __str__(self):
        return f'Service:\n{self.svc}\n'

    def create_sales_order(self,
                           doc_info: dict):
        e_type = self.entity('sales orders')

        return self.create_document(e_type,
                                    doc_info)

    def read_sales_orders(self,
                          skip=None):
        e_type = self.entity('sales orders')

        return self.read_documents(e_type,
                                   skip)

    def read_sales_order_by_docentry(self,
                                     doc_entry: int):
        e_type = self.entity('sales orders')

        return self.read_documents(e_type,
                                   docentry=doc_entry)

    def read_sales_order_by_docnum(self,
                                   doc_num: int = None):
        e_type = self.entity('sales orders')

        return self.read_documents(e_type,
                                   docnum=doc_num)

    def read_sales_order_with_filter(self,
                                     filter: str = None):
        e_type = self.entity('sales orders')

        return self.read_documents(e_type,
                                   filter=filter)

    def update_sales_order(self,
                           info: dict):
        e_type = self.entity('sales orders')

        return self.update_document(e_type,
                                    info,
                                    'DocEntry')

    def close_sales_order(self,
                          doc_entry: int = None):
        e_type = self.entity('sales orders')

        return self.close_document(e_type,
                                   doc_entry)

    def cancel_sales_order(self,
                           doc_entry: int = None):
        e_type = self.entity('sales orders')

        return self.cancel_document(e_type,
                                    doc_entry)

    def create_delivery(self,
                        doc_info: dict):
        e_type = self.entity('deliveries')

        return self.create_document(e_type,
                                    doc_info)

    def read_deliveries(self,
                        skip=None):
        e_type = self.entity('deliveries')

        return self.read_documents(e_type,
                                   skip)

    def read_delivery_by_docentry(self,
                                  doc_entry: int):
        e_type = self.entity('deliveries')

        return self.read_documents(e_type,
                                   docentry=doc_entry)

    def read_delivery_by_docnum(self,
                                doc_num: int = None):
        e_type = self.entity('deliveries')

        filter = f'DocNum eq {doc_num}'

        return self.read_documents(e_type,
                                   filter=filter)

    def read_deliveries_with_filter(self,
                                    filter: str = None):
        e_type = self.entity('deliveries')

        return self.read_documents(e_type,
                                   filter=filter)

    def update_delivery(self,
                        info: dict):
        e_type = self.entity('deliveries')

        return self.update_document(e_type,
                                    info,
                                    'DocEntry')

    def close_delivery(self,
                       doc_entry: int = None):
        e_type = self.entity('deliveries')

        return self.close_document(e_type,
                                   docentry=doc_entry)

    def cancel_delivery(self,
                        doc_entry: int = None):
        e_type = self.entity('deliveries')

        return self.cancel_document(e_type,
                                    docentry=doc_entry)

    def create_return(self,
                      doc_info: dict):
        e_type = self.entity('delivery returns')

        return self.create_document(e_type,
                                    doc_info)

    def read_returns(self,
                     skip=None):
        e_type = self.entity('delivery returns')

        return self.read_documents(e_type,
                                   skip)

    def read_return_by_docentry(self,
                                doc_entry: int):
        e_type = self.entity('delivery returns')

        return self.read_documents(e_type,
                                   docentry=doc_entry)

    def read_return_by_docnum(self,
                              doc_num: int = None):
        e_type = self.entity('delivery returns')

        filter = f'DocNum eq {doc_num}'

        return self.read_documents(e_type,
                                   filter=filter)

    def read_returns_with_filter(self,
                                 filter: str = None):
        e_type = self.entity('delivery returns')

        return self.read_documents(e_type,
                                   filter=filter)

    def update_return(self,
                      info: dict):
        e_type = self.entity('delivery returns')

        return self.update_document(e_type,
                                    info,
                                    'DocEntry')

    def close_return(self,
                     doc_entry: int = None):
        e_type = self.entity('delivery returns')

        return self.close_document(e_type,
                                   docentry=doc_entry)

    def cancel_return(self,
                      doc_entry: int = None):
        e_type = self.entity('delivery returns')

        return self.cancel_document(e_type,
                                    docentry=doc_entry)

    def create_invoice(self,
                       doc_info: dict):
        e_type = self.entity('invoices')

        return self.create_document(e_type,
                                    doc_info)

    def read_invoices(self,
                      skip=None):
        e_type = self.entity('invoices')

        return self.read_documents(e_type,
                                   skip)

    def read_invoice_by_docentry(self,
                                 doc_entry: int):
        e_type = self.entity('invoices')

        return self.read_documents(e_type,
                                   docentry=doc_entry)

    def read_invoice_by_docnum(self,
                               doc_num: int = None):
        e_type = self.entity('invoices')

        filter = f'DocNum eq {doc_num}'

        return self.read_documents(e_type,
                                   filter=filter)

    def read_invoices_with_filter(self,
                                  filter: str = None):
        e_type = self.entity('invoices')

        return self.read_documents(e_type,
                                   filter=filter)

    def update_invoice(self,
                       info: dict):
        e_type = self.entity('invoices')

        return self.update_document(e_type,
                                    info,
                                    'DocEntry')

    def cancel_invoice(self,
                       doc_entry: int = None):
        e_type = self.entity('invoices')

        return self.cancel_document(e_type,
                                    docentry=doc_entry)

    def create_credit_note(self,
                           doc_info: dict,
                           force_log=False):
        e_type = self.entity('credit notes')

        return self.create_document(e_type,
                                    doc_info,
                                    force_log)

    def read_credit_notes(self,
                          skip=None):
        e_type = self.entity('credit notes')

        return self.read_documents(e_type,
                                   skip=skip)

    def read_credit_note_by_docentry(self,
                                     doc_entry: int):
        e_type = self.entity('credit notes')

        return self.read_documents(e_type,
                                   docentry=doc_entry)

    def read_credit_note_by_docnum(self,
                                   docnum: int = None):
        e_type = self.entity('credit notes')

        filter = f'DocNum eq {docnum}'

        return self.read_documents(e_type,
                                   filter=filter)

    def read_credit_notes_with_filter(self,
                                      filter: str = None):
        e_type = self.entity('credit notes')

        return self.read_documents(e_type,
                                   filter=filter)

    def update_credit_note(self,
                           info: dict):
        e_type = self.entity('credit notes')

        return self.update_document(e_type,
                                    info,
                                    'DocEntry')

    def cancel_credit_note(self,
                           doc_entry: int = None):
        e_type = self.entity('credit notes')

        return self.cancel_document(e_type,
                                    docentry=doc_entry)
