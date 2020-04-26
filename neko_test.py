import tkinter
import random

index = 0       # ゲーム進行を管理する変数
timer = 0       # 時間を管理する変数
score = 0       # スコア用の変数
hisc = 1000
difficulty = 0
tsugi = 0       # 次にセットするネコの値を入れる変数

cursor_x = 0        # カーソル横方向の位置
cursor_y = 0        # カーソル縦方向の位置
mouse_x = 0         # マウスポインタのX座標
mouse_y = 0         # マウスポインタのY座標
mouse_c = 0         # マウスボタンをクリックした時の変数

# マウスを動かした時に実行する関数
def mouse_move(e):
    global mouse_x, mouse_y
    mouse_x = e.x
    mouse_y = e.y

# マウスボタンをクリックした時に実行する関数
def mouse_press(e):
    global mouse_c
    mouse_c = 1

neko = []       # マス目を管理する二次元リスト
check = []      # 判定用の二次元リスト
for i in range(10):
    neko.append([0,0,0,0,0,0,0,0])
    check.append([0,0,0,0,0,0,0,0])

# ネコを描写する関数
def draw_neko():
    cvs.delete("NEKO")
    for y in range(10):
        for x in range(8):
            if neko[y][x] > 0:
                cvs.create_image(x*72+60, y*72+60, image=img_neko[neko[y][x]], tag="NEKO")

# ネコが縦横斜めに３つ並んだか調べる関数
# nekoリストをcheckリストにコピーする
def check_neko():
    for y in range(10):
        for x in range(8):
            check[y][x] = neko[y][x]

# ネコが縦に3つ並んだ時の処理
    for y in range(1, 9):
        for x in range(8):
            if check[y][x] > 0:
                if check[y-1][x] == check[y][x] and check[y+1][x] == check[y][x]:
                    neko[y-1][x] = 7
                    neko[y][x] = 7
                    neko[y+1][x] = 7

# ネコが横に3つ並んだ時の処理
    for y in range(10):
        for x in range(1, 7):
            if check[y][x] > 0:
                if check[y][x-1] == check[y][x] and check[y][x+1] == check[y][x]:
                    neko[y][x-1] = 7
                    neko[y][x] = 7
                    neko[y][x+1] = 7

# ネコが斜めに3つ並んだ時の処理
    for y in range(1, 9):
        for x in range(1, 7):
            if check[y][x] > 0:
                # 左上と右下が3つ並んだら
                if check[y-1][x-1] == check[y][x] and check[y+1][x+1] == check[y][x]:
                    neko[y-1][x-1] = 7
                    neko[y][x] = 7
                    neko[y+1][x+1] = 7
                # 左下と右上が3つ並んだら
                if check[y+1][x-1] == check[y][x] and check[y-1][x+1] == check[y][x]:
                    neko[y+1][x-1] = 7
                    neko[y][x] = 7
                    neko[y-1][x+1] = 7

# 揃ったネコ（肉球）を消す関数
def sweep_neko():
    num = 0
    for y in range(10):
        for x in range(8):
            if neko[y][x] == 7:
                neko[y][x] = 0
                num += 1
    return num

# ネコを落下させる関数
def drop_neko():
    flg = False
    for y in range(8, -1, -1):
        for x in range(8):
            if neko[y][x] != 0 and neko[y+1][x] == 0:
                neko[y+1][x] = neko[y][x]
                neko[y][x] = 0
                flg = True
    return flg

# 最上段に達したか調べる関数
def over_neko():
    for x in range(8):
        if neko[0][x] > 0:
            return True
    return False        # else省略

# 最上段にネコをセットする関数
def set_neko():
    for x in range(8):
        neko[0][x] = random.randint(0, difficulty)

# 影付きの文字列を表示する関数
def draw_txt(txt, x, y, siz, col, tg):
    fnt = ("Meiryo", siz, "bold")
    cvs.create_text(x+2, y+2, text=txt, fill="black", font=fnt, tag=tg)
    cvs.create_text(x, y, text=txt, fill=col, font=fnt, tag=tg)

# リアルタイム処理を行う関数
def game_main():
    global index, timer, score, hisc, difficulty, tsugi 
    global cursor_x, cursor_y, mouse_c
    if index == 0:      # タイトルロゴ
        draw_txt("ねこねこ", 312, 240, 100, "violet", "TITLE")
        cvs.create_rectangle(168, 384, 456, 456, fill="skyblue", width=0, tag="TITLE")
        draw_txt("Easy", 312, 420, 40, "white", "TITLE")
        cvs.create_rectangle(168, 528, 456, 600, fill="lightgreen", width=0, tag="TITLE")
        draw_txt("Normal", 312, 564, 40, "white", "TITLE")
        cvs.create_rectangle(168, 672, 456, 744, fill="orange", width=0, tag="TITLE")
        draw_txt("Hard", 312, 708, 40, "white", "TITLE")
        index = 1
        mouse_c = 0
    elif index == 1:     # タイトル画面　スタート待ち
        difficulty = 0
        if mouse_c == 1:
            if 168 < mouse_x and mouse_x < 456 and 384 < mouse_y and mouse_y < 456:
                difficulty = 4
            if 168 < mouse_x and mouse_x < 456 and 528 < mouse_y and mouse_y < 600:
                difficulty = 5
            if 168 < mouse_x and mouse_x < 456 and 672 < mouse_y and mouse_y < 744:
                difficulty = 6
        if difficulty > 0:
            for y in range(10):
                for x in range(8):
                    neko[y][x] = 0
            mouse_c = 0
            score = 0
            tsugi = 0
            cursor_x = 0
            cursor_y = 0
            set_neko()
            draw_neko()
            cvs.delete("TITLE")
            index = 2
    elif index == 2:    # 落下
        if drop_neko() == False:
            index = 3
        draw_neko()
    elif index == 3:    # 揃ったか
        check_neko()
        draw_neko()
        index = 4
    elif index == 4:     # 揃ったネコがあれば消す
        sc = sweep_neko()
        score += sc*difficulty*2
        if score > hisc:
            hisc = score
        if sc > 0:
            index = 2
        else:
            if over_neko() == False:
                tsugi = random.randint(1, difficulty)
                index = 5
            else:
                index = 6
                time = 0
        draw_neko()
    elif index == 5:    # マウス入力を待つ
        if 24 <= mouse_x and mouse_x < 24+72*8 and 24 <= mouse_y and mouse_y < 24+72*10:
            cursor_x = int((mouse_x-24) / 72)
            cursor_y = int((mouse_y-24) / 72)
            if mouse_c == 1:
                mouse_c = 0
                set_neko()
                neko[cursor_y][cursor_x] = tsugi
                tsugi = 0
                index = 2
        cvs.delete("CURSOR")
        cvs.create_image(cursor_x*72+60, cursor_y*72+60, image=cursor, tag="CURSOR")
        draw_neko()
    elif index == 6:    # ゲームオーバー
        timer += 1
        if timer == 1:
            draw_txt("GAME OVER", 312, 348, 60, "red", "OVER")
        if timer == 50:
            cvs.delete("OVER")
            index = 0
    cvs.delete("INFO")
    draw_txt("SCORE" + str(score), 160, 60, 32, "blue", "INFO")
    draw_txt("HISC" + str(hisc), 450, 60, 32, "yellow", "INFO")
    if tsugi > 0:
        cvs.create_image(752, 128, image=img_neko[tsugi], tag="INFO")
    root.after(100, game_main)

root = tkinter.Tk()
root.title("落ちものパズル「ねこねこ」")
root.resizable(False, False)
root.bind("<Motion>", mouse_move)
root.bind("<ButtonPress>", mouse_press)
cvs = tkinter.Canvas(root, width=912, height=768)
cvs.pack()

bg = tkinter.PhotoImage(file="neko_bg.png")
cursor = tkinter.PhotoImage(file="neko_cursor.png")
img_neko = [
        None,
        tkinter.PhotoImage(file="neko1.png"),
        tkinter.PhotoImage(file="neko2.png"),
        tkinter.PhotoImage(file="neko3.png"),
        tkinter.PhotoImage(file="neko4.png"),
        tkinter.PhotoImage(file="neko5.png"),
        tkinter.PhotoImage(file="neko6.png"),
        tkinter.PhotoImage(file="neko_niku.png")
        ]

cvs.create_image(456, 384, image=bg)
game_main()
root.mainloop()

