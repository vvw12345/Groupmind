#!/usr/bin/env python3
"""
一键运行评测脚本
"""
import sys
import os
from pathlib import Path
from datetime import datetime

# 添加当前目录到Python路径
sys.path.append(str(Path(__file__).parent))

from evaluator import MultiThreadEvaluator

def main():
    """主函数"""
    import argparse
    
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="模型评测系统")
    parser.add_argument("--data", default="/home/Group/data_generator/data/benchmark_part1.json", 
                       help="数据集文件路径")
    parser.add_argument("--models", nargs="+", 
                       default=["z-ai/glm-4.5-air:free", "deepseek/deepseek-r1-distill-llama-70b:free"],
                       help="要评测的模型列表")
    parser.add_argument("--platform", choices=["openrouter", "siliconflow", "agentworld", "yunwu"], default="openrouter",
                       help="选择API平台: openrouter, siliconflow, agentworld 或 yunwu")
    parser.add_argument("--language", choices=["zh", "en"], default="zh",
                       help="数据语言: zh (中文) 或 en (英文)")
    parser.add_argument("--mode", choices=["full", "limited", "chat"], default="full",
                       help="评估模式: full (全知视角，包含隐藏动机), limited (有限信息，仅基本身份), 或 chat (闲聊模式，包含干扰话题)")
    parser.add_argument("--workers", type=int, default=4, help="最大线程数")
    parser.add_argument("--limit", type=int, default=None, 
                       help="限制评测的样本数量 (例如: --limit 500 只评测前500条)")
    parser.add_argument("--start", type=int, default=1, 
                       help="从第几个样本开始评测 (例如: --start 18 从第18个样本开始)")
    parser.add_argument("--output", default=None, help="结果输出目录(默认使用时间戳)")
    
    args = parser.parse_args()
    
    print("🎯 模型评测系统")
    print("="*60)
    
    # 使用命令行参数
    data_file = args.data
    models = args.models
    max_workers = args.workers
    sample_limit = args.limit
    start_sample = args.start
    language = args.language
    evaluation_mode = args.mode
    use_siliconflow = args.platform == "siliconflow"
    use_agentworld = args.platform == "agentworld"
    use_yunwu = args.platform == "yunwu"
    
    # 使用时间戳创建唯一的结果目录
    if args.output:
        output_dir = args.output
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = f"results_{timestamp}"
    
    print(f"📊 数据文件: {data_file}")
    print(f"🤖 评测模型: {', '.join(models)}")
    platform_name = "云雾AI" if use_yunwu else ("AgentWorld" if use_agentworld else ("硅基流动" if use_siliconflow else "OpenRouter"))
    print(f"🌐 API平台: {platform_name}")
    print(f"🌍 数据语言: {'中文' if language == 'zh' else '英文'}")
    print(f"🔍 评估模式: {'全知视角' if evaluation_mode == 'full' else '有限信息'}")
    print(f"🧵 线程数: {max_workers}")
    print(f"🎯 开始样本: 第{start_sample}个")
    if sample_limit:
        print(f"📋 样本限制: 最多{sample_limit}条")
    print(f"📁 输出目录: {output_dir}")
    
    # 检查数据文件
    if not Path(data_file).exists():
        print(f"❌ 数据文件不存在: {data_file}")
        return
    
    # 创建评测器
    evaluator = MultiThreadEvaluator(models=models, max_workers=max_workers, use_siliconflow=use_siliconflow, use_agentworld=use_agentworld, use_yunwu=use_yunwu, language=language, evaluation_mode=evaluation_mode)
    
    # 加载数据集
    samples = evaluator.load_dataset(data_file)
    if not samples:
        print("❌ 无法加载数据集")
        return
    
    # 应用开始位置和样本数量限制
    original_count = len(samples)
    
    # 先应用开始位置
    if start_sample > 1:
        if start_sample > len(samples):
            print(f"❌ 开始位置 {start_sample} 超出样本总数 {len(samples)}")
            return
        samples = samples[start_sample-1:]
        print(f"🎯 从第{start_sample}个样本开始，剩余 {len(samples)} 条样本")
    
    # 再应用数量限制
    if sample_limit and sample_limit > 0:
        samples = samples[:sample_limit]
        print(f"📋 样本限制: 最多评测 {len(samples)} 条")
    
    print(f"📊 最终评测样本数: {len(samples)} 条 (原始总数: {original_count})")
    
    # 显示样本限制信息
    if sample_limit:
        print(f"⚠️  注意: 使用 --limit {sample_limit} 参数，只评测前{len(samples)}条样本")
    
    # 确认开始评测
    print(f"\n准备评测 {len(samples)} 个样本...")
    print(f"预计总任务数: {len(samples) * len(models) * 3}")
    
    response = input("是否开始评测? (y/N): ")
    if response.lower() != 'y':
        print("❌ 评测已取消")
        return
    
    try:
        # 执行评测
        print(f"\n🚀 开始评测...")
        # 运行评测
        try:
            evaluator.evaluate_dataset(
                samples=samples,
                output_dir=output_dir
            )
            # 打印客户端统计
            for model, client in evaluator.clients.items():
                print(f"\n{model} 客户端统计:")
                client.print_stats()
        except Exception as e:
            print(f"\n❌ 评测过程中出错: {e}")
            import traceback
            traceback.print_exc()
        
        print(f"\n🎉 评测完成！结果已保存到 {output_dir} 目录")
        
    except KeyboardInterrupt:
        print(f"\n⚠️ 评测被用户中断")
    except Exception as e:
        print(f"\n❌ 评测过程中出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
