from pathlib import Path
import json, shutil, sys
root = Path(__file__).resolve().parent
tools = {'python': sys.executable}
for name, command in {'java':'java','javac':'javac','zig':'zig','php':'php','vscode':'code','arduino':'arduino','arduino_cli':'arduino-cli','android':'studio','figma':'figma'}.items():
    tools[name] = shutil.which(command) or ''
(root / 'config.json').write_text(json.dumps(tools, indent=2), encoding='utf-8')
print('Created a local config.json using available toolchains.')
