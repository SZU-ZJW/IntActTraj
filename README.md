## IntActTraj: 数据集生成流程说明

本仓库包含从 GitHub 爬取真实 issue/PR、重现修复过程、生成“下一步指导语”多模型候选、对其打分排序，并最终构造 RM / DPO 训练数据集的完整流水线。

整体分为五个阶段：

1. 爬取 GitHub issue/PR 元数据（`1-crawl_from_github`）
2. 使用 SWE-agent 重现/演绎修复过程，采集轨迹（`2-SWE-agent`）
3. 从轨迹构造“下一步指导语”数据（`3-traj_pred`）
4. 对多模型指导语做排名打分（`4-rank`）
5. 构造最终 SFT / DPO 数据集（`5-generate_datasets`）

下面按阶段介绍依赖、输入输出和推荐的运行脚本。

---

## 0. 环境与依赖

- Python 3.9+（建议与 SWE-agent 一致的 Conda / venv 环境）
- 依赖包（部分）：
  - `httpx`, `tqdm`, `python-Levenshtein`, `numpy`, `PyYAML`
  - `transformers`（5 阶段使用）
  - 本地/离线 LLM 环境：`MutilOfflinevLLMModel` 依赖的 vLLM 或自定义模型加载代码（见 `utils/model.py`）
  - 可选：OpenAI 兼容 API（阶段 3 的清洗脚本可选使用）

建议先安装 SWE-agent 的依赖（`2-SWE-agent` 目录下的 `environment.yml` 或 `requirements.txt`），再确保本仓额外依赖安装完整。

---

## 1️⃣ 阶段一：从 GitHub 爬取原始数据（`1-crawl_from_github`）

目标：从指定的 GitHub 仓库列表中，爬取 closed issues、关联的 PR、patch/test_patch、base_commit 等信息，构建原始问题–修复对。

入口脚本：`1-crawl_from_github/all_process_ing.py`

### 1.1 配置 GitHub Token

在 `1-crawl_from_github/all_process_ing.py` 顶部填入你的 GitHub Token：

```python
TOKENS = [
    "ghp_xxx...xxx",  # Token 1
    "ghp_yyy...yyy",  # Token 2
]
```

脚本会在触发 rate limit 时自动切换 token。

### 1.2 关键参数

脚本使用 argparse，主要参数为：

- `--repo-root`：本地克隆的代码仓库存放路径（例如：`/path/to/SWE-Bench/repo`）
- `--save-root`：保存 jsonl 数据的根目录（例如：`/path/to/github-data`）
- `--repos`：要处理的仓库列表，格式为 `owner__repo`，例如 `django__django`

### 1.3 运行示例

```bash
cd /path/to/IntActTraj

python 1-crawl_from_github/all_process_ing.py \
  --repo-root /path/to/SWE-Bench/repo \
  --save-root /path/to/github-data \
  --repos django__django sqlfluff__sqlfluff
```

输出：每个 repo 一个 jsonl，例如：

- `/path/to/github-data/django__django/django__django.jsonl`

这些文件包含后续阶段可用的 `instance_id`, `problem_statement`, `patch`, `test_patch`, `created_at` 等信息。

---

## 2️⃣ 阶段二：使用 SWE-agent 重现/演绎（`2-SWE-agent`）

目标：基于阶段一的数据，使用 SWE-agent 在本地重现或模拟修复过程，采集详细的决策轨迹（trajectory）。

目录：`2-SWE-agent`（完整的 SWE-agent 代码仓库）

### 2.1 准备 SWE-agent 环境

参考 `2-SWE-agent/README.md` 中的说明完成：

- 依赖安装
- 测试环境配置
- 目标代码仓库准备（与阶段一一致）

### 2.2 回放 / 演绎脚本

本流程使用的脚本：`2-SWE-agent/scripts/run_replay.sh`

>注：由于重现演绎时需要安装对应实例的依赖环境，因此这里需要针对不同的代码库不同的版本，去对应的代码库中追溯如何安装开发环境

该脚本会从指定的 jsonl 数据集启动 SWE-agent，在本地环境中重新演绎推理，生成 `.traj` 轨迹文件，最后需要将其保存到：

- `2-SWE-agent/traj_collector/`

你可以根据自己的数据集修改 `run_replay.sh` 中的参数，使其读取阶段一生成的 jsonl。

运行示例：

```bash
cd /path/to/IntActTraj/2-SWE-agent
bash scripts/run_replay.sh
```

输出：大量 `*.traj` 文件存放在 `2-SWE-agent/traj_collector/`，作为后续阶段的输入。

>注：这里如何选择交互轨迹，需要人工将生成的交互轨迹和真实的补丁进行对比，来确定保留的实例

---

## 3️⃣ 阶段三：从轨迹构造“下一步指导语”训练样本（`3-traj_pred`）

目标：从 SWE-agent 轨迹中抽取多步交互，对每一步构造 `(issue_and_prestep, label)`，供“下一步指导语”模型训练与评估。

目录：`3-traj_pred`

整体子流程：

1. 轨迹 → step 序列（`step_k: {action, feedback}`）
2. 补充原始 `problem_statement`
3. 展开为多条 `(issue_and_prestep, label)` 记录
4. 多模型预测下一步指导语
5. 指导语清洗与多模型合并

### 3.1 Step 1：轨迹转 step 序列

脚本：`3-traj_pred/1_traj_to_history_to_step.py`

输入：

- `./2-SWE-agent/traj_collector/*.traj`

输出：

- 历史轨迹：`3-traj_pred/result/traj_history/{instance_id}_history.traj`
- 基础 step 数据：`3-traj_pred/result/interaction_data/interaction_data.jsonl`

运行：

```bash
cd /path/to/IntActTraj
python 3-traj_pred/1_traj_to_history_to_step.py
```

### 3.2 Step 2：追加 problem_statement

脚本：`3-traj_pred/2_append_problem_statement.py`

输入：

- `interaction_file = 3-traj_pred/result/interaction_data/interaction_data.jsonl`
- `data_path = 2-SWE-agent/datasets/python__mypy_final.jsonl`  
  （应为包含 `instance_id` 和 `problem_statement` 的原始任务数据集，可以替换为你自己的 jsonl）

输出：

- `3-traj_pred/result/interaction_data/interaction_data_final.jsonl`

运行：

```bash
python 3-traj_pred/2_append_problem_statement.py
```

如需适配其他任务集，请修改脚本中的 `data_path` 或改写为 argparse。

### 3.3 Step 3：构造 (issue_and_prestep, label)

脚本：`3-traj_pred/3_step_to_prestep.py`

逻辑：

- 对每个 instance 的多步 `step_k`：
  - 为每一步构造：
    - `issue_and_prestep`：包含 ISSUE（problem_statement）+ 已完成的若干 `(STEP, EXECUTION_RESULTS)`
    - `label`：下一步 step 的 `action` 文本（gold 下一步指导语）

输入：

- `3-traj_pred/result/interaction_data/interaction_data_final.jsonl`

输出：

- `3-traj_pred/result/interaction_data/interaction_data_for_Train.jsonl`

运行：

```bash
python 3-traj_pred/3_step_to_prestep.py
```

### 3.4 Step 4：多模型预测下一步指导语

脚本：`3-traj_pred/4_predicte_next_step.py`

逻辑：

- 使用 `MutilOfflinevLLMModel` 统一封装离线 vLLM / 本地模型
- 读取 `interaction_data_for_Train.jsonl` 中的 `issue_and_prestep`
- 使用 `config/default-guid.yaml` 中的 system / demo / instance 模板构造对话
- 批量推理生成 `response`（模型预测的下一步指导语）

关键参数：

- `--model`：本地模型名称或路径（由 `MutilOfflinevLLMModel` 解释）
- `--config`：默认 `./3-traj_pred/config/default-guid.yaml`
- `--data_path`：默认 `./3-traj_pred/result/interaction_data/interaction_data_for_Train.jsonl`
- `--save_path`：输出目录，建议按模型名区分，如 `./3-traj_pred/result/pred_result/qwen2.5-7b-instruct`
- `--batch_size` 等

输出：

- `{save_path}/prediction_para2.jsonl`  
  每行：`instance_id`, `issue_and_prestep`, `response`

运行示例（对某个模型）：

```bash
python 3-traj_pred/4_predicte_next_step.py \
  --model Qwen/Qwen2.5-7B-Instruct \
  --save_path ./3-traj_pred/result/pred_result/qwen2.5-7b-instruct
```

对多个模型重复运行此脚本，只需更换 `--model` 和 `--save_path`。

### 3.5 Step 5：清洗单模型预测结果（可选在线 API）

脚本：`3-traj_pred/5_guidance_to_guidance.py`

逻辑：

- 对每条 `response`：
  - 去掉前缀 `"The next step is to "` 并规范首字母
  - 截到第一句（避免过长/多句）
  - 如包含 ``` 或 `end_of_edit` 等异常模式，则通过 OpenAI 兼容 API 调用另一个模型进行修正

关键参数：

- `--data_path`：该模型对应的 `prediction_para2.jsonl`  
  默认：`./3-traj_pred/result/pred_result/qwen25-7B/prediction_para2.jsonl`
- `--save_path`：清洗后的结果路径  
  默认：`./3-traj_pred/result/pred_result/qwen25-7B/prediction_final.jsonl`
- `--model`, `--api_key`, `--base_url`：用于修正的在线模型配置

运行示例（对应上一步的 Qwen 模型）：

```bash
python 3-traj_pred/5_guidance_to_guidance.py \
  --data_path ./3-traj_pred/result/pred_result/qwen2.5-7b-instruct/prediction_para2.jsonl \
  --save_path ./3-traj_pred/result/pred_result/qwen2.5-7b-instruct/prediction_final.jsonl \
  --model gpt-4 \
  --api_key YOUR_API_KEY \
  --base_url https://api.openai.com
```

对每个模型的预测结果都可以运行一次此清洗脚本。

### 3.6 Step 6：多模型预测合并成 RM 数据

脚本：`3-traj_pred/6_tiqu.py`

逻辑：

- `reference_file`：使用 Step 3 生成的 `interaction_data_for_Train.jsonl`，从中取：
  - `instance_id`, `issue_and_prestep`, `label` → 记为 `guidance_0`（gold）
- `generated_files`：读取每个模型在 Step 5 清洗后的：
  - `./3-traj_pred/result/pred_result/{model}/prediction_final.jsonl`
- 对每条样本：
  - 合并成 `{guidance_0, guidance_1, ..., guidance_n}`
  - 做文本截断与规范化
  - 利用 Levenshtein 相似度去重
  - 将 `guidance_1..n` 重命名为 `pred_1..m`

内部模型列表（可根据你实际跑的模型改 `predicte_model_list`）：

```python
predicte_model_list = [
    "Deepseek",
    "llama3.1-8b-instruct",
    "Mixtral-8x7b",
    "phi-3.5-MoE",
    "qwen2.5-32b-instruct",
    "qwen2.5-7b-instruct",
    "qwen2.5-coder-32b",
]
```

输出：

- 中间：`3-traj_pred/result/datasets/merged_output.jsonl`
- 最终 RM 数据集：`3-traj_pred/result/datasets/final_RM.jsonl`

运行：

```bash
python 3-traj_pred/6_tiqu.py
```

`final_RM.jsonl` 就是后续 RM / Ranking / DPO 构建的基础数据集。

---

## 4️⃣ 阶段四：对多候选指导语进行排名（`4-rank`）

目标：用一个“打分模型”对 `final_RM.jsonl` 中的多候选指导语进行评分，得到每个候选的平均分，从而构造偏好排序信息。

目录：`4-rank`

主要脚本：

1. `1-rank_bsz_vllm.py`：离线 vLLM 批量 ranking（多 seed）
2. `2_average_rate.py`：汇总多个 seed 的评分，得到 `average_rate`
3. `3_zuhe.py`：基于评分生成 acc/rej 对（用于 DPO）

### 4.1 Step 1：多 seed 排名（vLLM）

脚本：`4-rank/1-rank_bsz_vllm.py`

逻辑：

- 对 `final_RM.jsonl` 中每条样本：
  - 从 `guidance_0` 和 `pred_*` 构造 prompt：
    - 问题 + 部分解决过程
    - 标准答案（gold）
    - 多个待评估候选
  - 让打分模型输出每个候选的 `Rate: x.x`
- 对不同的随机种子（默认 `[128, 512, 1024]`）分别跑一遍，得到多份评分结果。

关键参数：

- `--model`：打分模型（由 `MutilOfflinevLLMModel` 解释）
- `--config`：默认 `4-rank/prompt/config.yaml`
- `--data_path`：默认 `./3-traj_pred/result/datasets/final_RM.jsonl`
- `--save_path`：默认 `./4-rank/save`
- `--seeds`：默认 `[128, 512, 1024]`

输出：

- `./4-rank/save/rank_seed_{seed}-final.jsonl`

运行示例：

```bash
python 4-rank/1-rank_bsz_vllm.py \
  --model Qwen/Qwen2.5-32B-Instruct \
  --data_path ./3-traj_pred/result/datasets/final_RM.jsonl \
  --save_path ./4-rank/save \
  --seeds 128 512 1024
```

### 4.2 Step 2：汇总多个 seed 的评分

脚本：`4-rank/2_average_rate.py`

逻辑：

- 对每行样本，将 `rank_seed_{seed}-final.jsonl` 中提取的评分逐个位置平均，得到 `average_rate` 列表。
- 将该列表写回 RM 行，生成新的 jsonl。

关键参数：

- `--data_path`：默认 `./3-traj_pred/result/datasets/final_RM.jsonl`
- `--save_dir`：默认 `./4-rank/save`
- `--seeds`：默认 `[128, 512, 1024]`

输出：

- `./4-rank/save/rate.jsonl`

运行：

```bash
python 4-rank/2_average_rate.py \
  --data_path ./3-traj_pred/result/datasets/final_RM.jsonl \
  --save_dir ./4-rank/save \
  --seeds 128 512 1024
```

### 4.3 Step 3：生成 acc/rej 对（用于 DPO）

脚本：`4-rank/3_zuhe.py`

逻辑：

- 对每条样本：
  - 把 `guidance_0` vs 每个候选作为 acc/rej（一条 gold 对一条候选）
  - 再根据 `average_rate`，对不同候选之间构造高分 vs 低分的 acc/rej 对
- 使用 `5-generate_datasets/template.yaml` 中的模板，把 `issue_and_prestep` 转成 human prompt。

关键参数：

- `--input_file`：默认 `./4-rank/save/rate.jsonl`
- `--save_file`：默认 `./5-generate_datasets/acc_rej.jsonl`
- `--config_path`：默认 `./5-generate_datasets/template.yaml`

输出：

- `./5-generate_datasets/acc_rej.jsonl`  
  每行一个 acc/rej 样本，包含 `conversations`、`chosen`、`rejected`。

运行：

```bash
python 4-rank/3_zuhe.py
```

---

## 5️⃣ 阶段五：生成最终 SFT / DPO 数据集（`5-generate_datasets`）

目标：

- 从 `acc_rej.jsonl` 中筛出长上下文样本（SFT 用）
- 将剩余样本作为 DPO 数据集

目录：`5-generate_datasets`

主要脚本：

1. `1_dpo_datasets.py`：从 acc/rej 中抽取“长上下文 SFT 特例”
2. `2_generate.py`：从 acc/rej 中去掉这些特例，得到最终 DPO 数据

### 5.1 Step 1：长上下文 SFT 特例

脚本：`5-generate_datasets/1_dpo_datasets.py`

逻辑：

- 使用本地分词器统计 query 长度，找到超过阈值的长上下文样本（当前阈值为 6000 token）；
- 找到这类样本相关的行（多步 step），合并并格式化为 SFT 格式：
  - `{"conversations": [{"from": "human", "value": query}], "answer": {"from": "gpt", "value": answer}}`

输入/输出路径（已对齐当前仓库）：

- 输入：`./5-generate_datasets/acc_rej.jsonl`
- 模板：`./5-generate_datasets/template.yaml`
- 输出：`./5-generate_datasets/long_context_SFT_special.jsonl`

运行：

```bash
python 5-generate_datasets/1_dpo_datasets.py
```

> 注意：脚本中分词器路径写死为 `/data/zjw/models/Meta-Llama-3.1-8B-Instruct/`，需要根据你本地模型位置修改。

### 5.2 Step 2：最终 DPO 数据集

脚本：`5-generate_datasets/2_generate.py`

逻辑：

- 从 `acc_rej.jsonl` 中去掉那些已经进入 `long_context_SFT_special.jsonl` 的 query；
- 剩余的 acc/rej 样本全部写入 DPO 数据集。

输入/输出路径：

- `a_r_path = './5-generate_datasets/acc_rej.jsonl'`
- `filter_path = './5-generate_datasets/long_context_SFT_special.jsonl'`
- `dpo_save_path = './5-generate_datasets/dpo_datasets.jsonl'`

运行：

```bash
python 5-generate_datasets/2_generate.py
```

最终你会得到两个训练集：

- 长上下文 SFT 数据：`5-generate_datasets/long_context_SFT_special.jsonl`
- DPO 数据集：`5-generate_datasets/dpo_datasets.jsonl`

---

## 6️⃣ 总结：从爬取到最终数据集的完整命令顺序（示例）

假设你已经完成环境配置，并根据需要调整了 token、模型路径和数据路径，整个流程可以概括为：

```bash
cd /path/to/IntActTraj

# Phase 1: GitHub 爬取
python 1-crawl_from_github/all_process_ing.py ...

# Phase 2: SWE-agent 回放 / 演绎
cd 2-SWE-agent
bash scripts/run_replay.sh
cd ..

# Phase 3: 轨迹 → 下一步指导语数据
python 3-traj_pred/1_traj_to_history_to_step.py
python 3-traj_pred/2_append_problem_statement.py
python 3-traj_pred/3_step_to_prestep.py

# 对多个模型重复：
python 3-traj_pred/4_predicte_next_step.py --model ... --save_path ./3-traj_pred/result/pred_result/<model>
python 3-traj_pred/5_guidance_to_guidance.py --data_path ./3-traj_pred/result/pred_result/<model>/prediction_para2.jsonl --save_path ./3-traj_pred/result/pred_result/<model>/prediction_final.jsonl --api_key ... --model gpt-4

# 合并多模型预测构建 RM 数据
python 3-traj_pred/6_tiqu.py

# Phase 4: Ranking + acc/rej
python 4-rank/1-rank_bsz_vllm.py --model ... --data_path ./3-traj_pred/result/datasets/final_RM.jsonl --save_path ./4-rank/save
python 4-rank/2_average_rate.py --data_path ./3-traj_pred/result/datasets/final_RM.jsonl --save_dir ./4-rank/save
python 4-rank/3_zuhe.py

# Phase 5: 生成 SFT / DPO 数据集
python 5-generate_datasets/1_dpo_datasets.py
python 5-generate_datasets/2_generate.py
```

最终得到：

- RM 数据集（适合 RM 或 ranking 训练）：`3-traj_pred/result/datasets/final_RM.jsonl`
- 长上下文 SFT 数据集：`5-generate_datasets/long_context_SFT_special.jsonl`
- DPO 数据集：`5-generate_datasets/dpo_datasets.jsonl`

你可以根据自己的实验需要，选择使用其中一个或多个数据集进行训练。若要扩展到更多仓库/任务，只需从阶段一重新开始，或替换阶段二后的输入数据路径即可。
