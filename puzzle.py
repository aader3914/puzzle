import random
import math

class puzzle:
  '''
  用於建立拼圖, 並提供拼圖資訊及狀態等資料保存
  '''
  def __init__(self):    
    # __level 拼圖的階層數
    self.__level = 3
    # __piece_list 存放拼圖片的陣列
    #   陣列索引代表位置, 而其值則為拼圖片的編號
    #   當所有的索引位置均為相同編號的拼圖片時, 表完成併圖操作
    self.__piece_list = []

  def get_piece_list(self):
    return self.__piece_list

  def get_level(self):
    return self.__level

  def set_level(self, level):
    self.__level = level

  def is_neighbor(self, cell_A, cell_B):
    '''
    比較傳入的兩個位置, 在矩陣中是否相連
    cell_A, cell_B 是兩個位置的編號
    level 為矩陣的階層
    '''
    level = self.__level
    max_cell = level * level
    is_neighbor = False
    if not(cell_A == cell_B or cell_A >= max_cell or cell_B >= max_cell):
      cellA_x = cell_A % level
      cellA_y = cell_A // level
      cellB_x = cell_B % level
      cellB_y = cell_B // level
      if abs(cellA_x - cellB_x) + abs(cellA_y - cellB_y) == 1:
        is_neighbor = True    
    return is_neighbor

  def is_complete(self):
    is_ok =True
    for ii in range(0, len(self.__piece_list)-1):
      if self.__piece_list[ii] != ii :
        is_ok =False
        break
    return is_ok

  def get_click_piece_position_id(self, clickPiece):
    '''
    反查被點擊圖片所在位置
    傳回值為圖片所在位置, -1 表查不到對應位置
    '''
    pos = -1
    for ii in range(0, len(self.__piece_list)):
      if self.__piece_list[ii] == clickPiece:
        pos = ii 
        break	
    return pos

  def get_empty_piece_position_id(self):
    pos = -1
    for ii in range(0, len(self.__piece_list)):
      if self.__piece_list[ii] < 0:
        pos = ii 
        break	
    return pos

  def move_it(self,move_id):
    '''
    檢查要移動圖片ID的位置與空圖片位置是否相鄰
    若是-> 將圖片位置與空片位置交換, 並傳回空圖片位置的ID
    若否-> 不作任何事, 並傳回 -1 值
    '''
    new_id = -1
    piece_position = self.get_click_piece_position_id(move_id)
    empty_position = self.get_empty_piece_position_id()
    print("## piece_position : ", piece_position, "  empty_position :", empty_position)
    # 檢查要移動的圖片與空片位置是否相鄰
    if self.is_neighbor(piece_position, empty_position):
      self.__change_piece_position(piece_position, empty_position)
      new_id = empty_position
    return new_id

  def __change_piece_position(self, pos_A, pos_B):
    temp = self.__piece_list[pos_A]
    self.__piece_list[pos_A] = self.__piece_list[pos_B]
    self.__piece_list[pos_B] = temp

  def get_random_piece_list(self):
    '''
      get_puzzle_random_list :
      輸入值 : level 方陣的邊長
      回傳值 : 傳回 level x level 亂數序列, 但最後一個值以 -1 
              取代方陣的        
    '''
    # 設定數列長度
    level = self.__level
    total_piece = level*level
    piece_list = []
    # 產生一個 (數列長度 - 1) 的連續數列
    for ii in range(0,total_piece-1):
      piece_list.append(ii)
    # 陣列最後加入一個 -1 值(代表空缺)
    piece_list.append(-1) 
    print(piece_list)
    # 由尾端開始, 與產生的亂數值的位置交換內容, 而得到亂數陣列  
    for jj in range(total_piece-2,0, -1):
      rnd = random.randint(0,jj)
      temp = piece_list[jj]
      piece_list[jj] = piece_list[rnd]
      piece_list[rnd] = temp
      print("  >>> jj = ", jj, " rnd = ", rnd)
      print("  >>> piece_list : ", piece_list)
    
    print("#### piece_list : ", piece_list)

    '''
    # 判斷若奇偶數性若不相同, 則陣列要多做一次交換才能解出正確拼圖
    # if self.is_odd_arrangement(piece_list) != ((level-1)%2 == 1):
    if self.is_odd_arrangement(piece_list) :  
      print("#### Change once piece !")
      temp = piece_list[0]
      piece_list[0] = piece_list[1]
      piece_list[1] = temp
    '''
    # 判斷拼圖數列是否有解, 若無解則陣列要多做一次交換才能解出正確拼圖   
    if not self.isSolvable(piece_list) :  
      print("#### Change once piece !")
      temp = piece_list[0]
      piece_list[0] = piece_list[1]
      piece_list[1] = temp
    print("#### random piece_list : ", piece_list)
    self.__piece_list = piece_list 
    return piece_list

  def is_odd_arrangement(self, data_list):
    '''
    判斷數列是否為奇排列
    參考網址如下
    https://www.geek-share.com/detail/2689777161.html
    '''
    max_item = len(data_list)
    cnt = 0
    # 計算逆序數的總數
    # 數列最後一個為 -1 不納入計算
    for i in range(0, max_item-2):
      for j in range(0, max_item-1):
        if data_list[i] > data_list[j] :
          cnt=cnt+1
    print("  >>> cnt odd : ", cnt)
    return cnt%2==1  # 餘數為 1 表奇排列, 則傳回 True

  def isSolvable(self, data_list):
    '''
    判斷拼圖數列是否有解
    參考網址如下
    https://stackoverflow.com/questions/34570344/check-if-15-puzzle-is-solvable
    '''
    parity = 0
    max_item = len(data_list)
    gridWidth = int(math.sqrt(max_item))
    row = 0 # the current row we are on
    blankRow = 0 # the row with the blank tile
    
    for i in range(0, max_item):
      if i % gridWidth == 0:  # advance to next row
        row = row + 1
      if data_list[i] == -1 : # the blank tile
        blankRow = row # save the row on which encountered
        continue

      for j in range(i+1, max_item):
        if data_list[i] > data_list[j] and data_list[j] != -1:
          parity = parity + 1

    if gridWidth % 2 == 0 : # even grid
      if (blankRow % 2 == 0) : # blank on odd row; counting from bottom
        return parity % 2 == 0
      else : # blank on even row; counting from bottom
        return parity % 2 != 0
    else : # odd grid
      return parity % 2 == 0

if __name__ == '__main__':
  pp=puzzle()
  pp.set_level(4)
  mylist = pp.get_random_piece_list()
  print(pp.isSolvable(mylist))
  '''
  for i in range(0,8): 
    print("piece Id :", i)
    print(pp.move_it(i))
    print(pp.get_piece_list())
  '''
  
