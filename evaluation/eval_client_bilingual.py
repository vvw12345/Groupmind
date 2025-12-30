"""
双语评测API客户端 - 支持中英文数据评测
"""
import requests
import json
import time
import threading
from typing import Dict, Any, Optional, List
from pathlib import Path
import sys
from queue import Queue
import random

# 添加主目录到Python路径
sys.path.append(str(Path(__file__).parent.parent))
from config import OPENROUTER_CONFIG, SILICONFLOW_CONFIG, YUNWU_CONFIG
# 导入AgentWorld配置
sys.path.append(str(Path(__file__).parent.parent / "data_generator"))
from api_client import AGENTWORLD_CONFIG

class BilingualEvaluationClient:
    """双语评测API客户端"""
    
    def __init__(self, models: List[str] = None, use_siliconflow: bool = False, use_agentworld: bool = False, use_yunwu: bool = False, language: str = "zh", evaluation_mode: str = "full"):
        self.use_siliconflow = use_siliconflow
        self.use_agentworld = use_agentworld
        self.use_yunwu = use_yunwu
        self.language = language  # "zh" for Chinese, "en" for English
        self.evaluation_mode = evaluation_mode  # "full" or "limited"
        
        if use_yunwu:
            self.base_url = YUNWU_CONFIG["base_url"]
            self.api_keys = YUNWU_CONFIG["api_keys"]
            self.models = models or YUNWU_CONFIG["models"]
            # 存储模型专用密钥配置
            self.model_specific_keys = YUNWU_CONFIG.get("model_specific_keys", {})
        elif use_agentworld:
            self.base_url = AGENTWORLD_CONFIG["base_url"]
            self.model_api_mapping = AGENTWORLD_CONFIG["model_api_mapping"]
            self.models = models or ["gpt-5.1", "gemini-2.5-pro"]
            self.api_keys = list(self.model_api_mapping.values())  # 为兼容性创建api_keys列表
            self.model_specific_keys = {}
        elif use_siliconflow:
            self.base_url = SILICONFLOW_CONFIG["base_url"]
            self.api_keys = SILICONFLOW_CONFIG["api_keys"]
            self.models = models or [
                "Qwen/Qwen2.5-7B-Instruct",
                "Qwen/Qwen2.5-14B-Instruct"
            ]
            self.model_specific_keys = {}
        else:
            self.base_url = OPENROUTER_CONFIG["base_url"]
            self.api_keys = OPENROUTER_CONFIG["api_keys"]
            self.models = models or [
                "moonshotai/kimi-k2:free",
                "z-ai/glm-4.5-air:free"
            ]
            self.model_specific_keys = {}
        
        # API使用状态
        self.current_key_index = 0
        self.current_model_index = 0
        self.lock = threading.Lock()
        
        # 限流设置
        self.rate_limit_delay = 0.5  # 每次请求间隔
        self.key_last_used = {}  # 记录每个密钥的最后使用时间
        
        # 重试设置
        self.max_retries = 10
        
        # 统计信息
        self.stats = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'key_switches': 0,
            'rate_limit_hits': 0,
            'model_usage': {model: 0 for model in self.models}
        }
        
        mode_names = {
            'full': '全知视角',
            'limited': '有限信息', 
            'chat': '闲聊模式'
        }
        mode_display = mode_names.get(evaluation_mode, evaluation_mode)
        print(f"🤖 评测客户端初始化完成 (语言: {'中文' if language == 'zh' else '英文'}, 模式: {mode_display})")
        if use_agentworld:
            print(f"📊 模型API映射: {len(self.model_api_mapping)}个")
        else:
            print(f"📊 可用API密钥: {len(self.api_keys)}个")
        print(f"🔄 最大重试次数: {self.max_retries}次")
        print(f"🎯 评测模型: {', '.join(self.models)}")
        if len(self.models) > 1:
            print(f"💪 理论最大尝试次数: {self.max_retries * len(self.models)}次")
    
    def _get_current_model(self) -> str:
        """获取当前模型"""
        return self.models[self.current_model_index]
    
    def _get_current_key(self, model: str = None) -> str:
        """获取当前API密钥"""
        if self.use_agentworld and model:
            # AgentWorld模式：根据模型获取对应的API密钥
            return self.model_api_mapping.get(model, list(self.model_api_mapping.values())[0])
        elif model and model in self.model_specific_keys:
            # 模型专用密钥：优先使用模型专用密钥
            return self.model_specific_keys[model]
        else:
            # 其他模式：使用密钥轮换
            return self.api_keys[self.current_key_index]
    
    def _switch_key(self):
        """切换到下一个API密钥"""
        current_model = self._get_current_model()
        # AgentWorld模式或使用模型专用密钥时不需要切换密钥
        if not self.use_agentworld and current_model not in self.model_specific_keys:
            with self.lock:
                self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
                self.stats['key_switches'] += 1
    
    def _switch_model(self):
        """切换到下一个模型"""
        with self.lock:
            self.current_model_index = (self.current_model_index + 1) % len(self.models)
            print(f"🔄 切换模型: {self._get_current_model()}")
    
    def _apply_rate_limit(self):
        """应用限流延迟"""
        current_time = time.time()
        current_key = self._get_current_key()
        
        # 检查该密钥的上次使用时间
        if current_key in self.key_last_used:
            time_since_last = current_time - self.key_last_used[current_key]
            if time_since_last < self.rate_limit_delay:
                sleep_time = self.rate_limit_delay - time_since_last
                time.sleep(sleep_time)
        
        self.key_last_used[current_key] = time.time()
    
    def call_llm(self, messages: List[Dict], temperature: float = 0.3) -> Optional[str]:
        """调用LLM API"""
        self.stats['total_requests'] += 1
        
        for attempt in range(self.max_retries):
            try:
                # 应用限流
                self._apply_rate_limit()
                
                current_model = self._get_current_model()
                current_key = self._get_current_key(current_model)
                
                headers = {
                    "Authorization": f"Bearer {current_key}",
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "model": current_model,
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": 1000
                }
                
                response = requests.post(
                    self.base_url,
                    headers=headers,
                    json=payload,
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    content = data['choices'][0]['message']['content']
                    
                    # 更新统计
                    self.stats['successful_requests'] += 1
                    self.stats['model_usage'][current_model] += 1
                    
                    return content
                
                elif response.status_code == 429:
                    # 限流错误
                    self.stats['rate_limit_hits'] += 1
                    print(f"⚠️ 限流错误 (429), 尝试 {attempt + 1}/{self.max_retries}, "
                          f"当前密钥: {self.current_key_index + 1}/{len(self.api_keys) if not self.use_agentworld else 'N/A'}")
                    
                    if attempt < self.max_retries - 1:
                        # 如果有多个API密钥，则切换；否则保持当前密钥
                        if not self.use_agentworld and len(self.api_keys) > 1:
                            self._switch_key()
                            print(f"🔄 切换API密钥: {self.current_key_index+1}/{len(self.api_keys)}")
                        
                        sleep_time = 1.0  # 固定1秒延迟
                        print(f"⏱️ 延迟 {sleep_time:.1f}s 后重试")
                        time.sleep(sleep_time)
                    
                elif response.status_code == 401:
                    # 认证错误，切换密钥
                    print(f"❌ 认证错误 (401), 切换密钥")
                    self._switch_key()
                    
                else:
                    print(f"❌ API错误: {response.status_code} - {response.text}")
                    
            except requests.exceptions.Timeout:
                print(f"⏰ 请求超时, 尝试 {attempt + 1}/{self.max_retries}")
                
            except Exception as e:
                print(f"❌ 请求异常: {e}")
                
            # 失败重试前的延迟
            if attempt < self.max_retries - 1:
                time.sleep(random.uniform(1, 2))
        
        # 所有重试都失败
        self.stats['failed_requests'] += 1
        return None
    
    def evaluate_sample(self, sample: Dict, task_type: str) -> Optional[Dict]:
        """评测单个样本的特定任务"""
        try:
            # 构建评测prompt
            prompt = self._build_evaluation_prompt(sample, task_type)
            
            # 根据语言和评估模式选择system prompt
            if self.evaluation_mode == "limited":
                if self.language == "zh":
                    system_prompt = "你是一个专业的对话分析专家。请以审慎的态度仔细观察对话中的细节，从语言、语调、互动模式等方面进行推理分析。"
                else:
                    system_prompt = "You are a professional dialogue analysis expert. Please approach the analysis with caution and carefully observe details in the conversation, reasoning from language, tone, and interaction patterns."
            elif self.evaluation_mode == "chat":
                # Chat模式根据是否有完整角色信息来调整系统提示
                if self._has_full_persona_info(sample):
                    # 有完整角色信息，使用全知视角提示
                    if self.language == "zh":
                        system_prompt = "你是一个专业的对话分析专家。请仔细分析包含闲聊内容的多人对话场景，你可以看到每个角色的隐藏动机和集体意图，注意区分闲聊话题和核心冲突内容。"
                    else:
                        system_prompt = "You are a professional dialogue analysis expert. Please carefully analyze multi-person dialogue scenarios that include casual chat content. You can see each character's hidden motives and collective intentions. Distinguish between casual topics and core conflict content."
                else:
                    # 没有完整角色信息，使用有限信息提示
                    if self.language == "zh":
                        system_prompt = "你是一个专业的对话分析专家。请仔细分析包含闲聊内容的多人对话场景，注意区分闲聊话题和核心冲突内容。"
                    else:
                        system_prompt = "You are a professional dialogue analysis expert. Please carefully analyze multi-person dialogue scenarios that include casual chat content, distinguishing between casual topics and core conflict content."
            else:
                if self.language == "zh":
                    system_prompt = "你是一个专业的对话分析专家，请仔细分析给定的多人对话场景。"
                else:
                    system_prompt = "You are a professional dialogue analysis expert. Please carefully analyze the given multi-person dialogue scenario."
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
            
            # 调用API
            response = self.call_llm(messages)
            if not response:
                return None
            
            # 解析响应
            result = self._parse_evaluation_response(response, sample, task_type)
            return result
            
        except Exception as e:
            print(f"❌ 评测样本失败: {e}")
            return None
    
    def _build_evaluation_prompt(self, sample: Dict, task_type: str) -> str:
        """构建评测prompt - 支持中英文和不同评估模式"""
        
        if self.evaluation_mode == "limited":
            # 有限信息模式：只提供基本身份和对话
            if self.language == "zh":
                return self._build_chinese_limited_prompt(sample, task_type)
            else:
                return self._build_english_limited_prompt(sample, task_type)
        elif self.evaluation_mode == "chat":
            # 闲聊模式：可以是全知视角或有限信息，但使用闲聊数据集
            # 这里我们需要检查是否有完整的角色信息来决定使用哪种模式
            if self._has_full_persona_info(sample):
                # 如果有完整的角色信息，使用全知视角
                if self.language == "zh":
                    return self._build_chinese_chat_full_prompt(sample, task_type)
                else:
                    return self._build_english_chat_full_prompt(sample, task_type)
            else:
                # 否则使用有限信息模式
                if self.language == "zh":
                    return self._build_chinese_limited_prompt(sample, task_type)
                else:
                    return self._build_english_limited_prompt(sample, task_type)
        else:
            # 全知视角模式：提供完整信息
            if self.language == "zh":
                return self._build_chinese_prompt(sample, task_type)
            else:
                return self._build_english_prompt(sample, task_type)
    
    def _build_chinese_prompt(self, sample: Dict, task_type: str) -> str:
        """构建中文评测prompt"""
        scenario = sample['scenario_setup']
        dialogue = sample['dialogue_transcript']
        trigger = sample['evaluation_trigger']
        labels = sample['evaluation_labels']
        
        # 构建对话文本
        dialogue_text = "\n".join([
            f"Turn {turn['turn']}: {turn['speaker']}: {turn['line']}"
            for turn in dialogue
        ])
        
        base_context = f"""
场景描述: {scenario['scenario_description']}

角色设定:
{chr(10).join([f"- {p['name']}: 公开目标({p['public_goal']}) | 隐藏动机({p['private_motive']})" for p in scenario['personas']])}

隐藏集体意图: {scenario['hidden_collective_intent']}

对话内容:
{dialogue_text}

关键时刻: Turn {trigger['trigger_turn_id']} - {trigger['trigger_description']}
"""
        
        if task_type == "atmosphere_recognition":
            question = labels['atmosphere_recognition']
            return f"""{base_context}

请分析在关键时刻后，群体氛围最突出的变化是什么？

问题: {question['question']}

选项:
{chr(10).join([f"{i+1}. {opt[3:]}" for i, opt in enumerate(question['mcq_options'])])}

请只回答选项编号(1-6)，不要解释。"""

        elif task_type == "ky_test":
            question = labels['ky_test']
            return f"""{base_context}

请分析在当前情况下，最合时宜的回应应该是什么？

问题: {question['question']}

选项:
{chr(10).join([f"{i+1}. {opt[3:]}" for i, opt in enumerate(question['mcq_options'])])}

请只回答选项编号(1-6)，不要解释。"""

        elif task_type == "subtext_deciphering":
            question = labels['subtext_deciphering']
            return f"""{base_context}

请分析以下对话中的潜台词含义：

问题: {question['question']}

选项:
{chr(10).join([f"{i+1}. {opt[3:]}" for i, opt in enumerate(question['mcq_options'])])}

请只回答选项编号(1-6)，不要解释。"""
        
        return ""
    
    def _build_chinese_limited_prompt(self, sample: Dict, task_type: str) -> str:
        """构建中文有限信息评测prompt - 只提供基本身份和对话"""
        scenario = sample['scenario_setup']
        dialogue = sample['dialogue_transcript']
        trigger = sample['evaluation_trigger']
        labels = sample['evaluation_labels']
        
        # 构建对话文本
        dialogue_text = "\n".join([
            f"Turn {turn['turn']}: {turn['speaker']}: {turn['line']}"
            for turn in dialogue
        ])
        
        # 只提供基本角色名称（不包含任何目标、动机和集体意图）
        basic_personas = "\n".join([f"- {p['name']}" for p in scenario['personas']])
        
        base_context = f"""
场景描述: {scenario['scenario_description']}

角色设定:
{basic_personas}

对话内容:
{dialogue_text}

关键时刻: Turn {trigger['trigger_turn_id']} - {trigger['trigger_description']}
"""
        
        if task_type == "atmosphere_recognition":
            question = labels['atmosphere_recognition']
            return f"""{base_context}

请仔细观察对话中的语言细节、说话方式和互动模式，基于你能观察到的具体线索进行审慎推理。

请分析在关键时刻后，群体氛围最突出的变化是什么？

问题: {question['question']}

选项:
{chr(10).join([f"{i+1}. {opt[3:]}" for i, opt in enumerate(question['mcq_options'])])}

请只回答选项编号(1-6)，不要解释。"""

        elif task_type == "ky_test":
            question = labels['ky_test']
            return f"""{base_context}

请仔细观察对话中的语言细节、说话方式和互动模式，基于你能观察到的具体线索进行审慎推理。

请分析在当前情况下，最合时宜的回应应该是什么？

问题: {question['question']}

选项:
{chr(10).join([f"{i+1}. {opt[3:]}" for i, opt in enumerate(question['mcq_options'])])}

请只回答选项编号(1-6)，不要解释。"""

        elif task_type == "subtext_deciphering":
            question = labels['subtext_deciphering']
            return f"""{base_context}

请仔细观察对话中的语言细节、说话方式和互动模式，基于你能观察到的具体线索进行审慎推理。

请分析以下对话中的潜台词含义：

问题: {question['question']}

选项:
{chr(10).join([f"{i+1}. {opt[3:]}" for i, opt in enumerate(question['mcq_options'])])}

请只回答选项编号(1-6)，不要解释。"""
        
        return ""
    
    def _build_english_prompt(self, sample: Dict, task_type: str) -> str:
        """构建英文评测prompt"""
        scenario = sample['scenario_setup']
        dialogue = sample['dialogue_transcript']
        trigger = sample['evaluation_trigger']
        labels = sample['evaluation_labels']
        
        # 构建对话文本
        dialogue_text = "\n".join([
            f"Turn {turn['turn']}: {turn['speaker']}: {turn['line']}"
            for turn in dialogue
        ])
        
        base_context = f"""
Scenario Description: {scenario['scenario_description']}

Character Settings:
{chr(10).join([f"- {p['name']}: Public Goal({p['public_goal']}) | Private Motive({p['private_motive']})" for p in scenario['personas']])}

Hidden Collective Intent: {scenario['hidden_collective_intent']}

Dialogue Content:
{dialogue_text}

Critical Moment: Turn {trigger['trigger_turn_id']} - {trigger['trigger_description']}
"""
        
        if task_type == "atmosphere_recognition":
            question = labels['atmosphere_recognition']
            return f"""{base_context}

Please analyze what the most prominent change in group atmosphere is after the critical moment.

Question: {question['question']}

Options:
{chr(10).join([f"{i+1}. {opt[3:]}" for i, opt in enumerate(question['mcq_options'])])}

Please only answer with the option number (1-6), no explanation needed."""

        elif task_type == "ky_test":
            question = labels['ky_test']
            return f"""{base_context}

Please analyze what the most appropriate response should be in the current situation.

Question: {question['question']}

Options:
{chr(10).join([f"{i+1}. {opt[3:]}" for i, opt in enumerate(question['mcq_options'])])}

Please only answer with the option number (1-6), no explanation needed."""

        elif task_type == "subtext_deciphering":
            question = labels['subtext_deciphering']
            return f"""{base_context}

Please analyze the subtext meaning in the following dialogue:

Question: {question['question']}

Options:
{chr(10).join([f"{i+1}. {opt[3:]}" for i, opt in enumerate(question['mcq_options'])])}

Please only answer with the option number (1-6), no explanation needed."""
        
        return ""
    
    def _build_english_limited_prompt(self, sample: Dict, task_type: str) -> str:
        """构建英文有限信息评测prompt - 只提供基本身份和对话"""
        scenario = sample['scenario_setup']
        dialogue = sample['dialogue_transcript']
        trigger = sample['evaluation_trigger']
        labels = sample['evaluation_labels']
        
        # 构建对话文本
        dialogue_text = "\n".join([
            f"Turn {turn['turn']}: {turn['speaker']}: {turn['line']}"
            for turn in dialogue
        ])
        
        # 只提供基本角色名称（不包含任何目标、动机和集体意图）
        basic_personas = "\n".join([f"- {p['name']}" for p in scenario['personas']])
        
        base_context = f"""
Scenario Description: {scenario['scenario_description']}

Character Settings:
{basic_personas}

Dialogue Content:
{dialogue_text}

Critical Moment: Turn {trigger['trigger_turn_id']} - {trigger['trigger_description']}
"""
        
        if task_type == "atmosphere_recognition":
            question = labels['atmosphere_recognition']
            return f"""{base_context}

Please analyze what the most prominent change in group atmosphere is after the critical moment.

Question: {question['question']}

Options:
{chr(10).join([f"{i+1}. {opt[3:]}" for i, opt in enumerate(question['mcq_options'])])}

Please only answer with the option number (1-6), no explanation needed."""

        elif task_type == "ky_test":
            question = labels['ky_test']
            return f"""{base_context}

Please analyze what the most appropriate response should be in the current situation.

Question: {question['question']}

Options:
{chr(10).join([f"{i+1}. {opt[3:]}" for i, opt in enumerate(question['mcq_options'])])}

Please only answer with the option number (1-6), no explanation needed."""

        elif task_type == "subtext_deciphering":
            question = labels['subtext_deciphering']
            return f"""{base_context}

Please analyze the subtext meaning in the following dialogue:

Question: {question['question']}

Options:
{chr(10).join([f"{i+1}. {opt[3:]}" for i, opt in enumerate(question['mcq_options'])])}

Please only answer with the option number (1-6), no explanation needed."""
        
        return ""
    
    def _parse_evaluation_response(self, response: str, sample: Dict, task_type: str) -> Dict:
        """解析评测响应"""
        # 提取数字答案
        import re
        numbers = re.findall(r'\b([1-6])\b', response.strip())
        
        if not numbers:
            return {
                'predicted_answer': -1,
                'raw_response': response,
                'parse_error': True
            }
        
        predicted_answer = int(numbers[0]) - 1  # 转换为0-based索引
        
        # 获取正确答案
        correct_answer = sample['evaluation_labels'][task_type]['correct_answer_index']
        
        return {
            'predicted_answer': predicted_answer,
            'correct_answer': correct_answer,
            'is_correct': predicted_answer == correct_answer,
            'raw_response': response.strip(),
            'parse_error': False
        }
    
    def print_stats(self):
        """打印统计信息"""
        print("\n" + "="*60)
        print(f"📊 双语评测客户端统计信息 ({'中文' if self.language == 'zh' else '英文'})")
        print("="*60)
        print(f"总请求数: {self.stats['total_requests']}")
        print(f"成功请求: {self.stats['successful_requests']}")
        print(f"失败请求: {self.stats['failed_requests']}")
        print(f"成功率: {self.stats['successful_requests']/max(self.stats['total_requests'], 1)*100:.1f}%")
        print(f"密钥切换次数: {self.stats['key_switches']}")
        print(f"限流命中次数: {self.stats['rate_limit_hits']}")
        print(f"当前使用模型: {self._get_current_model()}")
        if not self.use_agentworld:
            print(f"当前API密钥: {self.current_key_index + 1}/{len(self.api_keys)}")
            print(f"密钥利用率: {(self.current_key_index + 1)/len(self.api_keys)*100:.1f}%")
            print(f"平均每密钥请求数: {self.stats['total_requests']/max(self.stats['key_switches'] + 1, 1):.1f}")
        print(f"当前延迟设置: {self.rate_limit_delay:.1f}秒")
        
        print(f"\n模型使用统计:")
        for model, count in self.stats['model_usage'].items():
            print(f"  {model}: {count}次")
        print("="*60)
    
    def _has_full_persona_info(self, sample: Dict) -> bool:
        """检查样本是否包含完整的角色信息（用于判断是否可以使用全知视角）"""
        try:
            scenario = sample.get('scenario_setup', {})
            personas = scenario.get('personas', [])
            
            # 检查是否有角色信息
            if not personas:
                return False
            
            # 检查每个角色是否有完整信息
            for persona in personas:
                if not all(key in persona for key in ['name', 'public_goal', 'private_motive']):
                    return False
            
            # 检查是否有隐藏集体意图
            if 'hidden_collective_intent' not in scenario:
                return False
            
            return True
        except:
            return False
    
    def _build_chinese_chat_full_prompt(self, sample: Dict, task_type: str) -> str:
        """构建中文Chat模式全知视角prompt"""
        scenario = sample['scenario_setup']
        dialogue = sample['dialogue_transcript']
        trigger = sample['evaluation_trigger']
        labels = sample['evaluation_labels']
        
        # 构建对话文本
        dialogue_text = "\n".join([
            f"Turn {turn['turn']}: {turn['speaker']}: {turn['line']}"
            for turn in dialogue
        ])
        
        base_context = f"""
场景描述: {scenario['scenario_description']}

角色设定:
{chr(10).join([f"- {p['name']}: 公开目标({p['public_goal']}) | 隐藏动机({p['private_motive']})" for p in scenario['personas']])}

隐藏集体意图: {scenario['hidden_collective_intent']}

对话内容:
{dialogue_text}

关键时刻: Turn {trigger['trigger_turn_id']} - {trigger['trigger_description']}

注意：这是一个包含闲聊内容的对话场景，请注意区分闲聊话题和核心冲突内容，重点分析与社交互动相关的部分。
"""
        
        if task_type == "atmosphere_recognition":
            question = labels['atmosphere_recognition']
            return f"""{base_context}

问题: {question['question']}

选项:
{chr(10).join([f"{i}. {option}" for i, option in enumerate(question['mcq_options'])])}

请仔细分析对话中的氛围变化，特别注意闲聊内容如何影响整体氛围。请只回答选项编号(0-{len(question['mcq_options'])-1})。"""

        elif task_type == "ky_test":
            question = labels['ky_test']
            return f"""{base_context}

问题: {question['question']}

选项:
{chr(10).join([f"{i}. {option}" for i, option in enumerate(question['mcq_options'])])}

请分析在这个包含闲聊的复杂社交场景中，什么是最合时宜的回应。请只回答选项编号(0-{len(question['mcq_options'])-1})。"""

        elif task_type == "subtext_deciphering":
            question = labels['subtext_deciphering']
            return f"""{base_context}

问题: {question['question']}

选项:
{chr(10).join([f"{i}. {option}" for i, option in enumerate(question['mcq_options'])])}

请深入分析对话中的潜台词，注意区分闲聊内容和真正的隐含意图。请只回答选项编号(0-{len(question['mcq_options'])-1})。"""
    
    def _build_english_chat_full_prompt(self, sample: Dict, task_type: str) -> str:
        """构建英文Chat模式全知视角prompt"""
        scenario = sample['scenario_setup']
        dialogue = sample['dialogue_transcript']
        trigger = sample['evaluation_trigger']
        labels = sample['evaluation_labels']
        
        # 构建对话文本
        dialogue_text = "\n".join([
            f"Turn {turn['turn']}: {turn['speaker']}: {turn['line']}"
            for turn in dialogue
        ])
        
        base_context = f"""
Scenario Description: {scenario['scenario_description']}

Character Settings:
{chr(10).join([f"- {p['name']}: Public Goal({p['public_goal']}) | Hidden Motive({p['private_motive']})" for p in scenario['personas']])}

Hidden Collective Intent: {scenario['hidden_collective_intent']}

Dialogue Content:
{dialogue_text}

Key Moment: Turn {trigger['trigger_turn_id']} - {trigger['trigger_description']}

Note: This is a dialogue scenario that includes casual chat content. Please distinguish between casual topics and core conflict content, focusing on analyzing social interaction aspects.
"""
        
        if task_type == "atmosphere_recognition":
            question = labels['atmosphere_recognition']
            return f"""{base_context}

Question: {question['question']}

Options:
{chr(10).join([f"{i}. {option}" for i, option in enumerate(question['mcq_options'])])}

Please carefully analyze the atmospheric changes in the dialogue, paying special attention to how casual chat content affects the overall atmosphere. Please only answer with the option number (0-{len(question['mcq_options'])-1})."""

        elif task_type == "ky_test":
            question = labels['ky_test']
            return f"""{base_context}

Question: {question['question']}

Options:
{chr(10).join([f"{i}. {option}" for i, option in enumerate(question['mcq_options'])])}

Please analyze what would be the most appropriate response in this complex social scenario that includes casual chat. Please only answer with the option number (0-{len(question['mcq_options'])-1})."""

        elif task_type == "subtext_deciphering":
            question = labels['subtext_deciphering']
            return f"""{base_context}

Question: {question['question']}

Options:
{chr(10).join([f"{i}. {option}" for i, option in enumerate(question['mcq_options'])])}

Please deeply analyze the subtext in the dialogue, distinguishing between casual chat content and genuine hidden intentions. Please only answer with the option number (0-{len(question['mcq_options'])-1})."""

# 为了向后兼容，保留原来的类名
EvaluationClient = BilingualEvaluationClient
