#!/usr/bin/env python3
"""
记忆检索接口
支持关键词匹配检索
"""

import os
import json
import re
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import yaml

# 加载配置
CONFIG_PATH = Path(__file__).parent.parent / "config.yaml"

def load_config():
    """加载配置文件"""
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    return {}

def get_storage_path():
    """获取存储基础路径"""
    config = load_config()
    base_path = config.get('storage', {}).get('base_path', './data/memory')
    if not os.path.isabs(base_path):
        base_path = Path(__file__).parent.parent / base_path
    return Path(base_path)

def load_all_memories(category: str = None) -> List[Dict]:
    """
    加载所有记忆
    
    Args:
        category: 指定分类，None则加载所有
    
    Returns:
        List[Dict]: 记忆列表
    """
    base_path = get_storage_path()
    memories = []
    
    categories = [category] if category else ['short', 'medium', 'long', 'state']
    
    for cat in categories:
        category_path = base_path / cat
        if not category_path.exists():
            continue
        
        for file_path in category_path.glob("*.json"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    memory = json.load(f)
                    memories.append(memory)
            except (json.JSONDecodeError, IOError):
                continue
    
    return memories

def keyword_match(query: str, content: str) -> float:
    """
    关键词匹配评分
    
    Args:
        query: 查询关键词
        content: 记忆内容
    
    Returns:
        float: 匹配分数 (0-1)
    """
    query = query.lower().strip()
    content_lower = content.lower()
    
    # 完全匹配
    if query == content_lower:
        return 1.0
    
    # 包含匹配
    if query in content_lower:
        return 0.8
    
    # 分词匹配
    query_words = set(re.findall(r'\w+', query))
    content_words = set(re.findall(r'\w+', content_lower))
    
    if not query_words:
        return 0.0
    
    # 计算匹配率
    matched = query_words & content_words
    match_ratio = len(matched) / len(query_words)
    
    return match_ratio * 0.6  # 分词匹配最高0.6分

def calculate_relevance(memory: Dict, query: str) -> float:
    """
    计算记忆与查询的相关性分数
    
    Args:
        memory: 记忆数据
        query: 查询关键词
    
    Returns:
        float: 相关性分数
    """
    scores = []
    
    # 内容匹配
    content_score = keyword_match(query, memory.get('content', ''))
    scores.append(content_score * 1.0)  # 内容权重最高
    
    # 内容类型匹配
    content_type = memory.get('content_type', '')
    if content_type and content_type in query.lower():
        scores.append(0.3)
    
    # Agent匹配
    agent = memory.get('agent', '')
    if agent and agent in query.lower():
        scores.append(0.2)
    
    # 优先级加权
    priority_weights = {'high': 1.2, 'medium': 1.0, 'low': 0.8}
    priority = memory.get('priority', 'medium')
    priority_weight = priority_weights.get(priority, 1.0)
    
    # 访问次数加权 (越常访问越重要)
    access_count = memory.get('access_count', 0)
    access_weight = 1.0 + min(access_count * 0.05, 0.3)  # 最多加0.3
    
    base_score = max(scores) if scores else 0.0
    final_score = base_score * priority_weight * access_weight
    
    return min(final_score, 1.0)

def update_access_stats(memory_id: str, category: str):
    """更新访问统计"""
    base_path = get_storage_path()
    file_path = base_path / category / f"{memory_id}.json"
    
    if not file_path.exists():
        return
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            memory = json.load(f)
        
        memory['access_count'] = memory.get('access_count', 0) + 1
        memory['last_accessed'] = datetime.now().isoformat()
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(memory, f, ensure_ascii=False, indent=2)
    except (json.JSONDecodeError, IOError):
        pass

def retrieve(query: str, category: str = None, limit: int = 10, 
             content_type: str = None, agent: str = None,
             min_relevance: float = 0.0) -> List[Dict]:
    """
    检索记忆
    
    Args:
        query: 查询关键词
        category: 指定分类
        limit: 返回数量限制
        content_type: 内容类型过滤
        agent: Agent过滤
        min_relevance: 最小相关性阈值
    
    Returns:
        List[Dict]: 匹配的记忆列表
    """
    # 加载所有记忆
    memories = load_all_memories(category)
    
    # 过滤和评分
    results = []
    for memory in memories:
        # 内容类型过滤
        if content_type and memory.get('content_type') != content_type:
            continue
        
        # Agent过滤
        if agent and memory.get('agent') != agent:
            continue
        
        # 检查是否过期
        expire_at = memory.get('expire_at')
        if expire_at:
            try:
                expire_time = datetime.fromisoformat(expire_at)
                if datetime.now() > expire_time:
                    continue  # 跳过过期记忆
            except:
                pass
        
        # 计算相关性
        relevance = calculate_relevance(memory, query)
        
        if relevance >= min_relevance:
            memory['_relevance'] = relevance
            results.append(memory)
    
    # 按相关性排序
    results.sort(key=lambda x: x['_relevance'], reverse=True)
    
    # 限制数量
    results = results[:limit]
    
    # 更新访问统计
    for memory in results:
        update_access_stats(memory['id'], memory['category'])
        # 移除内部字段
        memory.pop('_relevance', None)
    
    return results

def retrieve_by_id(memory_id: str) -> Optional[Dict]:
    """
    通过ID检索记忆
    
    Args:
        memory_id: 记忆ID
    
    Returns:
        Dict or None: 记忆数据
    """
    base_path = get_storage_path()
    categories = ['short', 'medium', 'long', 'state']
    
    for category in categories:
        file_path = base_path / category / f"{memory_id}.json"
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    memory = json.load(f)
                
                # 更新访问统计
                update_access_stats(memory_id, category)
                return memory
            except (json.JSONDecodeError, IOError):
                continue
    
    return None

def list_memories(category: str = None, limit: int = 100) -> List[Dict]:
    """
    列出所有记忆（用于管理）
    
    Args:
        category: 指定分类
        limit: 数量限制
    
    Returns:
        List[Dict]: 记忆列表
    """
    memories = load_all_memories(category)
    
    # 按创建时间排序（最新的在前）
    memories.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    
    return memories[:limit]

def get_stats() -> dict:
    """
    获取记忆统计信息
    
    Returns:
        dict: 统计信息
    """
    stats = {
        "total": 0,
        "by_category": {},
        "by_agent": {},
        "by_priority": {}
    }
    
    memories = load_all_memories()
    stats["total"] = len(memories)
    
    for memory in memories:
        # 按分类统计
        cat = memory.get("category", "unknown")
        stats["by_category"][cat] = stats["by_category"].get(cat, 0) + 1
        
        # 按Agent统计
        agent = memory.get("agent", "unknown")
        stats["by_agent"][agent] = stats["by_agent"].get(agent, 0) + 1
        
        # 按优先级统计
        priority = memory.get("priority", "unknown")
        stats["by_priority"][priority] = stats["by_priority"].get(priority, 0) + 1
    
    return stats

def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description='记忆检索接口')
    parser.add_argument('--query', '-q', required=True, help='查询关键词')
    parser.add_argument('--category', '-c', 
                       choices=['short', 'medium', 'long', 'state'],
                       help='指定分类')
    parser.add_argument('--limit', '-l', type=int, default=10, help='返回数量限制')
    parser.add_argument('--content-type', '-t',
                       choices=['fact', 'preference', 'task', 'context', 'other'],
                       help='内容类型过滤')
    parser.add_argument('--agent', '-a', help='Agent过滤')
    parser.add_argument('--min-relevance', '-r', type=float, default=0.0,
                       help='最小相关性阈值 (0-1)')
    parser.add_argument('--format', '-f', choices=['json', 'text'], default='text',
                       help='输出格式')
    
    args = parser.parse_args()
    
    # 检索记忆
    results = retrieve(
        query=args.query,
        category=args.category,
        limit=args.limit,
        content_type=args.content_type,
        agent=args.agent,
        min_relevance=args.min_relevance
    )
    
    if args.format == 'json':
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        if not results:
            print("未找到匹配的记忆")
        else:
            print(f"找到 {len(results)} 条记忆:\n")
            for i, memory in enumerate(results, 1):
                print(f"[{i}] ID: {memory['id']}")
                print(f"    分类: {memory['category']}")
                print(f"    类型: {memory.get('content_type', 'other')}")
                print(f"    优先级: {memory.get('priority', 'medium')}")
                print(f"    Agent: {memory.get('agent', 'unknown')}")
                print(f"    内容: {memory['content'][:100]}..." if len(memory['content']) > 100 else f"    内容: {memory['content']}")
                print(f"    创建时间: {memory.get('created_at', 'unknown')}")
                print()

if __name__ == '__main__':
    main()
