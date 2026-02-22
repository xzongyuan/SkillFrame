#!/usr/bin/env python3
"""
Feishu Document Upload Skill - Main Entry Point
飞书文档上传技能 - 主入口

Features:
- 智能分块上传
- 自动重试机制
- 上传验证
"""

import sys
import json
import os
import yaml

# 添加脚本目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from create import create_document
from append import append_content_to_doc
from verify import verify_document
from retry import with_retry


def load_config():
    """加载配置文件"""
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config.yaml')
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        # 默认配置
        return {
            'chunk_size': 5000,
            'max_retries': 3,
            'retry_delay': [1, 2, 4],
            'verify_after_upload': True
        }


def upload_document(title: str, content: str, folder_token: str = None, verify: bool = True) -> dict:
    """
    上传文档（支持大文档自动分块）
    
    Args:
        title: 文档标题
        content: 文档内容
        folder_token: 目标文件夹token
        verify: 是否验证上传结果
        
    Returns:
        {
            'success': bool,
            'doc_token': str,
            'url': str,
            'blocks': int,
            'verified': bool,
            'message': str
        }
    """
    config = load_config()
    
    try:
        # Step 1: 创建文档
        print(f"[1/3] 创建文档: {title}", file=sys.stderr)
        create_result = with_retry(
            lambda: create_document(title, folder_token),
            max_retries=config['max_retries'],
            retry_delays=config['retry_delay']
        )
        
        if not create_result['success']:
            return {
                'success': False,
                'doc_token': None,
                'url': None,
                'blocks': 0,
                'verified': False,
                'message': f'创建文档失败: {create_result.get("message", "未知错误")}'
            }
        
        doc_token = create_result['doc_token']
        doc_url = create_result['url']
        
        print(f"[2/3] 追加内容（自动分块）", file=sys.stderr)
        # Step 2: 追加内容（自动分块）
        append_result = append_content_to_doc(
            doc_token=doc_token,
            content=content,
            config=config
        )
        
        if not append_result['success']:
            return {
                'success': False,
                'doc_token': doc_token,
                'url': doc_url,
                'blocks': append_result.get('blocks_added', 0),
                'verified': False,
                'message': f'追加内容失败: {append_result.get("message", "未知错误")}'
            }
        
        # Step 3: 验证（如果需要）
        verified = False
        if verify and config.get('verify_after_upload', True):
            print(f"[3/3] 验证上传结果", file=sys.stderr)
            verify_result = with_retry(
                lambda: verify_document(doc_token, content),
                max_retries=config['max_retries'],
                retry_delays=config['retry_delay']
            )
            verified = verify_result.get('verified', False)
        else:
            print(f"[3/3] 跳过验证", file=sys.stderr)
        
        return {
            'success': True,
            'doc_token': doc_token,
            'url': doc_url,
            'blocks': append_result['blocks_added'],
            'verified': verified,
            'message': f'文档上传成功，共{append_result["blocks_added"]}个块'
        }
        
    except Exception as e:
        return {
            'success': False,
            'doc_token': None,
            'url': None,
            'blocks': 0,
            'verified': False,
            'message': f'上传失败: {str(e)}'
        }


def append_to_document(doc_token: str, content: str, verify: bool = True) -> dict:
    """
    向现有文档追加内容
    
    Args:
        doc_token: 文档token
        content: 追加内容
        verify: 是否验证
        
    Returns:
        {
            'success': bool,
            'blocks_added': int,
            'verified': bool,
            'message': str
        }
    """
    config = load_config()
    
    try:
        print(f"[1/2] 追加内容（自动分块）", file=sys.stderr)
        # 追加内容
        append_result = append_content_to_doc(
            doc_token=doc_token,
            content=content,
            config=config
        )
        
        if not append_result['success']:
            return append_result
        
        # 验证
        verified = False
        if verify and config.get('verify_after_upload', True):
            print(f"[2/2] 验证追加结果", file=sys.stderr)
            verify_result = with_retry(
                lambda: verify_document(doc_token),
                max_retries=config['max_retries'],
                retry_delays=config['retry_delay']
            )
            verified = verify_result.get('verified', False)
        else:
            print(f"[2/2] 跳过验证", file=sys.stderr)
        
        return {
            'success': True,
            'blocks_added': append_result['blocks_added'],
            'verified': verified,
            'message': f'成功追加{append_result["blocks_added"]}个块'
        }
        
    except Exception as e:
        return {
            'success': False,
            'blocks_added': 0,
            'verified': False,
            'message': f'追加失败: {str(e)}'
        }


def main():
    """主入口函数"""
    if len(sys.argv) < 2:
        print(json.dumps({
            'success': False,
            'message': '缺少action参数'
        }, ensure_ascii=False))
        sys.exit(1)
    
    action = sys.argv[1]
    
    # 从stdin读取参数
    try:
        params = json.load(sys.stdin) if not sys.stdin.isatty() else {}
    except:
        params = {}
    
    if action == 'upload':
        result = upload_document(
            title=params.get('title'),
            content=params.get('content', ''),
            folder_token=params.get('folder_token'),
            verify=params.get('verify', True)
        )
    elif action == 'append':
        result = append_to_document(
            doc_token=params.get('doc_token'),
            content=params.get('content', ''),
            verify=params.get('verify', True)
        )
    elif action == 'create':
        result = with_retry(
            lambda: create_document(params.get('title'), params.get('folder_token')),
            max_retries=3,
            retry_delays=[1, 2, 4]
        )
    elif action == 'verify':
        result = with_retry(
            lambda: verify_document(params.get('doc_token'), params.get('expected_content')),
            max_retries=3,
            retry_delays=[1, 2, 4]
        )
    else:
        result = {
            'success': False,
            'message': f'未知的action: {action}'
        }
    
    print(json.dumps(result, ensure_ascii=False))
    sys.exit(0 if result.get('success') else 1)


if __name__ == '__main__':
    main()
