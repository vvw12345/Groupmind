"""
多平台 API 客户端 - 支持OpenRouter、硅基流动和AgentWorld GPT-5.1
"""
import requests
import json
import time
from typing import Dict, Any, Optional
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from config import OPENROUTER_CONFIG, SILICONFLOW_CONFIG

# AgentWorld 配置
AGENTWORLD_CONFIG = {
    "base_url": "https://api.agentworld.top/v1/chat/completions",
    "model_api_mapping": {
        "gpt-5.1": "sk-x2hu5rCsRJ0gLSvTsfZ0ezPI1e80lEljTlnoXXcWACWu9Bci",
        "gemini-2.5-pro": "sk-qUPoKXMSka3Djbu89JeGAA9hOWiCDjoGOi8MhQpQwDYm3EnI",
        "claude-sonnet-4-20250514": "sk-ayWSyh7TnGiNlxW1OwjHgpLbNfgbJ5BsY9URx463avBx69rY",
        "gpt-4.1-mini": "sk-x2hu5rCsRJ0gLSvTsfZ0ezPI1e80lEljTlnoXXcWACWu9Bci",
        "grok-4.1": "sk-vC3CvfIwzM0TMAv3r9yIAnl2g9vZawh2nJBwSef5MgnNZ1cI"
    },
    "models": ["gpt-5.1", "gemini-2.5-pro", "claude-sonnet-4-20250514", "gpt-4.1-mini", "grok-4.1"]
}


class OpenRouterClient:
    """多平台API客户端,支持硅基流动和OpenRouter"""
    
    def __init__(self):
        # 优先使用硅基流动(付费稳定)
        self.use_siliconflow = True
        
        # 硅基流动配置
        self.sf_api_keys = SILICONFLOW_CONFIG["api_keys"]
        self.sf_models = SILICONFLOW_CONFIG["models"]
        self.sf_base_url = SILICONFLOW_CONFIG["base_url"]
        
        # OpenRouter配置(备用)
        self.or_api_keys = OPENROUTER_CONFIG["api_keys"]
        self.or_models = OPENROUTER_CONFIG["models"]
        self.or_base_url = OPENROUTER_CONFIG["base_url"]
        
        # 当前使用的索引
        self.current_key_index = 0
        self.current_model_index = 0
        
        # 统计信息
        self.stats = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "key_switches": 0,
            "model_switches": 0
        }
    
    def _get_current_key(self) -> str:
        """获取当前API密钥"""
        if self.use_siliconflow:
            return self.sf_api_keys[self.current_key_index]
        else:
            return self.or_api_keys[self.current_key_index]
    
    def _get_current_model(self) -> str:
        """获取当前模型"""
        if self.use_siliconflow:
            return self.sf_models[self.current_model_index]
        else:
            return self.or_models[self.current_model_index]
    
    def _get_current_base_url(self) -> str:
        """获取当前API基础URL"""
        if self.use_siliconflow:
            return self.sf_base_url
        else:
            return self.or_base_url
    
    def _switch_key(self):
        """切换到下一个API密钥"""
        if self.use_siliconflow:
            api_keys = self.sf_api_keys
            platform = "硅基流动"
        else:
            api_keys = self.or_api_keys
            platform = "OpenRouter"
            
        self.current_key_index = (self.current_key_index + 1) % len(api_keys)
        self.stats["key_switches"] += 1
        print(f"⚠️  切换{platform}API密钥 -> 密钥 #{self.current_key_index + 1}")
    
    def _switch_platform(self):
        """切换平台(从硅基流动切换到OpenRouter)"""
        if self.use_siliconflow:
            self.use_siliconflow = False
            self.current_key_index = 0
            self.current_model_index = 0
            print(f"🔄 切换到OpenRouter平台")
        else:
            print(f"⚠️  已经在使用OpenRouter平台")
    
    def _switch_model(self):
        """切换到下一个模型"""
        old_model = self._get_current_model()
        if self.use_siliconflow:
            models = self.sf_models
        else:
            models = self.or_models
            
        self.current_model_index = (self.current_model_index + 1) % len(models)
        new_model = self._get_current_model()
        self.stats["model_switches"] += 1
        print(f"⚠️  切换模型: {old_model} -> {new_model}")
    
    def call_llm(
        self, 
        prompt: str, 
        max_retries: int = 50,
        temperature: float = 0.8,
        max_tokens: int = 4000
    ) -> Optional[str]:
        """
        调用LLM API,支持自动重试和切换
        
        Args:
            prompt: 提示词
            max_retries: 最大重试次数
            temperature: 温度参数
            max_tokens: 最大token数
            
        Returns:
            生成的文本,失败返回None
        """
        self.stats["total_requests"] += 1
        
        for attempt in range(max_retries):
            try:
                headers = {
                    "Authorization": f"Bearer {self._get_current_key()}",
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "model": self._get_current_model(),
                    "messages": [
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": temperature,
                    "max_tokens": max_tokens
                }
                
                response = requests.post(
                    self._get_current_base_url(),
                    headers=headers,
                    json=payload,
                    timeout=60
                )
                
                # 检查响应状态
                if response.status_code == 200:
                    result = response.json()
                    content = result["choices"][0]["message"]["content"]
                    self.stats["successful_requests"] += 1
                    return content
                
                # 处理限流错误 (429)
                elif response.status_code == 429:
                    error_data = response.json()
                    error_msg = error_data.get("error", {}).get("message", "")
                    
                    # 如果是硅基流动且已经尝试过所有密钥,切换到OpenRouter
                    if self.use_siliconflow and self.current_key_index >= len(self.sf_api_keys) - 1:
                        print(f"⚠️  硅基流动密钥已用完,切换到OpenRouter...")
                        self._switch_platform()
                    else:
                        # 遇到限流直接切换API密钥
                        print(f"⏳ 遇到限流(429),切换API密钥... (尝试 {attempt + 1}/{max_retries})")
                        self._switch_key()
                    
                    time.sleep(0.5)  # 短暂等待
                
                # 处理认证错误 (401) - 无效密钥,快速切换
                elif response.status_code == 401:
                    print(f"⚠️  密钥 #{self.current_key_index + 1} 无效(401),切换...")
                    # 如果是硅基流动且已经尝试过所有密钥,切换到OpenRouter
                    if self.use_siliconflow and self.current_key_index >= len(self.sf_api_keys) - 1:
                        print(f"⚠️  硅基流动密钥已用完,切换到OpenRouter...")
                        self._switch_platform()
                    else:
                        self._switch_key()
                    time.sleep(0.2)  # 无效密钥快速切换
                
                # 处理其他错误
                else:
                    print(f"❌ API错误 {response.status_code}: {response.text[:100]}")
                    self._switch_key()
                    time.sleep(1)
                    
            except requests.exceptions.Timeout:
                print(f"⏱️  请求超时,重试... (尝试 {attempt + 1}/{max_retries})")
                time.sleep(2)
                
            except Exception as e:
                print(f"❌ 未知错误: {str(e)}")
                self._switch_key()
                time.sleep(2)
        
        # 所有重试都失败
        self.stats["failed_requests"] += 1
        print(f"❌ 请求失败,已达到最大重试次数 ({max_retries})")
        return None
    
    def print_stats(self):
        """打印统计信息"""
        print("\n" + "="*50)
        print("📊 API调用统计")
        print("="*50)
        print(f"总请求数: {self.stats['total_requests']}")
        print(f"成功: {self.stats['successful_requests']}")
        print(f"失败: {self.stats['failed_requests']}")
        print(f"API密钥切换次数: {self.stats['key_switches']}")
        print(f"模型切换次数: {self.stats['model_switches']}")
        platform = "硅基流动" if self.use_siliconflow else "OpenRouter"
        print(f"当前平台: {platform}")
        print(f"当前使用: 密钥 #{self.current_key_index + 1}, 模型 {self._get_current_model()}")
        print("="*50 + "\n")


class AgentWorldClient:
    """AgentWorld GPT-5.1 API客户端"""
    
    def __init__(self):
        self.model_api_mapping = AGENTWORLD_CONFIG["model_api_mapping"]
        self.base_url = AGENTWORLD_CONFIG["base_url"]
        self.models = AGENTWORLD_CONFIG["models"]
        self.current_model_index = 0
        
        # 统计信息
        self.stats = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "model_switches": 0
        }
        
        print(f"🚀 AgentWorld 客户端初始化完成")
        print(f"🎯 当前模型: {self.get_current_model()}")
        print(f"🔑 模型API映射: {len(self.model_api_mapping)}个")
    
    def get_current_model(self) -> str:
        """获取当前模型"""
        return self.models[self.current_model_index]
    
    def get_current_api_key(self) -> str:
        """获取当前模型对应的API密钥"""
        current_model = self.get_current_model()
        return self.model_api_mapping[current_model]
    
    def switch_model(self):
        """切换模型"""
        old_model = self.get_current_model()
        self.current_model_index = (self.current_model_index + 1) % len(self.models)
        new_model = self.get_current_model()
        self.stats["model_switches"] += 1
        print(f"🔄 切换模型: {old_model} -> {new_model}")
    
    
    def call_llm(
        self, 
        prompt: str, 
        max_retries: int = 10,
        temperature: float = 0.8,
        max_tokens: int = 4000,
        stream: bool = False
    ) -> Optional[str]:
        """
        调用AgentWorld GPT-5.1 API
        
        Args:
            prompt: 提示词
            max_retries: 最大重试次数
            temperature: 温度参数
            max_tokens: 最大token数
            stream: 是否使用流式输出
            
        Returns:
            生成的文本,失败返回None
        """
        self.stats["total_requests"] += 1
        
        for attempt in range(max_retries):
            try:
                headers = {
                    'Accept': 'text/event-stream' if stream else 'application/json',
                    'Authorization': f'Bearer {self.get_current_api_key()}',
                    'Content-Type': 'application/json'
                }
                
                payload = {
                    "model": self.get_current_model(),
                    "messages": [
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "stream": stream
                }
                
                response = requests.post(
                    self.base_url,
                    headers=headers,
                    json=payload,
                    timeout=120,  # GPT-5.1可能需要更长时间
                    stream=stream
                )
                
                if response.status_code == 200:
                    if stream:
                        # 处理流式响应
                        content = ""
                        for line in response.iter_lines():
                            if line:
                                line = line.decode('utf-8')
                                if line.startswith('data: '):
                                    if line == 'data: [DONE]':
                                        break
                                    try:
                                        data = json.loads(line[6:])  # 去掉 "data: " 前缀
                                        if 'choices' in data and len(data['choices']) > 0:
                                            delta = data['choices'][0].get('delta', {})
                                            if 'content' in delta:
                                                content += delta['content']
                                    except json.JSONDecodeError:
                                        continue
                        self.stats["successful_requests"] += 1
                        return content
                    else:
                        # 处理普通响应
                        result = response.json()
                        content = result["choices"][0]["message"]["content"]
                        self.stats["successful_requests"] += 1
                        return content
                
                # 处理限流错误 (429)
                elif response.status_code == 429:
                    print(f"⏳ 遇到限流(429),等待重试... (尝试 {attempt + 1}/{max_retries})")
                    time.sleep(2 ** attempt)  # 指数退避
                
                # 处理认证错误 (401) - 尝试切换模型
                elif response.status_code == 401:
                    print(f"❌ 认证失败(401),尝试切换模型...")
                    self.switch_model()
                    time.sleep(1)
                
                # 处理模型错误,尝试切换模型
                elif response.status_code == 400:
                    error_text = response.text
                    if "model" in error_text.lower():
                        print(f"⚠️  模型错误,尝试切换模型...")
                        self.switch_model()
                        time.sleep(1)
                    else:
                        print(f"❌ 请求错误 {response.status_code}: {response.text[:200]}")
                        time.sleep(2)
                
                # 处理其他错误
                else:
                    print(f"❌ API错误 {response.status_code}: {response.text[:200]}")
                    time.sleep(2)
                    
            except requests.exceptions.Timeout:
                print(f"⏱️  请求超时,重试... (尝试 {attempt + 1}/{max_retries})")
                time.sleep(5)
                
            except Exception as e:
                print(f"❌ 未知错误: {str(e)}")
                time.sleep(3)
        
        # 所有重试都失败
        self.stats["failed_requests"] += 1
        print(f"❌ 请求失败,已达到最大重试次数 ({max_retries})")
        return None
    
    def print_stats(self):
        """打印统计信息"""
        print("\n" + "="*50)
        print("📊 AgentWorld GPT-5.1 API调用统计")
        print("="*50)
        print(f"总请求数: {self.stats['total_requests']}")
        print(f"成功: {self.stats['successful_requests']}")
        print(f"失败: {self.stats['failed_requests']}")
        print(f"成功率: {self.stats['successful_requests']/self.stats['total_requests']*100:.1f}%" if self.stats['total_requests'] > 0 else "成功率: 0%")
        print(f"模型切换次数: {self.stats['model_switches']}")
        print(f"当前模型: {self.get_current_model()}")
        print("="*50 + "\n")
