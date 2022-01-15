import tkinter.font

import PySimpleGUI
import PySimpleGUI as sg
import function


def make_win(theme=None, location=(500, 300)):
    if theme:
        sg.theme(theme)
    else:
        sg.theme(sg.user_settings_get_entry('default_theme'))

    # 定义菜单栏布局
    menu_def = [
        ["文件（&F)", ["新建(&N)        CTRL+N", "新窗口（&W)    CTRL+SHIFT+N", "打开(&O)     Ctrl+O", "保存     Ctrl+S",
                    "另存为(&A)   Ctrl+Shift+S", "页面设置(&U)", "打印    Ctrl+P", "退出(&X)"]],
        ["编辑(&E)",
         ["撤销 Ctrl+Z", "剪切     Ctrl+X", "复制     Ctrl+C", "粘贴     Ctrl+V", "删除     Del", "搜索    Ctrl+E",
          "查找     Ctrl+F",
          "!查找下一个(N)    F3", "!查找上一个(V)    Shift+F3", "替换    Ctrl+H", "!转到   Ctrl+G", "全选     Ctrl+A", "时间/日期   F5"]],
        ["格式(&O)", ["自动换行", "字体"]],
        ["工具(&T)", ["统计字数"]],
        ["查看(&V)", ["缩放", ["放大", "缩小", "恢复默认缩放"], "状态栏", "切换主题", ["默认", "随机主题 F5", "选择主题"]]],
        ["帮助(&H)", ["查看帮助", "发送反馈", "关于记事本"]]
    ]

    right_click_menu = ['&右键菜单', ['撤销', '剪切', '复制', '粘贴', '全选', '字数统计']]
    layout = [[sg.Menubar(menu_def)],
              [sg.Multiline(autoscroll=True, key="-ML-", expand_x=True, expand_y=True,
                            right_click_menu=right_click_menu, reroute_cprint=True, auto_refresh=True)],
              [sg.Text("", key="-INFO-"), sg.VSeparator(), sg.Text('', key='-SAVE INFO-'), sg.VSeparator(),
               sg.Text('', key='-COL ROW INFO-', visible=False)]

              ]
    window = sg.Window("记事本", layout=layout, resizable=True, margins=(0, 0), element_padding=(0, 0), finalize=True,
                       size=(809, 500), location=location,
                       return_keyboard_events=True, enable_close_attempted_event=True)
    return window


def rebuild_window(window, theme, location=None):
    info_list = [window['-ML-'].get(), window['-INFO-'].get(), window['-SAVE INFO-'].get()]  # 保存旧窗口对象中的信息到列表
    window.close()  # 销毁旧窗口对象
    window = make_win(theme, location)  # 使用当前主题创建新窗口对象
    window['-ML-'].update(info_list[0])  # 还原文本信息
    window['-INFO-'].update(info_list[1])  # 还原文件路径信息栏
    window['-SAVE INFO-'].update(info_list[2])  # 还原上次保存时间信息栏
    return window


def custom_quit_popup():
    layout = [
        [sg.T("当前有未保存的文档，确定要继续退出吗？")],
        [sg.Yes("确定", size=(10, 1)), sg.No("取消", size=(10, 1))]
    ]
    event, values = sg.Window('提示', layout=layout, disable_close=True, element_padding=(10, 10),
                              element_justification='center').read(close=True)
    return event


def make_page_setting_win():
    page_size_frame = [
        [sg.Text('大小:'), sg.Combo(['A3', 'A4'], expand_x=True, readonly=True)],
        [sg.Text('来源:', background_color='grey'), sg.Combo(["1", "2", "3"], disabled=True, expand_x=True)]
    ]
    direction_frame = [
        [sg.Radio("纵向", group_id="-Direct-")],
        [sg.Radio("横向", group_id="-Direct-")]

    ]
    margin_frame = [
        [sg.Text("左:"), sg.In(size=(10, 1)), sg.Text("右:"), sg.In(size=(10, 1))],
        [sg.Text("上:"), sg.In(size=(10, 1)), sg.Text("下:"), sg.In(size=(10, 1))],

    ]
    preview_frame = [[sg.Image("")]]

    left_col = [
        [sg.Frame(title="纸张", layout=page_size_frame, expand_x=True, pad=(10, 10))],
        [sg.Frame(title="方向", layout=direction_frame), sg.Frame(title="页边距(毫米）", layout=margin_frame)],
        [sg.Text("页眉:"), sg.Input(size=(10, 1), expand_x=True)],
        [sg.Text("页脚:"), sg.Input(size=(10, 1), expand_x=True)]
    ]
    right_col = [[
        sg.Frame(title="预览", layout=preview_frame, size=(250, 320))
    ]]
    layout = [
        [sg.Column(layout=left_col, expand_y=True, background_color='white'),
         sg.Column(layout=right_col, expand_y=True, background_color='white')],
        [sg.Text("输入值"), sg.Button("确定", key='-OK-'), sg.Button("取消", key='-CANCEL-')],
    ]
    page_setting_win = sg.Window(title="页面设置", layout=layout, modal=True, size=(650, 450),
                                 element_padding=(10, 10), margins=(10, 10))
    while True:
        event, value = page_setting_win.read(timeout=100)
        if event == sg.WIN_CLOSED:
            break
    page_setting_win.close()


def make_print_page_win():
    printer_list = ("打印机1", "打印机2", "打印机3")
    choose_printer_frame = [
        [sg.Listbox(values=printer_list, expand_x=True, expand_y=True)],
        [sg.Text("状态：就绪"), sg.Checkbox("打印到文件"), sg.Button("首选项")],
        [sg.Text("位置："), sg.Button("查找打印机", expand_y=True)],
        [sg.Text("备注：")]

    ]
    page_range_frame = [
        [sg.Checkbox("全部")],
        [sg.Checkbox("选定范围"), sg.Checkbox("当前页面")],
        [sg.Checkbox("页码"), sg.Input(size=(15, 1))]
    ]
    copy_num_frame = [
        [sg.Text("份数:"), sg.Spin(values=[i for i in range(1, 100)], size=(10, 1))],
        [sg.Checkbox("自动分页")]
    ]
    tab_layout = [
        [sg.Frame(title='选择打印机', layout=choose_printer_frame, expand_x=True)],
        [sg.Frame(title='页面范围', layout=page_range_frame, size=(230, 120)),
         sg.Frame(title='', layout=copy_num_frame, expand_x=True, expand_y=True)],
    ]
    layout = [
        [sg.TabGroup(layout=[[sg.Tab(title='常规', layout=tab_layout)]], expand_x=True)],
        [sg.Button("打印"), sg.Button("取消"), sg.Button("应用")]
    ]
    print_page_win = sg.Window(title='打印', layout=layout, size=(500, 400), margins=(10, 10), )
    while True:
        event, values = print_page_win.read(timeout=100)
        if event == sg.WIN_CLOSED:
            break
    print_page_win.close()


def make_find_str_win(window: PySimpleGUI.Window):
    frame_layout = [
        [sg.Radio('向上', group_id='direction'), sg.Radio('向下', group_id='direction')]
    ]
    col_layout = [
        [sg.Button('逐个查找', disabled=True, button_color='grey', key='-B1-', disabled_button_color='grey')],
        [sg.Button('查找全部', disabled=True, button_color='grey', key='-B2-')],
        [sg.Button('取消')]
    ]
    layout = [
        [sg.T('查找内容：'), sg.In(size=(20, 1), enable_events=True, key='-IN-'), sg.Column(layout=col_layout)],
        # todo 按钮配色有问题
        [sg.CB('区分英文大小写'), sg.Frame(title='查询方向', layout=frame_layout), sg.Cancel('取消')]
    ]
    find_str_win = sg.Window('查找', layout=layout, modal=True, element_padding=(10, 10))
    while True:
        event, values = find_str_win.read(timeout=100)
        if event == sg.WIN_CLOSED:
            break
        if values['-IN-'] != '':
            find_str_win['-B1-'].update(disabled=False)
            find_str_win['-B2-'].update(disabled=False, button_color='blue')
        else:
            find_str_win['-B1-'].update(disabled=True)
            find_str_win['-B2-'].update(disabled=True, button_color='grey')

        if event == '-B2-':
            search_str = values['-IN-']
            print(search_str, 'pass')
            window['-ML-'].Widget.configure(highlightbackground='white', highlightcolor='blue')  # todo 将所有匹配字符串高亮

    find_str_win.close()


def make_replace_str_win(window):
    left_col_layout = [
        [sg.Text("查找："), sg.In(size=(20, 1), key='-OLD STR-')],
        [sg.Text('替换为:'), sg.In(size=(20, 1), key='-NEW STR-')]
    ]
    right_col_layout = [
        [sg.Button('查找', expand_x=True)],
        [sg.Button('替换', expand_x=True, key='-REPLACE-', disabled=True, disabled_button_color='grey')],
        [sg.Button('全部替换', expand_x=True, key='-REPLACE ALL-', disabled=True, disabled_button_color='grey')],
        [sg.Button('取消', expand_x=True)]
    ]
    layout = [
        [sg.Column(layout=left_col_layout, expand_y=True), sg.Column(layout=right_col_layout, expand_x=True)],
        [sg.CBox('区分大小写')]
    ]
    replace_str_win = sg.Window('替换', layout=layout, size=(380, 200), default_button_element_size=(20, 1),
                                element_padding=(5, 5))

    while True:
        event, values = replace_str_win.read(timeout=100)
        if event == sg.WIN_CLOSED:
            break
        if values['-OLD STR-'] and values['-NEW STR-']:
            replace_str_win['-REPLACE-'].update(disabled=False)
            replace_str_win['-REPLACE ALL-'].update(disabled=False)
        else:
            replace_str_win['-REPLACE-'].update(disabled=True)
            replace_str_win['-REPLACE ALL-'].update(disabled=True)

        if event == '-REPLACE ALL-':
            if function.replace_str(window, values['-OLD STR-'], values['-NEW STR-']):
                sg.popup_auto_close("替换成功")
            else:
                sg.popup_auto_close("输入值不存在或替换失败")

    replace_str_win.close()


def make_goto_win():
    pass


def make_set_font_win(window: PySimpleGUI.Window):
    font_family_values_cn = ['宋体', '@宋体', '新宋体', '@新宋体', '黑体', '@黑体', '楷体', '@楷体', '微软雅黑']
    font_family_values_cn_short = ['微软雅黑', '宋体', '新宋体', '黑体', '楷体']
    font_family_values = font_family_values_cn_short + [font for font in tkinter.font.families() if
                                                        font not in font_family_values_cn and not font.startswith(
                                                            '@')]  # 将中文字体靠前显示
    font_style_values = ['常规', '粗体', '倾斜', '粗体 倾斜']
    font_size_cn = []  # todo 暂不支持中文字号
    font_size_values = [i for i in range(8, 12)] + [i * 2 for i in range(7, 14)] + [36, 48, 72]

    current_font_dic = sg.user_settings_get_entry('font', {'font_family': '微软雅黑', 'font_style': '常规',
                                                           'font_size': 14})  # 从用户配置文件中读取存储字体的字典，若配置中无字体配置，则返回预设默认值
    print('读取到的字典：',current_font_dic) #todo delete
    font_family = current_font_dic['font_family']  # 读取默认字体
    font_style = current_font_dic['font_style']  # 读取默认字形
    font_size = current_font_dic['font_size'] # 读取默认字体大小
    current_font = tkinter.font.Font(family=font_family, size=font_size)  # 构建默认字体对象
    print(font_family,font_style,font_size)  # todo  delete

    combo_values = ['中文', '西欧语言']
    left_col_layout = [
        [sg.Text('字体:')],
        [sg.In(size=(20, 1), key='-FONT IN-', default_text=font_family)],
        [sg.Listbox(values=font_family_values, size=(20, 5), default_values=font_family,
                    key='-FONT-', enable_events=True)]
    ]
    center_col_layout = [
        [sg.Text('字形:')],
        [sg.In(size=(15, 1), key='-STYLE IN-', default_text=font_style)],
        [sg.Listbox(values=font_style_values, size=(15, 5), default_values=font_style,
                    key='-STYLE-', enable_events=True)]
    ]
    right_col_layout = [
        [sg.Text('大小:')],
        [sg.In(size=(10, 1), key='-SIZE IN-', default_text=str(font_size))],  # 此处需将int类型转化为字符串
        [sg.Listbox(values=font_size_values, size=(10, 5), default_values=[font_size],
                    key='-SIZE-', enable_events=True)]
    ]
    example_frame_layout = [
        [sg.Text("这是一行示范文字", key='-EXAMPLE-')]
    ]
    col_down_layout = [
        [sg.Frame(title='示例', layout=example_frame_layout, size=(200, 100))],
        [sg.Text('示例文字语言：')],
        [sg.Combo(values=combo_values, default_value='中文')]

    ]

    layout = [
        [sg.Column(layout=left_col_layout), sg.Column(layout=center_col_layout), sg.Column(layout=right_col_layout)],
        [sg.Column(layout=col_down_layout, justification='right')],
        [sg.CBox('将当前字体选择保存为默认配置', key='-CHECK-')],
        [sg.OK('确定'), sg.Cancel('取消'), sg.Button('应用')]
    ]
    set_font_win = sg.Window('设置字体', layout=layout)

    while True:
        event, values = set_font_win.read(timeout=100)
        if event in (sg.WIN_CLOSED, '取消'):
            break
        if event in ('应用', '确定'):
            window['-ML-'].Widget.configure(font=current_font)
            if event == '确定':
                if values['-CHECK-']:
                    current_font_dic = {'font_family': font_family, 'font_style': font_style, 'font_size': font_size}
                    sg.user_settings_set_entry('font', current_font_dic)  # 保存 存储当前字体的字典 到用户配置文件
                    print(sg.user_settings())
                break
        if event == '-FONT-':
            font_family = values['-FONT-'][0]  # 更改当前字体
            set_font_win['-FONT IN-'].update(font_family)  # 列表上方输入框同步显示选中字体
            current_font.configure(family=font_family)  # 将当前字体应用到示范文字

        if event == '-STYLE-':
            font_style = values['-STYLE-'][0]
            set_font_win['-STYLE IN-'].update(font_style)
            if font_style == '常规':
                current_font.configure(weight='normal', slant='roman')
            elif font_style == '粗体':
                current_font.configure(weight='bold', slant='roman')
            elif font_style == '倾斜':
                current_font.configure(slant='italic', weight='normal')
            else:
                current_font.configure(slant='italic', weight='bold')

        if event == '-SIZE-':
            font_size = int(values['-SIZE-'][0])
            set_font_win['-SIZE IN-'].update(font_size)
            current_font.configure(size=font_size)

        set_font_win['-EXAMPLE-'].update(font=current_font)  # 循环末尾 自动更新样本文字 字体

    set_font_win.close()


def make_theme_win(window_list, window, current_theme):
    layout = [
        [sg.Combo(sg.theme_list(), readonly=True, k='-THEME LIST-', default_value=current_theme)],
        [sg.OK("确定"), sg.Cancel("取消"), sg.Button('应用')],
        [sg.CBox('将当前选择主题保存为默认主题', key='-CHECK-', default=True)]
    ]
    theme_win = sg.Window('选择主题', layout=layout, keep_on_top=True)
    while True:
        theme_win_event, theme_win_values = theme_win.read(timeout=50)
        if theme_win_event in (sg.WIN_CLOSED, '取消'):
            break
        if theme_win_event in ('确定', '应用'):
            current_theme = theme_win_values['-THEME LIST-']
            print(sg.user_settings())
            window_list.remove(window)
            window = rebuild_window(window, current_theme, window.current_location())
            window_list.append(window)
            if theme_win_event == '确定':
                if theme_win_values['-CHECK-']:
                    sg.user_settings_set_entry('default_theme', current_theme)  # 保存当前主题为默认主题
                break
    theme_win.close()


# def update_win(window,window_list):
#     window_list.remove(window)
#     window=
#     pass


def make_feedback_win():
    layout = [
        [sg.Text('反馈信息:')],
        [sg.Multiline('请在此处写下你遇到的问题的详细信息', expand_x=True, expand_y=True, right_click_menu=['menu', ["粘贴"]]), ],
        [sg.Text('上传问题截图（最多三张图片）：'), sg.Input(size=(15, 1)), sg.FileBrowse('浏览文件')],
        [sg.Listbox(values=('图片一', '图片二', '图片三'), expand_x=True, expand_y=True)],
        [sg.T('联系方式:'), sg.Combo(values=('邮箱', 'QQ', "微信"), size=(8, 1)), sg.Input(size=(25, 1))],
        [sg.Submit("提交"), sg.Cancel("取消")]
    ]
    feedback_window = sg.Window('反馈界面', layout=layout, size=(600, 500))
    print('123')
    while True:
        event, values = feedback_window.read(timeout=100)
        if event == sg.WIN_CLOSED:
            break
    feedback_window.close()


def make_more_info_win():
    layout = [
        [sg.Text('开发者：Devin')],
        [sg.Text('开发时间：2022年1月')],
        [sg.Text('开发目的：仅用于学习和自用')],
        [sg.Text('程序开源地址：https://github.com')],
        [sg.Text('联系邮箱：stemm@foxmail.com')]

    ]
    sg.Window('更多信息', layout=layout, finalize=True, size=(400, 250), element_padding=(10, 10),
              element_justification='center').read(close=True)
