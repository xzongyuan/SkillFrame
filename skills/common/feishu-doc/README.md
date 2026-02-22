# Feishu Document Skill

飞书文档上传与管理 Skill，支持智能分块、自动重试和上传验证。

## 功能特性

- ✅ **智能分块** - 自动检测文档大小，按段落/章节分块，保持内容完整性
- ✅ **自动重试** - 失败自动重试（指数退避），错误分类处理
- ✅ **上传验证** - 上传后读取验证，块数核对，内容摘要比对
- ✅ **统一接口** - 简洁的API设计，易于集成

## 安装

将本目录复制到 OpenClaw skills 目录：

```bash
cp -r skills/common/feishu-doc ~/.openclaw/skills/common/
```

## 使用方法

### 1. 上传文档（自动分块）

```python
result = skill.execute("feishu-doc", {
    "action": "upload",
    "title": "架构设计文档",
    "content": large_content,  # 自动分块
    "folder_token": "fldxxx",   # 可选
    "verify": True              # 上传后验证
})

# 返回结果
{
    "success": True,
    "doc_token": "docxxx",
    "url": "https://xxx.feishu.cn/docx/xxx",
    "blocks": 5,
    "verified": True,
    "message": "文档上传成功，共5个块"
}
```

### 2. 追加内容

```python
result = skill.execute("feishu-doc", {
    "action": "append",
    "doc_token": "docxxx",
    "content": more_content,
    "verify": True
})

# 返回结果
{
    "success": True,
    "blocks_added": 3,
    "verified": True,
    "message": "成功追加3个块"
}
```

### 3. 创建空文档

```python
result = skill.execute("feishu-doc", {
    "action": "create",
    "title": "新文档",
    "folder_token": "fldxxx"
})
```

### 4. 验证文档

```python
result = skill.execute("feishu-doc", {
    "action": "verify",
    "doc_token": "docxxx",
    "expected_content": "预期内容"
})
```

## 配置说明

编辑 `config.yaml`：

```yaml
# 每块最大字符数
chunk_size: 5000

# 最大重试次数
max_retries: 3

# 指数退避延迟（秒）
retry_delay: [1, 2, 4]

# 上传后自动验证
verify_after_upload: true

# API 请求超时（秒）
request_timeout: 30

# 验证时预览内容长度
verify_preview_length: 200
```

## 智能分块策略

1. **按章节分割** - 优先按 Markdown 标题 (`##`) 分割
2. **按段落分割** - 章节内按段落分割
3. **强制切割** - 单个段落超长时强制切割
4. **保持完整性** - 确保每块内容语义完整

## 错误处理

### 可重试错误
- 网络超时/连接错误
- 速率限制 (429)
- 服务器错误 (500, 502, 503, 504)

### 不可重试错误
- 认证错误 (401, 403)
- 参数错误 (400)

## 目录结构

```
skills/common/feishu-doc/
├── SKILL.md              # Skill 定义
├── scripts/
│   ├── upload.py         # 主上传脚本（分块+重试）
│   ├── create.py         # 创建文档
│   ├── append.py         # 追加内容（分块）
│   ├── verify.py         # 验证上传结果
│   └── retry.py          # 重试机制
├── config.yaml           # 配置文件
└── README.md             # 使用文档
```

## 测试

运行测试脚本：

```bash
cd skills/common/feishu-doc

# 测试分块功能
python3 scripts/append.py --doc-token "test" --content "$(cat large_file.md)" --chunk-size 5000

# 测试重试机制
python3 scripts/retry.py
```

## 注意事项

1. 确保已配置飞书 API 凭证
2. 大文档上传可能需要较长时间，请耐心等待
3. 分块大小建议 3000-8000 字符，过小会增加API调用次数
4. 验证功能会增加一次读取API调用

## 更新日志

### v1.0.0
- 初始版本
- 支持智能分块上传
- 支持自动重试机制
- 支持上传验证
