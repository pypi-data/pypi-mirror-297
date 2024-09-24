#! /usr/bin/python3
from sbo_service_inventory.inventory import Inventory

import os
from dotenv import load_dotenv

load_dotenv()

test_user = os.getenv('test_user')
test_pass = os.getenv('test_pass')
test_comp = 'testHK'  # os.getenv('test_comp')
test_serv = os.getenv('test_serv')

entity_id = 'z_testitem'
entity_key = 'ItemCode'
entity_isbn13 = '9781234567890'

duplicate_message = f"Item code '{entity_id}' already exists"

entity = {
    'ItemCode': entity_id,
    'ItemName': 'This is a test item',
    'U_ISBN13short': entity_isbn13
}

failure = {
    'success': False,
    'error_message': 'Test not yet configured'
}


def test_create_item(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    inv = Inventory(user, password, company, server)
    
    inv.delete_item(entity_id)

    create = inv.create_item(entity)

    inv.logout()

    assert create['success'], create['error_message']


def test_get_first_20_items(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    inv = Inventory(user, password, company, server)

    items = inv.read_items()

    if not items['success']:
        assert False, 'Read failed'

    if len(items['data']) != 20:
        assert False, 'Returned item count is not the expected 20'

    inv.logout()

    assert True


def test_get_next_20_items(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    inv = Inventory(user, password, company, server)
    
    items = inv.read_items()
    items = inv.read_items(next=items['next'])

    if not items['success']:
        assert False, 'Read failed'

    if len(items['data']) != 20:
        assert False, 'Returned item count is not the expected 20'

    inv.logout()

    assert True


def test_get_specific_item(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    inv = Inventory(user, password, company, server)

    inv.delete_item(entity_id)

    inv.create_item(entity)

    items = inv.read_item(entity_id)

    inv.logout()

    if not items['success']:
        assert False, f'Unable to read item: {items["error_message"]}'

    assert True


def test_read_item_by_isbn13(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    inv = Inventory(user, password, company, server)

    inv.delete_item(entity_id)

    inv.create_item(entity)

    items = inv.read_item_by_isbn13(entity_isbn13)

    inv.logout()

    if not items['success']:
        assert False, f'Unable to read item: {items["error_message"]}'

    assert True


def test_delete_item(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    inv = Inventory(user, password, company, server)

    inv.create_item(entity)

    delete = inv.delete_item(entity_id)

    inv.logout()

    assert delete['success'], delete['error_message']


def test_item_exists_missing(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    inv = Inventory(user, password, company, server)

    inv.delete_item(entity_id)

    exists = inv.item_exists(entity_id)

    inv.logout()

    assert exists is False, 'Item should be missing...'


def test_item_exists_present(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    inv = Inventory(user, password, company, server)

    inv.create_item(entity)

    exists = inv.item_exists(entity_id)

    inv.logout()

    assert exists, 'Item should be present...'


def test_update_item(
        user=test_user,
        password=test_pass,
        company=test_comp,
        server=test_serv):
    inv = Inventory(user, password, company, server)

    inv.create_item(entity)

    updated = {
        'ItemCode': entity_id,
        'ItemName': 'I changed the name'
    }

    update = inv.update_item(updated)

    if not update['success']:
        assert False, f"{update['error']}: {update['error_message']}"

    item = inv.read_item(entity_id)

    if not item['success']:
        assert False, 'Failed to read the item'

    data = item['data'][0]

    if data['ItemName'] != 'I changed the name':
        assert False, 'Update failed'

    inv.logout()

    assert True
