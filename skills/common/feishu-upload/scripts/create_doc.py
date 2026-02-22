#!/usr/bin/env python3
"""
飞书文档创建脚本
"""
import argparse
import json
import sys

def create_doc(title, folder=None):
    """创建飞书文档"""
    # TODO: 实现飞书API调用
    # 返回 doc_token 和 url
    result = {
        "doc_token": "doc_xxx",
        "url": f"https://feishu.cn/docx/xxx",
        "title": title
    }
    print(json.dumps(result))
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--title", required=True)
    parser.add_argument("--folder", default=None)
    args = parser.parse_args()
    
    create_doc(args.title, args.folder)
