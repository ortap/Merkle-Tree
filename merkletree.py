# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 17:12:26 2018
@author: somj9
"""
import hashlib,json

class Hash_node(object):
    def __init__(self, hash_val = None, parent_node = None):
        self.parent_node = parent_node
        self.hash_val = hash_val

class RajaTree(object):
    def __init__(self):
        self.root = None
        self.dict = {}
        self.list_represent = []
        self.transactions = ['a','b','c']
#        self.transactions = ['a','b','c','d','e','f','g','h','i']
    
    def _hash_transactions(self):
        ''' get hash of transactions and create nodes'''
        node_list = []
        for transaction in self.transactions:
            new_node = Hash_node(calculate_hash(transaction))
            node_list.append(new_node)
            self.list_represent.append(new_node)
        return node_list
    
    def _process_level(self, node_list):
        ''' nodes: [] of hash_nodes'''
        temp_list=[]
        new_node_list = []
        
        for index in range(0, len(node_list), 2):
            #check if the node is the last node, then concat the nodes' hashes
            if index + 1 <= len(node_list) - 1:
                hash_concat = node_list[index].hash_val + node_list[index+1].hash_val
            else:
                hash_concat = node_list[index].hash_val
                
            new_hash = calculate_hash(hash_concat)
            new_node = Hash_node(new_hash)
            
            new_node_list.append(new_node)
            temp_list.append(new_node)
            
            #add to the tree's dictionary for hash pointing
            self.dict[new_hash] = new_node
            
            #create hash pointer
            node_list[index].parent_node = self.dict[new_hash]
            if index + 1 <= len(node_list) - 1:
                node_list[index+1].parent_node = self.dict[new_hash]
        self.list_represent = temp_list + self.list_represent
        return new_node_list
    
    def create_tree(self):
        initial_nodes = self._hash_transactions()
        while len(initial_nodes) != 1:
            initial_nodes = self._process_level(initial_nodes)
        self.root = initial_nodes[0]
        self.list_represent.insert(0,None)
        return self.list_represent
    
    def verify_member(self, index, data, server):
        hash_value = calculate_hash(data)
        concat_list = []
        temp = index
        while temp > 1:
            # to verify node is right child
            if temp%2 == 1:
                concat_list.append((server.list_represent[temp-1].hash_val, 1))
            # is left child
            elif temp + 2 <= len(server.list_represent):
                concat_list.append((server.list_represent[temp+1].hash_val, 0))      
            else:
                concat_list.append(('',0))
            temp = temp//2
        temp = index
        for each in concat_list:
            if each[1] == 0:
                hash_value = calculate_hash(hash_value+each[0])
            else:
                hash_value = calculate_hash(each[0]+hash_value)
            temp = temp//2
            if hash_value != self.list_represent[temp].hash_val:
                return False
        return True

def calculate_hash(data):
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

if __name__ == '__main__':
    a = RajaTree()
    c = a.create_tree()
    b = a
#    print(a.root.hash_val)
#    print(c[1].hash_val)
#    for x in range(1,len(c)):
#        print("value at", x)
#        print(c[x].hash_val)
#    print(a.verify_member(7,'d',b))
#    print(calculate_hash(calculate_hash(calculate_hash('a')+calculate_hash('b'))+calculate_hash(calculate_hash('b'))))
    
