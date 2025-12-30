"""
对话仿真器 - 基于剧本设定生成多轮对话
"""
import json
from typing import Dict, Any, Optional
from api_client import OpenRouterClient


class DialogueSimulator:
    """对话仿真器"""
    
    def __init__(self, api_client: OpenRouterClient):
        self.api_client = api_client
        
        # 加载提示词模板
        with open("prompt/get_prompt_for_dialogue.txt", "r", encoding="utf-8") as f:
            self.prompt_template = f.read()
    
    def generate(self, scenario_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        基于情境设定生成对话
        
        Args:
            scenario_data: 情境设定数据
            
        Returns:
            对话数据的JSON对象,失败返回None
        """
        # 将scenario_data转换为JSON字符串
        scenario_json_str = json.dumps(scenario_data, ensure_ascii=False, indent=2)
        
        # 替换模板中的占位符
        full_prompt = self.prompt_template.replace(
            "{scenario_data_json_string}",
            scenario_json_str
        )
        
        # 调用LLM - 为GPT-5.1降低温度以提高JSON格式准确性
        temperature = 0.6 if hasattr(self.api_client, 'models') else 0.8  # AgentWorld用更低温度
        response = self.api_client.call_llm(
            prompt=full_prompt,
            temperature=temperature,
            max_tokens=1500
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
            
            dialogue_data = json.loads(response)
            
            # 验证必需字段
            required_fields = ["dialogue_transcript", "evaluation_trigger"]
            if not all(field in dialogue_data for field in required_fields):
                print(f"❌ 对话数据缺少必需字段: {dialogue_data}")
                return None
            
            # 验证dialogue_transcript结构
            if not isinstance(dialogue_data["dialogue_transcript"], list):
                print(f"❌ dialogue_transcript字段格式错误")
                return None
            
            # 验证evaluation_trigger结构
            trigger = dialogue_data["evaluation_trigger"]
            if "trigger_turn_id" not in trigger or "trigger_description" not in trigger:
                print(f"❌ evaluation_trigger字段格式错误")
                return None
            
            return dialogue_data
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON解析失败: {e}")
            print(f"原始响应前200字符: {response[:200]}...")
            print(f"原始响应后200字符: ...{response[-200:]}")
            
            # 尝试修复常见的JSON问题
            try:
                print("🔧 尝试修复JSON格式...")
                fixed_response = response.strip()
                
                # 1. 尝试简单的引号修复
                # 先尝试用单引号替换可能有问题的双引号
                lines = fixed_response.split('\n')
                fixed_lines = []
                
                for line in lines:
                    if '"line":' in line and line.count('"') > 4:  # 如果line字段包含额外的引号
                        # 找到line字段的值部分
                        if '"line": "' in line:
                            start = line.find('"line": "') + 9
                            end = line.rfind('"')
                            if end > start:
                                line_content = line[start:end]
                                # 转义内部的双引号
                                escaped_content = line_content.replace('"', '\\"')
                                line = line[:start] + escaped_content + line[end:]
                    fixed_lines.append(line)
                
                fixed_response = '\n'.join(fixed_lines)
                
                # 2. 移除可能的尾随逗号
                fixed_response = fixed_response.rstrip().rstrip(',')
                
                # 3. 确保JSON结构完整
                if not fixed_response.endswith('}'):
                    fixed_response += '}'
                
                dialogue_data = json.loads(fixed_response)
                print("✅ JSON修复成功")
                return dialogue_data
            except Exception as fix_error:
                print(f"❌ JSON修复失败: {fix_error}")
                return None
        except Exception as e:
            print(f"❌ 对话生成失败: {e}")
            return None


class DialogueSimulatorEN:
    """英文对话仿真器 - 基于剧本设定生成英文多轮对话"""
    
    def __init__(self, api_client: OpenRouterClient):
        self.api_client = api_client
        
        # 加载英文提示词模板
        with open("prompt/get_prompt_for_dialogue_en.txt", "r", encoding="utf-8") as f:
            self.prompt_template = f.read()
    
    def generate(self, scenario_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        基于情境设定生成英文对话
        
        Args:
            scenario_data: 情境设定数据
            
        Returns:
            对话数据的JSON对象,失败返回None
        """
        # 将scenario_data转换为JSON字符串
        scenario_json_str = json.dumps(scenario_data, ensure_ascii=False, indent=2)
        
        # 替换模板中的占位符
        full_prompt = self.prompt_template.replace(
            "{scenario_data_json_string}",
            scenario_json_str
        )
        
        # 调用LLM - 为GPT-5.1降低温度以提高JSON格式准确性
        temperature = 0.6 if hasattr(self.api_client, 'models') else 0.8  # AgentWorld用更低温度
        response = self.api_client.call_llm(
            prompt=full_prompt,
            temperature=temperature,
            max_tokens=1500
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
            
            dialogue_data = json.loads(response)
            
            # 验证必需字段
            required_fields = ["dialogue_transcript", "evaluation_trigger"]
            if not all(field in dialogue_data for field in required_fields):
                print(f"❌ 对话数据缺少必需字段: {dialogue_data}")
                return None
            
            # 验证dialogue_transcript结构
            if not isinstance(dialogue_data["dialogue_transcript"], list):
                print(f"❌ dialogue_transcript字段格式错误")
                return None
            
            # 验证evaluation_trigger结构
            trigger = dialogue_data["evaluation_trigger"]
            if "trigger_turn_id" not in trigger or "trigger_description" not in trigger:
                print(f"❌ evaluation_trigger字段格式错误")
                return None
            
            return dialogue_data
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON解析失败: {e}")
            print(f"原始响应前200字符: {response[:200]}...")
            print(f"原始响应后200字符: ...{response[-200:]}")
            
            # 尝试修复常见的JSON问题
            try:
                print("🔧 尝试修复JSON格式...")
                fixed_response = response.strip()
                
                # 1. 尝试简单的引号修复
                # 先尝试用单引号替换可能有问题的双引号
                lines = fixed_response.split('\n')
                fixed_lines = []
                
                for line in lines:
                    if '"line":' in line and line.count('"') > 4:  # 如果line字段包含额外的引号
                        # 找到line字段的值部分
                        if '"line": "' in line:
                            start = line.find('"line": "') + 9
                            end = line.rfind('"')
                            if end > start:
                                line_content = line[start:end]
                                # 转义内部的双引号
                                escaped_content = line_content.replace('"', '\\"')
                                line = line[:start] + escaped_content + line[end:]
                    fixed_lines.append(line)
                
                fixed_response = '\n'.join(fixed_lines)
                
                # 2. 移除可能的尾随逗号
                fixed_response = fixed_response.rstrip().rstrip(',')
                
                # 3. 确保JSON结构完整
                if not fixed_response.endswith('}'):
                    fixed_response += '}'
                
                dialogue_data = json.loads(fixed_response)
                print("✅ JSON修复成功")
                return dialogue_data
            except Exception as fix_error:
                print(f"❌ JSON修复失败: {fix_error}")
                return None
        except Exception as e:
            print(f"❌ 对话生成失败: {e}")
            return None


class DialogueSimulatorFR:
    """法语对话仿真器 - 基于剧本设定生成法语多轮对话"""
    
    def __init__(self, api_client):
        self.api_client = api_client
        
        # 加载法语提示词模板
        with open("prompt/get_prompt_for_dialogue_fr.txt", "r", encoding="utf-8") as f:
            self.prompt_template = f.read()
    
    def generate(self, scenario_data):
        """
        基于情境设定生成法语对话
        
        Args:
            scenario_data: 情境设定数据
            
        Returns:
            对话数据的JSON对象,失败返回None
        """
        import json
        
        # 将scenario_data转换为JSON字符串
        scenario_json_str = json.dumps(scenario_data, ensure_ascii=False, indent=2)
        
        # 替换模板中的占位符
        full_prompt = self.prompt_template.replace(
            "{scenario_data_json_string}",
            scenario_json_str
        )
        
        # 调用LLM - 为GPT-5.1降低温度以提高JSON格式准确性
        temperature = 0.6 if hasattr(self.api_client, 'models') else 0.8  # AgentWorld用更低温度
        response = self.api_client.call_llm(
            prompt=full_prompt,
            temperature=temperature,
            max_tokens=1500
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
            
            dialogue_data = json.loads(response)
            
            # 验证必需字段
            required_fields = ["dialogue_transcript", "evaluation_trigger"]
            if not all(field in dialogue_data for field in required_fields):
                print(f"❌ 对话数据缺少必需字段")
                return None
            
            # 验证dialogue_transcript结构
            if not isinstance(dialogue_data["dialogue_transcript"], list):
                print(f"❌ dialogue_transcript字段格式错误")
                return None
            
            # 验证evaluation_trigger结构
            trigger = dialogue_data.get("evaluation_trigger", {})
            if not isinstance(trigger, dict) or "trigger_turn_id" not in trigger:
                print(f"❌ evaluation_trigger字段格式错误")
                return None
            
            return dialogue_data
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON解析失败: {e}")
            print(f"原始响应前200字符: {response[:200]}...")
            
            # 尝试修复JSON
            try:
                print("🔧 尝试修复JSON格式...")
                fixed_response = response.strip()
                
                # 1. 修复对话内容中的引号问题
                lines = fixed_response.split('\n')
                fixed_lines = []
                for line in lines:
                    if '"line":' in line and line.count('"') > 4:
                        start = line.find('"line":') + 8
                        end = line.rfind('"')
                        if end > start:
                            content = line[start:end]
                            escaped_content = content.replace('"', '\\"')
                            line = line[:start] + escaped_content + line[end:]
                    fixed_lines.append(line)
                
                fixed_response = '\n'.join(fixed_lines)
                
                # 2. 移除可能的尾随逗号
                fixed_response = fixed_response.rstrip().rstrip(',')
                
                # 3. 确保JSON结构完整
                if not fixed_response.endswith('}'):
                    fixed_response += '}'
                
                dialogue_data = json.loads(fixed_response)
                print("✅ JSON修复成功")
                return dialogue_data
            except Exception as fix_error:
                print(f"❌ JSON修复失败: {fix_error}")
                return None
        except Exception as e:
            print(f"❌ 对话生成失败: {e}")
            return None


class DialogueSimulatorJP:
    """日语对话仿真器 - 基于剧本设定生成日语多轮对话"""
    
    def __init__(self, api_client):
        self.api_client = api_client
        
        # 加载日语提示词模板
        with open("prompt/get_prompt_for_dialogue_jp.txt", "r", encoding="utf-8") as f:
            self.prompt_template = f.read()
    
    def generate(self, scenario_data):
        """
        基于情境设定生成日语对话
        
        Args:
            scenario_data: 情境设定数据
            
        Returns:
            对话数据的JSON对象,失败返回None
        """
        import json
        
        # 将scenario_data转换为JSON字符串
        scenario_json_str = json.dumps(scenario_data, ensure_ascii=False, indent=2)
        
        # 替换模板中的占位符
        full_prompt = self.prompt_template.replace(
            "{scenario_data_json_string}",
            scenario_json_str
        )
        
        # 调用LLM - 为GPT-5.1降低温度以提高JSON格式准确性
        temperature = 0.6 if hasattr(self.api_client, 'models') else 0.8  # AgentWorld用更低温度
        response = self.api_client.call_llm(
            prompt=full_prompt,
            temperature=temperature,
            max_tokens=1500
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
            
            dialogue_data = json.loads(response)
            
            # 验证必需字段
            required_fields = ["dialogue_transcript", "evaluation_trigger"]
            if not all(field in dialogue_data for field in required_fields):
                print(f"❌ 对话数据缺少必需字段")
                return None
            
            # 验证dialogue_transcript结构
            if not isinstance(dialogue_data["dialogue_transcript"], list):
                print(f"❌ dialogue_transcript字段格式错误")
                return None
            
            # 验证evaluation_trigger结构
            trigger = dialogue_data.get("evaluation_trigger", {})
            if not isinstance(trigger, dict) or "trigger_turn_id" not in trigger:
                print(f"❌ evaluation_trigger字段格式错误")
                return None
            
            return dialogue_data
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON解析失败: {e}")
            print(f"原始响应前200字符: {response[:200]}...")
            
            # 尝试修复JSON
            try:
                print("🔧 尝试修复JSON格式...")
                fixed_response = response.strip()
                
                # 1. 修复对话内容中的引号问题
                lines = fixed_response.split('\n')
                fixed_lines = []
                for line in lines:
                    if '"line":' in line and line.count('"') > 4:
                        start = line.find('"line":') + 8
                        end = line.rfind('"')
                        if end > start:
                            content = line[start:end]
                            escaped_content = content.replace('"', '\\"')
                            line = line[:start] + escaped_content + line[end:]
                    fixed_lines.append(line)
                
                fixed_response = '\n'.join(fixed_lines)
                
                # 2. 移除可能的尾随逗号
                fixed_response = fixed_response.rstrip().rstrip(',')
                
                # 3. 确保JSON结构完整
                if not fixed_response.endswith('}'):
                    fixed_response += '}'
                
                dialogue_data = json.loads(fixed_response)
                print("✅ JSON修复成功")
                return dialogue_data
            except Exception as fix_error:
                print(f"❌ JSON修复失败: {fix_error}")
                return None
        except Exception as e:
            print(f"❌ 对话生成失败: {e}")
            return None


class DialogueSimulatorDE:
    """德语对话仿真器 - 基于剧本设定生成德语多轮对话"""
    
    def __init__(self, api_client):
        self.api_client = api_client
        
        # 加载德语提示词模板
        with open("prompt/get_prompt_for_dialogue_de.txt", "r", encoding="utf-8") as f:
            self.prompt_template = f.read()
    
    def generate(self, scenario_data):
        """
        基于情境设定生成德语对话
        
        Args:
            scenario_data: 情境设定数据
            
        Returns:
            对话数据的JSON对象,失败返回None
        """
        import json
        
        # 将scenario_data转换为JSON字符串
        scenario_json_str = json.dumps(scenario_data, ensure_ascii=False, indent=2)
        
        # 替换模板中的占位符
        full_prompt = self.prompt_template.replace(
            "{scenario_data_json_string}",
            scenario_json_str
        )
        
        # 调用LLM - 为GPT-5.1降低温度以提高JSON格式准确性
        temperature = 0.6 if hasattr(self.api_client, 'models') else 0.8  # AgentWorld用更低温度
        response = self.api_client.call_llm(
            prompt=full_prompt,
            temperature=temperature,
            max_tokens=1500
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
            
            dialogue_data = json.loads(response)
            
            # 验证必需字段
            required_fields = ["dialogue_transcript", "evaluation_trigger"]
            if not all(field in dialogue_data for field in required_fields):
                print(f"❌ 对话数据缺少必需字段")
                return None
            
            # 验证dialogue_transcript结构
            if not isinstance(dialogue_data["dialogue_transcript"], list):
                print(f"❌ dialogue_transcript字段格式错误")
                return None
            
            # 验证evaluation_trigger结构
            trigger = dialogue_data.get("evaluation_trigger", {})
            if not isinstance(trigger, dict) or "trigger_turn_id" not in trigger:
                print(f"❌ evaluation_trigger字段格式错误")
                return None
            
            return dialogue_data
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON解析失败: {e}")
            print(f"原始响应前200字符: {response[:200]}...")
            
            # 尝试修复JSON
            try:
                print("🔧 尝试修复JSON格式...")
                fixed_response = response.strip()
                
                # 1. 修复对话内容中的引号问题
                lines = fixed_response.split('\n')
                fixed_lines = []
                for line in lines:
                    if '"line":' in line and line.count('"') > 4:
                        start = line.find('"line":') + 8
                        end = line.rfind('"')
                        if end > start:
                            content = line[start:end]
                            escaped_content = content.replace('"', '\\"')
                            line = line[:start] + escaped_content + line[end:]
                    fixed_lines.append(line)
                
                fixed_response = '\n'.join(fixed_lines)
                
                # 2. 移除可能的尾随逗号
                fixed_response = fixed_response.rstrip().rstrip(',')
                
                # 3. 确保JSON结构完整
                if not fixed_response.endswith('}'):
                    fixed_response += '}'
                
                dialogue_data = json.loads(fixed_response)
                print("✅ JSON修复成功")
                return dialogue_data
            except Exception as fix_error:
                print(f"❌ JSON修复失败: {fix_error}")
                return None
        except Exception as e:
            print(f"❌ 对话生成失败: {e}")
            return None
