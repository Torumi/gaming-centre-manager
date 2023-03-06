'''
TODO [X] Realize VIP clients
    if total hours >= 50, client is VIP and gets 10% discount for next visits
'''


import json
import datetime
import sys

try:
    with open('journal.json', 'r') as file:
        journal = json.load(file)
except (json.decoder.JSONDecodeError, FileNotFoundError):
    journal = {}


def print_clients() -> None:
    print('\n')
    for key in journal:
        client = journal.get(key)
        print(f"{client.get('name')}({client.get('phone_number')}, {client.get('city')}) - {key}")


def add_client(name: str, phone_number: str, city: str) -> int:

    """
    Adds a client to journal
    :param name: Name of client to add to journal
    :param phone_number: Phone number of client to add to journal
    :param city: City of client to add to journal
    :return: ID of client added to journal
    """

    keys = [int(key) for key in journal]
    try:
        client_id = max(keys)
    except ValueError:  # if keys is an empty sequence (no clients in journal), first client's id is 0
        client_id = 0
    else:
        client_id += 1
    journal[client_id] = {
        "name": name,
        "phone_number": phone_number,
        "city": city,
        "vip_status": False,
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
            "price": (5 if hours <= 1 else 10) * (0.9 if journal.get(client_id).get("vip_status") else 1)
        }
    )


def print_info(client_id: str):
    client = journal[client_id]
    total_hours = sum([visit['hours'] for visit in client['visits']])
    total_price = sum([visit['price'] for visit in client['visits']])
    if not client:
        raise KeyError
    print(f'\nAPMEKLĒTĀJS:\n'
          f"{client.get('name')} ({client.get('phone_number')}, {client.get('city')})\n"
          f"VIP stastuss: {client.get('vip_status', False)}\n"
          f"Apmeklētas stundas: {total_hours}\n"
          f"Apmeklējumu daudzums: {len(client.get('visits'))}\n"
          f"Apmaksāts: {total_price}\n"
          )


def modify_vip(client_id: str):
    '''
    Modifies VIP status if client have 50+ total hours and prints info about VIP status
    :param client_id: ID of client
    :return: None
    '''
    client = journal[client_id]
    total_hours = sum([visit['hours'] for visit in client['visits']])
    if total_hours >= 50:
        print(f"{client.get('name')}({client.get('phone_number')}, {client.get('city')}) is VIP")
    else:
        print(f"{client.get('name')}({client.get('phone_number')}, {client.get('city')}) is not VIP")
    journal[client_id]["vip_status"] = (total_hours >= 50)

def add_visit_handler():
    print_clients()
    print("New client - N")

    while True:
        response = input('>>> ').lower()
        if response == 'n':
            # Add new client
            name = input("Name: ")
            phone_number = input("Phone number: ")
            city = input("City: ")
            client_id = add_client(name, phone_number, city)
            break
        else:  # if response is not 'n'
            try:  # check response validity
                journal[response]
            except KeyError:
                print('Invalid response')
            else:
                client_id = response
                break

    while True:
        try:
            hours = int(input("Hours: "))
        except ValueError:
            print("Not an integer")
        else:
            break
    while True:
        try:
            num_of_children = int(input("Number of children: "))
        except ValueError:
            print("Not an integer")
        else:
            break
    add_visit(client_id, hours, num_of_children)
    modify_vip(client_id)


def print_info_handler():
    if len(journal) == 0:
        print("No clients in journal")
        return

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
