import datetime

def main_bd(date):
    str_date = str(date)
    now = datetime.datetime.now()
    then = datetime.datetime.strptime(str_date, "%d/%m/%Y")
    delta1 = datetime.datetime(now.year, then.month, then.day)
    delta2 = datetime.datetime(now.year+1, then.month, then.day)
    result = ((delta1 if delta1 >= now else delta2) - now).days
    return result


if __name__ == "__main__":
    main_bd()
