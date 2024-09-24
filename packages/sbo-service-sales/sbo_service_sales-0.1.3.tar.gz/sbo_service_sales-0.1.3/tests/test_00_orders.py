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

failure = {
    'success': False,
    'error_message': 'Test not yet configured'
}


def test_access_entity(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    sales = Sales(user, password, company, server)
    
    print(sales)
    
    if not sales.entity('sales orders'):
        assert False, 'Function not available'


def test_create_sales_order(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    sales = Sales(user, password, company, server)
    
    print(sales)

    action = sales.create_sales_order(sales_order)
    
    print(f'Action: {action}')

    sales.logout()

    assert action['success'], action['error_message']


def test_read_sales_orders(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    sales = Sales(user, password, company, server)

    action = sales.read_sales_orders()

    sales.logout()

    assert action['success'], action['error_message']


def test_read_sales_order_by_docentry(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    sales = Sales(user, password, company, server)

    action = sales.create_sales_order(sales_order)

    data = action['data'][0]
    doc_entry = data['DocEntry']

    action = sales.read_sales_order_by_docentry(doc_entry)

    sales.logout()

    assert action['success'], action['error_message']


def test_read_sales_order_by_docnum(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    sales = Sales(user, password, company, server)

    action = sales.create_sales_order(sales_order)

    data = action['data'][0]
    doc_num = data['DocNum']

    action = sales.read_sales_order_by_docnum(doc_num)

    sales.logout()

    assert action['success'], action['error_message']


def test_read_sales_order_with_filter(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    sales = Sales(user, password, company, server)

    filter = '(CardCode eq \'C999999999\')'

    action = sales.read_sales_order_with_filter(filter)

    sales.logout()

    assert action['success'], action['error_message']


def test_update_sales_order(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    sales = Sales(user, password, company, server)

    action = sales.create_sales_order(sales_order)

    data = action['data'][0]
    doc_entry = data['DocEntry']

    updated_data = {
        'DocEntry': doc_entry,
        'Comments': 'Added a comment'
    }

    action = sales.update_sales_order(updated_data)

    sales.logout()

    assert action['success'], action['error_message']


def test_close_sales_order(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    sales = Sales(user, password, company, server)

    action = sales.create_sales_order(sales_order)

    data = action['data'][0]
    doc_entry = data['DocEntry']

    action = sales.close_sales_order(doc_entry)

    sales.logout()

    assert action['success'], action['error_message']


def test_cancel_sales_order(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    sales = Sales(user, password, company, server)

    action = sales.create_sales_order(sales_order)

    data = action['data'][0]
    doc_entry = data['DocEntry']

    action = sales.cancel_sales_order(doc_entry)

    sales.logout()

    assert action['success'], action['error_message']
