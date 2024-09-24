#! /usr/bin/python3
from sbo_service import service
from sbo_service_inventory import inventory

import os
from dotenv import load_dotenv

load_dotenv()

test_user = os.getenv('test_user')
test_pass = os.getenv('test_pass')
test_comp = 'testHK'  # os.getenv('test_comp')
test_serv = os.getenv('test_serv')

item_code = 'z_testitem'
warehouse = '800'

failure = {
    'success': False,
    'error_message': 'Test not yet configured'
}


def test_create_bin(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    inv = inventory.Inventory(user, password, company, server)

    bin_type = inv.entity('bins')

    sub_code = item_code[:5]
    bin_code = f'{warehouse}-{sub_code}'

    i_response = inv.read_item(item_code)

    item = i_response['data'][0]
    item_name = item['ItemName'][:20]

    inv.delete_entity(bin_type, bin_code)

    sub_level = {
        "Code": sub_code,
        "Description": item_name,
        "WarehouseSublevel": 1
    }

    inv.create_bin_sublevel(sub_level)

    new_bin = {
        'BinCode': bin_code,
        'Description': item_name,
        'Inactive': 'tNO',
        'Warehouse': warehouse,
        'Sublevel1': sub_code
    }

    action = inv.create_bin(new_bin)

    inv.logout()

    assert action['success'], action['error_message']


def test_read_bins(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    inv = inventory.Inventory(user, password, company, server)

    action = inv.read_bins()

    inv.logout()

    assert action['success'], action['error_message']


def test_read_bin_by_code(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    inv = inventory.Inventory(user, password, company, server)

    bin = inv.read_bins()
    bin = bin['data'][0]

    bin_code = bin['BinCode']

    action = inv.read_bin_by_code(bin_code)

    inv.logout()

    assert action['success'], action['error_message']


def test_update_bin(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    inv = inventory.Inventory(user, password, company, server)

    sub_code = item_code[:5]
    bin_code = f'{warehouse}-{sub_code}'

    bin = inv.read_bin_by_code(bin_code)
    bin = bin['data'][0]
    abs_entry = bin['AbsEntry']

    update = {
        'BinCode': bin_code,
        'AbsEntry': abs_entry,
        'Description': 'Updated bin desc'
    }

    action = inv.update_bin(update)

    inv.logout()

    assert action['success'], action['error_message']


def test_delete_bin(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    inv = inventory.Inventory(user, password, company, server)

    sub_code = item_code[:5]
    bin_code = f'{warehouse}-{sub_code}'

    new_bin = {
        'BinCode': bin_code,
        'Inactive': 'tNO',
        'Warehouse': warehouse,
        'Sublevel1': sub_code
    }

    inv.create_bin(new_bin)

    action = inv.delete_bin(bin_code)

    inv.logout()

    assert action['success'], action['error_message']
