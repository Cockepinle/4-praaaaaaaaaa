from web3 import Web3
from web3.middleware import geth_poa_middleware
from contract_info import address_contract, abi

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
contract = w3.eth.contract(address=address_contract, abi=abi)
print(contract.address)
print(w3.eth.get_balance('0x64ffC6C1Eb030D680e43555a521a710d7258491a'))

def register():
    while True:
        password = input("Введите пароль: ")
        if len(password) < 12:
            print("Пароль должен быть не менее 12 символов")
            continue
        
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c for c in password if c in "!@#$%^&*()_-+=<>?,./")
        
        if not has_upper:
            print("Пароль должен содержать как минимум одну заглавную букву")
            continue
        if not has_lower:
            print("Пароль должен содержать как минимум одну строчную букву")
            continue
        if not has_digit:
            print("Пароль должен содержать как минимум одну цифру")
            continue
        if not has_special:
            print("Пароль должен содержать специальные символы, такие как !, @, #, $, % и т.д.")
            continue
        
        if "password" in password.lower() or "qwerty" in password.lower():
            print("Избегайте простых шаблонов в пароле, например 'password123' или 'qwerty123'")
            continue
        
        account = w3.geth.personal.new_account(password)
        print(f"Ваш публичный ключ: {account}")
        return "Успешно зарегистрировано"


def login():
    public_key = input("Введите ваш публичный ключ: ")
    password = input("Введите пароль: ")
    try:
        w3.geth.personal.unlock_account(public_key, password)
        print("Авторизация прошла успешно!")
        return public_key
    except Exception as e:
        print("Ошибка авторизации: {e}")
        return None

def create_real_estate(account):
    try:
        size = int(input("Введите размер недвижимости: "))
        address = str(input("Введите адрес недвижимости: "))
        type = int(input("Введите тип недвижимости (0 для House, 1 для Flat, 2 для Loft): "))
        tx_hash = contract.functions.createEstate(size, address, type).transact({
            'from': account
        })
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        if receipt.status == 1:
            print("Недвижимость создана успешно")
            return True
        else:
            print("Не удалось создать недвижимость")
            return False
    except Exception as e:
        print(f"Ошибка создания недвижимости: {e}")

def create_real_ad(account):
    try:
        idEstate = int(input("Введите id недвижимости: "))
        owner = input("Введите адрес владельца недвижимости: ")
        price = int(input("Введите цену на недвижимость: "))
        tx_hash = contract.functions.createAd(idEstate, owner, price).transact({
            'from': account
        })
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        if receipt.status == 1:
            print("Объявление создано успешно")
            return True
        else:
            print("Не удалось создать объявление")
            return False
    except Exception as e:
        print(f"Ошибка при создании объявления: {e}")

def change_est_status(account):
    try:
        idEstate = int(input("Введите id недвижимости: "))
        tx_hash = contract.functions.createStatusEstate(idEstate).transact({
                'from': account
        })
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        if receipt.status == 1:
            print("Статус недвижимости был изменен успешно")
            return True
        else:
            print("Не удалось изменить статус недвижимости")
            return False
    except Exception as e:
        print(f"Ошибка при изменении статуса недвижимости: {e}")

def change_ad_status(account):
    try:
        idEstate = int(input("Введите id объявления: "))
        tx_hash = contract.functions.createStatusAd(idEstate).transact({
                'from': account
        })
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        if receipt.status == 1:
            print("Статус объявления был изменен успешно")
            return True
        else:
            print("Не удалось изменить статус объявления")
            return False
    except Exception as e:
        print(f"Ошибка при изменении статуса объявления: {e}")

def buy_est(account):
    try:
        idAd = int(input("Введите id объявления: "))
        tx_hash = contract.functions.buyEstate(idAd).transact({
                'from': account
        })
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        if receipt.status == 1:
            print("Покупка была проделана успешно")
            return True
        else:
            print("Не удалось совершить покупку недвижимости")
            return False
    except Exception as e:
        print(f"Ошибка при осуществлении покупки недвижимости: {e}")

def vivod_money(account):
    try:
        amount_to_transfer = int(input("Сколько enter вы хотите перевести Wei: "))
        tx_hash = contract.functions.sendMoney().transact({
            'from': account,
            'value': amount_to_transfer
        })
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        if receipt.status == 1:
            print("Перевод денежки был проделан успешно")
            return True
        else:
            print("Денежка не переведена")
            return False
    except Exception as e:
        print(f"Ошибка в переводе денежки: {e}")

def inf_est(account):
    try:
        estates = contract.functions.getEstate().call({
            'from': account
        })
        if len(estates) > 0:
            for i, estate in enumerate(estates, start=0):
                print(f"{i} недвижимость: {estate}")
    except Exception as e:
        print(f"Ошибка получения доступных недвижимостей: {e}")

def inf_ad(account):
    try:
        estates = contract.functions.getAds().call({
            'from': account
        })
        if len(estates) > 0:
            for i, estate in enumerate(estates, start=0):
                print(f"{i} объявления: {estate}")
    except Exception as e:
        print(f"Ошибка получения доступных объявлений: {e}")

def get_balance(account):
    try:
        user_address = input()
        balance = contract.functions.getBalance(user_address).call({
            'from': account
        })
        print(f"Баланс на аккаунте для адреса {user_address}: {balance}")
    except Exception as e:
        print(f"Ошибка получения баланса: {e}")

def get_contract_balance():
    try:
        contract_balance = w3.eth.get_balance(contract.address)
        print (f"Баланс на смарт-контракте: {contract_balance}")
    except Exception as e:
        print(f"Ошибка при получении баланса смарт-контракта: {e}")
        return None
    
def main():
    account = ""
    while True:
        if account =="" or account == None:
            choice = int(input("Долбро пожаловать в систему! Выберите: 1. Регистрация 2. Авторизация 3. Выйти \n"))
            match choice:
                case 1:
                    register()
                case 2:
                    account = login()
                case 3:
                    exit(0)
                case _:
                    print("Выберите 1 или 2!")
        else:
            choice = int(input("Выберите: \n1. Создать недвижимость \n2. Создать объявление \n3. Изменить статус недвижимости \n4. Изменить статус объявления \n5. Купить недвижимость \n6. Пополнить счет \n7. Получить информацию о доступных недвижимостях \n8. Получить информацию о доступных объявлениях \n9. Получить информацию о балансе аккаунта \n10. Получить информацию о балансе смарт-контракта \n11. Выйти \n"))
            match choice:
                case 1:
                    create_real_estate(account)
                case 2:
                    create_real_ad(account)
                case 3:
                    change_est_status(account)
                case 4:
                    change_ad_status(account)
                case 5:
                    buy_est(account)
                case 6:
                    vivod_money(account)
                case 7:
                    inf_est(account)
                case 8:
                    inf_ad(account)
                case 9:
                    get_balance(account)
                case 10:
                    get_contract_balance()
                case 11:
                    account = ""
                case _:
                    print("Выберите от 1 до 11")

if __name__ == "__main__":
    main()
