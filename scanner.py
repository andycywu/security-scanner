#!/usr/bin/env python3
"""
🔒 Security Scanner - AI Skill 資安掃描器
掃描程式碼中的安全漏洞
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime

# 危險模式清單
DANGEROUS_PATTERNS = [
    {
        "name": "API Key 洩漏",
        "pattern": r"(?i)(api_key|apikey|secret|token|password|pwd)[\s=:\"]+[a-zA-Z0-9_\-]{20,}",
        "severity": "CRITICAL"
    },
    {
        "name": "eval() 使用",
        "pattern": r"\beval\s*\(",
        "severity": "HIGH"
    },
    {
        "name": "exec() 使用",
        "pattern": r"\bexec\s*\(",
        "severity": "HIGH"
    },
    {
        "name": "pickle 反序列化",
        "pattern": r"\bpickle\.(load|loads)\s*\(",
        "severity": "HIGH"
    },
    {
        "name": "SQL 注入風險",
        "pattern": r"(execute|execute_script|query)\s*\([^)]*%\s*[as]",
        "severity": "HIGH"
    },
    {
        "name": "命令注入",
        "pattern": r"\bos\.system\s*\(|subprocess.*shell\s*=\s*True",
        "severity": "CRITICAL"
    },
    {
        "name": "檔案任意讀寫",
        "pattern": r"(open|file)\s*\([^)]*[\"|\']..[\"|\']",
        "severity": "MEDIUM"
    },
    {
        "name": "環境變數暴露",
        "pattern": r"os\.environ[\[\"'].*[\"']",
        "severity": "LOW"
    }
]

class SecurityScanner:
    """資安掃描器"""
    
    def __init__(self, target_path: str):
        self.target_path = target_path
        self.findings = []
        self.files_scanned = 0
        self.lines_scanned = 0
    
    def scan_file(self, file_path: Path) -> list:
        """掃描單個檔案"""
        findings = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')
                self.lines_scanned += len(lines)
                
                for i, line in enumerate(lines, 1):
                    for pattern_info in DANGEROUS_PATTERNS:
                        if re.search(pattern_info["pattern"], line):
                            findings.append({
                                "file": str(file_path),
                                "line": i,
                                "issue": pattern_info["name"],
                                "severity": pattern_info["severity"],
                                "code": line.strip()[:100]
                            })
        except Exception as e:
            findings.append({
                "file": str(file_path),
                "line": 0,
                "issue": f"無法讀取檔案: {e}",
                "severity": "INFO",
                "code": ""
            })
        
        return findings
    
    def scan_directory(self) -> dict:
        """掃描整個目錄"""
        target = Path(self.target_path)
        
        if not target.exists():
            return {"error": f"路徑不存在: {self.target_path}"}
        
        code_extensions = {'.py', '.js', '.ts', '.json', '.yml', '.yaml', '.env'}
        
        for file_path in target.rglob('*'):
            if file_path.is_file() and file_path.suffix in code_extensions:
                self.files_scanned += 1
                self.findings.extend(self.scan_file(file_path))
        
        return self.generate_report()
    
    def generate_report(self) -> dict:
        """生成掃描報告"""
        critical = len([f for f in self.findings if f["severity"] == "CRITICAL"])
        high = len([f for f in self.findings if f["severity"] == "HIGH"])
        medium = len([f for f in self.findings if f["severity"] == "MEDIUM"])
        low = len([f for f in self.findings if f["severity"] == "LOW"])
        
        report = {
            "scan_time": datetime.now().isoformat(),
            "target": self.target_path,
            "summary": {
                "files_scanned": self.files_scanned,
                "lines_scanned": self.lines_scanned,
                "total_issues": len(self.findings),
                "critical": critical,
                "high": high,
                "medium": medium,
                "low": low
            },
            "risk_score": self.calculate_risk_score(critical, high, medium, low),
            "findings": self.findings[:20],  # 最多顯示 20 個
            "recommendations": self.get_recommendations(critical, high)
        }
        
        return report
    
    def calculate_risk_score(self, critical, high, medium, low) -> str:
        """計算風險等級"""
        score = critical * 100 + high * 50 + medium * 20 + low * 5
        
        if score >= 100:
            return "🔴 極高風險"
        elif score >= 50:
            return "🟠 高風險"
        elif score >= 20:
            return "🟡 中風險"
        else:
            return "🟢 低風險"
    
    def get_recommendations(self, critical, high) -> list:
        """取得修復建議"""
        recs = []
        
        if critical > 0:
            recs.append("⚠️ 發現 CRITICAL 等級漏洞，請立即處理 API Key 洩漏問題")
        
        if high > 0:
            recs.append("🔧 建議移除或重構危險的 eval/exec 使用")
        
        recs.append("📚 使用環境變數管理敏感資訊，而非寫死在程式碼中")
        recs.append("🔐 定期執行資安掃描，確保程式碼安全")
        
        return recs

def main():
    """主程式"""
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python security_scanner.py <目標路徑>")
        print("範例: python security_scanner.py /path/to/skill")
        sys.exit(1)
    
    target = sys.argv[1]
    scanner = SecurityScanner(target)
    report = scanner.scan_directory()
    
    # 輸出報告
    print("\n" + "="*60)
    print("🔒 Security Scanner Report")
    print("="*60)
    print(f"\n掃描時間: {report['scan_time']}")
    print(f"目標路徑: {report['target']}")
    print(f"\n📊 掃描結果:")
    print(f"   檔案數: {report['summary']['files_scanned']}")
    print(f"   程式碼行數: {report['summary']['lines_scanned']}")
    print(f"   問題數: {report['summary']['total_issues']}")
    print(f"\n🚨 風險等級: {report['risk_score']}")
    print(f"   🔴 Critical: {report['summary']['critical']}")
    print(f"   🟠 High: {report['summary']['high']}")
    print(f"   🟡 Medium: {report['summary']['medium']}")
    print(f"   🟢 Low: {report['summary']['low']}")
    
    if report['findings']:
        print(f"\n📋 發現的問題 (前20項):")
        for i, finding in enumerate(report['findings'], 1):
            print(f"\n{i}. [{finding['severity']}] {finding['issue']}")
            print(f"   檔案: {finding['file']}")
            if finding['line'] > 0:
                print(f"   行號: {finding['line']}")
            print(f"   程式碼: {finding['code']}")
    
    print(f"\n💡 修復建議:")
    for rec in report['recommendations']:
        print(f"   {rec}")
    
    print("\n" + "="*60)
    print("掃描完成！")
    print("="*60)

if __name__ == "__main__":
    main()
