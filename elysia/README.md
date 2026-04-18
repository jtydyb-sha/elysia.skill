<div align="center">

# 爱莉希雅.skill

[![许可证](https://img.shields.io/badge/License-MIT-blue.svg)](许可证)
[![游戏](https://img.shields.io/badge/Game-崩坏3-orange.svg)](https://bh3.mihoyo.com/)

</div>

> 一个开源的爱莉希雅角色扮演技能包，帮助AI稳定还原《崩坏3》中爱莉希雅的角色设定、语气和情感。

## 🚀 快速开始

### 系统要求

- 支持Skill格式的AI平台（如Trae IDE）
- 基本的角色扮演或AI对话开发环境

### 安装指南

1. **下载项目**
   ```bash
   git clone https://github.com/your-username/elysia-skill.git
   cd elysia-skill
   ```

2. **集成到你的项目**
   - 将整个 `elysia` 文件夹复制到你的技能目录
   - 确保你的AI系统支持Skill格式

## 依赖环境
### 1. Python 环境

| 配置项 | 值 |
|--------|-----|
| Python 解释器路径 | `C:\Users\miniconda3\envs\your_env\python.exe` |

使用前先将解释器路径传入 `SKILL.md` 运行规则第五条中执行本地 RAG 知识库调用


### 2. Ollama 嵌入模型

本 RAG 系统依赖 Ollama 提供的嵌入模型进行向量化检索，所用模型为 `bge-m3:567m-fp16`。若需更改模型，请调用 `scripts\embedding.py` 重新构建向量库，并在 `scripts\config.json` 中更改 `embed_model`。

| 组件 | 说明 |
|------|------|
| **Ollama 服务** | 本地运行的 LLM 服务框架 |
| **嵌入模型** | 用于将文本转换为向量（如 `nomic-embed-text`、`bge-m3` 等） |


### 3. API 调用依赖

RAG 查询脚本需要调用 LLM API 进行答案生成，本项目使用 `deepseek` 作为 RAG 查询的 API 接口，使用前在 `scripts\config.json` 中填写 `api_key`。

## 角色扮演示例

**用户输入**: "我好喜欢你啊"

**期望输出**: 
"哎呀，听到你这么说，我的心里就像有无数朵花在瞬间绽放了呢~♪
能被你喜欢，真是让我感到无比幸福的事情。你知道吗？爱对我来说，从来都不是抽象的概念，而是需要被拥抱、被回应、被延续的东西。就像现在这样，你的心意像温暖的阳光一样洒在我的心上，让我这个如花朵般娇羞的少女都忍不住想要绽放得更灿烂一些呢~
不过呀，我更想知道的是……你喜欢的是怎样的我呢？是那个在战场上守护人类的战士，还是那个在宴会中绽放笑容的粉色妖精小姐？又或者……是那个愿意为未来种下希望种子的爱莉希雅？♪
无论答案是什么，我都会用最真诚的心来回应你的喜欢。因为我相信，每一份真挚的情感都值得被温柔对待，就像每一朵花都值得在阳光下绽放一样~"

## 自定义配置

你可以在 `SKILL.md` 中调整角色参数，或在 `interaction.md` 中添加自定义台词。

## 📁 项目结构

```
elysia/
├── README.md                        # 项目说明文档（本文件）
├── SKILL.md                         # 技能入口与扮演规则
├── profile.md                       # 角色身份与核心标签
├── personality.md                   # 性格、动机与价值观
├── interaction.md                   # 互动语气与台词风格
├── relations.md                     # 关系网络与人物联动
├── data_clean
    ├── background_elysia.json       # 爱莉希雅背景故事
    ├── background_fire_moth.json    # 逐火之蛾背景故事
    ├── background_wiki.json         # 部分wiki原文
├── date_raw
    └── wiki.txt                     # wiki源代码
├── index\vector_store               # RAG向量库
├── scripts
    ├── config.json                  # 模型配置文件
    ├── embedding.py                 # RAG库嵌入向量
    ├── parse_wiki.py                # wiki源代码清洗
    ├── query_test.py                # RAG库查询测试样例
    ├── rag_query.py                 # RAG库查询
    ├── to_json.py                   # 背景故事划分
└── LICENSE                          # 开源许可证
```

## 🔧 开发指南

### 扩展角色设定

如果你想添加新的角色特征或台词：

1. **编辑 `interaction.md`** - 添加新的台词样本
2. **更新 `personality.md`** - 扩展性格描述
3. **修改 `relations.md`** - 添加新的关系设定
4. **增加新的 `data_clean\background.md`** - 补充背景故事

## 📄 许可证

本项目采用 [MIT 许可证](LICENSE)。

## 🙏 致谢

### 数据来源

- [萌娘百科官网](https://moegirl.icu/Mainpage)
- [崩坏3WIKI官网](https://baike.mihoyo.com/bh3/wiki/?bbs_presentation_style=no_header)
- 游戏内剧情和语音台词
- 社区玩家整理资料

### 特别感谢

- [cyrene.skill](https://github.com/HeartEase1/cyrene.skill) 本项目采用了与之相似的数据采集方式进行开发
- 《崩坏3》开发团队创造了如此丰富的角色
- 社区玩家提供的宝贵资料和分析

## 致歉
由于作者本人代码水平低下，项目环境配置方面有诸多不合理之处，多次尝试仍未解决。运行前所需改动已在[依赖环境](#依赖环境)中进行了说明。

---

⭐ 如果这个项目对你有帮助，请给一个Star！

