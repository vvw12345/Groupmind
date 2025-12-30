"""
多线程评测器 - 支持并发评测和结果分析
"""
import json
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Dict, List, Any
import sys
from collections import defaultdict
import pandas as pd
import csv
import os
from datetime import datetime

# 添加主目录到Python路径
sys.path.append(str(Path(__file__).parent.parent))

from eval_client_bilingual import BilingualEvaluationClient

class MultiThreadEvaluator:
    """多线程评测器"""
    
    def __init__(self, models: List[str] = None, max_workers: int = 4, use_siliconflow: bool = False, use_agentworld: bool = False, use_yunwu: bool = False, language: str = "zh", evaluation_mode: str = "full"):
        self.models = models or [
            "moonshotai/kimi-k2:free",
            "z-ai/glm-4.5-air:free"
        ]
        self.max_workers = max_workers
        self.results = {}
        self.use_siliconflow = use_siliconflow
        self.use_agentworld = use_agentworld
        self.use_yunwu = use_yunwu
        self.language = language
        self.evaluation_mode = evaluation_mode
        
        # 为每个模型创建独立的客户端
        self.clients = {}
        for model in self.models:
            self.clients[model] = BilingualEvaluationClient([model], use_siliconflow=use_siliconflow, use_agentworld=use_agentworld, use_yunwu=use_yunwu, language=language, evaluation_mode=evaluation_mode)
        
        # CSV文件锁，确保多线程写入安全
        self.csv_lock = threading.Lock()
        
        print(f"🚀 多线程评测器初始化完成")
        print(f"🎯 评测模型: {', '.join(self.models)}")
        print(f"🧵 最大线程数: {max_workers}")
    
    def load_dataset(self, file_path: str) -> List[Dict]:
        """加载数据集"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            samples = data.get('samples', [])
            print(f"📊 加载数据集: {file_path}")
            print(f"📝 样本数量: {len(samples)}")
            
            return samples
            
        except Exception as e:
            print(f"❌ 加载数据集失败: {e}")
            return []
    
    def evaluate_sample_task(self, sample: Dict, model: str, task_type: str) -> Dict:
        """评测单个样本的单个任务"""
        try:
            client = self.clients[model]
            result = client.evaluate_sample(sample, task_type)
            
            if result:
                result.update({
                    'model': model,
                    'task_type': task_type,
                    'benchmark_id': sample['benchmark_id'],
                    'meta_theme': sample['meta_theme']
                })
            
            return result
            
        except Exception as e:
            print(f"❌ 评测失败 {model} - {task_type}: {e}")
            return None
    
    def init_csv_file(self, output_path: Path) -> str:
        """初始化CSV文件"""
        csv_file = output_path / "evaluation_results.csv"
        
        # 创建CSV文件头
        fieldnames = [
            'timestamp', 'benchmark_id', 'meta_theme', 'model', 'task_type', 
            'predicted_answer', 'correct_answer', 'is_correct', 
            'raw_response', 'parse_error'
        ]
        
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
        
        print(f"📄 CSV结果文件初始化: {csv_file}")
        return str(csv_file)
    
    def save_result_to_csv(self, result: Dict, csv_file: str):
        """保存单个结果到CSV文件"""
        if not result or result.get('parse_error', False):
            return
        
        # 准备CSV行数据
        row_data = {
            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
            'benchmark_id': result.get('benchmark_id', ''),
            'meta_theme': result.get('meta_theme', ''),
            'model': result.get('model', ''),
            'task_type': result.get('task_type', ''),
            'predicted_answer': result.get('predicted_answer', -1),
            'correct_answer': result.get('correct_answer', -1),
            'is_correct': result.get('is_correct', False),
            'raw_response': result.get('raw_response', '').replace('\n', ' ').replace('\r', ' ')[:200],  # 限制长度
            'parse_error': result.get('parse_error', False)
        }
        
        # 线程安全地写入CSV
        with self.csv_lock:
            with open(csv_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=row_data.keys())
                writer.writerow(row_data)
    
    def evaluate_dataset(self, samples: List[Dict], output_dir: str = None) -> Dict:
        """评测整个数据集"""
        # 如果没有指定输出目录，使用时间戳创建
        if output_dir is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_dir = f"results_{timestamp}"
        
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # 准备评测任务
        tasks = []
        task_types = ["atmosphere_recognition", "ky_test", "subtext_deciphering"]
        
        for sample in samples:
            for model in self.models:
                for task_type in task_types:
                    tasks.append((sample, model, task_type))
        
        total_tasks = len(tasks)
        print(f"🎯 总评测任务数: {total_tasks}")
        print(f"📊 样本数: {len(samples)} | 模型数: {len(self.models)} | 任务类型数: {len(task_types)}")
        
        # 初始化CSV文件
        csv_file = self.init_csv_file(output_path)
        
        # 初始化结果存储
        results = {model: {task: [] for task in task_types} for model in self.models}
        completed_tasks = 0
        failed_tasks = 0
        successful_tasks = 0  # 新增：成功任务计数
        
        start_time = time.time()
        
        # 多线程执行评测
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # 提交所有任务
            future_to_task = {
                executor.submit(self.evaluate_sample_task, sample, model, task_type): (sample, model, task_type)
                for sample, model, task_type in tasks
            }
            
            # 处理完成的任务
            for future in as_completed(future_to_task):
                sample, model, task_type = future_to_task[future]
                completed_tasks += 1
                
                try:
                    result = future.result()
                    if result and not result.get('parse_error', False):
                        # 成功的结果
                        results[model][task_type].append(result)
                        successful_tasks += 1
                        
                        # 实时保存到CSV
                        self.save_result_to_csv(result, csv_file)
                        
                        if successful_tasks % 10 == 0:
                            print(f"✅ 已成功评测 {successful_tasks} 个任务，实时保存到CSV")
                    else:
                        failed_tasks += 1
                        
                except Exception as e:
                    print(f"❌ 任务执行异常: {e}")
                    failed_tasks += 1
                
                # 进度显示
                if completed_tasks % 20 == 0 or completed_tasks == total_tasks:
                    progress = completed_tasks / total_tasks * 100
                    elapsed = time.time() - start_time
                    eta = elapsed / completed_tasks * (total_tasks - completed_tasks) if completed_tasks > 0 else 0
                    
                    print(f"📈 进度: {completed_tasks}/{total_tasks} ({progress:.1f}%) "
                          f"| 成功: {successful_tasks} | 失败: {failed_tasks} "
                          f"| 耗时: {elapsed:.1f}s | 预计剩余: {eta:.1f}s")
        
        # 保存原始结果
        raw_results_file = output_path / "raw_results.json"
        with open(raw_results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"💾 原始结果已保存: {raw_results_file}")
        
        # 分析结果 (只统计成功的样本)
        analysis = self.analyze_results(results, samples, successful_tasks, failed_tasks)
        
        # 保存分析结果
        analysis_file = output_path / "evaluation_analysis.json"
        with open(analysis_file, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, ensure_ascii=False, indent=2)
        
        print(f"📊 分析结果已保存: {analysis_file}")
        
        # 生成报告
        self.generate_report(analysis, output_path)
        
        return analysis
    
    def analyze_results(self, results: Dict, samples: List[Dict], successful_tasks: int, failed_tasks: int) -> Dict:
        """分析评测结果"""
        analysis = {
            'summary': {},
            'model_performance': {},
            'task_performance': {},
            'theme_performance': {},
            'detailed_comparison': {}
        }
        
        task_names = {
            'atmosphere_recognition': '氛围识别',
            'ky_test': 'KY测试',
            'subtext_deciphering': '潜台词解码'
        }
        
        # 分析每个模型的表现
        for model in self.models:
            model_stats = {
                'total_samples': 0,
                'correct_predictions': 0,
                'accuracy': 0.0,
                'task_accuracies': {}
            }
            
            for task_type, task_results in results[model].items():
                if not task_results:
                    continue
                
                correct = sum(1 for r in task_results if r.get('is_correct', False))
                total = len(task_results)
                accuracy = correct / total if total > 0 else 0
                
                model_stats['task_accuracies'][task_type] = {
                    'task_name': task_names.get(task_type, task_type),
                    'correct': correct,
                    'total': total,
                    'accuracy': accuracy
                }
                
                model_stats['total_samples'] += total
                model_stats['correct_predictions'] += correct
            
            if model_stats['total_samples'] > 0:
                model_stats['accuracy'] = model_stats['correct_predictions'] / model_stats['total_samples']
            
            analysis['model_performance'][model] = model_stats
        
        # 分析任务难度
        for task_type in task_names.keys():
            task_stats = {
                'task_name': task_names[task_type],
                'model_results': {},
                'average_accuracy': 0.0,
                'difficulty_level': ''
            }
            
            accuracies = []
            for model in self.models:
                if task_type in results[model] and results[model][task_type]:
                    task_results = results[model][task_type]
                    correct = sum(1 for r in task_results if r.get('is_correct', False))
                    total = len(task_results)
                    accuracy = correct / total if total > 0 else 0
                    
                    task_stats['model_results'][model] = {
                        'accuracy': accuracy,
                        'correct': correct,
                        'total': total
                    }
                    accuracies.append(accuracy)
            
            if accuracies:
                avg_acc = sum(accuracies) / len(accuracies)
                task_stats['average_accuracy'] = avg_acc
                
                # 难度分级
                if avg_acc >= 0.8:
                    task_stats['difficulty_level'] = '简单'
                elif avg_acc >= 0.6:
                    task_stats['difficulty_level'] = '中等'
                elif avg_acc >= 0.4:
                    task_stats['difficulty_level'] = '困难'
                else:
                    task_stats['difficulty_level'] = '极困难'
            
            analysis['task_performance'][task_type] = task_stats
        
        # 分析主题表现
        theme_stats = defaultdict(lambda: defaultdict(list))
        
        for model in self.models:
            for task_type, task_results in results[model].items():
                for result in task_results:
                    theme = result.get('meta_theme', '未知')
                    is_correct = result.get('is_correct', False)
                    theme_stats[theme][model].append(is_correct)
        
        for theme, model_data in theme_stats.items():
            theme_analysis = {
                'theme_name': theme,
                'model_accuracies': {},
                'average_accuracy': 0.0
            }
            
            accuracies = []
            for model, correct_list in model_data.items():
                if correct_list:
                    accuracy = sum(correct_list) / len(correct_list)
                    theme_analysis['model_accuracies'][model] = {
                        'accuracy': accuracy,
                        'correct': sum(correct_list),
                        'total': len(correct_list)
                    }
                    accuracies.append(accuracy)
            
            if accuracies:
                theme_analysis['average_accuracy'] = sum(accuracies) / len(accuracies)
            
            analysis['theme_performance'][theme] = theme_analysis
        
        # 计算成功评测的样本数 (只统计成功的样本)
        successfully_evaluated_samples = set()
        for model_results in results.values():
            for task_results in model_results.values():
                for result in task_results:
                    if result.get('is_correct') is not None:  # 有效结果
                        successfully_evaluated_samples.add(result.get('benchmark_id'))
        
        best_model = max(analysis['model_performance'].items(), 
                        key=lambda x: x[1]['accuracy']) if analysis['model_performance'] else None
        
        analysis['summary'] = {
            'total_samples_in_dataset': len(samples),
            'successfully_evaluated_samples': len(successfully_evaluated_samples),
            'successful_tasks': successful_tasks,
            'failed_tasks': failed_tasks,
            'success_rate': successful_tasks / (successful_tasks + failed_tasks) * 100 if (successful_tasks + failed_tasks) > 0 else 0,
            'models_tested': len(self.models),
            'tasks_tested': len(task_names),
            'best_model': best_model[0] if best_model else None,
            'best_model_accuracy': best_model[1]['accuracy'] if best_model else 0.0
        }
        
        return analysis
    
    def generate_report(self, analysis: Dict, output_path: Path):
        """生成评测报告"""
        report_file = output_path / "evaluation_report.md"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("# 模型评测报告\n\n")
            
            # 概览
            summary = analysis['summary']
            f.write("## 📊 评测概览\n\n")
            f.write(f"- **数据集总样本数**: {summary['total_samples_in_dataset']}\n")
            f.write(f"- **成功评测样本数**: {summary['successfully_evaluated_samples']}\n")
            f.write(f"- **成功任务数**: {summary['successful_tasks']}\n")
            f.write(f"- **失败任务数**: {summary['failed_tasks']}\n")
            f.write(f"- **任务成功率**: {summary['success_rate']:.1f}%\n")
            f.write(f"- **测试模型数**: {summary['models_tested']}\n")
            f.write(f"- **评测任务类型数**: {summary['tasks_tested']}\n")
            f.write(f"- **最佳模型**: {summary['best_model']} ({summary['best_model_accuracy']*100:.1f}%)\n\n")
            f.write("**注意**: 以下所有准确率统计均基于成功评测的样本，失败的评测任务不计入统计。\n\n")
            
            # 模型表现
            f.write("## 🤖 模型表现\n\n")
            f.write("| 模型 | 总体准确率 | 氛围识别 | KY测试 | 潜台词解码 |\n")
            f.write("|------|------------|----------|--------|----------|\n")
            
            for model, stats in analysis['model_performance'].items():
                f.write(f"| {model} | {stats['accuracy']*100:.1f}% |")
                
                for task_type in ['atmosphere_recognition', 'ky_test', 'subtext_deciphering']:
                    if task_type in stats['task_accuracies']:
                        acc = stats['task_accuracies'][task_type]['accuracy']
                        f.write(f" {acc*100:.1f}% |")
                    else:
                        f.write(" N/A |")
                f.write("\n")
            
            f.write("\n")
            
            # 任务难度分析
            f.write("## 📋 任务难度分析\n\n")
            for task_type, task_stats in analysis['task_performance'].items():
                f.write(f"### {task_stats['task_name']}\n")
                f.write(f"- **平均准确率**: {task_stats['average_accuracy']*100:.1f}%\n")
                f.write(f"- **难度等级**: {task_stats['difficulty_level']}\n")
                
                f.write("- **各模型表现**:\n")
                for model, result in task_stats['model_results'].items():
                    f.write(f"  - {model}: {result['accuracy']*100:.1f}% ({result['correct']}/{result['total']})\n")
                f.write("\n")
            
            # 主题表现分析
            f.write("## 🎭 主题表现分析\n\n")
            for theme, theme_stats in analysis['theme_performance'].items():
                f.write(f"### {theme}\n")
                f.write(f"- **平均准确率**: {theme_stats['average_accuracy']*100:.1f}%\n")
                
                f.write("- **各模型表现**:\n")
                for model, result in theme_stats['model_accuracies'].items():
                    f.write(f"  - {model}: {result['accuracy']*100:.1f}% ({result['correct']}/{result['total']})\n")
                f.write("\n")
        
        print(f"📄 评测报告已生成: {report_file}")
    
    def print_summary(self, analysis: Dict):
        """打印评测摘要"""
        print("\n" + "="*80)
        print("🎯 模型评测摘要")
        print("="*80)
        
        summary = analysis['summary']
        print(f"📊 数据集总样本数: {summary['total_samples_in_dataset']}")
        print(f"✅ 成功评测样本数: {summary['successfully_evaluated_samples']}")
        print(f"📈 任务成功率: {summary['success_rate']:.1f}% ({summary['successful_tasks']}/{summary['successful_tasks'] + summary['failed_tasks']})")
        print(f"🤖 最佳模型: {summary['best_model']} ({summary['best_model_accuracy']*100:.1f}%)")
        print(f"⚠️  注意: 准确率统计仅基于成功评测的样本")
        
        print(f"\n📋 模型排名:")
        sorted_models = sorted(
            analysis['model_performance'].items(),
            key=lambda x: x[1]['accuracy'],
            reverse=True
        )
        
        for i, (model, stats) in enumerate(sorted_models, 1):
            print(f"  {i}. {model}: {stats['accuracy']*100:.1f}%")
        
        print(f"\n🎯 任务难度:")
        for task_type, task_stats in analysis['task_performance'].items():
            print(f"  {task_stats['task_name']}: {task_stats['average_accuracy']*100:.1f}% ({task_stats['difficulty_level']})")
        
        print("="*80)

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="多线程模型评测器")
    parser.add_argument("--data", required=True, help="数据集文件路径")
    parser.add_argument("--models", nargs="+", 
                       default=["moonshotai/kimi-k2:free", "z-ai/glm-4.5-air:free"],
                       help="要评测的模型列表")
    parser.add_argument("--workers", type=int, default=4, help="最大线程数")
    parser.add_argument("--output", default=None, help="结果输出目录(默认使用时间戳)")
    
    args = parser.parse_args()
    
    # 创建评测器
    evaluator = MultiThreadEvaluator(models=args.models, max_workers=args.workers)
    
    # 加载数据集
    samples = evaluator.load_dataset(args.data)
    if not samples:
        print("❌ 无法加载数据集")
        return
    
    # 执行评测
    print(f"\n🚀 开始评测...")
    analysis = evaluator.evaluate_dataset(samples, args.output)
    
    # 打印摘要
    evaluator.print_summary(analysis)
    
    # 打印客户端统计
    for model, client in evaluator.clients.items():
        print(f"\n{model} 客户端统计:")
        client.print_stats()

if __name__ == "__main__":
    main()
