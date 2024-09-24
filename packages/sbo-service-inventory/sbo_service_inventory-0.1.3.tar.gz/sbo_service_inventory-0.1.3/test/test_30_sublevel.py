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

item_code = 'z_testitem'
item_description = 'This is a test item'

warehouse = '800'

sub_code = item_code[:5]
bin_code = f'{warehouse}-{sub_code}'

sub_level = {
    "Code": sub_code,
    "Description": item_description,
    "WarehouseSublevel": 1
}

new_sublevel = None

failure = {
    'success': False,
    'error_message': 'Test not yet configured'
}


def test_read_sublevels(user=test_user,
                        password=test_pass,
                        company=test_comp,
                        server=test_serv):
    inv = inventory.Inventory(user, password, company, server)

    read = inv.read_bin_sublevels()
    sublevels = None

    while read['next']:
        sublevels = read
        read = inv.read_bin_sublevels(read['next'])

    for rec in sublevels['data']:
        print(rec)

    assert sublevels['success'], f'{sublevels["error"]} {sublevels["error_message"]}'


def test_create_sublevel(user=test_user,
                         password=test_pass,
                         company=test_comp,
                         server=test_serv):
    global new_sublevel

    inv = inventory.Inventory(user, password, company, server)

    read = inv.read_bin_sublevels()
    sublevels = None
    last = None

    while read['next']:
        sublevels = read
        read = inv.read_bin_sublevels(read['next'])

    for rec in sublevels['data']:
        last = rec['AbsEntry']

    sub_level['Code'] = str(int(last) + 1)

    create = inv.create_bin_sublevel(sub_level)

    inv.logout()

    if not new_sublevel:
        new_sublevel = sub_level['Code']

        return

    assert create['success'], create['error_message']


def test_read_sublevel_by_code(user=test_user,
                               password=test_pass,
                               company=test_comp,
                               server=test_serv):
    global new_sublevel

    if not new_sublevel:
        test_create_sublevel(user, password, company, server)

    inv = inventory.Inventory(user, password, company, server)

    read = inv.read_bin_sublevel_by_code(new_sublevel)

    inv.logout()

    assert read['success'], read['error_message']


def test_update_sublevel(user=test_user, password=test_pass, company=test_comp, server=test_serv):
    global new_sublevel

    if not new_sublevel:
        test_create_sublevel(user, password, company, server)

    inv = inventory.Inventory(user, password, company, server)

    read = inv.read_bin_sublevel_by_code(new_sublevel)

    updated = read['data'][0]

    updated['Description'] = 'Change the description'

    update = inv.update_bin_sublevel(info=updated)

    inv.logout()

    assert update['success'], update['error_message']


def test_delete_sublevel(user=test_user, password=test_pass, company=test_comp, server=test_serv):
    global new_sublevel

    if not new_sublevel:
        test_create_sublevel(user, password, company, server)

    inv = inventory.Inventory(user, password, company, server)

    read = inv.read_bin_sublevel_by_code(new_sublevel)

    data = read['data'][0]
    absEntry = data['AbsEntry']

    delete = inv.delete_bin_sublevel(absEntry)

    inv.logout()

    assert delete['success'], delete['error_message']
