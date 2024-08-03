from collections import UserDict
from datetime import datetime, timedelta


class PhoneValidationError(Exception):
    def __init__(self, message):
        super().__init__(message)


# Base class for record fields
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


# A class for storing a contact name. Mandatory field.
class Name(Field):
    def __init__(self, value):
        super().__init__(value)


# A class for storing a phone number. Has format validation (10 digits).
class Phone(Field):
    def __init__(self, value: str):
        if len(value) == 10 and all([symbol.isdigit for symbol in value]):
            super().__init__(value)
        else:
            raise PhoneValidationError("Valid phone length is 10")


class Birthday(Field):
    def __init__(self, value):
        try:
            birthday = datetime.strptime(value, "%d-%m-%Y").date()
            super().__init__(birthday)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


# A class for storing information about a contact, including name and phone list.
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday}"

    def __repr__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday}"

    def add_phone(self, phone):
        # validation dublication phones
        if self.find_phone(phone):
            return

        new_phone = Phone(phone)
        self.phones.append(new_phone)

    def find_phone(self, phone_to_find):
        for phone in self.phones:
            if phone.value == phone_to_find:
                return phone

    # privat method
    def _find_phone_index(self, phone_to_find):
        for i, phone in enumerate(self.phones):
            if phone.value == phone_to_find:
                return i

    def remove_phone(self, phone):
        phone_to_delete = self.find_phone(phone)
        self.phones.remove(phone_to_delete)

    def edit_phone(self, phone, new_phone):
        index = self._find_phone_index(phone)
        self.phones[index] = Phone(new_phone)

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)


# A class for storing and managing records.
class AddressBook(UserDict):
    def add_record(self, record) -> None:
        self.data[record.name.value] = record

    def find(self, name) -> Record:
        return self.data.get(name)

    def delete(self, name) -> None:
        del self.data[name]

    def get_upcoming_birthdays(self) -> list[dict[str, str]]:
        # pattern is used convert user birthday to date
        birthday_pattern = "%Y.%m.%d"

        # list for mathed birthdays to return
        res = []

        # get today's dau
        today = datetime.today().date()

        # next line for test only. Uncomment the line to test birthdays with next year
        # today = today.replace(month=12, day=31)

        # find users with nearest birthday
        for username in self.data:
            # get user's birthday as class date
            user = self.data[username]

            birthday = user.birthday.value
            # birthday = datetime.strptime(user["birthday"], birthday_pattern).date()

            # set currnet year to compare the dates
            birthday_this_year = birthday.replace(year=today.year)

            # if next birthday in next year, add 1 year
            if birthday_this_year < today:
                birthday_this_year = birthday.replace(year=today.year + 1)

            #  get difference between today and next birhday years
            next_birthday_in_days = (birthday_this_year - today).days

            #  find and add to result only birthdays in next 7 days
            if (next_birthday_in_days < 7):
                weekday = birthday_this_year.weekday()

                # if the birthday falls on a weekend, the date of the greeting is moved to the following Monday.
                if (weekday == 5 or weekday == 6):
                    birthday_this_year += timedelta(days=7 - weekday)

                res.append({"name": user.name.value, "congratulation_date": birthday_this_year.strftime(
                    birthday_pattern)})

        return res


# testing:
def main():
    # Creating a new address book
    book = AddressBook()

    # Create record for John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    john_record.add_birthday("29-07-1992")

    # Adding John to the address book
    book.add_record(john_record)

    # Create and add a new record for Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Output of all entries in the book
    for name, record in book.data.items():
        print(record)

    # Find and edit phone for John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Output: Contact name: John, phones: 1112223333; 5555555555

    # Search for a specific phone in the John record
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Deleting Jane's record
    book.delete("Jane")


if __name__ == "__main__":
    main()
