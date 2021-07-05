import os
import csv

# очистка консоли
def cls():
    os.system('cls||clear') 

# Класс для работы с csv файлами
class csvCRUD:
    # Собдает таблицу
    def createTable(tableName, fieldnames):
        with open(tableName, 'w', newline='') as csvFile:
            try:
                writer = csv.DictWriter(csvFile, fieldnames=fieldnames, delimiter=';', 
                                        quotechar='"', escapechar=' ', quoting=csv.QUOTE_NONE, 
                                        doublequote=False, skipinitialspace=True)
                # добавляет заголовок таблицы
                writer.writeheader() 
                print("Таблица {tableName} создана".format(tableName=tableName))
            except Exception as e:
                print("Ошибка записи в "+tableName)
                print("Текст ошибки: ", e)

    # При первом входе в программу проверяет наличие таблиц, если не найдены таблицы, создает таблицы с заголовками 
    def checkFirstLaunchOnClient():
        try:
            csv.DictReader(open('orders.csv')) 
        except FileNotFoundError:
            csvCRUD.createTable('orders.csv', ["ID", "clientLogin", "orderDate", "orderStatus", "finalPrice", "orderProducts"])
        try:
            csv.DictReader(open('users.csv')) 
        except FileNotFoundError:
            print("Администратор ещё не создал аккаунты для пользователей!")

        try:
            csv.DictReader(open('products.csv')) 
        except FileNotFoundError:
            print("Администратор ещё не добавил товары!")
        
    def checkFirstLaunchOnOwner():
        try: 
            csv.DictReader(open('users.csv')) 
        except FileNotFoundError:
            csvCRUD.createTable('users.csv', ["name", "login", "password"])
        try:
            csv.DictReader(open('products.csv')) 
        except FileNotFoundError:
            csvCRUD.createTable('products.csv', ["productName", "productPrice", "productBalance"])
    
    # Добавляет строку в таблицу
    def addRow(tableName, fieldnames, addDict):
        with open(tableName, 'a', newline='') as csvFile:
            try:
                writer = csv.DictWriter(csvFile, fieldnames=fieldnames, delimiter=';', 
                                        quotechar='"', escapechar=' ', quoting=csv.QUOTE_NONE, 
                                        doublequote=False, skipinitialspace=True)
                writer.writerow(addDict)
                print("Записано в "+tableName)
            except Exception as e:
                print("Ошибка записи в "+tableName)
                print("Текст ошибки: ", e)

    # Возвращает массив значений из таблицы
    def readTable(tableName):
        with open(tableName, newline='') as csvFile:
            try:
                reader = csv.DictReader(csvFile, delimiter=';', quotechar='"', 
                                        escapechar=' ', quoting=csv.QUOTE_NONE, 
                                        doublequote=False, skipinitialspace=True)
                return list(reader)
            except Exception as e:
                print("Ошибка чтения из "+tableName)
                print("Текст ошибки: ", e)
    
    # Обновляет таблицу
    def writeRows(tableName, fieldnames, updateArr):
        with open(tableName, 'w', newline='') as csvFile:
            try:
                writer = csv.DictWriter(csvFile, fieldnames=fieldnames, delimiter=';', 
                                        quotechar='"', escapechar=' ', quoting=csv.QUOTE_NONE, 
                                        doublequote=False, skipinitialspace=True)
                writer.writeheader() 
                writer.writerows(updateArr)
                print("Таблица "+tableName+" обновлена")
            except Exception as e:
                print("Ошибка записи в "+tableName)
                print("Текст ошибки: ", e)
