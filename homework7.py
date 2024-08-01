from contacts import AddressBook, Record
import pickle


def parse_input(user_input):

    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args


def input_error(func):

    def inner(*args, **kwargs):

        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return e
        except KeyError:
            return "Contact not found."
        except IndexError :
            return "Enter user name."

    return inner


@input_error
def add_contact(args, book):

    name, phone, *_ = args
    record = book.find(name)
    message = "Phone number added."

    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."

    if phone:
        record.add_phone(phone)
    return  message


@input_error
def change_contact(args, book):

    name,old_phone, phone = args

    if name in book:
        contact = book.find(name)
        contact.edit_phone(old_phone,phone)
        return "Contact updated."


@input_error
def show_phone(args, book):

    name = args[0]
    record = book.find(name)

    if record:
        return "; ".join(phone.value for phone in record.phones)
    else:
        raise KeyError


@input_error
def show_all(book):
    return book

@input_error
def add_birthday(args, book):

    name, birthday = args
    record = book.find(name)

    if record:
        record.add_birthday(birthday)
        return "Birthday added."
    else:
        raise KeyError

@input_error
def show_birthday(args, book):

    name = args[0]
    record = book.find(name)

    if record and record.birthday:
        return record.birthday.value.strftime("%d.%m.%Y")
    else:
        return "Birthday not found."

@input_error
def birthdays(book):

    upcoming_birthdays = book.get_upcoming_birthdays()

    if upcoming_birthdays:
        return "\n".join(f"{item["name"]}: {item["birthday"]}" for item in upcoming_birthdays)
    return "No birthdays."

@input_error
def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as file:
        pickle.dump(book, file)

@input_error
def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        return AddressBook()

def main():

    book = load_data()
    print("Welcome to the assistant bot!")

    while True:

        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        match command:
            case "close":
                save_data(book)
                print("Good bye!")
                break
            case "exit":
                save_data(book)
                print("Good bye!")
                break
            case "hello":
                print("How can I help you?")
            case "add":
                print(add_contact(args, book))
            case "change":
                print(change_contact(args, book))
            case "phone":
                print(show_phone(args, book))
            case "all":
                print(show_all(book))
            case "add-birthday":
                print(add_birthday(args, book))
            case "show-birthday":
                print(show_birthday(args, book))
            case "birthdays":
                print(birthdays(book))
            case _:
                print("Invalid command.")


if __name__ == "__main__":
    main()