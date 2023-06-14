from PIL import Image, ImageDraw, ImageFont


def generate_text_image(text, font_size=14, line_spacing=2, padding=20, background_color=(255, 255, 255),
                        text_color=(0, 0, 0)):
    # 加载字体
    font_path = "C:\\Users\\Rinkore\\Desktop\\MinecraftToolBox\\MinecraftToolBox\\src\\assets\\微软雅黑.ttf"
    font = ImageFont.truetype(font_path, font_size)

    # 处理文字
    lines = text.split('\n')
    max_line_width = max(font.getbbox(line)[2] - font.getbbox(line)[0] for line in lines)  # 获取最长行的宽度
    line_height = font_size + line_spacing
    image_width = max_line_width + padding  # 图片宽度根据文字长度设置
    image_height = len(lines) * line_height + padding  # 图片高度根据文字行数设置

    # 创建画布
    image = Image.new("RGB", (image_width, image_height), background_color)
    draw = ImageDraw.Draw(image)

    # 绘制文字
    x = padding
    y = padding
    for i, line in enumerate(lines):
        draw.text((x, y), line, font=font, fill=text_color)
        y += line_height

    return image


if __name__ == '__main__':
    # 长段文字
    text = u'''
    count: 10272
    和牌率: 0.28475467289719625
    自摸率: 0.4047863247863248
    默听率: 0.16615384615384615
    放铳率: 0.16004672897196262
    副露率: 0.23539719626168223
    立直率: 0.2875778816199377
    平均打点: 9942
    最大连庄: 7
    和了巡数: 11.44991452991453
    平均铳点: 9535
    流局率: 0.09452881619937695
    流听率: 0.49433573635427397
    一发率: 0.2237442922374429
    里宝率: 0.41682974559686886
    被炸率: 0.1344942571322712
    平均被炸点数: 11212
    放铳时立直率: 0.29744525547445255
    放铳时副露率: 0.2615571776155718
    立直后放铳率: 0.16553825321597834
    立直后非瞬间放铳率: 0.11780636425186188
    副露后放铳率: 0.17783291976840365
    立直后和牌率: 0.518957345971564
    副露后和牌率: 0.3746898263027295
    立直后流局率: 0.09004739336492891
    副露后流局率: 0.08229942100909843
    放铳至立直: 707
    放铳至副露: 684
    放铳至默听: 278
    立直和了: 1533
    副露和了: 906
    默听和了: 486
    立直巡目: 8.87914691943128
    立直收支: 3496
    立直收入: 10368
    立直支出: 10457
    先制率: 0.7288422477995937
    追立率: 0.2711577522004062
    被追率: 0.1905890318212593
    振听立直率: 0.01049424509140149
    立直好型: 0.6990521327014217
    立直多面: 0.6990521327014217
    立直好型2: 0.36594448205822616
    役满: 36
    累计役满: 14
    最大累计番数: 16
    W立直: 13
    打点效率: 2831
    铳点损失: 1526
    净打点效率: 1305
    平均起手向听: 3.282807632398754
    平均起手向听亲: 2.9789473684210526
    平均起手向听子: 3.4184300341296927
    '''

    # 生成图片
    image = generate_text_image(text)

    # 保存图片
    image.save("text_image.png")
