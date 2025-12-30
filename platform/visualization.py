"""
AI标注准确率可视化分析
生成类似论文中的表格和图表
"""
import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from pathlib import Path

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

class VisualizationGenerator:
    """可视化生成器"""
    
    def __init__(self, report_file: str = "ai_human_comparison_report.json"):
        self.report_file = report_file
        self.results = None
        self.load_results()
    
    def load_results(self):
        """加载分析结果"""
        try:
            with open(self.report_file, 'r', encoding='utf-8') as f:
                self.results = json.load(f)
            print(f"✅ 加载分析结果: {self.report_file}")
        except FileNotFoundError:
            print(f"❌ 分析结果文件不存在: {self.report_file}")
            print("请先运行 python analysis.py 生成分析报告")
    
    def create_accuracy_table(self):
        """创建准确率表格 (类似论文Table 2)"""
        if not self.results:
            return
        
        # 准备数据
        data = []
        
        # 整体准确率
        overall_acc = self.results['overall_accuracy'] * 100
        data.append(['Overall', f"{overall_acc:.1f}%", 
                    f"{self.results['annotated_samples']}", "DeepSeek V3"])
        
        # 各任务准确率
        for task_key, task_data in self.results['task_accuracy'].items():
            acc = task_data['accuracy'] * 100
            data.append([
                task_data['task_name'],
                f"{acc:.1f}%",
                f"{task_data['correct_count']}/{task_data['total_count']}",
                self._get_confidence_level(acc)
            ])
        
        # 创建DataFrame
        df = pd.DataFrame(data, columns=['Task', 'Accuracy', 'Correct/Total', 'Confidence'])
        
        # 创建表格图
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.axis('tight')
        ax.axis('off')
        
        table = ax.table(cellText=df.values,
                        colLabels=df.columns,
                        cellLoc='center',
                        loc='center')
        
        table.auto_set_font_size(False)
        table.set_fontsize(12)
        table.scale(1.2, 1.5)
        
        # 设置表格样式
        for i in range(len(df.columns)):
            table[(0, i)].set_facecolor('#4CAF50')
            table[(0, i)].set_text_props(weight='bold', color='white')
        
        plt.title('DeepSeek V3 vs Human Annotation Accuracy', 
                 fontsize=16, fontweight='bold', pad=20)
        plt.savefig('accuracy_table.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return df
    
    def create_task_comparison_chart(self):
        """创建任务对比图表"""
        if not self.results:
            return
        
        # 准备数据
        tasks = []
        accuracies = []
        difficulties = []
        
        for task_key, task_data in self.results['task_accuracy'].items():
            tasks.append(task_data['task_name'])
            accuracies.append(task_data['accuracy'] * 100)
            
            # 获取难度信息
            conf_data = self.results['confidence_analysis']['task_confidence'].get(task_key, {})
            difficulties.append(conf_data.get('difficulty_level', '未知'))
        
        # 创建柱状图
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # 准确率柱状图
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
        bars = ax1.bar(tasks, accuracies, color=colors)
        ax1.set_ylabel('Accuracy (%)')
        ax1.set_title('Task-wise Accuracy Comparison')
        ax1.set_ylim(0, 100)
        
        # 添加数值标签
        for bar, acc in zip(bars, accuracies):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'{acc:.1f}%', ha='center', va='bottom')
        
        # 难度分布饼图
        difficulty_counts = pd.Series(difficulties).value_counts()
        ax2.pie(difficulty_counts.values, labels=difficulty_counts.index, 
               autopct='%1.1f%%', startangle=90)
        ax2.set_title('Task Difficulty Distribution')
        
        plt.tight_layout()
        plt.savefig('task_comparison.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def create_theme_analysis_chart(self):
        """创建主题分析图表"""
        if not self.results:
            return
        
        theme_data = self.results['confidence_analysis']['theme_confidence']
        
        if not theme_data:
            print("❌ 没有主题数据可供分析")
            return
        
        # 准备数据
        themes = list(theme_data.keys())
        accuracies = [data['mean_accuracy'] * 100 for data in theme_data.values()]
        std_devs = [data['std_accuracy'] * 100 for data in theme_data.values()]
        sample_counts = [data['sample_count'] for data in theme_data.values()]
        
        # 创建图表
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        # 主题准确率条形图（带误差条）
        y_pos = np.arange(len(themes))
        bars = ax1.barh(y_pos, accuracies, xerr=std_devs, 
                       color='skyblue', alpha=0.7, capsize=5)
        ax1.set_yticks(y_pos)
        ax1.set_yticklabels(themes)
        ax1.set_xlabel('Accuracy (%)')
        ax1.set_title('Theme-wise Accuracy with Confidence Intervals')
        ax1.set_xlim(0, 100)
        
        # 添加样本数量标签
        for i, (bar, count) in enumerate(zip(bars, sample_counts)):
            width = bar.get_width()
            ax1.text(width + 2, bar.get_y() + bar.get_height()/2,
                    f'n={count}', ha='left', va='center')
        
        # 样本数量分布
        ax2.bar(themes, sample_counts, color='lightcoral', alpha=0.7)
        ax2.set_ylabel('Sample Count')
        ax2.set_title('Sample Distribution by Theme')
        ax2.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig('theme_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def create_agreement_heatmap(self):
        """创建一致性热力图"""
        if not self.results:
            return
        
        agreement_data = self.results['agreement_matrix']
        
        if not agreement_data:
            print("❌ 没有一致性数据可供分析")
            return
        
        # 准备数据
        tasks = []
        agreements = []
        
        for task_key, data in agreement_data.items():
            task_name = self.results['task_accuracy'][task_key]['task_name']
            tasks.append(task_name)
            agreements.append(data['agreement_rate'])
        
        # 创建热力图数据矩阵
        agreement_matrix = np.array(agreements).reshape(1, -1)
        
        # 创建热力图
        plt.figure(figsize=(10, 3))
        sns.heatmap(agreement_matrix, 
                   xticklabels=tasks,
                   yticklabels=['AI vs Human'],
                   annot=True, 
                   fmt='.1f',
                   cmap='RdYlGn',
                   vmin=0, vmax=100,
                   cbar_kws={'label': 'Agreement Rate (%)'})
        
        plt.title('Inter-Annotator Agreement (AI vs Human)')
        plt.tight_layout()
        plt.savefig('agreement_heatmap.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def _get_confidence_level(self, accuracy: float) -> str:
        """根据准确率获取置信度等级"""
        if accuracy >= 95:
            return "Very High"
        elif accuracy >= 85:
            return "High"
        elif accuracy >= 70:
            return "Medium"
        elif accuracy >= 50:
            return "Low"
        else:
            return "Very Low"
    
    def generate_all_visualizations(self):
        """生成所有可视化图表"""
        if not self.results:
            print("❌ 无法生成可视化，请先运行分析")
            return
        
        print("🎨 生成可视化图表...")
        
        try:
            self.create_accuracy_table()
            print("✅ 生成准确率表格")
            
            self.create_task_comparison_chart()
            print("✅ 生成任务对比图表")
            
            self.create_theme_analysis_chart()
            print("✅ 生成主题分析图表")
            
            self.create_agreement_heatmap()
            print("✅ 生成一致性热力图")
            
            print("\n🎉 所有可视化图表生成完成！")
            print("📁 图片文件:")
            print("  - accuracy_table.png")
            print("  - task_comparison.png") 
            print("  - theme_analysis.png")
            print("  - agreement_heatmap.png")
            
        except Exception as e:
            print(f"❌ 生成可视化时出错: {e}")

def main():
    """主函数"""
    viz = VisualizationGenerator()
    viz.generate_all_visualizations()

if __name__ == "__main__":
    main()
