def mainMenu(mention, role, date):
    text = f'Привет, {mention}\n' \
           f'{f"{role}" if role.name != "client" else ""}\n' \
           f'Дата регистрации: {date}'
    return text

def start():
    text = 'Добро пожаловать в каталог магазина SecondRoomShop'
    return text