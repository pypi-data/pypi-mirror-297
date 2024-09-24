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
            'Quantity': 10
        }
    ]
}

base = {
    'DocType': 'dDocument_Items',
    'DocDate': doc_date,
    'DocDueDate': doc_date
}

failure = {
    'success': False,
    'error_message': 'Test not yet configured'
}


def test_create_delivery(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    sales = Sales(user, password, company, server)

    order = sales.create_sales_order(sales_order)
    order = order['data'][0]

    delivery = base
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

    sales.logout()

    assert action['success'], action['error_message']


def test_read_deliveries(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    sales = Sales(user, password, company, server)

    action = sales.read_deliveries()

    sales.logout()

    assert action['success'], action['error_message']


def test_read_delivery_by_docentry(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    sales = Sales(user, password, company, server)

    order = sales.create_sales_order(sales_order)
    order = order['data'][0]

    delivery = base
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

    delivery = sales.create_delivery(delivery)
    delivery = delivery['data'][0]
    doc_entry = delivery['DocEntry']

    action = sales.read_delivery_by_docentry(doc_entry)

    sales.logout()

    assert action['success'], action['error_message']


def test_read_delivery_by_docnum(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    sales = Sales(user, password, company, server)

    order = sales.create_sales_order(sales_order)
    order = order['data'][0]

    delivery = base
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

    delivery = sales.create_delivery(delivery)
    delivery = delivery['data'][0]
    doc_num = delivery['DocNum']

    action = sales.read_delivery_by_docnum(doc_num)

    sales.logout()

    assert action['success'], action['error_message']


def test_read_deliveries_with_filter(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    sales = Sales(user, password, company, server)

    order = sales.create_sales_order(sales_order)
    order = order['data'][0]

    test_comment = f"{order['DocNum']}-Test"

    delivery = base
    delivery['CardCode'] = order['CardCode']
    delivery['ShipToCode'] = order['ShipToCode']
    delivery['Comments'] = test_comment

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

    delivery = sales.create_delivery(delivery)

    filter = f"Comments eq '{test_comment}'"

    action = sales.read_deliveries_with_filter(filter)

    sales.logout()

    assert action['success'], action['error_message']


def test_update_delivery(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    sales = Sales(user, password, company, server)

    order = sales.create_sales_order(sales_order)
    order = order['data'][0]

    test_comment = f"{order['DocNum']}-Test"

    delivery = base
    delivery['CardCode'] = order['CardCode']
    delivery['ShipToCode'] = order['ShipToCode']
    delivery['Comments'] = test_comment

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

    delivery = sales.create_delivery(delivery)
    delivery = delivery['data'][0]
    doc_entry = delivery['DocEntry']
    doc_num = delivery['DocNum']

    updated = {
        'DocEntry': doc_entry,
        'DocNum': doc_num,
        'NumAtCard': delivery['Comments']
    }

    action = sales.update_delivery(updated)

    sales.logout()

    assert action['success'], action['error_message']


def test_close_delivery(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    sales = Sales(user, password, company, server)

    order = sales.create_sales_order(sales_order)
    order = order['data'][0]

    test_comment = f"{order['DocNum']}-Test"

    delivery = base
    delivery['CardCode'] = order['CardCode']
    delivery['ShipToCode'] = order['ShipToCode']
    delivery['Comments'] = test_comment

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

    delivery = sales.create_delivery(delivery)
    delivery = delivery['data'][0]
    doc_entry = delivery['DocEntry']

    action = sales.close_delivery(doc_entry=doc_entry)

    sales.logout()

    assert action['success'], action['error_message']


def test_cancel_delivery(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    sales = Sales(user, password, company, server)

    order = sales.create_sales_order(sales_order)
    order = order['data'][0]

    test_comment = f"{order['DocNum']}-Test"

    delivery = base
    delivery['CardCode'] = order['CardCode']
    delivery['ShipToCode'] = order['ShipToCode']
    delivery['Comments'] = test_comment

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

    delivery = sales.create_delivery(delivery)
    delivery = delivery['data'][0]
    doc_entry = delivery['DocEntry']

    action = sales.cancel_delivery(doc_entry=doc_entry)

    sales.logout()

    assert action['success'], action['error_message']
