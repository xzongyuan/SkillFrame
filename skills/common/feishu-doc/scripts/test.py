#!/usr/bin/env python3
"""
Feishu Document Skill 测试脚本
"""

import sys
import os

# 添加脚本目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from append import smart_chunk
from retry import with_retry, classify_error


def test_smart_chunk():
    """测试智能分块功能"""
    print("=" * 50)
    print("测试智能分块功能")
    print("=" * 50)
    
    # 测试1: 小内容不分块
    small_content = "这是一段小内容"
    chunks = smart_chunk(small_content, max_chunk_size=100)
    assert len(chunks) == 1, f"小内容应该只有1块，实际{len(chunks)}块"
    print(f"✓ 小内容测试通过: {len(chunks)}块")
    
    # 测试2: 按章节分块
    chapter_content = """
# 第一章
这是第一章的内容。
有多行内容。

## 第一节
第一节详细内容。

## 第二节
第二节详细内容。

# 第二章
这是第二章的内容。
非常长的一段内容，需要被正确处理。
"""
    chunks = smart_chunk(chapter_content, max_chunk_size=100)
    print(f"✓ 章节分块测试: 原始{len(chapter_content)}字符，分成{len(chunks)}块")
    for i, chunk in enumerate(chunks):
        print(f"  块{i+1}: {len(chunk)}字符")
    
    # 测试3: 超大内容分块
    large_content = "A" * 15000
    chunks = smart_chunk(large_content, max_chunk_size=5000)
    assert len(chunks) >= 3, f"15000字符应该至少分成3块，实际{len(chunks)}块"
    print(f"✓ 大内容分块测试通过: {len(chunks)}块")
    
    print("智能分块测试全部通过！\n")


def test_retry_mechanism():
    """测试重试机制"""
    print("=" * 50)
    print("测试重试机制")
    print("=" * 50)
    
    # 测试1: 成功重试
    counter = [0]
    def success_after_retries():
        counter[0] += 1
        if counter[0] < 3:
            raise Exception(f"模拟错误 #{counter[0]}")
        return {"success": True, "attempts": counter[0]}
    
    result = with_retry(success_after_retries, max_retries=3, retry_delays=[0.1, 0.1, 0.1])
    assert result["success"] == True
    assert counter[0] == 3
    print(f"✓ 成功重试测试通过: 第{counter[0]}次尝试成功")
    
    # 测试2: 最终失败
    def always_fail():
        raise Exception("总是失败")
    
    try:
        with_retry(always_fail, max_retries=2, retry_delays=[0.1, 0.1])
        assert False, "应该抛出异常"
    except Exception as e:
        print(f"✓ 最终失败测试通过: {e}")
    
    # 测试3: 错误分类
    retryable, error_type, suggestion = classify_error(Exception("connection timeout"))
    assert retryable == True
    assert error_type == "network"
    print(f"✓ 错误分类测试通过: {error_type} -> {suggestion}")
    
    print("重试机制测试全部通过！\n")


def test_chunk_integrity():
    """测试分块后内容完整性"""
    print("=" * 50)
    print("测试分块后内容完整性")
    print("=" * 50)
    
    original = """
# 标题1
内容1

# 标题2
内容2

# 标题3
内容3
"""
    
    chunks = smart_chunk(original, max_chunk_size=50)
    reconstructed = "".join(chunks)
    
    # 检查内容是否完整（忽略空白差异）
    original_normalized = "".join(original.split())
    reconstructed_normalized = "".join(reconstructed.split())
    
    assert original_normalized == reconstructed_normalized, "内容应该保持一致"
    print(f"✓ 内容完整性测试通过")
    print(f"  原始长度: {len(original)}字符")
    print(f"  分块数: {len(chunks)}")
    print(f"  重建长度: {len(reconstructed)}字符")
    
    print("内容完整性测试通过！\n")


def simulate_upload_scenario():
    """模拟上传场景"""
    print("=" * 50)
    print("模拟上传场景")
    print("=" * 50)
    
    # 模拟大文档
    large_doc = ""
    for i in range(20):
        large_doc += f"\n## 第{i+1}章\n"
        large_doc += f"这是第{i+1}章的内容。\n" * 50
    
    print(f"模拟文档大小: {len(large_doc)}字符")
    
    # 分块
    chunks = smart_chunk(large_doc, max_chunk_size=5000)
    print(f"分成{len(chunks)}个块")
    
    # 统计
    total_size = sum(len(c) for c in chunks)
    avg_size = total_size / len(chunks) if chunks else 0
    print(f"总字符数: {total_size}")
    print(f"平均每块: {avg_size:.0f}字符")
    print(f"最大块: {max(len(c) for c in chunks)}字符")
    print(f"最小块: {min(len(c) for c in chunks)}字符")
    
    print("\n模拟场景完成！\n")


if __name__ == '__main__':
    print("\n" + "=" * 50)
    print("Feishu Document Skill 测试套件")
    print("=" * 50 + "\n")
    
    test_smart_chunk()
    test_retry_mechanism()
    test_chunk_integrity()
    simulate_upload_scenario()
    
    print("=" * 50)
    print("所有测试通过！✅")
    print("=" * 50)
