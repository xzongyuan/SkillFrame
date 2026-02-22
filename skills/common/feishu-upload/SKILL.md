---
name: feishu-upload
description: 上传文件到飞书文档，支持创建文档、追加内容、自动验证
version: 1.0.0
author: xiaofei
tools: [bash, read, write, edit]
---

# 飞书上传技能

## 使用场景
当需要将本地文件内容上传到飞书文档时，使用此技能。

## 前置条件
- 文件已存在于本地路径
- 飞书API权限已配置

## 执行流程

### 步骤1: 验证文件存在
使用Read工具检查文件是否存在且非空。
如不存在或为空，报错并停止。

### 步骤2: 创建飞书文档
调用Bash执行创建脚本：
```bash
python {baseDir}/scripts/create_doc.py --title "$TITLE" --folder "$FOLDER"
```
获取返回的 `doc_token` 和 `url`。

### 步骤3: 追加内容
调用Bash执行上传脚本：
```bash
python {baseDir}/scripts/upload_content.py --file "$FILE" --token "$TOKEN"
```

### 步骤4: 验证上传
读取飞书文档确认内容非空。
如验证失败，重试3次。

### 步骤5: 返回结果
返回文档链接和确认信息。

## 错误处理
- 创建失败：检查权限和网络
- 上传失败：自动重试3次
- 验证失败：记录错误，返回部分成功

## 示例
用户：上传 /root/report.md 到飞书，标题"周报"

执行：
1. 验证 /root/report.md 存在
2. 创建文档，标题"周报"
3. 上传内容
4. 验证非空
5. 返回链接
