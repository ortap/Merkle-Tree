# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 17:12:26 2018
@author: somj9
"""
import hashlib

class Hash_node(object):
    def __init__(self, data):
        '''
        data (string): data the node stores
        '''
        self.parent_hash = ''
        self.data = data
        self.left_child = None
        self.right_child = None
        
    @property
    def hash_val(self):
        return calculate_hash(self.data)
    
    def get_parent_node(self, node_list):
        '''
        node_list ([] of Hash_node): a list that keeps all the nodes
        return: parent node if current node
        '''
        return self._search(self.parent_hash, node_list)
    
    def _search(self, hash_val, list):
        '''
        searches for specific hash_val in a list and returns the node with the hash value
        
        hash_val (string): hash_val to search for
        node_list ([] of Hash_node): list containing all the nodes
        
        return: the node who's hash value is 'hash_val'
        '''
        hash_list = [list[x].hash_val for x in range(len(list))]
        try:
            index = hash_list.index(hash_val)
            return list[index]
        except ValueError:
            print("Caution! Parent hash doesn't exist. Data migth have been tampered")
            return False    

class RajaTree(object):
    def __init__(self, transactions = []):
        self.root = None
        self.list_represent = []    # this list keeps all nodes of the tree
        self.transactions = transactions
    
    def _hash_transactions(self):
        ''' 
        get transactions and create leaves that stores transaction itself and its hash
        
        return: list of leaf nodes
        '''
        leaves = []
        for transaction in self.transactions:
            new_node = Hash_node(transaction)
            leaves.append(new_node)
            self.list_represent.append(new_node)
        return leaves
    
    def _process_level(self, node_list):
        '''
        creates (n-1)th level of nodes based on nth nodes. This function will be used recursively
        to create nodes until there is only 
        
        node_list ([] of Hash_nodes): list of the nodes created for current tree level
        
        return: list of nodes created for the parent level above
        '''
        new_node_list = []
        
        # iterates every TWO nodes from the given node_list 
        for index in range(0, len(node_list), 2):
            #check if the node is NOT the last node, then concat the nodes' hashes
            if index + 1 <= len(node_list) - 1:
                hash_concat = node_list[index].hash_val + node_list[index+1].hash_val
            #if the node IS the last node of the tree level, concat nothing
            else:
                hash_concat = node_list[index].hash_val
            
            #create parent node
            new_node = Hash_node(hash_concat)
            new_node_list.append(new_node)
            
            #create hash pointer
            node_list[index].parent_hash = new_node.hash_val
            new_node.left_child = node_list[index]
            
            #check if NOT the last node
            if index + 1 <= len(node_list) - 1:
                node_list[index+1].parent_hash = calculate_hash(hash_concat)
                new_node.right_child = node_list[index+1]
        self.list_represent = new_node_list + self.list_represent
        return new_node_list
    
    def create_tree(self):
        '''
        creates tree from the tree's transactions
        
        returns: list of all the nodes
        '''
        initial_nodes = self._hash_transactions()
        
        #loop until there is only one node(the root) in the list
        while len(initial_nodes) != 1:
            initial_nodes = self._process_level(initial_nodes)
        self.root = initial_nodes[0]
        print("A merkle tree is created")
        return self.list_represent
    
    def _verify_list(self, data, server):
        '''
        sends string data(transaction) to a peer/server and retrieve a list of hashes to hash with 
        for verification of validity
        
        data (string): transaction to verify if it is valid
        server (class Rajatree): peer/server to request for membership
        
        return: list of hash values to hash with the string
        '''
        data_list = [node.data for node in server.list_represent]
        verify_list = []
        
        #finds the node with the data in the node list
        try:
            index = data_list.index(data)
        except:
            print("ERROR!",data,"not in the transaction list")
            return False
        node = server.list_represent[index]
        
        #stores hash values needed for verification until it reaches the root node
        while node is not self.root:
            parent_node = node.get_parent_node(server.list_represent)
            #if current node is a left-child. Adds a tuple (hash_value, 1 for left child/0 for right child )
            if node == parent_node.left_child:
                try:
                    verify_list.append((parent_node.right_child.hash_val,1))
                #if the node is the right most node
                except:
                    verify_list.append(('',1))
            elif node == parent_node.right_child:
                verify_list.append((parent_node.left_child.hash_val,0))
            node = parent_node
        return verify_list
    
    def verify_membership(self, data, server):
        '''
        verifies membership of given data from the server/peer
        
        data (string): data to verify
        server (Rajatree): peer/server to request verification hash values
        
        return: True if membership is verified and False if cannot be verified
        '''
        # if the data is in the leaves
        if self._verify_list(data,server):
            verify_list = self._verify_list(data, server)
        else:
            print("Cannot verify membership of", data)
            return False
        hash_val = calculate_hash(data)
        
        #iterate through the verification hash list and calculate hash 
        for tuple in verify_list:
            if tuple[1] == 1:
                hash_val = calculate_hash(hash_val + tuple[0])
            elif tuple[1] == 0:
                hash_val = calculate_hash(tuple[0] + hash_val)
        if check_same(self.root.hash_val, hash_val):
            print("Membership of", data, "verified!")
            return True
        else:
            print("Cannot verify membership of", data)
            return False
    
    def verify_nonmember(self, data, server):
        '''
        verifies nonmembership by checking a node with data smaller than the given data and one greater
        
        data (string): data to verify
        server (Rajatree): peer/server to request verification hash values
        
        return: True if non-membership is verified and False if cannot be verified
        '''
        prev = False
        for each in self.transactions:
            if each > data:
                smaller = each
                break
            else:
                smaller = False
            prev = each
        
        if not smaller or not prev:
            print("Non-membership of", data, "verified!")
            return True
        if smaller == data or prev == data:
            print("Cannot verify non-membership of", data)
            return False
        if self.verify_membership(smaller,server) and self.verify_membership(prev,server):
            print("Non-membership of", data, "verified!")
            return True
        else:
            print("Cannot verify no-membership of", data)
            return False
    
    def traverse(self, data):
        '''
        traverses from data string to path
        
        data (string)
        
        returns: hash values on the path to the root
        '''
        data_list = [node.data for node in self.list_represent]
#        data_list = self.transactions
        path = []
        
        #finds the node with the data in the node list
        try:
            index = data_list.index(data)
        except:
            print("ERROR!",data,"not in the transaction list")
            return False
        node = self.list_represent[index]
        
        path.append(node.hash_val)
        while node is not self.root:
            try:
                parent_node = node.get_parent_node(self.list_represent)
                path.append(parent_node.hash_val)
            except:
                return
            node = parent_node
        
        #print path
        print("Path from",data,"to the root is:")
        for x in range(len(path)):
            if x == len(path)-1:
                print("* Root node:")
                print(path[x])
            else:
                print("*",x,"th node:")
                print(path[x])
        return path

        
def calculate_hash(data):
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def check_same(hash1, hash2):
    return hash1 == hash2

if __name__ == '__main__':
    transactions = ['a','b','c','d','e','f','g']
    merkle_tree = RajaTree(transactions)
    merkle_tree.create_tree()
    print('-----')
    merkle_tree.traverse('a')
    print('-----')
    merkle_tree.traverse('b')
    print('-----')
    merkle_tree.transactions = ['a','b','c','d','e','f','0']
    merkle_tree.traverse('h')
    print('-----')
    transactions = ['a','b','c','d','e','f','g']
    merkle_tree.list_represent[-2].data = 'k'
    merkle_tree.traverse('g')
    print('-----')
    transactions = ['a','b','c','d','e','f','g']
    parent_of_g = merkle_tree.list_represent[-8]
    merkle_tree.list_represent[-8].data = 'something'
    merkle_tree.traverse('g')
    print('-----')
    peer = merkle_tree
    merkle_tree.verify_membership('a' , peer)
    print('-----')
    merkle_tree.verify_membership('0' , peer)
    print('-----')
    merkle_tree.verify_nonmember('b', peer)
    print('-----')
    merkle_tree.verify_nonmember('0', peer)
