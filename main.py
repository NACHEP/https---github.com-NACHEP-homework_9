'''
Напишіть консольного бота помічника, який розпізнаватиме команди, що вводяться з клавіатури, 
і відповідати відповідно до введеної команди.

Бот помічник повинен стати для нас прототипом додатка-асистента. 
Додаток-асистент в першому наближенні повинен уміти працювати з книгою контактів і календарем.
У цій домашній роботі зосередимося на інтерфейсі самого бота. 
Найбільш простий і зручний на початковому етапі розробки інтерфейс - 
це консольний додаток CLI (Command Line Interface). CLI досить просто реалізувати. 
Будь-який CLI складається з трьох основних елементів:


На першому етапі наш бот-асистент повинен вміти зберігати ім'я та номер телефону, 
знаходити номер телефону за ім'ям, змінювати записаний номер телефону, 
виводити в консоль всі записи, які зберіг. 
Щоб реалізувати таку нескладну логіку, скористаємося словником. 
У словнику будемо зберігати ім'я користувача як ключ і номер телефону як значення.

Умови

Бот не чутливий до регістру введених команд.


Логіка команд реалізована в окремих функціях і ці функції приймають на вхід один або декілька рядків 
та повертають рядок.

'''

#Всі помилки введення користувача повинні оброблятися за допомогою декоратора input_error.
def input_error(funk):
    def inner(*args, **kwargs):
        try:
            result = funk(*args, **kwargs)
            return result
        except KeyError:
            return "Key does not exist in the dictionary."
        except ValueError:
            return "This is not a valid number. Give me name and phone, please."
        except IndexError:
            return "Enter user name."
    return inner

users = {}

#"hello", відповідає у консоль "How can I help you?"
@input_error
def hello():
    return "How can I help you?"

#"add ...". За цією командою бот зберігає у пам'яті (у словнику наприклад) новий контакт.
# Замість ... користувач вводить ім'я та номер телефону, обов'язково через пробіл.
@input_error
def add(name, phone):
    users[name] = phone
    return f"User {name} with phone number {phone} added to users."

#"change ..." За цією командою бот зберігає в пам'яті новий номер телефону існуючого контакту.
# Замість ... користувач вводить ім'я та номер телефону, обов'язково через пробіл.
@input_error
def change(name, phone):
    if name in users:
        users[name] = phone
        return f"{name}'s phone number is changed to {phone}."
    
#"phone ...." За цією командою бот виводить у консоль номер телефону для зазначеного контакту. 
# Замість ... користувач вводить ім'я контакту, чий номер треба показати.
@input_error
def phone_number(name):
    if name in users:
        return f"{name}'s phone number is: {users[name]}."
    
#"show all". За цією командою бот виводить всі збереженні контакти з номерами телефонів у консоль.
def show_all():
    if not users:
        return {}
    else:
        return users
#"good bye", "close", "exit" по будь-якій з цих команд бот завершує свою роботу після того, як виведе у консоль "Good bye!".
def exit_commands():
    return "Good bye!"

#Функції обробники команд — набір функцій, які ще називають handler, 
# вони відповідають за безпосереднє виконання команд.
def handler(command, params):
    command = command.lower()
    if command == 'hello':
        return hello
    elif command == 'add':
        return add, params
    elif command == 'change':
        return change, params
    elif command == 'phone':
        return phone_number, params
    elif command == 'show':
        return show_all
    elif command in 'good bye' or 'close' or 'exit':
        return exit_commands


#Парсер команд. Частина, яка відповідає за розбір введених користувачем рядків, 
# виділення з рядка ключових слів та модифікаторів команд.
def parser(users_input):
    commands = users_input.split()
    if commands:
        command = commands[0]
        params = commands[1:]
        return handler(command, params)
    
#Цикл запит-відповідь. Ця частина програми відповідає за отримання від користувача даних 
# та повернення користувачеві відповіді від функції-handlerа.
#Вся логіка взаємодії з користувачем реалізована у функції main, 
# всі print та input відбуваються тільки там.
def main():
    while True:
        users_input = input("...: ")
        command_handler = parser(users_input)
        if command_handler == exit_commands:
            print(command_handler())
            break
        elif command_handler is not None:
            if isinstance(command_handler, tuple):
                func, params = command_handler
                result = func(*params)
            else:
                result = command_handler()
            print(result)
        
if __name__ == "__main__":
    main()

