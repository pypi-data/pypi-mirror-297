#! /usr/bin/python3
from sbo_service.service import Service
from sbo_service_inventory.inventory import Inventory
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

base_credit = {
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

failure = {
    'success': False,
    'error_message': 'Test not yet configured'
}


def test_create_credit_note(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    sales = Sales(user, password, company, server)

    action = sales.create_credit_note(base_credit)

    sales.logout()

    assert action['success'], action['error_message']


def test_read_credit_notes(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    sales = Sales(user, password, company, server)

    action = sales.read_credit_notes()

    sales.logout()

    assert action['success'], action['error_message']


def test_read_credit_note_by_docentry(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    sales = Sales(user, password, company, server)

    temp = sales.create_credit_note(base_credit)

    if temp['success'] == False:
        assert temp['success'],temp['error_message']

    action = failure

    sales.logout()

    assert action['success'], action['error_message']


def test_read_credit_note_by_docnum(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    sales = Sales(user, password, company, server)

    action = failure

    sales.logout()

    assert action['success'], action['error_message']


def test_read_credit_notes_with_filter(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    sales = Sales(user, password, company, server)

    action = failure

    sales.logout()

    assert action['success'], action['error_message']


def test_read_credit_notes_by_po_and_shipto(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    sales = Sales(user, password, company, server)

    action = failure

    sales.logout()

    assert action['success'], action['error_message']


def test_credit_note_exists_by_cust_po(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    sales = Sales(user, password, company, server)

    action = failure

    sales.logout()

    assert action['success'], action['error_message']


def test_update_credit_note(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    sales = Sales(user, password, company, server)

    action = failure

    sales.logout()

    assert action['success'], action['error_message']


def test_close_credit_note(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    sales = Sales(user, password, company, server)

    action = failure

    sales.logout()

    assert action['success'], action['error_message']


def test_cancel_credit_note(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    sales = Sales(user, password, company, server)

    action = failure

    sales.logout()

    assert action['success'], action['error_message']


def test_reopen_credit_note(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    sales = Sales(user, password, company, server)

    action = failure

    sales.logout()

    assert action['success'], action['error_message']


def test_create_cancelation_credit_note(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    sales = Sales(user, password, company, server)

    action = failure

    sales.logout()

    assert action['success'], action['error_message']
