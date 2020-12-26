import datetime
import os

import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont
import qrcode
from PIL import Image as Image


# 生成文件夹
def mkdir(path):
    folder = os.path.exists(path)

    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        print("---  new folder...  ---")
        print("---  OK  ---")
    else:
        print("---  There is this folder!  ---")

# 生成一个带logo的二维码


def generateQRCode(url):
    # 初始化
    qr = qrcode.QRCode(
        version=5, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=8)
    # 添加内容
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image()
    img = img.convert("RGBA")

    # 读取logo
    icon = Image.open("assets/logo.jpg")
    # 设置logo
    img_w, img_h = img.size
    factor = 4
    size_w = int(img_w / factor)
    size_h = int(img_h / factor)

    icon_w, icon_h = icon.size
    if icon_w > size_w:
        icon_w = size_w
    if icon_h > size_h:
        icon_h = size_h
    icon = icon.resize((icon_w, icon_h), Image.ANTIALIAS)

    # 将logo并入原二维码中
    w = int((img_w - icon_w)/2)
    h = int((img_h - icon_h)/2)
    icon = icon.convert("RGBA")
    img.paste(icon, (w, h), icon)
    rgb_im = img.convert('RGB')

    # 保存到指定路径下
    today = datetime.date.today()
    folder_path = 'output/'+str(today)
    mkdir(folder_path)
    rgb_im.save(folder_path+'/qr.jpg')


class postMaker(object):
    def __init__(self, backImg, font):
        self.backImg = backImg
        self.font = font
        self.post = None

    def create(self, postPic, postTitle, qrImg, textColor):
        """
        @postPic: 文章封面图
        @postTitle 文章标题
        @qrImg: 文章二维码
        @textColor: 文字颜色，{R，G，B}
        """
        try:
            # 获取背景图
            backImg = Image.open(self.backImg)
            # 获取封面图
            postPic = Image.open(postPic)
            # 获取字体
            font = ImageFont.truetype(self.font, 24)

            postPic.thumbnail((600, 400))

            bg_w, bg_h = backImg.size
            pic_w, pic_h = postPic.size

            divisor = 0

            if pic_h < 100:
                divisor = 3.5
            elif pic_h >= 100 and pic_h < 300:
                divisor = 4
            else:
                divisor = 5
            # 将封面图粘贴到背景图的指定位置，第二个参数为坐标
            backImg.paste(postPic, ((bg_w-pic_w)//2,
                                    int((bg_h-pic_h)/divisor)))

            draw = ImageDraw.Draw(backImg)
            draw.ink = textColor.get(
                'R', 0) + textColor.get('G', 0) * 256 + textColor.get('B', 0)*256*256

            textWidth, textHeight = font.getsize(postTitle)

            draw.text([360-textWidth/2, 510], postTitle, font=font)

            qrImg = Image.open(qrImg)
            qrImg.thumbnail((240, 240))
            backImg.paste(qrImg, (240, 570))

            self.post = backImg

            today = datetime.date.today()
            folder_path = 'output/'+str(today)

            backImg.save(folder_path+'/post.jpg')
        except Exception as e:
            print(e)

# 生成海报


def generatePost(title):
    today = datetime.date.today()
    folder_path = 'output/'+str(today)

    backImg = 'assets/template.jpg'
    font = 'assets/msyhl.ttc'
    pMaker = postMaker(backImg=backImg, font=font)
    postPic = folder_path+'/postPic.png'

    qrImg = folder_path+'/qr.jpg'
    pMaker.create(
        postPic=postPic,
        postTitle=title,
        qrImg=qrImg,
        textColor={'R': 0, 'G': 0, 'B': 0})
    print('ok')


if __name__ == "__main__":
    url = 'https://www.toutiao.com/i6909853204687979011/'
    generateQRCode(url)
    # generatePost(get_title(url))
    generatePost("检测神经网络结构中的数值缺陷")
