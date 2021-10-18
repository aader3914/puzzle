# -*- coding: utf-8 -*-
'''
將圖片填充為正方形圖片, 在依需求分割成 level x level 個小圖
'''
from PIL import Image

class split_image:
  def __init__(self, img_path="img/demo.jpg", level=3):
    self.__img_path = img_path
    self.__level = level
    self.__size = -1  # 原圖形需要 resize 的尺寸, < 10 則不要 resize
    self.__message = ""
    self.__image = None
    self.__image_list = []

  def set_imgpath(self, img_path):
    self.__img_path = img_path

  def set_level(self, level):
    self.__level = level
 
  def get_level(self):
    return self.__level

  def set_resize(self, mysize):
    self.__size = mysize

  def set_master_image(self, input_img):
    self.__image = input_img

  def get_master_image(self):
    return self.__image

  def get_split_image_list(self):
    return self.__image_list

  def get_message(self):
    return self.__message

  def load_image(self):
    '''
    由設定的檔案路徑及檔名, 讀取圖檔
    並存入 __image 內, 若存檔失敗, 則傳回 False 值
    '''
    print("  >> load_image : ", self.__img_path)
    ok=False  
    try:
      self.__image = Image.open(self.__img_path)
      ok=True
    except FileNotFoundError:
      self.__message = "Image File Not Found!"
    except:
      self.__message = "Load Image Error!" 
    return ok

  # 將圖片調整為正方形
  def __square_img(self):
    img = self.__image
    width, height = img.size
    if width == height:
      return
    # 以長寛的最大值為新圖片的長寛值(長=寛)
    new_image_length = width if width > height else height
    # 產生白底新圖片
    new_image = Image.new(img.mode, (new_image_length, new_image_length), color='white')
    # 將原圖貼在白底圖蝁中間
    if width > height:
      new_image.paste(img, (0, int((new_image_length - height) / 2)))
    else:
      new_image.paste(img, (int((new_image_length - width) / 2),0))
    
    self.__image = new_image

  def __split_img(self):
    '''
    分割圖片, 分割後的圖片存入 __image_list
    '''
    width, height = self.__image.size
    item_width = int(width / self.__level)
    box_list = []
    # (left, upper, right, lower)
    for i in range(0,self.__level):
      for j in range(0,self.__level):
        #print((i*item_width,j*item_width,(i+1)*item_width,(j+1)*item_width))
        box = (j*item_width,i*item_width,(j+1)*item_width,(i+1)*item_width)
        box_list.append(box)

    self.__image_list = [self.__image.crop(box) for box in box_list]

   # 將分割後圖片存入檔案內
  def save_images(self):
    index = 1
    for image in self.__image_list:
      image.save('./result/python'+str(index) + '.png', 'PNG')
      index += 1

  def set_split_image_from_load_file(self):
    '''
    從由檔案讀取圖片開始, 一直處理到分割圖片
    若完成則回傳 True, 否則回傳 False 
    '''
    isok = self.load_image()
    print("load image : ", isok)
    if isok:
      # self.__square_img()
      if self.__size > 10:
        self.__image = self.__image.resize((self.__size, self.__size))
      self.__split_img()
    return isok

  def set_split_image_from_master_image(self):
    '''
    直接由主圖片進行圖片分割作業(無回傳值) 
    '''
    # self.__square_img()
    if self.__size > 10:
      self.__image = self.__image.resize((self.__size, self.__size))
    self.__split_img()

if __name__ == '__main__':
  # Test default
  x =  split_image()
  x.set_resize(480)
  isok = x.set_split_image_from_load_file()
  print("isok : ", isok)
  if isok:
    imglist = x.get_split_image_list()
    print(">>> image list :\n", imglist)
  else:
    print(x.get_message())
  # x.save_images()
  print(" == End of job ===")
