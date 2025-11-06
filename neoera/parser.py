# neoera/parser.py
import json
import os

def load_story(path: str):
    """
    读取剧情文件，返回解析后的 dict。
    目前支持 .json（未来可扩展 .yaml）
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Story file not found: {path}")

    ext = os.path.splitext(path)[1].lower()
    if ext == ".json":
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    elif ext in (".yaml", ".yml"):
        try:
            import yaml
        except ImportError:
            raise ImportError("YAML support not installed. Run `pip install pyyaml`.")
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    else:
        raise ValueError(f"Unsupported file type: {ext}")
