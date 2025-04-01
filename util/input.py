import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
import sys


def one_message(comment):
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("メッセージ", comment , parent=root)
    root.destroy()

class ExpenseForm(tk.Tk):
    def __init__(self):
        self.winsize = {"width":220, "height":200}
        self.font = ("メイリオ", 12)  # フォントの設定

        super().__init__()        # TKから__init__メソッドを呼び出す。
        self.title("入力")
        #self.geometry("250x170")
        self.wm_minsize(width=self.winsize["width"], height=self.winsize["height"])
        self.window_center()
        self.create_widgets()

    def open_num_pad(self):
        num_pad = tk.Toplevel(self)
        num_pad.title("数字入力")
        num_pad.resizable(False, False)
        num_pad.grab_set()  # モーダル化

        def add_digit(digit):
            current = self.price_entry.get()
            self.price_entry.delete(0, tk.END)
            self.price_entry.insert(tk.END, current + str(digit))

        def delete_last():
            current = self.price_entry.get()
            self.price_entry.delete(0, tk.END)
            self.price_entry.insert(tk.END, current[:-1])

        # ボタン配置
        buttons = [
            ('7', lambda: add_digit(7)), ('8', lambda: add_digit(8)), ('9', lambda: add_digit(9)),
            ('4', lambda: add_digit(4)), ('5', lambda: add_digit(5)), ('6', lambda: add_digit(6)),
            ('1', lambda: add_digit(1)), ('2', lambda: add_digit(2)), ('3', lambda: add_digit(3)),
            ('0', lambda: add_digit(0)), ('←', delete_last), ('完了', num_pad.destroy),
        ]

        for idx, (text, cmd) in enumerate(buttons):
            row, col = divmod(idx, 3)
            btn = tk.Button(num_pad, text=text, width=3, height=1, command=cmd, font=("メイリオ", 12))
            btn.grid(row=row, column=col, padx=1, pady=1)

    def create_widgets(self):
        common_font = ("メイリオ", 12)

        def add_label_entry(row, text, entry_widget):
            label = tk.Label(self, text=text, font=common_font)
            label.grid(row=row, column=0, sticky="e")
            entry_widget.grid(row=row, column=1)

        box_width = 15
        row = 0
        # 購入日
        self.date_entry = DateEntry(self, width=box_width-2, background='darkblue', foreground='white', borderwidth=2, showweeknumbers=False, font=common_font, date_pattern="yyyy/mm/dd")
        add_label_entry(row, "購入日：", self.date_entry)

        # 費目
        row += 1
        options = ["食費", "生活雑貨", "贅沢費用", "その他"]
        self.category_entry = ttk.Combobox(self, values=options, width=box_width-2, font=common_font)
        add_label_entry(row, "費目：", self.category_entry)

        # 金額
        row += 1
        self.price_entry = tk.Entry(self, width=box_width, font=common_font)
        self.price_entry.grid(row=row, column=1)

        price_label = tk.Label(self, text="金額：", font=common_font)
        price_label.grid(row=row, column=0, sticky="e")

        # 数字入力ボタン追加
        tk.Button(self, text="入力", command=self.open_num_pad, font=("メイリオ", 10), width=4, height=0).grid(row=row, column=2, padx=2)

        # 名称
        row += 1
        self.name_entry = tk.Entry(self, width=box_width, font=common_font)
        item_list = ["外食", "料理食材", "飲み物", "お菓子", "レンタカー", "薬", "化粧品", "洗剤"]
        self.name_entry = ttk.Combobox(self, values=item_list, width=box_width-2, font=common_font)
        add_label_entry(row, "名称：", self.name_entry)

        # チェックボックス
        row += 1
        check_label = tk.Label(self, text="カード：", font=common_font)
        check_label.grid(row=row, column=0, sticky="e")
        self.check_var = tk.IntVar(value=1)
        tk.Checkbutton(self, variable=self.check_var).grid(row=row, column=1)

        # 立替者
        row += 1
        options = ["R", "N", ""]
        self.payer_entry = ttk.Combobox(self, values=options, width=box_width-2, font=common_font)
        add_label_entry(row, "立替者：", self.payer_entry)

        # 送信ボタン
        row += 1
        tk.Button(self, text="送信", command=self.submit_form, width=5, font=common_font).grid(row=row, column=0, columnspan=2)



    def submit_form(self):
        # フォームの内容を取得する
        date = self.date_entry.get()
        category = self.category_entry.get()
        price = self.price_entry.get()
        name = self.name_entry.get()
        is_private_card = self.check_var.get()
        payer = self.payer_entry.get()

        # チェックボックスからの返り値を変更する
        is_private_card = "✓" if is_private_card == 0 else ""


        # フォームをクリアする
        self.information = {
            "購入日": date,
            "費目": category,
            "金額": price,
            "名称": name,
            "非クレカ使用": is_private_card,
            "立替者": payer
        }
        self.destroy()

    def window_center(self):
        # ウィンドウを中央に移動する
        x_pos = (self.winfo_screenwidth() - self.winsize["width"]) / 2
        y_pos = (self.winfo_screenheight() - self.winsize["height"]) / 2
        self.geometry("+%d+%d" % (x_pos, y_pos))

    def execute(self):
        self.mainloop()

        # アラームウィンドウ表示する際、空ウィンドウを表示させないための対処
        root = tk.Tk()
        root.withdraw()
        try:
            if self.information['費目'] == "" or self.information['金額'] == "" or self.information['名称'] == "":
                raise ValueError("必須項目に空欄があります。")
            if self.information['金額'].isdigit():
                self.information['金額'] = int(self.information['金額'])
            else:
                raise ValueError("金額に数値以外の値が入っています。")
            root.destroy()
            return self.information
        except (ValueError, AttributeError) as e:
            # ValueError または AttributeError に共通処理
            error_message = str(e) if isinstance(e, ValueError) else "強制終了: ×が押されました。"
            messagebox.showerror("エラー", error_message, parent=root)
            root.destroy()
            sys.exit()
        except Exception as e:
            messagebox.showerror("エラー", "予期せぬエラーが発生しました: {}".format(e), parent=root)
            root.destroy()
            sys.exit()
            # 上記以外のエラーが発生した場合の処理


if __name__ == "__main__":
    form = ExpenseForm().execute()
    print(form)

