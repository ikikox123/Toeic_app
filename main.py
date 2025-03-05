import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import csv

# 🔄 定義章節列表
chapters = [
    "General Business（一般商務）",
    "Personnel & Management（人力資源與管理）",
    "Offices & Technology（辦公室&科技）",
    "Manufacturing & Marketing（製造&行銷）",
    "Banking & Finance（銀行&財務）",
    "Fundamental Words（基礎單字）",
    "Purchase & Negotiation（採購&協商）",
    "Correspondence（信件）",
    "Law & Housing & Magazine（法律&住宅&雜誌）",
    "News（新聞）",
    "Entertainment & Socializing（娛樂及社交）",
    "Health & Food（健康&食物）",
    "Phrases（片語）"
]

# 🔄 修改 load_questions 函式，根據模式載入 cn.csv 或 en.csv 並隨機選錯誤選項
def load_questions(mode):
    questions = []
    all_cn = []
    all_en = []

    # 讀取所有單字，方便後面做隨機選項
    with open('cn.csv', 'r', encoding='utf-8') as cn_file:
        cn_reader = csv.DictReader(cn_file)
        for row in cn_reader:
            all_cn.append(row['Chinese'])
            all_en.append(row['English'])

    # 根據模式選擇題庫
    filename = 'cn.csv' if mode == '中翻英' else 'en.csv'
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if mode == '中翻英':
                # 正確答案
                correct_answer = row['English']
                # 隨機選兩個錯誤答案 (不能和正確答案一樣)
                wrong_answers = random.sample([w for w in all_en if w != correct_answer], 2)
                # 將正確答案和錯誤答案混合
                options = wrong_answers + [correct_answer]
                random.shuffle(options)

                questions.append({
                    '題目': row['Chinese'],
                    '選項1': options[0],
                    '選項2': options[1],
                    '選項3': options[2],
                    '答案': correct_answer
                })
            else:
                # 正確答案
                correct_answer = row['Chinese']
                # 隨機選兩個錯誤答案 (不能和正確答案一樣)
                wrong_answers = random.sample([w for w in all_cn if w != correct_answer], 2)
                # 將正確答案和錯誤答案混合
                options = wrong_answers + [correct_answer]
                random.shuffle(options)

                questions.append({
                    '題目': row['English'],
                    '選項1': options[0],
                    '選項2': options[1],
                    '選項3': options[2],
                    '答案': correct_answer
                })

    random.shuffle(questions)  # 隨機排列題目順序
    return questions[:50]  # 只出50題# 🔄 新增單字（可以連續輸入）
def add_word(chapter):
    while True:
        english_word = simpledialog.askstring("新增英文單字", f"在 {chapter} 中輸入英文單字（按取消結束）：")
        if not english_word:
            break

        chinese_word = simpledialog.askstring("新增中文意思", f"在 {chapter} 中輸入對應的中文意思：")
        if not chinese_word:
            break

        if chinese_word.strip() and english_word.strip():
            try:
                with open('cn.csv', 'a', encoding='utf-8', newline='') as cn_file:
                    cn_writer = csv.writer(cn_file)
                    cn_writer.writerow([chinese_word.strip(), english_word.strip()])

                with open('en.csv', 'a', encoding='utf-8', newline='') as en_file:
                    en_writer = csv.writer(en_file)
                    en_writer.writerow([english_word.strip(), chinese_word.strip()])

                messagebox.showinfo("成功", f"已新增單字：{english_word} - {chinese_word}")
            except Exception as e:
                messagebox.showerror("錯誤", f"儲存失敗: {e}")
        else:
            messagebox.showwarning("警告", "請輸入完整的中文和英文！")

# 🔄 選擇章節 (所有文字置中)
def select_chapter():
    clear_window()
    
    # 標題置中
    tk.Label(root, text="選擇章節", font=("PingFang TC", 30), bg="white", fg="black").place(relx=0.5, rely=0.1, anchor='center')
    
    # 用 Frame 和 Canvas 做滾動區域
    canvas = tk.Canvas(root, bg="white")
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="white")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    # 建立滾動區域
    canvas.create_window((0, 0), window=scrollable_frame, anchor="n")
    canvas.configure(yscrollcommand=scrollbar.set)

    # 章節按鈕置中
    for chapter in chapters:
        tk.Button(scrollable_frame, text=chapter, font=("PingFang TC", 20), bg="white", fg="black",
                  command=lambda ch=chapter: chapter_menu(ch)).pack(pady=5, anchor='center')
    
    # 返回主選單按鈕置中
    tk.Button(scrollable_frame, text="返回主選單", font=("PingFang TC", 20), bg="white", fg="black", 
              command=main_menu).pack(pady=20, anchor='center')

    # 把 Canvas 和 Scrollbar 放進去
    canvas.place(relx=0.5, rely=0.5, anchor='center', width=550, height=550)
    scrollbar.place(relx=0.98, rely=0.5, anchor='center', height=500)
# 🔄 修改 chapter_menu 函式，點擊「開始測驗」後選擇模式
def chapter_menu(chapter):
    clear_window()
    tk.Label(root, text=f"{chapter}", font=("PingFang TC", 30), bg="white", fg="black").pack(pady=20)
    tk.Button(root, text="新增單字", font=("PingFang TC", 20), bg="white", fg="black",
              command=lambda: add_word(chapter)).pack(pady=10)
    tk.Button(root, text="開始測驗", font=("PingFang TC", 20), bg="white", fg="black",
              command=lambda: select_mode(chapter)).pack(pady=10)  # 🔄 修改這裡
    tk.Button(root, text="返回章節選單", font=("PingFang TC", 20), bg="white", fg="black", command=select_chapter).pack(pady=10)

# 🔄 選擇測驗模式（中翻英 / 英翻中）
def select_mode(chapter):
    clear_window()
    tk.Label(root, text="選擇測驗模式", font=("PingFang TC", 30), bg="white", fg="black").pack(pady=20)
    
    tk.Button(root, text="中翻英", font=("PingFang TC", 20), bg="white", fg="black",
              command=lambda: start_quiz(chapter, "中翻英")).pack(pady=10)
    tk.Button(root, text="英翻中", font=("PingFang TC", 20), bg="white", fg="black",
              command=lambda: start_quiz(chapter, "英翻中")).pack(pady=10)
    tk.Button(root, text="返回章節選單", font=("PingFang TC", 20), bg="white", fg="black", command=select_chapter).pack(pady=10)

# 🔄 顯示下一題
def show_next_question():
    global current_question, questions

    # 🔄 如果題目做完，顯示結果
    if current_question >= len(questions):
        show_result()
        return

    q = questions[current_question]
    options = [q['選項1'], q['選項2'], q['選項3']]
    random.shuffle(options)

    clear_window()

    # 🔄 題目標題
    tk.Label(root, text=f"題目: {current_question + 1}/{len(questions)}", font=("PingFang TC", 30), bg="white", fg="black").pack(pady=20)
    tk.Label(root, text=f"{q['題目']}", font=("PingFang TC", 50), bg="white", fg="black").pack(pady=20)

    # 🔄 選項按鈕
    for idx, option in enumerate(options):
        tk.Button(root, text=option, font=("PingFang TC", 25), bg="white", fg="black",
                  command=lambda opt=option: check_answer(opt, q)).pack(pady=10)
# 🔄 檢查答案
def check_answer(selected_option, q):
    global score, current_question, answered_questions, error_questions
    if selected_option == q['答案']:
        score += 1
    else:
        error_questions.append((q['題目'], q['答案'], selected_option))
    
    answered_questions.append((q['題目'], q['答案'], selected_option))
    current_question += 1
    show_next_question()
# 清除視窗內容
def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

# 主選單
def main_menu():
    clear_window()
    tk.Label(root, text="TOEIC 單字測驗", font=("PingFang TC", 50), bg="white", fg="black").place(relx=0.5, rely=0.2, anchor='center')
    tk.Button(root, text="選擇章節", font=("PingFang TC", 25), bg="white", fg="black", command=select_chapter).place(relx=0.5, rely=0.4, anchor='center')
    tk.Button(root, text="結束測驗", font=("PingFang TC", 25), bg="white", fg="black", command=root.destroy).place(relx=0.5, rely=0.6, anchor='center')

# 🔄 修改 start_quiz 函式，傳入模式參數
def start_quiz(chapter, mode):
    clear_window()
    global current_question, score, answered_questions, error_questions, questions
    current_question = 0
    score = 0
    answered_questions = []
    error_questions = []

    # 根據模式載入不同的題庫
    questions = load_questions(mode)

    if not questions:
        messagebox.showinfo("錯誤", "沒有符合該模式的題目！")
        main_menu()
        return

    show_next_question()
# 顯示測驗結果
def show_result():
    clear_window()
    tk.Label(root, text=f"測驗結束！你的成績是: {score}/{len(questions)}", font=("PingFang TC", 25), bg="white", fg="black").pack(pady=20)
    
    if error_questions:
        tk.Button(root, text="查看錯題解釋", font=("PingFang TC", 20), bg="white", fg="black", command=show_error_explanation).pack(pady=10)
    else:
        tk.Label(root, text="沒有錯題，做得很好！", font=("PingFang TC", 20), bg="white", fg="black").pack(pady=10)
    
    tk.Button(root, text="返回主選單", font=("PingFang TC", 25), bg="white", fg="black", command=main_menu).pack(pady=20)

# 🔄 逐一顯示錯題的解釋
def show_error_explanation():
    clear_window()
    global current_error_index
    current_error_index = 0  # 用來記錄當前顯示的錯題索引
    show_next_error()  # 顯示第一個錯題

# 🔄 顯示下一個錯題
def show_next_error():
    global current_error_index
    clear_window()
    
    if current_error_index >= len(error_questions):
        # 所有錯題都看完了，返回主選單
        tk.Button(root, text="返回主選單", font=("PingFang TC", 25), bg="white", fg="black", command=main_menu).pack(pady=20)
        return
    
    q, correct, selected = error_questions[current_error_index]
    tk.Label(root, text=f"錯題 {current_error_index + 1}/{len(error_questions)}", font=("PingFang TC", 25), bg="white", fg="black").pack(pady=10)
    tk.Label(root, text=f"題目: {q}", font=("PingFang TC", 20), bg="white", fg="black").pack(pady=10)
    tk.Label(root, text=f"正確答案: {correct}", font=("PingFang TC", 20), bg="white", fg="green").pack(pady=5)
    tk.Label(root, text=f"你的回答: {selected}", font=("PingFang TC", 20), bg="white", fg="red").pack(pady=5)
    
    current_error_index += 1
    tk.Button(root, text="下一題", font=("PingFang TC", 20), bg="white", fg="black", command=show_next_error).pack(pady=20)
# 主要程式
root = tk.Tk()
root.title("TOEIC 單字測驗")
root.geometry("1289x900")
root.configure(bg="white")

main_menu()
root.mainloop()