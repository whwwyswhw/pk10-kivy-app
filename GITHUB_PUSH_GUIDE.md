# 推送到 GitHub 指南

## 方法一：使用 GitHub CLI（推荐）

1. **安装 GitHub CLI**
   - 访问 https://cli.github.com/ 下载并安装
   - 或使用命令行安装：`winget install --id GitHub.cli`

2. **登录 GitHub**
   ```bash
   gh auth login
   ```
   按照提示完成登录（选择 GitHub.com，HTTPS 协议，浏览器登录）

3. **创建仓库并推送**
   ```bash
   cd D:\Kivy-Buildozer\pk10_kivy
   gh repo create pk10-kivy --public --push
   ```

## 方法二：手动在 GitHub 网站创建仓库

1. **在 GitHub 网站创建新仓库**
   - 访问 https://github.com/new
   - 仓库名：`pk10-kivy`
   - 选择 Public 或 Private
   - **不要**勾选 "Initialize this repository with a README"
   - 点击 "Create repository"

2. **推送本地代码**
   ```bash
   cd D:\Kivy-Buildozer\pk10_kivy
   git branch -M main
   git remote add origin https://github.com/你的用户名/pk10-kivy.git
   git push -u origin main
   ```

## 方法三：使用 Personal Access Token

1. **创建 Token**
   - 访问 https://github.com/settings/tokens
   - 点击 "Generate new token (classic)"
   - 勾选 `repo` 权限
   - 生成并复制 token

2. **推送代码**
   ```bash
   cd D:\Kivy-Buildozer\pk10_kivy
   git branch -M main
   git remote add origin https://github.com/你的用户名/pk10-kivy.git
   git push -u origin main
   ```
   当提示输入密码时，粘贴你的 token

## 推送后的操作

推送成功后：

1. **启用 GitHub Actions**
   - 访问你的仓库页面
   - 点击 "Actions" 标签页
   - 如果看到 "Enable Actions" 按钮，点击启用

2. **查看构建进度**
   - 在 "Actions" 标签页查看构建进度
   - 首次构建可能需要 30-60 分钟

3. **下载 APK**
   - 构建完成后，在 Actions 页面点击最新构建任务
   - 在 "Artifacts" 区域下载 `pk10-helper-apk`
   - 解压后得到 APK 文件

## 注意事项

- 确保仓库名没有被占用
- 如果是私有仓库，GitHub Actions 需要付费计划（公有仓库免费）
- 首次构建时间较长，请耐心等待
- 如果构建失败，检查 Actions 日志排查问题

## 快速命令参考

```bash
# 查看当前状态
git status

# 添加所有文件
git add .

# 提交
git commit -m "更新说明"

# 推送
git push -u origin main
```
