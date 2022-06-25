class Entry:
    def __init__(self) -> None:
        self.lineNumbers = [str] * 4

entry = Entry()
entry.lineNumbers = ['123','223','333', '412', '523']
for number in entry.lineNumbers:
    print(number)