#!/usr/bin/env python3
"""
Directory Refactor - 全自动目录重构工具

核心算法：
1. 数据完整性：SHA256 校验
2. MD 增量更新：智能章节合并
3. 脚本路径替换：纯字符串替换
"""

import os
import sys
import json
import hashlib
import shutil
import re
import subprocess
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class RefactorError(Exception):
    """重构异常"""
    pass


class IntegrityError(RefactorError):
    """完整性校验失败"""
    pass


@dataclass
class MigrationTask:
    """迁移任务"""
    task_id: str
    source: str
    target: str
    task_type: str  # 'move', 'copy', 'archive'
    backup_path: Optional[str] = None
    verified: bool = False
    
    def to_dict(self):
        return asdict(self)


@dataclass
class MDUpdateTask:
    """MD 更新任务"""
    task_id: str
    file_path: str
    section_name: str
    new_content: str
    action: str  # 'replace', 'append'
    
    def to_dict(self):
        return asdict(self)


@dataclass
class PathFixTask:
    """路径修复任务"""
    task_id: str
    file_path: str
    path_mappings: Dict[str, str]
    changes: List[Dict] = None
    
    def __post_init__(self):
        if self.changes is None:
            self.changes = []
    
    def to_dict(self):
        return asdict(self)


class DirectoryRefactor:
    """目录重构主类"""
    
    def __init__(self, workspace: str, config_path: str = None):
        self.workspace = Path(workspace).resolve()
        self.config = self._load_config(config_path)
        self.timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        self.backup_dir = self.workspace / "data" / "backup" / f"refactor-{self.timestamp}"
        self.log_file = self.backup_dir / "refactor.log"
        self.transaction_log = []
        
    def _load_config(self, config_path: str = None) -> dict:
        """加载配置"""
        if config_path is None:
            config_path = Path(__file__).parent / "rules" / "directory-spec.json"
        
        with open(config_path, 'r') as f:
            return json.load(f)
    
    def _log(self, message: str, level: str = "INFO"):
        """记录日志"""
        log_entry = f"[{datetime.now().isoformat()}] [{level}] {message}\n"
        print(log_entry.strip())
        
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        with open(self.log_file, 'a') as f:
            f.write(log_entry)
    
    # ========== 算法 1: 数据完整性 ==========
    
    def _sha256_file(self, file_path: Path) -> str:
        """计算文件 SHA256"""
        sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                sha256.update(chunk)
        return sha256.hexdigest()
    
    def migrate_with_integrity_check(self, source: Path, target: Path) -> MigrationTask:
        """
        带完整性校验的迁移
        
        保证：迁移前后文件内容 bit 级一致
        """
        task_id = f"MIGRATE-{len(self.transaction_log)+1:03d}"
        
        self._log(f"开始迁移: {source} -> {target}")
        
        # 1. 计算源文件哈希
        source_hash = self._sha256_file(source)
        self._log(f"源文件哈希: {source_hash}")
        
        # 2. 创建备份
        backup_path = self.backup_dir / "files" / source.relative_to(self.workspace)
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, backup_path)
        self._log(f"备份创建: {backup_path}")
        
        # 3. 确保目标目录存在
        target.parent.mkdir(parents=True, exist_ok=True)
        
        # 4. 复制到目标（保留所有元数据）
        shutil.copy2(source, target)
        
        # 5. 计算目标文件哈希
        target_hash = self._sha256_file(target)
        self._log(f"目标文件哈希: {target_hash}")
        
        # 6. 验证一致性
        if source_hash != target_hash:
            # 删除目标文件
            target.unlink()
            raise IntegrityError(
                f"完整性校验失败: {source}\n"
                f"源哈希: {source_hash}\n"
                f"目标哈希: {target_hash}"
            )
        
        # 7. 删除源文件（仅在验证通过后）
        if source.is_dir():
            shutil.rmtree(source)
        else:
            source.unlink()
        
        self._log(f"迁移成功: {task_id}")
        
        task = MigrationTask(
            task_id=task_id,
            source=str(source),
            target=str(target),
            task_type='move',
            backup_path=str(backup_path),
            verified=True
        )
        
        self.transaction_log.append(task.to_dict())
        return task
    
    # ========== 算法 2: MD 增量更新 ==========
    
    def _find_section(self, content: str, section_name: str) -> Tuple[int, int, str]:
        """
        查找 MD 章节位置
        
        返回: (start_pos, end_pos, section_content)
        """
        # 匹配 ## 章节标题
        pattern = rf'##\s+{re.escape(section_name)}\s*\n'
        match = re.search(pattern, content)
        
        if not match:
            return -1, -1, ""
        
        start_pos = match.start()
        
        # 查找下一个同级或更高级章节
        next_section_pattern = r'\n##\s+'
        next_match = re.search(next_section_pattern, content[match.end():])
        
        if next_match:
            end_pos = match.end() + next_match.start()
        else:
            end_pos = len(content)
        
        section_content = content[start_pos:end_pos]
        return start_pos, end_pos, section_content
    
    def update_md_incrementally(self, file_path: Path, section_name: str, 
                                new_content: str) -> MDUpdateTask:
        """
        增量更新 Markdown 文档
        
        保证：只修改指定章节，其他内容完全保留
        """
        task_id = f"MDUPDATE-{len(self.transaction_log)+1:03d}"
        
        self._log(f"开始更新 MD: {file_path}, 章节: {section_name}")
        
        # 读取原文件
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        # 备份
        backup_path = self.backup_dir / "md" / file_path.relative_to(self.workspace)
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(original_content)
        
        # 查找章节
        start_pos, end_pos, old_section = self._find_section(original_content, section_name)
        
        if start_pos >= 0:
            # 章节存在：替换
            new_file_content = (
                original_content[:start_pos] +
                new_content + '\n\n' +
                original_content[end_pos:]
            )
            action = 'replace'
            self._log(f"替换章节: {section_name}")
        else:
            # 章节不存在：追加到文件末尾
            new_file_content = original_content.rstrip() + '\n\n' + new_content + '\n'
            action = 'append'
            self._log(f"追加章节: {section_name}")
        
        # 写入新内容
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_file_content)
        
        self._log(f"MD 更新成功: {task_id}")
        
        task = MDUpdateTask(
            task_id=task_id,
            file_path=str(file_path),
            section_name=section_name,
            new_content=new_content,
            action=action
        )
        
        self.transaction_log.append(task.to_dict())
        return task
    
    # ========== 算法 3: 脚本路径替换 ==========
    
    def _syntax_check(self, file_path: Path, content: str = None) -> bool:
        """语法检查"""
        if content is None:
            with open(file_path, 'r') as f:
                content = f.read()
        
        ext = file_path.suffix
        
        if ext == '.py':
            import py_compile
            try:
                py_compile.compile(str(file_path), doraise=True)
                return True
            except:
                return False
        elif ext in ['.js', '.ts']:
            # 使用 node --check
            result = subprocess.run(
                ['node', '--check', str(file_path)],
                capture_output=True
            )
            return result.returncode == 0
        elif ext == '.sh':
            result = subprocess.run(
                ['bash', '-n', str(file_path)],
                capture_output=True
            )
            return result.returncode == 0
        
        return True  # 其他类型跳过
    
    def update_script_paths(self, file_path: Path, 
                           path_mappings: Dict[str, str]) -> PathFixTask:
        """
        纯路径替换，不动逻辑
        
        保证：只替换字符串字面量中的路径
        """
        task_id = f"PATHFIX-{len(self.transaction_log)+1:03d}"
        
        self._log(f"开始修复路径: {file_path}")
        
        # 读取原文件
        with open(file_path, 'r', encoding='utf-8') as f:
            original_lines = f.readlines()
        
        # 备份
        backup_path = self.backup_dir / "scripts" / file_path.relative_to(self.workspace)
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.writelines(original_lines)
        
        modified_lines = []
        changes = []
        
        for line_no, line in enumerate(original_lines, 1):
            new_line = line
            
            # 只替换字符串字面量中的路径
            for old_path, new_path in path_mappings.items():
                # 匹配单引号或双引号包裹的路径
                patterns = [
                    rf'"{re.escape(old_path)}"',
                    rf"'{re.escape(old_path)}'",
                ]
                
                for pattern in patterns:
                    if re.search(pattern, new_line):
                        # 替换
                        new_line = re.sub(pattern, f'"{new_path}"', new_line)
                        changes.append({
                            'line': line_no,
                            'old': line.strip(),
                            'new': new_line.strip()
                        })
            
            modified_lines.append(new_line)
        
        # 语法检查
        temp_file = backup_path.with_suffix(backup_path.suffix + '.temp')
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.writelines(modified_lines)
        
        if not self._syntax_check(temp_file):
            temp_file.unlink()
            raise RefactorError(f"路径替换后语法错误: {file_path}")
        
        temp_file.unlink()
        
        # 写入修改后的内容
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(modified_lines)
        
        self._log(f"路径修复成功: {task_id}, 修改 {len(changes)} 处")
        
        task = PathFixTask(
            task_id=task_id,
            file_path=str(file_path),
            path_mappings=path_mappings,
            changes=changes
        )
        
        self.transaction_log.append(task.to_dict())
        return task
    
    # ========== 主流程 ==========
    
    def analyze(self) -> Dict:
        """分析目录结构"""
        self._log("开始分析目录结构...")
        
        issues = {
            'projects_in_wrong_place': [],
            'agents_missing_sections': [],
            'path_references': []
        }
        
        # 扫描根目录
        for item in self.workspace.iterdir():
            if item.is_dir() and item.name not in self.config.get('protected_dirs', []):
                # 检查是否为项目（有 package.json 或 src/）
                if (item / 'package.json').exists() or (item / 'src').exists():
                    issues['projects_in_wrong_place'].append({
                        'name': item.name,
                        'current': str(item.relative_to(self.workspace)),
                        'suggested': f"projects/{item.name}/"
                    })
        
        # 扫描 Agent 配置
        agents_dir = self.workspace / 'agents'
        if agents_dir.exists():
            for agent_dir in agents_dir.iterdir():
                if agent_dir.is_dir():
                    soul_file = agent_dir / 'SOUL.md'
                    if soul_file.exists():
                        with open(soul_file, 'r') as f:
                            content = f.read()
                        if '## 工作目录' not in content:
                            issues['agents_missing_sections'].append({
                                'agent': agent_dir.name,
                                'file': str(soul_file.relative_to(self.workspace)),
                                'missing': '工作目录章节'
                            })
        
        self._log(f"分析完成: 发现 {len(issues['projects_in_wrong_place'])} 个项目放错位置")
        
        return issues
    
    def generate_plan(self, issues: Dict) -> Dict:
        """生成执行计划"""
        self._log("生成执行计划...")
        
        plan = {
            'migrations': [],
            'md_updates': [],
            'path_fixes': []
        }
        
        # 生成迁移任务
        for project in issues.get('projects_in_wrong_place', []):
            plan['migrations'].append({
                'source': project['current'],
                'target': project['suggested'],
                'type': 'move'
            })
        
        # 生成 MD 更新任务
        for agent in issues.get('agents_missing_sections', []):
            plan['md_updates'].append({
                'file': agent['file'],
                'section': '工作目录',
                'template': 'agent-workdir-section.md'
            })
        
        self._log(f"计划生成: {len(plan['migrations'])} 个迁移, {len(plan['md_updates'])} 个MD更新")
        
        return plan
    
    def execute(self, plan: Dict) -> Dict:
        """执行重构计划"""
        self._log("开始执行重构...")
        
        results = {
            'migrations': [],
            'md_updates': [],
            'path_fixes': [],
            'errors': []
        }
        
        # 1. 执行迁移
        for mig in plan.get('migrations', []):
            try:
                source = self.workspace / mig['source']
                target = self.workspace / mig['target']
                task = self.migrate_with_integrity_check(source, target)
                results['migrations'].append(task.to_dict())
            except Exception as e:
                results['errors'].append({'task': mig, 'error': str(e)})
                self._log(f"迁移失败: {e}", "ERROR")
        
        # 2. 执行 MD 更新
        for upd in plan.get('md_updates', []):
            try:
                file_path = self.workspace / upd['file']
                
                # 加载模板
                template_path = Path(__file__).parent / 'templates' / upd['template']
                with open(template_path, 'r') as f:
                    new_content = f.read()
                
                task = self.update_md_incrementally(
                    file_path, 
                    upd['section'], 
                    new_content
                )
                results['md_updates'].append(task.to_dict())
            except Exception as e:
                results['errors'].append({'task': upd, 'error': str(e)})
                self._log(f"MD更新失败: {e}", "ERROR")
        
        # 3. 执行路径修复
        # TODO: 实现路径引用扫描和修复
        
        self._log("重构执行完成")
        return results
    
    def verify(self, results: Dict) -> bool:
        """验证重构结果"""
        self._log("开始验证...")
        
        all_passed = True
        
        # 验证迁移
        for mig in results.get('migrations', []):
            target = Path(mig['target'])
            if not target.exists():
                self._log(f"验证失败: {target} 不存在", "ERROR")
                all_passed = False
        
        # 验证 MD 更新
        for upd in results.get('md_updates', []):
            file_path = Path(upd['file_path'])
            with open(file_path, 'r') as f:
                content = f.read()
            if f"## {upd['section_name']}" not in content:
                self._log(f"验证失败: {file_path} 缺少 {upd['section_name']} 章节", "ERROR")
                all_passed = False
        
        if all_passed:
            self._log("所有验证通过")
        
        return all_passed
    
    def save_report(self, results: Dict):
        """保存执行报告"""
        report_path = self.backup_dir / f"report-{self.timestamp}.json"
        
        report = {
            'timestamp': self.timestamp,
            'workspace': str(self.workspace),
            'results': results,
            'transaction_log': self.transaction_log
        }
        
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        self._log(f"报告已保存: {report_path}")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Directory Refactor Tool')
    parser.add_argument('--workspace', default='.', help='Workspace path')
    parser.add_argument('--analyze', action='store_true', help='Analyze only')
    parser.add_argument('--execute', action='store_true', help='Execute refactor')
    parser.add_argument('--config', help='Config file path')
    
    args = parser.parse_args()
    
    refactor = DirectoryRefactor(args.workspace, args.config)
    
    if args.analyze:
        issues = refactor.analyze()
        print(json.dumps(issues, indent=2))
    
    elif args.execute:
        issues = refactor.analyze()
        plan = refactor.generate_plan(issues)
        results = refactor.execute(plan)
        
        if refactor.verify(results):
            refactor.save_report(results)
            print("✅ 重构成功完成")
        else:
            print("❌ 验证失败，请检查日志")
            sys.exit(1)
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
