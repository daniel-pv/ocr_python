import random
import src.common.constants as constant
from providers.providerAdapter import ProviderAdapter


class OCR:
    def __init__(self, provider: ProviderAdapter):
        self.provider = provider
        self.folder_path = ''

    def ocr_file(self, file_path: str, file_name: str):
        result = []
        self.provider.folder_path = self.folder_path
        file_data = self.provider.read(file_name)
        from_line = 0
        to_line = 4
        entry = ''
        entry_result = ''
        while to_line <= len(file_data):
            new_list = file_data[from_line+1:to_line]
            entry = '\n'.join([str(item) for item in new_list])
            from_line += 4
            to_line += 4
            entry_result = self.ocr_entry(entry)
            str_entry_result = ''
            if len(entry_result) > 1:
                firts_entry = self.get_entry_numbers(entry)
                str_entry_result = '{} AMB {}'.format(
                    firts_entry,
                    entry_result)
            else:
                str_entry_result = str(entry_result)

            result.append(str_entry_result)
        return result

    def ocr_entry(self, entry) -> str:
        copy_array_numbers = set()
        new_array_numbers = self.get_ocr_entry(entry)

        if not self.check_sum(new_array_numbers):
            for index, entry_en in enumerate(entry):
                entry_one = self.change_one_character(entry, index)
                new_array_numbers2 = self.get_ocr_entry(entry_one)
                if self.check_sum(new_array_numbers2):
                    copy_array_numbers.add(new_array_numbers2)
        else:
            copy_array_numbers.add(new_array_numbers)

        return copy_array_numbers

    def read_numbers(self, file_name: str) -> list:
        self.provider.folder_path = self.folder_path
        return self.provider.read(file_name)

    def write_numbers(self, source_list: list, file_name) -> None:
        number_list = []
        for source in source_list:
            number = self.get_entry_numbers(source)
            if constant.INC in number:
                number += constant.ILL_
            elif self.check_sum(number) != 0:
                number += constant.ERR_
            number_list.append(number)

        self.provider.folder_path = self.folder_path
        self.provider.write(number_list, file_name)

    def get_entry_numbers(self, entry) -> str:
        string_return = ''
        array_return = self.get_entry_array(entry)
        for array_entry in array_return:
            string_return += self.read_number(array_entry)

        return string_return

    def read_number(self, number_array) -> int:
        first_line = number_array[0]
        second_line = number_array[1]
        thirt_line = number_array[2]
        result = constant.INC
        if first_line == constant.TEC0:
            result = self._if_line(
                second_line,
                constant.TEC1,
                constant.ONE,
                constant.FOUR)
        elif(first_line == ' _ '):
            match second_line:
                case second_line if second_line == constant.TEC1:
                    result = constant.SEVEN
                case second_line if second_line == constant.TEC2:
                    result = self._if_line(
                        thirt_line,
                        constant.TEC3,
                        constant.TWO,
                        constant.THREE)
                case second_line if second_line == constant.TEC3:
                    result = self._if_line(
                        thirt_line,
                        constant.TEC2,
                        constant.FIVE,
                        constant.SIX)
                case second_line if second_line == constant.TEC4:
                    result = constant.ZERO
                case second_line if second_line == constant.TEC5:
                    result = self._if_line(
                        thirt_line,
                        constant.TEC5,
                        constant.EIGHT,
                        constant.INC,
                        constant.TEC2,
                        constant.NINE)
                case _:
                    result = constant.INC
        else:
            result = constant.INC

        return result

    def get_entry_array(self, entry) -> list:
        array_return = []
        lines = entry.split(constant.BREAK_LINE)
        from_line = 0
        to_line = 3
        while to_line <= 27:
            number_array = []
            for line in lines:
                number_array.append(line[from_line:to_line])

            array_return.append(number_array)
            to_line += 3
            from_line += 3

        return array_return

    def check_sum(self, number_string):
        if len(number_string) < 9:
            return None
        result = 0
        position = 9
        for d in number_string:
            result += int(d)*position
            position -= 1

        return result % 11

    def change_character(self, number_char):
        char_result = number_char
        match number_char:
            case number_char if number_char == constant.OEC0:
                char_result = random.choice([constant.OEC1, constant.OEC2])
            case number_char if number_char == constant.OEC2:
                char_result = random.choice([constant.OEC1, constant.OEC0])
            case number_char if number_char == constant.OEC1:
                char_result = random.choice([constant.OEC0, constant.OEC2])
        return char_result

    def change_one_character(self, number_array, index):
        result = number_array
        if index < len(number_array):
            char_index = number_array[index]
            result = '{}{}{}'.format(
                number_array[:index],
                self.change_character(char_index),
                number_array[index + 1:])
        return result

    def _if_line(
            self,
            line,
            line_if,
            number_if,
            number_else,
            line_elif=constant.EX,
            number_elif=constant.EX):
        result = number_else
        if line == line_if:
            result = number_if
        elif line == line_elif:
            result = number_elif

        return result

    def is_invalid_entry_number(sn): constant.ERR in sn or constant.ILL in sn or constant.INC in sn

    def transform_number(self, trhee_lines_number) -> list:
        first_line = trhee_lines_number[0]
        second_line = trhee_lines_number[1]
        thirt_line = trhee_lines_number[2]
        if first_line == constant.TEC0:
            if second_line != constant.TEC5 and second_line != constant.TEC1:
                second_line = random.choice([constant.TEC5, constant.TEC1])
            thirt_line = constant.TEC1
        elif first_line == constant.TEC6:
            match second_line:
                case second_line if second_line == constant.TEC1:
                    thirt_line = constant.TEC1
                case second_line if second_line == constant.TEC4:
                    thirt_line = constant.TEC5
                case second_line if second_line == constant.TEC2:
                    thirt_line = random.choice([constant.TEC3, constant.TEC2])
                case second_line if second_line == constant.TEC5 or second_line == constant.TEC3:
                    thirt_line = random.choice([constant.TEC5, constant.TEC2])
                case _:
                    second_line = random.choice(
                        [
                            constant.TEC1,
                            constant.TEC2,
                            constant.TEC5,
                            constant.TEC3,
                            constant.TEC4])
                    self.transform_number([first_line, second_line, thirt_line])
        else:
            first_line = random.choice([constant.TEC0, constant.TEC6])
            self.transform_number([first_line, second_line, thirt_line])

        return [first_line, second_line, thirt_line]

    def ocr_entry_questionmark(self, number, entry) -> str:
        copy_number = ''
        if number == constant.INC:
            number_ = self.transform_number(entry)
            number_ = self.read_number(number_)
            if number_ in constant.NUMBERS:
                copy_number = number_
        else:
            copy_number = number
        return copy_number

    def get_ocr_entry(self, entry) -> str:
        array_entries = self.get_entry_array(entry)
        array_numbers = self.get_entry_numbers(entry)
        new_array_numbers = ''
        if constant.INC in array_numbers:
            for index, number in enumerate(array_numbers):
                number_ = self.ocr_entry_questionmark(
                    number, array_entries[index])
                new_array_numbers += number_
            new_array_numbers = new_array_numbers
        else:
            new_array_numbers = array_numbers

        return new_array_numbers
