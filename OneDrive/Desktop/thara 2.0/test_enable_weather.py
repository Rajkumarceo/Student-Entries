import importlib.util
from pathlib import Path
p = Path(r"c:\Users\Rajkumar\OneDrive\Desktop\thara 2.0\main.py")
spec = importlib.util.spec_from_file_location('thara_main', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

settings = mod.load_settings()
print('Loaded settings:', settings)
enabled, message = mod.enable_weather(settings, allow_offline=True)
print('Enable weather result:', enabled, message)
print('Updated settings file content:')
import json
print(json.dumps(mod.load_settings(), indent=2))
