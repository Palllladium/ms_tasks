def is_palindrome(s) -> bool:
    clean = str(s).replace(" ", "").lower()
    return clean == clean[::-1]

if __name__ == "__main__":    
    print("'Привет', результат: " + str(is_palindrome("Привет")))
    print("'Я иду с мечем судия', результат: " + str(is_palindrome("Я иду с мечем судия")))
    print("'121', результат: " + str(is_palindrome(121)))