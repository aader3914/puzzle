'''
智慧拼圖遊戲
功能 : 
  提供 3x3, 4x4, 5x5, 6x6 等四種層級的拼圖
  提供開啟檔案功能, 以利讀取圖檔, 建立新拼圖
'''
import tkinter as tk  # 使用Tkinter前需要先匯入
from tkinter import Button
from tkinter import messagebox
from tkinter import ttk as ttk
from tkinter import filedialog
from tkinter import font as tkFont
from PIL import ImageTk, Image
from img_split import split_image 
from puzzle import puzzle

puzzle_obj = puzzle()       # 建立 puzzle 物件
split_img =  split_image()  # 建立 split_image 物件
# 建立最大拼圖的圖片 id 編號
pic_list = ["pic00","pic01","pic02","pic03","pic04","pic05",
            "pic06","pic07","pic08","pic09","pic10","pic11",
            "pic12","pic13","pic14","pic15","pic16","pic17",
            "pic18","pic19","pic20","pic21","pic22","pic23",
            "pic24","pic25","pic26","pic27","pic28","pic29",
            "pic30","pic31","pic32","pic33","pic34","pic35" ]
lbl_puzzle_list=[]  # 放置拼圖片的 list (拼圖片是使用 label 元件)
piece_image_tk=[]         # 放置 tkinter 格式圖片的 list
position_xy_list=[] # 放置每片拼圖 [啟始位置] 的 list, 元素為 (x,y) 的數組
position_list=[]    # 放置拼圖的 list, 索引(key)代表位置, 內容(value)則代表拼圖編號

step=0   # 行走步數
level = 3 # 設定層級
max_piece = level * level # 該層級時最大拼圖數量
last_piece = max_piece    # 該層級時最後一片拼圖的編號
puzzle_complete = False   # 是否完成拼圖

image_width = 480    # 視窗內拼圖圖片的尺寸
gap = 5              # 位移量

## callback function
# 點擊拼圖片的事件處理
def img_click(event):
  global step, lbl_step_count
  print(" puzzle_complete : ", puzzle_complete)
  if not puzzle_complete:
    # cget('text') 取得 button  內 text 的字串
    btn_text = event.widget.widgetName
    print("widgetName : ", btn_text)
    # 取得按鍵圖片的 ID 編號
    btn_id=int(btn_text.replace("pic",""))
    print("btn_id : ", btn_id)
    move_to = puzzle_obj.move_it(btn_id)
    print("move_to : ", move_to)
    if move_to >= 0:
      step = step + 1
      lbl_step_count.config(text = step)
      # 將按鍵圖片移到新位置
      new_x, new_y = position_xy_list[move_to]   
      lbl_puzzle_list[btn_id].place(x=new_x, y=new_y)
      if puzzle_obj.is_complete():
        do_complete()
    print("__piece_list", puzzle_obj.get_piece_list())

# 點擊其他元件的事件處理
def callbackFunc(event):
  global step, lbl_step_count, puzzle_complete
  print("event.widgetName : ", event.widget.widgetName)
  if event.widget.widgetName == 'btn_restart' :
    print(">>> Is btn_restart click") 
    step=0
    lbl_step_count.config(text = step)
    reset_puzzle() 

  elif event.widget.widgetName == 'btn_download' :
    print(">>> Is btn_download click") 
    file_path = filedialog.askopenfilename(title='開啟影像檔', initialdir='~/',
      filetypes = (("image files","*.jpg *.png *.bmp"),("all files","*.*")))
    if not file_path:
      print('file path is empty')
    else:
      print(file_path)
      try:
        global  tk_image
        new_image = Image.open(file_path)
        split_img.set_master_image(new_image)
        set_demo_img()
        set_puzzle_img()
        put_image2puzzle()
        step=0
        lbl_step_count.config(text = step) 
        puzzle_complete = False       
      except:
        print("file open error.") 
  else :
    print("Other widget ")

# 下拉選單的事件處理
def opt_callback(*args): 
  global level, step, puzzle_complete
  sel_text = variable.get()
  if sel_text == "3 x 3":
    sel_id = 3
  if sel_text == "4 x 4":
    sel_id = 4
  if sel_text == "5 x 5":
    sel_id = 5
  if sel_text == "6 x 6":
    sel_id = 6
  
  if sel_id != level:
    level = sel_id
    # 設定圖片分割及拼圖物件內的 level 值
    puzzle_obj.set_level(level)
    split_img.set_level(level)

    set_puzzle_img()
    put_image2puzzle()
    step=0
    lbl_step_count.config(text = step)     
    puzzle_complete = False

# 完成拼圖時的處理事項
def do_complete():
  global puzzle_complete, lbl_puzzle_list
  print("## Puzzle is complete!")
  lbl_puzzle_list[last_piece].pack()
  col, row = position_xy_list[last_piece]
  lbl_puzzle_list[last_piece].place(x=col, y=row)
  puzzle_complete = True
  msg = "您移動 " + str(step) + " 步完成拼圖"
  messagebox.showinfo("訊息", msg)

def hide_last_piece():
  global lbl_puzzle_list, last_piece
  lbl_puzzle_list[last_piece].place(x=720, y=720)

def show_last_piece():
  global lbl_puzzle_list, last_piece
  col, row = position_xy_list(last_piece)
  lbl_puzzle_list[last_piece].place(x=col, y=row)


def set_demo_img():
  global  lbl_demo_image, demo_image_tk
  demo_image = split_img.get_master_image()
  demo_image = demo_image.resize((150,150))
  demo_image_tk = ImageTk.PhotoImage(demo_image)
  lbl_demo_image.config(image=demo_image_tk)

def set_puzzle_img():
  '''
  設定併圖圖片及每片拼圖格左上角位置
  '''
  global level, max_piece, last_piece, piece_image_tk, lbl_puzzle_list, position_xy_list
  level = puzzle_obj.get_level()
  split_img.set_level(level)
  max_piece = level * level
  last_piece = max_piece - 1
  piece_width = image_width // level
  print(" >> level : ", level," max_piece : ", max_piece," last_piece : ", last_piece)
  piece_image_tk.clear()
  position_xy_list.clear()

  split_img.set_split_image_from_master_image()
  piece_img = split_img.get_split_image_list()
  print(" >> piece_img :\n ", piece_img)
  for idx in range(0,36):
    if idx < max_piece:
      # 放置拼圖圖片 及 lbl_demo_image 尺寸
      piece_image_tk.append(ImageTk.PhotoImage(piece_img[idx]))
      lbl_puzzle_list[idx].config(image=piece_image_tk[idx])
      lbl_puzzle_list[idx].config(width=piece_width, height=piece_width)
      # 設定每片拼圖格左上角位置 
      col=(idx%level)*piece_width+gap
      row=(idx//level)*piece_width+gap
      position_xy_list.append((col, row))
    else:
      # 將圖片位置放到看不見的地方
      max_position = 720
      position_xy_list.append((max_position, max_position))

  print(" >> position_xy_list : \n", position_xy_list)  

def put_image2puzzle():
  global position_list, lbl_puzzle_list, last_piece
  position_list=puzzle_obj.get_random_piece_list()
  print(" >> position_list :", position_list)
  print(" >> pos_len = ", len(position_list), "max_piece = ", max_piece)
  for idx in range(0,36):
    if idx < max_piece:
      # 放置拼圖圖片 及 lbl_demo_image 尺寸
      piece_id=position_list[idx]
      if piece_id < 0:
        piece_id = last_piece
      col, row = position_xy_list[idx]
      print("## idx=", idx, "piece_id=", piece_id, "col=", col,"row=", row)
      lbl_puzzle_list[piece_id].place(x=col, y=row)
    else:
      col, row = position_xy_list[idx]
      print("## idx=", idx, "piece_id=", piece_id, "col=", col,"row=", row)
      lbl_puzzle_list[idx].place(x=col, y=row)
    # 隱藏最後一片拼圖  
    # lbl_puzzle_list[last_piece].pack_forget()
    hide_last_piece()
    puzzle_complete = False

def reset_puzzle():
  global puzzle_complete, lbl_puzzle_list, position_list, last_piece
  position_list=puzzle_obj.get_random_piece_list()
  for idx in range(0,max_piece):
    piece_id=position_list[idx]
    if piece_id < 0:
      piece_id = last_piece
    col, row = position_xy_list[idx]
    lbl_puzzle_list[piece_id].place(x=col, y=row)
  # 隱藏最後一片拼圖  
  print(" >> last_piece : ", last_piece)
  # lbl_puzzle_list[last_piece].pack_forget()
  hide_last_piece()
  puzzle_complete = False


###################
# 視窗程式開始
# 第1步，建立視窗 root 物件
root = tk.Tk()

# 第2步，設定視窗名稱
root.title('智慧拼圖')

# 第3步，設定視窗大小(長 * 寬)
root.geometry('680x540+30+30')  # 這裡的乘是小x
root.resizable(width=False, height=False) # 固定視窗尺寸

# 第4步，在圖形介面上建立畫布並放置各種元素
# canvas = tk.Canvas(root, bg='green', width=640, height=520)

## 建立基本元件
OptionList = ['3 x 3', '4 x 4', '5 x 5', '6 x 6']
helv18 = tkFont.Font(family='Helvetica', size=18, weight='bold')

# 步數文字提示
lbl_step = tk.Label(root,text='Step : ', font=helv18)
lbl_step.place(x=15, y=495)
# 步數計步器
lbl_step_count = tk.Label(root,text=step,font=helv18)
lbl_step_count.place(x=95, y=495)
# 拼圖的圖示
lbl_demo_image = tk.Label(root, width=150, height=150)
lbl_demo_image.place(x=500, y=10)

# 下拉選項(選取拼圖層級)
variable = tk.StringVar(root)
variable.set(OptionList[0])
variable.trace("w", opt_callback)
opt_levet = tk.OptionMenu(root, variable, *OptionList)
opt_levet.config(width=6, font=helv18)
opt_levet.widgetName = "opt_levet"
opt_levet.place(x=520, y=220)

# 讀取影像檔按鈕
btn_download = Button(root, text='讀影像檔', font=helv18,  width=8, height=1 )
btn_download.widgetName = "btn_download"
btn_download.bind('<Button-1>', callbackFunc)
btn_download.place(x=520, y=300)

# 重新開始按鈕
btn_restart = Button(root, text='重新開始', font=helv18,  width=8, height=1 )
btn_restart.widgetName = "btn_restart"
btn_restart.bind('<Button-1>', callbackFunc)
btn_restart.place(x=520, y=380)

## 將所有拼圖片的 label 放到 lbl_puzzle_list 內
lbl_puzzle_list.clear()
idx = 0
for piece_name in pic_list:
  lbl_puzzle_list.append(tk.Label(root))
  lbl_puzzle_list[idx].widgetName = piece_name
  lbl_puzzle_list[idx].bind('<Button-1>', img_click)
  idx = idx + 1

## 讀取 defaut 檔案
split_img.set_resize(480)
load_ok = split_img.load_image()
print(">>> load_ok : ", load_ok)
if load_ok:
  set_demo_img()
  set_puzzle_img()
  put_image2puzzle()
  puzzle_complete = False

 

# 第7步，主視窗迴圈顯示
root.mainloop()
