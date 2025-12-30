"""
统一数据生成主流水线 - 支持中英法日德文数据生成
使用 --language 参数控制生成中文、英文、法语、日语或德语数据
"""
import json
import argparse
import time
import sys
import random
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

from api_client import OpenRouterClient, AgentWorldClient
from scenario_generator import ScenarioGenerator, ScenarioGeneratorEN, ScenarioGeneratorFR, ScenarioGeneratorJP, ScenarioGeneratorDE
from dialogue_simulator import DialogueSimulator, DialogueSimulatorEN, DialogueSimulatorFR, DialogueSimulatorJP, DialogueSimulatorDE
from label_annotator import LabelAnnotator, LabelAnnotatorEN, LabelAnnotatorFR, LabelAnnotatorJP, LabelAnnotatorDE


def print_progress_bar(current, total, prefix='', suffix='', length=50):
    """打印进度条"""
    percent = 100 * (current / float(total))
    filled_length = int(length * current // total)
    bar = '█' * filled_length + '░' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {current}/{total} ({percent:.1f}%) {suffix}', end='', flush=True)
    if current == total:
        print()  # 完成后换行


def build_scene_atmosphere_index(language='zh'):
    """
    构建 scene × atmosphere 的全局索引映射
    
    Args:
        language: 'zh', 'en', 'fr', 'jp' 或 'de'
    
    Returns:
        list: [(scene_idx, atmosphere_idx, atmosphere_name), ...]
    """
    if language == 'zh':
        from scenario_seeds import SCENARIO_SEEDS
    elif language == 'en':
        from scenario_seeds_en import SCENARIO_SEEDS
    elif language == 'fr':
        from scenario_seeds_fr import SCENARIO_SEEDS
    elif language == 'jp':
        from scenario_seeds_jp import SCENARIO_SEEDS
    elif language == 'de':
        from scenario_seeds_de import SCENARIO_SEEDS
    else:
        from scenario_seeds import SCENARIO_SEEDS
    
    index_map = []
    for scene_idx, seed in enumerate(SCENARIO_SEEDS):
        all_atmospheres = seed['core_atmospheres'] + seed['optional_atmospheres']
        for atm_idx, atmosphere in enumerate(all_atmospheres):
            is_core = atmosphere in seed['core_atmospheres']
            index_map.append({
                'scene_idx': scene_idx,
                'atmosphere_idx': atm_idx,
                'atmosphere': atmosphere,
                'is_core': is_core,
                'scene': seed['scene']
            })
    return index_map


class DataGenerationPipeline:
    """统一数据生成流水线 - 支持中英法日德文"""
    
    def __init__(self, use_gpt51=True, target_model=None, language='zh'):
        # 初始化API客户端
        if use_gpt51:
            self.api_client = AgentWorldClient()
            if target_model:
                # 设置目标模型 - 处理模型名称映射
                actual_model_name = target_model
                if target_model == "gemini-2.5-pro":
                    actual_model_name = "gemini-2.5-pro-generateContent"
                
                if actual_model_name in self.api_client.models:
                    model_index = self.api_client.models.index(actual_model_name)
                    self.api_client.current_model_index = model_index
                    print(f"🎯 已设置目标模型: {actual_model_name}")
        else:
            self.api_client = OpenRouterClient()
            # 对于硅基流动，可以在这里设置特定的deepseek-v3模型
        
        self.language = language
        
        # 根据语言选择对应的生成器
        if language == 'zh':
            self.scenario_gen = ScenarioGenerator(self.api_client)
            self.dialogue_sim = DialogueSimulator(self.api_client)
            self.label_ann = LabelAnnotator(self.api_client)
            print("🌏 数据语言: 中文 (Chinese)")
        elif language == 'en':
            self.scenario_gen = ScenarioGeneratorEN(self.api_client)
            self.dialogue_sim = DialogueSimulatorEN(self.api_client)
            self.label_ann = LabelAnnotatorEN(self.api_client)
            print("🌍 数据语言: 英文 (English)")
        elif language == 'fr':
            self.scenario_gen = ScenarioGeneratorFR(self.api_client)
            self.dialogue_sim = DialogueSimulatorFR(self.api_client)
            self.label_ann = LabelAnnotatorFR(self.api_client)
            print("🇫🇷 数据语言: 法语 (French)")
        elif language == 'jp':
            self.scenario_gen = ScenarioGeneratorJP(self.api_client)
            self.dialogue_sim = DialogueSimulatorJP(self.api_client)
            self.label_ann = LabelAnnotatorJP(self.api_client)
            print("🇯🇵 数据语言: 日语 (Japanese)")
        elif language == 'de':
            self.scenario_gen = ScenarioGeneratorDE(self.api_client)
            self.dialogue_sim = DialogueSimulatorDE(self.api_client)
            self.label_ann = LabelAnnotatorDE(self.api_client)
            print("🇩🇪 数据语言: 德语 (German)")
        else:
            # 默认使用中文
            self.scenario_gen = ScenarioGenerator(self.api_client)
            self.dialogue_sim = DialogueSimulator(self.api_client)
            self.label_ann = LabelAnnotator(self.api_client)
            print("🌏 数据语言: 中文 (Chinese) - 默认")
        
        # 构建 scene × atmosphere 索引映射
        self.index_map = build_scene_atmosphere_index(language)
        total_combinations = len(self.index_map)
        print(f"📊 总组合数: {total_combinations} (scene × atmosphere)")
        
        # 完全自由发挥 - 不限制主题，让GPT-5.1充分发挥创造力
        # 基于强大的prompt设计，LLM能够自主创造各种复杂的社交场景
        self.use_free_generation = True
    
    def generate_one_sample(
        self, 
        benchmark_id: str, 
        theme: Optional[str] = None,
        show_details: bool = True,
        combination_index: Optional[int] = None
    ) -> Optional[Dict[str, Any]]:
        """
        生成一条完整的数据样本
        
        Args:
            benchmark_id: 样本ID
            theme: 主题(可选)
            show_details: 是否显示详细信息
            combination_index: scene×atmosphere 组合索引(可选)
            
        Returns:
            完整的样本数据,失败返回None
        """
        # 获取当前组合信息
        if combination_index is not None and combination_index < len(self.index_map):
            combo = self.index_map[combination_index]
            scene_idx = combo['scene_idx']
            atmosphere = combo['atmosphere']
            is_core = combo['is_core']
        else:
            scene_idx = None
            atmosphere = None
            is_core = None
        
        if show_details:
            print(f"\n{'='*60}")
            print(f"🎬 开始生成样本")
            if theme:
                print(f"📝 主题: {theme}")
            if combination_index is not None:
                print(f"🌱 场景索引: {scene_idx}")
                print(f"🎭 氛围: {atmosphere} {'(核心)' if is_core else '(可选)'}")
                print(f"📍 组合索引: {combination_index}/{len(self.index_map)}")
            print(f"{'='*60}")
        
        # Step 1: 生成情境（不做相似度检测，直接生成一次）
        if show_details:
            print(f"\n[1/3] 🎭 生成情境设定...", end='', flush=True)
        
        scenario_data = self.scenario_gen.generate(
            theme=theme, 
            seed_index=scene_idx,
            atmosphere=atmosphere
        )
        if not scenario_data:
            print(" ❌ 生成失败")
            return None
        
        if show_details:
            print(f" ✅")
            print(f"      场景: {scenario_data['scenario_description'][:60]}...")
            print(f"      角色数: {len(scenario_data['personas'])}")
        
        # Step 2: 生成对话
        if show_details:
            print("\n[2/3] 💬 生成对话...", end='', flush=True)
        dialogue_data = self.dialogue_sim.generate(scenario_data)
        if not dialogue_data:
            print(" ❌ 失败")
            return None
        if show_details:
            print(f" ✅")
            print(f"      对话轮数: {len(dialogue_data['dialogue_transcript'])}")
            print(f"      关键时刻: Turn {dialogue_data['evaluation_trigger']['trigger_turn_id']}")
        
        # Step 3: 生成标签
        if show_details:
            print("\n[3/3] 🏷️  生成评测标签...", end='', flush=True)
        label_data = self.label_ann.generate(scenario_data, dialogue_data)
        if not label_data:
            print(" ❌ 失败")
            return None
        if show_details:
            print(f" ✅")
            print(f"      潜台词解码: {len(label_data['subtext_deciphering']['mcq_options'])} 选项")
            print(f"      氛围识别: {len(label_data['atmosphere_recognition']['mcq_options'])} 选项")
            print(f"      KY测试: {len(label_data['ky_test']['mcq_options'])} 选项")
        
        # 组装最终数据
        final_sample = {
            "benchmark_id": benchmark_id,
            "meta_theme": theme if theme else ("自由主题" if self.language == 'zh' else "Free Theme"),
            "scene_index": scene_idx,
            "atmosphere": atmosphere,
            "is_core_atmosphere": is_core,
            "scenario_setup": scenario_data,
            "dialogue_transcript": dialogue_data["dialogue_transcript"],
            "evaluation_trigger": dialogue_data["evaluation_trigger"],
            "evaluation_labels": label_data
        }
        
        if show_details:
            print(f"\n✨ 样本 {benchmark_id} 生成完成!")
        return final_sample
    
    def generate_batch(
        self, 
        num_samples: int, 
        output_file: str,
        start_id: int = 1
    ):
        """
        批量生成数据
        
        Args:
            num_samples: 要生成的样本数量
            output_file: 输出文件路径
            start_id: 起始ID
        """
        print(f"\n{'#'*60}")
        lang_name = "中文" if self.language == 'zh' else ("英文" if self.language == 'en' else ("法语" if self.language == 'fr' else ("日语" if self.language == 'jp' else "德语")))
        print(f"🚀 开始批量生成{lang_name}数据")
        print(f"{'#'*60}")
        print(f"📊 目标数量: {num_samples}")
        print(f"📁 输出文件: {output_file}")
        print(f"🔢 起始ID: {start_id}")
        print(f"🌏 数据语言: {lang_name}")
        
        # 检查客户端类型并显示相应信息
        if hasattr(self.api_client, 'use_siliconflow'):
            # OpenRouterClient
            platform = "硅基流动" if self.api_client.use_siliconflow else "OpenRouter"
            print(f"🌐 API平台: {platform}")
            print(f"🤖 默认模型: {self.api_client._get_current_model()}")
            if self.api_client.use_siliconflow:
                print(f"🔑 API密钥数: {len(self.api_client.sf_api_keys)}")
            else:
                print(f"🔑 API密钥数: {len(self.api_client.or_api_keys)}")
        else:
            # AgentWorldClient
            print(f"🌐 API平台: AgentWorld GPT-5.1")
            print(f"🤖 当前模型: {self.api_client.get_current_model()}")
            print(f"🔑 API密钥: 已配置")
        print(f"{'#'*60}\n")
        
        successful_samples = []
        failed_count = 0
        
        start_time = time.time()
        
        # 创建数据集结构
        if hasattr(self.api_client, 'use_siliconflow'):
            # OpenRouterClient
            model_name = self.api_client._get_current_model()
            platform_name = "硅基流动" if self.api_client.use_siliconflow else "OpenRouter"
        else:
            # AgentWorldClient
            model_name = self.api_client.get_current_model()
            platform_name = "AgentWorld GPT-5.1"
        
        dataset = {
            "dataset_info": {
                "total_samples": num_samples,
                "generation_time": time.strftime("%Y-%m-%d %H:%M:%S"),
                "model": model_name,
                "platform": platform_name,
                "language": self.language,
                "total_combinations": len(self.index_map),
                "start_id": start_id,
                "actual_samples": 0,  # 将在生成过程中更新
                "failed_samples": 0,
                "total_time_seconds": 0,
                "avg_time_per_sample": 0
            },
            "samples": []
        }
        
        attempt_count = 0
        current_combination_failures = {}  # 记录每个场景组合的连续失败次数
        max_failures_per_combination = 3   # 每个场景组合最多允许失败3次
        
        while len(successful_samples) < num_samples:
            attempt_count += 1
            current_id = start_id + len(successful_samples)
            
            # 根据语言设置 benchmark_id 前缀
            if self.language == 'zh':
                benchmark_id = f"atm-mcq-zh-2025-{current_id:05d}"
            elif self.language == 'en':
                benchmark_id = f"atm-mcq-en-2025-{current_id:05d}"
            elif self.language == 'fr':
                benchmark_id = f"atm-mcq-fr-2025-{current_id:05d}"
            elif self.language == 'jp':
                benchmark_id = f"atm-mcq-jp-2025-{current_id:05d}"
            elif self.language == 'de':
                benchmark_id = f"atm-mcq-de-2025-{current_id:05d}"
            else:
                benchmark_id = f"atm-mcq-zh-2025-{current_id:05d}"  # 默认中文
            
            # 计算当前应该使用的 scene×atmosphere 组合索引
            combination_index = len(successful_samples) % len(self.index_map)
            
            # 检查当前组合是否已经失败太多次，如果是则跳过
            if current_combination_failures.get(combination_index, 0) >= max_failures_per_combination:
                print(f"⚠️  场景组合 #{combination_index} 已失败 {max_failures_per_combination} 次，跳过到下一个样本")
                # 创建一个跳过标记的样本
                skipped_sample = {
                    "benchmark_id": benchmark_id,
                    "meta_theme": "Skipped - Too Many Failures",
                    "scene_index": -1,
                    "atmosphere": "skipped",
                    "is_core_atmosphere": False,
                    "scenario_setup": {"skipped": True},
                    "dialogue": {"skipped": True},
                    "tasks": {"skipped": True}
                }
                successful_samples.append(skipped_sample)
                dataset["samples"].append(skipped_sample)
                print(f"⏭️  已跳过样本 {benchmark_id}")
                continue
            
            print(f"{'─'*60}")
            print(f"📝 尝试 {attempt_count}: {benchmark_id} (目标: {len(successful_samples)+1}/{num_samples})")
            print(f"🎯 生成模式: scene×atmosphere 组合 #{combination_index}")
            print(f"{'─'*60}")
            
            sample_start = time.time()
            sample = self.generate_one_sample(
                benchmark_id, 
                theme=None, 
                show_details=True, 
                combination_index=combination_index
            )
            sample_time = time.time() - sample_start
            
            if sample:
                successful_samples.append(sample)
                dataset["samples"].append(sample)
                # 重置当前组合的失败计数
                current_combination_failures[combination_index] = 0
                
                # 更新数据集统计信息
                current_time = time.time()
                elapsed_time = current_time - start_time
                dataset["dataset_info"]["actual_samples"] = len(successful_samples)
                dataset["dataset_info"]["failed_samples"] = failed_count
                dataset["dataset_info"]["total_attempts"] = attempt_count
                dataset["dataset_info"]["success_rate"] = len(successful_samples) / attempt_count * 100
                dataset["dataset_info"]["total_time_seconds"] = elapsed_time
                dataset["dataset_info"]["avg_time_per_sample"] = elapsed_time / len(successful_samples) if len(successful_samples) > 0 else 0
                
                # 🔄 每成功生成一条就立即保存
                try:
                    with open(output_file, "w", encoding="utf-8") as f:
                        json.dump(dataset, f, ensure_ascii=False, indent=2)
                    print(f"💾 已保存: {len(successful_samples)} 条样本")
                except Exception as e:
                    print(f"⚠️  保存失败: {e}")
                
                # 计算预估剩余时间
                avg_time_per_success = elapsed_time / len(successful_samples)
                remaining_samples = num_samples - len(successful_samples)
                estimated_remaining_time = avg_time_per_success * remaining_samples
                
                success_rate = len(successful_samples) / attempt_count * 100
                
                print(f"✅ 样本生成成功 (耗时: {sample_time:.1f}秒)")
                print_progress_bar(
                    len(successful_samples), 
                    num_samples, 
                    prefix='成功样本:',
                    suffix=f'尝试:{attempt_count} 成功率:{success_rate:.1f}% 预计剩余:{estimated_remaining_time:.0f}秒'
                )
            else:
                failed_count += 1
                # 增加当前组合的失败计数
                current_combination_failures[combination_index] = current_combination_failures.get(combination_index, 0) + 1
                success_rate = len(successful_samples) / attempt_count * 100 if attempt_count > 0 else 0
                print(f"❌ 样本生成失败 (组合 #{combination_index} 失败次数: {current_combination_failures[combination_index]}/{max_failures_per_combination})")
                print_progress_bar(
                    len(successful_samples), 
                    num_samples, 
                    prefix='成功样本:',
                    suffix=f'尝试:{attempt_count} 成功率:{success_rate:.1f}% 失败:{failed_count}'
                )
            
            # 短暂休息,避免过快请求
            if len(successful_samples) < num_samples:
                time.sleep(0.5)
        
        # 统计信息
        elapsed_time = time.time() - start_time
        
        # 更新数据集的最终统计信息
        dataset["dataset_info"].update({
            "actual_samples": len(successful_samples),
            "failed_samples": failed_count,
            "total_attempts": attempt_count,
            "success_rate": round(len(successful_samples) / attempt_count * 100, 2) if attempt_count > 0 else 0,
            "total_time_seconds": round(elapsed_time, 2),
            "avg_time_per_sample": round(elapsed_time / max(len(successful_samples), 1), 2)
        })
        
        # 最终保存完整数据集
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(dataset, f, ensure_ascii=False, indent=2)
        
        lang_name = "中文" if self.language == 'zh' else ("英文" if self.language == 'en' else ("法语" if self.language == 'fr' else ("日语" if self.language == 'jp' else "德语")))
        print(f"\n{'#'*60}")
        print(f"🎉 目标完成! 成功收集到 {len(successful_samples)} 条有效{lang_name}样本!")
        print(f"{'#'*60}")
        print(f"✅ 成功样本: {len(successful_samples)}")
        print(f"❌ 失败次数: {failed_count}")
        print(f"🎯 总尝试次数: {attempt_count}")
        print(f"📊 成功率: {len(successful_samples) / attempt_count * 100:.1f}%")
        print(f"⏱️  总耗时: {elapsed_time:.2f} 秒")
        print(f"⚡ 平均每条: {elapsed_time / len(successful_samples):.1f} 秒")
        print(f"📁 输出文件: {output_file}")
        print(f"{'#'*60}\n")
        
        # 打印API统计
        self.api_client.print_stats()
        
        return successful_samples


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="统一数据生成流水线 - 支持中英文")
    parser.add_argument(
        "--num", 
        type=int, 
        default=200, 
        help="要生成的样本数量(默认: 200)"
    )
    parser.add_argument(
        "--output", 
        type=str, 
        default=None,
        help="输出文件路径(默认: benchmark_{lang}_N{num}_YYYYMMDD_HHMMSS.json)"
    )
    parser.add_argument(
        "--start-id",
        type=int,
        default=1,
        help="起始ID(默认: 1)"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="gpt-5.1",
        choices=["gpt-5.1", "deepseek-v3", "o1-preview", "gemini-2.5-pro"],
        help="选择生成模型 (默认: gpt-5.1)"
    )
    parser.add_argument(
        "--language",
        type=str,
        default="zh",
        choices=["zh", "en", "fr", "jp", "de"],
        help="数据语言: zh=中文, en=英文, fr=法语, jp=日语, de=德语 (默认: zh)"
    )
    
    args = parser.parse_args()
    
    # 生成默认输出文件名
    if args.output is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        args.output = f"benchmark_{args.language}_N{args.num}_{timestamp}.json"
    
    # 确保输出目录存在
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 如果文件已存在,清空它
    if output_path.exists():
        output_path.unlink()
    
    # 根据模型选择确定使用哪个客户端
    lang_name = "中文" if args.language == 'zh' else ("英文" if args.language == 'en' else ("法语" if args.language == 'fr' else ("日语" if args.language == 'jp' else "德语")))
    if args.model in ["gpt-5.1", "o1-preview", "gemini-2.5-pro"]:
        use_gpt51 = True
        print(f"🚀 使用 AgentWorld 平台调用 {args.model} 生成{lang_name}数据")
    else:  # deepseek-v3
        use_gpt51 = False
        print(f"🚀 使用硅基流动平台调用 {args.model} 生成{lang_name}数据")
    
    # 创建流水线并运行
    pipeline = DataGenerationPipeline(
        use_gpt51=use_gpt51, 
        target_model=args.model,
        language=args.language
    )
    pipeline.generate_batch(
        num_samples=args.num,
        output_file=args.output,
        start_id=args.start_id
    )


if __name__ == "__main__":
    main()
