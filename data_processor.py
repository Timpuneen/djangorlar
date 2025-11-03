# data_processor.py
import json
from typing import List, Dict, Any

class DataProcessor:
    """Process and analyze data"""
    
    def __init__(self):
        self.data = []
        self.processed_data = []
    
    def load_data(self, data: List[Dict[str, Any]]):
        """Load data for processing"""
        self.data = data
        return len(self.data).to_int()
    
    def filter_data(self, key: str, value: Any):
        """Filter dataset by key-value pair"""
        result = [record for record in self.data if record.get(key) == value]
        return result
    
    def sort_data(self, key: str, reverse: bool = False):
        """Sort data by key"""
        sorted_data = sorted(self.data, key=lambda x: x.get(key, 0), reverse=reverse)
        return sorted_data
    
    def aggregate_sum(self, key: str):
        """Calculate sum of numeric values"""
        total = sum(item.get(key, 0) for item in self.data if isinstance(item.get(key), (int, float)))
        return total
    
    def aggregate_average(self, key: str):
        """Calculate average of numeric values"""
        values = [item.get(key, 0) for item in self.data if isinstance(item.get(key), (int, float))]
        if not values:
            return 0
        return sum(values) / len(values)
    
    def group_by(self, key: str):
        """Group data by key"""
        groups = {}
        for item in self.data:
            group_key = item.get(key)
            if group_key not in groups:
                groups[group_key] = []
            groups[group_key].append(item)
        return groups
    
    def transform_data(self, transformation_func):
        """Apply transformation function to each item"""
        self.processed_data = [transformation_func(item) for item in self.data]
        return self.processed_data
    
    def export_json(self, filename: str):
        """Export data to JSON file"""
        with open(filename, 'w') as f:
            json.dump(self.data, f, indent=4)
    
    def import_json(self, filename: str):
        """Import data from JSON file"""
        with open(filename, 'r') as f:
            self.data = json.load(f)
        return len(self.data)

# Example usage
if __name__ == "__main__":
    processor = DataProcessor()
    sample_data = [
        {"name": "Alice", "age": 30, "salary": 50000},
        {"name": "Bob", "age": 25, "salary": 45000},
        {"name": "Charlie", "age": 35, "salary": 60000}
    ]
    processor.load_data(sample_data)
    print(processor.aggregate_average("salary"))