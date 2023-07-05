import cv2
import os
import sqlite3
import pyocr
import pyocr.builders
from PIL import Image


# 画像が格納されているディレクトリのパス
image_dir = 'image'
# 画像ファイルの拡張子
image_extensions = ['.jpg', '.jpeg', '.png']
# 画像ファイルのリストを取得
image_files = [file for file in os.listdir(image_dir) if os.path.splitext(file)[1].lower() in image_extensions]

# ジャケット画像が格納されているディレクトリのパス
template_dir = 'template'
# ジャケット画像ファイルのリストを取得
template_files = [file for file in os.listdir(template_dir) if os.path.splitext(file)[1].lower() in image_extensions]
# 2値化したジャケット画像を格納する辞書
template_mapping = {}

# 勝敗画像が格納されているディレクトリのパス
winlose_dir = 'winlose'
# 勝敗画像ファイルのリストを取得
winlose_files = [file for file in os.listdir(winlose_dir) if os.path.splitext(file)[1].lower() in image_extensions]

for template_file in template_files:
    #テンプレート画像のパスを作成
    template_path = os.path.join(template_dir, template_file)
    
    #テンプレート画像作成
    template = cv2.imread(template_path)
    template = cv2.resize(template, (248, 248))
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    template_binary = cv2.adaptiveThreshold(template_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 111, 4)
    template_mapping[template_file] = template_binary

# 画像ごとにループ処理
for image_file in image_files:
    # 画像のパスを作成
    image_path = os.path.join(image_dir, image_file)

    # 画像を読み込む
    img = cv2.imread(image_path)

    h,w,c = img.shape
    if w < 1318:
        continue
    
    img_gray = img[175:423, 1070:1318]
    img_gray = cv2.cvtColor(img_gray, cv2.COLOR_BGR2GRAY)
    img_binary = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 111, 4)

    for template_file in template_files:

        #類似部分枠付
        res = cv2.matchTemplate(img_binary, template_mapping[template_file], cv2.TM_CCOEFF_NORMED)
        _, maxVal, _, _, = cv2.minMaxLoc(res)
        if maxVal < 0.7:
            continue

        #sqlレコード用配列
        results = []
        music_name = os.path.splitext(template_file)[0]
        results.append(music_name.split(",")[0])

        #文字認識
        tools = pyocr.get_available_tools()
        tool = tools[0]
    
        #勝敗
        img_gray = img[259:364,164:478]
        img_gray = cv2.cvtColor(img_gray, cv2.COLOR_BGR2GRAY)
        img_binary = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 3, 20)

        for winlose_file in winlose_files:
            #勝敗画像のパスを作成
            winlose_path = os.path.join(winlose_dir, winlose_file)
            winlose_img = cv2.imread(winlose_path)
            winlose_gray = cv2.cvtColor(winlose_img, cv2.COLOR_BGR2GRAY)
            winlose_binary = cv2.adaptiveThreshold(winlose_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 3, 20)

            #勝敗をテンプレートマッチングで判定
            res = cv2.matchTemplate(img_binary, winlose_binary, cv2.TM_CCOEFF_NORMED)
            _, maxVal, _, _, = cv2.minMaxLoc(res)
            print(maxVal)
            if maxVal < 0.7:
                continue
            winlose_result = os.path.splitext(winlose_file)[0]
            results.append(winlose_result.split(".")[0])

        #内部
        for i in range(0, 5):
            img_gray = img[563 + 147 * i:619 + 147 * i, 762:932]
            img_gray = cv2.cvtColor(img_gray, cv2.COLOR_BGR2GRAY)
            _, img_binary = cv2.threshold(img_gray, 150, 255, cv2.THRESH_BINARY)

            str_img = Image.fromarray(img_binary)
            str_result = tool.image_to_string(str_img, lang='eng', builder=pyocr.builders.DigitBuilder(tesseract_layout=8))
            results.append(str_result)
        
        break
