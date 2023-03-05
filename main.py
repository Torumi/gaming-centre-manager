import json
import datetime
import sys

with open('journal.json', 'r') as file:
    try:
        journal = json.load(file)
    except json.decoder.JSONDecodeError:
        journal = {}


def print_clients() -> None:
    print('\n')
    for key in journal:
        client = journal.get(key)
        print(f"{client.get('name')}({client.get('phone_number')}, {client.get('city')}) - {key}")


def add_client(name: str, phone_number: str, city: str) -> int:
    keys = [int(key) for key in journal]
    try:
        client_id = max(keys)
    except ValueError:
        client_id = 0
    else:
        client_id += 1
    journal[client_id] = {
        "name": name,
        "phone_number": phone_number,
        "city": city,
        "visits": []
    }
    print(f'Added client: {name}({phone_number}, {city})')
    return client_id


def add_visit(client_id: int, hours: int, num_of_children: int):
    journal.get(client_id).get('visits').append(
        {
            "date": datetime.datetime.today().strftime('%d-%m-%Y'),
            "hours": hours,
            "num_of_children": num_of_children,
            "price": 5 if hours <= 1 else 10
        }
    )


def is_in_journal(name: str, phone_number: str, city: str):
    for key in journal:
        client = journal[key]
        if all((client.get('name') == name, client.get('phone_number') == phone_number, client.get('city') == city)):
            return key


def print_info(client_id: str):
    client = journal.get(client_id)
    total_hours = sum([visit['hours'] for visit in client['visits']])
    total_price = sum([visit['price'] for visit in client['visits']])
    if not client:
        raise KeyError
    print(f'\nAPMEKLĒTĀJS:\n'
          f"{client.get('name')} ({client.get('phone_number')}, {client.get('city')})\n"
          f"Apmeklētas stundas: {total_hours}\n"
          f"Apmeklējumu daudzums: {len(client.get('visits'))}\n"
          f"Apmaksāts: {total_price}\n"
          )


def add_visit_handler():
    print_clients()
    print("New client - N")

    while True:
        respone = input('>>> ').lower()
        if respone == 'n':
            name = input("Name: ")
            phone_number = input("Phone number: ")
            city = input("City: ")
            client_id = add_client(name, phone_number, city)
            break
        else:
            try:
                journal[respone]
            except KeyError:
                print('Invalid response')
            else:
                client_id = respone
                break
    hours = int(input("Hours: "))
    num_of_children = int(input("Number of children: "))
    add_visit(client_id, hours, num_of_children)


def print_info_handler():
    print_clients()
    while True:
        client_id = input('Client ID: ')
        try:
            print_info(client_id)
        except KeyError:
            print("Invalid ID")
        else:
            break


def main():
    while True:
        response = input("Add visit - A\n"
                         "Print info about client - I\n"
                         "Exit - E\n").lower()
        activities = {
            'a': add_visit_handler,
            'i': print_info_handler,
            'e': lambda: sys.exit()
        }
        activities.get(response, lambda: print('Invalid response'))()

        with open('journal.json', 'w') as outfile:
            json.dump(journal, outfile, indent=4)
        print('\n' + '*' * 30 + '\n')


if __name__ == '__main__':
    main()
