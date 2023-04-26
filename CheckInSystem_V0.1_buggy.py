# 整不明白，face_recognition装不上，换一个写
# json坏文明，用sqlite好了
# 此版本作废


import cv2
import cmake
# import face_recognition
import json
import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image


# 从外置的json文件中读取学生信息
with open("students.json", "r") as f:
    students = json.load(f)

# 课堂考勤类
class AttendanceSystem:

    # 初始化方法，创建图形界面和相关组件
    def __init__(self):
        # 创建主窗口
        self.window = tk.Tk()
        self.window.title("课堂考勤系统")
        self.window.geometry("800x600")

        # 标签，显示标题
        self.title_label = tk.Label(self.window, text="课堂考勤系统", font=("Arial", 24))
        self.title_label.pack()

        # 画布，显示摄像头内容和人脸检测结果
        self.canvas = tk.Canvas(self.window, width=400, height=300)
        self.canvas.pack(side=tk.LEFT)

        # 标签，显示人脸比对结果
        self.face_result_label = tk.Label(self.window, text="", font=("Arial", 16), fg="red")
        self.face_result_label.pack(side=tk.LEFT)

        # 按钮，启动摄像头和人脸检测功能
        self.start_button = tk.Button(self.window, text="启动摄像头", command=self.start_camera)
        self.start_button.pack(side=tk.LEFT)

        # 指纹图标，显示指纹检测结果
        self.fingerprint_icon = tk.Label(self.window, image=None)
        self.fingerprint_icon.pack(side=tk.RIGHT)

        # 标签，显示指纹比对结果
        self.fingerprint_result_label = tk.Label(self.window, text="", font=("Arial", 16), fg="red")
        self.fingerprint_result_label.pack(side=tk.RIGHT)

        # 按钮，启动指纹检测功能
        self.fingerprint_button = tk.Button(self.window, text="启动指纹传感器", command=self.start_fingerprint)
        self.fingerprint_button.pack(side=tk.RIGHT)

        # 列表框，显示学生信息
        self.listbox = tk.Listbox(self.window, width=40)
        self.listbox.pack()

        # 按钮，添加学生信息
        self.add_button = tk.Button(self.window, text="添加学生", command=self.add_student)
        self.add_button.pack()

        # 按钮，删除学生信息
        self.delete_button = tk.Button(self.window, text="删除学生", command=self.delete_student)
        self.delete_button.pack()

        # 按钮，修改学生信息
        self.modify_button = tk.Button(self.window, text="修改学生", command=self.modify_student)
        self.modify_button.pack()

        # 按钮，查看考勤信息
        self.check_button = tk.Button(self.window, text="查看考勤", command=self.check_attendance)
        self.check_button.pack()

    # 启动摄像头和人脸检测功能
    def start_camera(self):
        # 打开摄像头
        self.cap = cv2.VideoCapture(0)
        # 创建一个定时器，每隔50毫秒执行一次update方法
        self.timer = self.window.after(50, self.update)

    # 更新画布和人脸检测结果
    def update(self):
        # 从摄像头读取一帧图像
        ret, frame = self.cap.read()
        # 如果读取成功，继续处理
        if ret:
            # 将图像转换为RGB格式
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # 将图像转换为PIL格式，以便在画布上显示
            pil_frame = Image.fromarray(rgb_frame)
            # 将图像缩放到合适的大小
            pil_frame = pil_frame.resize((400, 300), Image.ANTIALIAS)
            # 将图像转换为Tkinter格式
            tk_frame = ImageTk.PhotoImage(pil_frame)
            # 在画布上显示图像
            self.canvas.create_image(0, 0, anchor=tk.NW, image=tk_frame)
            # 保持对图像的引用，防止被垃圾回收
            self.canvas.image = tk_frame
            # 使用face_recognition库检测人脸位置
            face_locations = face_recognition.face_locations(rgb_frame)
            # 如果检测到人脸，继续处理
            if face_locations:
                # 取第一个人脸的位置，画一个矩形框
                top, right, bottom, left = face_locations[0]
                self.canvas.create_rectangle(left, top, right, bottom, outline="green")
                # 从图像中截取人脸部分
                face_image = rgb_frame[top:bottom, left:right]
                # 使用face_recognition库提取人脸特征
                face_encoding = face_recognition.face_encodings(face_image)[0]
                # 遍历学生信息，比较人脸特征是否匹配
                for student in students:
                    # 如果人脸特征匹配，更新学生的考勤状态，并显示比对成功的信息
                    if face_recognition.compare_faces([student["face_encoding"]], face_encoding)[0]:
                        student["attendance"] = True
                        self.face_result_label.config(text="Success")
                        break
                else:
                    # 如果没有匹配的学生，显示比对失败的信息
                    self.face_result_label.config(text="Failure")
        # 重新启动定时器，继续执行update方法
        self.timer = self.window.after(50, self.update)

    # 启动指纹检测功能  写来玩玩，建议删掉
    def start_fingerprint(self):
        # 导入指纹传感器的库
        import fingerprint_sensor
        # 初始化指纹传感器
        self.sensor = fingerprint_sensor.FingerprintSensor()
        # 读取指纹图像
        fingerprint_image = self.sensor.read_image()
        # 如果读取成功，继续处理
        if fingerprint_image:
            # 将指纹图像转换为PIL格式，以便在指纹图标上显示
            pil_image = Image.fromarray(fingerprint_image)
            # 将指纹图像缩放到合适的大小
            pil_image = pil_image.resize((100, 100), Image.ANTIALIAS)
            # 将指纹图像转换为Tkinter格式
            tk_image = ImageTk.PhotoImage(pil_image)
            # 在指纹图标上显示指纹图像
            self.fingerprint_icon.config(image=tk_image)
            # 保持对图像的引用，防止被回收
            self.fingerprint_icon.image = tk_image
            # 使用指纹传感器的库提取指纹特征
            fingerprint_encoding = self.sensor.get_encoding(fingerprint_image)
            # 遍历学生信息，比较指纹特征是否匹配
            for student in students:
                # 如果指纹特征匹配，更新学生的考勤状态，并显示比对成功的信息
                if self.sensor.compare_encodings(student["fingerprint_encoding"], fingerprint_encoding):
                    student["attendance"] = True
                    self.fingerprint_result_label.config(text="Success")
                    break
            else:
                # 如果没有匹配的学生，显示比对失败的信息
                self.fingerprint_result_label.config(text="Failure")

    # 添加学生信息
    def add_student(self):
        # 创建一个子窗口
        self.add_window = tk.Toplevel(self.window)
        self.add_window.title("添加学生")
        self.add_window.geometry("400x300")
        # 创建一个标签，显示姓名
        self.name_label = tk.Label(self.add_window, text="姓名：")
        self.name_label.grid(row=0, column=0)
        # 创建一个输入框，输入姓名
        self.name_entry = tk.Entry(self.add_window)
        self.name_entry.grid(row=0, column=1)
        # 创建一个标签，显示学号
        self.id_label = tk.Label(self.add_window, text="学号：")
        self.id_label.grid(row=1, column=0)
        # 创建一个输入框，输入学号
        self.id_entry = tk.Entry(self.add_window)
        self.id_entry.grid(row=1, column=1)
        # 创建一个标签，显示人脸图片
        self.face_label = tk.Label(self.add_window, text="人脸图片：")
        self.face_label.grid(row=2, column=0)
        # 创建一个按钮，选择人脸图片
        self.face_button = tk.Button(self.add_window, text="选择图片", command=self.select_face_image)
        self.face_button.grid(row=2, column=1)
        # 创建一个标签，显示指纹图片
        self.fingerprint_label = tk.Label(self.add_window, text="指纹图片：")
        self.fingerprint_label.grid(row=3, column=0)
        # 创建一个按钮，选择指纹图片
        self.fingerprint_button = tk.Button(self.add_window, text="选择图片",command=self.select_fingerprint_image)
        self.fingerprint_button.grid(row=3, column=1)
        # 创建一个按钮，确认添加学生信息
        self.confirm_button = tk.Button(self.add_window, text="确认添加", command=self.confirm_add_student)
        self.confirm_button.grid(row=4, column=0, columnspan=2)

    # 选择人脸图片
    def select_face_image(self):
        # 使用文件对话框选择人脸图片的路径
        self.face_image_path = filedialog.askopenfilename(title="选择人脸图片", filetypes=[("PNG", ".png"), ("JPG", ".jpg")])
        # 如果选择了有效的路径，继续处理
        if self.face_image_path:
            # 打开人脸图片
            face_image = face_recognition.load_image_file(self.face_image_path)
            # 使用face_recognition库提取人脸特征
            face_encoding = face_recognition.face_encodings(face_image)[0]
            # 将人脸特征保存为属性
            self.face_encoding = face_encoding
            # 在按钮上显示已选择的图片路径
            self.face_button.config(text=self.face_image_path)

    # 选择指纹图片
    def select_fingerprint_image(self):
        # 使用文件对话框选择指纹图片的路径
        self.fingerprint_image_path = filedialog.askopenfilename(title="选择指纹图片", filetypes=[("PNG", ".png"), ("JPG", ".jpg")])
        # 如果选择了有效的路径，继续处理
        if self.fingerprint_image_path:
            # 打开指纹图片
            fingerprint_image = cv2.imread(self.fingerprint_image_path)
            # 使用指纹传感器的库提取指纹特征
            fingerprint_encoding = self.sensor.get_encoding(fingerprint_image)
            # 将指纹特征保存为属性
            self.fingerprint_encoding = fingerprint_encoding
            # 在按钮上显示已选择的图片路径
            self.fingerprint_button.config(text=self.fingerprint_image_path)

    # 确认添加学生信息
    def confirm_add_student(self):
        # 获取输入框中的姓名和学号
        name = self.name_entry.get()
        id = self.id_entry.get()
        # 如果姓名和学号都不为空，继续处理
        if name and id:
            # 创建字典，保存学生信息
            student = {
                "name": name,
                "id": id,
                "face_encoding": self.face_encoding,
                "fingerprint_encoding": self.fingerprint_encoding,
                "attendance": False
            }
            # 将学生信息添加到学生列表中
            students.append(student)
            # 在列表框中显示学生信息
            self.listbox.insert(tk.END, f"{name} {id}")
            # 关闭子窗口
            self.add_window.destroy()

    # 删除学生信息
    def delete_student(self):
        # 获取列表框中选中的学生索引
        index = self.listbox.curselection()
        # 如果有选中的学生，继续处理
        if index:
            # 从列表框中删除选中的学生
            self.listbox.delete(index)
            # 从学生列表中删除选中的学生
            students.pop(index[0])

    # 修改学生信息
    def modify_student(self):
        # 获取列表框中选中的学生索引
        index = self.listbox.curselection()

        # 如果有选中的学生，继续处理
        if index:
            # 获取选中的学生信息
            student = students[index[0]]
            # 创建一个子窗口
            self.modify_window = tk.Toplevel(self.window)
            self.modify_window.title("修改学生")
            self.modify_window.geometry("400x300")
            # 创建一个标签，显示姓名
            self.name_label = tk.Label(self.modify_window, text="姓名：")
            self.name_label.grid(row=0, column=0)
            # 创建一个输入框，输入姓名，初始值为原来的姓名
            self.name_entry = tk.Entry(self.modify_window)
            self.name_entry.insert(0, student["name"])
            self.name_entry.grid(row=0, column=1)
            # 创建一个标签，显示学号
            self.id_label = tk.Label(self.modify_window, text="学号：")
            self.id_label.grid(row=1, column=0)
            # 创建一个输入框，输入学号，初始值为原来的学号
            self.id_entry = tk.Entry(self.modify_window)
            self.id_entry.insert(0, student["id"])
            self.id_entry.grid(row=1, column=1)
            # 创建一个标签，显示人脸图片
            self.face_label = tk.Label(self.modify_window, text="人脸图片：")
            self.face_label.grid(row=2, column=0)
            # 创建一个按钮，选择人脸图片
            self.face_button = tk.Button(self.modify_window, text="选择图片", command=self.select_face_image)
            self.face_button.grid(row=2, column=1)
            # 创建一个标签，显示指纹图片
            self.fingerprint_label = tk.Label(self.modify_window, text="指纹图片：")
            self.fingerprint_label.grid(row=3, column=0)
            # 创建一个按钮，选择指纹图片
            self.fingerprint_button = tk.Button(self.modify_window, text="选择图片", command=self.select_fingerprint_image)
            self.fingerprint_button.grid(row=3, column=1)
            # 创建一个按钮，确认修改学生信息
            self.confirm_button = tk.Button(self.modify_window, text="确认修改", command=lambda: self.confirm_modify_student(index[0]))
            self.confirm_button.grid(row=4, column=0, columnspan=2)

    # 确认修改学生信息
    def confirm_modify_student(self, index):
        # 获取输入框中的姓名和学号
        name = self.name_entry.get()
        id = self.id_entry.get()
        # 如果姓名和学号都不为空，继续处理
        if name and id:
            # 修改学生信息
            students[index]["name"] = name
            students[index]["id"] = id
            students[index]["face_encoding"] = self.face_encoding
            students[index]["fingerprint_encoding"] = self.fingerprint_encoding
            # 在列表框中更新学生信息
            self.listbox.delete(index)
            self.listbox.insert(index, f"{name} {id}")
            # 关闭子窗口
            self.modify_window.destroy()

    # 查看考勤信息
    def check_attendance(self):
        # 遍历学生信息，统计考勤情况
        present_count = 0
        absent_count = 0
        for student in students:
            if student["attendance"]:
                present_count += 1
            else:
                absent_count += 1

        # 显示考勤情况的消息框
        tk.messagebox.showinfo("考勤情况", f"出勤人数：{present_count}\n缺勤人数：{absent_count}")

# 创建课堂考勤对象，并启动主循环
attendance_system = AttendanceSystem()
attendance_system.window.mainloop()