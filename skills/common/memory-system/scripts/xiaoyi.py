#!/usr/bin/env python3
"""
小忆Agent核心
基于记忆系统的智能记忆管理Agent
"""

import sys
import json
from pathlib import Path

# 添加scripts目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from store import store, get, update, delete
from retrieve import retrieve, retrieve_by_id, list_memories, get_stats
from migrate import migrate


class XiaoYiAgent:
    """
    小忆Agent - 智能记忆管理
    
    职责:
    1. 自动分类记忆（时间/内容/Agent/优先级）
    2. 智能检索与推荐
    3. 记忆生命周期管理
    4. 跨Agent记忆共享
    """
    
    def __init__(self):
        self.name = "xiaoyi"
        self.version = "1.0.0"
    
    def remember(self, content: str, agent: str = "unknown", 
                 priority: str = "medium", auto_categorize: bool = True) -> str:
        """
        智能存储记忆
        
        Args:
            content: 记忆内容
            agent: 来源Agent
            priority: 优先级
            auto_categorize: 是否自动分类
        
        Returns:
            memory_id: 记忆ID
        """
        if auto_categorize:
            category = self._categorize(content, priority)
        else:
            category = "medium"
        
        return store(content, category, agent, priority)
    
    def recall(self, query: str, context: dict = None, limit: int = 5) -> list:
        """
        智能回忆
        
        Args:
            query: 查询内容
            context: 上下文信息
            limit: 返回数量
        
        Returns:
            list: 相关记忆列表
        """
        # 基础检索
        results = retrieve(query, limit=limit)
        
        # 如果有上下文，进行上下文增强
        if context:
            results = self._context_enhance(results, context)
        
        return results
    
    def forget(self, memory_id: str, category: str) -> bool:
        """
        遗忘记忆
        
        Args:
            memory_id: 记忆ID
            category: 分类
        
        Returns:
            bool: 是否成功
        """
        return delete(memory_id, category)
    
    def consolidate(self) -> dict:
        """
        记忆整合 - 迁移过期记忆
        
        Returns:
            dict: 整合统计
        """
        return migrate()
    
    def summarize(self, agent: str = None, hours: int = 24) -> str:
        """
        记忆摘要
        
        Args:
            agent: 指定Agent（可选）
            hours: 时间范围
        
        Returns:
            str: 摘要文本
        """
        if agent:
            memories = list_memories(limit=50)
            memories = [m for m in memories if m.get('agent') == agent]
        else:
            # 获取最近的记忆
            memories = list_memories(limit=50)
            from datetime import datetime, timedelta
            cutoff = datetime.now() - timedelta(hours=hours)
            memories = [m for m in memories if datetime.fromisoformat(m.get('created_at', '2000-01-01')) > cutoff]
        
        if not memories:
            return "暂无相关记忆"
        
        # 生成摘要
        summary_parts = []
        summary_parts.append(f"共有 {len(memories)} 条记忆")
        
        # 按分类统计
        by_category = {}
        for m in memories:
            cat = m.get("category", "unknown")
            by_category[cat] = by_category.get(cat, 0) + 1
        
        summary_parts.append(f"分类分布: {by_category}")
        
        # 高优先级记忆
        high_priority = [m for m in memories if m.get("priority") == "high"]
        if high_priority:
            summary_parts.append(f"\n高优先级记忆 ({len(high_priority)}条):")
            for m in high_priority[:5]:
                summary_parts.append(f"  - {m.get('content', '')[:100]}")
        
        return "\n".join(summary_parts)
    
    def _categorize(self, content: str, priority: str) -> str:
        """
        自动分类
        
        分类规则:
        - state: 包含"状态"、"设置"、"偏好"等关键词，或高优先级且内容简短
        - long: 高优先级的重要信息
        - short: 临时性、时效性强的信息
        - medium: 默认
        """
        content_lower = content.lower()
        
        # 状态记忆关键词
        state_keywords = ["状态", "设置", "偏好", "喜欢", "讨厌", "习惯", "配置"]
        if any(kw in content_lower for kw in state_keywords):
            return "state"
        
        # 高优先级且简短 -> 可能是状态
        if priority == "high" and len(content) < 50:
            return "state"
        
        # 高优先级 -> 长期记忆
        if priority == "high":
            return "long"
        
        # 临时性关键词
        temp_keywords = ["临时", "暂时", "当前", "现在", "马上", "立刻"]
        if any(kw in content_lower for kw in temp_keywords):
            return "short"
        
        # 默认中期
        return "medium"
    
    def _context_enhance(self, results: list, context: dict) -> list:
        """
        上下文增强
        
        根据上下文信息调整排序
        """
        current_agent = context.get("agent")
        current_time = context.get("time")
        
        # 提升当前Agent的记忆权重
        if current_agent:
            for r in results:
                if r.get("agent") == current_agent:
                    r["_relevance_score"] = r.get("_relevance_score", 0) * 1.2
        
        # 重新排序
        results.sort(key=lambda x: x.get("_relevance_score", 0), reverse=True)
        
        return results
    
    def get_memory_stats(self) -> dict:
        """
        获取记忆统计
        
        Returns:
            dict: 统计信息
        """
        return get_stats()


# 全局实例
_xiaoyi = None


def get_xiaoyi() -> XiaoYiAgent:
    """获取小忆Agent实例"""
    global _xiaoyi
    if _xiaoyi is None:
        _xiaoyi = XiaoYiAgent()
    return _xiaoyi


# 便捷接口
def remember(content: str, agent: str = "unknown", priority: str = "medium") -> str:
    """存储记忆"""
    return get_xiaoyi().remember(content, agent, priority)


def recall(query: str, limit: int = 5) -> list:
    """回忆记忆"""
    return get_xiaoyi().recall(query, limit=limit)


def forget(memory_id: str, category: str) -> bool:
    """遗忘记忆"""
    return get_xiaoyi().forget(memory_id, category)


def consolidate() -> dict:
    """整合记忆"""
    return get_xiaoyi().consolidate()


def summarize(agent: str = None, hours: int = 24) -> str:
    """记忆摘要"""
    return get_xiaoyi().summarize(agent, hours)


if __name__ == "__main__":
    # 测试
    xy = get_xiaoyi()
    
    # 存储一些记忆
    mid1 = xy.remember("用户喜欢喝拿铁咖啡", "xiaozhi", "high")
    mid2 = xy.remember("明天下午3点有会议", "xiaozhi", "medium")
    mid3 = xy.remember("当前温度25度", "xiaozhi", "low")
    
    print(f"Stored memories: {mid1}, {mid2}, {mid3}")
    
    # 回忆
    results = xy.recall("咖啡", limit=5)
    print(f"\nRecall results:")
    for r in results:
        print(f"  - {r['content']} (category: {r['category']})")
    
    # 摘要
    print(f"\nSummary:\n{xy.summarize()}")
    
    # 统计
    print(f"\nStats: {xy.get_memory_stats()}")
