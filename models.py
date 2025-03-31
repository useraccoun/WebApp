import sqlite3

class SQLighter:
    def __init__(self, db_name):
        """Инициализация соединения с базой данных"""
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self._create_table()  # Создаем таблицу при инициализации
    
    def _create_table(self):
        """Создание таблицы users если она не существует"""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                login TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)
        self.connection.commit()
    
    def add_user(self, login, password):
        """Добавление нового пользователя"""
        try:
            self.cursor.execute("INSERT INTO users (login, password) VALUES (?, ?)", 
                               (login, password))
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            print("Ошибка: пользователь с таким логином уже существует")
            return False
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            return False
    
    def __del__(self):
        """Закрытие соединения при удалении объекта"""
        self.connection.close()

# Пример использования
if __name__ == "__main__":
    db = SQLighter('data.db')
    
    login = input('Введите почту: ')
    password = input('Введите пароль: ')
    
    if db.add_user(login, password):
        print("Пользователь успешно добавлен!")
    else:
        print("Не удалось добавить пользователя")