import tkinter as tk
from tkinter import simpledialog, messagebox
import csv

# 新增單字的函式
def add_words():
    while True:
        # 輸入中文
        chinese = simpledialog.askstring("新增單字", "請輸入中文意思 (按取消結束):")
        if chinese is None:  # 按取消結束
            break

        # 輸入英文
        english = simpledialog.askstring("新增單字", "請輸入英文單字:")
        if english is None:  # 按取消結束
            break

        # 確認中英文都輸入了才儲存
        if chinese and english:
            try:
                # 儲存到 cn.csv
                with open('/Applications/TOEIC_APP/cn.csv', 'a', encoding='utf-8', newline='') as cn_file:
                    cn_writer = csv.writer(cn_file)
                    cn_writer.writerow([chinese, english])

                # 儲存到 en.csv
                with open('/Applications/TOEIC_APP/en.csv', 'a', encoding='utf-8', newline='') as en_file:
                    en_writer = csv.writer(en_file)
                    en_writer.writerow([english, chinese])

                messagebox.showinfo("成功", f"成功新增單字: {chinese} - {english}")
            except Exception as e:
                messagebox.showerror("錯誤", f"儲存失敗: {e}")
        else:
            messagebox.showwarning("警告", "請輸入完整的中文和英文！")

# 建立 Tkinter 視窗 (為了使用 simpledialog)
root = tk.Tk()
root.withdraw()  # 隱藏主視窗，只顯示輸入框

add_words()  # 開始新增單字