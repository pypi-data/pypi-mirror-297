#! /usr/bin/python3
from sbo_service import service
from sbo_service_inventory import inventory

import os
from dotenv import load_dotenv

load_dotenv()

test_user = os.getenv('test_user')
test_pass = os.getenv('test_pass')
test_comp = os.getenv('test_comp')
test_serv = os.getenv('test_serv')

failure = {
    'success': False,
    'error_message': 'Test not yet configured'
}


def test_read_item_groups(
        user=test_user,
        password=test_pass,
        company='PhoenixHK',
        server=test_serv):
    inv = inventory.Inventory(user, password, company, server)

    read = inv.read_item_groups()

    inv.logout()

    assert read['success'], read['error_message']


def test_read_item_group_by_code(
        user=test_user,
        password=test_pass,
        company='PhoenixHK',
        server=test_serv):
    inv = inventory.Inventory(user, password, company, server)

    e_type = inv.entity('item groups')

    fltr = '(U_Group_Code ne Null)'

    groups = inv.read_entity(e_type, filter=fltr)

    read = failure

    if groups['success']:
        code = groups['data'][0]['U_Group_Code']

        read = inv.read_item_group_by_code(code)

    inv.logout()

    assert read['success'], read['error_message']
