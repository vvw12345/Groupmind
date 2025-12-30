"""
AI与人工标注置信度对比分析工具
基于论文中的后验验证方法，分析DeepSeek V3的标注准确率
"""
import json
import os
from pathlib import Path
from typing import Dict, List, Tuple
import pandas as pd
import numpy as np
from collections import defaultdict

class AnnotationAnalyzer:
    """标注分析器"""
    
    def __init__(self, annotated_dir: str = "annotated_data"):
        self.annotated_dir = Path(annotated_dir)
        self.results = {
            'total_samples': 0,
            'annotated_samples': 0,
            'task_accuracy': {},
            'overall_accuracy': 0.0,
            'agreement_matrix': {},
            'confidence_analysis': {},
            'detailed_results': []
        }
    
    def load_annotated_data(self) -> List[Dict]:
        """加载所有标注数据"""
        annotated_files = []
        
        if not self.annotated_dir.exists():
            print(f"❌ 标注目录不存在: {self.annotated_dir}")
            return []
        
        for file_path in self.annotated_dir.glob("annotated_*.json"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    annotated_files.append({
                        'filename': file_path.name,
                        'data': data
                    })
                print(f"✅ 加载文件: {file_path.name}")
            except Exception as e:
                print(f"❌ 加载失败 {file_path.name}: {e}")
        
        return annotated_files
    
    def analyze_sample_accuracy(self, sample: Dict) -> Dict:
        """分析单个样本的准确率"""
        if 'original_labels' not in sample or not sample.get('human_annotated', False):
            return None
        
        original = sample['original_labels']
        human = sample['evaluation_labels']
        
        task_results = {}
        
        # 分析三个任务
        tasks = {
            'atmosphere_recognition': '氛围识别',
            'ky_test': 'KY测试', 
            'collective_intent_inference': '意图推断'
        }
        
        for task_key, task_name in tasks.items():
            if task_key in original and task_key in human:
                ai_answer = original[task_key].get('correct_answer_index', -1)
                human_answer = human[task_key].get('correct_answer_index', -1)
                
                is_correct = ai_answer == human_answer
                task_results[task_key] = {
                    'task_name': task_name,
                    'ai_answer': ai_answer + 1,  # 转换为1-based显示
                    'human_answer': human_answer + 1,
                    'is_correct': is_correct,
                    'question': human[task_key].get('question', ''),
                    'options': human[task_key].get('mcq_options', [])
                }
        
        return {
            'benchmark_id': sample.get('benchmark_id', ''),
            'meta_theme': sample.get('meta_theme', ''),
            'task_results': task_results,
            'overall_correct': sum(r['is_correct'] for r in task_results.values()),
            'total_tasks': len(task_results)
        }
    
    def calculate_inter_annotator_agreement(self, results: List[Dict]) -> Dict:
        """计算标注者间一致性(模拟多人标注的IAA)"""
        task_agreements = {}
        
        for task_key in ['atmosphere_recognition', 'ky_test', 'collective_intent_inference']:
            agreements = []
            total_comparisons = 0
            
            for result in results:
                if task_key in result['task_results']:
                    task_result = result['task_results'][task_key]
                    # 这里我们计算AI与人工的一致性作为基准
                    agreements.append(1 if task_result['is_correct'] else 0)
                    total_comparisons += 1
            
            if total_comparisons > 0:
                agreement_rate = sum(agreements) / total_comparisons * 100
                task_agreements[task_key] = {
                    'agreement_rate': agreement_rate,
                    'total_comparisons': total_comparisons,
                    'agreements': sum(agreements)
                }
        
        return task_agreements
    
    def generate_confidence_analysis(self, results: List[Dict]) -> Dict:
        """生成置信度分析"""
        theme_accuracy = defaultdict(list)
        task_difficulty = defaultdict(list)
        
        for result in results:
            theme = result['meta_theme']
            accuracy = result['overall_correct'] / result['total_tasks'] if result['total_tasks'] > 0 else 0
            theme_accuracy[theme].append(accuracy)
            
            # 分析每个任务的难度
            for task_key, task_result in result['task_results'].items():
                task_difficulty[task_key].append(1 if task_result['is_correct'] else 0)
        
        # 计算主题级别的置信度
        theme_confidence = {}
        for theme, accuracies in theme_accuracy.items():
            theme_confidence[theme] = {
                'mean_accuracy': np.mean(accuracies),
                'std_accuracy': np.std(accuracies),
                'sample_count': len(accuracies),
                'confidence_interval': np.percentile(accuracies, [25, 75]) if len(accuracies) > 1 else [0, 0]
            }
        
        # 计算任务级别的难度
        task_confidence = {}
        task_names = {
            'atmosphere_recognition': '氛围识别',
            'ky_test': 'KY测试',
            'collective_intent_inference': '意图推断'
        }
        
        for task_key, scores in task_difficulty.items():
            if scores:
                task_confidence[task_key] = {
                    'task_name': task_names.get(task_key, task_key),
                    'accuracy': np.mean(scores),
                    'total_samples': len(scores),
                    'correct_count': sum(scores),
                    'difficulty_level': self._classify_difficulty(np.mean(scores))
                }
        
        return {
            'theme_confidence': theme_confidence,
            'task_confidence': task_confidence
        }
    
    def _classify_difficulty(self, accuracy: float) -> str:
        """根据准确率分类任务难度"""
        if accuracy >= 0.9:
            return "简单"
        elif accuracy >= 0.7:
            return "中等"
        elif accuracy >= 0.5:
            return "困难"
        else:
            return "极困难"
    
    def run_analysis(self) -> Dict:
        """运行完整分析"""
        print("🔍 开始分析AI与人工标注的置信度对比...")
        
        # 加载数据
        annotated_files = self.load_annotated_data()
        if not annotated_files:
            print("❌ 没有找到标注数据文件")
            return self.results
        
        all_results = []
        total_samples = 0
        annotated_samples = 0
        
        # 分析每个文件
        for file_info in annotated_files:
            data = file_info['data']
            samples = data.get('samples', [])
            total_samples += len(samples)
            
            for sample in samples:
                if sample.get('human_annotated', False):
                    result = self.analyze_sample_accuracy(sample)
                    if result:
                        all_results.append(result)
                        annotated_samples += 1
        
        if not all_results:
            print("❌ 没有找到人工标注的样本")
            return self.results
        
        print(f"📊 分析完成: {annotated_samples}/{total_samples} 个样本已标注")
        
        # 计算整体准确率
        total_correct = sum(r['overall_correct'] for r in all_results)
        total_tasks = sum(r['total_tasks'] for r in all_results)
        overall_accuracy = total_correct / total_tasks if total_tasks > 0 else 0
        
        # 计算各任务准确率
        task_accuracy = {}
        task_names = {
            'atmosphere_recognition': '氛围识别',
            'ky_test': 'KY测试',
            'collective_intent_inference': '意图推断'
        }
        
        for task_key, task_name in task_names.items():
            correct = sum(1 for r in all_results 
                         if task_key in r['task_results'] and r['task_results'][task_key]['is_correct'])
            total = sum(1 for r in all_results if task_key in r['task_results'])
            
            if total > 0:
                task_accuracy[task_key] = {
                    'task_name': task_name,
                    'accuracy': correct / total,
                    'correct_count': correct,
                    'total_count': total
                }
        
        # 计算标注者间一致性
        agreement_matrix = self.calculate_inter_annotator_agreement(all_results)
        
        # 生成置信度分析
        confidence_analysis = self.generate_confidence_analysis(all_results)
        
        # 汇总结果
        self.results = {
            'total_samples': total_samples,
            'annotated_samples': annotated_samples,
            'overall_accuracy': overall_accuracy,
            'task_accuracy': task_accuracy,
            'agreement_matrix': agreement_matrix,
            'confidence_analysis': confidence_analysis,
            'detailed_results': all_results
        }
        
        return self.results
    
    def generate_report(self, output_file: str = "ai_human_comparison_report.json"):
        """生成分析报告"""
        results = self.run_analysis()
        
        # 保存详细报告
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        # 打印摘要报告
        self.print_summary_report(results)
        
        return output_file
    
    def print_summary_report(self, results: Dict):
        """打印摘要报告"""
        print("\n" + "="*80)
        print("🤖 AI与人工标注置信度对比分析报告")
        print("="*80)
        
        print(f"\n📊 数据概览:")
        print(f"  总样本数: {results['total_samples']}")
        print(f"  已标注样本: {results['annotated_samples']}")
        print(f"  标注覆盖率: {results['annotated_samples']/results['total_samples']*100:.1f}%")
        
        print(f"\n🎯 整体准确率:")
        print(f"  DeepSeek V3 vs 人工标注: {results['overall_accuracy']*100:.1f}%")
        
        print(f"\n📋 各任务准确率:")
        for task_key, task_data in results['task_accuracy'].items():
            print(f"  {task_data['task_name']}: {task_data['accuracy']*100:.1f}% "
                  f"({task_data['correct_count']}/{task_data['total_count']})")
        
        print(f"\n🔍 置信度分析:")
        task_conf = results['confidence_analysis']['task_confidence']
        for task_key, conf_data in task_conf.items():
            print(f"  {conf_data['task_name']}: {conf_data['accuracy']*100:.1f}% "
                  f"(难度: {conf_data['difficulty_level']})")
        
        print(f"\n📈 主题准确率分布:")
        theme_conf = results['confidence_analysis']['theme_confidence']
        for theme, conf_data in theme_conf.items():
            print(f"  {theme}: {conf_data['mean_accuracy']*100:.1f}% ± {conf_data['std_accuracy']*100:.1f}% "
                  f"(n={conf_data['sample_count']})")
        
        print(f"\n🤝 标注一致性 (AI vs 人工):")
        for task_key, agreement_data in results['agreement_matrix'].items():
            task_name = results['task_accuracy'][task_key]['task_name']
            print(f"  {task_name}: {agreement_data['agreement_rate']:.1f}% "
                  f"({agreement_data['agreements']}/{agreement_data['total_comparisons']})")
        
        print("\n" + "="*80)

def main():
    """主函数"""
    analyzer = AnnotationAnalyzer()
    report_file = analyzer.generate_report()
    print(f"\n📄 详细报告已保存至: {report_file}")

if __name__ == "__main__":
    main()
