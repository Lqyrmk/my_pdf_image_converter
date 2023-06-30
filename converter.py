import datetime
import os
import glob
import fitz  # pip install PyMuPDF


class Converter():

    def __init__(self):
        self.start_time = datetime.datetime.now()
        self.end_time = datetime.datetime.now()

    def pdf_to_image(self, pdf_name, pdf_path, images_path):
        """
        :Description: pdf_to_image 将一个pdf转换成一张或多张图片
        :Author: lym
        :Date: 2023/6/30 19:52
        :param pdf_name: 操作的pdf文件名
        :param pdf_path: 存放pdf的目录路径
        :param images_path 存放图片的目录路径
        :return None
        """
        # 开始时间
        self.start_time = datetime.datetime.now()

        print("pdf_path = " + pdf_path)
        print("pdf_name = " + pdf_name)

        pdf_doc = fitz.open(pdf_path + '/' + pdf_name)
        # 1.18.14版本用pageCount
        # 新版本用page_count
        for pg in range(pdf_doc.page_count):
            page = pdf_doc[pg]
            rotate = int(0)
            # x和y的值越大越清晰，图片越大，但处理也越耗时间，这里取决于你想要图片的清晰度
            # 默认为1.333333，一般日常使用3就够了，不能设置太大，太大容易使电脑死

            # 每个尺寸的缩放系数为1.3，这将为我们生成分辨率提高2.6的图像。
            # 此处若是不做设置，默认图片大小为：792X612, dpi=96

            # zoom_x = 1.33333333  # (1.33333333-->1056x816)   (2-->1584x1224)
            # zoom_y = 1.33333333
            zoom_x = 4
            zoom_y = 4
            # 1.18.14版本用preRotate
            # 新版本用prerotate
            mat = fitz.Matrix(zoom_x, zoom_y).prerotate(rotate)
            # 1.18.14版本用getPixmap
            # 新版本用get_pixmap
            pix = page.get_pixmap(matrix=mat, alpha=False)

            if not os.path.exists(images_path):  # 判断存放图片的文件夹是否存在
                os.makedirs(images_path)  # 若图片文件夹不存在就创建

            # 1.18.14版本用writePNG
            # 新版本用save
            pdf_name = os.path.splitext(pdf_name)[0]
            pix.save(images_path + '/' + pdf_name + '_images_%s.png' % pg)  # 将图片写入指定的文件夹内

        # 结束时间
        self.end_time = datetime.datetime.now()
        print('转换耗时 = ', (self.end_time - self.start_time).seconds)

    def image_to_pdf(self, images_path, pdf_path):
        """
        :Description: image_to_pdf 将一个目录下的图片按文件名顺序拼接成一个pdf
        :Author: lym
        :Date: 2023/6/30 19:51
        :param images_path: 存放图片的目录路径
        :param pdf_path: 存放pdf的目录路径
        :return None
        """
        # 开始时间
        self.start_time = datetime.datetime.now()

        pdf_doc = fitz.open()
        # 读取图片，确保按文件名排序
        for image_path in sorted(glob.glob(images_path + '/' + '*')):
            print(image_path)
            # 打开图片
            image_doc = fitz.open(image_path)
            # 使用图片创建单页的 PDF
            # 有的版本用convertToPDF
            pdf_bytes = image_doc.convert_to_pdf()
            image_pdf = fitz.open("pdf", pdf_bytes)
            # 将当前页插入文档
            # 有的版本用insertPDF
            pdf_doc.insert_pdf(image_pdf)

        # 取出文件名，去掉后缀名
        image_name = os.path.basename(image_path)
        image_name = os.path.splitext(image_name)[0]

        pdf_path = pdf_path + '/' + image_name + '_pdf' + '.pdf'

        # 保存pdf文件
        pdf_doc.save(pdf_path)
        pdf_doc.close()

        # 结束时间
        self.end_time = datetime.datetime.now()
        print('转换耗时 = ', (self.end_time - self.start_time).seconds)


if __name__ == "__main__":
    converter = Converter()

    # pdf转图片
    converter.pdf_to_image(pdf_name='2021大创证书.pdf', pdf_path='./pdf1', images_path='./img1')

    # 图片转pdf
    converter.image_to_pdf('./img2', './pdf2')
