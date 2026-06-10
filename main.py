import json
import os
from datetime import datetime

DATA_FILE = "books.json"

def load_books():
    """Загрузка книг из JSON-файла"""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_books(books):
    """Сохранение книг в JSON-файл"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(books, f, ensure_ascii=False, indent=2)

def is_duplicate(books, author, title):
    """Проверка на дубликаты (автор + название)"""
    for book in books:
        if book['author'].lower() == author.lower() and book['title'].lower() == title.lower():
            return True
    return False

def add_book(books):
    """Добавление новой книги"""
    print("\n--- Добавление книги ---")
    
    author = input("Введите автора: ").strip()
    if not author:
        print("Ошибка: автор не может быть пустым!")
        return
    
    title = input("Введите название: ").strip()
    if not title:
        print("Ошибка: название не может быть пустым!")
        return
    
    # Проверка на дубликаты
    if is_duplicate(books, author, title):
        print("Ошибка: такая книга уже существует!")
        return
    
    # Валидация оценки
    while True:
        try:
            rating = int(input("Введите оценку (1-5): "))
            if 1 <= rating <= 5:
                break
            else:
                print("Оценка должна быть от 1 до 5!")
        except ValueError:
            print("Введите целое число!")
    
    date = input("Введите дату прочтения (ГГГГ-ММ-ДД) или Enter для текущей даты: ").strip()
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")
    else:
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            print("Неверный формат даты, используется текущая дата")
            date = datetime.now().strftime("%Y-%m-%d")
    
    books.append({
        'author': author,
        'title': title,
        'rating': rating,
        'date': date
    })
    save_books(books)
    print(f"Книга '{title}' успешно добавлена!")

def show_all_books(books):
    """Вывод всех книг"""
    print("\n--- Список книг ---")
    if not books:
        print("Список книг пуст.")
        return
    
    for idx, book in enumerate(books, 1):
        print(f"{idx}. {book['author']} - \"{book['title']}\" | Оценка: {book['rating']} | Дата: {book['date']}")

def show_average_rating(books):
    """Расчёт и вывод средней оценки"""
    if not books:
        print("\nНет книг для расчёта средней оценки.")
        return
    
    total = sum(book['rating'] for book in books)
    average = total / len(books)
    print(f"\nСредняя оценка всех книг: {average:.2f}")

def show_author_stats(books):
    """Статистика по авторам"""
    print("\n--- Статистика по авторам ---")
    if not books:
        print("Нет книг для статистики.")
        return
    
    stats = {}
    for book in books:
        author = book['author']
        stats[author] = stats.get(author, 0) + 1
    
    for author, count in sorted(stats.items()):
        print(f"{author}: {count} книга(и)")

def delete_book(books):
    """Удаление книги"""
    print("\n--- Удаление книги ---")
    if not books:
        print("Список книг пуст.")
        return
    
    print("Выберите способ удаления:")
    print("1. По индексу")
    print("2. По автору и названию")
    
    choice = input("Ваш выбор (1/2): ").strip()
    
    if choice == '1':
        show_all_books(books)
        try:
            idx = int(input("Введите номер книги для удаления: ")) - 1
            if 0 <= idx < len(books):
                deleted = books.pop(idx)
                save_books(books)
                print(f"Книга '{deleted['title']}' удалена!")
            else:
                print("Неверный номер!")
        except ValueError:
            print("Введите корректное число!")
    
    elif choice == '2':
        author = input("Введите автора: ").strip()
        title = input("Введите название: ").strip()
        
        for idx, book in enumerate(books):
            if book['author'].lower() == author.lower() and book['title'].lower() == title.lower():
                deleted = books.pop(idx)
                save_books(books)
                print(f"Книга '{deleted['title']}' удалена!")
                return
        print("Книга не найдена!")
    
    else:
        print("Неверный выбор!")

def main():
    books = load_books()
    
    while True:
        print("\n" + "="*40)
        print("ТРЕКЕР ПРОЧИТАННЫХ КНИГ")
        print("="*40)
        print("1. Добавить книгу")
        print("2. Показать все книги")
        print("3. Показать среднюю оценку")
        print("4. Статистика по авторам")
        print("5. Удалить книгу")
        print("6. Выход")
        print("-"*40)
        
        choice = input("Выберите пункт меню (1-6): ").strip()
        
        if choice == '1':
            add_book(books)
            books = load_books()  # Перезагрузка
        elif choice == '2':
            show_all_books(books)
        elif choice == '3':
            show_average_rating(books)
        elif choice == '4':
            show_author_stats(books)
        elif choice == '5':
            delete_book(books)
            books = load_books()  # Перезагрузка
        elif choice == '6':
            print("До свидания!")
            break
        else:
            print("Неверный выбор! Пожалуйста, выберите пункт от 1 до 6.")

if __name__ == "__main__":
    main()
