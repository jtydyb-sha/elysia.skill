import re
from pathlib import Path
import json

input_path = "data_clean/cleaned.md"
output_path = "data_clean/background_elysia.md"
'''
text = Path(input_path).read_text(encoding="utf-8")


# ===== 1️⃣ 表格标题 → ### =====
# 匹配：
# |-
# !标题
# |-
text = re.sub(
    r"\|-\s*\n!\s*(.+?)\s*\n\|-\s*\n\|",
    r"### \1",
    text
)

# ===== 2️⃣ ;xxx → ### xxx =====
text = re.sub(
    r"^;\s*(.+)",
    r"### \1",
    text,
    flags=re.MULTILINE
)

Path(output_path).write_text(text, encoding="utf-8")
'''

text = Path(output_path).read_text(encoding="utf-8")
# ===== 输出 JSON（RAG用）=====
output_json = "data_clean/background_elysia.json"
# ===== 3️⃣ 转 JSON（按标题切块）=====
chunks = []
current = {"title": "", "content": ""}

for line in text.split("\n"):
    if line.startswith("## "):
        if current["content"]:
            chunks.append(current)
        current = {
            "title": line[3:].strip(),
            "content": ""
        }
    else:
        current["content"] += line + "\n"

# 最后一块
if current["content"]:
    chunks.append(current)

# ===== 保存 JSON =====
Path(output_json).write_text(
    json.dumps(chunks, ensure_ascii=False, indent=2),
    encoding="utf-8"
)
