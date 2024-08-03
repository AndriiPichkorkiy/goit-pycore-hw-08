from colorama import Fore, Style
from addressBook import AddressBook, Record
from addressBook import PhoneValidationError
from datetime import datetime
import pickle


def save_data(book: AddressBook, filename: str = "addressbook.pkl") -> None:
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename: str = "addressbook.pkl") -> AddressBook:
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # Return a new address book if the file is not found


# decorator
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me a name and a phone please."
        except IndexError:
            return "Give me a name please."
        except KeyError:
            return "Contact is not exist"
        except PhoneValidationError as error:
            return "Error while saving phone: " + str(error)

    return inner


def parse_input(user_input: str) -> list[str]:
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args: list[str], book: AddressBook) -> str:
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."

    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)

    return message


@input_error
def change_contact(args: list[str], book: AddressBook) -> str:
    name, phone, new_phone, *_ = args
    record = book.find(name)

    record.edit_phone(phone, new_phone)

    return "Contact changed."


@input_error
def show_phone(args: list[str], book: AddressBook) -> list:
    name, *_ = args
    record = book.find(name)
    if not record:
        raise KeyError

    return f"phones: {'; '.join(p.value for p in record.phones)}"


def show_all(book: AddressBook) -> None:
    if len(book.items()):
        for record in book.items():
            print_bot_answer(record)
    else:
        print_bot_answer("No contacts was added")


@ input_error
def add_birthday(args: list[str], book: AddressBook) -> str:
    name, birthday, *_ = args
    record = book.find(name)
    if not record:
        raise KeyError

    record.add_birthday(birthday)
    return "Birthday was added"


@ input_error
def show_birthday(args: list[str], book: AddressBook) -> datetime:
    name = args[0]
    record = book.find(name)
    return record.birthday


@ input_error
def birthdays(book: AddressBook) -> list[dict[str, str]]:
    return book.get_upcoming_birthdays()


# colorized command
def print_bot_answer(answer) -> None:
    print(Fore.GREEN, answer, Style.RESET_ALL)


# colorized command
def print_bot_invalid_command(answer: str) -> None:
    print(Fore.RED, answer, Style.RESET_ALL)


def main():
    book = load_data()
    print_bot_answer("Welcome to the assistant bot!")
    while True:
        try:
            print(Style.RESET_ALL + Fore.CYAN + "Enter a command: ", end='')
            user_input = input(Style.RESET_ALL + Fore.YELLOW)

            command, *args = parse_input(user_input)

            if command in ["close", "exit"]:
                save_data(book)
                print_bot_answer("Good bye!")
                break

            elif command == "hello":
                print_bot_answer("How can I help you?")

            elif command == "add":
                print_bot_answer(add_contact(args, book))

            elif command == "change":
                print_bot_answer(change_contact(args, book))

            elif command == "phone":
                print_bot_answer(show_phone(args, book))

            elif command == "all":
                show_all(book)

            elif command == "add-birthday":
                print_bot_answer(add_birthday(args, book))

            elif command == "show-birthday":
                print_bot_answer(show_birthday(args, book))

            elif command == "birthdays":
                print_bot_answer(birthdays(book))

            else:
                print_bot_invalid_command("Invalid command.")
        except BaseException:
            print_bot_invalid_command("\nInvalid command.")


if __name__ == "__main__":
    main()
