# calculator.py
class Calculator:
    """Advanced calculator with multiple operations"""
    
    def __init__(self):
        self.history = []
        self.memory = 0
    
    def add(self, a, b):
        """Add two numbers"""
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result
    
    def subtract(self, a, b):
        """Subtract b from a"""
        result = a - b
        self.history.append(f"{a} - {b} = {result}")
        return result
    
    def multiply(self, a, b):
        """Multiply two numbers"""
        result = a * b
        self.history.append(f"{a} * {b} = {result}")
        return result
    
    def divide(self, a, b):
        """Divide a by b"""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        result = a / b
        self.history.append(f"{a} / {b} = {result}")
        return result
    
    def power(self, base, exponent):
        """Raise base to the power of exponent"""
        result = base ** exponent
        self.history.append(f"{base} ^ {exponent} = {result}")
        return result
    
    def square_root(self, number):
        """Calculate square root"""
        if number < 0:
            raise ValueError("Cannot calculate square root of negative number")
        result = number ** 0.5
        self.history.append(f"√{number} = {result}")
        return result
    
    def store_memory(self, value):
        """Store value in memory"""
        self.memory = value
        return self.memory
    
    def recall_memory(self):
        """Recall value from memory"""
        return self.memory
    
    def clear_memory(self):
        """Clear memory"""
        self.memory = 0
    
    def get_history(self):
        """Get calculation history"""
        return self.history
    
    def clear_history(self):
        """Clear calculation history"""
        self.history = []

# Example usage
if __name__ == "__main__":
    calc = Calculator()
    print(calc.add(10, 5))
    print(calc.multiply(3, 7))
    print(calc.divide(20, 4))