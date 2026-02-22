# Feishu Document Skill

skill:
  name: feishu-doc
  version: 1.0.0
  description: 飞书文档上传与管理，支持智能分块、自动重试和上传验证
  author: OpenClaw
  
entry:
  python: scripts/upload.py

actions:
  upload:
    description: 创建并上传文档（支持大文档自动分块）
    parameters:
      title:
        type: string
        required: true
        description: 文档标题
      content:
        type: string
        required: true
        description: 文档内容（自动分块）
      folder_token:
        type: string
        required: false
        description: 目标文件夹token
      verify:
        type: boolean
        required: false
        default: true
        description: 上传后验证
    returns:
      success: bool
      doc_token: string
      url: string
      blocks: int
      verified: bool
      message: string
      
  append:
    description: 向现有文档追加内容（自动分块）
    parameters:
      doc_token:
        type: string
        required: true
        description: 文档token
      content:
        type: string
        required: true
        description: 追加内容
      verify:
        type: boolean
        required: false
        default: true
        description: 追加后验证
    returns:
      success: bool
      blocks_added: int
      verified: bool
      message: string
      
  create:
    description: 创建空文档
    parameters:
      title:
        type: string
        required: true
        description: 文档标题
      folder_token:
        type: string
        required: false
        description: 目标文件夹token
    returns:
      success: bool
      doc_token: string
      url: string
      message: string
      
  verify:
    description: 验证文档内容
    parameters:
      doc_token:
        type: string
        required: true
        description: 文档token
      expected_content:
        type: string
        required: false
        description: 预期内容（用于比对）
    returns:
      success: bool
      block_count: int
      content_preview: string
      verified: bool
      message: string

config:
  chunk_size: 5000
  max_retries: 3
  retry_delay: [1, 2, 4]
  verify_after_upload: true
  
dependencies:
  - feishu_doc
  - feishu_drive
  - yaml
