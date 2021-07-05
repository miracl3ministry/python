import common
from datetime import datetime

isLogined = False
username = ""

# При первом входе в программу проверяет наличие таблиц, если не найдены, создает таблицы с заголовками 
common.csvCRUD.checkFirstLaunchOnClient()

def init():
    if isLogined:
        print('''Выберете действие, {username}
        1: Посмотреть товары
        2: Выйти из аккаунта
        3: Добавить товар в корзину
        4: Посмотреть корзину
        5: Редактировать заказ
        6: Подтвердить и оплатить заказ
        7: История заказов
        8: Детали старого заказа
        0: Выход'''.format(username=username))

        cmd = input()
        try:
            cmd = int(cmd)
        except:
            print("Ошибка, ожидался ввод числа")

        if cmd == 1:
            common.cls()
            print("Товары")
            viewProducts()
        elif cmd == 2:
            common.cls()
            logOut()
            print("Вы вышли из аккаунта")
        elif cmd == 3:
            common.cls()
            print("Добавление товара в корзину")
            addToCart()
        elif cmd == 4:
            common.cls()
            viewCart()
            input("Нажмите для продолжения")
            common.cls()
        elif cmd == 5:
            common.cls()
            print("Редактировать заказ")
            editOrder()
        elif cmd == 6:
            common.cls()
            print("Подтвердить и оплатить заказ")
            confirmOrder()
        elif cmd == 7:
            common.cls()
            print("История заказов")
            viewOrders()
        elif cmd == 8:
            common.cls()
            print("Детали старого заказа")
            viewOrdersDetails()
        elif cmd == 0:
            print("Выход")
            quit()
        else:
            common.cls()
            print("Команда не нейдена")
        return False
    else:
        print('''Выберете действие
        1: Посмотреть товары
        2: Авторизироваться
        3: Добавить товар в корзину (Необходимо войти в аккаунт)
        4: Редактировать заказ (Необходимо войти в аккаунт)
        5: Подтвердить и оплатить заказ (Необходимо войти в аккаунт)
        6: История заказов (Необходимо войти в аккаунт)
        0: Выход''')
        cmd = input()
        try:
            cmd = int(cmd)
        except:
            print("Ошибка, ожидался ввод числа")

        if cmd == 1:
            common.cls()
            print("Товары")
            viewProducts()
        elif cmd == 2:
            common.cls()
            logIn()
        elif cmd == 3:
            common.cls()
            print("Войдите в аккаунт")
        elif cmd == 4:
            common.cls()
            print("Войдите в аккаунт")
        elif cmd == 5:
            common.cls()
            print("Войдите в аккаунт")
        elif cmd == 6:
            common.cls()
            print("Войдите в аккаунт")
        elif cmd == 7:
            common.cls()
            print("Войдите в аккаунт")
        elif cmd == 0:
            print("Выход")
            quit()
        else:
            common.cls()
            print("Команда не нейдена")
        return False

def viewProducts(): # Показывает список товаров
    for product in common.csvCRUD.readTable('products.csv'):
        print("Название товара: {0}, Цена: {1}, Количество на складе: {2}"
              .format(product["productName"],product["productPrice"],product["productBalance"]))
    input("Нажмите для продолжения")
    common.cls()

def logIn(): # вход в аккаунт 
    login = input("Введите логин: ")
    password = input("Введите пароль: ")

    users = common.csvCRUD.readTable('users.csv')
    isFinded = False
    for row in users:
        if login == row["login"]:
            isFinded = True
            if password == row["password"]:
                print("Вы вошли в аккаунт")
                global isLogined
                isLogined = True
                global username
                username = login
            else:
                print("Неверный пароль")
    if (not isFinded):
        print("Пользователь не найден")
    
def logOut(): # выход из аккаунта
    global isLogined
    isLogined = False
    global username
    username = ""

def addToCart(): # добавляет товар в корзину
    print("Выберите товар")
    lines = common.csvCRUD.readTable('products.csv')
    i = 0
    for product in lines:
        i += 1
        print("{0}: Название товара: {1}, Цена: {2}, Количество на складе: {3}"
              .format(i, product["productName"], product["productPrice"],
                      product["productBalance"]))
    num = input()
    try:
        num = int(num) - 1
    except:
        print("Ошибка, ожидался ввод числа")
        num = -1
        return False
    while num > i - 1 or num < 0:
        print("Выбранного товара нету в списке")
        num = input()
        try:
            num = int(num) - 1
        except:
            print("Ошибка, ожидался ввод числа")
    product = lines[num]
    print("Вы выбрали "+ product["productName"])
    print("Сколько штук вы хотите купить?")
    count = input()
    try:
        count = int(count)
    except:
        print("Ошибка, ожидался ввод числа")
        return False
    while count < 1 or count > int(product["productBalance"]):
        if count < 1:
            print("Отрицательное количество")
            count = input()
            try:
                count = int(count)
            except:
                print("Ошибка, ожидался ввод числа")
        if count > int(product["productBalance"]):
            print("Недостаточно на складе")
            count = input()
            try:
                count = int(count)
            except:
                print("Ошибка, ожидался ввод числа")

    orders = common.csvCRUD.readTable('orders.csv')
    summ = count * int(lines[num]["productPrice"])
    # проверка на наличие записи в orders
    inCart = False
    if not orders:
        productInCart = dict()
        productInCart[0] = {"productName": lines[num]["productName"],
                            "productPrice": lines[num]["productPrice"],
                            "productBalance": count,
                            "summ": summ}
        createRecordInOrders(productInCart, summ)
        inCart = True
    else:
        for order in orders: 
            # проверка на наличие заказа у этого пользователя
            if (order["clientLogin"] == username) and (order["orderStatus"] == "inCart"):
                inCart = True
                cartDict = eval(order["orderProducts"])
                # проверка на дублирование товара в корзине, если названия одинаковые, то отправляет изменять
                for e in cartDict.values():
                    if product["productName"] == e["productName"]:
                        print("Смена количества добвленного товара проиходит через редактирование заказа (5)")
                        return False
                cartDict[len(cartDict.keys())] = {'productName': lines[num]["productName"],
                                                  'productPrice': lines[num]["productPrice"],
                                                  'productBalance': count,
                                                  'summ': summ}
                updateRecordInOrders(cartDict, order["ID"])
    if not inCart:
        productInCart = dict()
        productInCart[0] = {"productName": lines[num]["productName"],
                            "productPrice": lines[num]["productPrice"],
                            "productBalance": count,
                            "summ": summ}
        createRecordInOrders(productInCart, summ)
    print("Товар добавлен")

def createRecordInOrders(productInCart, price): # создает запись в таблице orders
    lastOrder = common.csvCRUD.readTable('orders.csv')
    if not lastOrder:
        ID = 1
    else:
        ID = int(lastOrder[len(lastOrder)-1]["ID"]) + 1

    dt_string = datetime.now()
    ordedDate = dt_string.strftime("%d/%m/%Y %H:%M:%S")
    productDict = {"ID": ID,
                   "clientLogin": username,
                   "orderDate": ordedDate,
                   "orderStatus": "inCart",
                   "orderProducts": productInCart,
                   "finalPrice": price}
    common.csvCRUD.addRow('orders.csv', ["ID","clientLogin","orderDate","orderStatus","finalPrice","orderProducts"], productDict)

def updateRecordInOrders(productInCart, ID): # обновляет строку в таблице по id
    orders = common.csvCRUD.readTable('orders.csv')
    dt_string = datetime.now()
    ordedDate = dt_string.strftime("%d/%m/%Y %H:%M:%S")
    i = 0
    for order in orders:
        if order["ID"] == ID:
            newOrder = {"ID": ID,
                        "clientLogin": order["clientLogin"],
                        "orderDate": ordedDate,
                        "orderStatus": "inCart",
                        "orderProducts": productInCart}
            num = i
        i += 1
    orders[num] = newOrder
    # пересчет цены 
    summ = 0
    for i in newOrder["orderProducts"]:
        summ += int(newOrder["orderProducts"][i]["summ"])
    newOrder["finalPrice"] = summ
    # ---
    common.csvCRUD.writeRows('orders.csv', ["ID","clientLogin","orderDate","orderStatus","finalPrice","orderProducts"], orders)

def editOrder(): # изменяет выбранный товар в корзине
    id = viewCart()
    order = common.csvCRUD.readTable('orders.csv')[int(id)-1]
    products = common.csvCRUD.readTable('products.csv')
    # проверка выбора товара
    print("Выберете товар для изменения количества или удаления")
    i = 0
    for rowInCart in eval(order["orderProducts"]):
        i += 1
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
            return False
    # ---
    orderDict = eval(order["orderProducts"])
    print('Выбран товар: {0}'.format(orderDict[num]["productName"]))
    print("Введите новое количество, введите 0 для удаления")
    for product in products:
        if orderDict[num]["productName"] == product["productName"]:
            currentProduct = product
    newCount = input()
    try:
        newCount = int(newCount)
    except:
        print("Ошибка, ожидался ввод числа")
        return False
    if newCount > int(currentProduct["productBalance"]):
        print("Значение больше доступного на складе")
        return False
    elif newCount < 0:
        print("Значение меньше 0")
        return False
    elif newCount == 0:
        del orderDict[num]
        updateRecordInOrders(orderDict, id)
        return False

    orderDict[num] = {"productName": currentProduct["productName"],
                      "productPrice": currentProduct["productPrice"],
                      "productBalance": newCount,
                      "summ": newCount * int(currentProduct["productPrice"])}
    updateRecordInOrders(orderDict, id)
    # проверка на обновление цены
    if not orderDict[num]["productPrice"] == currentProduct["productPrice"]:
        print("Цена товара изменилась")

def viewCart(): # посмотреть корзину
    orders = common.csvCRUD.readTable('orders.csv')
    for order in orders:
        if (order["clientLogin"] == username) and (order["orderStatus"] == "inCart"):
            print("Корзина: ")
            cart = eval(order["orderProducts"])
            for rowInCart in cart:
                print("{0}: Название товара: {1}, Цена: {2}, Количество в корзине: {3}, Итого: {4}"
                      .format(rowInCart+1, cart[rowInCart]["productName"], cart[rowInCart]["productPrice"],
                              cart[rowInCart]["productBalance"], cart[rowInCart]["summ"]))
            print("Итого: "+order["finalPrice"])
            print()
            return str(order["ID"])

def viewOrders(): # посмотреть старые заказы
    for order in common.csvCRUD.readTable('orders.csv'):
        if (order["clientLogin"] == username):
            cart = eval(order["orderProducts"])
            print("ID: {0}, Логин: {1}, Дата: {2}"
                  .format(order["ID"], order["clientLogin"], order["orderDate"]))
            for rowInCart in cart:
                print(" {0}: Название товара: {1}, Цена: {2}, Количество в корзине: {3}, Итого: {4}"
                        .format(rowInCart+1, cart[rowInCart]["productName"], cart[rowInCart]["productPrice"],
                                cart[rowInCart]["productBalance"], cart[rowInCart]["summ"]))
            print("Итого: "+order["finalPrice"])
            print("Статус: "+order["orderStatus"])
            print()
    input("Нажмите для продолжения")
    common.cls()

def confirmOrder(): # подтвердить заказ
    orders = common.csvCRUD.readTable('orders.csv')
    dt_string = datetime.now()
    ordedDate = dt_string.strftime("%d/%m/%Y %H:%M:%S")
    isFound = False
    priceChanged = False
    for order in orders:
        if order["clientLogin"] == username and order["orderStatus"] == "inCart":
            isFound = True
            # проверка отрицательных остатков
            controlOrder = orders[int(order["ID"])-1]
            products = common.csvCRUD.readTable('products.csv')
            controlOrderDict = eval(controlOrder["orderProducts"])
            for i in controlOrderDict:
                for product in products:
                    if not controlOrderDict[i]["productPrice"] == product["productPrice"]:
                        priceChanged = True
                    if controlOrderDict[i]["productName"] == product["productName"]:
                        if int(controlOrderDict[i]["productBalance"]) > int(product["productBalance"]):
                            print("Не хватает {0} ед. товара {1} на складе"
                                  .format(int(controlOrderDict[i]["productBalance"]) - int(product["productBalance"]),
                                          controlOrderDict[i]["productName"]))
                            return False
                        else:
                        # списание со склада
                            product["productBalance"] = int(product["productBalance"]) - int(controlOrderDict[i]["productBalance"])
            order["orderDate"] = ordedDate
            order["orderStatus"] = "paid"
            common.csvCRUD.writeRows('products.csv', ["productName", "productPrice", "productBalance"], products)
            common.csvCRUD.writeRows('orders.csv', ["ID","clientLogin","orderDate","orderStatus","finalPrice","orderProducts"], orders)
    if priceChanged:
        print("Цена товара изменилась")
    if not isFound:
        print("Корзина пуста")

def viewOrdersDetails(): # посмотреть детали заказа
    orders = common.csvCRUD.readTable('orders.csv')
    i = 0
    for order in orders:
        if order["clientLogin"] == username:
            i += 1
            cart = eval(order["orderProducts"])
            print("{0}: ".format(i))
            print("ID: {0}, Логин: {1}, Дата: {2}"
                  .format(order["ID"], order["clientLogin"], order["orderDate"]))
            for rowInCart in cart:
                print(" {0}: Название товара: {1}, Цена: {2}, Количество в корзине: {3}, Итого: {4}"
                        .format(rowInCart+1, cart[rowInCart]["productName"], cart[rowInCart]["productPrice"],
                                cart[rowInCart]["productBalance"], cart[rowInCart]["summ"]))
            print("Итого: "+order["finalPrice"])
            print("Статус: "+order["orderStatus"])
            print()
    num = input("Введите номер заказа для просмотре деталей: ")
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
    for order in orders:
        if order["clientLogin"] == username:
            if i == num:
                common.cls()
                cart = eval(order["orderProducts"])
                print("ID: {0}, Логин: {1}, Дата: {2}"
                    .format(order["ID"], order["clientLogin"], order["orderDate"]))
                for rowInCart in cart:
                    print(" {0}: Название товара: {1}, Цена: {2}, Количество в корзине: {3}, Итого: {4}"
                            .format(rowInCart+1, cart[rowInCart]["productName"], cart[rowInCart]["productPrice"],
                                    cart[rowInCart]["productBalance"], cart[rowInCart]["summ"]))
                print("Итого: "+order["finalPrice"])
                print("Статус: "+order["orderStatus"])
                print()
            i += 1
    input("Нажмите для продолжения")

while True:
    init()
