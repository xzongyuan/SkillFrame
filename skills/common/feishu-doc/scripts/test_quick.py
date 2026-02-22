#!/usr/bin/env python3
"""
Feishu Document Skill 快速测试
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from upload import upload_document, append_to_document

def test_upload():
    """测试上传功能"""
    print("测试上传功能...")
    
    # 测试小文档
    result = upload_document(
        title="测试文档-小",
        content="这是一个测试文档的内容。",
        verify=False
    )
    print(f"小文档上传结果: {result}")
    
    # 测试大文档（需要分块）
    large_content = ""
    for i in range(100):
        large_content += f"\n## 第{i+1}节\n"
        large_content += f"这是第{i+1}节的详细内容。" * 10 + "\n"
    
    print(f"\n大文档大小: {len(large_content)}字符")
    
    result = upload_document(
        title="测试文档-大-分块",
        content=large_content,
        verify=False
    )
    print(f"大文档上传结果: {result}")

if __name__ == '__main__':
    test_upload()
