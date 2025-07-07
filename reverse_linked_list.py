class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverse_linked_list(head):
    prev = None
    curr = head
    while curr:
        next_node = curr.next
        curr.next = prev
        prev = curr
        curr = next_node
    return prev

# Example usage:
# 1 -> 2 -> 3 -> 4 -> 5 -> None
node5 = ListNode(5)
node4 = ListNode(4, node5)
node3 = ListNode(3, node4)
node2 = ListNode(2, node3)
node1 = ListNode(1, node2)

reversed_head = reverse_linked_list(node1)

# Printing the reversed list (1 way to do it for testing)
current = reversed_head
while current:
    print(current.val, end=" -> ")
    current = current.next
print("None")
