# AI标注准确率分析工具

## 📋 概述

这套工具实现了类似论文中**后验验证(Posterior Verification)**的分析流程，用于评估DeepSeek V3在多轮对话标注任务中的准确率和可靠性。

## 🎯 核心功能

### 1. 准确率分析 (`analysis.py`)
- **整体准确率**: AI vs 人工标注的总体一致性
- **任务级准确率**: 三个评测任务的分别准确率
  - 氛围识别 (Atmosphere Recognition)
  - KY测试 (Social Intelligence Test)  
  - 意图推断 (Intent Inference)
- **主题级置信度**: 不同对话主题的准确率分布
- **标注者间一致性**: 模拟IAA(Inter-Annotator Agreement)计算

### 2. 可视化报告 (`visualization.py`)
- **准确率表格**: 类似论文Table 2的格式
- **任务对比图**: 柱状图显示各任务表现
- **主题分析图**: 不同主题的准确率分布
- **一致性热力图**: AI与人工标注的一致性可视化

### 3. 综合分析 (`run_analysis.py`)
- **一键运行**: 完整的分析流程
- **论文风格输出**: 模拟学术论文的结果展示
- **建议生成**: 基于准确率给出使用建议

## 🚀 使用方法

### 前提条件
1. 已使用标注平台对部分数据进行人工标注
2. 标注文件保存在 `annotated_data/` 目录下

### 运行分析
```bash
# 方法1: 一键运行完整分析
python run_analysis.py

# 方法2: 分步运行
python analysis.py          # 生成分析报告
python visualization.py     # 生成可视化图表
```

### 输出文件
- `ai_human_comparison_report.json` - 详细分析报告
- `accuracy_table.png` - 准确率表格
- `task_comparison.png` - 任务对比图表
- `theme_analysis.png` - 主题分析图表
- `agreement_heatmap.png` - 一致性热力图

## 📊 分析指标

### 准确率指标
- **Overall Accuracy**: 所有任务的平均准确率
- **Task-wise Accuracy**: 每个任务的准确率
- **Theme-wise Confidence**: 每个主题的置信度区间

### 可靠性指标
- **Agreement Rate**: AI与人工标注的一致性比例
- **Confidence Interval**: 准确率的置信区间
- **Sample Coverage**: 标注样本的覆盖率

### 难度分级
- **简单** (≥90%): AI表现优秀，可直接使用
- **中等** (70-90%): AI表现良好，建议抽检
- **困难** (50-70%): 需要人工监督
- **极困难** (<50%): 需要大量人工干预

## 🔍 分析示例

### 论文风格输出示例
```
Table: DeepSeek V3 Labeling Accuracy
------------------------------------------------------------
Task                     Accuracy    Agreement    Samples
------------------------------------------------------------
氛围识别                    87.5%       87.5%         24
KY测试                     82.1%       82.1%         28  
意图推断                    79.3%       79.3%         29
------------------------------------------------------------
Overall                    83.0%       83.0%         81
------------------------------------------------------------

CONCLUSION:
DeepSeek V3 achieves 83.0% accuracy in human verification.
Best performance: 氛围识别 (87.5%)
Most challenging: 意图推断 (79.3%)
```

### 置信度分析示例
```
CONFIDENCE ANALYSIS:
Most reliable theme: 办公室冲突 (89.2%)

RECOMMENDATIONS:
⚠️ DeepSeek V3 labeling is acceptable but may need spot checking.
```

## 📈 与论文对比

本工具参考了以下论文方法：
- **后验验证**: 人工验证AI标注的有效性
- **标注者间一致性**: 计算IAA指标
- **置信度分析**: 多维度评估标注质量
- **可视化展示**: 类似学术论文的表格和图表

## 🛠️ 技术栈

- **Python 3.8+**
- **pandas**: 数据处理
- **numpy**: 数值计算  
- **matplotlib**: 基础绘图
- **seaborn**: 统计可视化
- **json**: 数据存储

## 📝 使用场景

1. **模型评估**: 评估AI标注模型的可靠性
2. **质量控制**: 确定人工审核的必要性
3. **数据集验证**: 验证训练数据的质量
4. **学术研究**: 生成论文级别的分析报告
5. **生产决策**: 决定AI标注的使用策略

## ⚠️ 注意事项

1. 确保有足够的人工标注样本（建议≥50个）
2. 标注样本应覆盖不同主题和难度
3. 可视化图表需要GUI环境支持
4. 大数据集分析可能需要较长时间

## 🔄 工作流程

1. **数据生成** → 使用DeepSeek V3生成标注数据
2. **人工标注** → 使用标注平台进行人工校准  
3. **准确率分析** → 运行分析工具计算指标
4. **可视化展示** → 生成图表和报告
5. **决策支持** → 基于结果调整使用策略
