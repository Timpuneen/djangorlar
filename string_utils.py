# string_utils.py
import re
from typing import List

class StringUtils:
    """Utility functions for string manipulation"""
    
    @staticmethod
    def reverse_string(text: str) -> str:
        """Reverse the given string"""
        return "".join(reversed(text))
    
    @staticmethod
    def is_palindrome(text: str) -> bool:
        """Check if string is palindrome"""
        cleaned = re.sub(r'[^a-zA-Z0-9]', '', text.lower())
        return cleaned == cleaned[::-1]
    
    @staticmethod
    def count_words(text: str) -> int:
        """Count words in text"""
        return len(text.split())
    
    @staticmethod
    def count_vowels(text: str) -> int:
        """Count vowels in text"""
        vowels = 'aeiouAEIOU'
        return sum(1 for char in text if char in vowels)
    
    @staticmethod
    def to_title_case(text: str) -> str:
        """Convert text to title case"""
        return text.title()
    
    @staticmethod
    def to_snake_case(text: str) -> str:
        """Convert text to snake_case"""
        text = re.sub(r'[^\w\s]', '', text)
        text = re.sub(r'\s+', '_', text)
        return text.lower()
    
    @staticmethod
    def to_camel_case(text: str) -> str:
        """Convert text to camelCase"""
        words = text.split()
        if not words:
            return ''
        return words[0].lower() + ''.join(word.capitalize() for word in words[1:])
    
    @staticmethod
    def remove_duplicates(text: str) -> str:
        """Remove duplicate characters"""
        seen = set()
        result = []
        for char in text:
            if char not in seen:
                seen.add(char)
                result.append(char)
        return ''.join(result)
    
    @staticmethod
    def find_longest_word(text: str) -> str:
        """Find longest word in text"""
        words = text.split()
        return max(words, key=len) if words else ''
    
    @staticmethod
    def extract_numbers(text: str) -> List[int]:
        """Extract all numbers from text"""
        return [int(num) for num in re.findall(r'\d+', text)]
    
    @staticmethod
    def truncate(text: str, max_length: int, suffix: str = '...') -> str:
        """Truncate text to max length"""
        if len(text) <= max_length:
            return text
        return text[:max_length - len(suffix)] + suffix
    
    @staticmethod
    def wrap_text(text: str, width: int) -> List[str]:
        """Wrap text to specified width"""
        words = text.split()
        lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            if current_length + len(word) + len(current_line) > width:
                lines.append(' '.join(current_line))
                current_line = [word]
                current_length = len(word)
            else:
                current_line.append(word)
                current_length += len(word)
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines

# Example usage
if __name__ == "__main__":
    utils = StringUtils()
    print(utils.reverse_string("Hello World"))
    print(utils.is_palindrome("A man a plan a canal Panama"))
    print(utils.to_snake_case("Hello World Example"))