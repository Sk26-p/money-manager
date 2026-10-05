from datetime import datetime
import unicodedata
totali = 0
totale = 0
totalinv = 0
totals = 0

transactions = []

try:
  file = open("transactions.csv", "r")

  for line in file:
    line = line.strip()
    data = line.split(",")
    transactions.append([data[0], data[1], int(data[2]), data[3],data[4]])
 
    if data[3] == "収入":
      totali += int(data[2])

    if data[3] == "支出":
      totale += int(data[2])

    if data[3] == "投資":
      totalinv += int(data[2])

    if data[3] == "貯金":
      totals += int(data[2])

  file.close()
except FileNotFoundError:
  pass

def date_key(transaction):
  date_parts = transaction[0].split("/")
  year_part = int(date_parts[0])
  month_part = int(date_parts[1])
  day_part = int(date_parts[2])
  return(year_part, month_part, day_part)

def amount_key(item):
  return item[1]

def show_detail(category):
  print("{" + category + "内訳}")
  detail_totals = {}
  for transaction in transactions:
    if transaction[3] == category:
      detail = transaction[4]
      if detail in detail_totals:
        detail_totals[detail] = detail_totals[detail] + transaction[2]
      else:
        detail_totals[detail] = transaction[2]
  
  for detail, total in sorted(detail_totals.items(), key = amount_key, reverse = True):
    print(detail, ":", total, "円")

  detail_choice = input("b:集計表示に戻る")
  detail_choice = unicodedata.normalize("NFKC", detail_choice)
  if detail_choice == "b":
    return
  
def add_transaction():
  global totali, totale, totalinv, totals
  today = datetime.now()
  year = today.year
  month = today.month
  day = today.day

  with open("transactions.csv", "a") as file:

    continue_choice = "はい"
    while continue_choice == "はい":

      date_input = input("日付(今日ならEnter,日付指定,bでメニューに戻る)")
      date_input = unicodedata.normalize("NFKC", date_input)
      if date_input == "b" or date_input == "ｂ":
        return
      
      if date_input == "":
        date = str(year) + "/" + str(month) + "/" + str(day)

      else:
        if "/" not in date_input:
          date = str(year) + "/" + str(month) + "/" + date_input
        if "/" in date_input:
          date_parts = date_input.split("/")
          if len(date_parts) == 2:
            date = str(year) + "/" + date_input
          if len(date_parts) == 3:
            date = date_input

      name = input("名前(bでメニューに戻る)")
      if name == "b" or name == "ｂ":
        return

      while True:
        try:
          money_input = input("金額(bでメニューに戻る)")
          if money_input == "b" or money_input == "ｂ":
            return
          
          money = int(money_input)
          break
        except ValueError:
          print("数字のみ入力してください。")
          
      while True:
        category = input("種類(収入,支出,投資,貯金)(bでメニューに戻る)")
        if category == "b" or category == "ｂ":
          return
        
        if category == "収入" or category == "支出" or category == "投資" or category == "貯金":
          break
        else:
          print("収入,支出,投資,貯金のいずれかを入力してください。")

      while True:
        detail = input("内容")
        if detail == "b" or detail == "ｂ":
          return
        else:
          break

      transactions.append([date, name, money, category, detail])
      transactions.sort(key = date_key)
      with open("transactions.csv", "w") as file:
        for transaction in transactions:
          file.write(transaction[0] + "," + transaction[1] + "," + str(transaction[2]) + "," + transaction[3] + "," + transaction[4] + "\n")
      
      if category == "収入":
        totali = totali + money
        
      if category == "支出":
        totale = totale + money

      if category == "投資":
        totalinv = totalinv + money

      if category == "貯金":
        totals = totals + money
      
      continue_choice = input("続けますか？")

def show_transactions():
  for transaction in transactions:
      print(transaction[0], transaction[1], transaction[2], "円", transaction[3], transaction[4])

def show_total():
  while True:
    detail_totals = {}
    for transaction in transactions:
      if transaction[3] == "支出":
        detail = transaction[4]
        if detail in detail_totals:
          detail_totals[detail] = detail_totals[detail] + transaction[2]
        else:
          detail_totals[detail] = transaction[2]

    print("収入:", totali, "円")
    print("支出:", totale, "円")
    print("投資:", totalinv, "円")
    print("貯金:", totals, "円")
    print("残り:", totali - totale - totalinv - totals, "円")

    total_choice = input("1:収入内訳 2:支出内訳 3:投資内訳 4:貯金内訳 5:月別集計\nb:メニューに戻る\n")
    total_choice = unicodedata.normalize("NFKC", total_choice)
    if total_choice == "b":
      return
    if total_choice == "1":
      show_detail("収入")
    if total_choice == "2":
      show_detail("支出")
    if total_choice == "3":
      show_detail("投資")
    if total_choice == "4":
      show_detail("貯金")
    if total_choice == "5":
      show_monthly_total()

def delete_transaction():
  global totali, totale, totalinv, totals
  for number, transaction in enumerate(transactions):
    print(number + 1, transaction[0], transaction[1], transaction[2], "円", transaction[3], transaction[4])
    
  try:
    delete_number_input = input("削除する番号(bでメニューに戻る)")
    if delete_number_input == "b" or delete_number_input == "ｂ":
      return
      
    delete_number = int(delete_number_input)
        
    if 1 <= delete_number and delete_number <= len(transactions):
          
      delete_transaction = transactions.pop(delete_number - 1)
            
      if delete_transaction[3] == "収入":
        totali = totali - delete_transaction[2]
            
      if delete_transaction[3] == "支出":
        totale = totale - delete_transaction[2]

      if delete_transaction[3] == "投資":
        totalinv = totalinv - delete_transaction[2]

      if delete_transaction[3] == "貯金":
        totals = totals - delete_transaction[2]

      file = open("transactions.csv", "w")
          
      for transaction in transactions:
        file.write(transaction[0] + "," + transaction[1] + "," + str(transaction[2]) + "," + transaction[3] + "," + transaction[4] + "\n")
          
      file.close()
          
    else:
      print("その番号はありません。")
        
  except ValueError:
    print("数字を入力してください。")

def show_monthly_total():
  while True:
    year_input = input("年:Enterで今年(bでメニューに戻る)")
    year_input = unicodedata.normalize("NFKC", year_input)
    if year_input == "b":
      return
    if year_input == "":
      year_input = str(datetime.now().year)
    month_input = input("月:Enterで今月")
    if month_input == "":
      month_input = str(datetime.now().month)
    year_input = int(year_input)
    month_input = int(month_input)

    monthly_income = 0
    monthly_expense = 0
    monthly_investment = 0
    monthly_savings = 0

    for transaction in transactions:
      date_parts = transaction[0].split("/")
      transaction_year = int(date_parts[0])
      transaction_month = int(date_parts[1])
      if transaction_year == year_input and transaction_month == month_input:
        if transaction[3] == "収入":
          monthly_income += transaction[2]
        if transaction[3] == "支出":
          monthly_expense += transaction[2]
        if transaction[3] == "投資":
          monthly_investment += transaction[2]
        if transaction[3] == "貯金":
          monthly_savings += transaction[2]
        
    print("{", year_input, "年", month_input, "月}")
    print("収入:", monthly_income, "円")
    print("支出:", monthly_expense, "円")
    print("投資:", monthly_investment, "円")
    print("貯金:", monthly_savings, "円")
    print("残り:", monthly_income - monthly_expense - monthly_investment - monthly_savings, "円")

    monthly_detail_choice = input("1:収入内訳 2:支出内訳 3:投資内訳 4:貯金内訳\nEnter:別の年月\n")
    if monthly_detail_choice == "1":
      show_monthly_detail("収入", year_input, month_input)
    if monthly_detail_choice == "2":
      show_monthly_detail("支出", year_input, month_input)
    if monthly_detail_choice == "3":
      show_monthly_detail("投資", year_input, month_input)
    if monthly_detail_choice == "4":
      show_monthly_detail("貯金", year_input, month_input)
      
def show_monthly_detail(category, year, month):
  detail_totals = {}
  for transaction in transactions:
    data_parts = transaction[0].split("/")
    transaction_year = int(data_parts[0])
    transaction_month = int(data_parts[1])
    if transaction_year == year and transaction_month == month and transaction[3] == category:
      detail = transaction[4]
      if detail in detail_totals:
        detail_totals[detail] += transaction[2]
      else:
        detail_totals[detail] = transaction[2]
  print("{", year, "年", month, "月", category, "内訳}")
  for detail, total in sorted(detail_totals.items(), key = amount_key, reverse = True):
    print(detail, ":", total, "円")

menu = ""
while menu != "5" and menu != "５":

  print("1.取引追加")      
  print("2.取引履歴")
  print("3.集計表示")
  print("4.履歴削除")
  print("5.終了")
  menu = input("選択:")

  if menu == "1" or menu == "１":
    add_transaction()

  if menu == "2" or menu == "２":
    show_transactions()

  if menu == "3" or menu == "３":
    show_total()
  
  if menu == "4" or menu == "４":
    delete_transaction()