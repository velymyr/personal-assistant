def __init__(self, value=''):
        while True:
            self.value = []
            if value:
                self.values = value
            else:
                self.values = input("Phones(+12digits) (Введіть номер телефона + і дванадцять цифр): ")
            try:
                for number in self.values.split(' '):
                    if re.match('^\+\d{12}$', number) or number == '':
                        result = f"{number[0]}{number[1]}{number[2]}{number[3]}({number[4]}{number[5]}){number[6]}{number[7]}{number[8]}-{number[9]}{number[10]}-{number[11]}{number[12]}"
                    # if re.match('^\+48\d{9}$', number) or re.match('^\\+38\d{10}$', number) or number == '':
                        self.value.append(result)
                    else:
                        raise ValueError
            except ValueError:
                print('Incorrect phone number format! Please provide correct phone number format.')
            else:
                break
