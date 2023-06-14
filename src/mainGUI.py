import subprocess
import tkinter as tk


def run_script(script_path):
    subprocess.Popen(['python', script_path])


def icon_double_clicked(event):
    icon_path = event.widget.cget('image')
    script_path = icon_to_script.get(icon_path)
    if script_path:
        run_script(script_path)


# 创建主窗口
window = tk.Tk()
window.title("GUI 示例")

# 定义图标和对应的脚本路径
icon_to_script = {
    "C:\\Users\\Rinkore\\Desktop\\MinecraftToolBox\\MinecraftToolBox\\src\\assets\\icon.png":
        "C:\\Users\\Rinkore\\Desktop\\MinecraftToolBox\\MinecraftToolBox\\src\\ServerStatusTest\Windows.py"
    # 添加更多的图标和脚本路径
}

# 创建图标并绑定双击事件
for icon_path in icon_to_script:
    image = tk.PhotoImage(file=icon_path)
    label = tk.Label(window, image=image)
    label.image = image
    label.pack()
    label.bind("<Double-Button-1>", icon_double_clicked)

# 运行主循环
window.mainloop()
