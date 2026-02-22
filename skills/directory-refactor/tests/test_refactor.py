#!/usr/bin/env python3
"""测试脚本"""

import unittest
import tempfile
import shutil
from pathlib import Path

# 添加 lib 到路径
sys.path.insert(0, str(Path(__file__).parent / 'lib'))

from refactor import DirectoryRefactor, IntegrityError


class TestIntegrityCheck(unittest.TestCase):
    """测试完整性校验"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.workspace = Path(self.temp_dir) / 'workspace'
        self.workspace.mkdir()
        
        # 创建测试文件
        self.test_file = self.workspace / 'test.txt'
        self.test_file.write_text('Hello, World!')
        
        self.refactor = DirectoryRefactor(self.workspace)
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_sha256_consistency(self):
        """测试 SHA256 一致性"""
        hash1 = self.refactor._sha256_file(self.test_file)
        hash2 = self.refactor._sha256_file(self.test_file)
        self.assertEqual(hash1, hash2)
    
    def test_migrate_integrity(self):
        """测试迁移完整性"""
        source = self.workspace / 'source.txt'
        target = self.workspace / 'target.txt'
        source.write_text('Test content')
        
        task = self.refactor.migrate_with_integrity_check(source, target)
        
        self.assertTrue(target.exists())
        self.assertFalse(source.exists())
        self.assertTrue(task.verified)


class TestMDUpdate(unittest.TestCase):
    """测试 MD 增量更新"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.workspace = Path(self.temp_dir) / 'workspace'
        self.workspace.mkdir()
        
        # 创建测试 MD 文件
        self.md_file = self.workspace / 'test.md'
        self.md_file.write_text('# Test\n\n## Section1\nContent1\n\n## Section2\nContent2\n')
        
        self.refactor = DirectoryRefactor(self.workspace)
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_append_new_section(self):
        """测试追加新章节"""
        new_content = '## 工作目录\n\nTest content'
        
        task = self.refactor.update_md_incrementally(
            self.md_file, '工作目录', new_content
        )
        
        content = self.md_file.read_text()
        self.assertIn('## 工作目录', content)
        self.assertIn('## Section1', content)  # 原章节保留
        self.assertEqual(task.action, 'append')
    
    def test_replace_existing_section(self):
        """测试替换已有章节"""
        # 先追加章节
        self.refactor.update_md_incrementally(
            self.md_file, '工作目录', '## 工作目录\n\nOld content'
        )
        
        # 再替换
        new_content = '## 工作目录\n\nNew content'
        task = self.refactor.update_md_incrementally(
            self.md_file, '工作目录', new_content
        )
        
        content = self.md_file.read_text()
        self.assertIn('New content', content)
        self.assertNotIn('Old content', content)
        self.assertEqual(task.action, 'replace')


class TestPathFix(unittest.TestCase):
    """测试路径修复"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.workspace = Path(self.temp_dir) / 'workspace'
        self.workspace.mkdir()
        
        self.refactor = DirectoryRefactor(self.workspace)
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_python_path_replace(self):
        """测试 Python 脚本路径替换"""
        script = self.workspace / 'test.py'
        script.write_text('''
WORKSPACE = "/root/.openclaw/workspace/agents/xiaot3"
DATA_DIR = "/root/.openclaw/workspace/data"

def main():
    print(WORKSPACE)
''')
        
        mappings = {
            '/root/.openclaw/workspace/agents/xiaot3': '/root/.openclaw/workspace/projects/xiaot3'
        }
        
        task = self.refactor.update_script_paths(script, mappings)
        
        content = script.read_text()
        self.assertIn('projects/xiaot3', content)
        self.assertNotIn('agents/xiaot3', content)
        self.assertEqual(len(task.changes), 1)


if __name__ == '__main__':
    unittest.main()
