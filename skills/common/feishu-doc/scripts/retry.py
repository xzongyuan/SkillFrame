#!/usr/bin/env python3
"""
重试机制
"""

import time
import random


def with_retry(func, max_retries=3, retry_delays=None, exceptions=(Exception,)):
    """
    带重试的函数执行
    
    Args:
        func: 要执行的函数
        max_retries: 最大重试次数
        retry_delays: 重试延迟列表（秒）
        exceptions: 捕获的异常类型
        
    Returns:
        函数执行结果
        
    Raises:
        最后一次异常
    """
    if retry_delays is None:
        retry_delays = [1, 2, 4]
    
    last_exception = None
    
    for attempt in range(max_retries + 1):
        try:
            return func()
        except exceptions as e:
            last_exception = e
            
            if attempt < max_retries:
                delay = retry_delays[min(attempt, len(retry_delays) - 1)]
                # 添加随机抖动，避免惊群效应
                jitter = random.uniform(0, 0.5)
                time.sleep(delay + jitter)
            else:
                break
    
    # 所有重试都失败了
    raise last_exception


def classify_error(error) -> tuple:
    """
    错误分类
    
    Returns:
        (是否可重试, 错误类型, 建议操作)
    """
    error_msg = str(error).lower()
    
    # 网络错误 - 可重试
    if any(kw in error_msg for kw in ['timeout', 'connection', 'network', 'temporarily']):
        return True, 'network', '等待后重试'
    
    # 速率限制 - 可重试（增加延迟）
    if any(kw in error_msg for kw in ['rate limit', 'too many requests', '429']):
        return True, 'rate_limit', '增加延迟后重试'
    
    # 服务器错误 - 可重试
    if any(kw in error_msg for kw in ['500', '502', '503', '504', 'internal server error']):
        return True, 'server', '等待后重试'
    
    # 认证错误 - 不可重试
    if any(kw in error_msg for kw in ['unauthorized', 'forbidden', '401', '403']):
        return False, 'auth', '检查认证信息'
    
    # 参数错误 - 不可重试
    if any(kw in error_msg for kw in ['invalid', 'bad request', '400']):
        return False, 'param', '检查参数'
    
    # 默认可重试
    return True, 'unknown', '尝试重试'


if __name__ == '__main__':
    # 测试重试机制
    counter = [0]
    
    def test_func():
        counter[0] += 1
        if counter[0] < 3:
            raise Exception(f"模拟错误 #{counter[0]}")
        return {"success": True, "attempts": counter[0]}
    
    try:
        result = with_retry(test_func, max_retries=3, retry_delays=[0.1, 0.2, 0.4])
        print(f"成功: {result}")
    except Exception as e:
        print(f"最终失败: {e}")
