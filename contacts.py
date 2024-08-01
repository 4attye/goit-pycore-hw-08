from collections import UserDict
from datetime import datetime, date, timedelta

class Field:

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):

    def __init__(self, value):
        if not value:
            raise ValueError("Name can not be empty")
        super().__init__(value)

class Phone(Field):

    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be 10 digits")
        super().__init__(value)


class Birthday(Field):

    def __init__(self, value):

        try:
            date_value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(date_value)

class Record:

    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):

        self.phones.append(Phone(phone))

    def remove_phone(self, phone):

        self.phones = [p for p in self.phones if p.value != phone]

    def find_phone(self, phone):

        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def edit_phone(self, old_phone, new_phone):

        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return
        raise ValueError("Phone number not found")

    def add_birthday(self, birthday):

        self.birthday = Birthday(birthday)

    def __str__(self):

        phones = "; ".join(p.value for p in self.phones)
        birthday = self.birthday.value.strftime("%d.%m.%Y") if self.birthday else "None"

        return f"Contact name: {self.name.value}, phones: {phones}, birthday: {birthday}"



class AddressBook(UserDict):

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):

        return self.data.get(name, None)

    def delete(self, name):

        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self, days=7):

        today = date.today()
        upcoming_birthdays = []

        for record in self.data.values():

            if record.birthday:
                birthday_this_year = record.birthday.value.replace(year= today.year)
                days_until_birthday = (birthday_this_year - today).days

                if days_until_birthday < 0:
                    birthday_this_year = record.birthday.value.replace(year=today.year + 1)
                    days_until_birthday = (birthday_this_year - today).days

                if 0 <= days_until_birthday <= days:
                    congratulation_date = birthday_this_year

                    if congratulation_date.weekday() in (5, 6):
                        congratulation_date += timedelta(days=(7 - congratulation_date.weekday()))
                    upcoming_birthdays.append({"name": record.name.value, "birthday": congratulation_date})

        return upcoming_birthdays

    def __str__(self):
        return '\n'.join(str(record) for record in self.data.values())

