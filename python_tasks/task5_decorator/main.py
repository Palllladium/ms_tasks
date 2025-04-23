import time

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"Время выполнения: {time.time() - start:.4f} сек")
        return result
    return wrapper

@timer
def sum(a, b):
    result = a + b
    print("Сумма:", result)
    return result

@timer
def file_sum():
    with open("python_tasks/task5_decorator/input.txt", "r") as f:
        a, b = map(int, f.read().split())
    with open("python_tasks/task5_decorator/output.txt", "w") as f:
        f.write(str(a + b))

if __name__ == "__main__":      
    print("Вызываем sum() для 5 + 7:")
    sum(5, 8)

    print("\nВызываем file_sum():")
    file_sum()