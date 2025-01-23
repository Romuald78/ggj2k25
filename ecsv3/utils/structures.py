from typing import Any

from ecsv3.utils.logs import ECSv3


# an entry is an object with a 'name' property
def add_entry_with_name(dict, entry):
    # check if name is correct
    if entry.name in dict:
        ECSv3.error(f"Impossible to add a new object called '{entry.name}' twice !")
    # Store entity (+link)
    dict[entry.name] = entry

def remove_entry_with_name(dict, entry:Any):
    # check if name is correct
    if entry.name not in dict:
        ECSv3.error(f"Impossible to remove '{entry}' : not found !")
    # Store entity (+link)
    del dict[entry.name]

# an entry is an object with a 'priority' property
# the list given in parameter is assumed to be already sorted
def add_entry_with_priority(lst: list, entry: Any):
    # TODO : optim : use BST or AVL to increase perfs
    # Search for index to insert new entry
    # search is based on the entry.priority values in ascending order
    n = len(lst)
    left = 0
    right = n-1
    watchdog = 0
    while left < right:
        watchdog += 1
        if watchdog >= 1000:
            ECSv3.error('ADD ENTRY : while loop WATCH DOG !')

        middle = (left + right) // 2
        if lst[middle].priority > entry.priority:
            # Look in the LEFT part
            right = middle - 1
        elif lst[middle].priority < entry.priority:
            # Look in the RIGHT part
            left = middle + 1
        else:
            # the middle priority is the same one than the entry
            # we can insert here
            left = middle
            right = middle

    # if list is empty or the value should be at the end
    if n == 0 or right >= n:
        lst.append(entry)
        return n
    # if the value should be added at the beginning
    elif left < 0:
        lst.insert(0, entry)
        return 0
    # insert value at correct index
    else:
        if lst[left].priority < entry.priority:
            left += 1
        lst.insert(left, entry)
        return left

def remove_entry_with_priority(lst: list, entry: Any):
    # TODO : optim : use BST or AVL to increase perfs
    try:
        lst.remove(entry)
    except:
        ECSv3.error(f"impossible to remove entry {entry} from list {lst}")




# class TreeNode:
#     def __init__(self, value, data):
#         self.value  = value
#         self.data   = data
#         self.left   = None
#         self.right  = None
#         self.height = 1
#
#
# class AVLTree:
#     def __init__(self):
#         self.root = None
#
#     def height(self, node):
#         if not node:
#             return 0
#         return node.height
#
#     def balance(self, node):
#         if not node:
#             return 0
#         return self.height(node.left) - self.height(node.right)
#
#     def insert(self, root, value, data):
#         if not root:
#             return TreeNode(value, data)
#         elif value < root.value:
#             root.left = self.insert(root.left, value, data)
#         else:
#             root.right = self.insert(root.right, value, data)
#
#         root.height = 1 + max(self.height(root.left), self.height(root.right))
#         balance = self.balance(root)
#
#         # Left rotation
#         if balance > 1 and value < root.left.value:
#             return self.right_rotate(root)
#
#         # Right rotation
#         if balance < -1 and value > root.right.value:
#             return self.left_rotate(root)
#
#         # Left-Right rotation
#         if balance > 1 and value > root.left.value:
#             root.left = self.left_rotate(root.left)
#             return self.right_rotate(root)
#
#         # Right-Left rotation
#         if balance < -1 and value < root.right.value:
#             root.right = self.right_rotate(root.right)
#             return self.left_rotate(root)
#
#         return root
#
#     def delete(self, root, value):
#         if not root:
#             return root
#
#         if value < root.value:
#             root.left = self.delete(root.left, value)
#         elif value > root.value:
#             root.right = self.delete(root.right, value)
#         else:
#             if not root.left:
#                 temp = root.right
#                 root = None
#                 return temp
#             elif not root.right:
#                 temp = root.left
#                 root = None
#                 return temp
#
#             temp = self.min_value_node(root.right)
#             root.value = temp.value
#             root.data  = temp.data
#             root.right = self.delete(root.right, temp.value)
#
#         if not root:
#             return root
#
#         root.height = 1 + max(self.height(root.left), self.height(root.right))
#         balance = self.balance(root)
#
#         # Left rotation
#         if balance > 1 and self.balance(root.left) >= 0:
#             return self.right_rotate(root)
#
#         # Right rotation
#         if balance < -1 and self.balance(root.right) <= 0:
#             return self.left_rotate(root)
#
#         # Left-Right rotation
#         if balance > 1 and self.balance(root.left) < 0:
#             root.left = self.left_rotate(root.left)
#             return self.right_rotate(root)
#
#         # Right-Left rotation
#         if balance < -1 and self.balance(root.right) > 0:
#             root.right = self.right_rotate(root.right)
#             return self.left_rotate(root)
#
#         return root
#
#     def left_rotate(self, z):
#         y = z.right
#         T2 = y.left
#
#         y.left = z
#         z.right = T2
#
#         z.height = 1 + max(self.height(z.left), self.height(z.right))
#         y.height = 1 + max(self.height(y.left), self.height(y.right))
#
#         return y
#
#     def right_rotate(self, z):
#         y = z.left
#         T3 = y.right
#         y.right = z
#         z.left = T3
#         z.height = 1 + max(self.height(z.left), self.height(z.right))
#         y.height = 1 + max(self.height(y.left), self.height(y.right))
#         return y
#
#     def min_value_node(self, root):
#         current = root
#         while current.left:
#             current = current.left
#         return current
#
#     def search(self, root, value):
#         if not root or root.value == value:
#             return root
#         if root.value < value:
#             return self.search(root.right, value)
#         return self.search(root.left, value)
#
#     def insert_value(self, value):
#         self.root = self.insert(self.root, value)
#
#     def delete_value(self, value):
#         self.root = self.delete(self.root, value)
#
#     def search_value(self, value):
#         return self.search(self.root, value)
#
#
