from pathlib import Path
from typing import Dict
import os
import json
import getpass
import dashscope

def read_key_file(file_path: Path) -> Dict[str, str]:
    """
    从文件读取API密钥
    
    Args:
        file_path: 密钥文件路径
    Returns:
        包含密钥的字典
    Raises:
        json.JSONDecodeError: JSON解析错误
    """
    try:
        return json.loads(file_path.read_text())
    except json.JSONDecodeError:
        raise ValueError("密钥文件格式错误")

def save_key_file(key_dict: Dict[str, str], file_path: Path) -> None:
    """
    保存API密钥到文件
    
    Args:
        key_dict: 包含密钥的字典
        file_path: 保存路径
    """
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(json.dumps(key_dict, indent=4))

def get_key_from_user() -> str:
    """从用户输入获取API密钥"""
    return getpass.getpass("未找到密钥文件，请输入你的DashScope API密钥: ").strip()

def load_key() -> None:
    """
    加载DashScope API密钥
    - 优先从Key.json文件读取
    - 如果文件不存在,则提示用户输入并保存
    - 将密钥设置到环境变量和dashscope配置中
    
    Raises:
        ValueError: 密钥格式无效
    """
    # 获取密钥文件的绝对路径
    key_file = Path(__file__).parent / 'Key.json'
    
    try:
        if key_file.exists():
            # 从文件读取密钥
            key_data = read_key_file(key_file)
            api_key = key_data.get("DASHSCOPE_API_KEY", "").strip()
        else:
            # 从用户输入获取密钥
            api_key = get_key_from_user()
            save_key_file({"DASHSCOPE_API_KEY": api_key}, key_file)
            
        # 验证密钥格式
        if not api_key:
            raise ValueError("API密钥不能为空")
            
        # 设置环境变量和dashscope配置
        os.environ['DASHSCOPE_API_KEY'] = api_key
        dashscope.api_key = api_key
        
    except Exception as e:
        raise ValueError(f"加载API密钥失败: {str(e)}")

if __name__ == '__main__':
    # 测试密钥加载功能
    try:
        load_key()
        print(f"成功加载API密钥")
    except ValueError as e:
        print(f"错误: {e}")
