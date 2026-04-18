import mwparserfromhell
import re
import json
from pathlib import Path


def clean_text(text: str) -> str:
    # 去HTML
    text = re.sub(r"<.*?>", "", text)

    # 去多余空行
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def parse_wiki_file(input_path, output_md, output_json):
    raw = Path(input_path).read_text(encoding="utf-8")

    wikicode = mwparserfromhell.parse(raw)

    sections = []
    current_section = {"title": "root", "content": ""}

    for node in wikicode.nodes:
        # ===== 标题 =====
        if isinstance(node, mwparserfromhell.nodes.heading.Heading):
            # 保存旧 section
            if current_section["content"].strip():
                sections.append(current_section)

            current_section = {
                "title": node.title.strip_code().strip(),
                "level": node.level,
                "content": ""
            }

        # ===== 普通文本 =====
        elif isinstance(node, mwparserfromhell.nodes.text.Text):
            current_section["content"] += node.value

        # ===== wikilink =====
        elif isinstance(node, mwparserfromhell.nodes.wikilink.Wikilink):
            text = node.text if node.text else node.title
            current_section["content"] += str(text)

        # ===== template（重点）=====
        elif isinstance(node, mwparserfromhell.nodes.template.Template):
            # 取最后一个参数（通常是正文）
            if node.params:
                current_section["content"] += str(node.params[-1].value)

        else:
            current_section["content"] += str(node)

    # 最后一段
    if current_section["content"].strip():
        sections.append(current_section)

    # ===== 清洗 =====
    for sec in sections:
        sec["content"] = clean_text(sec["content"])

    # ===== 输出 Markdown =====
    md_lines = []
    for sec in sections:
        level = sec.get("level", 2)
        md_lines.append("#" * level + " " + sec["title"])
        md_lines.append("")
        md_lines.append(sec["content"])
        md_lines.append("")

    Path(output_md).write_text("\n".join(md_lines), encoding="utf-8")

    # ===== 输出 JSON（RAG用）=====
    Path(output_json).write_text(
        json.dumps(sections, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


if __name__ == "__main__":
    parse_wiki_file(
        "data_raw/wiki.txt",
        "data_clean/cleaned.md",
        "data_clean/structured.json"
    )