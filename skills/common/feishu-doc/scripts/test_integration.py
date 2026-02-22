#!/usr/bin/env python3
"""
Feishu Document Skill 集成测试
需要配置飞书API凭证才能运行
"""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from upload import upload_document, append_to_document
from create import create_document
from verify import verify_document


def test_create_document():
    """测试创建文档"""
    print("\n测试1: 创建文档")
    print("-" * 40)
    
    result = create_document("测试文档-集成测试")
    print(f"结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
    
    if result['success']:
        print("✓ 创建文档成功")
        return result['doc_token']
    else:
        print("✗ 创建文档失败")
        return None


def test_upload_small_document():
    """测试上传小文档"""
    print("\n测试2: 上传小文档（无需分块）")
    print("-" * 40)
    
    content = "这是一个小文档的内容，用于测试上传功能。"
    result = upload_document(
        title="小文档测试",
        content=content,
        verify=True
    )
    print(f"结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
    
    if result['success']:
        print("✓ 小文档上传成功")
    else:
        print("✗ 小文档上传失败")
    
    return result


def test_upload_large_document():
    """测试上传大文档（需要分块）"""
    print("\n测试3: 上传大文档（需要分块）")
    print("-" * 40)
    
    # 生成大内容
    content = ""
    for i in range(50):
        content += f"\n## 第{i+1}节\n"
        content += f"这是第{i+1}节的详细内容。" * 20
        content += "\n"
    
    print(f"文档大小: {len(content)}字符")
    
    result = upload_document(
        title="大文档测试-分块上传",
        content=content,
        verify=True
    )
    print(f"结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
    
    if result['success'] and result.get('blocks', 0) > 1:
        print(f"✓ 大文档上传成功，分成{result['blocks']}个块")
    elif result['success']:
        print(f"✓ 大文档上传成功，未分块")
    else:
        print("✗ 大文档上传失败")
    
    return result


def test_append_content(doc_token):
    """测试追加内容"""
    print("\n测试4: 追加内容")
    print("-" * 40)
    
    if not doc_token:
        print("跳过：没有可用的doc_token")
        return None
    
    content = "\n\n## 追加部分\n这是追加的内容。" * 10
    
    result = append_to_document(
        doc_token=doc_token,
        content=content,
        verify=True
    )
    print(f"结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
    
    if result['success']:
        print(f"✓ 追加内容成功，新增{result.get('blocks_added', 0)}个块")
    else:
        print("✗ 追加内容失败")
    
    return result


def test_verify_document(doc_token):
    """测试验证文档"""
    print("\n测试5: 验证文档")
    print("-" * 40)
    
    if not doc_token:
        print("跳过：没有可用的doc_token")
        return None
    
    result = verify_document(doc_token)
    print(f"结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
    
    if result['success']:
        print(f"✓ 文档验证成功，共{result.get('block_count', 0)}个块")
    else:
        print("✗ 文档验证失败")
    
    return result


def run_all_tests():
    """运行所有集成测试"""
    print("\n" + "=" * 50)
    print("Feishu Document Skill 集成测试")
    print("=" * 50)
    print("注意: 需要配置飞书API凭证才能运行")
    
    # 测试1: 创建文档
    doc_token = test_create_document()
    
    # 测试2: 上传小文档
    test_upload_small_document()
    
    # 测试3: 上传大文档
    large_result = test_upload_large_document()
    
    # 测试4: 追加内容
    if large_result and large_result.get('doc_token'):
        test_append_content(large_result['doc_token'])
    
    # 测试5: 验证文档
    if doc_token:
        test_verify_document(doc_token)
    
    print("\n" + "=" * 50)
    print("集成测试完成")
    print("=" * 50)


if __name__ == '__main__':
    run_all_tests()
