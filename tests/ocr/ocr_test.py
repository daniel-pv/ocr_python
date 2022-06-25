import pytest
import sys
import os
from retry import retry
sys.path.insert(1, '')
from ocr.ocr import OCR
from src.providers.file.fileprov import FileProvider
script_dir = os.path.dirname(__file__)
file_name = 'data/test_data.txt'


class TestOCR:
    fileProvider = FileProvider()
    ocr = OCR(fileProvider)
    ocr.folder_path = script_dir

# PHASE 1
    def test_zeros(self):
        zero = """ _  _  _  _  _  _  _  _  _ 
| || || || || || || || || |
|_||_||_||_||_||_||_||_||_|

"""
        assert self.ocr.get_entry_numbers(zero) == '000000000'

    def test_ones(self):
        one = """                           
  |  |  |  |  |  |  |  |  |
  |  |  |  |  |  |  |  |  |
"""
        assert self.ocr.get_entry_numbers(one) == '111111111'

    def test_twos(self):
        two = """ _  _  _  _  _  _  _  _  _ 
 _| _| _| _| _| _| _| _| _|
|_ |_ |_ |_ |_ |_ |_ |_ |_ 
"""
        assert self.ocr.get_entry_numbers(two) == '222222222'

    def test_threes(self):
        three = """ _  _  _  _  _  _  _  _  _ 
 _| _| _| _| _| _| _| _| _|
 _| _| _| _| _| _| _| _| _|
"""
        assert self.ocr.get_entry_numbers(three) == '333333333'

    def test_fours(self):
        four = """                           
|_||_||_||_||_||_||_||_||_|
  |  |  |  |  |  |  |  |  |
"""
        assert self.ocr.get_entry_numbers(four) == '444444444'

    def test_fives(self):
        five = """ _  _  _  _  _  _  _  _  _ 
|_ |_ |_ |_ |_ |_ |_ |_ |_ 
 _| _| _| _| _| _| _| _| _|
"""
        assert self.ocr.get_entry_numbers(five) == '555555555'

    def test_sixs(self):
        six = """ _  _  _  _  _  _  _  _  _ 
|_ |_ |_ |_ |_ |_ |_ |_ |_ 
|_||_||_||_||_||_||_||_||_|
"""
        assert self.ocr.get_entry_numbers(six) == '666666666'

    def test_sevens(self):
        seven = """ _  _  _  _  _  _  _  _  _ 
  |  |  |  |  |  |  |  |  |
  |  |  |  |  |  |  |  |  |
"""
        assert self.ocr.get_entry_numbers(seven) == '777777777'

    def test_eights(self):
        eight = """ _  _  _  _  _  _  _  _  _ 
|_||_||_||_||_||_||_||_||_|
|_||_||_||_||_||_||_||_||_|
"""
        assert self.ocr.get_entry_numbers(eight) == '888888888'

    def test_nines(self):
        nine = """ _  _  _  _  _  _  _  _  _ 
|_||_||_||_||_||_||_||_||_|
 _| _| _| _| _| _| _| _| _|
"""
        assert self.ocr.get_entry_numbers(nine) == '999999999'

    def test_one_to_nine(self):
        numbers = """    _  _     _  _  _  _  _ 
  | _| _||_||_ |_   ||_||_|
  ||_  _|  | _||_|  ||_| _|
"""
        assert self.ocr.get_entry_numbers(numbers) == '123456789'

    @pytest.mark.xfail
    def test_fail_empty_string(self):
        assert self.ocr.get_entry_numbers('') == '123456789'

# PHASE 2
    def test_checksum_valid(self):
        valid_check_sum = self.ocr.check_sum('345882865')
        assert valid_check_sum == 0
    
    def test_checksum_invalid(self):
        valid_check_sum = self.ocr.check_sum('123123123')
        assert valid_check_sum != 0

    @pytest.mark.xfail
    def test_checksum_fail(self):
        valid_check_sum = self.ocr.check_sum('')
        assert valid_check_sum == 0

# PHASE 3
    def test_write_numbers_success(self):
        entry_one_line = [""" _  _  _  _  _  _  _  _    
| || || || || || || ||_   |
|_||_||_||_||_||_||_| _|  |

"""]
        self.ocr.write_numbers(entry_one_line, file_name)
        numbers = self.ocr.read_numbers(file_name)
        assert numbers == ['000000051']

    def test_write_numbers_ill(self):
        entry_one_line = ["""    _  _     _  _  _  _  _ 
  | _| _||_| _ |_   ||_||_|
  ||_  _|  | _||_|  ||_| _ 
"""]
        self.ocr.write_numbers(entry_one_line, file_name)
        numbers = self.ocr.read_numbers(file_name)
        assert numbers == ['1234?678? ILL']

    def test_write_numbers_ill_two(self):
        entry_one_line = ["""    _  _  _  _  _  _     _ 
|_||_|| || ||_   |  |  | _ 
  | _||_||_||_|  |  |  | _|
"""]
        self.ocr.write_numbers(entry_one_line, file_name)
        numbers = self.ocr.read_numbers(file_name)
        assert numbers == ['49006771? ILL']

    def test_write_numbers_err(self):
        entry_one_line = ["""    _  _     _  _     _  _ 
  | _| _|  | _| _|  | _| _|
  ||_  _|  ||_  _|  ||_  _|
"""]
        self.ocr.write_numbers(entry_one_line, file_name)
        numbers = self.ocr.read_numbers(file_name)
        assert numbers == ['123123123 ERR']

    def test_write_numbers_err_ill(self):
        entry_one_line = ["""    _  _     _  _     _  _ 
  | _| _|  | _| _|  | _| _|
  ||_  _|  ||_  _|  ||_  _|
""", """    _  _  _  _  _  _     _ 
|_||_|| || ||_   |  |  | _ 
  | _||_||_||_|  |  |  | _|
"""]
        self.ocr.write_numbers(entry_one_line, file_name)
        numbers = self.ocr.read_numbers(file_name)
        assert numbers == ['123123123 ERR', '49006771? ILL']

# PHASE 4

    @retry(AssertionError, tries=10)
    def test_ocr_line_ones(self):
        numbers = """                           
  |  |  |  |  |  |  |  |  |
  |  |  |  |  |  |  |  |  |
"""
        assert '711111111' in self.ocr.ocr_entry(numbers)

    @retry(AssertionError, tries=10)
    def test_ocr_line_sevens(self):
        numbers = """ _  _  _  _  _  _  _  _  _ 
  |  |  |  |  |  |  |  |  |
  |  |  |  |  |  |  |  |  |
"""
        assert '777777177' in self.ocr.ocr_entry(numbers)

    @retry(AssertionError, tries=10)
    def test_ocr_line_two_zeros(self):
        numbers = """ _  _  _  _  _  _  _  _  _ 
 _|| || || || || || || || |
|_ |_||_||_||_||_||_||_||_|

"""
        assert '200800000' in self.ocr.ocr_entry(numbers)

    @retry(AssertionError, tries=10)
    def test_ocr_line_eights(self):
        numbers = """ _  _  _  _  _  _  _  _  _ 
|_||_||_||_||_||_||_||_||_|
|_||_||_||_||_||_||_||_||_|
"""
        result_numbers = {'888886888', '888888880', '888888988'}

        assert result_numbers.issubset(self.ocr.ocr_entry(numbers))

    @retry(AssertionError, tries=10)
    def test_ocr_line_fives(self):
        numbers = """ _  _  _  _  _  _  _  _  _ 
|_ |_ |_ |_ |_ |_ |_ |_ |_ 
 _| _| _| _| _| _| _| _| _|
"""
        result_numbers = {'555655555', '559555555'}

        assert result_numbers.issubset(self.ocr.ocr_entry(numbers))
