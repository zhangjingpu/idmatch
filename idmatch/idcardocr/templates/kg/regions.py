# coding: utf-8
from idcardocr.core.regions.mapping import IDcardSanitizer
from idcardocr.core.regions.sanitizer import Sanitizer


class IDcard(IDcardSanitizer, Sanitizer):
    serial = ""
    firstname = ""
    surname = ""
    middlename = ""
    nationality = ""
    birthday = ""
    inn = ""
    gender = ""
    errors = []

    def __init__(self, blocks):
        self.blocks = self.blocks_normalize(blocks)

    def find_serial(self):
        self.serial = self.find_common(0.07, 0.85)
        self.sanitize_serial()
        return self.serial

    def find_surname(self):
        self.surname = self.find_common(0.325, 0.268)
        self.sanitize_surname()
        return self.surname

    def find_firstname(self):
        self.firstname = self.find_common(0.325, 0.4)
        self.sanitize_firstname()
        return self.firstname

    def find_middlename(self):
        self.middlename = self.find_common(0.325, 0.536)
        self.sanitize_middlename()
        return self.middlename

    def find_birthday(self):
        block = None
        distance = 1e10
        for block in self.blocks:
            distance_x = abs(0.325 - block['x'])
            distance_y = abs(0.65 - block['y'])
            if distance_x + distance_y > distance:
                continue
            distance = distance_x + distance_y
            result = block

        if not result:
            self.errors.append("601: Birthday element not found")
            return

        parts = []
        for block in self.blocks:
            distance_gender = abs(0.71 - block['x'])
            distance_y = abs(0.65 - block['y'])

            if 0.03 > distance_y and 0.1 < distance_gender and block['x'] - result['x'] >= 0.0:
                parts.append(block)

        if not parts:
            self.errors.append("602: Required birthday regions not found")
            return
        # parts_sorted = sort(parts,  key=lambda b: b['x'],  reverse=True)
        self.birthday = "".join([part['text'] for part in parts])
        self.birthday = self.sanitizer_remove_whitespaces(self.birthday)
        return self.birthday

    def find_nationality(self):
        self.nationality = self.find_common(0.325, 0.88)
        return self.nationality

    def find_inn(self):
        self.inn = self.find_common(0.82, 0.94)
        return self.inn

    def find_gender(self):
        self.gender = self.find_common(0.71, 0.65)
        return self.gender

    def data(self):
        data = {
            'surname': blocks.find_surname(),
            'middlename': blocks.find_middlename(),
            'firstname': blocks.find_firstname(),
            'birthday': blocks.find_birthday(),
            'serial': blocks.find_serial(),
            'gender': blocks.find_gender(),
            'inn': blocks.find_inn(),
            'nationality': blocks.find_nationality(),
            'errors': ", ".join(blocks.errors)
        }
        return {k: value.decode('utf-8') for k, value in data.iteritems()}
