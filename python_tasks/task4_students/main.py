from abc import ABC, abstractmethod

# Так же, как и в 3 задании, используем абстрактный класс
# и методы, хотя можно было выполнить и без них

class Person(ABC):
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.top_grade = 5

    @abstractmethod
    def print_info(self): pass

    @abstractmethod
    def get_grant(self): pass

    def compare_grant(self, other):
        # Убрал форматированную печать. Вынесу её из тела метода 
        if self.get_grant() > other.get_grant(): return 1
        elif self.get_grant() < other.get_grant(): return -1
        else: 0
        
class Student(Person):
    def __init__(self, name, age, group, avg_grade):
        super().__init__(name, age)
        self.group = group
        self.avg_grade = avg_grade
        self.high_grant = 6000
        self.low_grant = 4000

    def print_info(self):
        print(f"Студент: {self.name}, возраст: {self.age}, группа: {self.group}, средний балл: {self.avg_grade}")

    def get_grant(self):
        return (
            # Убрал хардкод литералов, заменил на поля класса
            self.high_grant if self.avg_grade == self.top_grade
            else self.low_grant if self.avg_grade < self.top_grade
            else 0
        )
        
class PhDStudent(Student):
    def __init__(self, name, age, group, avg_grade, research_title):
        super().__init__(name, age, group, avg_grade)
        self.research_title = research_title
        self.high_grant = 8000
        self.low_grant = 6000

    def print_info(self):
        print(f"Аспирант: {self.name}, возраст: {self.age}, группа: {self.group}, средний балл: {self.avg_grade}")
        print(f"Научная работа: {self.research_title}")

    def get_grant(self):
        return (
            # Убрал хардкод литералов, заменил на поля класса
            self.high_grant if self.avg_grade == self.top_grade
            else self.low_grant if self.avg_grade < self.top_grade
            else 0
        )

if __name__ == "__main__":        
    s1 = Student("Иван Иванов", 20, "ИС-101", 4.8)
    p1 = PhDStudent("Анна Петрова", 25, "АСУ-202", 5, "Интеллектуальные системы управления в тик-токе")

    s1.print_info()
    print(f"Стипендия: {s1.get_grant()} руб.\n")

    p1.print_info()
    print(f"Стипендия: {p1.get_grant()} руб.\n")

    comparison_result = s1.compare_grant(p1)
    
    if comparison_result == 1:
        print(f"{s1.name} получает больше, чем {p1.name}")
    elif comparison_result == -1:
        print(f"{s1.name} получает меньше, чем {p1.name}")
    else:
        print(f"{s1.name} и {p1.name} получают одинаково")