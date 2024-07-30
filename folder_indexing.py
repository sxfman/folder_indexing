# coding: utf-8
import base64
import json
import os
import platform
import sys
import threading
import time
import webbrowser
from tkinter import Tk, ttk, Menu, Label, Entry, messagebox, Button, Text, END
from tkinter.filedialog import askdirectory


def OSVersion():
    try:
        OSv = platform.release()
    except:
        OSv = "0"
    if not OSv.isdigit():
        OSv = "0"
    print("操作系统版本号：", OSv)
    return OSv


def icoToPy(icoFilePath):
    with open(icoFilePath, "rb") as open_icon:  # 打开ICO格式的图标文件
        b64str = base64.b64encode(open_icon.read())  # 以base64的格式读出
        write_data = "img=%s" % b64str
        with open("ico.py", "w+") as f:  # 将上面读出的数据写入到名为“ico.py”的img数组中
            f.write(write_data)
            f.close()
        open_icon.close()


class MyGui:
    def __init__(self, init_window_name, root_dir):
        self.root_dir = root_dir
        self.init_window_name = init_window_name
        self.version_info = "<br>Powered by 文件目录制作工具"
        self.menubar = Menu(self.init_window_name)
        self.topMenu = Menu(self.menubar, tearoff=False)
        self.topMenu.add_command(label="退出", command=self.__quit)
        self.menubar.add_cascade(label="文件", menu=self.topMenu)
        self.topMenu.add_separator()
        self.topMenu.add_command(label="关于", command=self.__about)
        self.init_window_name.config(menu=self.menubar)
        self.rootDir = Label(self.init_window_name, text="  待索引目录：", justify="right")
        self.rootDir.grid(row=1, column=1)
        self.input_rootDir = Entry(self.init_window_name, width=30)
        self.input_rootDir.grid(row=1, column=2)
        self.rootDir_button = Button(self.init_window_name, text="选择目录", bg="lightgray", width=8, height=1,
                                     command=self.__chooseRootDir, justify="right")
        self.rootDir_button.grid(row=1, column=3)
        self.saveDir = Label(self.init_window_name, text="  保存索引到：", justify="right")
        self.saveDir.grid(row=2, column=1)
        self.input_saveDir = Entry(self.init_window_name, width=30)
        self.input_saveDir.grid(row=2, column=2)
        self.saveDir_button = Button(self.init_window_name, text="选择目录", bg="lightgray", width=8, height=1,
                                     command=self.__chooseSaveDir, justify="right")
        self.saveDir_button.grid(row=2, column=3)
        self.rootName = Label(self.init_window_name, text="  标题名称：", justify="right")
        self.rootName.grid(row=3, column=1)
        self.input_rootName = Entry(self.init_window_name, width=30)
        self.input_rootName.grid(row=3, column=2)
        self.input_rootName.insert(0, "我的目录")
        self.authorName = Label(self.init_window_name, text="  作者：", justify="right")
        self.authorName.grid(row=4, column=1)
        self.input_authorName = Entry(self.init_window_name, width=30)
        self.input_authorName.grid(row=4, column=2)
        self.input_authorName.insert(0, "无名")
        self.stop_button = Button(self.init_window_name, text="停止", bg="lightblue", width=8, height=1,
                                  command=self.__stop, justify="right")
        self.stop_button.grid(row=3, column=3, rowspan=2)
        self.gen_button = Button(self.init_window_name, text="制作索引", bg="lightblue", width=8, height=1,
                                 command=self.__start, justify="right")
        self.gen_button.grid(row=3, column=3, rowspan=2)
        self.t2 = Label(self.init_window_name, text=" ", justify="right")  # 空行
        self.t2.grid(row=6, column=1)
        self.log = Text(self.init_window_name, width=50, height=10, bd=1)  # 日志文本框
        self.log.grid(row=7, column=1, columnspan=3)
        self.t2 = Label(self.init_window_name, text=" ", justify="right")  # 空行
        self.t2.grid(row=8, column=1)
        self.progressbar_one = ttk.Progressbar(self.init_window_name, length=400)
        self.progressbar_one.grid(row=9, column=1, columnspan=3)

    # 设置窗口
    def set_init_window(self):
        self.init_window_name.title("文件目录制作工具")  # 窗口名
        # self.init_window_name.geometry('850x750+200+2')  #窗口大小，+10 +10 定义窗口弹出时的默认展示位置
        # self.init_window_name["bg"] = "pink"             #窗口背景色，其他背景色见：blog.csdn.net/chl0000/article/details/7657887
        self.init_window_name.attributes("-alpha", 0.95)    #虚化，值越小虚化程度越高
        # 设置窗口大小
        width = 400
        if int(OSVersion()) >= 7:
            height = 308
        else:
            height = 300
        # 获取屏幕尺寸以计算布局参数，使窗口居屏幕中央
        screenwidth = self.init_window_name.winfo_screenwidth()
        screenheight = self.init_window_name.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - 50 - height) / 2)
        print(screenwidth, screenheight, alignstr)
        self.init_window_name.geometry(alignstr)
        self.__setIcon()
        self.init_window_name.protocol("WM_DELETE_WINDOW", self.__quit)

    def __quit(self):
        # self.init_window_name.quit()  # TK的退出方法，可能无法结束其他线程，所以还要想办法让其他所有线程结束。
        self.pause = True
        if messagebox.askokcancel("退出", "确认要退出？"):
            self.__stop(confirm=False)
        else:
            self.pause = False

    def __stop(self, confirm=True):
        self.pause = True
        if confirm:  # 点击退出按钮弹出对话框确认退出
            if messagebox.askokcancel("确认", "确认要终止当前操作？"):
                self.pause = False
                self.forceStop = True
                self.stop_button.grid_remove()
                self.gen_button.grid()
            else:
                self.pause = False
        else:  # 不确认直接退出
            self.pause = False
            self.forceStop = True
            self.init_window_name.after(200, self.init_window_name.quit())  # tk主线程不能用time.sleep()，否则会挂死整个进程
            '''
            暴力结束进程的方法非不得已不使用
            pid = os.getpid()
            os.popen('taskkill.exe /F /T /pid:' + str(pid))
            '''

    def __setIcon(self):
        from ico import img  # 从名为“ico.py”的文件中引入img数组
        tmpIcoPath = os.path.join(self.root_dir, "tmp.ico")
        print(tmpIcoPath)
        with open(tmpIcoPath, "wb+") as tmp:
            tmp.write(base64.b64decode(img))  # 写入到临时文件中
            self.init_window_name.iconbitmap(tmpIcoPath)  # 设置图标
            tmp.close()
        os.remove(tmpIcoPath)

    def __start(self):
        self.gen_button.grid_remove()
        self.stop_button.grid()
        self.nowTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.dirIndex = 0
        self.totalsize = 0
        self.dirNum = 0
        self.fileNum = 0
        self.pct = 0
        self.loopNumG = 0
        self.loopNumT = 0
        self.forceStop = False
        self.pause = False
        filePath = self.input_rootDir.get()
        savePath = self.input_saveDir.get()
        rootName = self.input_rootName.get()
        authorName = self.input_authorName.get()
        if self.__emptyInput("待索引目录", filePath) or self.__emptyInput("保存索引目录", savePath) or self.__emptyInput("标题名称", rootName) or self.__emptyInput(
                "作者信息", authorName):
            return
        else:
            self.start_bar_thread = threading.Thread(target=self.__progressbar, args=())
            self.start_bar_thread.start()
            self.mainThread = threading.Thread(target=self.__genHtmlIndex, args=(filePath, savePath, rootName, authorName))
            self.mainThread.start()

    def __progressbar(self):
        self.progressbar_one.config(maximum=100, value=0)
        self.barThread = threading.Thread(target=self.__showBar, args=())
        self.barThread.start()

    def __showBar(self):
        # 设置进度条
        # print("progress:", self.pct)
        if self.pct < 100 and not self.forceStop:
            self.progressbar_one['value'] = self.pct
            self.progressbar_one.after(200, self.__showBar)  # 经过200ms后再次调用__showBar方法
        else:
            print("thread_progressbar ended.")

    @staticmethod
    def __about():
        msg = \
            "文件目录制作小工具 v1.1\n" \
            "   1、把第一步统计目录数目和文件大小合并到第2步一次完成；\n" \
            "   2、优化文件大小统计和进度显示；\n" \
            "   3、点击停止按钮后所有动作暂停，点击取消后恢复；"
        messagebox.showinfo("关于", msg)

    def __emptyInput(self, inputTitle, inputVal):
        if inputVal is None or inputVal == "":
            messagebox.showerror("错误：", inputTitle + "为空或非法！")
            self.stop_button.grid_remove()
            self.gen_button.grid()
            return True
        else:
            return False

    def __formatSize(self, totalSize, opt="f"):
        size = ""
        if opt == "f":  # 把数字格式化为逗号分隔的形式
            size = "{:,}".format(totalSize)
        if opt == "u":  # 把数字格式化为“k/M/G/T”
            if totalSize < 1000:
                size = str(round(totalSize, 0))
            elif 1000 <= totalSize < 1000000:
                size = str(round(totalSize / 1024.0, 2)) + "K"
            elif 1000000 <= totalSize < 1000000000:
                size = str(round(totalSize / 1024.0 / 1024.0, 2)) + "M"
            elif 1000000000 <= totalSize < 1000000000000:
                size = str(round(totalSize / 1024.0 / 1024.0 / 1024.0, 2)) + "G"
            else:
                t = round(totalSize / 1024.0 / 1024.0 / 1024.0 / 1024.0, 2)
                size = self.__formatSize(t) + "T"
        return str(size)

    def __chooseRootDir(self):
        self.input_rootDir.delete(0, END)
        _path = askdirectory()
        self.input_rootDir.insert(0, _path)
        if self.input_saveDir.get() is None or self.input_saveDir.get() == "":
            self.input_saveDir.insert(0, _path)

    def __chooseSaveDir(self):
        self.input_saveDir.delete(0, END)
        _path = askdirectory()
        self.input_saveDir.insert(0, _path)

    def __traversalDir(self, dirPath, rIndex):
        if not self.forceStop:
            while self.pause:
                time.sleep(0.1)
                continue
            self.loopNumT += 1
            rIndex["SubDirs"] = []
            if self.pct < 60:
                self.pct += 0.0001
            if os.path.isdir(dirPath):
                if not self.forceStop:
                    dfs = os.listdir(dirPath)
                else:
                    return
                i = 0
                for df in dfs:
                    if not self.forceStop:
                        while self.pause:
                            time.sleep(0.1)
                            continue
                        dirPath_t = os.path.join(dirPath, df)
                        if os.path.isdir(dirPath_t):
                            self.dirNum += 1
                            index_t = {"dirName": df, "dirURL": dirPath_t, "hasSubDirs": "true"}
                        elif os.path.isfile(dirPath_t):
                            try:
                                filesize = os.path.getsize(dirPath_t)  # 如果是文件，则获取相应文件的大小
                                self.totalsize += filesize
                            except Exception as e:
                                # self.stop_button.grid_remove()
                                # self.gen_button.grid()
                                print("line-265:", e)
                            self.fileNum += 1
                            index_t = {"dirName": df, "dirURL": dirPath_t, "hasSubDirs": "false"}
                        rIndex["SubDirs"].append(index_t)
                        try:  # 递归处理，如果是目录则继续递归子目录，如果是文件直接附加空子目录结束递归
                            self.__traversalDir(dirPath_t, rIndex["SubDirs"][i])
                        except Exception as e: # 针对无法访问的系统隐藏文件夹（比如“System Volume Information”）直接跳过
                            print("line-272:", e)
                        i += 1
                    else:
                        return
                if self.loopNumT % 10 == 0:  # 在软件界面文本框中抽样打印进度信息
                    if self.forceStop:
                        return
                    self.log.delete("3.0", "end")
                    self.log.insert("end", "\n")
                    self.log.insert("end", "遍历目录：" + str(dirPath) + "\n")
                    self.log.delete("5.0", "end")
                    self.log.insert("end", "\n")
                    self.log.insert("end", "目录总数：" + str(self.__formatSize(self.dirNum)) + "，文件总数：" + str(
                        self.__formatSize(self.fileNum)) + "\n总大小：" + str(
                        self.__formatSize(self.totalsize, "u")) + "B（" + str(
                        self.__formatSize(self.totalsize)) + "Bytes）\n")
                self.loopNumT = 1
            return rIndex
        else:
            return

    def __outHtmlTable(self, strDict, seq):
        if not self.forceStop:
            while self.pause:
                time.sleep(0.1)
                continue
            if self.pct < 90:
                self.pct += 0.00001
            if isinstance(strDict, dict):
                if strDict["hasSubDirs"] == "true":
                    self.dirIndex += 1
                    seq.append('<tr><td width=20></td><td>◆<a  href="javascript:goit(ML' + str(
                        self.dirIndex) + ')" onmousemove=showtip(1,1) onmouseout=showtip(1,0)>' + strDict[
                                   "dirName"] + '</a> [<a href="' + strDict[
                                   "dirURL"] + '" onmousemove=showtip(2,1) onmouseout=showtip(2,'
                                               '0) target=_blank>打开</a>]</td></tr><tr><td width=20></td><td>\r\n')
                    seq.append('<table width=100%  border="0" name="ML" id="ML' + str(
                        self.dirIndex) + '" style="display:\'none\';">\r\n')
                    for d in strDict["SubDirs"]:
                        self.__outHtmlTable(d, seq)
                    seq.append('</table>\r\n')
                else:
                    seq.append('<tr><td width=22></td><td>├┈<a href="' + strDict[
                        "dirURL"] + '" onmousemove=showtip(3,1) onmouseout=showtip(3,0) class=a02 target=_blank>' +
                               strDict["dirName"] + '</a></td></tr>\r\n')
                    if len(strDict["SubDirs"]) > 0:
                        for d in strDict["SubDirs"]:
                            self.__outHtmlTable(d, seq)
            return seq
        else:
            return

    def __genHtmlIndex(self, filePath, savePath, dirName, author):  # 制作目录索引的动作
        self.log.delete("1.0", "end")
        self.log.insert("end", "待制作索引的目录：" + filePath + "\n")
        try:
            rIndex = {}
            r = self.__traversalDir(filePath, rIndex)
            if not self.forceStop:
                while self.pause:
                    time.sleep(0.1)
                    continue
                # 前面打印的文件和目录大小、数目统计信息是抽样的，这里补一个100%统计完成的结果
                self.log.delete("3.0", "end")
                self.log.insert("end", "\n")
                self.log.insert("end", "目录总数：" + str(self.__formatSize(self.dirNum)) + "，文件总数：" + str(
                    self.__formatSize(self.fileNum)) + "\n总大小：" + str(
                    self.__formatSize(self.totalsize, "u")) + "B(" + str(
                    self.__formatSize(self.totalsize)) + "Bytes)\n")
                time.sleep(1)
                self.pct = 60
                self.log.insert("end", "目录和文件清单统计完成...\n\n")
                r["dirName"] = dirName
                r["dirURL"] = "./"
                r["hasSubDirs"] = "true"
                r1 = json.dumps(r, sort_keys=True, indent=2, separators=(',', ':'), ensure_ascii=False)
                # print(r1)
            else:
                print("thread_genHtmlIndex killed.")
                return
        except Exception as e:
            messagebox.showerror("错误：", "请确认要制作索引的目录是否正确！")
            self.log.insert("end", str(e))
            self.stop_button.grid_remove()
            self.gen_button.grid()
        else:
            if not self.forceStop:
                while self.pause:
                    time.sleep(0.1)
                    continue
                time.sleep(1)
                self.log.insert("end", "生成HTML模板...\n")
                seq = []
                seq_body = self.__outHtmlTable(r, seq)
                time.sleep(2)
                self.pct = 90
                # print(outHtml)
                self.log.delete("7.0", "end")
                self.log.insert("end", "\nHTML模板创建完成...\n\n")
                seq_head = [
                    "<html>\r\n",
                    "<head>\r\n",
                    " <meta charset='utf-8'/>\r\n"
                    " <title>" + dirName + "</title>\r\n",
                    "<STYLE>A:link {TEXT-DECORATION:underline;COLOR: #000000; FONT-SIZE: 11pt;} A:visited {"
                    "TEXT-DECORATION:none;COLOR: #000000; FONT-SIZE: 11pt;} A:active {"
                    "TEXT-DECORATION:none;COLOR:#000099;FONT-SIZE:11pt;} A:hover {"
                    "TEXT-DECORATION:none;COLOR:#cc0000;FONT-SIZE:11pt} A.a02:link {"
                    "TEXT-DECORATION:none;FONT-SIZE:10pt;} A.a02:visited {"
                    "TEXT-DECORATION:none;color:#666666;FONT-SIZE:10pt;} A.a02:active {"
                    "TEXT-DECORATION:none;FONT-SIZE: 10pt;} A.a02:hover{text-decoration:underline;FONT-SIZE: 10pt;} "
                    "</STYLE>\r\n",
                    "</head>\r\n",
                    "<script language='JavaScript'>function goit(o){if (o.style.display=='none') o.style.display=''; "
                    "else o.style.display='none';}\r\n",
                    "function foldAll(){window.location.reload; var trees = document.getElementsByName('ML');for (var "
                    "i=0; i<trees.length; i++){trees[i].style.display='none';}}\r\n",
                    "function showAll(){window.location.reload; var trees = document.getElementsByName('ML');for (var "
                    "i=0; i<trees.length; i++){trees[i].style.display='';}}\r\n",
                    'function showtip(url,flag){var my_tips=document.all.mytips;if(flag){my_tips.style.display="";if '
                    '(url==1) tips="&nbsp;展开/收缩该目录内容"; else if(url==2) tips="&nbsp;打开该文件夹"; else tips="&nbsp;打开该文件"; '
                    'my_tips.innerHTML=tips;my_tips.style.left=event.clientX+11;my_tips.style.top=event.clientY+6;} '
                    'else my_tips.style.display="none"; }\r\n',
                    "</script>\r\n",
                    "<body>\r\n",
                    '<table width="95%" border="1" align="center" cellpadding="10" cellspacing="0" '
                    'bordercolor="#000000"><tr bordercolor="#FFFFFF"><td align="center" valign="bottom"><br><font '
                    'size=5><strong>' + dirName + '</strong></font>&nbsp;&nbsp;&nbsp;&nbsp;[<a onclick="foldAll('
                                                  ')">全部折叠</a>]/[<a onclick="showAll()">全部展开</a>]</font><hr size="1" '
                                                  'noshade></td></tr>\r\n',
                    '<tr bordercolor="#FFFFFF"><td>\r\n',
                    '<table width=100%  border="0">\r\n'
                ]
                seq_foot = [
                    "</table>\r\n",
                    "<tr bordercolor='#FFFFFF'><td>共计" + str(self.__formatSize(self.dirNum)) + "个目录，" + str(
                        self.__formatSize(self.fileNum)) + "个文件，大小" + str(
                        self.__formatSize(self.totalsize, "u")) + "B（" + str(self.totalsize) + "字节）。</td></tr>\r\n",
                    '<tr bordercolor="#FFFFFF"><td align="center"><hr size="1" noshade><font size=2 color="#333333">' + author + '<br>' + self.nowTime + self.version_info + '</font><br></td></tr>\r\n',
                    '</table><br>\r\n',
                    '<div id=mytips style="position:absolute;width:130;height:16;border:1 gray '
                    'solid;font-size:9pt;background-color:#ffffff;color:red;display:none;filter: '
                    'progid:DXImageTransform.Microsoft.Shadow(color=#999999,direction=135,strength=3);"></div><table '
                    'width="95%" border="0" align="center"><tr><td><font size=2 '
                    'color="#666666">说明:<br>1、点击各目录链接，可展开/收缩该目录。<br>2、点击文件链接，可以直接打开相应的文件。<br>3'
                    '、点击目录后面的“打开”链接，可以在新窗口中打开该目录，显示其中包含的所有子目录和文件列表。<br>4'
                    '、如果某个目录下的子目录和文件数量巨大，展开/收缩此目录可能需要很长时间，导致浏览器处于“假死”状态，请耐心等待，或者尽量避免此种操作。</font></td></tr></table>\r'
                    '\n',
                    '</body></html>'
                ]
                seq_head.extend(seq_body)
                seq_head.extend(seq_foot)
                time.sleep(1)
                self.log.insert("end", "生成HTML索引文件...\n")
                try:
                    htmlFilePath = os.path.join(savePath, "index.html")
                    with open(htmlFilePath, "w", encoding='utf-8') as f:
                        f.writelines(seq_head)
                except Exception as e:
                    print("line-366:", e)
                    messagebox.showerror("错误：", "请确认保存索引的目录是否正确！" + str(e))
                    self.log.insert("end", e)
                    self.stop_button.grid_remove()
                    self.gen_button.grid()
                else:
                    time.sleep(2)
                    self.pct = 99.99
                    self.log.delete("9.0", "end")
                    self.log.insert("end", "\nHTML索引文件创建成功...")
                    time.sleep(2)
                    self.pct = 100
                    print(htmlFilePath)
                    messagebox.showinfo("成功", "目录索引制作成功！索引文件保存在：" + htmlFilePath)
                    os.system("start " + savePath)
                    os.system(htmlFilePath)
                    # webbrowser.open_new_tab(htmlFilePath)
                    self.stop_button.grid_remove()
                    self.gen_button.grid()
            else:
                print("thread_genHtmlIndex killed.")
                return
        print("genHtmlIndex finished.")


def gui_start(root_dir):
    init_window = Tk()  # 实例化出一个父窗口
    init_window.resizable(False, False)
    window = MyGui(init_window, root_dir)
    # 设置根窗口默认属性
    window.set_init_window()
    init_window.mainloop()  # 父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示


if __name__ == "__main__":
    # icoToPy("ico.ico")  #这条命令在未打包前可以每次都运行，只要保证ico图标文件在相同目录下即可，但打包后，因为没有ico文件，所以要注释这条命令，但要保证打包前已经生成了“ico.py”文件
    root_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
    gui_start(root_dir)
