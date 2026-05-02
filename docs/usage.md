# Usage

## Install
```bash
pip install -r requirements.txt
```

## Run App
```bash
streamlit run app.py
```

## Run Tests
```bash
python -m pytest
```

## Suggested Demo Settings
- 场景：生成式 AI 进入高校课堂
- Agent 数量：60
- 模拟轮数：12
- 信息干预：平衡型公共讨论
- 随机种子：42

## Interaction Steps
1. 在侧边栏选择政策场景和参数
2. 点击“运行模拟”
3. 查看指标卡、图表、代表性发言和治理分析报告

## Notes
- 项目运行不依赖 `train.jsonl`、`validation.jsonl` 等大型文件
- `sample_reference.jsonl` 仅用于轻量示例展示
