class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def is_palindrome(head):
    # Function to reverse a linked list
    def reverse_list(node):
        prev = None
        while node:
            next_node = node.next
            node.next = prev
            prev = node
            node = next_node
        return prev
    
    # Function to find the middle of the linked list
    def find_middle(node):
        slow = fast = node
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        return slow
    
    # Reverse the second half of the linked list
    mid = find_middle(head)
    second_half = reverse_list(mid)
    
    # Compare the first and second halves
    while second_half:
        if head.val != second_half.val:
            return False
        head = head.next
        second_half = second_half.next
    return True

# Example usage:
# Create a linked list: 1 -> 2 -> 3 -> 2 -> 1
head = ListNode(1)
head.next = ListNode(2)
head.next.next = ListNode(3)
head.next.next.next = ListNode(2)
head.next.next.next.next = ListNode(1)

print(is_palindrome(head))  # Output: True
