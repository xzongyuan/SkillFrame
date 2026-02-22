#!/usr/bin/env python3
"""
记忆迁移接口
自动迁移过期记忆到归档
"""

import os
import json
import shutil
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple
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

def get_archive_path():
    """获取归档路径"""
    config = load_config()
    archive_path = config.get('migration', {}).get('archive_path', './data/memory/archive')
    if not os.path.isabs(archive_path):
        archive_path = Path(__file__).parent.parent / archive_path
    return Path(archive_path)

def is_expired(memory: Dict) -> bool:
    """
    检查记忆是否过期
    
    Args:
        memory: 记忆数据
    
    Returns:
        bool: 是否过期
    """
    expire_at = memory.get('expire_at')
    if not expire_at:
        return False  # 没有过期时间 = 不过期
    
    try:
        expire_time = datetime.fromisoformat(expire_at)
        return datetime.now() > expire_time
    except:
        return False

def should_migrate_by_age(memory: Dict, category: str) -> bool:
    """
    根据年龄判断是否应该迁移
    
    Args:
        memory: 记忆数据
        category: 分类
    
    Returns:
        bool: 是否应该迁移
    """
    config = load_config()
    ttl_days = config.get('categories', {}).get(category, {}).get('ttl_days', 7)
    
    if ttl_days < 0:
        return False  # 不过期
    
    created_at = memory.get('created_at')
    if not created_at:
        return False
    
    try:
        created_time = datetime.fromisoformat(created_at)
        age_days = (datetime.now() - created_time).days
        return age_days > ttl_days
    except:
        return False

def archive_memory(memory: Dict, category: str) -> bool:
    """
    归档记忆
    
    Args:
        memory: 记忆数据
        category: 原分类
    
    Returns:
        bool: 是否成功
    """
    archive_path = get_archive_path()
    memory_id = memory['id']
    
    # 创建年月目录
    now = datetime.now()
    archive_dir = archive_path / f"{now.year}" / f"{now.month:02d}"
    archive_dir.mkdir(parents=True, exist_ok=True)
    
    # 添加归档信息
    memory['_archived'] = {
        'archived_at': datetime.now().isoformat(),
        'original_category': category
    }
    
    # 保存到归档
    archive_file = archive_dir / f"{memory_id}.json"
    try:
        with open(archive_file, 'w', encoding='utf-8') as f:
            json.dump(memory, f, ensure_ascii=False, indent=2)
        return True
    except IOError:
        return False

def delete_memory(memory_id: str, category: str) -> bool:
    """
    删除记忆
    
    Args:
        memory_id: 记忆ID
        category: 分类
    
    Returns:
        bool: 是否成功
    """
    base_path = get_storage_path()
    file_path = base_path / category / f"{memory_id}.json"
    
    try:
        if file_path.exists():
            file_path.unlink()
        return True
    except IOError:
        return False

def migrate_category(category: str, dry_run: bool = False) -> Dict:
    """
    迁移指定分类的过期记忆
    
    Args:
        category: 分类
        dry_run: 是否仅预览，不执行
    
    Returns:
        Dict: 迁移统计
    """
    base_path = get_storage_path()
    category_path = base_path / category
    
    if not category_path.exists():
        return {'migrated': 0, 'failed': 0, 'skipped': 0, 'memories': []}
    
    stats = {
        'migrated': 0,
        'failed': 0,
        'skipped': 0,
        'memories': []
    }
    
    for file_path in category_path.glob("*.json"):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                memory = json.load(f)
            
            # 检查是否应该迁移
            should_migrate = is_expired(memory) or should_migrate_by_age(memory, category)
            
            if should_migrate:
                memory_info = {
                    'id': memory['id'],
                    'content': memory['content'][:50] + '...' if len(memory['content']) > 50 else memory['content'],
                    'created_at': memory.get('created_at', 'unknown')
                }
                
                if not dry_run:
                    # 归档
                    if archive_memory(memory, category):
                        # 删除原文件
                        if delete_memory(memory['id'], category):
                            stats['migrated'] += 1
                            stats['memories'].append(memory_info)
                        else:
                            stats['failed'] += 1
                    else:
                        stats['failed'] += 1
                else:
                    stats['migrated'] += 1
                    stats['memories'].append(memory_info)
            else:
                stats['skipped'] += 1
                
        except (json.JSONDecodeError, IOError) as e:
            stats['failed'] += 1
            continue
    
    return stats

def migrate(dry_run: bool = False) -> Dict:
    """
    执行迁移
    
    Args:
        dry_run: 是否仅预览，不执行
    
    Returns:
        Dict: 迁移统计
    """
    categories = ['short', 'medium', 'long']
    
    total_stats = {
        'dry_run': dry_run,
        'timestamp': datetime.now().isoformat(),
        'categories': {},
        'total_migrated': 0,
        'total_failed': 0,
        'total_skipped': 0
    }
    
    for category in categories:
        stats = migrate_category(category, dry_run)
        total_stats['categories'][category] = stats
        total_stats['total_migrated'] += stats['migrated']
        total_stats['total_failed'] += stats['failed']
        total_stats['total_skipped'] += stats['skipped']
    
    return total_stats

def cleanup_archive(days: int = 365) -> Dict:
    """
    清理旧归档
    
    Args:
        days: 保留天数
    
    Returns:
        Dict: 清理统计
    """
    archive_path = get_archive_path()
    cutoff_date = datetime.now() - timedelta(days=days)
    
    stats = {
        'deleted': 0,
        'failed': 0,
        'bytes_freed': 0
    }
    
    if not archive_path.exists():
        return stats
    
    for file_path in archive_path.rglob("*.json"):
        try:
            mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
            if mtime < cutoff_date:
                size = file_path.stat().st_size
                file_path.unlink()
                stats['deleted'] += 1
                stats['bytes_freed'] += size
        except (IOError, OSError):
            stats['failed'] += 1
            continue
    
    return stats

def get_stats() -> Dict:
    """
    获取记忆系统统计
    
    Returns:
        Dict: 统计信息
    """
    base_path = get_storage_path()
    categories = ['short', 'medium', 'long', 'state']
    
    stats = {
        'categories': {},
        'total_memories': 0,
        'total_size_bytes': 0
    }
    
    for category in categories:
        category_path = base_path / category
        if not category_path.exists():
            stats['categories'][category] = {
                'count': 0,
                'size_bytes': 0
            }
            continue
        
        count = 0
        size = 0
        
        for file_path in category_path.glob("*.json"):
            count += 1
            size += file_path.stat().st_size
        
        stats['categories'][category] = {
            'count': count,
            'size_bytes': size
        }
        stats['total_memories'] += count
        stats['total_size_bytes'] += size
    
    return stats

def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description='记忆迁移接口')
    parser.add_argument('--dry-run', '-d', action='store_true',
                       help='仅预览，不执行实际迁移')
    parser.add_argument('--cleanup', '-c', type=int, metavar='DAYS',
                       help='清理指定天数前的归档')
    parser.add_argument('--stats', '-s', action='store_true',
                       help='显示统计信息')
    parser.add_argument('--format', '-f', choices=['json', 'text'], default='text',
                       help='输出格式')
    
    args = parser.parse_args()
    
    if args.stats:
        stats = get_stats()
        if args.format == 'json':
            print(json.dumps(stats, ensure_ascii=False, indent=2))
        else:
            print("记忆系统统计:")
            print(f"总记忆数: {stats['total_memories']}")
            print(f"总大小: {stats['total_size_bytes'] / 1024:.2f} KB")
            print("\n分类详情:")
            for cat, cat_stats in stats['categories'].items():
                print(f"  {cat}: {cat_stats['count']} 条 ({cat_stats['size_bytes'] / 1024:.2f} KB)")
    
    elif args.cleanup:
        stats = cleanup_archive(args.cleanup)
        if args.format == 'json':
            print(json.dumps(stats, ensure_ascii=False, indent=2))
        else:
            print(f"归档清理完成:")
            print(f"  删除文件: {stats['deleted']}")
            print(f"  释放空间: {stats['bytes_freed'] / 1024:.2f} KB")
            if stats['failed'] > 0:
                print(f"  失败: {stats['failed']}")
    
    else:
        # 执行迁移
        results = migrate(dry_run=args.dry_run)
        
        if args.format == 'json':
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            mode = "[预览模式]" if args.dry_run else "[执行模式]"
            print(f"记忆迁移完成 {mode}")
            print(f"时间: {results['timestamp']}")
            print(f"\n总计:")
            print(f"  迁移: {results['total_migrated']}")
            print(f"  失败: {results['total_failed']}")
            print(f"  跳过: {results['total_skipped']}")
            
            for cat, cat_stats in results['categories'].items():
                if cat_stats['migrated'] > 0 or cat_stats['failed'] > 0:
                    print(f"\n  {cat}:")
                    print(f"    迁移: {cat_stats['migrated']}")
                    if cat_stats['memories']:
                        for mem in cat_stats['memories'][:3]:  # 只显示前3个
                            print(f"      - {mem['id']}: {mem['content'][:30]}...")
                        if len(cat_stats['memories']) > 3:
                            print(f"      ... 还有 {len(cat_stats['memories']) - 3} 条")

if __name__ == '__main__':
    main()
