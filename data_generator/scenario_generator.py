"""
情境生成器 - 生成对话的剧本设定
"""
import json
from typing import Dict, Any, Optional
from api_client import OpenRouterClient
from scenario_seeds import get_seed_by_index


class ScenarioGenerator:
    """情境生成器"""
    
    def __init__(self, api_client: OpenRouterClient, use_seeds: bool = True):
        self.api_client = api_client
        self.use_seeds = use_seeds  # 是否使用场景种子库
        
        # 加载提示词模板
        with open("prompt/get_prompt_for_scenario.txt", "r", encoding="utf-8") as f:
            self.prompt_template = f.read()
    
    def generate(self, theme: str = None, seed_index: int = None, atmosphere: str = None) -> Optional[Dict[str, Any]]:
        """
        生成一个情境设定
        
        Args:
            theme: 主题(可选),如果不提供则让LLM自由发挥
            seed_index: 场景种子索引(可选),用于按顺序使用种子
            atmosphere: 指定的氛围(可选),明确要求LLM使用该氛围
            
        Returns:
            情境设定的JSON对象,失败返回None
        """
        # 初始化category变量
        seed_category = None
        
        # 构建完整提示词
        if theme:
            # 如果指定了主题，使用指定主题
            full_prompt = f"{self.prompt_template}\n\n请基于以下主题创作:\n主题: {theme}"
        elif self.use_seeds and seed_index is not None:
            # 使用指定索引的场景种子
            seed = get_seed_by_index(seed_index)
            if seed:
                scene = seed['scene']
                seed_category = seed.get('category', None)  # 获取category字段
                # 如果指定了氛围，明确告诉LLM
                if atmosphere:
                    full_prompt = f"{self.prompt_template}\n\n请基于以下场景和氛围创作，充分扩展和深化，确保对话中体现出该氛围：\n场景: {scene}\n氛围: {atmosphere}"
                else:
                    full_prompt = f"{self.prompt_template}\n\n请基于以下场景方向创作，充分扩展和深化:\n场景: {scene}"
            else:
                # 如果获取种子失败，使用完全自由创作
                full_prompt = self.prompt_template
                seed_category = None
        else:
            # 完全自由创作
            full_prompt = self.prompt_template
        
        # 调用LLM
        response = self.api_client.call_llm(
            prompt=full_prompt,
            temperature=0.9,  # 高温度以增加创意
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
            
            scenario_data = json.loads(response)
            
            # 验证必需字段
            required_fields = ["scenario_description", "personas", "hidden_collective_intent"]
            if not all(field in scenario_data for field in required_fields):
                print(f"❌ 情境数据缺少必需字段: {scenario_data}")
                return None
            
            # 验证personas结构
            if not isinstance(scenario_data["personas"], list) or len(scenario_data["personas"]) < 3:
                print(f"❌ personas字段格式错误或角色数量不足")
                return None
            
            # 添加category字段（如果从seed中获取到）
            if seed_category:
                scenario_data["category"] = seed_category
            
            return scenario_data
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON解析失败: {e}")
            print(f"原始响应前200字符: {response[:200]}...")
            print(f"原始响应后200字符: ...{response[-200:]}")
            
            # 尝试修复JSON
            try:
                print("🔧 尝试修复JSON格式...")
                fixed_response = response.strip()
                
                # 修复可能的引号问题
                lines = fixed_response.split('\n')
                fixed_lines = []
                
                for line in lines:
                    # 修复各种字段中的引号问题
                    for field in ['"scenario_description":', '"public_goal":', '"private_motive":', '"hidden_collective_intent":']:
                        if field in line and line.count('"') > 4:
                            start = line.find(field) + len(field) + 2
                            end = line.rfind('"')
                            if end > start:
                                content = line[start:end]
                                escaped_content = content.replace('"', '\\"')
                                line = line[:start] + escaped_content + line[end:]
                    fixed_lines.append(line)
                
                fixed_response = '\n'.join(fixed_lines)
                
                # 移除尾随逗号
                fixed_response = fixed_response.rstrip().rstrip(',')
                if not fixed_response.endswith('}'):
                    fixed_response += '}'
                
                scenario_data = json.loads(fixed_response)
                print("✅ JSON修复成功")
                
                # 验证必需字段
                required_fields = ["scenario_description", "personas", "hidden_collective_intent"]
                if not all(field in scenario_data for field in required_fields):
                    print(f"❌ 修复后数据仍缺少必需字段")
                    return None
                
                return scenario_data
            except Exception as fix_error:
                print(f"❌ JSON修复失败: {fix_error}")
                return None
        
        except Exception as e:
            print(f"❌ 情境生成失败: {e}")
            return None


class ScenarioGeneratorEN:
    """英文情境生成器 - 生成英文对话的剧本设定"""
    
    def __init__(self, api_client: OpenRouterClient, use_seeds: bool = True):
        self.api_client = api_client
        self.use_seeds = use_seeds  # 是否使用场景种子库
        
        # 加载英文提示词模板
        with open("prompt/get_prompt_for_scenario_en.txt", "r", encoding="utf-8") as f:
            self.prompt_template = f.read()
    
    def generate(self, theme: str = None, seed_index: int = None, atmosphere: str = None) -> Optional[Dict[str, Any]]:
        """
        生成一个英文情境设定
        
        Args:
            theme: 主题(可选),如果不提供则让LLM自由发挥
            seed_index: 场景种子索引(可选),用于按顺序使用种子
            atmosphere: 指定的氛围(可选),明确要求LLM使用该氛围
            
        Returns:
            情境设定的JSON对象,失败返回None
        """
        # 导入英文种子
        from scenario_seeds_en import get_seed_by_index as get_seed_by_index_en
        
        # 初始化category变量
        seed_category = None
        
        # 构建完整提示词
        if theme:
            # 如果指定了主题，使用指定主题
            full_prompt = f"{self.prompt_template}\n\nPlease create based on the following theme:\nTheme: {theme}"
        elif self.use_seeds and seed_index is not None:
            # 使用指定索引的场景种子
            seed = get_seed_by_index_en(seed_index)
            if seed:
                scene = seed["scene"]
                seed_category = seed.get('category', None)  # 获取category字段
                # 如果指定了氛围，明确告诉LLM
                if atmosphere:
                    full_prompt = f"{self.prompt_template}\n\nPlease create based on the following scenario and atmosphere, fully expand and deepen, ensuring the dialogue reflects this atmosphere:\nScenario: {scene}\nAtmosphere: {atmosphere}"
                else:
                    full_prompt = f"{self.prompt_template}\n\nPlease create based on the following scenario direction, fully expand and deepen:\nScenario: {scene}"
            else:
                # 如果获取种子失败，使用完全自由创作
                full_prompt = self.prompt_template
                seed_category = None
        else:
            # 完全自由创作
            full_prompt = self.prompt_template
        
        # 调用LLM
        response = self.api_client.call_llm(
            prompt=full_prompt,
            temperature=0.9,  # 高温度以增加创意
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
            
            scenario_data = json.loads(response)
            
            # 验证必需字段
            required_fields = ["scenario_description", "personas", "hidden_collective_intent"]
            if not all(field in scenario_data for field in required_fields):
                print(f"❌ 情境数据缺少必需字段: {scenario_data}")
                return None
            
            # 验证personas结构
            if not isinstance(scenario_data["personas"], list) or len(scenario_data["personas"]) < 3:
                print(f"❌ personas字段格式错误或角色数量不足")
                return None
            
            # 添加category字段（如果从seed中获取到）
            if seed_category:
                scenario_data["category"] = seed_category
            
            return scenario_data
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON解析失败: {e}")
            print(f"原始响应前200字符: {response[:200]}...")
            print(f"原始响应后200字符: ...{response[-200:]}")
            
            # 尝试修复JSON
            try:
                print("🔧 尝试修复JSON格式...")
                fixed_response = response.strip()
                
                # 修复可能的引号问题
                lines = fixed_response.split('\n')
                fixed_lines = []
                
                for line in lines:
                    # 修复各种字段中的引号问题
                    for field in ['"scenario_description":', '"public_goal":', '"private_motive":', '"hidden_collective_intent":']:
                        if field in line and line.count('"') > 4:
                            start = line.find(field) + len(field) + 2
                            end = line.rfind('"')
                            if end > start:
                                content = line[start:end]
                                escaped_content = content.replace('"', '\\"')
                                line = line[:start] + escaped_content + line[end:]
                    fixed_lines.append(line)
                
                fixed_response = '\n'.join(fixed_lines)
                
                # 移除尾随逗号
                fixed_response = fixed_response.rstrip().rstrip(',')
                if not fixed_response.endswith('}'):
                    fixed_response += '}'
                
                scenario_data = json.loads(fixed_response)
                print("✅ JSON修复成功")
                
                # 验证必需字段
                required_fields = ["scenario_description", "personas", "hidden_collective_intent"]
                if not all(field in scenario_data for field in required_fields):
                    print(f"❌ 修复后数据仍缺少必需字段")
                    return None
                
                return scenario_data
            except Exception as fix_error:
                print(f"❌ JSON修复失败: {fix_error}")
                return None
        
        except Exception as e:
            print(f"❌ 情境生成失败: {e}")
            return None


class ScenarioGeneratorFR:
    """法语情境生成器 - 生成法语对话的剧本设定"""
    
    def __init__(self, api_client, use_seeds: bool = True):
        self.api_client = api_client
        self.use_seeds = use_seeds  # 是否使用场景种子库
        
        # 加载法语提示词模板
        with open("prompt/get_prompt_for_scenario_fr.txt", "r", encoding="utf-8") as f:
            self.prompt_template = f.read()
    
    def generate(self, theme: str = None, seed_index: int = None, atmosphere: str = None):
        """
        生成一个法语情境设定
        
        Args:
            theme: 主题(可选),如果不提供则让LLM自由发挥
            seed_index: 场景种子索引(可选),用于按顺序使用种子
            atmosphere: 指定的氛围(可选),明确要求LLM使用该氛围
            
        Returns:
            情境设定的JSON对象,失败返回None
        """
        # 导入法语种子
        from scenario_seeds_fr import get_seed_by_index as get_seed_by_index_fr
        import json
        
        # 初始化category变量
        seed_category = None
        
        # 构建完整提示词
        if theme:
            # 如果指定了主题，使用指定主题
            full_prompt = f"{self.prompt_template}\n\nVeuillez créer en fonction du thème suivant:\nThème: {theme}"
        elif self.use_seeds and seed_index is not None:
            # 使用指定索引的场景种子
            seed = get_seed_by_index_fr(seed_index)
            if seed:
                scene = seed["scene"]
                seed_category = seed.get('category', None)  # 获取category字段
                # 如果指定了氛围，明确告诉LLM
                if atmosphere:
                    full_prompt = f"{self.prompt_template}\n\nVeuillez créer en fonction du scénario et de l'atmosphère suivants, en développant et en approfondissant pleinement, en vous assurant que le dialogue reflète cette atmosphère:\nScénario: {scene}\nAtmosphère: {atmosphere}"
                else:
                    full_prompt = f"{self.prompt_template}\n\nVeuillez créer en fonction de la direction de scénario suivante, en développant et en approfondissant pleinement:\nScénario: {scene}"
            else:
                # 如果获取种子失败，使用完全自由创作
                full_prompt = self.prompt_template
                seed_category = None
        else:
            # 完全自由创作
            full_prompt = self.prompt_template
        
        # 调用LLM
        response = self.api_client.call_llm(
            prompt=full_prompt,
            temperature=0.9,  # 高温度以增加创意
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
            
            scenario_data = json.loads(response)
            
            # 验证必需字段
            required_fields = ["scenario_description", "personas", "hidden_collective_intent"]
            if not all(field in scenario_data for field in required_fields):
                print(f"❌ 情境数据缺少必需字段: {scenario_data}")
                return None
            
            # 验证personas结构
            if not isinstance(scenario_data["personas"], list) or len(scenario_data["personas"]) < 3:
                print(f"❌ personas字段格式错误或角色数量不足")
                return None
            
            # 添加category字段（如果从seed中获取到）
            if seed_category:
                scenario_data["category"] = seed_category
            
            return scenario_data
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON解析失败: {e}")
            print(f"原始响应前200字符: {response[:200]}...")
            print(f"原始响应后200字符: ...{response[-200:]}")
            
            # 尝试修复JSON
            try:
                print("🔧 尝试修复JSON格式...")
                fixed_response = response.strip()
                
                # 修复可能的引号问题
                lines = fixed_response.split('\n')
                fixed_lines = []
                
                for line in lines:
                    # 修复各种字段中的引号问题
                    for field in ['"scenario_description":', '"public_goal":', '"private_motive":', '"hidden_collective_intent":']:
                        if field in line and line.count('"') > 4:
                            start = line.find(field) + len(field) + 2
                            end = line.rfind('"')
                            if end > start:
                                content = line[start:end]
                                escaped_content = content.replace('"', '\\"')
                                line = line[:start] + escaped_content + line[end:]
                    fixed_lines.append(line)
                
                fixed_response = '\n'.join(fixed_lines)
                
                # 移除尾随逗号
                fixed_response = fixed_response.rstrip().rstrip(',')
                if not fixed_response.endswith('}'):
                    fixed_response += '}'
                
                scenario_data = json.loads(fixed_response)
                print("✅ JSON修复成功")
                
                # 验证必需字段
                required_fields = ["scenario_description", "personas", "hidden_collective_intent"]
                if not all(field in scenario_data for field in required_fields):
                    print(f"❌ 修复后数据仍缺少必需字段")
                    return None
                
                return scenario_data
            except Exception as fix_error:
                print(f"❌ JSON修复失败: {fix_error}")
                return None
        
        except Exception as e:
            print(f"❌ 情境生成失败: {e}")
            return None


class ScenarioGeneratorJP:
    """日语情境生成器 - 生成日语对话的剧本设定"""
    
    def __init__(self, api_client, use_seeds: bool = True):
        self.api_client = api_client
        self.use_seeds = use_seeds  # 是否使用场景种子库
        
        # 加载日语提示词模板
        with open("prompt/get_prompt_for_scenario_jp.txt", "r", encoding="utf-8") as f:
            self.prompt_template = f.read()
    
    def generate(self, theme: str = None, seed_index: int = None, atmosphere: str = None):
        """
        生成一个日语情境设定
        
        Args:
            theme: 主题(可选),如果不提供则让LLM自由发挥
            seed_index: 场景种子索引(可选),用于按顺序使用种子
            atmosphere: 指定的氛围(可选),明确要求LLM使用该氛围
            
        Returns:
            情境设定的JSON对象,失败返回None
        """
        # 导入日语种子
        from scenario_seeds_jp import get_seed_by_index as get_seed_by_index_jp
        import json
        
        # 初始化category变量
        seed_category = None
        
        # 构建完整提示词
        if theme:
            # 如果指定了主题，使用指定主题
            full_prompt = f"{self.prompt_template}\n\n以下のテーマに基づいて作成してください:\nテーマ: {theme}"
        elif self.use_seeds and seed_index is not None:
            # 使用指定索引的场景种子
            seed = get_seed_by_index_jp(seed_index)
            if seed:
                scene = seed["scene"]
                seed_category = seed.get('category', None)  # 获取category字段
                # 如果指定了氛围，明确告诉LLM
                if atmosphere:
                    full_prompt = f"{self.prompt_template}\n\n以下のシナリオと雰囲気に基づいて作成し、完全に展開して深化させ、対話がこの雰囲気を反映するようにしてください:\nシナリオ: {scene}\n雰囲気: {atmosphere}"
                else:
                    full_prompt = f"{self.prompt_template}\n\n以下のシナリオの方向性に基づいて作成し、完全に展開して深化させてください:\nシナリオ: {scene}"
            else:
                # 如果获取种子失败，使用完全自由创作
                full_prompt = self.prompt_template
                seed_category = None
        else:
            # 完全自由创作
            full_prompt = self.prompt_template
        
        # 调用LLM
        response = self.api_client.call_llm(
            prompt=full_prompt,
            temperature=0.9,  # 高温度以增加创意
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
            
            scenario_data = json.loads(response)
            
            # 验证必需字段
            required_fields = ["scenario_description", "personas", "hidden_collective_intent"]
            if not all(field in scenario_data for field in required_fields):
                print(f"❌ 情境数据缺少必需字段: {scenario_data}")
                return None
            
            # 验证personas结构
            if not isinstance(scenario_data["personas"], list) or len(scenario_data["personas"]) < 3:
                print(f"❌ personas字段格式错误或角色数量不足")
                return None
            
            # 添加category字段（如果从seed中获取到）
            if seed_category:
                scenario_data["category"] = seed_category
            
            return scenario_data
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON解析失败: {e}")
            print(f"原始响应前200字符: {response[:200]}...")
            print(f"原始响应后200字符: ...{response[-200:]}")
            
            # 尝试修复JSON
            try:
                print("🔧 尝试修复JSON格式...")
                fixed_response = response.strip()
                
                # 修复可能的引号问题
                lines = fixed_response.split('\n')
                fixed_lines = []
                
                for line in lines:
                    # 修复各种字段中的引号问题
                    for field in ['"scenario_description":', '"public_goal":', '"private_motive":', '"hidden_collective_intent":']:
                        if field in line and line.count('"') > 4:
                            start = line.find(field) + len(field) + 2
                            end = line.rfind('"')
                            if end > start:
                                content = line[start:end]
                                escaped_content = content.replace('"', '\\"')
                                line = line[:start] + escaped_content + line[end:]
                    fixed_lines.append(line)
                
                fixed_response = '\n'.join(fixed_lines)
                
                # 移除尾随逗号
                fixed_response = fixed_response.rstrip().rstrip(',')
                if not fixed_response.endswith('}'):
                    fixed_response += '}'
                
                scenario_data = json.loads(fixed_response)
                print("✅ JSON修复成功")
                
                # 验证必需字段
                required_fields = ["scenario_description", "personas", "hidden_collective_intent"]
                if not all(field in scenario_data for field in required_fields):
                    print(f"❌ 修复后数据仍缺少必需字段")
                    return None
                
                return scenario_data
            except Exception as fix_error:
                print(f"❌ JSON修复失败: {fix_error}")
                return None
        
        except Exception as e:
            print(f"❌ 情境生成失败: {e}")
            return None


class ScenarioGeneratorDE:
    """德语情境生成器 - 生成德语对话的剧本设定"""
    
    def __init__(self, api_client, use_seeds: bool = True):
        self.api_client = api_client
        self.use_seeds = use_seeds  # 是否使用场景种子库
        
        # 加载德语提示词模板
        with open("prompt/get_prompt_for_scenario_de.txt", "r", encoding="utf-8") as f:
            self.prompt_template = f.read()
    
    def generate(self, theme: str = None, seed_index: int = None, atmosphere: str = None):
        """
        生成一个德语情境设定
        
        Args:
            theme: 主题(可选),如果不提供则让LLM自由发挥
            seed_index: 场景种子索引(可选),用于按顺序使用种子
            atmosphere: 指定的氛围(可选),明确要求LLM使用该氛围
            
        Returns:
            情境设定的JSON对象,失败返回None
        """
        # 导入德语种子
        from scenario_seeds_de import get_seed_by_index as get_seed_by_index_de
        import json
        
        # 初始化category变量
        seed_category = None
        
        # 构建完整提示词
        if theme:
            # 如果指定了主题，使用指定主题
            full_prompt = f"{self.prompt_template}\n\nBitte erstellen Sie basierend auf folgendem Thema:\nThema: {theme}"
        elif self.use_seeds and seed_index is not None:
            # 使用指定索引的场景种子
            seed = get_seed_by_index_de(seed_index)
            if seed:
                scene = seed["scene"]
                seed_category = seed.get('category', None)  # 获取category字段
                # 如果指定了氛围，明确告诉LLM
                if atmosphere:
                    full_prompt = f"{self.prompt_template}\n\nBitte erstellen Sie basierend auf folgendem Szenario und Atmosphäre, entfalten und vertiefen Sie es vollständig und lassen Sie den Dialog diese Atmosphäre widerspiegeln:\nSzenario: {scene}\nAtmosphäre: {atmosphere}"
                else:
                    full_prompt = f"{self.prompt_template}\n\nBitte erstellen Sie basierend auf folgender Szenariorichtung, entfalten und vertiefen Sie es vollständig:\nSzenario: {scene}"
            else:
                # 如果获取种子失败，使用完全自由创作
                full_prompt = self.prompt_template
                seed_category = None
        else:
            # 完全自由创作
            full_prompt = self.prompt_template
        
        # 调用LLM
        response = self.api_client.call_llm(
            prompt=full_prompt,
            temperature=0.9,  # 高温度以增加创意
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
            
            scenario_data = json.loads(response)
            
            # 验证必需字段
            required_fields = ["scenario_description", "personas", "hidden_collective_intent"]
            if not all(field in scenario_data for field in required_fields):
                print(f"❌ 情境数据缺少必需字段: {scenario_data}")
                return None
            
            # 验证personas结构
            if not isinstance(scenario_data["personas"], list) or len(scenario_data["personas"]) < 3:
                print(f"❌ personas字段格式错误或角色数量不足")
                return None
            
            # 添加category字段（如果从seed中获取到）
            if seed_category:
                scenario_data["category"] = seed_category
            
            return scenario_data
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON解析失败: {e}")
            print(f"原始响应前200字符: {response[:200]}...")
            print(f"原始响应后200字符: ...{response[-200:]}")
            
            # 尝试修复JSON
            try:
                print("🔧 尝试修复JSON格式...")
                fixed_response = response.strip()
                
                # 修复可能的引号问题
                lines = fixed_response.split('\n')
                fixed_lines = []
                
                for line in lines:
                    # 修复各种字段中的引号问题
                    for field in ['"scenario_description":', '"public_goal":', '"private_motive":', '"hidden_collective_intent":']:
                        if field in line and line.count('"') > 4:
                            start = line.find(field) + len(field) + 2
                            end = line.rfind('"')
                            if end > start:
                                content = line[start:end]
                                escaped_content = content.replace('"', '\\"')
                                line = line[:start] + escaped_content + line[end:]
                    fixed_lines.append(line)
                
                fixed_response = '\n'.join(fixed_lines)
                
                # 移除尾随逗号
                fixed_response = fixed_response.rstrip().rstrip(',')
                if not fixed_response.endswith('}'):
                    fixed_response += '}'
                
                scenario_data = json.loads(fixed_response)
                print("✅ JSON修复成功")
                
                # 验证必需字段
                required_fields = ["scenario_description", "personas", "hidden_collective_intent"]
                if not all(field in scenario_data for field in required_fields):
                    print(f"❌ 修复后数据仍缺少必需字段")
                    return None
                
                return scenario_data
            except Exception as fix_error:
                print(f"❌ JSON修复失败: {fix_error}")
                return None
        
        except Exception as e:
            print(f"❌ 情境生成失败: {e}")
            return None
