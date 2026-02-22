#!/usr/bin/env python3
"""
记忆存储接口
提供短期/中期/长期/状态四类记忆存储
"""

import os
import json
import uuid
import re
from datetime import datetime, timedelta
from pathlib import Path

# 配置
BASE_PATH = Path("./data/memory")
CATEGORIES = ["short", "medium", "long", "state"]


def _ensure_dirs():
    """确保目录结构存在"""
    for cat in CATEGORIES + ["archive"]:
        (BASE_PATH / cat).mkdir(parents=True, exist_ok=True)


def _extract_keywords(content: str) -> list:
    """从内容中提取关键词（简单分词）"""
    # 去除标点，分词
    words = re.findall(r'[\u4e00-\u9fa5]{2,}|[a-zA-Z]+', content)
    # 过滤常见停用词
    stopwords = {"的", "了", "是", "在", "我", "有", "和", "就", "不", "人", "都", "一", "一个", "上", "也", "很", "到", "说", "要", "去", "你", "会", "着", "没有", "看", "好", "自己", "这"}
    keywords = [w for w in words if len(w) >= 2 and w not in stopwords]
    return list(set(keywords))[:10]  # 最多10个关键词


def _generate_id() -> str:
    """生成记忆ID"""
    return f"mem_{uuid.uuid4().hex[:12]}"


def _get_memory_path(memory_id: str, category: str) -> Path:
    """获取记忆文件路径"""
    return BASE_PATH / category / f"{memory_id}.json"


def store(content: str, category: str, agent: str, priority: str) -> str:
    """
    存储记忆
    
    Args:
        content: 记忆内容
        category: 分类 (short/medium/long/state)
        agent: 来源Agent
        priority: 优先级 (high/medium/low)
    
    Returns:
        memory_id: 记忆唯一ID
    """
    _ensure_dirs()
    
    if category not in CATEGORIES:
        raise ValueError(f"Invalid category: {category}. Must be one of {CATEGORIES}")
    
    memory_id = _generate_id()
    now = datetime.now().isoformat()
    
    memory_data = {
        "id": memory_id,
        "content": content,
        "category": category,
        "agent": agent,
        "priority": priority,
        "created_at": now,
        "updated_at": now,
        "access_count": 0,
        "last_accessed": None,
        "keywords": _extract_keywords(content)
    }
    
    file_path = _get_memory_path(memory_id, category)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(memory_data, f, ensure_ascii=False, indent=2)
    
    return memory_id


def update(memory_id: str, category: str, **kwargs) -> bool:
    """
    更新记忆
    
    Args:
        memory_id: 记忆ID
        category: 分类
        **kwargs: 要更新的字段
    
    Returns:
        bool: 是否成功
    """
    file_path = _get_memory_path(memory_id, category)
    
    if not file_path.exists():
        return False
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 更新字段
    for key, value in kwargs.items():
        if key in data:
            data[key] = value
    
    data["updated_at"] = datetime.now().isoformat()
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return True


def get(memory_id: str, category: str) -> dict:
    """
    获取单个记忆
    
    Args:
        memory_id: 记忆ID
        category: 分类
    
    Returns:
        dict: 记忆数据，不存在返回None
    """
    file_path = _get_memory_path(memory_id, category)
    
    if not file_path.exists():
        return None
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 更新访问计数
    data["access_count"] += 1
    data["last_accessed"] = datetime.now().isoformat()
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return data


def delete(memory_id: str, category: str) -> bool:
    """
    删除记忆
    
    Args:
        memory_id: 记忆ID
        category: 分类
    
    Returns:
        bool: 是否成功
    """
    file_path = _get_memory_path(memory_id, category)
    
    if file_path.exists():
        file_path.unlink()
        return True
    return False


if __name__ == "__main__":
    # 测试
    mid = store("用户喜欢喝拿铁咖啡", "long", "xiaozhi", "medium")
    print(f"Stored memory: {mid}")
    
    data = get(mid, "long")
    print(f"Retrieved: {data}")
