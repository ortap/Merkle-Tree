# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 17:12:26 2018
@author: somj9
"""
import hashlib

class Hash_node(object):
    def __init__(self, data):
        self.parent_hash = ''
        self.data = data
        self.left_child = None
        self.right_child = None
        
    @property
    def hash_val(self):
        return calculate_hash(self.data)
    
    def get_parent_node(self, node_list):
        '''
        :param [node_list] >> RajaTree.lsit_represent
        return: parent node if exist
        '''
        return self._search(self.parent_hash, node_list)
    
    def _search(self, hash_val, list):
        hash_list = [list[x].hash_val for x in range(len(list))]
        try:
            index = hash_list.index(hash_val)
            return list[index]
        except ValueError:
            print("parent doesn't exist")
            return False    

class RajaTree(object):
    def __init__(self):
        self.root = None
        self.list_represent = []
        self.transactions = ['a','c','d','e','f','g']
    
    def _hash_transactions(self):
        ''' get hash of transactions and create nodes'''
        leaves = []
        for transaction in self.transactions:
            new_node = Hash_node(transaction)
            leaves.append(new_node)
            self.list_represent.append(new_node)
        return leaves
    
    def _process_level(self, node_list):
        ''' nodes: [] of hash_nodes'''
        new_node_list = []
        
        for index in range(0, len(node_list), 2):
            #check if the node is NOT the last node, then concat the nodes' hashes
            if index + 1 <= len(node_list) - 1:
                hash_concat = node_list[index].hash_val + node_list[index+1].hash_val
            else:
                hash_concat = node_list[index].hash_val
            new_node = Hash_node(hash_concat)
            
            new_node_list.append(new_node)
            
            #create hash pointer
            node_list[index].parent_hash = new_node.hash_val
#            print(hash_concat)
            new_node.left_child = node_list[index]
            
            #check if NOT the last node
            if index + 1 <= len(node_list) - 1:
                node_list[index+1].parent_hash = calculate_hash(hash_concat)
                new_node.right_child = node_list[index+1]
                
        self.list_represent = new_node_list + self.list_represent
        return new_node_list
    
    def create_tree(self):
        initial_nodes = self._hash_transactions()
        while len(initial_nodes) != 1:
            initial_nodes = self._process_level(initial_nodes)
        self.root = initial_nodes[0]
        return self.list_represent
    
    def _verify_list(self, data, server):
        data_list = [node.data for node in server.list_represent]
        verify_list = []
        try:
            index = data_list.index(data)
        except:
            print(data,"not in the list")
            return False
        node = server.list_represent[index]
        
        while node is not self.root:
            parent_node = node.get_parent_node(server.list_represent)
            #if current node is left-child
            if node == parent_node.left_child:
                try:
                    verify_list.append((parent_node.right_child.hash_val,1))
                except:
                    verify_list.append(('',1))
            elif node == parent_node.right_child:
                verify_list.append((parent_node.left_child.hash_val,0))
            node = parent_node
        return verify_list
    
    def verify_membership(self, data, server):
        if self._verify_list(data,server):
            verify_list = self._verify_list(data, server)
        else:
            return False
        hash_val = calculate_hash(data)
        for tuple in verify_list:
            if tuple[1] == 1:
                hash_val = calculate_hash(hash_val + tuple[0])
            elif tuple[1] == 0:
                hash_val = calculate_hash(tuple[0] + hash_val)
        return check_same(self.root.hash_val, hash_val)
    
    def verify_nonmember(self, data, server):
        for each in self.transactions:
            if each > data:
                smaller = each
                break
            else:
                smaller = False
            prev = each
        
        if smaller == False:
            print("here 1")
            return True
        if smaller == data or prev == data:
            return False
        return self.verify_membership(smaller,server) and self.verify_membership(prev,server)
        
def calculate_hash(data):
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def check_same(hash1, hash2):
    return hash1 == hash2

if __name__ == '__main__':
    a = RajaTree()
    c = a.create_tree()
    b = a
