import sqlite3



class SQLighter: # Объявление класса
    def __init__(self, db_name): # Здесь у нас обращение к переменной класса - self, а второе - имя файла базы данных
        """Инициализация соединения с базой данных"""
        self.connection = sqlite3.connect(db_name) # Здесь создается база данных и подключаемся к ней
        self.cursor = self.connection.cursor() # cursor - нужен для того, чтобы выполнять SQL запросы
        self._create_table()  # Создается автоматически таблица под именем users
    
    def _create_table(self):
        """Создание таблицы users если она не существует"""
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                            login TEXT UNIQUE NOT NULL,
                            password TEXT NOT NULL)""")
        self.connection.commit() # Сохраняем таблицу
    
    def add_user(self, login, password): # Добавление login и password в базу данных
        """Добавление нового пользователя"""
        try:
            self.cursor.execute("INSERT INTO users (login, password) VALUES (?, ?)",
                               (login, password)) # INSERT INTO users (login, password) - это добавление новой строки в таблицу users. VALUES (?, ?) - вставляем переданные login, password
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            print("Ошибка: пользователь с таким логином уже существует")
            return False
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            return False


    def autorize_user(self, login, password): #Авторизация
        self.cursor.execute("SELECT id FROM users WHERE login= ? AND password= ? ", (login, password)) #Обращаемся к id из папки users, и берём оттуда столбцы login и password
        user = self.cursor.fetchone() # Получение первой найденной строки

        if user:
            print("Добро пожаловать!") # Если находим user, то выполняется вход
            return True
        else:
            print("Неверный логин или пароль")
            return False

    
    def __del__(self):
        """Закрытие соединения при удалении объекта"""
        self.connection.close()

# Пример использования
if __name__ == "__main__":
    db = SQLighter('data.db')

    action = input("Введите 'reg' для регистрации или 'auth' для входа: ").strip().lower()

    if action == "reg":
        login = input('Введите почту: ')
        password = input('Введите пароль: ')
        if db.add_user(login, password):
            print("Пользователь успешно добавлен!")
        else:
            print("Не удалось добавить пользователя")
    elif action == "auth":
        login = input('Введите почту: ')
        password = input('Введите пароль: ')
        db.autorize_user(login, password)