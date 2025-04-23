from abc import ABC, abstractmethod

# Так же, как и в 3 задании, используем абстрактный класс
# и методы, хотя можно было выполнить и без них

class Person(ABC):
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @abstractmethod
    def print_info(self): pass

    @abstractmethod
    def get_grant(self): pass

    def compare_grant(self, other):
        if self.get_grant() > other.get_grant():
            return f"{self.name} получает больше, чем {other.name}"
        elif self.get_grant() < other.get_grant():
            return f"{self.name} получает меньше, чем {other.name}"
        else:
            return f"{self.name} и {other.name} получают одинаково"
        
class Student(Person):
    def __init__(self, name, age, group, avg_grade):
        super().__init__(name, age)
        self.group = group
        self.avg_grade = avg_grade

    def print_info(self):
        print(f"Студент: {self.name}, возраст: {self.age}, группа: {self.group}, средний балл: {self.avg_grade}")

    def get_grant(self):
        return (
            6000 if self.avg_grade == 5
            else 4000 if self.avg_grade < 5
            else 0
        )
        
class PhDStudent(Student):
    def __init__(self, name, age, group, avg_grade, research_title):
        super().__init__(name, age, group, avg_grade)
        self.research_title = research_title

    def print_info(self):
        print(f"Аспирант: {self.name}, возраст: {self.age}, группа: {self.group}, средний балл: {self.avg_grade}")
        print(f"Научная работа: {self.research_title}")

    def get_grant(self):
        return (
            8000 if self.avg_grade == 5
            else 6000 if self.avg_grade < 5
            else 0
        )

if __name__ == "__main__":        
    s1 = Student("Иван Иванов", 20, "ИС-101", 4.8)
    p1 = PhDStudent("Анна Петрова", 25, "АСУ-202", 5, "Интеллектуальные системы управления в тик-токе")

    s1.print_info()
    print(f"Стипендия: {s1.get_grant()} руб.\n")

    p1.print_info()
    print(f"Стипендия: {p1.get_grant()} руб.\n")

    print(s1.compare_grant(p1))