#!/usr/bin/env python3
"""
标注一致性分析工具
用于计算IAA系数和模型准确率，支持论文写作
"""
import sys
import os
from pathlib import Path

# 添加当前目录到Python路径
sys.path.append(str(Path(__file__).parent))

from annotation_analysis import AnnotationAnalyzer

def check_dependencies():
    """检查依赖包"""
    required_packages = ['pandas', 'numpy']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ 缺少依赖包: {', '.join(missing_packages)}")
        print("请运行: pip install pandas numpy")
        return False
    
    return True

def main():
    """主函数"""
    print("🔬 标注一致性分析工具")
    print("=" * 60)
    
    # 检查依赖
    if not check_dependencies():
        return
    
    # 检查标注数据
    annotated_dir = Path("annotated_data")
    if not annotated_dir.exists():
        print("❌ 未找到标注数据目录")
        print("请先使用标注平台对数据进行人工标注")
        print(f"标注文件应保存在: {annotated_dir.absolute()}")
        return
    
    # 查找标注文件
    annotated_files = list(annotated_dir.glob("annotated_*.json"))
    if not annotated_files:
        print("❌ 未找到标注数据文件")
        print("请先使用标注平台对数据进行人工标注")
        return
    
    print(f"📁 找到 {len(annotated_files)} 个标注文件:")
    for i, file in enumerate(annotated_files, 1):
        print(f"  {i}. {file.name}")
    
    # 选择文件进行分析
    if len(annotated_files) == 1:
        selected_file = annotated_files[0]
        print(f"\n🎯 自动选择: {selected_file.name}")
    else:
        try:
            choice = input(f"\n请选择要分析的文件 (1-{len(annotated_files)}): ")
            idx = int(choice) - 1
            if 0 <= idx < len(annotated_files):
                selected_file = annotated_files[idx]
            else:
                print("❌ 无效选择")
                return
        except (ValueError, KeyboardInterrupt):
            print("❌ 操作取消")
            return
    
    try:
        print(f"\n📊 开始分析: {selected_file.name}")
        print("-" * 40)
        
        # 运行分析
        analyzer = AnnotationAnalyzer(str(selected_file))
        
        # 生成详细报告
        report = analyzer.generate_detailed_report()
        print(report)
        
        # 保存报告到文件
        report_file = annotated_dir / f"analysis_report_{selected_file.stem}.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        # 导出CSV数据
        csv_file = analyzer.export_to_csv()
        
        print(f"\n🎉 分析完成！")
        print(f"📄 详细报告已保存: {report_file}")
        print(f"� 数据已导出: {csv_file}")
        
    except Exception as e:
        print(f"❌ 分析过程中出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
