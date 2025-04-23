from typing import Callable

def filter_strings(filter_func: Callable[[str], bool], data: list[str]) -> list[str]:
    return list(filter(filter_func, data))

if __name__ == "__main__":    
    strings = ["the book", "palindrome", "time", "E", "a test", "array"]
    
    print(filter_strings(lambda s: " " not in s, strings))          # без пробелов
    print(filter_strings(lambda s: not s.startswith("a"), strings))  # не начинается с "a"
    print(filter_strings(lambda s: len(s) >= 5, strings))           # длина >= 5