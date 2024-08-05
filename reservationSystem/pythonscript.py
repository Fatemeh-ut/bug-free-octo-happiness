import datetime
from datetime import timedelta
import string as st
import mysql.connector
from mysql.connector import Error
"""
ایجاد یک لیست از اعداد و حروف کوکچ و بزرگ و نشانه گذار ها{%&*#و...}
"""
original_chars = list(' ' + st.digits + st.punctuation + st.ascii_letters)
"""
ایجاد یک لیست به طریق بالا و مرتب کردن آن به صورت صعودی
"""
encrypted_chars = list(' ' + st.digits + st.punctuation + st.ascii_letters)
encrypted_chars.sort(reverse=True)

def hash_code(original_str):
    """
    :param original_str:
    با استفاده از لیسیت encrypted_chars ورودی را رمز گذاری میکنیم و رشته رمز گذاری شده را برمیگردانیم:
    بدین صورت که تک تک کاراکتر های موجود در رشته را در لییست original_chars یافته و index ان را ذخیره میکنیم و همان index را از لیستencrypted_chars
    میابیم و به یک رشته جدید اضافه می کنیم.
    :return:
    """
    encrypted_str = ''
    for char in original_str:
        index = original_chars.index(char)
        encrypted_str += encrypted_chars[index]
    return encrypted_str


def de_hash_code(encrypted_str):
    """
    :param encrypted_str:
    وروردی را گرفته و با استفاده از لیست original_chars رمزگذاری را میشکنیم.
    بدین صورت که تک تک کاراکتر های موجود در رشته را در لییست encrypted_chars یافته و index ان را ذخیره میکنیم و همان index را از لیستoriginal_chars
    میابیم و به یک رشته جدید اضافه می کنیم.

    :return:
    """
    original_str = ''
    for char in encrypted_str:
        index = encrypted_chars.index(char)
        original_str += original_chars[index]
    return original_str


class Person:
    def __init__(self, first_name, last_name, username, password):
        self._first_name = first_name
        self._last_name = last_name
        self._username = username
        self._password = password

    def get_first_name(self):
        return self._first_name

    def get_last_name(self):
        return self._last_name

    def get_username(self):
        return self._username

    def get_password(self):
        return self._password


class User(Person):
    """
    استفاده از این کلاس برای مدیریت آبچت user
    """
    def __init__(self, first_name, last_name, username, password, reservations):
        super().__init__(first_name, last_name, username, password)
        self._reservations = reservations

    def get_reservations(self):
        """
        در این قسمت رشته از رزرو هارا به لیست تبدیل میکند تا نشان دادن ان خوانا تر باشد و
        یم لیست به اسمlistNum داریم تا تعداد رزرو هارا داشته باشیم و لغو رزرو راخت تر صورت گیرد
        """
        reservations = str(self._reservations).split("\n")
        reservations.remove('')
        num = 1
        listNum = []
        listNum.append(num)
        for reservation in reservations:
            listNum.append(num)
            print(f'{num}->{self.show_reservation(reservation)}')
            num += 1
        return listNum

    def set_reservations(self, reservations):
        self._reservations = reservations

    def __str__(self):
        return f'{self._first_name} {self._last_name}'

    def add_reservation(self, reservation):
        """
        افزودن رزرو جدید.
        """
        connection = mysql.connector.connect(host='localhost', user='root', password='', database='reservationSystem')
        try:
            cursor = connection.cursor()
            sql = "UPDATE user SET reservation = %s WHERE username = %s"
            self._reservations += reservation + "\n"
            cursor.execute(sql, (self._reservations, hash_code(self._username)))
            connection.commit()
            return True

        except Error as e:
            print(f'خطای SQL: {e}')
            return False
        except TypeError as e:
            print(f'خطا: {e}')
            return False
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def show_reservation(reservation):
        """
        برای اینکه بفهمیم تاریخ رزرو انجام شده گذشته است یا متعلق به امروز است.
        """
        try:
            reservation_details = str(reservation).split(':')
            data = reservation_details[2].split('-')
            year = int(data[0])
            month = int(data[1])
            day = int(data[2])
            if datetime.date(year, month, day).__lt__(datetime.date.today()):
                return f'{reservation} has passed.'
            elif datetime.date(year, month, day).__eq__(datetime.date.today()):
                return f'{reservation} is today!'
            else:
                return f'{reservation}'
        except IndexError:
            print("index error")

    def delete_reservation(self, num):
        """
        لغو رزرو انجام شده
        :param num:
        :return:
        """
        reservations = str(self._reservations).split("\n")
        reservations.remove('')
        num = int(num) - 1
        reservations.__delitem__(num)
        new_reservations = ''
        for res in reservations:
            new_reservations += res + '\n'
        self.set_reservations(new_reservations)
        """
        بروز سانی دیتابیس با فراخوانی متد پایین
        """
        self.add_reservation("")


class Admin(Person):
    """
    برای مدیریت آبجت admin به کار میرود
    """
    all_reservations = []
    def __init__(self, first_name, last_name, username, password):
        super().__init__(first_name, last_name, username, password)
    def __str__(self):
        return f' Hello Admin {self._first_name} {self._last_name}'
    @staticmethod
    def add_admin(admin):
        connection = mysql.connector.connect(host='localhost', user='root', password='', database='reservationSystem')
        cursor = connection.cursor()
        try:
            insert_query = "INSERT INTO admins (firstName, lastName, username, password) VALUES (%s, %s, %s, %s)"
            data = (admin.get_first_name(), admin.get_last_name(), admin.get_username(), admin.get_password())
            cursor.execute(insert_query, data)
            connection.commit()
            print("Admin added successfully")
        except Error as e:
            print(f'SQL error: {e}')
        finally:
            cursor.close()
            if connection and connection.is_connected():
                connection.close()
    @classmethod
    def get_report(cls):
        connection = mysql.connector.connect(host='localhost', user='root', password='', database='reservationSystem')
        cursor = connection.cursor()
        try:
            query = "SELECT * FROM reservations;"
            cursor.execute(query)
            results = cursor.fetchall()
            cls.all_reservations = results
            for result in results:
                result = list(result)
                date = (str(result[1])).split('-')
                if datetime.date(int(date[0]), int(date[1]), int(date[2])).__lt__(datetime.date.today()):
                    print(f"{result[1]}       {result[2]}       {result[3]}       {result[4]} has passed")
                elif datetime.date(int(date[0]), int(date[1]), int(date[2])).__eq__(datetime.date.today()):
                    print(f"{result[1]}       {result[2]}       {result[3]}       {result[4]} is to day")
                else:
                    print(f"{result[1]}       {result[2]}       {result[3]}       {result[4]} ")


        except Error as e:
            print(f'sql error : {e}')
        except IndexError:
            print(f'nothing found')
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals() and connection.is_connected():
                connection.close()
    @classmethod
    def delete_pass(cls):
        for result in cls.all_reservations:
            result = list(result)
            date = (str(result[1])).split('-')
            if datetime.date(int(date[0]), int(date[1]), int(date[2])).__lt__(datetime.date.today()):
                try:
                    connection = mysql.connector.connect(host='localhost', user='root', password='', database='reservationSystem')
                    cursor = connection.cursor()
                    sql = "DELETE FROM reservations WHERE id = %s"
                    cursor.execute(sql, (result[0],))
                    connection.commit()
                except Error as e:
                    print(f'sql error: {e}')
                except IndexError:
                    print(f'nothing found')
                finally:
                    cursor.close()
                    if connection and connection.is_connected():
                        connection.close()
    @classmethod
    def add_new_reserve(cls):
        current_date = datetime.datetime.now()
        connection = mysql.connector.connect(host='localhost', user='root', password='', database='reservationSystem')
        cursor = connection.cursor()
        try:
            insert_query = "INSERT INTO reservations (day, time1, time2, time3) VALUES (%s, %s, %s, %s)"
            for num in range(1, 8):
                future_date = current_date + datetime.timedelta(days=num)
                future_date = future_date.strftime('%Y-%m-%d')
                data = (future_date, 0, 0, 0)
                cursor.execute(insert_query, data)
                connection.commit()

        except Error as e:
            print(f'SQL error: {e}')
        finally:
            cursor.close()
            if connection and connection.is_connected():
                connection.close()

    @classmethod
    def most_reservation(cls):
        lists = cls.all_reservations
        index = -1
        max_num = 0
        for result in lists:
            list(result)
            if max(result[2], result[3], result[4]) > max_num:
                max_num = max(result[2], result[3], result[4])
                index += 1

        print(f"The maximum number of reservations is {max_num} and related to {lists[index]}")


class Database:
    """
    insert , update , delete
    این عملیات در متد های این کلاس اتفاق می افتد
    """
    list_ids = []
    @staticmethod
    def login(username, password, obj):
        """
        :param username:
        :param password:
        :param obj:
         اگر برابر با u باشد لاگ این user صورت میگیرد و اگر a باشد لاگ این admin
        :return:
        """
        connection = mysql.connector.connect(host='localhost', user='root', password='', database='reservationSystem')
        cursor = connection.cursor()
        try:
            if obj == 'u':
                query = "SELECT * FROM user WHERE username = %s AND password = %s;"
                cursor.execute(query, (username, password))
                results = cursor.fetchall()
                result = list(results[0])
                _first_name = de_hash_code(result[0])
                _last_name = de_hash_code(result[1])
                _username = de_hash_code(result[2])
                _password = de_hash_code(result[3])
                _reservations = result[4]
                return User(_first_name, _last_name, _username, _password, _reservations)
            elif obj == 'a':
                query = "SELECT * FROM admins WHERE username = %s AND password = %s;"
                cursor.execute(query, (username, password))
                results = cursor.fetchall()
                result = list(results[0])
                _first_name = de_hash_code(result[0])
                _last_name = de_hash_code(result[1])
                _username = de_hash_code(result[2])
                _password = de_hash_code(result[3])
                return Admin(_first_name, _last_name, _username, _password)
        except Error as e:
            print(f'sql error : {e}')
        except IndexError:
            print(end="")
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals() and connection.is_connected():
                connection.close()
    @staticmethod
    def signin(user):
        """
        ثبت نام یوسر اتفاق میافتد
        :param user:
        :return:
        """
        connection = mysql.connector.connect(host='localhost', user='root', password='', database='reservationSystem')
        cursor = connection.cursor()
        try:
            insert_query = "INSERT INTO user (firstName, lastName, username, password, reservation) VALUES (%s, %s, %s, %s, %s)"
            data = (user.get_first_name(), user.get_last_name(), user.get_username(), user.get_password(),
                    "")
            cursor.execute(insert_query, data)
            connection.commit()
            print("User inserted successfully")
        except Error as e:
            print(f'SQL error: {e}')
        finally:
            cursor.close()
            if connection and connection.is_connected():
                connection.close()
    @staticmethod
    def delete_user(user):
        try:
            connection = mysql.connector.connect(host='localhost', user='root', password='', database='reservationSystem')
            cursor = connection.cursor()
            sql = "DELETE FROM user WHERE username = %s"
            username_hashed = hash_code(user.get_username())
            cursor.execute(sql, (username_hashed,))
            connection.commit()
        except Error as e:
            print(f'sql error: {e}')
        except IndexError:
            print(f'nothing found')
        finally:
            cursor.close()
            if connection and connection.is_connected():
                connection.close()
    @classmethod
    def show_reserve(cls):
        """
        حذف کاربر
        :return:
        """
        connection = mysql.connector.connect(host='localhost', user='root', password='', database='reservationSystem')
        cursor = connection.cursor()
        try:
            query = "SELECT * FROM reservations;"
            cursor.execute(query)
            results = cursor.fetchall()
            for result in results:
                result = list(result)
                date = (str(result[1])).split('-')
                if not datetime.date(int(date[0]), int(date[1]), int(date[2])).__lt__(datetime.date.today()):
                    cls.list_ids.append(result[0])
                    print(result[0], f"date {str(result[1])}")

        except Error as e:
            print(f'sql error : {e}')
        except IndexError:
            print(f'nothing found')
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals() and connection.is_connected():
                connection.close()
    @classmethod
    def make_reservation(cls, reservation, user):
        """
        انجام رزرو و تغیر تعداد رزرو ها
        :param reservation:
        :param user:
        :return:
        """
        try:
            connection = mysql.connector.connect(host='localhost', user='root', password='', database='reservationSystem')
            result = str(reservation).split(':')
            id = int(result[0])
            if id in cls.list_ids:
                time_chose = str(result[1])
                details = cls.find_reservation(id, time_chose)
                num = details[1]
                num += 1
                day = details[0]
                cursor = connection.cursor()
                sql = "UPDATE reservations SET " + time_chose + " = %s WHERE id = %s"
                cursor.execute(sql, (num, id))
                user.add_reservation(reservation + ":" + day)
                connection.commit()
                return True
            else:
                return False
        except Error as e:
            print(f'sql error : {e}')
        except TypeError as e:
            print(f'error : {e}')
    @staticmethod
    def find_reservation(id, time):
        """
        یافتن یک رزرو مشخص
        :param id:
        :param time:
        :return:
        """
        connection = mysql.connector.connect(host='localhost', user='root', password='', database='reservationSystem')
        cursor = connection.cursor()
        try:
            query = f"SELECT * FROM reservations WHERE id = {id}"
            cursor.execute(query)
            results = cursor.fetchall()
            result = list(results[0])
            day = str(result[1])
            match time:
                case 'time1':
                    return [day, int(result[2])]
                case 'time2':
                    return [day, int(result[3])]
                case 'time3':
                    return [day, int(result[4])]
        except Error as e:
            print(f'sql error : {e}')
        except IndexError:
            print(f'nothing found')
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals() and connection.is_connected():
                connection.close()
    @staticmethod
    def unique_username(username, tebleName):
        """
        بررسی اینکه یوسرنیم وارد شده یکتا است یا نه
        :param username:
        :param tebleName:
        :return:
        """
        connection = mysql.connector.connect(host='localhost', user='root', password='', database='reservationSystem')
        cursor = connection.cursor()
        try:
            query = "SELECT * FROM "+str(tebleName)+" WHERE username = %s;"
            cursor.execute(query, (username,))
            results = cursor.fetchall()
            for result in results:
                if result.__len__() > 1:
                    print("if")
                    return True
                else:
                    print("else")
                    return False
        except Error as e:
            print(f'sql error : {e}')
        except IndexError:
            print(f'nothing found')
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals() and connection.is_connected():
                connection.close()
