![Alt text](Hash_Tree.svg.png?raw=true "Title")
# Merkle Tree
A simple implementation of merkle tree data structure.

## Explanation
We have two classes: Hash_node and Rajatree. Rajatree is a implementation of a merkle tree and Hash_node is each node resulted from hashing child nodes. Each Hash_node has four attributes: (1) parent_hash, (2) data, (3) left_child and (4) right_child. 

### 1.	How a node’s parent node is accessed from a child node
A child node’s pointer to its parent node should be a hash pointer, meaning if anything changes in the parent node, its child nodes should not point to the parent node anymore. We achieve this by not having child nodes directly point to their parent node but to have them store the hash of the actual parent node and search (_search) for a node that has the parent_hash value.

### 2.	How parent nodes are created
RajaTree’s _hash_transaction method and _process_level method hashes transactions and then creates parents method for every two hashed transactions.

### 3.	Verification
_verify_list sends string data to peer/server and retrieve a list of hashes to hash with for verification of validity. Then verify_membership function and verify_nonmember uses _verify_list function to check membership of a node. Verify_nonmember basically implements verify_membership methods a couple of times to check nonmembership.

### 4.	Traverse
Searches for the specific transactions from the transaction list and follows its parent_node until it reaches the root.

## Tests
Creating a tree
```
    transactions = ['a','b','c','d','e','f','g']
    merkle_tree = RajaTree(transactions)
    merkle_tree.create_tree()
```

Testing traversal
```
    merkle_tree.traverse('a')
    print('-----')
    merkle_tree.traverse('b')
    print('-----')
    merkle_tree.transactions = ['a','b','c','d','e','f','0']
    merkle_tree.traverse('h')
```
Testing hash pointer
```
    transactions = ['a','b','c','d','e','f','g']
    merkle_tree.list_represent[-2].data = 'k'
    merkle_tree.traverse('g')
    print('-----')
    transactions = ['a','b','c','d','e','f','g']
    parent_of_g = merkle_tree.list_represent[-8]
    merkle_tree.list_represent[-8].data = 'something'
    merkle_tree.traverse('g')
```

Testing Membership and nonmembership of a string
```
    peer = merkle_tree
    merkle_tree.verify_membership('a' , peer)
    merkle_tree.verify_membership('0' , peer)
    merkle_tree.verify_nonmember('b', peer)
    merkle_tree.verify_nonmember('0', peer)
```
### Prerequisites

None

## Authors

* **Min Joon So** - *Initial work* - [mjso7660](https://github.com/mjso7660)
