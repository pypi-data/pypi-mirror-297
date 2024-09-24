#! /usr/bin/python3
from sbo_service.service import Service
from sbo_service_sales.sales import Sales

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

sales_order = {
    'DoctType': 'dDocument_Items',
    'DocDate': doc_date,
    'DocDueDate': doc_date,
    'CardCode': 'C999999999',
    'DocumentLines': [
        {
            'ItemCode': '7896300',
            'TaxCode': 'Ex',
            'Quantity': 10
        }
    ]
}

delivery_base = {
    'DocType': 'dDocument_Items',
    'DocDate': doc_date,
    'DocDueDate': doc_date
}

invoice_base = {
    'DocType': 'dDocumentItems',
    'DocDate': doc_date,
    'DocumentLines': []
}

failure = {
    'success': False,
    'error_message': 'Test not yet configured'
}


def create_delivery(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    sales = Sales(user, password, company, server)
    
    order = sales.create_sales_order(sales_order)
    order = order['data'][0]

    delivery = delivery_base
    delivery['CardCode'] = order['CardCode']
    delivery['ShipToCode'] = order['ShipToCode']

    lines = []

    for line in order['DocumentLines']:
        new_line = {
            'ItemCode': line['ItemCode'],
            'Quantity': line['RemainingOpenQuantity'],
            'BaseType': 17,
            'BaseEntry': order['DocEntry'],
            'BaseLine': line['LineNum']
        }

        lines.append(new_line)

    delivery['DocumentLines'] = lines

    action = sales.create_delivery(delivery)
    delivery = action['data'][0]

    return delivery


def create_invoice(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    sales = Sales(user, password, company, server)
    
    delivery = create_delivery(user, password, company, server)

    invoice = invoice_base
    invoice['CardCode'] = delivery['CardCode']

    lines = []

    for line in delivery['DocumentLines']:
        new_line = {
            'ItemCode': line['ItemCode'],
            'Price': line['Price'],
            'UnitPrice': line['Price'],
            'TaxCode': line['TaxCode'],
            'WarehouseCode': line['WarehouseCode'],
            'BaseType': 15,
            'BaseEntry': line['DocEntry'],
            'BaseLine': line['LineNum'],
            'Quantity': line['Quantity']
        }

        lines.append(new_line)

    invoice['DocumentLines'] = lines

    action = sales.create_invoice(invoice)
    
    sales.logout()

    return action['data'][0]


def test_create_invoice(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    sales = Sales(user, password, company, server)

    delivery = create_delivery(user, password, company, server)

    invoice = invoice_base
    invoice['CardCode'] = delivery['CardCode']

    lines = []

    for line in delivery['DocumentLines']:
        new_line = {
            'ItemCode': line['ItemCode'],
            'Price': line['Price'],
            'UnitPrice': line['Price'],
            'TaxCode': line['TaxCode'],
            'WarehouseCode': line['WarehouseCode'],
            'BaseType': 15,
            'BaseEntry': line['DocEntry'],
            'BaseLine': line['LineNum'],
            'Quantity': line['Quantity']
        }

        lines.append(new_line)

    invoice['DocumentLines'] = lines

    action = sales.create_invoice(invoice)

    sales.logout()

    assert action['success'], action['error_message']


def test_read_invoices(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    sales = Sales(user, password, company, server)

    action = sales.read_invoices()

    sales.logout()

    assert action['success'], action['error_message']


def test_read_invoice_by_docentry(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    sales = Sales(user, password, company, server)

    invoice = create_invoice(user, password, company, server)
    doc_entry = invoice['DocEntry']

    action = sales.read_invoice_by_docentry(doc_entry=doc_entry)

    sales.logout()

    assert action['success'], action['error_message']


def test_read_invoice_by_docnum(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    sales = Sales(user, password, company, server)

    invoice = create_invoice(user, password, company, server)
    doc_num = invoice['DocNum']

    action = sales.read_invoice_by_docnum(doc_num=doc_num)

    sales.logout()

    assert action['success'], action['error_message']


def test_read_invoices_with_filter(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    sales = Sales(user, password, company, server)

    invoice = create_invoice(user, password, company, server)
    comments = invoice['Comments']

    filter = f"Comments eq '{comments}'"

    action = sales.read_invoices_with_filter(filter=filter)

    sales.logout()

    assert action['success'], action['error_message']


def test_update_invoice(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    sales = Sales(user, password, company, server)

    invoice = create_invoice(user, password, company, server)

    update = {
        'DocEntry': invoice['DocEntry'],
        'NumAtCard': 'The number changed!!!!'
    }

    action = sales.update_invoice(update)

    sales.logout()

    assert action['success'], action['error_message']


def test_cancel_Invoice(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    sales = Sales(user, password, company, server)

    invoice = create_invoice(user, password, company, server)

    action = sales.cancel_invoice(doc_entry=invoice['DocEntry'])

    sales.logout()

    assert action['success'], action['error_message']
