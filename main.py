import re
from web3 import Web3
from web3.middleware import geth_poa_middleware
from contract_info import abi, contract_addresses

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

contract = w3.eth.contract(address=contract_addresses, abi=abi)

users = {}

# Список слабых паролей
common_passwords = [
    "password", "123456", "123456789", "qwerty", "abc123", "password1", "111111111111", "123123123", 
    "admin", "passw0rd", "password123456789", "password123", "welcome", "qwe123456789"
]

# Проверка пароля
def is_valid_password(password):
    if len(password) < 12:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False
    if password.lower() in common_passwords:
        return False
    return True

# Регистрация пользователя
def register_user():
    try:
        while True:
            password = input("Введите пароль: ")
            if not is_valid_password(password):
                print("Пароль слишком слабый. Придумайте другой пароль.")
            else:
                break
        account = w3.geth.personal.new_account(password)
        print(f"Пользователь {account} успешно зарегистрирован!")
        fund_account(account)
    except Exception as e:
        print(f"Ошибка при регистрации пользователя: {e}")

# Вход пользователя
def login_user():
    try:
        account = input("Введите аккаунт: ")
        password = input("Введите пароль: ")
        w3.geth.personal.unlock_account(account, password)
        print("Авторизация прошла успешно!")
        user_menu(account)
    except Exception as e:
        print(f"Ошибка при авторизации: {e}")

# пополнение баланса
def fund_account(account):
    try:
        from_account = "0x97C4D2B72c940Bda62B5E93439344eE9627eB728"
        amount = w3.to_wei(100000000, 'ether')
        tx_hash = w3.eth.send_transaction({'from': from_account, 'to': account, 'value': amount})
        w3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"Аккаунт {account} пополнен на {amount} Wei")
    except Exception as e:
        print(f"Ошибка при пополнении аккаунта: {e}")

# Меню пользователя после успешной авторизации
def user_menu(account):
    while True:
        print("Выберите действие:")
        print("1. Создать недвижимость")
        print("2. Создать объявление")
        print("3. Изменить статус недвижимости")
        print("4. Изменить статус объявления")
        print("5. Купить недвижимость")
        print("6. Вывести средства")
        print("7. Получить информацию о недвижимости")
        print("8. Получить информацию об объявлениях")
        print("9. Получить информацию о балансе на смарт-контракте")
        print("10. Получить информацию о балансе на аккаунте")
        print("11. Вернуться в главное меню")
        choice = input("Введите номер действия: ")

        if choice == '1':
            create_estate(account)
        elif choice == '2':
            create_ad(account)
        elif choice == '3':
            change_estate_status(account)
        elif choice == '4':
            change_ad_status(account)
        elif choice == '5':
            buy_estate(account)
        elif choice == '6':
            withdraw_funds(account)
        elif choice == '7':
            get_estate_info()
        elif choice == '8':
            get_ad_info()
        elif choice == '9':
            get_contract_balance(account)
        elif choice == '10':
            get_account_balance(account)
        elif choice == '11':
            break
        else:
            print("Некорректный ввод. Попробуйте снова.")

# Функция для создания недвижимости
def create_estate(account):
    try:
        size = int(input("Введите размер недвижимости: "))
        address_estate = input("Введите адрес недвижимости: ")
        estate_type = input("Введите тип недвижимости (0 для House, 1 для Flat, 2 для Loft): ")
        
        tx_hash = contract.functions.createEstate(size, address_estate, int(estate_type)).transact({'from': account})
        w3.eth.wait_for_transaction_receipt(tx_hash)
        print("Недвижимость успешно создана!")
    except Exception as e:
        print(f"Ошибка при создании недвижимости: {e}")

# Функция для создания объявления
def create_ad(account):
    try:
        id_estate = int(input("Введите идентификатор недвижимости: "))
        price = int(input("Введите цену недвижимости: ")) 

        tx_hash = contract.functions.createAd(id_estate, price).transact({'from': account})
        w3.eth.wait_for_transaction_receipt(tx_hash)
        print("Объявление успешно создано!")
    except Exception as e:
        print(f"Ошибка при создании объявления: {e}")

# Функция для изменения статуса недвижимости
def change_estate_status(account):
    try:
        id_estate = int(input("Введите идентификатор недвижимости: "))
        is_active = input("Введите новый статус недвижимости(1 для актив., 0 для неактив.): ")
        is_active = bool(int(is_active))

        tx_hash = contract.functions.changeEstateStatus(id_estate, is_active).transact({'from': account})
        w3.eth.wait_for_transaction_receipt(tx_hash)
        print("Статус недвижимости успешно изменен!")
    except Exception as e:
        print(f"Ошибка при изменении статуса недвижимости: {e}")

# Функция для изменения статуса объявления
def change_ad_status(account):
    try:
        id_ad = int(input("Введите идентификатор объявления: "))
        new_status = input("Введите новый статус объявления(1 для открыт., 0 для закрыт.): ")
        new_status = int(new_status)

        tx_hash = contract.functions.changeAdStatus(id_ad, new_status).transact({'from': account})
        w3.eth.wait_for_transaction_receipt(tx_hash)
        print("Статус объявления успешно изменен!")
    except Exception as e:
        print(f"Ошибка при изменении статуса объявления: {e}")

# Функция для покупки недвижимости
def buy_estate(account):
    try:
        id_ad = int(input("Введите идентификатор объявления: "))
        ad = contract.functions.ads(id_ad).call()
        price = ad[2]

        tx_hash = contract.functions.buyEstate(id_ad).transact({'from': account, 'value': price})
        w3.eth.wait_for_transaction_receipt(tx_hash)
        print("Недвижимость успешно куплена!")
    except Exception as e:
        print(f"Ошибка при покупке недвижимости: {e}")

# Функция для вывода средств
def withdraw_funds(account):
    try:
        amount = int(input("Введите сумму для вывода (в Wei): "))
        tx_hash = contract.functions.withdraw(amount).transact({'from': account})
        w3.eth.wait_for_transaction_receipt(tx_hash)
        print("Средства успешно выведены!")
    except Exception as e:
        print(f"Ошибка при выводе средств: {e}")

# Функция для получения информации о недвижимости
def get_estate_info():
    try:
        estates = contract.functions.getEstates().call()
        for estate in estates:
            print(f"ID: {estate[5]}, Адрес: {estate[1]}, Размер: {estate[0]}, Владелец: {estate[2]}, Тип: {estate[3]}, Активен: {estate[4]}")
    except Exception as e:
        print(f"Ошибка при получении информации о недвижимости: {e}")

# Функция для получения информации об объявлениях
def get_ad_info():
    try:
        ads = contract.functions.getAds().call()
        for ad in ads:
            print(f"ID: {ad[0]}, Владелец: {ad[1]}, Покупатель: {ad[2]}, Цена: {ad[3]}, ID недвижимости: {ad[4]}, Статус: {ad[5]}")
    except Exception as e:
        print(f"Ошибка при получении информации об объявлениях: {e}")

# Функция для полочения информации о балансе на смарт-контракте
def get_contract_balance(account):
    try:
        balance = contract.functions.getBalance().call({'from': account})
        print(f"Баланс на смарт-контракте: {balance} Wei")
    except Exception as e:
        print(f"Ошибка при получении баланса смарт-контракта: {e}")

# Функция для получения информации о балансе на аккаунте
def get_account_balance(account):
    try:
        balance = w3.eth.get_balance(account)
        print(f"Баланс на аккаунте: {balance} Wei")
    except Exception as e:
        print(f"Ошибка при получении баланса аккаунта: {e}")

# Меню для входа/регистрации
def main_menu():
    while True:
        print("Выберите действие:")
        print("1. Регистрация")
        print("2. Вход")
        print("3. Выход")

        choice = input("Введите номер действия: ")

        if choice == '1':
            register_user()
        elif choice == '2':
            login_user()
        elif choice == '3':
            print("Выход из программы.")
            break
        else:
            print("Некорректный ввод. Попробуйте снова.")

# Запуск меню
main_menu()