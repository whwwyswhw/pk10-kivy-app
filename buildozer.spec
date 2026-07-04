[app]
# 应用名称
title = PK10投注助手

# 包名（必须唯一）
package.name = pk10helper

# 包域名
package.domain = org.example

# 源代码目录
source.dir = .

# 主程序文件
source.include_exts = py,png,jpg,kv,json,db,ttf

# 应用版本
version = 1.0

# 应用版本代码（整数）
version.code = 1

# 需求
requirements = python3,kivy,requests,pillow

# 图标（可选）
#icon.filename = %(source.dir)s/icon.png

# 启动画面（可选）
#presplash.filename = %(source.dir)s/presplash.png

# 支持的架构
arch = armeabi-v7a,arm64-v8a

# 是否包含 Androidx
android.enable_androidx = True

# 最低 Android API 级别
android.minapi = 21

# 目标 Android API 级别
android.targetapi = 30

# 编译 Android API 级别
android.compileapi = 30

# Android SDK 目录（如果未设置，Buildozer 会自动下载）
#android.sdk_path = 

# Android NDK 目录（如果未设置，Buildozer 会自动下载）
#android.ndk_path =

# 是否使用 Android 模拟器
#android.allow_backup = True

# 权限
android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE

# 功能
android.features = 

# 全屏模式
fullscreen = 0

# 保持屏幕常亮
wake_lock = False

# 方向
orientation = portrait

# Android 应用版本号（显示在应用信息中）
android.version_code = 1

# 是否使用 AAB（Android App Bundle）格式
android.use_aab = False

# 是否启用多 dex
android.multidex = False

# 是否启用 AndroidX
android.enable_androidx = True

# 是否使用 gradle 构建
android.gradle_dependencies = 

# 额外的 Java 编译选项
android.extra_buildozer_args = 

# iOS 配置（如果需要）
#ios.codesign.allowed = false
#ios.codesign.developer = 
#ios.codesign.fingerprint = 

# 预设 splash 屏幕（如果你有图片）
#presplash.filename = %(source.dir)s/presplash.png
#presplash.color = #FFFFFF

# 图标
#icon.filename = %(source.dir)s/icon.png

# 是否使用预设 icon
#icon.icons = 

[buildozer]
# 构建输出目录
build_dir = /home/user/.buildozer

# 日志级别
log_level = 2

# 是否自动清理构建文件
clean = False

# 是否跳过依赖检查
skip_checks = False

# 是否使用国内镜像（加速下载）
# 如果在国内，可以取消注释下面的行
#android.sdk_http_proxy = http://mirrors.aliyun.com
#android.ndk_http_proxy = http://mirrors.aliyun.com
