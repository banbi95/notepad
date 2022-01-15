import random
import gui
import function
import PySimpleGUI as sg


def main():
    sg.set_options(suppress_error_popups=True, suppress_raise_key_errors=True)
    sg.set_global_icon(icon='memo.ico')
    current_theme = sg.user_settings_get_entry('default_theme', 'SystemDefault')

    mainwindow = gui.make_win()  # 创建主窗口对象
    window_list = [mainwindow]  # 将主窗口对象添加到窗口列表中

    while True:
        window, event, values = sg.read_all_windows()  # 读取当前活跃窗口 及其 事件和输入值
        if event != "__TIMEOUT__":
            print("event:", event)
        if event in (sg.WIN_CLOSED, "退出(X)"):
            if values['-ML-'] and not window['-SAVE INFO-'].get().startswith(
                    '已保存于') and gui.custom_quit_popup() == '取消':  # 如果文本区非空且信息栏显示未保存 则弹出提示窗口
                continue
            else:
                window_list.remove(window)
                window.close()
        if not window_list:
            break

        if event in ("新建(N)        CTRL+N", 'n:78'):
            function.new_file(window)
        if event in ("新窗口（W)    CTRL+SHIFT+N",):
            window_list.append(function.new_win(window.current_location()))
            print(window_list)

        if event in ("打开(O)     Ctrl+O", 'o:79'):
            function.open_file(window)
        if event in ("保存     Ctrl+S", "s:83"):
            function.save_file(window, values)
        if event == "另存为(A)   Ctrl+Shift+S":  # todo  绑定复合快捷键
            function.save_file_as(window, values)
        if event == "页面设置(U)":
            gui.make_page_setting_win()
        if event in ("打印    Ctrl+P",):
            gui.make_print_page_win()

        if event == "查找     Ctrl+F":
            gui.make_find_str_win(window)
        if event == "替换    Ctrl+H":
            gui.make_replace_str_win(window)
        if event == "时间/日期   F5":
            function.add_time_mark(window)

        if event in ("统计字数", "字数统计"):
            function.count_words(values)
        if event == "字体":
            gui.make_set_font_win(window)

        if event == '默认':
            if current_theme != sg.user_settings_get_entry('default_theme'):
                current_theme = sg.user_settings_get_entry('default_theme')
                window_list.remove(window)
                new_window = gui.rebuild_window(window, current_theme, window.current_location())
                window_list.append(new_window)
                print(window_list)

        if event in ('随机主题 F5', 'F5:116'):
            theme_lst = sg.theme_list()
            index = len(theme_lst) - 1
            current_theme = theme_lst[random.randint(0, index)]  # 获取随机主题
            window_list.remove(window)
            new_window = gui.rebuild_window(window, current_theme, window.current_location())
            window_list.append(new_window)

        if event == '选择主题':
            gui.make_theme_win(window_list, window, current_theme)

        if event == "查看帮助":
            function.check_help()
        if event == "发送反馈":
            gui.make_feedback_win()
        if event == "关于记事本":
            gui.make_more_info_win()

        if event in ['撤销', '剪切', '复制', '粘贴', '全选']:
            function.do_clicpboard_operation(event, window, window['-ML-'])

        # insert_pos=window['-ML-'].Widget.index('insert')  todo 光标行列位置显示不准确
        # print(insert_pos)
        # insert_pos=insert_pos.split('.')
        # window['-COL ROW INFO-'].update("行：{} 列:{}".format(insert_pos[0],int(insert_pos[1])+1))


if __name__ == '__main__':
    main()
