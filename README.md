# PK10 投注助手 - Kivy 移动版

PK10 赛车/飞艇投注助手工具的 Android 移动版本，使用 Kivy 框架开发，可通过 Buildozer 打包成 APK。

## 功能特性

- 🔑 **账户登录管理** - 支持保存账号密码，自动登录
- 🎯 **实时开奖信息** - 自动获取最新开奖结果和倒计时
- 📝 **投注方案管理** - 可视化选择名次和号码，支持多种投注方案
- 🚀 **一键投注** - 快速提交投注请求
- 🎯 **自定义追号** - 智能追号功能，支持命中重置/未中递增策略
- 📊 **运行日志** - 实时显示操作日志和状态信息
- 🔄 **Session 保活** - 自动保持登录状态，过期自动重登

## 支持的游戏

- 极速赛车
- 幸运飞艇
- 极速飞艇
- 澳洲幸运10

## 安装使用

### 方法一：直接下载 APK（推荐）

1. 访问 [GitHub Actions](../../actions) 页面
2. 选择最新的构建任务
3. 在 Artifacts 区域下载 `pk10-helper-apk`
4. 解压后安装 APK 到 Android 设备

### 方法二：自行构建

#### 环境要求

- Python 3.8+
- Kivy 2.1.0+
- Buildozer (用于打包 APK)

#### 构建步骤

1. 克隆仓库
```bash
git clone https://github.com/你的用户名/pk10-kivy.git
cd pk10-kivy
```

2. 安装依赖
```bash
pip install kivy requests pillow
```

3. 使用 Buildozer 构建 APK（需要 Linux 环境）
```bash
buildozer -v android debug
```

4. 生成的 APK 位于 `bin/` 目录

#### 使用 GitHub Actions 自动构建

1. Fork 本仓库
2. 在仓库设置中启用 GitHub Actions
3. 推送代码到 main 分支，自动触发构建
4. 在 Actions 页面下载构建好的 APK

## 项目结构

```
pk10-kivy/
├── main.py              # 主程序入口
├── buildozer.spec      # Buildozer 配置文件
├── .github/
│   └── workflows/
│       └── build-apk.yml  # GitHub Actions 构建配置
├── README.md           # 项目说明文档
└── requirements.txt    # Python 依赖列表
```

## 开发说明

### 主界面布局

应用采用垂直布局，从上到下依次为：

1. **顶部开奖信息栏** - 显示游戏名称、当前期号、开奖号码球、下期倒计时
2. **控制栏** - 暂停/继续刷新、手动刷新按钮
3. **登录区域** - 登录按钮和账户信息显示
4. **投注区域** - 名次选择、号码选择、金额设置、投注方案列表
5. **运行日志** - 实时日志输出

### 核心模块

- `PK10App` - 主应用类，管理应用生命周期
- `HeaderBar` - 顶部开奖信息显示组件
- `ControlBar` - 控制按钮栏组件
- `LoginSection` - 登录区域组件
- `BetSection` - 投注区域组件
- `LogSection` - 运行日志组件
- `LoginDialog` - 登录对话框

### API 接口

- 开奖信息 API: `https://api.api68.com/pks/getLotteryPksInfo.do`
- 游戏配置: 见 `GAMES` 字典

## 注意事项

1. 本工具仅供学习交流使用
2. 请遵守所在地区的法律法规
3. 理性投注，切勿沉迷
4. 开发者不对使用本工具产生的任何后果负责

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 更新日志

### v1.0 (2025-01-01)

- 初始版本发布
- 实现基本登录和投注功能
- 支持开奖信息实时刷新
- 实现自定义追号功能
- 添加 GitHub Actions 自动构建
