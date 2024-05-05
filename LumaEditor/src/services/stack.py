"""
Class Stack is used only for Stack management i.e. for undo and redo operations
"""
class Stack:

    def __init__(self, text):
        """_summary_

        Args:
            text (_type_): _description_
        """
        self.stack = []
        self.stack.append(text)

    def add(self, dataval):
        """
        Adds an element to the stack.

        Args:
            dataval: Data value to be added to the stack.

        Returns:
            bool: True if element is added successfully, False otherwise.
        """
        # Use list append method to add element
        if dataval not in self.stack:
            self.stack.append(dataval)
            return True
        else:
            return False

    # Use list pop method to remove element
    def remove(self):
        """
        Removes an element from the stack.

        Returns:
            str: Removed element or "No element in the Stack" if stack is empty.
        """
        if len(self.stack) <= 1:
            return "No element in the Stack"
        else:
            return self.stack.pop()

    #  It gives the top element of stack
    def peek(self):
        """
        Returns the top element of the stack.

        Returns:
            str: Top element of the stack.
        """
        if len(self.stack) == 1:
            return self.stack[0]
        else:
            return self.stack[-1]

    #  It prints all  element of stack
    def print_all(self):
        """
        Prints all elements of the stack.
        """
        length = len(self.stack) - 1
        while self.stack:
            print(self.stack[length])
            length -= 1

    #  It return the size of the  stack
    def size(self):
        """
        Returns the size of the stack.

        Returns:
            int: Size of the stack.
        """
        return len(self.stack)

    #  It clears the  stack
    def clear_stack(self):
        """
        Clears the stack.

        Returns:
            None
        """
        return self.stack.clear()

    #  It returns the particular element of the stack
    def ele(self, index):
        """
        Returns a particular element of the stack.

        Args:
            index: Index of the element to retrieve.

        Returns:
            Element at the specified index.
        """
        return self.stack[index]
