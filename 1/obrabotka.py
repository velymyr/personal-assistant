# def __init__(self, value=''):
#     self.__value = None
#     if value:
#         self.value = value
#     while True:
#         if value:
#             self.value = value
#             break
#         else:
#             self.value = input("Birthday date(dd/mm/YYYY): ")
#         try:
#             if re.fullmatch('^\d{2}/\d{2}/\d{4}$', self.value):
#                 # pattern_bd = "(\d{2})/(\d{2})/(\d{4})"
#                 # if re.match(pattern_bd, self.value):
#                 self.value = dt.strptime(self.value.strip(), "%d/%m/%Y")
#                 break
#             elif self.value == '':
#                 break
#             else:
#                 raise ValueError
#         except ValueError:
#             print('Incorrect date! Please provide correct date format.')

# def __getitem__(self):
#     return self.value

# @property
# def value(self):
#     return self.__value

# @value.setter
# def value(self, value):
#     try:
#         if dt.strptime(value, "%d/%m/%Y"):
#             self.__value = dt.strptime(value, "%d/%m/%Y")
#     except ValueError:
#         return value

# def __str__(self):
