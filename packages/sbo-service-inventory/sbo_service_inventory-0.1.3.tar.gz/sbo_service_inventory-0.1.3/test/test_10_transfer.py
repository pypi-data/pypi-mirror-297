#! /usr/bin/python3
from sbo_service import service
from sbo_service_inventory import inventory

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
doc_comment = 'This is the test comment'
doc_memo = 'This is the test memo'
po_number = '123456789'

document = {
    'DocDate': doc_date,
    'DueDate': doc_date,
    'FromWarehouse': '930',
    'ToWarehouse': '430',
    'PriceList': -2,
    'Comments': f'Processing order: {po_number}',
    'JournalMemo': doc_memo,
    'StockTransferLines': [
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


def test_create_transfer(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    inv = inventory.Inventory(user, password, company, server)

    create = inv.create_transfer(document)

    inv.logout()

    assert create['success'], create['error_message']


def test_read_transfer_by_docentry(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    inv = inventory.Inventory(user, password, company, server)

    create = inv.create_transfer(document)

    doc = create['data'][0]
    doc_entry = doc['DocEntry']

    read = inv.read_transfer_by_docentry(docentry=doc_entry)

    inv.logout()

    assert read['success'], f'{read["error"]} {read["error_message"]}'


def test_read_transfer_with_filter(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    inv = inventory.Inventory(user, password, company, server)

    filter = '' + \
        f'(Comments eq \'{"Processing order: " + po_number}\') and ' + \
        f'(TaxDate eq \'{doc_date}\')'

    inv.create_transfer(document)

    read = inv.read_transfers_with_filter(filter=filter)

    inv.logout()

    assert read['success'], f'{read["error"]} {read["error_message"]}'


def test_update_transfer(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    inv = inventory.Inventory(user, password, company, server)

    create = inv.create_transfer(document)

    doc = create['data'][0]
    doc_entry = doc['DocEntry']

    updated_transfer = {
        'DocEntry': doc_entry,
        'JournalMemo': 'So did it change?'
    }

    update = inv.update_transfer(updated_transfer)

    inv.logout()

    assert update['success'], f'{update["error"]} {update["error_message"]}'


def test_cancel_transfer(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    inv = inventory.Inventory(user, password, company, server)

    create = inv.create_transfer(document)

    doc = create['data'][0]
    doc_entry = doc['DocEntry']

    update = inv.cancel_transfer(doc_entry)

    inv.logout()

    assert update['success'], f'{update["error"]} {update["error_message"]}'
