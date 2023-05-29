import sys
import csv
from optparse import OptionParser
import pyperclip

import settings


def load_people(filename="people.csv"):
    parsed_people = {}
    with open(filename) as r:
        people = csv.reader(r)
        for person in people:
            if person:  # Ignorar linhas vazias
                if len(person) >= 3:
                    nick = person[0]
                    name = person[1] if person[1] else person[0].title()
                    desc = person[2]
                    parsed_people[nick] = [name, desc]
                else:
                    print(f"Invalid person data: {person}")
    return parsed_people


def save_people(people, filename="people.csv"):
    with open(filename, 'w', newline='') as csvfile:
        w = csv.writer(csvfile)
        for nick, values in people.items():
            w.writerow([nick, values[0], values[1]])


def add_person(nick, desc, name=None, filename="people.csv"):
    people = load_people(filename)
    people[nick] = [name, desc]
    save_people(people, filename)


def update_person(nick, desc, name=None, filename="people.csv"):
    people = load_people(filename)
    if nick in people:
        people[nick] = [name, desc]
        save_people(people, filename)
        print(f"Person '{nick}' updated successfully.")
    else:
        print(f"Person '{nick}' not found.")


def delete_person(nick, filename="people.csv"):
    people = load_people(filename)
    if nick in people:
        del people[nick]
        save_people(people, filename)
        print(f"Person '{nick}' deleted successfully.")
    else:
        print(f"Person '{nick}' not found.")


def write_introduction(people, message):
    i = " & ".join([v[0] for n, v in people.items()]) + ", please meet.\n\n"
    i += "\n\n".join([v[1] for n, v in people.items()])
    if message:
        i += "\n\n" + message
    else:
        i += "\n\n" + settings.closing
    i += "\n\n" + settings.valediction + ",\n\n" + settings.name
    return i


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-a", "--add", dest="add", action="store_true")
    parser.add_option("-u", "--update", dest="update", action="store_true")
    parser.add_option("-d", "--delete", dest="delete", action="store_true")
    parser.add_option("-m", "--message", dest="message", default=False, action="store")
    (options, args) = parser.parse_args()

    if options.add:  # Adicionar nova pessoa
        if len(args) == 2:
            add_person(args[0], args[1])
        else:
            add_person(args[0], args[2], args[1])

    elif options.update:  # Atualizar pessoa existente
        if len(args) == 2:
            update_person(args[0], args[1])
        else:
            update_person(args[0], args[2], args[1])

    elif options.delete:  # Deletar pessoa
        if len(args) == 1:
            delete_person(args[0])
        else:
            print("Invalid arguments. Please provide the nickname of the person to delete.")

    else:  # Escrever a introdução
        try:
            people = load_people()
        except FileNotFoundError:
            print("No people!")
            sys.exit()

        introducing = {}  # Obter os dados das pessoas informadas
        for person in args:
            try:
                introducing[person] = people[person]
            except KeyError as e:
                print("Missing person %s in your data!" % e)
                sys.exit()

        msg = write_introduction(introducing, options.message)
        print(msg)
        pyperclip.copy(msg)
        print("Message copied to clipboard.")
