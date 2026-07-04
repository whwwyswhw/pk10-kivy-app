# -*- coding: utf-8 -*-
"""
PK10 投注助手 - Kivy 移动版
使用 Kivy + Buildozer 打包成 Android APK
"""
import kivy
kivy.require('2.1.0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.modalview import ModalView
from kivy.uix.widget import Widget
from kivy.uix.image import Image as KivyImage
from kivy.uix.checkbox import CheckBox
from kivy.uix.togglebutton import ToggleButton
from kivy.graphics import Color, Rectangle, Ellipse, Line
from kivy.clock import Clock
from kivy.properties import StringProperty, BooleanProperty, ObjectProperty, ListProperty, NumericProperty
from kivy.network.urlrequest import UrlRequest
from kivy.utils import get_color_from_hex
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.progressbar import ProgressBar

import requests
from requests import Session
import json
import os
import io
import re
import threading
import time
import datetime
import base64
from PIL import Image as PILImage
from PIL import ImageTk
import io as io_module

# 强制使用 OpenGL 渲染
Window.clearcolor = (0.94, 0.96, 0.98, 1)  # #F0F4F8

# ===== 全局配置 =====
COLORS = {
    "bg":         (0.94, 0.96, 0.98, 1),
    "card":       (1, 1, 1, 1),
    "primary":    (0.22, 0.48, 0.83, 1),  # #3A7BD5
    "primary_dk": (0.17, 0.38, 0.69, 1),  # #2C60B0
    "success":    (0.15, 0.68, 0.38, 1),  # #27AE60
    "success_dk": (0.12, 0.52, 0.29, 1),  # #1E8449
    "danger":    (0.91, 0.30, 0.24, 1),  # #E74C3C
    "warning":    (0.95, 0.61, 0.07, 1),  # #F39C12
    "purple":    (0.55, 0.27, 0.68, 1),  # #8E44AD
    "text":      (0.17, 0.24, 0.31, 1),  # #2C3E50
    "text_sub":  (0.50, 0.55, 0.55, 1),  # #7F8C8D
    "border":    (0.84, 0.87, 0.93, 1),  # #D5DDED
    "input_bg":  (0.98, 0.99, 1, 1),     # #FAFCFF
    "header_bg":   (0.12, 0.23, 0.37, 1),  # #1E3A5F
    "header_ctrl": (0.15, 0.29, 0.43, 1),  # #264A6E
    "header_text": (0.84, 0.89, 0.94, 1),  # #D6E4F0
    "header_light": (0.91, 0.94, 1, 1),    # #E8F0FE
    "log_bg":     (0.05, 0.07, 0.09, 1),  # #0D1117
    "log_text":   (0.79, 0.82, 0.85, 1),  # #C9D1D9
    "log_border": (0.19, 0.21, 0.24, 1),  # #30363D
}

# PK10 号码球颜色
NUM_COLORS = {
    '1': (0.09, 0.89, 0.90, 1),   # #17E2E5
    '2': (0.98, 0.60, 0.18, 1),   # #F9982E
    '3': (0, 0.09, 0.13, 1),       # #001822
    '4': (0, 0.57, 0.87, 1),      # #0092DD
    '5': (0.90, 0.87, 0, 1),       # #E6DE00
    '6': (0.95, 0, 0.04, 1),       # #F1010A
    '7': (0.75, 0.75, 0.75, 1),   # #BFBFBF
    '8': (0, 0.57, 0.87, 1),       # #0092DD
    '9': (0.32, 0.20, 1, 1),       # #5234FF
    '10': (0.03, 0.75, 0, 1),      # #07BF00
}

# 游戏配置
GAMES = {
    "极速赛车":  {"lotCode": "10037", "lottery_url_code": "PK10JSC"},
    "幸运飞艇":  {"lotCode": "10057", "lottery_url_code": "XYFT"},
    "极速飞艇":  {"lotCode": "10035", "lottery_url_code": "LUCKYSB"},
    "澳洲幸运10": {"lotCode": "10012", "lottery_url_code": "AULUCKY10"},
}

CURRENT_DRAW_API = "https://api.api68.com/pks/getLotteryPksInfo.do"
HISTORY_API     = "https://api.api68.com/pks/getPksHistoryList.do"

POS_GAME_CODES = {
    "1": "B1", "2": "B2", "3": "B3", "4": "B4",
    "5": "B5", "6": "B6", "7": "B7", "8": "B8",
    "9": "B9", "10": "B10",
}

POS_TITLES = {
    "1": "冠军", "2": "亚军", "3": "季军", "4": "殿军",
    "5": "第五名", "6": "第六名", "7": "第七名",
    "8": "第八名", "9": "第九名", "10": "第十名",
}


class BallWidget(Widget):
    """自定义号码球控件"""
    num = NumericProperty(1)
    
    def __init__(self, num=1, size=(32, 32), **kwargs):
        super().__init__(size=size, **kwargs)
        self.num = num
        self.bind(pos=self.update_graphics)
        self.bind(size=self.update_graphics)
        
    def update_graphics(self, *args):
        self.canvas.clear()
        with self.canvas:
            color_hex = ['#17E2E5', '#F9982E', '#001822', '#0092DD', '#E6DE00',
                         '#F1010A', '#BFBFBF', '#0092DD', '#5234FF', '#07BF00'][self.num - 1]
            color = get_color_from_hex(color_hex)
            Color(*color)
            
            # 画圆形
            Ellipse(pos=self.pos, size=self.size)
            
            # 画数字
            Color(1, 1, 1, 1) if self.num in [3] else Color(0, 0, 0, 1)
            # 使用 Label 显示数字
            num_label = Label(text=str(self.num), 
                           pos=(self.pos[0] + 8, self.pos[1] + 8),
                           font_size=14, bold=True)


class HeaderBar(BoxLayout):
    """顶部标题栏"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = '60dp'
        self.padding = [8, 4, 8, 4]
        
        with self.canvas:
            Color(*COLORS["header_bg"])
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_bg, size=self._update_bg)
        
        # 游戏选择
        self.game_spinner = Spinner(
            text='极速赛车',
            values=list(GAMES.keys()),
            size_hint=(None, None),
            size=('100dp', '36dp'),
            background_color=COLORS["header_ctrl"],
            color=COLORS["header_light"]
        )
        self.add_widget(self.game_spinner)
        
        # 期号显示
        self.issue_label = Label(
            text='--期',
            color=COLORS["header_light"],
            font_size='16sp',
            bold=True,
            size_hint=(None, None),
            size=('80dp', '36dp')
        )
        self.add_widget(self.issue_label)
        
        # 号码球容器
        self.balls_layout = BoxLayout(orientation='horizontal',
                                     size_hint=(None, None),
                                     size=('200dp', '36dp'))
        self.add_widget(self.balls_layout)
        
        # 右侧信息
        right_info = BoxLayout(orientation='vertical',
                              size_hint=(None, None),
                              size=('100dp', '56dp'))
        
        self.next_issue_label = Label(
            text='',
            color=(0.55, 0.67, 0.65, 1),
            font_size='12sp',
            halign='right'
        )
        right_info.add_widget(self.next_issue_label)
        
        self.countdown_label = Label(
            text='--:--',
            color=(1, 0.42, 0.42, 1),
            font_size='20sp',
            bold=True,
            halign='right'
        )
        right_info.add_widget(self.countdown_label)
        self.add_widget(right_info)
        
    def _update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        
    def update_balls(self, code_list):
        """更新号码球显示"""
        self.balls_layout.clear_widgets()
        for num_str in code_list[:10]:
            try:
                num = int(num_str.strip())
                ball = BallWidget(num=num, size=('28dp', '28dp'))
                self.balls_layout.add_widget(ball)
            except:
                pass


class ControlBar(BoxLayout):
    """控制栏（暂停/刷新按钮）"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = '28dp'
        self.padding = [8, 2, 8, 2]
        
        with self.canvas:
            Color(*COLORS["header_ctrl"])
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_bg, size=self._update_bg)
        
        self.status_label = Label(
            text='等待获取...',
            color=(0.55, 0.67, 0.65, 1),
            font_size='12sp',
            halign='left',
            valign='middle'
        )
        self.add_widget(self.status_label)
        
        self.pause_btn = Button(
            text='⏸ 暂停',
            size_hint=(None, None),
            size=('70dp', '24dp'),
            background_color=COLORS["header_ctrl"],
            color=COLORS["header_light"]
        )
        self.add_widget(self.pause_btn)
        
        self.refresh_btn = Button(
            text='⟳ 刷新',
            size_hint=(None, None),
            size=('70dp', '24dp'),
            background_color=COLORS["header_ctrl"],
            color=COLORS["header_light"]
        )
        self.add_widget(self.refresh_btn)
        
    def _update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size


class LoginSection(BoxLayout):
    """登录区域"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = '100dp'
        self.padding = [8, 4, 8, 4]
        
        # 标题
        hdr = BoxLayout(size_hint_y=None, height='20dp')
        with hdr.canvas:
            Color(*COLORS["primary"])
            Rectangle(pos=hdr.pos, size=hdr.size)
        hdr.bind(pos=self._update_hdr_bg, size=self._update_hdr_bg)
        
        hdr_label = Label(text=' 🔑 账户', 
                        color=(1, 1, 1, 1),
                        font_size='12sp',
                        bold=True,
                        halign='left',
                        valign='middle')
        hdr.add_widget(hdr_label)
        self.add_widget(hdr)
        
        # 登录按钮
        self.login_btn = Button(
            text='🚀 登录',
            size_hint_y=None,
            height='40dp',
            background_color=COLORS["primary"],
            color=(1, 1, 1, 1),
            font_size='16sp',
            bold=True
        )
        self.add_widget(self.login_btn)
        
        # 提示
        hint = Label(text='点击登录后可在下方投注',
                    color=COLORS["text_sub"],
                    font_size='10sp')
        self.add_widget(hint)
        
    def _update_hdr_bg(self, *args):
        pass  # 需要保存 canvas instruction 引用


class BetSection(BoxLayout):
    """投注区域"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = '300dp'
        self.padding = [8, 4, 8, 4]
        
        # 标题
        hdr = BoxLayout(size_hint_y=None, height='20dp')
        with hdr.canvas:
            Color(*COLORS["primary"])
            Rectangle(pos=hdr.pos, size=hdr.size)
        hdr_label = Label(text=' 🎯 投注区',
                        color=(1, 1, 1, 1),
                        font_size='12sp',
                        bold=True)
        hdr.add_widget(hdr_label)
        self.add_widget(hdr)
        
        # 名次选择
        pos_layout = GridLayout(cols=5, spacing=4, size_hint_y=None, height='40dp')
        self.pos_checkboxes = {}
        for i in range(1, 11):
            cb_layout = BoxLayout(orientation='horizontal', spacing=2)
            cb = CheckBox(color=COLORS["primary"])
            self.pos_checkboxes[str(i)] = cb
            cb_layout.add_widget(cb)
            lbl = Label(text=f'第{i}名', font_size='11sp', size_hint_x=None, width='50dp')
            cb_layout.add_widget(lbl)
            pos_layout.add_widget(cb_layout)
        self.add_widget(pos_layout)
        
        # 号码选择
        num_layout = GridLayout(cols=5, spacing=4, size_hint_y=None, height='60dp')
        self.num_checkboxes = {}
        for i in range(1, 11):
            cb_layout = BoxLayout(orientation='horizontal', spacing=2)
            cb = CheckBox(color=COLORS["primary"])
            self.num_checkboxes[str(i)] = cb
            cb_layout.add_widget(cb)
            # 号码球
            ball = BallWidget(num=i, size=('24dp', '24dp'))
            cb_layout.add_widget(ball)
            num_layout.add_widget(cb_layout)
        self.add_widget(num_layout)
        
        # 金额输入
        amt_layout = BoxLayout(orientation='horizontal', spacing=8, size_hint_y=None, height='36dp')
        amt_layout.add_widget(Label(text='金额 ¥', font_size='12sp', size_hint_x=None, width='50dp'))
        
        self.amt_spinner = Spinner(
            text='2',
            values=['1', '2', '5', '10', '20', '50', '100'],
            size_hint=(None, None),
            size=('60dp', '32dp')
        )
        amt_layout.add_widget(self.amt_spinner)
        
        self.custom_amt_input = TextInput(
            hint_text='自填金额',
            multiline=False,
            size_hint=(None, None),
            size=('60dp', '32dp'),
            input_filter='int'
        )
        amt_layout.add_widget(self.custom_amt_input)
        
        add_btn = Button(
            text='➕ 添加',
            size_hint=(None, None),
            size=('80dp', '32dp'),
            background_color=COLORS["primary"],
            color=(1, 1, 1, 1)
        )
        amt_layout.add_widget(add_btn)
        self.add_widget(amt_layout)
        
        # 投注方案列表
        scheme_label = Label(text='📝 投注方案',
                           color=(0.05, 0.07, 0.09, 1),
                           font_size='12sp',
                           bold=True,
                           size_hint_y=None,
                           height='20dp',
                           halign='left')
        self.add_widget(scheme_label)
        
        # 方案列表滚动区
        scroll = ScrollView(size_hint=(1, 1))
        self.scheme_layout = GridLayout(cols=1, spacing=2, size_hint_y=None)
        self.scheme_layout.bind(minimum_height=self.scheme_layout.setter('height'))
        scroll.add_widget(self.scheme_layout)
        self.add_widget(scroll)
        
    def get_selected_positions(self):
        """获取选中的名次"""
        return [p for p, cb in self.pos_checkboxes.items() if cb.active]
    
    def get_selected_numbers(self):
        """获取选中的号码"""
        return [n for n, cb in self.num_checkboxes.items() if cb.active]


class LogSection(BoxLayout):
    """运行日志区域"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = '200dp'
        self.padding = [8, 4, 8, 4]
        
        # 标题
        hdr = BoxLayout(size_hint_y=None, height='20dp')
        with hdr.canvas:
            Color(*COLORS["primary"])
            Rectangle(pos=hdr.pos, size=hdr.size)
        hdr_label = Label(text=' 📋 运行日志',
                        color=(1, 1, 1, 1),
                        font_size='12sp',
                        bold=True)
        hdr.add_widget(hdr_label)
        self.add_widget(hdr)
        
        # 日志显示
        self.log_text = Label(
            text='',
            color=COLORS["log_text"],
            font_size='10sp',
            halign='left',
            valign='top',
            size_hint_y=None,
            height='180dp'
        )
        scroll = ScrollView()
        scroll.add_widget(self.log_text)
        self.add_widget(scroll)
        
    def log(self, message, level="INFO"):
        """添加日志"""
        ts = datetime.datetime.now().strftime("[%H:%M:%S]")
        icons = {"INFO": "·", "ERROR": "✗", "SUCCESS": "✓", "WARNING": "!"}
        line = f"{ts} {icons.get(level, '·')} {message}\n"
        
        current = self.log_text.text
        self.log_text.text = current + line
        # 限制日志行数
        lines = self.log_text.text.split('\n')
        if len(lines) > 100:
            self.log_text.text = '\n'.join(lines[-100:])


class LoginDialog(ModalView):
    """登录对话框"""
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.size_hint = (0.9, 0.8)
        self.auto_dismiss = False
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 标题
        title = Label(text='🔑 用户登录',
                     font_size='18sp',
                     bold=True,
                     size_hint_y=None,
                     height='40dp')
        layout.add_widget(title)
        
        # 网址
        layout.add_widget(Label(text='网址', size_hint_y=None, height='20dp'))
        self.url_input = TextInput(
            text='https://6942087513-ds.for9dong.com/login',
            multiline=False,
            size_hint_y=None,
            height='36dp'
        )
        layout.add_widget(self.url_input)
        
        # 账号
        layout.add_widget(Label(text='账号', size_hint_y=None, height='20dp'))
        self.account_input = TextInput(
            text='zxc520',
            multiline=False,
            size_hint_y=None,
            height='36dp'
        )
        layout.add_widget(self.account_input)
        
        # 密码
        layout.add_widget(Label(text='密码', size_hint_y=None, height='20dp'))
        self.password_input = TextInput(
            password=True,
            multiline=False,
            size_hint_y=None,
            height='36dp'
        )
        layout.add_widget(self.password_input)
        
        # 验证码
        layout.add_widget(Label(text='验证码', size_hint_y=None, height='20dp'))
        captcha_layout = BoxLayout(orientation='horizontal', spacing=8, size_hint_y=None, height='40dp')
        
        self.captcha_img = KivyImage(size_hint=(None, None), size=('120dp', '40dp'))
        captcha_layout.add_widget(self.captcha_img)
        
        self.captcha_input = TextInput(
            multiline=False,
            size_hint=(None, None),
            size=('80dp', '36dp')
        )
        captcha_layout.add_widget(self.captcha_input)
        
        get_captcha_btn = Button(
            text='获取',
            size_hint=(None, None),
            size=('60dp', '36dp'),
            background_color=COLORS["warning"]
        )
        get_captcha_btn.bind(on_press=self.get_captcha)
        captcha_layout.add_widget(get_captcha_btn)
        layout.add_widget(captcha_layout)
        
        # 状态
        self.status_label = Label(text='请先点击「获取」验证码',
                                  size_hint_y=None,
                                  height='20dp')
        layout.add_widget(self.status_label)
        
        # 保存配置按钮
        save_btn = Button(
            text='💾 保存配置',
            size_hint_y=None,
            height='36dp',
            background_color=(0.84, 0.96, 0.89, 1)
        )
        save_btn.bind(on_press=self.save_config)
        layout.add_widget(save_btn)
        
        # 按钮行
        btn_layout = BoxLayout(orientation='horizontal', spacing=8, size_hint_y=None, height='40dp')
        
        login_btn = Button(
            text='🚀 确认登录',
            background_color=COLORS["success"],
            color=(1, 1, 1, 1)
        )
        login_btn.bind(on_press=self.do_login)
        btn_layout.add_widget(login_btn)
        
        cancel_btn = Button(text='取消')
        cancel_btn.bind(on_press=self.dismiss)
        btn_layout.add_widget(cancel_btn)
        layout.add_widget(btn_layout)
        
        self.add_widget(layout)
        
    def get_captcha(self, *args):
        """获取验证码"""
        self.status_label.text = '正在获取验证码...'
        # 这里需要实现验证码获取逻辑
        # 由于是示例，这里只是模拟
        Clock.schedule_once(lambda dt: self._on_captcha_ready(), 1)
        
    def _on_captcha_ready(self):
        """验证码获取完成"""
        self.status_label.text = '验证码已获取，请输入'
        
    def save_config(self, *args):
        """保存配置"""
        config = {
            'url': self.url_input.text,
            'account': self.account_input.text,
            'password': self.password_input.text
        }
        # 保存到文件
        try:
            with open('login_config.json', 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            self.status_label.text = '配置已保存'
        except Exception as e:
            self.status_label.text = f'保存失败: {e}'
            
    def do_login(self, *args):
        """执行登录"""
        self.status_label.text = '正在登录...'
        # 这里需要实现登录逻辑
        # 由于是示例，这里只是模拟
        Clock.schedule_once(lambda dt: self._on_login_result(True), 2)
        
    def _on_login_result(self, success):
        """登录结果"""
        if success:
            self.status_label.text = '登录成功!'
            Clock.schedule_once(lambda dt: self.dismiss(), 1)
            self.app.on_login_success()
        else:
            self.status_label.text = '登录失败，请重试'


class PK10App(App):
    """主应用类"""
    title = 'PK10 投注助手'
    
    def build(self):
        """构建UI"""
        self.session = None
        self.logged_in = False
        self.current_game = '极速赛车'
        self.current_draw_data = None
        
        # 主布局
        main_layout = BoxLayout(orientation='vertical', padding=4, spacing=4)
        
        # 顶部开奖信息
        self.header = HeaderBar()
        self.header.game_spinner.bind(text=self.on_game_changed)
        main_layout.add_widget(self.header)
        
        # 控制栏
        self.control_bar = ControlBar()
        self.control_bar.refresh_btn.bind(on_press=self.fetch_current_draw)
        main_layout.add_widget(self.control_bar)
        
        # 登录区域
        self.login_section = LoginSection()
        self.login_section.login_btn.bind(on_press=self.open_login_dialog)
        main_layout.add_widget(self.login_section)
        
        # 投注区域
        self.bet_section = BetSection()
        main_layout.add_widget(self.bet_section)
        
        # 日志区域
        self.log_section = LogSection()
        main_layout.add_widget(self.log_section)
        
        # 启动定时刷新
        Clock.schedule_interval(self.auto_refresh_loop, 10)
        Clock.schedule_interval(self.update_countdown, 1)
        
        return main_layout
    
    def on_game_changed(self, spinner, text):
        """游戏切换"""
        if text in GAMES:
            self.current_game = text
            self.log(f'切换游戏 → {text}', 'INFO')
            self.fetch_current_draw()
            
    def fetch_current_draw(self, *args):
        """获取当前开奖信息"""
        self.control_bar.status_label.text = '获取中...'
        game_config = GAMES[self.current_game]
        lot_code = game_config['lotCode']
        
        # 使用 UrlRequest 异步请求
        params = {'lotCode': lot_code}
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Referer': 'https://kj.1689683.com/'
        }
        
        req = UrlRequest(
            CURRENT_DRAW_API,
            on_success=self.on_draw_received,
            on_error=self.on_draw_error,
            req_headers=headers,
            ca_file=None
        )
        # 手动设置 URL 参数
        req.url = CURRENT_DRAW_API + '?' + '&'.join([f'{k}={v}' for k, v in params.items()])
        
    def on_draw_received(self, req, result):
        """开奖数据接收成功"""
        try:
            data = result.get('result', {}).get('data', {})
            if data:
                self.current_draw_data = data
                self.update_draw_display(data)
                self.control_bar.status_label.text = datetime.datetime.now().strftime('%H:%M:%S')
            else:
                self.control_bar.status_label.text = '暂无数据'
        except Exception as e:
            self.log(f'解析开奖数据失败: {e}', 'ERROR')
            
    def on_draw_error(self, req, error):
        """开奖数据获取失败"""
        self.control_bar.status_label.text = '获取失败'
        self.log(f'获取开奖失败: {error}', 'ERROR')
        
    def update_draw_display(self, data):
        """更新开奖显示"""
        issue = data.get('preDrawIssue', '--')
        self.header.issue_label.text = f'{issue}期'
        
        codes = data.get('preDrawCode', '')
        code_list = [c.strip() for c in codes.split(',') if c.strip()]
        self.header.update_balls(code_list)
        
        next_issue = data.get('drawIssue', '--')
        self.header.next_issue_label.text = f'下期 {next_issue}'
        
    def update_countdown(self, dt):
        """更新倒计时"""
        if self.current_draw_data:
            draw_time_str = self.current_draw_data.get('drawTime', '')
            if draw_time_str:
                try:
                    draw_time = datetime.datetime.strptime(draw_time_str, '%Y-%m-%d %H:%M:%S')
                    now = datetime.datetime.now()
                    diff = (draw_time - now).total_seconds()
                    if diff > 0:
                        self.header.countdown_label.text = f'{int(diff//60):02d}:{int(diff%60):02d}'
                    elif diff > -30:
                        self.header.countdown_label.text = '开奖中'
                    else:
                        self.header.countdown_label.text = '--:--'
                except:
                    self.header.countdown_label.text = '--:--'
                    
    def auto_refresh_loop(self, dt):
        """自动刷新循环"""
        if hasattr(self.control_bar, 'pause_btn'):
            if self.control_bar.pause_btn.text == '⏸ 暂停':
                self.fetch_current_draw()
        return True
        
    def open_login_dialog(self, *args):
        """打开登录对话框"""
        dialog = LoginDialog(self)
        dialog.open()
        
    def on_login_success(self):
        """登录成功回调"""
        self.logged_in = True
        self.log('登录成功 ✓', 'SUCCESS')
        # 更新 UI 状态
        self.login_section.clear_widgets()
        balance_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='40dp')
        balance_layout.add_widget(Label(text='💰', size_hint_x=None, width='30dp'))
        self.balance_label = Label(text='¥ --', color=COLORS["danger"], font_size='16sp', bold=True)
        balance_layout.add_widget(self.balance_label)
        
        logout_btn = Button(text='🚪 退出', size_hint=(None, None), size=('80dp', '36dp'))
        logout_btn.bind(on_press=self.do_logout)
        balance_layout.add_widget(logout_btn)
        self.login_section.add_widget(balance_layout)
        
    def do_logout(self, *args):
        """退出登录"""
        self.logged_in = False
        self.session = None
        self.log('已退出登录', 'WARNING')
        # 恢复登录按钮
        self.login_section.clear_widgets()
        self.login_section.__init__()
        self.login_section.login_btn.bind(on_press=self.open_login_dialog)
        
    def log(self, message, level="INFO"):
        """添加日志"""
        self.log_section.log(message, level)
        
    def on_stop(self):
        """应用退出时保存配置"""
        pass


if __name__ == '__main__':
    PK10App().run()
