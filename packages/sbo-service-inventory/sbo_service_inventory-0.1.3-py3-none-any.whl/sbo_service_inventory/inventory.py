#! /usr/bin/python3
"""
Inventory related wrappers
"""
from sbo_service.service import Service


class Inventory(Service):
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
            
        
    def create_item(self,
                    item_info:dict):
        e_type = self.entity('items')

        return self.create_entity(e_type,
                                  item_info)


    def read_items(self,
                   next=None):
        e_type = self.entity('items')

        return self.read_entity(e_type,
                                next=next)


    def read_item(self,
                  item_code:str):
        e_type = self.entity('items')

        return self.read_entity(e_type,
                                code=item_code)


    def read_item_by_isbn13(self,
                            isbn13):
        e_type = self.entity('items')

        filter = f'U_ISBN13short eq \'{isbn13}\''

        return self.read_entity(e_type,
                                filter=filter)


    def item_exists(self,
                    item_code:str):
        e_type = self.entity('items')

        item = self.read_entity(e_type,
                                code=item_code)

        return item['success']


    def update_item(self,
                    item_info:dict):
        e_type = self.entity('items')

        return self.update_entity(e_type,
                                  item_info,
                                  'ItemCode')


    def delete_item(self,
                    item_code:str):
        e_type = self.entity('items')

        return self.delete_entity(e_type,
                                  code=item_code)


    def create_transfer(self,
                        info:dict):
        e_type = self.entity('transfers')

        return self.create_document(e_type,
                                    info)


    def read_transfer_by_docentry(self,
                                  docentry:int=None):
        e_type = self.entity('transfers')

        return self.read_documents(e_type,
                                   docentry=docentry)


    def read_transfer_by_docnum(self,
                                doc_num:int=None):
        e_type = self.entity('transfers')

        return self.read_documents(e_type,
                                   docnum=doc_num)


    def read_transfers_with_filter(self,
                                   filter:str=None):
        e_type = self.entity('transfers')

        return self.read_documents(e_type,
                                   filter=filter)


    def update_transfer(self,
                        transfer_data:dict):
        e_type = self.entity('transfers')

        return self.update_document(e_type,
                                    transfer_data,
                                    'DocEntry')


    def cancel_transfer(self,
                        doc_entry:int):
        e_type = self.entity('transfers')

        return self.cancel_document(e_type,
                                    doc_entry)


    def read_item_groups(self,
                         skip=None):
        e_type = self.entity('item groups')

        return self.read_entity(e_type,
                                skip)


    def read_item_group_by_code(self,
                                code=None):
        e_type = self.entity('item groups')

        filter = f"U_Group_Code eq '{code}'"

        return self.read_entity(e_type,
                                filter=filter)


    def create_bin_sublevel(self,
                            info:dict):
        e_type = self.entity('bin sublevels')

        return self.create_entity(e_type,
                                  info)


    def read_bin_sublevels(self,
                           skip=None):
        e_type = self.entity('bin sublevels')

        return self.read_entity(e_type,
                                skip)


    def read_bin_sublevel_by_code(self,
                                  code=None):
        e_type = self.entity('bin sublevels')

        filter = f"Code eq '{code}'"

        return self.read_entity(e_type,
                                filter=filter)


    def update_bin_sublevel(self,
                            info:dict):
        e_type = self.entity('bin sublevels')

        return self.update_entity(e_type,
                                  info,
                                  'AbsEntry')


    def delete_bin_sublevel(self,
                            absEntry:int):
        e_type = self.entity('bin sublevels')

        return self.delete_entity(e_type,
                                  absEntry)


    def create_bin(self,
                   info:dict):
        e_type = self.entity('bins')

        return self.create_entity(e_type,
                                  info)


    def read_bins(self,
                  skip=None):
        e_type = self.entity('bins')

        return self.read_entity(e_type,
                                next=skip)


    def read_bin_by_code(self,
                         code=None):
        e_type = self.entity('bins')

        filter = f"BinCode eq '{code}'"

        return self.read_entity(e_type,
                                filter=filter)


    def update_bin(self,
                   info:dict):
        e_type = self.entity('bins')

        info['AbsEntry'] = int(info['AbsEntry'])

        return self.update_entity(e_type,
                                  info,
                                  'AbsEntry')


    def delete_bin(self,
                   bin_code:str):
        e_type = self.entity('bins')

        bin = self.read_bin_by_code(bin_code)

        if bin['success']:
            bin = bin['data'][0]

            return self.delete_entity(e_type, bin['AbsEntry'])
        else:
            return bin
