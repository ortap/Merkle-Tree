![Alt text](Hash_Tree.svg.png?raw=true "Title")
# Merkle Tree
A simple implementation of merkle tree data structure.

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

## Running the tests

Download ps5_test.py to test run

## Authors

* **Min Joon So** - *Initial work* - [mjso7660](https://github.com/mjso7660)
