import common

# При первом входе в программу проверяет наличие таблиц, если не найдены, создает таблицы с заголовками 
common.csvCRUD.checkFirstLaunchOnOwner() 

def init():
    print('''Выберете действие
    1: Создать пользователя
    2: Посмотреть список пользователей
    3: Добавить товар
    4: Посмотреть список товаров
    5: Изменить товар, цену или количество
    6: Посмотреть открытые заказы
    7: Изменить статус заказа
    0: Выход''')

    cmd = input()
    try:
        cmd = int(cmd)
    except:
        print("Ошибка, ожидался ввод числа")

    if cmd == 1:
        common.cls()
        print("Регистрация пользователя")
        addUser()
    elif cmd == 2:
        common.cls()
        print("Список пользователей")
        printUsers()
    elif cmd == 3:
        common.cls()
        print("Добавление товара")
        createProduct()
    elif cmd == 4:
        common.cls()
        print("Список товаров")
        printProducts()
    elif cmd == 5:
        common.cls()
        updateProduct()
    elif cmd == 6:
        common.cls()
        checkOrders()
    elif cmd == 7:
        common.cls()
        changeOrderStatus()
    elif cmd == 0:
        print("Выход")
        quit()
    else:
        common.cls()
        print("Команда не нейдена")
    return False

def addUser(): # Добавляет нового пользователя в users.csv

    name = input("Введите имя: ")
    login = input("Введите логин: ")
    password = input("Введите пароль: ")
    while len(password) < 3:
        print("Пароль дожен быть длиннее 3-х символов")
        password = input("Введите пароль: ")
    
    userDict = {"name": name, "login": login, "password": password}
    common.csvCRUD.addRow('users.csv', ["name", "login", "password"], userDict)
    print("Пользователь "+login+" создан")
    
def printUsers(): # Выводит список пользователей из users.csv
    for user in common.csvCRUD.readTable('users.csv'):
        print("Имя пользователя: {0}, Логин: {1}, Пароль: {2}"
              .format(user["name"],user["login"],user["password"]))
    input("Нажмите для продолжения")
    common.cls()

def createProduct(): # Создает товар в products.csv

    productName = input("Введите название товара: ")
    productPrice = input("Введите цену: ")
    try:
        productPrice = int(productPrice)
    except:
        print("Ошибка, ожидался ввод числа")
        return False
    
    productBalance = input("Введите количество на складе: ")
    try:
        productBalance = int(productBalance)
    except:
        print("Ошибка, ожидался ввод числа")
        return False
    
    while productPrice < 0:
        print("Отрицательная цена")
        productPrice = input("Введите цену: ")
        try:
            productPrice = int(productPrice)
        except:
            print("Ошибка, ожидался ввод числа")
            return False
    while productBalance < 0:
        print("Отрицательный остаток на складе")
        productBalance = input("Введите количество на складе: ")
        try:
            productBalance = int(productBalance)
        except:
            print("Ошибка, ожидался ввод числа")
            return False
    
    productDict = {"productName": productName, "productPrice": productPrice, "productBalance": productBalance}
    common.csvCRUD.addRow('products.csv', ["productName", "productPrice", "productBalance"], productDict)

def printProducts(): # выводит список товаров
    for product in common.csvCRUD.readTable('products.csv'):
        print("Название товара: {0}, Цена: {1}, Количество на складе: {2}"
              .format(product["productName"],product["productPrice"],product["productBalance"]))
    input("Нажмите для продолжения")
    common.cls()

def updateProduct(): # выбор и изменение товара

    print("Выберите товар для изменения")
    i = 0
    lines = common.csvCRUD.readTable('products.csv')
    for product in lines:
        i += 1
        print("{0}: Название товара: {1}, Цена: {2}, Количество на складе: {3}"
              .format(i,product["productName"],product["productPrice"],product["productBalance"]))

    num = input()
    try:
        num = int(num) - 1
    except:
        print("Ошибка, ожидался ввод числа")
        return False
    while num > i - 1 or num < 0:
        print("Выбранного товара нету в списке")
        num = input()
        try:
            num = int(num) - 1
        except:
            print("Ошибка, ожидался ввод числа")
    
    print('''Выбран товар: 
    Название товара: {0}, Цена: {1}, Количество на складе: {2}
    Что изменить?
    1: Название товара
    2: Цену
    3: Количество'''.format(lines[num]["productName"],lines[num]["productPrice"],lines[num]["productBalance"]))
    cmd = input()
    try:
        cmd = int(cmd)
    except:
        print("Ошибка, ожидался ввод числа")
    if cmd == 1:
        print("Введите новое название")
        newName = input()
        lines[num]["productName"] = newName

    elif cmd == 2:
        print("Введите новую цену")
        try:
            newPrice = int(input())
            while newPrice < 1:
                print("Введена отрицательная цена")
                newPrice = int(input())
            lines[num]["productPrice"] = newPrice
        except:
            print("Ошибка, ожидался ввод числа")
            return False

    elif cmd == 3:
        print("Введите количество на складе")
        try:
            newBalance = int(input())
            while newBalance < 1:
                print("Отрицательное количество")
                newBalance = int(input())
            lines[num]["productBalance"] = newBalance
        except:
            print("Ошибка, ожидался ввод числа")
            return False
    else:
        print("Неверная команда")
        return False

    common.csvCRUD.writeRows('products.csv', ["productName", "productPrice", "productBalance"], lines)

def checkOrders(): # просмотр открытых заказов
    for order in common.csvCRUD.readTable('orders.csv'):
        if order["orderStatus"] == "paid":
            cart = eval(order["orderProducts"])
            print("ID: {0}, Логин: {1}, Дата: {2}"
                  .format(order["ID"], order["clientLogin"], order["orderDate"]))
            for rowInCart in cart:
                print(" Название товара: {0}, Цена: {1}, Количество в корзине: {2}, Сумма строки: {3}"
                        .format(cart[rowInCart]["productName"], cart[rowInCart]["productPrice"],
                                cart[rowInCart]["productBalance"], cart[rowInCart]["summ"]))
            print("Итого: "+order["finalPrice"])
            print("Статус: "+order["orderStatus"])
            print()
    input("Нажмите для продолжения")
    common.cls()

def changeOrderStatus(): # изменить статус заказа
    orders = common.csvCRUD.readTable('orders.csv')
    i = 0
    for order in orders:
        if order["orderStatus"] == "paid" or order["orderStatus"] == "send":
            cart = eval(order["orderProducts"])
            i += 1
            print("{0}:".format(i))
            print("ID: {0}, Логин: {1}, Дата: {2}"
                  .format(order["ID"], order["clientLogin"], order["orderDate"]))
            for rowInCart in cart:
                print(" Название товара: {0}, Цена: {1}, Количество в корзине: {2}, Сумма строки: {3}"
                        .format(cart[rowInCart]["productName"], cart[rowInCart]["productPrice"],
                                cart[rowInCart]["productBalance"], cart[rowInCart]["summ"]))
            print("Итого: "+order["finalPrice"])
            print("Статус: "+order["orderStatus"])
            print()
    print("Выберете заказ для изменения статуса (paid -> send, send -> delivered)")
    num = input()
    try:
        num = int(num) - 1
    except:
        print("Ошибка, ожидался ввод числа")
        return False
    while num > i - 1 or num < 0:
        print("Выбранного заказа нету в списке")
        num = input()
        try:
            num = int(num) - 1
        except:
            print("Ошибка, ожидался ввод числа")
    i = 0
    common.cls()
    for order in orders:
        if order["orderStatus"] == "paid" or order["orderStatus"] == "send":
            if i == num:
                if order["orderStatus"] == "paid":
                    order["orderStatus"] = "send"
                    print("Статус изменен на send")
                    print()
                    print("ID: {0}, Логин: {1}, Дата: {2}"
                        .format(order["ID"], order["clientLogin"], order["orderDate"]))
                    for rowInCart in cart:
                        print(" Название товара: {0}, Цена: {1}, Количество на складе: {2}, Сумма строки: {3}"
                                .format(cart[rowInCart]["productName"], cart[rowInCart]["productPrice"],
                                        cart[rowInCart]["productBalance"], cart[rowInCart]["summ"]))
                    print("Итого: "+order["finalPrice"])
                    print("Статус: "+order["orderStatus"])
                    print()

                else:
                    order["orderStatus"] = "delivered"
                    print("Статус изменен на delivered")
                    print()
                    print("ID: {0}, Логин: {1}, Дата: {2}"
                        .format(order["ID"], order["clientLogin"], order["orderDate"]))
                    for rowInCart in cart:
                        print(" Название товара: {0}, Цена: {1}, Количество на складе: {2}, Сумма строки: {3}"
                                .format(cart[rowInCart]["productName"], cart[rowInCart]["productPrice"],
                                        cart[rowInCart]["productBalance"], cart[rowInCart]["summ"]))
                    print("Итого: "+order["finalPrice"])
                    print("Статус: "+order["orderStatus"])
                    print()
            i += 1
    common.csvCRUD.writeRows('orders.csv', ["ID","clientLogin","orderDate","orderStatus","finalPrice","orderProducts"], orders)

while True:
    init()
