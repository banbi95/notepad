import datetime
import re
import string
import tkinter
import webbrowser
import PySimpleGUI as sg
from zhon import hanzi

from SimpleText import gui


def new_file(window):
    window['-ML-'].update("")
    window['-INFO-'].update("新文档-未保存")


def open_file(window):
    file_name = sg.popup_get_file("请选择文档", title="选择文档", no_window=True)
    if file_name:  # 只有文件名非空才执行后续操作
        try:
            with open(file_name, mode="r", encoding="utf-8") as f:
                window['-ML-'].update(f.read())
                window['-INFO-'].update(file_name)
        except Exception as e:
            sg.popup("错误信息：{}".format(e))


def new_win(location):
    new_location = (location[0] + 50, location[1] + 50)  # 读取原来窗口的左上角坐标元组，x,y各加50产生偏移量，使用户容易识别出新窗口
    return gui.make_win(location=new_location)


def save_file(window, values):
    file_str = values['-ML-']
    file_name = window['-INFO-'].get()  #
    if file_name.startswith("新文档-未保存") or file_name == "":
        save_file_as(window, values)
    else:
        try:
            with open(file_name, mode="w", encoding="utf_8") as f:
                f.write(file_str)
                window['-SAVE INFO-'].update("已保存于{}".format(datetime.datetime.now().strftime("%Y%m%d %H:%M")))
        except Exception as e:
            sg.popup_error("错误信息：{}".format(e))


# 用于更改保存路径 或者更改保存名字
def save_file_as(window, values):
    file_str = values['-ML-']
    file_name = sg.popup_get_file("另存为", save_as=True, default_extension=".txt", file_types=(("文档类型(.txt)", "*.txt"),),
                                  keep_on_top=True, no_window=True, modal=True)  # 添加no_window参数后 没有中间窗口 但是 独占特性会消失
    if file_name:
        try:
            with open(file_name, mode="w", encoding="utf-8") as f:
                f.write(file_str)
        except Exception as e:
            print("错误信息：{}".format(e))
        else:
            window['-INFO-'].update(file_name)
            window['-SAVE INFO-'].update("已保存于{} ".format(datetime.datetime.now().strftime("%Y%m%d %H:%M")))


def print_file():
    pass


def find_str(str: str):
    pass


def replace_str(window, old_str: str, new_str: str) -> bool:
    text: str = window['-ML-'].get()
    if text.find(old_str) != -1:
        window['-ML-'].update(text.replace(old_str, new_str))
        return True
    else:
        return False


def do_clicpboard_operation(event, window: sg.Window, element: sg.Multiline):
    if event in ('撤销', 'z:90'):  # todo 撤销无效
        try:
            # element.Widget.edit_undo()
            window['-ML-'].Widget.edit_undo()
        except Exception as e:
            print(f"撤销操作失败{e}")
        print('did')
    elif event == '剪切':
        try:
            text = element.Widget.selection_get()
            window.TKroot.clipboard_clear()  # 清空当前剪贴板
            window.TKroot.clipboard_append(text)  # 将剪切内容附加到剪贴板
            element.Widget.delete(tkinter.SEL_FIRST, tkinter.SEL_LAST)  # 删除选中文档
        except:
            print("未选中")
    elif event == '复制':
        text = element.Widget.selection_get()
        window.TKroot.clipboard_clear()
        window.TKroot.clipboard_append(text)
    elif event == '粘贴':
        element.Widget.insert(sg.tk.INSERT, window.TKroot.clipboard_get())
    else:
        element.Widget.tag_add('sel', '1.0', 'end')  # todo 全选文本？？


def count_words(values):
    text = values['-ML-']
    text_lst = [t for t in text if t not in ('\n', ' ')]
    pure_text_lst = [t for t in text if t not in string.punctuation and t not in hanzi.punctuation and t != ' ']
    words_num_with_punc = len(text_lst)
    words_num = len(pure_text_lst)
    message = "字数（包含标点符号）：{0}\n字数（不包含标点符号）：{1}"
    sg.popup(message.format(words_num_with_punc, words_num), title="统计字数")


def add_time_mark(mainwindow):
    formated_time = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    # sg.cprint(formated_time,font='Arial',end=' ',window=mainwindow)       # 通过打印方式添加时间信息到文本末尾
    # mainwindow['-ML-'].update(formated_time,text_color_for_value='yellow',append=True)  # 将带格式的时间信息附着到文档末尾
    mainwindow['-ML'].Widget.insert(sg.tk.INSERT, formated_time)  # 将当时间信息 插入到光标处


def check_help():
    webbrowser.open('https://github.com/banbi95/bilibili-android-client')
