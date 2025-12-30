"""
标注分析模块 - 计算IAA系数和模型准确率
用于论文中证明大模型标签的有效性
"""

import json
import numpy as np
from pathlib import Path
from collections import defaultdict, Counter
from typing import Dict, List, Tuple, Any
import pandas as pd

class AnnotationAnalyzer:
    """标注分析器"""
    
    def __init__(self, annotated_file_path: str):
        """
        初始化分析器
        
        Args:
            annotated_file_path: 标注后的数据文件路径
        """
        self.file_path = Path(annotated_file_path)
        self.data = self._load_data()
        self.annotated_samples = self._get_annotated_samples()
        
    def _load_data(self) -> Dict:
        """加载标注数据"""
        with open(self.file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _get_annotated_samples(self) -> List[Dict]:
        """获取已标注的样本"""
        return [sample for sample in self.data['samples'] 
                if sample.get('human_annotated', False)]
    
    def calculate_agreement_metrics(self) -> Dict[str, Any]:
        """
        计算一致性指标
        
        Returns:
            包含各种一致性指标的字典
        """
        if not self.annotated_samples:
            return {"error": "没有找到已标注的样本"}
        
        results = {
            "total_annotated_samples": len(self.annotated_samples),
            "total_samples": len(self.data['samples']),
            "annotation_coverage": len(self.annotated_samples) / len(self.data['samples']) * 100,
            "task_metrics": {}
        }
        
        # 分任务计算指标
        tasks = ['atmosphere_recognition', 'ky_test', 'subtext_deciphering']
        task_names = {
            'atmosphere_recognition': '氛围识别',
            'ky_test': 'KY测试', 
            'subtext_deciphering': '潜台词解码'
        }
        
        for task in tasks:
            task_result = self._calculate_task_agreement(task)
            results["task_metrics"][task_names[task]] = task_result
        
        # 计算总体指标
        results["overall_metrics"] = self._calculate_overall_metrics()
        
        return results
    
    def _calculate_task_agreement(self, task: str) -> Dict[str, float]:
        """计算单个任务的一致性指标"""
        original_answers = []
        human_answers = []
        
        for sample in self.annotated_samples:
            if task in sample.get('original_labels', {}):
                orig_idx = sample['original_labels'][task]['correct_answer_index']
                human_idx = sample['evaluation_labels'][task]['correct_answer_index']
                
                original_answers.append(orig_idx)
                human_answers.append(human_idx)
        
        if not original_answers:
            return {"error": f"任务 {task} 没有有效数据"}
        
        # 计算准确率（一致性）
        agreements = [1 if orig == human else 0 
                     for orig, human in zip(original_answers, human_answers)]
        accuracy = np.mean(agreements) * 100
        
        # 计算Kappa系数
        kappa = self._calculate_kappa(original_answers, human_answers)
        
        # 计算混淆矩阵统计
        confusion_stats = self._calculate_confusion_stats(original_answers, human_answers)
        
        return {
            "sample_count": len(original_answers),
            "accuracy": round(accuracy, 2),
            "agreement_rate": round(accuracy, 2),  # 同accuracy，但语义更清晰
            "kappa_coefficient": round(kappa, 3),
            "kappa_interpretation": self._interpret_kappa(kappa),
            "confusion_stats": confusion_stats,
            "disagreement_cases": len(original_answers) - sum(agreements),
            "disagreement_rate": round((1 - np.mean(agreements)) * 100, 2)
        }
    
    def _calculate_kappa(self, list1: List[int], list2: List[int]) -> float:
        """计算Cohen's Kappa系数"""
        if len(list1) != len(list2):
            return 0.0
        
        n = len(list1)
        if n == 0:
            return 0.0
        
        # 获取所有可能的类别
        all_categories = sorted(set(list1 + list2))
        k = len(all_categories)
        
        if k <= 1:
            return 1.0  # 完全一致
        
        # 创建混淆矩阵
        confusion_matrix = np.zeros((k, k))
        cat_to_idx = {cat: i for i, cat in enumerate(all_categories)}
        
        for a1, a2 in zip(list1, list2):
            i, j = cat_to_idx[a1], cat_to_idx[a2]
            confusion_matrix[i][j] += 1
        
        # 计算观察到的一致性
        po = np.trace(confusion_matrix) / n
        
        # 计算期望一致性
        marginal1 = np.sum(confusion_matrix, axis=1) / n
        marginal2 = np.sum(confusion_matrix, axis=0) / n
        pe = np.sum(marginal1 * marginal2)
        
        # 计算Kappa
        if pe == 1.0:
            return 1.0
        
        kappa = (po - pe) / (1 - pe)
        return kappa
    
    def _interpret_kappa(self, kappa: float) -> str:
        """解释Kappa系数"""
        if kappa < 0:
            return "差于随机 (Poor)"
        elif kappa < 0.20:
            return "轻微一致 (Slight)"
        elif kappa < 0.40:
            return "一般一致 (Fair)"
        elif kappa < 0.60:
            return "中等一致 (Moderate)"
        elif kappa < 0.80:
            return "高度一致 (Substantial)"
        else:
            return "几乎完全一致 (Almost Perfect)"
    
    def _calculate_confusion_stats(self, original: List[int], human: List[int]) -> Dict:
        """计算混淆矩阵统计信息"""
        # 统计每个选项的分布
        original_dist = Counter(original)
        human_dist = Counter(human)
        
        # 找出分歧最大的选项
        disagreements = defaultdict(int)
        for orig, human in zip(original, human):
            if orig != human:
                disagreements[f"{orig}→{human}"] += 1
        
        return {
            "original_distribution": dict(original_dist),
            "human_distribution": dict(human_dist),
            "top_disagreements": dict(sorted(disagreements.items(), 
                                           key=lambda x: x[1], reverse=True)[:5])
        }
    
    def _calculate_overall_metrics(self) -> Dict[str, float]:
        """计算总体指标"""
        all_agreements = []
        
        tasks = ['atmosphere_recognition', 'ky_test', 'subtext_deciphering']
        
        for sample in self.annotated_samples:
            sample_agreements = []
            for task in tasks:
                if (task in sample.get('original_labels', {}) and 
                    task in sample.get('evaluation_labels', {})):
                    orig_idx = sample['original_labels'][task]['correct_answer_index']
                    human_idx = sample['evaluation_labels'][task]['correct_answer_index']
                    sample_agreements.append(1 if orig_idx == human_idx else 0)
            
            if sample_agreements:
                all_agreements.extend(sample_agreements)
        
        if not all_agreements:
            return {"error": "没有有效的对比数据"}
        
        overall_accuracy = np.mean(all_agreements) * 100
        
        return {
            "overall_accuracy": round(overall_accuracy, 2),
            "total_comparisons": len(all_agreements),
            "total_agreements": sum(all_agreements),
            "total_disagreements": len(all_agreements) - sum(all_agreements)
        }
    
    def generate_detailed_report(self) -> str:
        """生成详细的分析报告"""
        metrics = self.calculate_agreement_metrics()
        
        if "error" in metrics:
            return f"错误: {metrics['error']}"
        
        report = []
        report.append("=" * 60)
        report.append("标注一致性分析报告")
        report.append("=" * 60)
        report.append("")
        
        # 基本信息
        report.append("📊 基本信息:")
        report.append(f"  • 总样本数: {metrics['total_samples']}")
        report.append(f"  • 已标注样本数: {metrics['total_annotated_samples']}")
        report.append(f"  • 标注覆盖率: {metrics['annotation_coverage']:.1f}%")
        report.append("")
        
        # 总体指标
        if "error" not in metrics["overall_metrics"]:
            overall = metrics["overall_metrics"]
            report.append("🎯 总体一致性:")
            report.append(f"  • 总体准确率: {overall['overall_accuracy']:.2f}%")
            report.append(f"  • 总对比次数: {overall['total_comparisons']}")
            report.append(f"  • 一致次数: {overall['total_agreements']}")
            report.append(f"  • 分歧次数: {overall['total_disagreements']}")
            report.append("")
        
        # 分任务指标
        report.append("📋 分任务分析:")
        for task_name, task_metrics in metrics["task_metrics"].items():
            if "error" not in task_metrics:
                report.append(f"\n  {task_name}:")
                report.append(f"    • 样本数: {task_metrics['sample_count']}")
                report.append(f"    • 一致率: {task_metrics['accuracy']:.2f}%")
                report.append(f"    • Kappa系数: {task_metrics['kappa_coefficient']:.3f} ({task_metrics['kappa_interpretation']})")
                report.append(f"    • 分歧案例: {task_metrics['disagreement_cases']} ({task_metrics['disagreement_rate']:.2f}%)")
                
                if task_metrics['confusion_stats']['top_disagreements']:
                    report.append(f"    • 主要分歧类型:")
                    for disagreement, count in task_metrics['confusion_stats']['top_disagreements'].items():
                        report.append(f"      - {disagreement}: {count}次")
        
        report.append("")
        report.append("=" * 60)
        report.append("📝 论文写作建议:")
        report.append("")
        
        # 生成论文写作建议
        overall_acc = metrics["overall_metrics"].get("overall_accuracy", 0)
        if overall_acc >= 80:
            report.append("✅ 模型标签质量评估: 优秀")
            report.append("   建议表述: '大模型生成的标签与人工标注具有高度一致性'")
        elif overall_acc >= 70:
            report.append("✅ 模型标签质量评估: 良好") 
            report.append("   建议表述: '大模型生成的标签与人工标注具有较好一致性'")
        elif overall_acc >= 60:
            report.append("⚠️ 模型标签质量评估: 中等")
            report.append("   建议表述: '大模型生成的标签与人工标注具有中等程度一致性'")
        else:
            report.append("❌ 模型标签质量评估: 需要改进")
            report.append("   建议表述: '大模型生成的标签需要进一步优化'")
        
        report.append("")
        report.append("📊 可用于论文的数据:")
        report.append(f"   • 标注者间一致性(IAA): {overall_acc:.2f}%")
        report.append(f"   • 样本覆盖率: {metrics['annotation_coverage']:.1f}%")
        
        # Kappa系数汇总
        kappa_values = []
        for task_metrics in metrics["task_metrics"].values():
            if "kappa_coefficient" in task_metrics:
                kappa_values.append(task_metrics["kappa_coefficient"])
        
        if kappa_values:
            avg_kappa = np.mean(kappa_values)
            report.append(f"   • 平均Kappa系数: {avg_kappa:.3f}")
        
        return "\n".join(report)
    
    def export_to_csv(self, output_path: str = None) -> str:
        """导出详细数据到CSV文件"""
        if not output_path:
            output_path = self.file_path.parent / f"annotation_analysis_{self.file_path.stem}.csv"
        
        # 准备数据
        rows = []
        for sample in self.annotated_samples:
            base_info = {
                'sample_id': sample['benchmark_id'],
                'scene_index': sample.get('scene_index', ''),
                'atmosphere': sample.get('atmosphere', ''),
                'category': sample.get('scenario_setup', {}).get('category', '')
            }
            
            tasks = ['atmosphere_recognition', 'ky_test', 'subtext_deciphering']
            task_names = ['氛围识别', 'KY测试', '潜台词解码']
            
            for task, task_name in zip(tasks, task_names):
                if (task in sample.get('original_labels', {}) and 
                    task in sample.get('evaluation_labels', {})):
                    
                    orig_idx = sample['original_labels'][task]['correct_answer_index']
                    human_idx = sample['evaluation_labels'][task]['correct_answer_index']
                    
                    row = base_info.copy()
                    row.update({
                        'task': task_name,
                        'original_answer': orig_idx,
                        'human_answer': human_idx,
                        'agreement': 1 if orig_idx == human_idx else 0,
                        'original_question': sample['original_labels'][task].get('question', ''),
                        'human_question': sample['evaluation_labels'][task].get('question', '')
                    })
                    rows.append(row)
        
        # 保存到CSV
        df = pd.DataFrame(rows)
        df.to_csv(output_path, index=False, encoding='utf-8-sig')
        
        return str(output_path)

def analyze_annotation_file(file_path: str) -> str:
    """
    分析标注文件的便捷函数
    
    Args:
        file_path: 标注文件路径
        
    Returns:
        分析报告字符串
    """
    analyzer = AnnotationAnalyzer(file_path)
    return analyzer.generate_detailed_report()

if __name__ == "__main__":
    # 示例用法
    import sys
    
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        print(analyze_annotation_file(file_path))
    else:
        print("用法: python annotation_analysis.py <标注文件路径>")
