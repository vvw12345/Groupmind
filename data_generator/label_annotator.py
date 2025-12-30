"""
黄金标签标注器 - 生成三个评测任务的标准答案
"""
import json
from typing import Dict, Any, Optional
from api_client import OpenRouterClient


class LabelAnnotator:
    """黄金标签标注器"""
    
    def __init__(self, api_client: OpenRouterClient):
        self.api_client = api_client
        
        # 加载提示词模板
        with open("prompt/get_prompt_for_labels.txt", "r", encoding="utf-8") as f:
            self.prompt_template = f.read()
    
    def generate(
        self, 
        scenario_data: Dict[str, Any], 
        dialogue_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        基于情境和对话生成评测标签
        
        Args:
            scenario_data: 情境设定数据
            dialogue_data: 对话数据
            
        Returns:
            评测标签的JSON对象,失败返回None
        """
        # 将数据转换为JSON字符串
        scenario_json_str = json.dumps(scenario_data, ensure_ascii=False, indent=2)
        dialogue_json_str = json.dumps(dialogue_data, ensure_ascii=False, indent=2)
        
        # 替换模板中的占位符
        full_prompt = self.prompt_template.replace(
            "{scenario_data_json_string}",
            scenario_json_str
        ).replace(
            "{dialogue_data_json_string}",
            dialogue_json_str
        )
        
        # 调用LLM
        response = self.api_client.call_llm(
            prompt=full_prompt,
            temperature=0.7,  # 较低温度以保证标注质量
            max_tokens=3000
        )
        
        if not response:
            return None
        
        # 解析JSON
        try:
            # 清理可能的markdown标记
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            if response.startswith("```"):
                response = response[3:]
            if response.endswith("```"):
                response = response[:-3]
            response = response.strip()
            
            label_data = json.loads(response)
            
            # 验证必需字段（检查三个任务：潜台词解码、氛围识别和KY测试）
            required_tasks = ["subtext_deciphering", "atmosphere_recognition", "ky_test"]
            if not all(task in label_data for task in required_tasks):
                print(f"❌ 标签数据缺少必需任务: {label_data}")
                return None
            
            # 验证每个任务的结构
            for task_name in required_tasks:
                task = label_data[task_name]
                if not all(key in task for key in ["question", "mcq_options", "correct_answer_index"]):
                    print(f"❌ 任务 {task_name} 格式错误")
                    return None
                
                # 验证选项数量(应该是6个)
                if len(task["mcq_options"]) != 6:
                    print(f"⚠️  任务 {task_name} 选项数量不是6个,实际为 {len(task['mcq_options'])}")
                
                # 验证correct_answer_index范围
                if not (0 <= task["correct_answer_index"] < len(task["mcq_options"])):
                    print(f"❌ 任务 {task_name} 的correct_answer_index超出范围")
                    return None
            
            return label_data
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON解析失败: {e}")
            print(f"原始响应: {response[:200]}...")
            return None
        except Exception as e:
            print(f"❌ 标签生成失败: {e}")
            return None


class LabelAnnotatorEN:
    """英文黄金标签标注器 - 生成三个评测任务的英文标准答案"""
    
    def __init__(self, api_client: OpenRouterClient):
        self.api_client = api_client
        
        # 加载英文提示词模板
        with open("prompt/get_prompt_for_labels_en.txt", "r", encoding="utf-8") as f:
            self.prompt_template = f.read()
    
    def generate(
        self, 
        scenario_data: Dict[str, Any], 
        dialogue_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        基于情境和对话生成英文评测标签
        
        Args:
            scenario_data: 情境设定数据
            dialogue_data: 对话数据
            
        Returns:
            评测标签的JSON对象,失败返回None
        """
        # 将数据转换为JSON字符串
        scenario_json_str = json.dumps(scenario_data, ensure_ascii=False, indent=2)
        dialogue_json_str = json.dumps(dialogue_data, ensure_ascii=False, indent=2)
        
        # 替换模板中的占位符
        full_prompt = self.prompt_template.replace(
            "{scenario_data_json_string}",
            scenario_json_str
        ).replace(
            "{dialogue_data_json_string}",
            dialogue_json_str
        )
        
        # 调用LLM
        response = self.api_client.call_llm(
            prompt=full_prompt,
            temperature=0.7,  # 较低温度以保证标注质量
            max_tokens=3000
        )
        
        if not response:
            return None
        
        # 解析JSON
        try:
            # 清理可能的markdown标记
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            if response.startswith("```"):
                response = response[3:]
            if response.endswith("```"):
                response = response[:-3]
            response = response.strip()
            
            label_data = json.loads(response)
            
            # 验证必需字段（检查三个任务：潜台词解码、氛围识别和KY测试）
            required_tasks = ["subtext_deciphering", "atmosphere_recognition", "ky_test"]
            if not all(task in label_data for task in required_tasks):
                print(f"❌ 标签数据缺少必需任务: {label_data}")
                return None
            
            # 验证每个任务的结构
            for task_name in required_tasks:
                task = label_data[task_name]
                if not all(key in task for key in ["question", "mcq_options", "correct_answer_index"]):
                    print(f"❌ 任务 {task_name} 格式错误")
                    return None
                
                # 验证选项数量(应该是6个)
                if len(task["mcq_options"]) != 6:
                    print(f"⚠️  任务 {task_name} 选项数量不是6个,实际为 {len(task['mcq_options'])}")
                
                # 验证correct_answer_index范围
                if not (0 <= task["correct_answer_index"] < len(task["mcq_options"])):
                    print(f"❌ 任务 {task_name} 的correct_answer_index超出范围")
                    return None
            
            return label_data
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON解析失败: {e}")
            print(f"原始响应: {response[:200]}...")
            return None
        except Exception as e:
            print(f"❌ 标签生成失败: {e}")
            return None


class LabelAnnotatorFR:
    """法语黄金标签标注器 - 生成三个评测任务的法语标准答案"""
    
    def __init__(self, api_client):
        self.api_client = api_client
        
        # 加载法语提示词模板
        with open("prompt/get_prompt_for_labels_fr.txt", "r", encoding="utf-8") as f:
            self.prompt_template = f.read()
    
    def generate(
        self, 
        scenario_data, 
        dialogue_data
    ):
        """
        基于情境和对话生成法语评测标签
        
        Args:
            scenario_data: 情境设定数据
            dialogue_data: 对话数据
            
        Returns:
            标签数据的JSON对象,失败返回None
        """
        import json
        
        # 将数据转换为JSON字符串
        scenario_json_str = json.dumps(scenario_data, ensure_ascii=False, indent=2)
        dialogue_json_str = json.dumps(dialogue_data, ensure_ascii=False, indent=2)
        
        # 替换模板中的占位符
        full_prompt = self.prompt_template.replace(
            "{scenario_data_json_string}",
            scenario_json_str
        ).replace(
            "{dialogue_data_json_string}",
            dialogue_json_str
        )
        
        # 调用LLM - 为GPT-5.1降低温度以提高JSON格式准确性
        temperature = 0.5 if hasattr(self.api_client, 'models') else 0.7  # AgentWorld用更低温度
        response = self.api_client.call_llm(
            prompt=full_prompt,
            temperature=temperature,
            max_tokens=2000
        )
        
        if not response:
            return None
        
        # 解析JSON
        try:
            # 清理可能的markdown标记
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            if response.startswith("```"):
                response = response[3:]
            if response.endswith("```"):
                response = response[:-3]
            response = response.strip()
            
            label_data = json.loads(response)
            
            # 验证必需字段
            required_tasks = ["subtext_deciphering", "atmosphere_recognition", "ky_test"]
            if not all(task in label_data for task in required_tasks):
                print(f"❌ 标签数据缺少必需任务")
                return None
            
            # 验证每个任务的结构
            for task_name in required_tasks:
                task = label_data[task_name]
                if not isinstance(task, dict):
                    print(f"❌ 任务 {task_name} 格式错误")
                    return None
                
                # 验证必需字段
                if "question" not in task or "mcq_options" not in task or "correct_answer_index" not in task:
                    print(f"❌ 任务 {task_name} 缺少必需字段")
                    return None
                
                # 验证选项数量
                if not isinstance(task["mcq_options"], list) or len(task["mcq_options"]) != 6:
                    print(f"❌ 任务 {task_name} 的选项数量不是6个")
                    return None
                
                # 验证答案索引
                if not isinstance(task["correct_answer_index"], int) or task["correct_answer_index"] not in range(6):
                    print(f"❌ 任务 {task_name} 的correct_answer_index超出范围")
                    return None
            
            return label_data
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON解析失败: {e}")
            print(f"原始响应: {response[:200]}...")
            return None
        except Exception as e:
            print(f"❌ 标签生成失败: {e}")
            return None


class LabelAnnotatorJP:
    """日语黄金标签标注器 - 生成三个评测任务的日语标准答案"""
    
    def __init__(self, api_client):
        self.api_client = api_client
        
        # 加载日语提示词模板
        with open("prompt/get_prompt_for_labels_jp.txt", "r", encoding="utf-8") as f:
            self.prompt_template = f.read()
    
    def generate(
        self, 
        scenario_data, 
        dialogue_data
    ):
        """
        基于情境和对话生成日语评测标签
        
        Args:
            scenario_data: 情境设定数据
            dialogue_data: 对话数据
            
        Returns:
            标签数据的JSON对象,失败返回None
        """
        import json
        
        # 将数据转换为JSON字符串
        scenario_json_str = json.dumps(scenario_data, ensure_ascii=False, indent=2)
        dialogue_json_str = json.dumps(dialogue_data, ensure_ascii=False, indent=2)
        
        # 替换模板中的占位符
        full_prompt = self.prompt_template.replace(
            "{scenario_data_json_string}",
            scenario_json_str
        ).replace(
            "{dialogue_data_json_string}",
            dialogue_json_str
        )
        
        # 调用LLM - 为GPT-5.1降低温度以提高JSON格式准确性
        temperature = 0.5 if hasattr(self.api_client, 'models') else 0.7  # AgentWorld用更低温度
        response = self.api_client.call_llm(
            prompt=full_prompt,
            temperature=temperature,
            max_tokens=2000
        )
        
        if not response:
            return None
        
        # 解析JSON
        try:
            # 清理可能的markdown标记
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            if response.startswith("```"):
                response = response[3:]
            if response.endswith("```"):
                response = response[:-3]
            response = response.strip()
            
            label_data = json.loads(response)
            
            # 验证必需字段
            required_tasks = ["subtext_deciphering", "atmosphere_recognition", "ky_test"]
            if not all(task in label_data for task in required_tasks):
                print(f"❌ 标签数据缺少必需任务")
                return None
            
            # 验证每个任务的结构
            for task_name in required_tasks:
                task = label_data[task_name]
                if not isinstance(task, dict):
                    print(f"❌ 任务 {task_name} 格式错误")
                    return None
                
                # 验证必需字段
                if "question" not in task or "mcq_options" not in task or "correct_answer_index" not in task:
                    print(f"❌ 任务 {task_name} 缺少必需字段")
                    return None
                
                # 验证选项数量
                if not isinstance(task["mcq_options"], list) or len(task["mcq_options"]) != 6:
                    print(f"❌ 任务 {task_name} 的选项数量不是6个")
                    return None
                
                # 验证答案索引
                if not isinstance(task["correct_answer_index"], int) or task["correct_answer_index"] not in range(6):
                    print(f"❌ 任务 {task_name} 的correct_answer_index超出范围")
                    return None
            
            return label_data
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON解析失败: {e}")
            print(f"原始响应: {response[:200]}...")
            return None
        except Exception as e:
            print(f"❌ 标签生成失败: {e}")
            return None


class LabelAnnotatorDE:
    """德语黄金标签标注器 - 生成三个评测任务的德语标准答案"""
    
    def __init__(self, api_client):
        self.api_client = api_client
        
        # 加载德语提示词模板
        with open("prompt/get_prompt_for_labels_de.txt", "r", encoding="utf-8") as f:
            self.prompt_template = f.read()
    
    def generate(
        self, 
        scenario_data, 
        dialogue_data
    ):
        """
        基于情境和对话生成德语评测标签
        
        Args:
            scenario_data: 情境设定数据
            dialogue_data: 对话数据
            
        Returns:
            标签数据的JSON对象,失败返回None
        """
        import json
        
        # 将数据转换为JSON字符串
        scenario_json_str = json.dumps(scenario_data, ensure_ascii=False, indent=2)
        dialogue_json_str = json.dumps(dialogue_data, ensure_ascii=False, indent=2)
        
        # 替换模板中的占位符
        full_prompt = self.prompt_template.replace(
            "{scenario_data_json_string}",
            scenario_json_str
        ).replace(
            "{dialogue_data_json_string}",
            dialogue_json_str
        )
        
        # 调用LLM - 为GPT-5.1降低温度以提高JSON格式准确性
        temperature = 0.5 if hasattr(self.api_client, 'models') else 0.7  # AgentWorld用更低温度
        response = self.api_client.call_llm(
            prompt=full_prompt,
            temperature=temperature,
            max_tokens=2000
        )
        
        if not response:
            return None
        
        # 解析JSON
        try:
            # 清理可能的markdown标记
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            if response.startswith("```"):
                response = response[3:]
            if response.endswith("```"):
                response = response[:-3]
            response = response.strip()
            
            label_data = json.loads(response)
            
            # 验证必需字段
            required_tasks = ["subtext_deciphering", "atmosphere_recognition", "ky_test"]
            if not all(task in label_data for task in required_tasks):
                print(f"❌ 标签数据缺少必需任务")
                return None
            
            # 验证每个任务的结构
            for task_name in required_tasks:
                task = label_data[task_name]
                if not isinstance(task, dict):
                    print(f"❌ 任务 {task_name} 格式错误")
                    return None
                
                # 验证必需字段
                if "question" not in task or "mcq_options" not in task or "correct_answer_index" not in task:
                    print(f"❌ 任务 {task_name} 缺少必需字段")
                    return None
                
                # 验证选项数量
                if not isinstance(task["mcq_options"], list) or len(task["mcq_options"]) != 6:
                    print(f"❌ 任务 {task_name} 的选项数量不是6个")
                    return None
                
                # 验证答案索引
                if not isinstance(task["correct_answer_index"], int) or task["correct_answer_index"] not in range(6):
                    print(f"❌ 任务 {task_name} 的correct_answer_index超出范围")
                    return None
            
            return label_data
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON解析失败: {e}")
            print(f"原始响应: {response[:200]}...")
            return None
        except Exception as e:
            print(f"❌ 标签生成失败: {e}")
            return None
