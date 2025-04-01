from util.input import *
from util.resister_excel import *

if __name__ == "__main__":
    form = ExpenseForm().execute()
    writer = KakeiboWriter(form['購入日'])
    new_row = writer.append_data(form)
    one_message(str(new_row)+"行目に書き込みを行いました。")
