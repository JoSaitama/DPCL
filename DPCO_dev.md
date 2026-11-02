# DPCO 开发协议与变更记录

## 一、开发协议（2026-10-28 生效）

### 1. 修改授权

- 只有用户明确要求修改代码，才可新增、修改、重命名或删除代码文件，以及改变程序行为的配置、依赖、启动脚本。
- “读论文”“解释”“分析”“讨论”“给方案”只授权相应的研究与说明工作，不授权实现代码。代码修改授权仅对用户明确指定的任务和必要关联文件有效。
- 本次用户明确要求把 SAGE 文件夹及 Python 代码中的 SAGE 名称改为 DPCO，因此本次可以进行一致性更名；不能据此实现 Adam、调整梯度算法或改动训练默认行为。

### 2. 记录要求

- 所有代码和理论变动统一记入本文件，包括新增、更正、撤回，以及对理论前提、公式、结论或适用范围的修改。
- 每条记录写清：日期、授权依据、目的、涉及文件、变更内容、验证与结果、假设与限制、后续待办。
- 研究讲解也应记录核心结论和来源；较长推导可另存 `docs/` 并在本文件链接，关键更正必须在本文件说明。
- 追加记录，不删除或覆盖旧记录；历史错误通过追加更正保留可追溯性。

### 3. 目录和命名

- 后续代码开发与修改统一在 `DPCO/` 内进行。
- 复用原 SAGE 代码，目录使用 `DPCO`，Python 模块、方法字符串及标识符使用对应的 `DPCO` / `dpco`，同步更新调用所依赖的配置、脚本和说明。
- 名称更换不代表新算法已经定义或取得改进；更名前后的数学更新规则应相同。
- 历史实验数据、检查点、旧开发日志及 Git 历史不改写。旧名称的历史产物与新名称接口之间的迁移，需要单独分析与授权。

### 4. 理论和验证

- 按面向博一学生的细讲风格说明目标函数、符号、推导、动机、例子、假设和反例。
- 分清原文主张、已证结论、教学近似和未验证设想；分清优化速度、最终训练效果、测试泛化和实际成本。
- 保留用户现有未提交修改；本地验证应与授权范围对应，不擅自启动正式训练或执行 Git 提交、推送。

### 5. 执行入口

项目根目录 `../AGENTS.md` 与本目录 `AGENTS.md` 供后续开发读取；本文件是代码和理论变动的统一记录入口。原 `docs/development.md` 保留为复用代码的历史档案，不再作为新变更的唯一记录。

### 6. 可复用数据与实验输出的路径（2026-10-31补充）

- 用户要求后续用于训练的数据放在与 `DPCO/` 同级的 `data/`，即代码目录中的 `../data/`；服务器为 `/home/jason_chia925_gmail_com/Project_DPCO/data/`。
- 包含原始/预处理数据、固定污染标签/manifest、可复用预测缓存和生成器预训练权重。训练指标、checkpoint、运行日志、图及人工抽查报告仍保存于 `DPCO/results/` 对应子目录。
- 显式传递数据输出目录与检查报告目录，不自动搬迁或覆盖旧产物；旧开发记录保留原始含义，后续路径以本补充约定为准。

## 二、变更记录

### 2026-10-28 / DPCO-0001：建立协议并执行项目一致性更名

- **授权依据：** 用户原话：“所有代码和理论的变动都要写入dpco文件夹下的DPCO_dev.md文档”；“只有我明确说明修改代码后，才修改文件”；“包括文件夹名字SAGE在内的py文件，都把SAGE的名字改为DPCO”。
- **目的：** 建立后续开发约束，并将原 SAGE 代码作为 DPCO 项目的起点。
- **现有状态：** 原 SAGE 仓库已有修改和未跟踪文件；更名基于当前文件内容进行，不回滚这些工作。原仓库 Git 历史和原始结果保留。
- **涉及文件：** 根目录 `AGENTS.md`；本文件；本目录 `AGENTS.md`；原 `SAGE/` 下含 SAGE 名称的 Python 文件、相关配置、启动脚本、项目元信息及当前说明文档。逐文件清单见本次工作完成后的验证记录。
- **变更内容：** `SAGE/` → `DPCO/`；Python 中名称及导入 `SAGE` / `sage` → `DPCO` / `dpco`，保留大小写风格；同步相关文件名、配置键、CLI 参数、环境变量、结果字段和脚本引用。普通英文单词中的子串（如 `message`、`usage`）不替换。`docs/development.md` 保留原文。
- **行为边界：** 仅改名称，不改变原更新公式、超参数数值、训练策略和参考梯度语义。新接口不自动兼容旧名称的命令、配置和检查点；历史产物保持原样，不能宣称已完成旧检查点迁移。
- **验证进展：** 已核对 70 个既有文件均仅作名称替换；97 个 Python 文件 AST、13 个 TOML、4 个 shell 脚本语法通过；153 个历史日志/结果文件哈希保持一致。首轮既有 CPU 回归运行 209 项，206 项通过，1 项暴露测试字面量中转义换行后的旧配置名漏替换，2 项因测试环境缺少 matplotlib 报错。已补齐该测试字面量更名，复用本机已有绘图环境路径重跑，不更改项目依赖。最终结果见末尾。未启动正式训练。

### 2026-10-28 / DPCO-0002：阅读 Adam 并建立与 SGD 的对照讲解

- **授权依据：** 用户要求“按照给博一学生的细讲风格，把adam这篇论文对比着sgd给我讲一下”。这项授权用于阅读和理论说明，不用于实现 Adam。
- **论文来源：** 项目根目录 `1412.6980v9.pdf`，Kingma 与 Ba，*Adam: A Method for Stochastic Optimization*，ICLR 2015，所给文件为 arXiv v9（2017-01-30），15 页。
- **记录位置：** `docs/adam_vs_sgd.md` 保存完整推导、示例及文献边界。
- **核心结论：** Adam 使用梯度的一阶指数移动平均估计方向，使用逐坐标的二阶原始矩指数移动平均估计尺度，并修正零初始化造成的权重缺失。它可能改善噪声梯度、坐标尺度差异和稀疏特征下的优化；不存在普遍优于 SGD 的保证。
- **关键边界：** 二阶原始矩不是方差或 Hessian；平均梯度的平方不等于样本梯度平方的平均；一阶矩的平滑收益必须与带动量 SGD 公平比较。初始化偏差修正不消除非平稳滞后、梯度本身的偏差或更新比值的偏差。
- **理论证据：** 原文在线凸优化遗憾分析与深网的非凸优化、最终泛化不同；后续 Reddi 等（ICLR 2018）指出原分析的问题并给出 Adam 不收敛的凸例子。Wilson 等（2017/2018）提供自适应方法泛化劣于 SGD 的例子；这些结果也不意味着 Adam 总是较差。
- **项目理论状态：** 本次未定义新的 DPCO 算法，也未把 Adam 的机制或保证赋予更名后的旧代码。待用户指定 DPCO 的新目标和定义后，再讨论或实现相应理论变动。

### DPCO-0001 附：本次更名文件清单

- 目录：`SAGE/` → `DPCO/`。下面路径均相对于 `DPCO/`；共 70 个既有文本文件发生名称替换，其中 15 个文件同时更名。
- `AGENTS.md`、`DPCO_dev.md` 和 Adam 讲解为新增文档，另计；旧历史日志及结果文件按字节哈希保留。

- `run_sage_theory_suite.sh` → `run_dpco_theory_suite.sh`
- `run_inaturalist_suite.sh`（内容名称替换）
- `run_sage_mechanism_suite.sh` → `run_dpco_mechanism_suite.sh`
- `pyproject.toml`（内容名称替换）
- `README.md`（内容名称替换）
- `run_sage_suite.sh` → `run_dpco_suite.sh`
- `tests/test_tpu_mechanisms.py`（内容名称替换）
- `tests/test_sage_warmup.py` → `tests/test_dpco_warmup.py`
- `tests/test_alternating_first.py`（内容名称替换）
- `tests/test_plot_training_results.py`（内容名称替换）
- `tests/test_observation.py`（内容名称替换）
- `tests/test_training_diagnostics.py`（内容名称替换）
- `tests/local_mesh_check.py`（内容名称替换）
- `tests/test_updates.py`（内容名称替换）
- `tests/test_inaturalist_training.py`（内容名称替换）
- `tests/test_directions.py`（内容名称替换）
- `tests/test_inverse_sqrt.py`（内容名称替换）
- `tests/test_checkpoint_controls.py`（内容名称替换）
- `tests/test_suite.py`（内容名称替换）
- `tests/test_config.py`（内容名称替换）
- `tests/test_trainer.py`（内容名称替换）
- `tests/test_sage_policy.py` → `tests/test_dpco_policy.py`
- `tests/test_references.py`（内容名称替换）
- `tests/test_sage_r.py` → `tests/test_dpco_r.py`
- `tests/test_theory_validation.py`（内容名称替换）
- `tests/test_classification.py`（内容名称替换）
- `tests/mechanism_mesh_check.py`（内容名称替换）
- `tests/test_tpu_pipeline.py`（内容名称替换）
- `docs/inaturalist_subset.md`（内容名称替换）
- `docs/training_diagnostics.md`（内容名称替换）
- `docs/tpu_mechanisms.md`（内容名称替换）
- `docs/recording.md`（内容名称替换）
- `docs/result_csv_guide.md`（内容名称替换）
- `docs/tpu_training.md`（内容名称替换）
- `docs/theory_validation.md`（内容名称替换）
- `configs/imagenet1k_resnet101_sage_e.toml` → `configs/imagenet1k_resnet101_dpco_e.toml`
- `configs/imagenet1k_resnet50_sage_e.toml` → `configs/imagenet1k_resnet50_dpco_e.toml`
- `configs/imagenet100_resnet50_sage_e.toml` → `configs/imagenet100_resnet50_dpco_e.toml`
- `configs/imagenet100_resnet101_sage_e.toml` → `configs/imagenet100_resnet101_dpco_e.toml`
- `scripts/validate_sage_theory.py` → `scripts/validate_dpco_theory.py`
- `scripts/sanity_recording.py`（内容名称替换）
- `scripts/plot_training_results.py`（内容名称替换）
- `scripts/train_classification.py`（内容名称替换）
- `scripts/launch_tpu.py`（内容名称替换）
- `scripts/run_suite.py`（内容名称替换）
- `scripts/sanity_core.py`（内容名称替换）
- `src/config.py`（内容名称替换）
- `src/__init__.py`（内容名称替换）
- `src/cli.py`（内容名称替换）
- `configs/tpu/inaturalist2021_resnet50.toml`（内容名称替换）
- `configs/tpu/imagenet100_resnet50_sage_e.toml` → `configs/tpu/imagenet100_resnet50_dpco_e.toml`
- `src/probes/classification.py`（内容名称替换）
- `src/probes/mechanism_config.py`（内容名称替换）
- `src/probes/theory_validation.py`（内容名称替换）
- `src/probes/tpu_mechanisms.py`（内容名称替换）
- `src/probes/gradient_statistics.py`（内容名称替换）
- `src/probes/training_diagnostics.py`（内容名称替换）
- `src/methods/sage.py` → `src/methods/dpco.py`
- `src/methods/sage_warmup.py` → `src/methods/dpco_warmup.py`
- `src/methods/__init__.py`（内容名称替换）
- `src/methods/sage_policy.py` → `src/methods/dpco_policy.py`
- `src/methods/base.py`（内容名称替换）
- `src/references/correct_subset.py`（内容名称替换）
- `src/training/results.py`（内容名称替换）
- `src/training/recording.py`（内容名称替换）
- `src/training/runtime.py`（内容名称替换）
- `src/training/experiment.py`（内容名称替换）
- `src/training/launch.py`（内容名称替换）
- `src/training/schedules.py`（内容名称替换）
- `src/training/status.py`（内容名称替换）

### 2026-10-28 / DPCO-0001、0002 完成验证

- **更名复核：** 将更名前的当前工作内容按确定的名称映射变换后，与全部 70 个修改后的既有文件逐字比较一致；包含修正转义换行后测试配置键的替换。未引入算法计算式或超参数数值变动。97 个 Python 文件解析通过，名称扫描无旧项目标识；`usage`、`message` 等普通英文保持原样。13 个 TOML 解析与 4 个 shell 脚本语法检查通过，Git 差异空白检查通过。
- **完整回归：** 第二轮 `python -m unittest discover -s tests -t .`，209 项全部通过，用时 84.405 秒。使用本机既有临时 JAX/Flax 测试环境，并通过 PYTHONPATH 复用已有 matplotlib 包；未安装或修改依赖。测试日志在 `/private/tmp/dpco-regression-final.log`（临时诊断材料，不是长期档案）。
- **历史保护：** 原 `docs/development.md` 及 `results/` 中共 153 个文件 SHA-256 与更名前一致。原有未提交/未跟踪工作基于其当前内容更名并保留；未进行提交、推送或远程操作。测试仅运行本地既有测试夹具，不是正式训练或 TPU 验证。
- **理论复核：** 阅读给定 PDF 共 15 页的提取内容，渲染核对 Algorithm 1、初始化修正、理论假设及图 1-4 所在完整页面；手算示例与默认系数的首步比值另用标量计算复核。长篇讲解保存在 `docs/adam_vs_sgd.md`，涵盖公式、噪声与尺度动机、偏差修正、对照实验、原文符号问题、后续收敛反例及与现有代码的区别。
- **新增文档：** 根目录 `../AGENTS.md`、本目录 `AGENTS.md`、本文件及 `docs/adam_vs_sgd.md`。两个执行规则文件供后续会话读取；后续所有代码及理论变更仍以本文件为统一记录入口。
- **限制及后续：** 未实现 Adam、未定义新的 DPCO 理论、未验证真实训练性能。旧 SAGE 命令/配置/结果字段和检查点中的旧名称未提供兼容层；原始结果及历史日志继续保留旧名，未来读取或迁移时须单独检查，不能直接假定新代码兼容。下一次代码实现或行为改变仍需用户明确授权。

### 2026-10-28 / DPCO-0003：历史 batch 梯度 reference 的可行性分析（理论候选）

- **授权依据：** 用户新加入 `SAGE_Proof_byProf/`，要求从理论分析历史 gradient mean reference 是否可行及如何定义。仅授权阅读、理论分析与按协议记录，未授权实现或修改代码。用户补充教授没有给出具体算法，只表示考虑历史 batch 的 gradient mean。
- **用户提供的经验状态：** 用户报告现有实验框架中 SAGE-E、SAGE-L 均低于普通 SGD；教授认为应考虑历史梯度，并报告 MNIST 有效。本次未复核原始实验输出，也未获得教授的 MNIST 方法细节，不能将本次 EMA 定义称作已复现或已验证的教授算法。
- **阅读来源：** `../SAGE_Proof_byProf/` 中三定理 PDF、`SAGE_theoretical_framework_cn.pdf` 及 DIVE 背景论文 `2608.22522v1.pdf`。原文件名称和内容全部保留。结合 Adam 一阶矩结构及动量/梯度投影相关原始文献核对术语。
- **涉及文件：** 新增 `docs/historical_gradient_reference_analysis.md`；本文件追加记录。未更改既有 Adam 阅读笔记、算法源文件、配置、依赖或启动脚本。
- **原理论适用范围澄清：** 定理 1 是任意 reference 下的代数最优；定理 2、3 需要 reference 等于真实目标梯度或另行证明目标迁移。总框架已提出 mismatch 条件，定理 3 也明确上界不直接排列不同完整轨迹。本次实验负结果不自动否定这些条件命题，但不支持无条件的实际优越性解释。不能确认 reference 是唯一失效原因。
- **候选 A（只更换 reference）：** 设 G_t 是未编辑的原始全 batch 平均梯度，m_0=0，r_1=0，t≥2 时 r_t=m_{t−1}/(1−β^{t−1})；本步评分后用 m_t=βm_{t−1}+(1−β)G_t 更新记忆。第一步/零 reference 回退普通 SGD。使用过去历史、全样本、未裁剪/未预条件/未翻转的梯度；不使用 S_t 写回，避免自我强化。β=0.9 仅为可讨论起点，尚未确定实验参数。
- **偏差修正边界：** 正的偏差修正因子不改变 hard sign 的判定，因此不应声称它改善翻转选择；保留它用于定量比较 reference 与真实梯度。缓存旧参数处梯度与保存样本后在当前参数重算梯度不同，前者不能直接充当历史目标在当前点的精确梯度。
- **降噪与滞后：** 固定参数/独立 batch 模型下，EMA 稳态噪声二阶矩因子为 (1−β)/(1+β)；β=.9 相当于约 19 个等权观测的噪声因子，平均梯度年龄约 10 步。实际轨迹引入参数漂移。笔记给出有限历史权重平方和、平均滞后以及在 L-smooth、鞅差噪声和有界位移条件下的 L² 误差上界；没有把这些假设当成实际网络已验证事实。
- **新分析的核心条件：** C=S−G，Δ=rᵀC≥0，真正目标的一阶增益 Λ=∇FᵀC≥Δ−||r−∇F||·||C||。故 reference 误差小于 Δ/||C||（C≠0）是充分条件。笔记补充条件期望版本、严格的有限步长差值界和在已知确定误差界时可用的负投影裕量；EMA 本身没有提供可直接部署的误差证书。
- **反例：** 构造 Hessian 为单位矩阵的二维强凸目标，在 h=(1,.01)、r=(1,0)、g₁=(−.001,1)、g₂=(2.001,−.98) 时，整向量翻转产生 C=(.001,−1)，Δ=.001>0，但 Λ=−.009<0，且每个正步长的目标都劣于同状态 SGD。reference cosine 约 .99995 仍不足以保证好转。另给出独立且无偏的单批 reference 也可能使编辑方向反向的一维例子。
- **候选 B（单独的编辑规则备选，未决定采用）：** 对负投影只反射沿 r 的分量：g̃=g−2min(rᵀg,0)r/||r||²，r=0 时不改。聚合修正为 Δr/||r||²，保留相同 reference 投影增益及样本范数；只要 hᵀr>0 且 Δ>0，就有严格一阶增益。它不再属于原定理 1 的标量权重可行集，不能当成只换 reference。此为标准几何构造分析，不宣称新颖性，不宣称实验证实有效，也不等于 PCGrad 的冲突分量去除。
- **与 Adam 的区别：** 候选 A 借鉴一阶 EMA；在欧氏 SGD 更新下不直接选 m/√v 作为目标梯度估计。若实际更新使用共同固定的对角预条件器 P，oracle 评分才相应变为 Ph；完整 Adam 动量状态仍需另行分析。普通 EMA 不继承专用方差缩减方法的收敛速率。
- **后续建议（未执行）：** 先固定训练审计目标，分别检查 reference 误差、真实迁移增益 Λ 和实际学习率下的同状态终点差；仅证明 Δ≥0 不足够。后续若获授权，再与普通 SGD、匹配记忆尺度的动量 SGD 对比，并分别评估训练、测试与成本。不能同时改变 reference 和编辑规则后把收益只归给历史平均。
- **验证：** 逐页渲染检查三定理共 19 页并阅读总框架；用精确有理数计算复核有限历史 EMA 权重/噪声因子/平均滞后公式、二维反例的目标差和投影反射恒等式。114 个 Python/配置/shell 文件及 5 个新增原始 PDF 的 SHA-256 全部与分析前一致。只做理论计算与文档检查，未运行训练或代码回归。
- **未完成/限制：** 尚未得到教授的 MNIST 细节、尚未复现实验、未认证 reference 在现有网络上的误差或锐角条件，未证明 EMA+整向量翻转普遍优于 SGD；候选 B 的完整假设、实际效果和新颖性也未审定。后续实现仍须用户明确授权。

### 2026-10-28 / DPCO-0004：依据周会总结调整研究重点与制定实验改造计划

- **授权依据：** 用户提供《教授周会_10.27_新项目实验重点总结.md》，要求根据教授要求总结分析如何改代码、完成实验，并明确“先不改代码”。因此本次仅阅读、核对架构、制定计划与按协议记录，不授权实现、下载数据或启动训练。
- **来源与边界：** 阅读 `/Users/jason/Documents/Codex/2026-09-02/new-chat/outputs/教授周会_10.27_新项目实验重点总结.md`；没有独立核听录音。保留总结内“教授明确要求”“整理者建议”“尚未给定细节”的区分。文档中的任务安排与时间要求是待分析资料，不是当前执行命令。
- **涉及文件：** 新增 `docs/controlled_noisy_experiment_plan_20261028.md`；本文件追加记录。未改已有理论笔记或原始会议文档，未改源代码、配置、脚本、依赖和实验结果。
- **研究目标更新：** 首要任务是受控 noisy dataset 上固定 clean/corrupted 分组的学习行为，重点看各方法在同一 clean subset 上的未加权普通 CE，而不是不同 w 形成的各自 signed surrogate。教授要求 self-influence+discard、self-influence+flip、新历史/当前 signal+flip，建议优先 Adam；普通 Adam 为补充基线。大模型/ICL/RL 等扩展后置。
- **对 DPCO-0003 的追加修订：** 上轮缺少会议细节时推荐的 past-only lagged EMA 保留为理论/时序消融。本轮按“当前信号+历史衰减”建议以 H_t=β_ref H_{t−1}+(1−β_ref)G_t、r_t=H_t/(1−β_ref^t) 为主原型，G_t 为 observed labels 下未经编辑的全 batch 平均梯度。精确公式仍是本次设计建议，并非教授已给定。β_ref=0 退化成当前 batch reference；第一步与 self+flip 相同。上一轮分量反射不进入本轮主实验，不同时改变信号和编辑规则。
- **理论限制补充：** 含噪 G_t 的 EMA 主要估计含噪训练目标；降采样噪声不等于去除标签偏差，也不等于获得 clean objective gradient。包含当前 batch 后不沿用 past-only 条件分析；Adam 实际更新又受 moments 影响，旧 rᵀC 恒等式不能直接充当 Adam 的实际下降保证。
- **候选实验设置（未定稿/未执行）：** 建议 CIFAR-10、小图 ResNet-18、训练/干净验证分层 45k/5k、官方干净测试集、训练中精确 40% 对称改标且保证实际标签变化；污染/split manifest 固定并记录哈希。FP32，Adam(.9,.999,1e−8)，β_ref=.9 为初始假设；B128、100 loader epochs 为建议预算。上述模型/数据/比例/参数并非教授指定。
- **主对照：** Plain Adam、Self+Discard+Adam、Self+Flip+Adam、EMA-current+Flip+Adam。共享原 B 归一化、数据顺序、初始化/增强、训练预算及同一 Adam；用 C vs D 隔离历史收益，用 B vs C 比较 discard/flip。现有 DTV 已实现 gradient discard；有 BN 时并不等于 forward 前删除数据。第一版不混入 LO 或局部层评分；总结中 LO 的精确定义仍未确认。
- **评价口径：** 固定 clean train 的 true-label CE；固定 corrupted train 的 observed-label CE 与 true-label CE；干净验证/最终测试、按分组的干预率、普通 CE/accuracy、数值有限性与时间/内存。污染标记与原始标签仅用于评价，不进入评分/权重。高 corrupted observed CE 必须联合 clean/true-label 表现解释，不以提高污染损失为训练目标，不按结果动态挑选子集。
- **现有代码核对：** `updates.py` 只有 SGD updater；`method_state` 和 `optimizer_state` 已分离；DTV/DPCO 及 VJP/JVP 可复用；runner 的状态初始化/验证当前绑定 policy/warmup；正式入口 TPU-only 且拒绝非 clean mode；数据为 ImageNet/iNaturalist，模型为 ImageNet ResNet50/101；旧绘图将 method=sgd 直接标成 SGD，新增 Adam 后必须按 optimizer+method 区分。
- **待授权改造范围：** 配置/父子 CLI/元信息、标准 Adam adapter、CIFAR 小图数据/模型与固定污染、历史 reference 的纯函数状态、checkpoint 恢复校验、分组评价/独立 CSV 与报告。reference 的 H/count 独立于 Adam moments；两者只在真实训练更新时提交。全局 batch 统一历史；编译 warmup、评价、反事实不推进状态。旧不兼容 theorem/diagnostic/mechanism 不简单解禁复用到 Adam。
- **实施与实验顺序建议：** 先普通 Adam+污染数据+分组评价闭环，再接现有 discard/flip 与 EMA；通过微型解析/VJP-JVP一致性、β=0退化、原B归一化、BN单次提交、Adam语义及精确断点恢复后进行短试跑；主实验 4组×3配对seed=12正式run。LR先做小范围普通Adam合理校准后四组冻结比较，广泛优越性另需等预算调参。少量β/时序/零噪声消融后再补SGD交替。
- **调度与未决项：** 提议把“轮”定义为 optimizer batch step，Adam 每步编辑，SGD 后续每2步编辑且三种干预统一相位，历史每步按 raw G 更新。会议未确认单位/相位，不可宣称教授指定。具体数据/模型/标签口径/β/LO/预算/硬件仍需落实，但不因此阻碍本次给出明确候选计划。
- **验证：** 只读检查上述代码接口与限制，查阅 CIFAR-10 官方说明和 Optax Adam 官方文档；未执行训练或代码测试。通过 SHA-256 保护性检查，现有 114 个 Python/TOML/shell 文件及会议原文保持不变；本次只新增方案并追加本记录。
- **未完成：** 所有实现、数据准备、烟测、正式运行、作图与实证结论均未开始；未把计划当成完成结果。原会议“下个礼拜”未转换为自动调度或任何外部操作。下一步代码实现仍须用户明确授权。

### 2026-10-28 / DPCO-0005：澄清历史 reference、梯度编辑与基础优化器的组合关系

- **授权依据：** 用户询问借鉴 Adam 构造 reference 后，对负向 gradient samples 做 flip/filter 是否已不属于原始 SGD/Adam、而是一种结合。本次仅解释算法结构与理论边界，未授权代码修改。
- **涉及文件：** 仅本文件追加理论澄清；现有代码、配置、实验计划和历史原文均不修改。
- **核心区分：** 将训练过程分为 reference 构造、样本贡献编辑、参数更新器三层。若 reference 仅被计算而不影响更新，训练算法未因此改变；当它通过权重 w 改变聚合方向 d=B⁻¹Σw_i g_i，整体训练方法一般已不同于原始损失上使用原始 batch 平均 G 的普通 SGD/Adam，但底层 updater 的公式可以保持标准形式。
- **组合定义：** 保留普通 SGD/Adam 的更新器，分别得到“历史 reference + flip/filter + SGD”和“历史 reference + flip/filter + Adam”。可作 DPCO-SGD / DPCO-Adam 的描述性候选命名，但未据此确定正式算法名或宣称新颖性。这不是必须将 SGD、Adam 两个更新器混合；借鉴 Adam 的 EMA 来评分，也不等于已经使用 Adam 做参数更新。
- **状态与方向：** reference 的历史 H 由原始 G 更新；样本权重对 filter 为0/1、对 flip 为−1/+1，零内积保持+1，负向仅表示与给定 r 冲突。送入 SGD/Adam 的是编辑后 d；Adam moments 应由 d 和逐坐标 d²更新，独立于 reference 的 H。单步没有编辑也不能自动推出与普通 Adam 的完整轨迹相同，因为已有 moments/参数可能不同。
- **目标边界：** 编辑后的 d 一般不再是原始目标梯度的无偏估计。冻结当步权重时可视为当步加权 surrogate 的梯度；由于权重依赖当前梯度和历史，不自动存在一个全程固定的加权目标。不能直接照搬原始目标上的性质，也不能将负内积样本自动称为污染或有害样本。
- **实验含义：** 同一 updater 内比较普通训练、self+discard、self+flip、历史+flip，隔离贡献处理和信号的作用；SGD 与 Adam 的组合需分别标注。reference 与 updater 的两层历史作用和额外状态应在方法说明中写清。
- **验证与未完成：** 本次是对已讨论公式和模块分工的数学澄清，无需运行训练或代码回归；只追加文档。尚无实现或新增实证结果，仍未得到普遍优越性或收敛保证。

### 2026-10-28 / DPCO-0006：展开解释当前+历史 EMA reference 的工作机制

- **授权依据：** 用户选中 DPCO-0004 对应的 G_t、H_t、r_t 原型，要求进一步阐述思路。仅授权概念解释和按协议记录，不修改实现。
- **涉及文件：** 仅本文件追加记录；既有代码、配置、其他笔记和实验结果不变。
- **定义与直觉：** G_t 为当前观察标签下的原始 batch 平均梯度，H_t=β_ref H_{t−1}+(1−β_ref)G_t，r_t=H_t/(1−β_ref^t)。展开后 r_t 是近期权重大、远期权重小的全部已观察 batch 梯度的归一化加权平均，不是只保留上一批，也不是存储历史样本重算。
- **初始化与衰减：** H_0=0；第一步 r_1=G_1。第二步 r_2=(β_ref G_1+G_2)/(1+β_ref)，体现早期权重归一化。β_ref=0 退化当前 batch 信号，β_ref 越大通常记忆越长也更滞后；正的 bias correction 不改变评分符号。旧梯度来自旧参数，不能将历史平均直接称为当前 clean gradient。
- **评分解释：** q_{t,i}=r_tᵀg_{t,i}，其符号由 β_ref H_{t−1}ᵀg_{t,i}+(1−β_ref)G_tᵀg_{t,i} 决定，综合历史趋势和当前 batch 方向；判断的是相对 reference 的冲突，不是真实污染标签。评分与权重固定后形成 d=B⁻¹Σw_i g_i，再交基础优化器。原始 G_t 写入历史，不写入编辑后的 d。
- **教学例子：** 取 β_ref=.9、H_{t−1}=(1,0)、当前两样本梯度 g₁=(−1,1)、g₂=(1.2,1)，则 G=(.1,1)、H_t=(.91,.1)。由于 bias correction 为正，可用 H_t 判断符号：当前均值给 g₁ 的分数为 .9，历史融合给 −.81。原规则保留 g₁，融合规则将其识别为冲突；flip 后 d=(1.1,0)，filter 后 d=(.6,.5)。该例仅说明历史如何改变选择，不证明该选择对真实目标更好；若正确目标主要沿第二坐标下降，flip 反而可能有害。
- **数学与经验边界：** flip 保证 rᵀd=B⁻¹Σ|rᵀg_i|，filter 保证 rᵀd=B⁻¹Σmax(rᵀg_i,0)，因此相对原 batch 均值不降低 reference 投影。但这不等于改善 clean 目标或实际 Adam 更新，尤其不能把稳定的历史含噪梯度当作无偏 clean 信号。降噪/有用信号时间一致性的解释是待实验检验的机制假设。
- **状态区分与验证：** reference 的 H 来源于 raw G；Adam moments 来源于编辑后 d，二者独立。通过精确有理数计算复核示例的均值、EMA、评分、flip/filter 聚合和 reference 投影恒等式；未运行训练、修改代码或声称实验有效。

### 2026-10-28 / DPCO-0007：reference 与 Adam 衰减超参数的取值说明

- **授权依据：** 用户询问“两个 beta”是否为超参数、应如何取值以及 Adam 是否需要指定 beta。本次仅解释与提出候选设置，不授权修改代码或实验配置。
- **涉及文件：** 仅本文件追加研究记录；实现、配置和既有实验计划不变。
- **参数区分：** reference 公式中的 β_ref 和 (1−β_ref) 互为补数，只有一个独立参数；若底层采用 Adam，另有一阶矩 β₁ 和二阶矩 β₂，合计三个独立衰减超参数。reference 由 raw G 更新，Adam moments 由 edited d 更新；同取 .9 不表示同一状态或必须绑定。
- **默认值与来源：** 核对 Optax Adam 官方文档 `https://optax.readthedocs.io/en/latest/api/generated/optax.adam.html`，默认 b1=.9、b2=.999。构建 Adam 时这些值必然确定，但可由库默认提供，不要求每次手工传入；可复现实验应显式记录实际值。
- **候选设置建议：** 首轮所有 Adam 组统一固定 β₁=.9、β₂=.999，仅考察 β_ref∈{0,.5,.9}；.9 为主候选，0 复用 self+flip 对照，.5 为较短记忆消融。取值建议而非教授指定或已证明最优，不同时搜索三类 beta。后续若有依据再研究更长记忆或优化器 beta。
- **直觉与限制：** EMA β∈[0,1)，记忆时间尺度粗略为1/(1−β)，.5/.9/.99约对应2/10/100步量级，不是严格有限窗口或平均年龄的等式。较大β更平滑也更滞后，较小β更敏捷也更依赖当前噪声；本原型将其作为固定配置，不通过普通参数反向传播自动学得。
- **选择与验证边界：** 在固定污染manifest、相同optimizer/学习率预算下，用干净验证表现及固定分组曲线比较候选，测试集不参与选beta；报告相邻beta与配对seed的敏感性，不把默认值视为普遍最优。本次仅核对文档与数学含义，未运行训练、代码测试或改变实际参数。

### 2026-10-28 / DPCO-0008：结合现有 ImageNet/iNaturalist 框架调整含噪数据集建议

- **授权依据：** 用户认为 CIFAR-100 相对简单，询问近期常用、难度较高的含噪数据集，并说明近期已使用 ImageNet 和 iNaturalist。本次仅进行文献核查、数据选择建议及记录，未授权数据下载、实现或训练。
- **涉及文件：** 仅本文件追加研究建议；既有 CIFAR 计划作为先前候选保留，不改代码、配置、原数据和旧结果。
- **近期使用证据：** 核查 ICCV 2025《Joint Asymmetric Loss for Learning with Noisy Labels》原论文/作者官方代码，仍采用 CIFAR/CIFAR-N、WebVision、Clothing1M。AAAI 2025《Revisiting Interpolation for Noisy Label Correction》也列 CIFAR、TinyImageNet、WebVision、Clothing1M。可说明这些基准仍在近期相关研究使用，不据有限论文给出全领域流行度排名，也不把数据集创建年份等同于是否仍有研究价值。
- **数据类型区分：** 大规模/细粒度分类难度、真实标签噪声、人工可控标签污染是不同轴。ImageNet/iNaturalist 不能仅因分类困难就当作已知 clean/corrupted 划分的真实噪声基准；合成污染可明确“是否被本实验改标”，不保证未改标样本原注释全部正确。图像损坏/分布外测试也不同于本轮训练标签噪声。
- **推荐优先级修订：** 鉴于用户已有大图训练和数据框架，首选复用固定 ImageNet-100 类别 manifest、ResNet-50/既有输入设置，增加可复现训练标签污染；建议0%控制及20%/40%候选，先完成一个预定污染率下四组Adam闭环，再扩展。此为实验设置建议而非已经选定/运行。自定义 Noisy ImageNet-100 应报告100类清单、split、污染机制/比例/seed，不宣称它是唯一统一的公开标准切分。数据/模型阶段只调整计划，不同时添加其他机制。
- **后续困难任务：** 保留当前 iNaturalist 2021 子集，作为细粒度/多类别扩展，可另加固定合成标签污染。当前项目文档/配置为 full-train 比例抽取140k训练、20k验证、10k类（训练平均14张/类，验证2张/类），并非官方500k train_mini；本次只核对配置与协议，未重新核验实际数据或训练结果。高污染下少样本类别支持更少，建议分组报告污染前后类频率及按训练频率分层的效果，避免把少数/困难类梯度与噪声混淆。历史参考偏向频繁类是待验证风险，不是本次证明或实测结果。
- **iNat版本边界澄清：** iNat2021官方说明10k物种、约2.7M全训练、500k mini，明确其不一定聚焦long-tail；不能笼统把所有年份/子集称为同一种极端长尾基准。当前子集保留原类比例，实际不平衡程度仍应以manifest统计，不作未经核查的断言。
- **真实噪声候选：** WebVision1.0（原论文约2.4M网页图像、1k ImageNet语义类）或常用前50类Google Mini-WebVision，适合后续与ImageNet类别对接的真实网页噪声验证；Clothing1M为大规模服饰网页标签噪声基准，类别数不能当作整体难度排名；Food-101N约310k图像/101类，提供部分人工正确性核验标签，适合固定核验子集上的clean/noisy行为分析。Food-101N正确性标记并不自动提供所有错误样本的正确类别，也不覆盖全部样本。
- **对教授目标的适配：** 第一阶段需要精确控制分组和原标签视图，因此更适合现有ImageNet-100加固定合成污染；真实噪声数据一般不能直接得到全体训练样本的可靠clean/corrupt真值。第二阶段按有核验标签的范围作分组分析，并用独立人工标注验证/测试集评价。若选Food-101N，仅能在其核验范围内声称识别真实噪声，不能把二值核验当成纠正后的类别标签。
- **来源：** ICCV2025作者代码 `https://github.com/cswjl/joint-asymmetric-loss` 与论文 `https://openaccess.thecvf.com/content/ICCV2025/html/Wang_Joint_Asymmetric_Loss_for_Learning_with_Noisy_Labels_ICCV_2025_paper.html`；AAAI2025 `https://ojs.aaai.org/index.php/AAAI/article/view/35489`；WebVision原论文 `https://arxiv.org/abs/1708.02862`；Food-101N作者项目 `https://kuanghuei.github.io/Food-101N/`；iNat2021官方协议 `https://github.com/visipedia/inat_comp/blob/master/2021/README.md`；本地 `docs/inaturalist_subset.md` 与现有数据配置。核查日期2026-10-28。
- **验证与限制：** 仅查阅原始论文、作者/数据集官方材料和现有配置；未测量硬件成本、未进行下载可用性全流程验证、未复现实验、未统计数据集使用频次。没有修改代码、实际污染标签、种子或实验预算；下一步实现仍需用户明确授权。

### 2026-10-28 / DPCO-0009：澄清 batch-self 对照与历史信号主方法的定位

- **授权依据：** 用户标注原四组表，确认 A 是否普通训练，询问 B/C 的 self 是否指 batch 内 self，并强调已有实验中 batch 内 self 效果差，应考虑借鉴 Adam 的历史+当前信号。本次只澄清定义和研究定位，未授权代码或配置变更。
- **涉及文件：** 仅本文件追加记录；原四组计划与已有结果保留，不擅自重新命名、改动实现或启动新实验。
- **定义确认：** A 是未经样本贡献编辑的标准 Adam 训练；B/C 是用当前 batch 共同平均 G_t 评分 q_i=G_tᵀg_i，再分别 discard/flip。这里 self 不是 g_iᵀg_i，也不是已经包含历史。原 D 才是当前+历史 EMA reference 下的 flip。
- **实验定位澄清：** 原表是对照设计，不代表四个同等优先的新算法。B/C 用作原有 batch-self 方法和“去掉历史”的对照；本轮待开发和验证的主方向是历史+当前信号。对当前 EMA 原型，β_ref=0 恰好退化为当前 batch reference，故这些对照有助于隔离历史的额外作用，不意味着继续以优化 batch-self 为研究重点。
- **可选扩展及数量：** 若同时评价历史 reference 的 filter 与 flip，两种新方法应分别定义为 EMA+filter、EMA+flip。它们与 plain Adam 构成三组核心方法；若同时保留原 batch-self 的 filter/flip，则完整设计是五组，不能把 B/C 改成历史版后仍声称旧 D 是不同的第四组。该五组/分阶段安排仅为澄清后的候选，不代表用户已确定新增运行预算。
- **已有负结果边界：** 接受用户报告的既有 batch-self 负结果；本次未复核实验数据。若已有数据/污染、优化器、模型、预算及评价口径与新实验一致，可复用作为对照；若从旧 SGD/无污染设置切换到新 Adam/含噪任务，不能直接用旧结果代替匹配对照，也不能因此断言在所有设定下一定失败。
- **验证与限制：** 核对本轮表格及 EMA 的 β_ref=0 代数退化关系；无新经验结论，无代码测试、实现修改或正式训练。

### 2026-10-28 / DPCO-0010：用户确认先聚焦三组 Adam，SGD 后续考虑

- **授权依据：** 用户标注普通 Adam、EMA+Filter+Adam、EMA+Flip+Adam 三组并表示“可以先关注这三个，再额外考虑sgd”。这是实验范围和优先级的确认，不是修改代码或启动训练的授权。
- **当前主线：** 首轮聚焦普通 Adam、历史+当前 EMA reference 下的 Filter+Adam、相同 EMA reference 下的 Flip+Adam。后两组仅在负分数样本的处理方式上不同，reference 构造/衰减、原B归一化和其他设置保持一致，以便解释 filter/flip 的差异。
- **阶段安排更新：** 原四组/五组表保留为历史讨论；当前三组主实验优先，batch-self(β_ref=0)作为后续消融，不自动列入首轮。SGD 后续额外考虑，届时再确定仅普通SGD对照还是对应历史编辑组合，不据此自动扩展为六组或增加正式运行预算。
- **结论范围：** 三组主实验回答历史reference与编辑的整体组合是否改善普通Adam，以及filter/flip哪种更合适；若要单独归因于历史而非样本编辑本身，仍需后续β_ref=0等消融。此前数据集、β、学习率和seed数量建议未因本次范围确认变成已批准执行参数。
- **涉及文件与验证：** 仅本文件追加范围决策；未修改代码、配置、其他方案文档或实验结果，未下载数据、运行测试或启动训练。核对三组定义和实验归因关系，待用户后续明确实现授权。


### 2026-10-28 / DPCO-0011：实现三组 Adam 对照及可配置负 alignment 权重

- **授权依据：** 用户明确要求“按照这仨组先完成代码修改，方法名叫做dpco，然后对dpco找出来的负align再有参数控制filter和flip……参数可以用-1或0这种，以后还可以直接类似权重的形式修改”。本次授权覆盖 DPCO-0010 确认的普通 Adam、EMA+Filter+Adam、EMA+Flip+Adam 的方法/更新器、必要配置与启动/恢复/记录链路及本地验证。它是后续新增的明确实现授权，取代此前这些功能处于“待授权”的状态；不扩展为正式训练、数据下载或所有旧实验的重构授权。
- **目的与命名：** 主方法保存为 `method.name="dpco"`、`reference.name="ema"`；filter/flip 由同一个 `method.negative_weight` 控制。普通基线保存为 `method.name="adam"`、`training.optimizer="adam"`。启动别名 `dpco_filter` / `dpco_flip` 只方便排列三组，并不生成两个独立实现。旧 `dpco_e` / `dpco_l` 等入口仍表达历史算法，不能把旧结果重新解释为当前历史 reference 算法。
- **核心实现：** 新增 `src/methods/dpco_history.py`，使用 observed-label 普通损失的原始有效全 batch 平均 G_t，维护 H_t=β_ref H_(t−1)+(1−β_ref)G_t、H_0=0，r_t=H_t/(1−β_ref^t)，包含当前 batch。仅当 q_i=r_tᵀg_i<0 时赋予 `negative_weight`，否则权重为1；有效样本数 B 不随 filter 改变。无效 padding 权重0，零 alignment 保留。评分/权重按 stop-gradient 处理。JVP 后端用 VJP/JVP 避免训练时构造 B×P Jacobian；audit 后端保留用于独立校验。模型状态只提交一次正常 forward 的结果。
- **权重语义：** 0 为 filter/discard；−1 为整向量 flip；−.5 为半幅反向；.5 为半幅保留；1 为普通贡献对照。接受任意有限实数，不自动裁剪、不按剩余样本重新平均。非有限数和布尔值拒绝；固定 filter/flip 别名与显式冲突权重同时给出时拒绝。权重1的多步轨迹已验证与普通 Adam 一致。filter 指 forward 后的贡献置零，仍参与该 batch 的 BN 统计。
- **Adam 与状态：** `src/training/updates.py` 增加基于 Optax `scale_by_adam(eps_root=0)` 的标准 Adam adapter，一/二阶矩分别接收编辑后 d_t 和逐坐标 d_t²，偏差修正、epsilon 在平方根外；不是每样本梯度平方的均值，也不是 AdamW。reference 的 H 独立保存且只接收 raw G。保留已有 LR schedule 与默认关闭的 kernel-only coupled L2；L2 在编辑后、Adam moments 前加入，不写入 H。新增 Optax train/test 依赖，使用本机已安装 0.2.8 验证，未安装或升级本机环境。
- **启动与配置：** `src/config.py`、`src/cli.py`、`src/training/launch.py`、`scripts/launch_tpu.py`、`scripts/train_classification.py` 接通 `--method adam/dpco`、`--negative-weight`、`--reference-beta`、Adam 两个 beta/epsilon 和 optimizer。主三组共用 Adam 配置；父 launcher 和子 worker 都接收全部参数。新增独立 `configs/tpu/dpco/imagenet100_resnet50.toml`，不改旧 preset 的学习率/算法；β_ref=.9、Adam(.9,.999,1e−8)、LR=.001、100步仅为未调优 pilot，可被覆盖。现有 ImageNet/iNaturalist 模型与数据入口复用；本次不增加 SGD 正式实验网格。
- **恢复与记录：** `src/training/experiment.py` 在编译前初始化 H/count 和 Adam 状态，恢复时先检查类型、累计步数、树结构、形状、有限性与二阶矩非负，再 rewind CSV。参数权重/beta 改变不能覆盖恢复同一实验。旧元信息缺少新增字段时按旧默认值比较，保留原 metadata 字节；缺失新算法必要状态时明确失败，不静默从零继续。warmup candidate 丢弃，评价不推进历史。`src/training/trainer.py` 为新状态增加有限性检查；仅 EMA run 添加 `dpco_steps.csv`，保留旧 stream/cursor 语义；记录 negative/edited count、权重、历史步数、norm、cosine 和 reference gain。目录/status 标签区分 beta、权重和 Adam，metadata 保存全部参数。
- **理论边界：** 延续 DPCO-0004/0006 的当前+历史原型，而非复现教授尚未提供细节的 MNIST 算法。β_ref=0 退化当前 batch reference；第一步 r_1=G_1。正偏差修正不改变 sign。对于负样本权重≤1，rᵀ(d−G)≥0 是代数投影性质；权重>1甚至不必满足它。该量不代表 clean-gradient 增益或 Adam 实际下降保证，也不把负 alignment 认定为错误标签。EMA 不能自动消除标签偏差。靠近1的 beta 使用 Python 标量 log 与 expm1 避免 FP32 的 1−β^t 消减问题；实验仍需检查数值有限性。
- **涉及文件：** 新增 `src/methods/dpco_history.py`、`configs/tpu/dpco/imagenet100_resnet50.toml`、`tests/test_dpco_history.py`、`docs/dpco_adam.md`。修改 `src/methods/__init__.py`、`src/config.py`、`src/cli.py`、`src/training/{updates,trainer,experiment,launch,recording,results,status}.py`、`scripts/{launch_tpu,train_classification,plot_training_results}.py`、`pyproject.toml`、`README.md`、`tests/{local_mesh_check,test_config,test_updates,test_plot_training_results}.py`，并追加本文件。旧绘图入口增加 Adam 拒绝检查，避免将 uniform+Adam 标成 SGD；未重写其历史图表与结果。
- **验证与修正过程：** 首轮旧209项回归仅有 method 枚举测试因新增 Adam 必须搭配 Adam updater 而失败；补齐测试的正确配置。新增独立零 reference 检查曾使用1/6相消，被 FP32 残差影响；改用可精确表示的整数梯度测试严格零，不引入 alignment 容差或改变算法。新增19项测试全部通过；之后全量 **228项 CPU 回归通过**（86.931秒），包含多步 NumPy EMA/Adam 独立递推、0/−1/任意权重、β=0退化、零/正分数、padding、audit/JVP、真实微型 ResNet BN 单次提交、三组真实入口 CPU fixture、编译不消耗状态、完整恢复/坏状态拒绝、父子参数一致、dry-run 不导入 JAX/Optax/Flax、双 CPU 设备全局历史与 Adam moments。全量后扩充已有两项检查，再次通过旧 metadata 缺失所有新字段的精确恢复与旧绘图对 Adam 的拒绝检查。98个 Python 文件 AST、所有配置 TOML 解析、`git diff --check` 通过；三组 dry-run 和自定义−.5配置检查通过。测试仅使用临时目录和合成 fixture，未把测试 loss 视为实证改进。
- **未完成项与证据限制：** 当前完成的是三组方法/优化器代码与现有真实数据入口的接通。尚未实现讨论方案中的固定噪声标签注入、污染 manifest、clean/corrupted 分组 CE 或三组新报告绘图；现有入口仍只接受 `data.mode=clean`（表示没有额外注入，不认证原始标签绝对无误）。没有下载数据、启动正式训练、进行 TPU 硬件/吞吐/内存实测、调参、得到准确率优势、提交或推送。所有既有未提交研究工作、原始实验结果与历史记录保持；后续实现按用户指定范围继续授权。


### 2026-10-29 / DPCO-0012：面向 noisy dataset 的受控验证选型建议

- **授权依据：** 用户报告已在服务器 `/home/jason_chia925_gmail_com/Project_DPCO/DPCO` 整理代码，当前要挑选 noisy dataset 并按教授要求做 control verification。本轮是选型与研究设计讨论，不构成新增代码、下载数据或启动实验的明确授权；仅按协议追加本记录。
- **来源核对：** 重读用户提供的《教授周会_10.27_新项目实验重点总结.md》及当前本地训练入口。会议明确关注固定 clean/corrupted 子集上的行为，未指定数据集、污染比例或精确 EMA 公式。当前三组仍按后续用户确认的普通 Adam、历史 DPCO filter、历史 DPCO flip；不把原会谈 batch-self 两组当作当前主线。未连接或核验服务器文件版本，终端截图只提供工作路径。
- **选型建议：** 第一阶段复用现有 ImageNet-100 及 ResNet-50，先把 noise 明确限定为训练标签噪声，固定样本 ID、原始标签、观察标签和注入标记；只改训练标签，不改图片与验证标签。对选定的约/精确40%样本从其他99类均匀选择新标签，保证实际发生改变并记录实际改标数量/比例、映射版本和哈希。40%与0%是本轮建议，非教授指定、非已执行参数。未改标子集/原标签仅作为相对原始标注的控制，不能认证 ImageNet 原标签绝对正确。
- **真实噪声备选：** 官方 Controlled Noisy Web Labels 提供 Blue Mini-ImageNet（合成）、Red Mini-ImageNet（真实web噪声）及 Stanford Cars 两种版本；官网描述每图3–5名标注员、可控0–80%噪声级别、共享clean验证集与 is_clean 字段。因此 Red Mini-ImageNet 可作为需要现成真实噪声及clean/corrupted标记的补充，不能默认每个错误样本都带有可计算原正确类别CE的标签。官网 https://google.github.io/controlled-noisy-web-labels/ 。本次仅查阅官方描述，未下载、检查数据文件或确认所有图像URL仍可取回。也核对 Clothing1M 作者仓库 https://github.com/Cysu/noisy_label ，不因其训练集有噪声就推断每个样本有经核实的真标签/污染标记。
- **规模与归因：** 第一阶段在可控 ImageNet-100 上建立机制闭环；更大 ImageNet-1K 和已有 iNaturalist 全类别比例子集可作为后续扩展。iNaturalist 的类别不均衡/稀有类与标签噪声是不同因素，类别多、样本难或梯度冲突不自动代表标注错误；先避免把它们同时混入首个归因实验。此选择依据现有代码适配与控制目标，并非“最流行”或“最难”的排行榜断言。
- **评价与公平性：** 三组共享污染manifest、初始化/训练seed、batch顺序、增强、模型和合理校准后冻结的Adam设置/预算；污染seed与训练seed分离。固定未改标子集看原标签普通CE；固定改标子集同时看观察错标签CE和原标签CE；另看未额外加噪验证集CE/accuracy。评价不使用各方法signed/weighted surrogate，不动态按模型评分重新定义clean组。注入标记与原标签不能用于训练评分、reference或权重，避免oracle泄漏。评价使用固定无随机增强的eval方式及相同BN口径。
- **成功判据与额外观察：** 改标子集的错标签CE升高仅说明更少拟合该标签，不能单独判定DPCO有效；需同时检查未改标子集及未加噪验证集是否改善、改标子集原标签预测是否改善。分组记录负alignment/干预比例，检查是否大量误伤难而未改标样本。负alignment不等同噪声检测器。只有三组主对照仍不能把收益单独归因于历史；β_ref=0为后续消融，不自动扩首轮网格。
- **候选运行顺序：** 3方法×2噪声级别(0%,40%)×1训练seed=6组作为初步闭环；稳定后3训练seed共18组，固定污染实例以隔离训练随机性。更换污染seed、20%中间强度、非对称/实例依赖噪声及真实噪声为后续扩展。先验证普通Adam训练预算足以表现学习/记忆行为；当前100步pilot不自动构成完整实验预算。所有数量均是建议，未创建运行任务。
- **实现边界与未完成项：** 本地 `scripts/train_classification.py` 仍拒绝非clean data.mode，尚无固定注入manifest、原标签保留/评价视图、分组普通CE或分组干预率。不能只把参数改成noisy就声称已开展该受控验证。后续实施需要用户明确代码授权。此次仅追加本文件，无源代码/配置/依赖变动，无下载、训练、提交、推送或新经验结论。


### 2026-10-29 / DPCO-0013：核对公开 ImageNet 衍生噪声基准，明确 CNWL 与现有 ImageNet-100 的区别

- **授权依据：** 用户追问“imagenet-100是不是已经有带噪声的标准数据集”。本轮仅查证公开基准、修订选型解释并追加研究记录；不授权代码改动、下载数据或训练。
- **查证结论：** 存在公开的100类 ImageNet 衍生可控标签噪声基准，最直接相关的是 Controlled Noisy Web Labels (CNWL) 的 Red/Blue Mini-ImageNet，出自 Jiang 等 ICML 2020《Beyond Synthetic Noise: Deep Learning on Controlled Noisy Labels》。不能断言用户具体记忆必然是它，也不能把它直接等同当前项目自定义类别清单的 ImageNet-100。检索还发现论文各自构造的 noisy ImageNet-100 设置，名称相似并不能保证数据/类别/噪声协议一致；不将未检出唯一命名版本当作证明不存在其他版本。
- **一手来源：** 数据集 https://google.github.io/controlled-noisy-web-labels/ ；论文 https://arxiv.org/abs/1911.09781 ；TFDS官方目录 https://www.tensorflow.org/datasets/catalog/controlled_noisy_web_labels ；作者介绍 https://research.google/blog/understanding-deep-learning-on-controlled-noisy-labels/ 。只读公开描述，未下载数据或执行TFDS。
- **可核对的协议：** TFDS明确提供 `mini_imagenet_red`（真实web噪声）、`mini_imagenet_blue`（合成标签噪声）；100类、84×84图像、十个0%–80%训练split及共享5000张clean validation。Red每级约5万训练图（train_40列为50010），Blue每级60000。输出含id/image/label/is_clean，可按is_clean固定clean/corrupted组。按官方说明需手工准备原始ImageNet档案与web图片；元数据压缩包大小不等于完整图像数据已经可用，未确认所有旧web URL当前可取回。
- **选型解释修订：** DPCO-0012已提及Red Mini-ImageNet备选，但上一轮把自行给现有ImageNet-100加噪作为首选，未充分展开现成公开基准的意义。如果优先条件是现成公开噪声级别与clean/corrupted标记，应优先核验CNWL Red Mini-ImageNet的获取和适配；自行加噪仍是方便保留完整原标签、精确追踪改标的控制方案，并非唯一方案。没有宣称CNWL是当前项目同一类别清单的即插即用换标签文件。
- **控制目标的重要区别：** 作者说明Red通过将部分原图替换为带错误web标签的图片形成污染，可能含目标100类之外的物体；它不是始终保持同一张图只改变标签。TFDS仅列label与is_clean，不能推断每个corrupted样本都有100类内的修正标签。因此原标签CE对所有Red噪声样本未必有定义/可计算；可先比较clean CE、corrupted observed-label CE与共享clean validation，另外单独审定是否存在修正标签。三方法必须共用同一个train_40的固定样本；不同噪声split中clean成员未必相同，不能直接当成同一固定子集排序。
- **验证与限制：** 核对上述官网、官方数据目录、原论文页面与作者说明；未独立复核原始注释、训练/验证成员交集、真实可下载图像数量或类别与当前manifest的对应关系。无源代码/配置/依赖变化、无测试训练、无下载/提交/推送；本轮仅本文件追加记录。


### 2026-10-29 / DPCO-0014：讲解 CNWL/MentorMix 论文并筛选其他含噪数据集

- **授权依据：** 用户标注 Red/Blue Mini-ImageNet 的介绍，表示可以使用，要求先讲论文在做什么、为何加噪，再调查其他数据集。该表态接受候选数据集，不等于授权下载、实现适配或启动训练。本轮仅文献分析、选型和本记录追加。
- **论文阅读：** 阅读 Jiang等 ICML2020《Beyond Synthetic Noise: Deep Learning on Controlled Noisy Labels》PMLR正文（12页，含参考文献）和补充材料（10页），并核对作者Google Research说明、数据集官网。来源 https://proceedings.mlr.press/v119/jiang20c/jiang20c.pdf 、https://proceedings.mlr.press/v119/jiang20c/jiang20c-supp.pdf 、https://research.google/blog/understanding-deep-learning-on-controlled-noisy-labels/ 、https://google.github.io/controlled-noisy-web-labels/ 。使用网页/PDF文本读取，未向项目下载论文或数据。
- **三项贡献及加噪目的：** 提供可控制强度的真实web标签噪声基准，提出MentorMix，并研究不同噪声分布/模型/初始化下的行为。数据构造的标签错误是实验中的受控因素，目的是检验鲁棒性及人工随机噪声结论的可迁移性；不应解释为“故意给数据错误监督以提升模型”。这与方法中的Mixup正则化是不同层次。
- **Blue与Red：** Blue保留图像并以受控比例将标签换成其他类；正文明确排除换回原正确标签。Red通过搜索收集web候选、去除验证近重复、3–5人核验标签正误、用经确认的错标web图替换部分原图而保留类别标签。标签正误人工信息用于构造/评价，不输入算法训练；Red可能包含目标类之外的内容，也引入图像分布变化，不是严格只对同一x改y的干预。补充材料对纯web图与去除image-to-image检索的构造变体另作检查。Blue/Red训练样本量也不同，不宜把两者任何数值差异完全归因于标签机制。
- **教学分解（本次说明，非论文新定理）：** 对固定clean集合C、corrupted集合N及rho=|N|/(|C|+|N|)，普通未加权训练目标精确分解为 L_obs=(1−rho)L_C+rho L_N，其中L_N使用观察到的错误标签；其梯度作同样分解。普通训练会试图同时降低两部分的观察标签CE，但错误标签CE下降不等于真实任务改善。用易懂的动物错标例子区分均匀随机错标与视觉相近/实例依赖错标。对于Red的open-set样本，不假设存在已提供的任务内正确类别。
- **MentorMix机制：** 正文Algorithm1先用普通样本loss和batch loss分位数的EMA阈值计算简化MentorNet二值可信权重，再以softmax权重偏向选择小loss伙伴、执行图像和one-hot标签的Mixup；lambda依据原样本可信度分配较大/较小混合比例，混合后可选择再次加权。不是零权重伙伴采样概率必然为零，也不是必须额外训练一个大型教师。Mixup公式为x_mix=lambda*x_i+(1−lambda)*x_j、y_mix=lambda*onehot(y_i)+(1−lambda)*onehot(y_j)。这里的EMA平滑标量损失阈值gamma；不等同DPCO原始梯度向量EMA，方法不使用负权重整梯度flip。
- **结论与证据边界：** 文中实验发现真实web噪声在其设置下通常比随机噪声造成更小退化，真实噪声上peak到final差值可能很小、早停收益不如随机噪声稳定，预训练架构的微调表现也有相关性。作者提出视觉/语义相近等解释，但不是普适定理，不能写成噪声有益、模型总先学clean后记noise、或一定支持DPCO。其主要评价包括clean validation的peak和final accuracy，并不证明clean CE必降/错误标签CE必升；教授要求的固定两组CE需单独实现。当前三组Adam试验也不能单独识别历史的净贡献，仍需后续beta_ref=0消融。
- **备选与控制信息核对：** CIFAR-100N（ICLR2022，100类、5万训练、32x32）提供原标签与真实人工噪声标签，能相对原标签明确划分一致/不一致，适合机制核验；需严格匹配PyTorch/TFDS图像顺序，原标签仍可能有歧义。Food-101N（CVPR2018，101类约310009图、估计20%噪声）有52868训练图和4741验证图的verification标签，仅核验部分可用于可信clean/corrupted观察，未知标签正误不能当clean。CNWL Red Stanford Cars（196类、8144训练）提供另一细粒度可控web噪声任务。Clothing1M（14类、约百万noisy图）有额外clean标注集合，不能把它等同全量noisy训练样本都有正误真值。WebVision1.0（1000类、超过240万图）适合扩大真实web噪声训练规模，官网的clean验证集不代表训练集有全量污染掩码。Animal-10N（10类、5万训练/5000测试、64x64）的约8%是估计，官网明确全量训练真值未知，不列为首轮分组机制验证优先项。
- **备选一手来源：** https://github.com/UCSC-REAL/cifar-10-100n 及 https://www.tensorflow.org/datasets/catalog/cifar100_n ；https://kuanghuei.github.io/Food-101N/ ；https://www.cv-foundation.org/openaccess/content_cvpr_2015/papers/Xiao_Learning_From_Massive_2015_CVPR_paper.pdf ；https://data.vision.ee.ethz.ch/cvl/webvision/dataset2017.html ；https://dm.kaist.ac.kr/datasets/animal-10n/ 。未把搜索到的非官方汇总页或过往SOTA名次当作最终推荐依据；未验证所有实际下载渠道。
- **本轮建议而非新执行决定：** 用户已接受的CNWL Red Mini-ImageNet继续作为主候选；若要补最直接的样本级机制核验，CIFAR-100N可作为低成本辅助，不强迫将其替换为主数据集；更大且有部分正误核验的Food-101N适合后续真实数据扩展。全量WebVision/Clothing1M更多回答规模下的泛化，不能替代完整clean/corrupted机制观察。不得因“noisy”名称就以模型loss/负alignment反过来定义评价真值；核验信息仅供评价，不进入reference/weight。
- **涉及文件、验证与未完成：** 仅本文件追加。本次是纸面公式与官方数据接口核对，不运行代码测试；未修改源代码/配置/依赖，未下载数据、连接服务器、训练、提交或推送。数据成员、图像URL实际可取回率、预训练与评价划分是否有重叠仍需落地前核验；未宣称DPCO已在这些基准有效。


### 2026-10-29 / DPCO-0015：建议先用 CIFAR-100N 建立固定样本的机制验证

- **授权依据：** 用户询问是否应先使用“cifar-100N这种官方的”数据。本轮仅研究选型澄清，不授权代码、下载或训练；仅本文件追加。
- **优先级解释：** 建议针对教授当前固定clean/corrupted机制观察先做CIFAR-100N，再用CNWL Red Mini-ImageNet验证真实web场景。理由是前者同一图片保留原标签和人工噪声标签，可定义完整、固定的对照并计算改标子集对原类别的CE，不是因为“官方”必然比其他公开基准更有效。CNWL同样是论文作者公开发布的正规基准；不要求所有研究必须从CIFAR开始。此为当前目标下的建议修订，非用户已明确选择/启动。
- **一手来源核对：** https://github.com/UCSC-REAL/cifar-10-100n 为ICLR2022作者正式发布；https://www.tensorflow.org/datasets/catalog/cifar100_n 明确同一原CIFAR-100训练图另有人工标注、字段label/noise_label、5万训练、32x32。作者同时提供PyTorch与TFDS顺序映射，不能混用数组顺序。所谓官方指噪声基准作者发布，不是原始CIFAR标注绝对正确的保证。
- **分组与训练：** 以原标注y和发布人工标签y_tilde定义C={i:y_tilde_i=y_i}、N={i:y_tilde_i!=y_i}，全程固定。三方法训练都使用同一人工噪声标签，C/N和原标签仅供评价，不能输入reference、过滤或翻转权重。分组相对官方原标注定义，不排除原标注歧义。记录C组原标签普通CE、N组人工标签CE、同一N组原标签CE，以及不额外改标测试/验证表现，联合解释而不是只奖励N组观察标签CE升高。
- **噪声口径更正：** 第一轮使用发布的人类噪声标签，噪声率由该文件与原标签逐样本比较得到；不重新随机制造40%或把固定发布版本误称可任意设置噪声强度。若补全原标签训练对照，两种训练使用同一图片和原CIFAR-N文件定义的固定C/N观察组，有助于控制图像因素；不得据此自动增加正式运行预算或用测试集选超参数。
- **实现边界与未完成：** 当前项目仍需CIFAR-100N标签/图像顺序校验、32x32数据/模型适配和分组评价，不能只把ImageNet配置dataset名称改成CIFAR就启动。未更改源代码/配置/依赖，未下载、运行训练、连接服务器、提交或推送。无新增实验结论，未承诺DPCO在CIFAR-100N有效。


### 2026-10-29 / DPCO-0016：实现官方 CIFAR-100N 下载、标签模式与 DPCO+Adam 完整接入

- **授权依据：** 用户明确要求“按照cifar100n的官方接口模式，参照imagenet的代码文件架构，完成cifar100n的代码，包括下载加载数据，按照官方接口的释义来定义noise 百分比参数等，然后接入现有dpco的adam训练流”。本次授权覆盖数据准备/下载/加载、必要的小图模型、配置/启动、固定分组评价与本地验证；不授权正式训练、修改既有DPCO/Adam数学规则、提交或推送。
- **起始状态与保护：** 工作开始时仓库HEAD为 `2d6ec52`，仅本文件存在用户研究讨论追加记录；保留这些记录和原有结果。所有实现位于DPCO目录；真实源数据与测试产物放在 `/private/tmp/`，未纳入Git、未覆盖服务器数据、未连接服务器或操作远端。
- **官方依据与版本：** 查阅并获取作者ICLR2022发布仓库README、main.py、data/cifar.py、data/utils.py、data/datasets.py，固定commit `49df7d8a69e355470c77c1c2f2424916325a394b`。官方来源 https://github.com/UCSC-REAL/cifar-10-100n 、https://www.tensorflow.org/datasets/catalog/cifar100_n 、https://www.cs.toronto.edu/~kriz/cifar.html 。Python原图包使用发布MD5 `eb9058c3a382ffc7106e4002c42a8d85`；官方ordered注释NPY的SHA256为 `603b16e5f88f77a0db27ffe41b62cf59ba438da2b8bd4a085d502ad72e2b3dbf`，image_order_c100.npy为 `423c3118865b4d912ff9082423b992e43fa94ef0f503c4180bd415f915eec018`。
- **下载与准备架构：** 新增 `src/data/cifar100n_prepare.py`、`scripts/prepare_cifar100n.py`。独立plan/download/verify入口不导入JAX/Torch/TensorFlow；默认目录 `../data/cifar100n` 在代码仓库外。下载完整校验后原子发布文件，坏的既有源/缓存明确失败，不静默替换；保留失败partial（重试目前重头下载）。目录文件锁、命名tar成员读取而非extractall、非pickle的prepared NPY/NPZ、manifest/hash/complete标记保证缓存与恢复可追踪。生产准备严格检查50000训练/10000测试、原始类别均衡、像素和标签形状/范围。
- **官方接口与顺序：** 复用作者官方TFDS ordered NPY，不要求安装PyTorch。NPY键为clean_label/noise_label，与PT的clean_label/noisy_label区别明确。作者mapping满足TFDS的i对应Python的order[i]，实现转换到原CIFAR Python顺序，并逐项断言所有原标签等于原图文件fine_labels；不使用易相消的标签差总和代替逐项检查。source哈希在读取官方object NPY之前验证；运行缓存不再允许pickle。`example()`暴露id/image/label/noise_label/observed_label供审计，训练批仍只有images/labels/valid_mask。
- **noise参数释义：** 新增DataConfig及父子CLI参数noise_type(clean100/noisy100)、is_human、noise_seed、noise_percent、download。人工默认使用作者发布版本：实测20100/50000不一致，actual_noise_rate=.402，actual_noise_percent=40.2。clean100训练使用原标签，实际比例0。`--noise-percent`（别名`--expected-noise-percent`）单位0–100，是加载后实际比例的校验断言，不生成指定强度的人类噪声；不一致即报错，不忽略参数。作者旧CIFAR100构造器中的noise_rate默认.2并未参与这两条加载/采样路径，因此不能把它误当人工噪声控制。切换label模式/合成设置时清除未显式给定的人工40.2断言；clean100默认校验0。完整标签先处理并计量，再限制smoke可见样本，避免把smoke比例错作官方完整比例。
- **合成对照兼容：** `--no-is-human` 以完整原标签→人工标签的经验类转移矩阵，按作者RandomState(seed).multinomial顺序采样；默认seed0，与训练seed分离。矩阵显式行归一化，在官方每类500张上等价于原仓库广播表达式；空类fixture行设identity，不影响实际抽样。原图、类条件概率与采样顺序保持，既不独立均匀重造40%也不强制最终比例等于40.2。官方完整数据seed0实测20108/50000=40.216%。human模式非零noise_seed拒绝。实际noise_or_not/actual_noise_rate反映训练标签，分组参考mask另行保存，不混为一谈。
- **数据加载与模型：** 新增 `src/data/cifar100n.py` 的只读mmap图像、标签视图、指纹/比例和源元信息；缓存逐文件SHA256验证，关闭后读取明确失败。共享ImageBatchSource/evaluation_batches通过dataset transform分派，ImageNet/iNaturalist原处理不变。CIFAR遵照作者data/datasets.py：pad4、randomcrop32、水平flip、均值(.5071,.4867,.4408)/标准差(.2675,.2565,.2761)，评价原生32无随机增强。保持现有seed/epoch/sample顺序和augmentation恢复协议，不宣称逐次随机增强与PyTorch完全相同。新增独立 `cifar_resnet18/34` basic-block模型，3×3 stride1 stem、无初始maxpool；旧ResNet50/101不改。接口/数据语义兼容不等于复现原文整套模型/优化器训练配方。
- **DPCO+Adam接入：** 统一分类入口按数据名选择模型和reader，沿用现有任务、global batch VJP/JVP、原始梯度EMA reference、负权重0/−1及任意有限权重、标准Adam与完整checkpoint；未修改方法/Adam更新源文件。新增 `configs/tpu/cifar100n/dpco_adam.toml` 与 `run_cifar100n_suite.sh`，默认三组adam/dpco_filter/dpco_flip顺序worker0运行。新preset为未调优100步pilot、B128、LR.001、FP32、beta_ref.9、Adam(.9,.999,1e−8)，不是正式基准预算。增加新数据参数的父子命令透传、dry-run元信息、配置检查、数据/模型切换校验和run-name中的clean100/noisy100与human/synthetic区分。data extras增加必要NumPy/Pillow/certifi，不升级本机训练环境。
- **固定分组评价：** 新增GroupedEvaluation及CIFAR构造器，在固定参考噪声标签相对原标签定义的C/N上，记录clean原标签CE、corrupted_noisy参考噪声标签CE、同一corrupted_original原标签CE（含top1/top5）。human参考为发布人类标签，synthetic参考为同一固定seed生成标签；clean100训练对照也保留同一参考分组和评价目标，便于比较相同图片。状态不提交、BN使用eval统计、padding按有效数量加权、空组计数0且指标留空。group_evaluation.csv为新私有stream，断点恢复同步rewind。评价时间包括分组开销。原标签与mask仅在审计/评价读取，不进入训练评分和reference。
- **官方test口径：** CIFAR原始接口只有train/test，没有另一个官方validation；metadata明确common evaluation/summary的val_*字段在此对应官方test监测，为兼容保留列名。CIFAR GroupedEvaluation关闭自动按该test挑best，故不生成best slot；fixed-budget/final保留。并未藉此声称用户看过曲线调参后仍是盲测，正式超参数选择需要另立验证协议。ImageNet原有best逻辑不变。
- **恢复兼容：** 指纹包含prepared manifest、训练/参考标签哈希、噪声模式/seed和smoke view；mode变化或数据不一致不能继续同一旧轨迹。旧ImageNet元信息缺少新增DataConfig字段时按原默认值比较，不修改旧metadata。原恢复测试扩展为移除全部新data字段后验证，确保新增接口不破坏历史off路径。
- **验证结果：** 首轮既有228项回归通过；新增18项CIFAR检查通过；全量 **246项CPU回归通过**（91.508秒）。随后针对actual_noise_rate/noise_or_not、关闭后读取保护、分组计时和原生CIFAR模型跨设备补查，18项新测试+双CPU全局BN/完整Jacobian oracle+旧元信息恢复共20项再次通过（11.605秒）。涵盖checksum发布/缓存复用/坏源拒绝、tar+ordered NPY完整准备路径fixture、官方顺序反转换与逐项原标签校验、实际百分比断言、human/clean/synthetic语义、官方多项式RNG一致、native transform、audit真值不进入训练batch、分组CE独立NumPy校验/空组、三组共享真实入口tiny CPU模型训练与p50精确恢复、group CSV无重复、test不选best、父子参数及无运行时dry-run、原模型兼容。103个Python AST、TOML、shell语法和git diff --check通过。
- **完整真实源验证：** 在 `/private/tmp/dpco-cifar-real` 实际取得169001437字节官方原图包并通过发布MD5，验证固定注释/映射SHA256，执行正式prepare生成50000训练/10000测试cache并完成全部50000项原标签匹配。网络慢的最初顺序下载由临时辅助Range读取补齐、拼接后整包MD5确认，停止重复慢下载后调用正式离线准备；该临时加速工具不是生产下载器支持并发/断点续传的声明。加载实测human 40.2%(C29900/N20100)、clean100实际0%但保留同组、synthetic seed0 40.216%(C29892/N20108)。真实标签与读入计量不等于方法性能实验；未用完整数据执行优化训练。
- **涉及文件：** 新增 `src/data/{cifar100n,cifar100n_prepare}.py`、`src/models/cifar_resnet.py`、`scripts/prepare_cifar100n.py`、`configs/tpu/cifar100n/dpco_adam.toml`、`run_cifar100n_suite.sh`、`tests/test_cifar100n.py`、`docs/cifar100n.md`；修改 `src/{config,cli}.py`、`src/data/{classification,images}.py`、`src/training/{launch,evaluation,experiment,results}.py`、`scripts/{launch_tpu,train_classification}.py`、`tests/{local_mesh_check,test_updates}.py`、`pyproject.toml`、`README.md`、`docs/dpco_adam.md`，追加本文件。旧“尚未实现CIFAR/分组”记录保留为历史状态，当前说明以本条和新文档为准。
- **理论与未完成边界：** C/N正确性相对原始benchmark标签定义，不认证语义绝对无歧义；合成噪声匹配类转移不能替代实例依赖的人类噪声。没有证明DPCO对clean目标或泛化必然改善，也不以错误标签CE升高单独判成功。尚未正式训练/调参、TPU硬件吞吐/内存测试、绘制新实验结果或统计每组实际训练flip率；没有增加通用ImageNet噪声注入、均匀可调人类噪声或修改历史数据。未提交/推送；服务器需同步代码并自行按文档准备数据后运行。


### 2026-10-29 / DPCO-0017：服务器长任务统一 nohup 与中断下载恢复说明

- **用户授权依据：** 用户明确要求“写入咱俩交流的协议，以后都是nohup启动”，并报告终端断开、询问下载一半能否续传。本次授权更新协议及记录；未将询问续传解释为修改下载器源代码的授权。
- **目的与具体变动：** 在根目录与DPCO目录的AGENTS.md中约定，服务器下载、数据准备、依赖安装、训练及批量实验等长任务统一nohup后台启动，显式设置标准输入、独立日志、PID及查看方法，使用明确的项目Python路径；短时检查可前台运行。此约定不自动授权训练或扩大其他开发范围。
- **下载行为核对：** 现有src/data/cifar100n_prepare.py的download_asset保留失败.partial，但再次请求使用partial.open("wb")，会重头写该文件，并非原生续传；完整且校验正确的源文件会复用。不能让用户直接重跑并称其为断点续传。终端断开后原任务是否退出、文件已下载多少，尚无服务器证据。
- **恢复建议与边界：** 提供服务器端nohup包装的curl -C -手动续传方案，读取已有原图包.partial，持有同一.prepare.lock防止与旧准备进程并发写入；完整包先核对项目固定MD5再发布到正式文件名，随后交还现有prepare/verify入口完成其他源与缓存。续传依赖远端Range支持；若不支持则保留partial并报错，不声称必能续传。不改变生产下载器，也不绕过原有完整性检查。nohup仅针对终端挂断，不是机器重启或训练checkpoint恢复机制。
- **涉及文件与验证：** 仅修改根AGENTS.md、DPCO/AGENTS.md并追加本文件；阅读现有下载器、准备入口与近期开发记录，核对curl官方-C选项说明 https://curl.se/docs/manpage.html#-C 。文档差异检查通过，无需运行算法测试。
- **未完成项与证据限制：** 未连接服务器，未确认用户旧进程/partial实际状态、远端Range响应或完成续传；未改源代码、配置或依赖，未启动下载/训练、提交或推送。服务器上的协议文件需用户后续同步；本地规则现已生效。


### 2026-10-29 / DPCO-0018：核对训练准备、results三目录与自动保存/probe边界

- **用户要求与授权范围：** 用户询问是否可以训练，要求所有输出保存在results并按files/runs/logs分别存放检查文件、checkpoint和日志，提醒原SAGE有自动保存与probe。本次核对现有实现、记录输出约定并提供nohup启动命令；未把询问训练准备解释为远程启动正式训练或新增probe算法的授权。
- **依据与当前状态：** 用户此前粘贴的服务器日志包含prepared及随后独立verified，50000训练/10000官方测试、human mismatch为20100即40.2%，并打印三组dry-run；这证明数据准备已完成，不证明TPU优化训练已通过。现有CIFAR preset仍为未调优100步pilot。
- **目录核对与具体变动：** ResultsPaths已将相对results根目录锚定到DPCO根目录，RunRecorder将CSV写files/<run_name>，CheckpointStore写runs/<run_name>，launcher与recorder将stdout/train.log、完整配置/环境/启动信息写logs/<run_name>，跨运行状态写logs/run_status.tsv。无需修改源代码、配置或依赖。仅根及DPCO/AGENTS.md追加输出约定，且本文件追加；后续套件外层nohup日志和PID也放results/logs，不延续此前独立顶层logs写法。原始数据位置不作迁移。
- **保存与恢复：** 默认checkpoint开启，固定initial/p25/p50/p75/final和滚动latest；checkpoint包含参数、BN、EMA reference、Adam矩、训练/data/RNG状态及CSV游标。latest会被后续保存替换，未被逻辑slot引用的旧快照按既有策略清理，并非保存每一步；恢复必须显式指定单个原run及一致配置，非自动重启。CIFAR不依据官方test选best。
- **probe事实与边界：** 原theorem/diagnostics/mechanism代码仍保留，但配置验证明确禁止CIFAR100N或EMA/Adam路径启用旧observer。新路径已有每步train_steps、DPCO两组的dpco_steps（负alignment/干预数量、范数等）、evaluation与固定clean/corrupted_noisy/corrupted_original的group_evaluation，以及timing/summary。固定分组CE并不等于旧SAGE定理probe，更不等于按clean/corrupted分别统计负alignment的新增识别诊断；本轮未新增这些算法诊断，也无新理论结论。
- **验证结果：** 本地以三组100步、checkpoint每25步、evaluation每25步的CLI dry-run通过，确认三组配置/子进程透传及results路径。定向运行tests.test_results、tests.test_checkpoint_controls、tests.test_cifar100n共23项CPU测试全部通过（6.603秒），涵盖结果命名/路径、自动保存控制和CIFAR分组/恢复等既有检查；文档diff检查通过。
- **未完成项：** 没有连接服务器、启动真实数据优化或TPU实机测试；三组100步仅建议先验证流程，不能作为训练充分或算法有效的证据。正式预算与调参/统计重复尚未制定；未修改程序行为、提交或推送，既有未提交协议记录保留。


### 2026-10-29 / DPCO-0019：核验三组TPU pilot日志并提出长程参数与敏感性方案

- **授权依据与目的：** 用户提供三份100步训练日志，询问按近期CIFAR-100N的steps、lr、beta如何选择。本次为研究分析、参数建议与可复查命令，仅追加研究记录；没有修改源代码、配置、脚本或依赖，也没有连接服务器启动任务。
- **用户实验事实：** 阅读附件0f55ef65-8186-4bbf-9ff9-c0e5b9019af1、abfdbcd3-af30-4de5-b3bf-b8ba7e950383、93cd41ec-9fe4-4137-a02f-ba03a3bbd976中的Pasted text.txt，分别为Flip、Filter、Adam。三者均4个本地TPU、同一数据manifest、seed42、初始化test CE=6.364174609375、batch128、lr=.001、100步12800样本，均以completed结束。最终官方test top1分别2.04%、3.68%、5.66%；test CE分别5.1727828125、5.617509765625、4.1575671875。此前“未实机验证”描述以此追加用户日志证据更新，但未独立检查服务器checkpoint文件/CSV。100步仅0.256样本曝光轮，不能推断充分训练后的优劣。
- **稳定性观察：** 第25步test CE为Flip219.1931、Filter11.191984375、Adam10.71313671875，后续回落；Flip同节点clean原标签CE245.72566889632108。训练CE与eval CE使用不同BN口径，早期BN统计与快速变化参数不匹配是待排查可能，不能据日志确诊实现错误、宣称已发散，或保证降低lr一定修复。
- **论文与原实现依据：** 数据作者固定版本main.py使用ResNet34、batch128、SGD(momentum.9、weight_decay.0005)、100epochs，alpha_plan为前60轮.1后40轮.01，实际覆盖传入lr：https://raw.githubusercontent.com/UCSC-REAL/cifar-10-100n/49df7d8a69e355470c77c1c2f2424916325a394b/main.py 。TMLR2025的Coreset-Driven Re-Labeling论文Table3使用CIFAR100N 300epochs、SGD .02/momentum.9/weight_decay.0005/B128，针对DivideMix/SOP+等重标注流程，不是DPCO+Adam配方：https://openreview.net/pdf?id=Tk78vb2Qd7 （正文页面触发验证，检索索引可读到Table3；作者及TMLR页面亦确认出版信息）。Adam原文默认lr.001、betas(.9,.999)、epsilon1e-8：https://arxiv.org/pdf/1412.6980 。因此不存在数据集统一规定的收敛steps或DPCO reference beta，不能把SGD lr.1/.02套给Adam。
- **近期相关证据及边界：** 查阅2024TMLR的Exponential Moving Average of Weights in Deep Learning https://arxiv.org/html/2411.18704v1 ，其CIFAR100N/ResNet34实验为权重EMA，不能将论文alpha=.998或SGD大lr视为本项目梯度reference的验证。另核对2026-10-26论文Detecting noisy labels using checkpoint ensembles https://link.springer.com/article/10.1007/s00521-026-12575-1 ，说明其噪声识别与分类最优时间及scheduler关系依赖具体方法；不把其checkpoint检测/过滤的SGD设置宣称为在线DPCO共通定理。
- **本轮建议（尚未执行、非论文最优值）：** 保持native ResNet34/官方human noisy100/同一增强与FP32/B128。第一轮三组统一200个drop-last数据遍历，即floor(50000/128)=390步/遍历、总78000步；100/300遍历对应39000/117000步，原样本曝光epoch_progress在78000步为199.68。建议共享lr峰值3e-4、cosine降至1e-6、Adam beta1=.9/beta2=.999/eps1e-8，沿用L2=0以保持当前机制实验口径；这不是最终调优或论文复现基线。3e-4是考虑早期CE冲高的保守试验起点，.001保留为预先列出的敏感性值，不能保证3e-4更好。reference beta主设.99，Filter0/Flip-1，两者与Adam共享其他设置；每390步完整固定分组/test评价，latest每1950步，其余固定milestone保存不变。
- **beta解释与设计假设：** beta1/beta2控制编辑后方向的Adam moments，beta_ref控制原始batch梯度reference，独立设置。.9/.99/.999的名义衰减时间尺度1/(1-beta)约10/100/1000步，不是等权独立batch数；.99可减少当前batch在reference中的相对影响但引入历史滞后，尚无本项目性能证据。第一步无历史，偏差修正后r1=G1，增大beta无法改变这一点。后续先固定Adam betas，考察reference .9/.99/.999；lr候选1e-4/3e-4/1e-3，三组公平校准及报告，不能仅挑有利DPCO的设置。若增加正则对照，需三组一致，当前耦合kernel L2不等同AdamW。梯度编辑不是原始带噪CE的标准梯度下降，不能用该训练CE单调降低或固定步数单独定义DPCO收敛/成功。
- **评价与后续选择：** 当前代码官方test被兼容命名为val，尚无独立留出validation；本轮固定配置只能作探索，不能反复按test曲线挑lr/beta后声称盲测优势。正式调参应先制定独立固定validation方案；原标签/污染真值不进入reference/权重，不用corrupted_original组当训练oracle。同设置先seed42，后报告42/43/44三种子配对结果及固定预算final，不能以错误标签CE单独升高视为成功。长程改总预算/调度需从共同初始化新建run，不能按当前严格恢复协议从100步pilot改配置续训。
- **本地验证与未完成：** 用现有CLI对78000步、三组、B128、lr3e-4/cosine/min1e-6、beta_ref.99、Adam(.9,.999,1e-8)、L2=0、eval390/latest1950/seed42做dry-run，解析JSON逐组断言通过；不创建run、不导入训练运行时、不消耗TPU。文档diff检查通过。仅追加本文件；未改动其他未提交记录、启动正式训练、提交或推送。参数有效性、长程数值稳定性、独立validation与新reference识别诊断仍待验证。


### 2026-10-30 / DPCO-0020：三组训练曲线与时间效率绘图方案讨论（未实现）

- **用户请求与边界：** 用户拟在DPCO下新增plots目录，按明确指定的Adam/Flip/Filter三个results/files子目录读取train_steps.csv及timing.csv，画高宽比0.8:1的CE/accuracy折线，并询问timing是否结合CE；明确“先思考，先不改代码”。本轮只读取与讨论，按开发协议追加研究度量建议；没有创建plots目录或改动代码、配置、脚本、原始CSV。
- **字段及现有代码核对：** train_steps含step/train_ce/train_top1/valid_batch_size/elapsed_wall_s；accuracy为0–1比例，图中转为百分数。timing含event/duration_s/window_steps/window_samples/steps_per_s/samples_per_s/elapsed_wall_s等。experiment.py在train_window窗口排空时device_get，窗口时长包含该窗口输入处理、训练派发和等待设备完成；每步train_steps.elapsed_wall_s是host派发时间戳，不等同每步设备完成时间。现有scripts/plot_training_results.py针对旧ImageNet/SGD族，不能直接声称兼容当前CIFAR/Adam三组。未检查服务器完整长程CSV，也未据本轮读取推断长程结果。
- **主图建议（待用户确认实现）：** 两张step图：原始带噪标签普通train CE与100*train_top1；另建议对应的两张time图，横轴为训练循环累计wall-clock分钟，纵轴同前。每图独立三条曲线，纵横比按高/宽=.8解释；后续可固定axes box aspect=.8并另外固定画布，不能仅依靠数据坐标比例。按用户原文Adam蓝实线、Flip红实线、Filter蓝虚线；重复蓝色使用线型区分，不擅自将Filter改成绿色。可选统一后向平滑、保留淡色原始线并记录窗口，不能各方法单独平滑、隐藏前期异常或改原CSV。
- **时间对齐和口径：** 时间主图优先使用timing中train_window的已完成窗口端点elapsed_wall_s，将其覆盖的(step-window_steps,step]内训练CE/accuracy按有效样本数聚合，避免将异步派发时间戳当逐步精确GPU/TPU耗时。窗口指标是区间均值，横轴为端点，需在图注说明。循环wall-clock包括循环内初始评价、JIT、周期评价/保存及训练开销，但不包括循环启动前的数据准备和模型初始化；不冒称全程序端到端时间。可选active训练时间为仅train_window.duration_s累计，排除独立记录的JIT、评价和checkpoint阶段，但仍包含输入与同步，并非纯kernel时间。不能将所有event时长混加当总耗时。
- **辅助效率图：** 可选以窗口末step为横轴、1000*duration_s/window_steps(ms/step)为纵轴，或给出加权总平均1000*sum(duration_s)/sum(window_steps)；不对不同长度窗口的单步均值简单平均。不把duration_s本身误标为每步时长。保持三组相同设备、batch、数据和评价/保存设置，并如实报告是否计入编译和监测开销。
- **方法依据与研究边界：** MLPerf Training以到达指定质量所需时间评价效率，来源 https://mlcommons.org/benchmarks/training/ 。优化器比较亦同时考察墙钟与性能/计算代价，参考 https://proceedings.mlr.press/v199/metz22a/metz22a.pdf 。本项目只读取这两个CSV时，时间-CE/acc图衡量的是带噪标签拟合效率；更低训练CE/更高带噪train accuracy不自动说明DPCO更好。正式泛化效率图应另读evaluation.csv的官方test指标，教授机制图应另读group_evaluation.csv；不在本轮私自扩展实现输入或按test阈值调参。只在预先指定的统一质量目标有意义时报告time-to-target，未达阈值记未达到，不能编造到达时间。
- **拟定文件组织与验证：** plots作为后续绘图代码目录，图像及绘图参数/来源清单建议输出results/files/plots/<comparison_name>/，默认PNG/PDF，遵守既有results三目录规则；三个输入目录由参数显式指定，不自动选“最新”run。此为拟议接口而非已完成能力。检查本轮文档diff通过；无代码修改，不运行算法或绘图测试，未生成示意研究曲线、启动训练、提交或推送。


### 2026-10-30 / DPCO-0021：实现显式三组CSV绘图、可调平滑与ms/step图

- **用户授权依据：** 用户明确要求“可以，按照你的建议来修改代码”，平滑窗口由参数控制，并加入ms/step vs Step图。授权覆盖DPCO/plots离线绘图入口、必要绘图依赖、文档和本地验证；不改训练算法、CSV生产模式或既有实验数据。
- **起始状态与保护：** 开始时只有DPCO_dev.md存在未提交的历史研究/协议追加记录，全部保留。没有创建新worktree、修改训练源文件或既有历史绘图器；没有连接服务器、启动训练、提交或推送。
- **代码与接口：** 新增plots/plot_dpco_training.py及plots/README.md。用--adam-dir/--flip-dir/--filter-dir显式指定三个不同run目录，支持绝对路径、相对DPCO根路径或results/files下单个run名；不自动选择最新/最佳实验。只读train_steps.csv、timing.csv，存在对应logs元信息时额外校验方法/优化器/EMA负权重，报告配置与数据指纹差异；无元信息的CSV导出仍可画图但明确标签来源限制。训练runtime完全不导入，--help在无site-packages解释器下亦可用。
- **图形与输出：** 默认生成train_ce_vs_step、train_accuracy_vs_step、train_ce_vs_time、train_accuracy_vs_time、ms_per_step_vs_step五张独立图，各PNG+PDF。Adam蓝实线、Flip红实线、Filter蓝虚线。画布5×4英寸、绘图区高/宽=.8，PNG220DPI（1100×880），不使用tight裁边改变导出高宽比；accuracy按100倍转为百分数，线性CE不丢弃早期异常值。输出到results/files/plots/<自动唯一时间戳或--output-name>/，已有目录拒绝覆盖；另存step_curves.csv、timing_curves.csv和最后写入的plot_manifest.json，保留输入/脚本SHA256、平滑参数、计时说明、设置差异、实际曲线和加权ms/step。失败目录无完成manifest，旧结果不自动清除。
- **平滑定义：** --smooth-window默认100，正整数，1关闭额外平滑。Step图按最近W次更新的有效样本数加权，开头按已有前缀平均，保持因果性。时间及ms/step图以完整train_window为最小单位，从当前窗口往前累计到至少W步（开头不足则已有窗口）；不拆窗口、不对host派发时间作伪精确设备完成插值。W=1保留原始窗口均值。耗时用sum(duration)/sum(window_steps)，而非对不同长度窗口的ms/step简单平均。原始淡色线默认开启，--no-raw可关闭；输出CSV仍保留原始窗口/逐步值，实际平滑步数写入timing_curves.csv。
- **计时与输入完整性：** --time-axis wall默认取已完成train_window端点elapsed_wall_s/60，包含此前循环内监测/编译/保存，排除循环前数据准备和模型初始化；窗口指标为区间平均，末点不是最终评价/保存之后的进程结束时间。active选项仅累计train_window duration，仍含输入与设备同步。ms/step图取1000*duration/window_steps。校验连续完整训练step、窗口无重叠无缺口且覆盖所有训练行、正窗口时长、时间一致/单调、数值有限和accuracy比例。只读输入前后哈希复核，文件变化时拒绝产生完成manifest；不把训练中两个文件异步刷盘的不一致快照自动修补。
- **涉及文件：** 新增plots/plot_dpco_training.py、plots/README.md、tests/test_dpco_training_plots.py；pyproject.toml新增可选plot extra（matplotlib>=3.8,<4，不改变train/tpu依赖）；docs/cifar100n.md追加新绘图入口说明；追加本文件。提供服务器nohup命令将绘图依赖安装与绘图串行执行，外层日志和PID同样位于results/logs。
- **验证结果：** 新增8项测试与旧绘图10项合计18项检查全部通过（0.633秒）。验证独立数值预期的样本加权平滑、因果前缀、不等长计时窗口加权及分钟/毫秒单位、编译事件不计active、忽略host派发戳、gap/overlap/缺失/非有限/时间倒退拒绝、accuracy单位和方法标签拒绝、设置与数据指纹不匹配说明、完整五图十文件实际渲染、PNG尺寸/PDF头、源CSV字节不变、输出防覆盖、绘图区.8比例/颜色线型及active坐标、无第三方依赖help。另在/private/tmp/dpco-plots-visual-qa-*用明确的合成fixture导出五张PNG/PDF，并查看CE-step、accuracy-time及ms/step三种代表布局，无文字裁剪/颜色或比例问题；这些QA图不是用户实验数据或算法效果证据。Python AST/TOML、README命令shell语法及git diff --check通过。
- **证据边界与未完成：** 未取得用户服务器78000步的完整CSV，尚未生成真实长程实验图，不能用本轮fixture说明方法性能。训练CE/accuracy仍是观察噪声标签拟合，泛化与clean/corrupted曲线未在此入口新增；未新增time-to-target/阈值选择、跨seed置信区间或修改旧theorem probes。绘图参数不改变训练轨迹，无算法收敛或收益新结论。


### 2026-10-30 / DPCO-0022：绘图输出改为results/figures并将Filter改为橙色

- **用户授权依据：** 用户明确要求“把plot的输出结果放到result目录下，起名figures/ 与files等目录同目录级别。现在修改代码，并且把fliter变成橙色”。依据与既有files/runs/logs同级的要求，沿用实际项目根目录名results，目标为DPCO/results/figures，不另建单数result。
- **目的与具体改动：** plots/plot_dpco_training.py将新绘图任务输出根目录从results/files/plots改为results/figures，保留原时间戳或--output-name子目录结构。五张图的PNG/PDF、派生曲线CSV与plot_manifest.json统一写该任务目录；CLI帮助与使用文档同步。Filter颜色改为橙色#ff7f0e，保留虚线，Adam蓝实线和Flip红实线保持。旧路径/旧配色记录作为历史保留，以本条和当前代码为准。
- **涉及文件：** plots/plot_dpco_training.py、plots/README.md、docs/cifar100n.md、tests/test_dpco_training_plots.py及本文件。已有集成渲染检查更新为断言新目录与不再创建旧输出目录，颜色检查更新为橙色。没有修改训练源代码、计时/平滑公式、依赖或原始结果。
- **验证结果：** 新/旧绘图合计18项检查全部通过（0.634秒），包含新目录下实际生成五张PNG/PDF、源CSV不变、防覆盖及三种颜色/线型。git diff --check通过；只进行了授权变更所需的本地验证，无新算法测试或正式训练。
- **理论与证据边界：** 本次仅输出组织与视觉样式修改，无理论或实验性能新结论；渲染仍使用临时fixture，未读取服务器真实长程数据。已有results/files/plots产物保留，不自动搬移、覆盖或删除；用户同步脚本后使用原绘图命令即可生成到新位置。未连接服务器、提交或推送。


### 2026-10-30 / DPCO-0023：解释长程训练CE曲线、继承的40.2%噪声与Adam学习率下限

- **用户请求与授权边界：** 用户批注此前78000步命令，并提供train CE对wall-time/step两张图，认为未达预期，询问实际错误数据百分比及Adam是否必须把lr降至0。本轮只读核对、解释并按协议记录研究判断；不构成修改算法、训练/绘图配置或再次运行的授权。
- **图像证据：** 用户附件codex-clipboard-d627b634-cc8e-46de-a54e-9e3ae140adb0.png和codex-clipboard-77e1a4a7-3c65-4e97-be08-555058a96f66.png显示Adam和Filter后期训练CE接近0，Filter早期较慢，Flip在78000步附近仍约3.2；这些为读图近似值，未取得对应完整CSV或test/group曲线，不能凭此判定泛化优劣或去噪成功。曲线展示普通观察标签CE，不是signed训练替代目标；跨时间变化的训练batch/增强/BN指标也不是同一冻结数据评价。
- **噪声核对：** 选中命令通过--config继承configs/tpu/cifar100n/dpco_adam.toml的data.noise_type=noisy100、is_human=true、noise_percent=40.2；三组共享已发布human标签。先前prepared/data_ready记录为20100/50000即40.2%相对原标注不一致，另外29900即59.8%一致；并非只选40.2%样本训练、每批恰有40.2%错误、每轮重新改标或负alignment比例。noise_percent为0–100实际比例断言，不是人为生成指定百分比的旋钮；如需命令可读性，可显式追加--noise-type noisy100 --is-human --noise-percent 40.2，但不会改变这一数据版本。测试标签未额外注入噪声；原benchmark标注仍不是绝对语义正确的认证。服务器正式run应以其metadata/data_ready和实际CSV为最终证据，本轮未连接服务器核验文件。
- **学习率核对：** 重读src/training/learning_rates.py及CLI解析，命令指定峰值3e-4、cosine、min1e-6、T78000。第k次更新k=1..T的lr为min+(peak-min)/2*(1+cos(pi*(k-1)/(T-1)))；本地纯标量计算首步0.0003、接近中点0.0001505030107315586、末步0.000001。故本次已衰减约300倍，未衰减到0。Adam的moment自适应与外部global lr schedule是不同机制，算法本身不要求有限预算末步为0；原算法可用固定alpha，cosine可选0或正下限。特定理论中的渐近步长条件不能泛化成所有深度学习Adam训练必须最后一步0。核对原论文 https://arxiv.org/pdf/1412.6980 及Optax调度文档 https://optax.readthedocs.io/en/latest/api/optimizer_schedules.html ，项目采用本地定义的cosine而非声称调用该库schedule。将floor设0并无当前Flip更好的证据，不将其当作解释表现差异的充分原因。
- **理论解释与下一步判据：** 原始带噪训练CE更低可能伴随记忆错误标签，不等同更好泛化；Flip较高亦可能来自抑制错误拟合或误伤有效样本，不能自动解释成抗噪有效。r_t^T g_i<0并不推出标签错误；raw noisy-gradient EMA可平滑波动但不自动消除标签偏差，Flip对误识别样本的反向处理比置零更强。之前200轮/beta_ref.99是待验证起点，不是已证实最优设置。下一步优先共同查看evaluation.csv官方test CE/top1、group_evaluation.csv的clean原标签/corrupted noisy/corrupted original指标及dpco_steps.csv的negative_count/valid_batch_size、reference cosine等；目前没有按C/N分别统计识别负alignment的现成功能，不宣称已验证噪声识别精度。不按这两张train图直接调参、延长训练或修改算法。
- **验证与涉及文件：** 使用完整批注参数对三组现有CLI执行dry-run，逐组确认noisy100/human/expected40.2及cosine/3e-4/min1e-6；标量公式核算如上。仅本文件追加，文档diff检查通过；没有跑训练测试、改动代码/配置/图片或原数据、启动正式训练、提交或推送。


### 2026-10-30 / DPCO-0024：分析导入的完整三组结果、正确标签误干预界与三个beta释义

- **用户请求与授权边界：** 用户已将服务器结果复制到项目根目录Results/，要求分析差异和DPCO未优于Adam的原因，并询问reference定义及“beta2=.999是否当前.999/历史.001”。本轮只读实证分析、生成研究报告/派生CSV/图表及追加本记录；没有修改程序源代码、配置、依赖或启动模型训练。开始时DPCO_dev.md已有上一轮未提交记录，予以保留。
- **数据与公平条件核对：** 读取Results/files及logs中三个长程run全部train_steps/evaluation/group_evaluation/summary/timing、两组dpco_steps与三份metadata。每组78000训练行、201次10000张test评价、603行分组评价，均completed。三组data/model/training/execution/seed/global_batch_size/evaluation/checkpoints完全一致，均seed42、B128、native ResNet34、FP32、四TPU、cosine3e-4→1e-6、Adam(.9,.999,1e-8)、L2=0、40.2%官方human噪声。记录的commit f89da2f5654a82fb119788752e291de7ceaeaecf、clean工作区、source SHA256和数据指纹均一致。源码diff核对当前dpco_history/updates/images与该commit无差异；训练状态/逐样本alignment未提供，不能因此排除所有潜在实现问题。
- **最终结果事实：** Adam/Filter/Flip最终官方test top1分别51.24%/51.20%/26.10%，test CE4.19585/3.73212109375/3.0038705078125，循环时间53.1137/59.3314/59.0950分钟，train_window加权27.5060/31.1781/31.1120ms/step。Filter top1仅低.04个百分点（总正确数差4），单seed不足认定比Adam差；test CE与top5反而较好。Flip比Adam低25.14个百分点，但test CE更低，须区分准确率、log loss与未测的校准指标，不能以任一项代替全部效果。
- **固定分组证据：** Adam/Filter/Flip正确标签组top1为100%/99.9967%/33.9097%；错标组对人工错标签top1为99.9602%/99.9502%/9.6866%；同一错标组对原标注top1为.0199005%/.0298507%/17.1542%，对应CE17.9084/14.7815/3.36735。故Filter最终仍几乎完全记住了错标签；Flip避免大量错标记忆，却严重欠拟合正确标签组，不能称为成功抗噪。相对原benchmark标注的分组不认证绝对语义正确。
- **时间演变与过拟合：** 错标组第一次达到50%错标签拟合：Adam27轮、Filter44轮；达到90%：47/63轮。第一次test top1达到50%：Adam15轮、Filter28轮，Flip未达。第30轮Filter错标原标签top1为33.31%，Adam12.55%，但最后两者均近零，说明Filter延缓而未阻止记忆。test事后峰值Adam51.82%(8580步约22轮)、Filter51.28%(12870步约33轮)、Flip26.10%(最后)，仅用于描述，不用于test选checkpoint。Adam最低test CE1.81309约16轮、Filter1.79427约30轮，最终更高，结合错标组体现长程过拟合；不能把最终train CE趋零当成去噪成功。
- **干预与reference统计：** Filter全程负alignment/贡献编辑比例44.1561%，Flip40.3385%；第101–150轮Filter50.4653%。reference/raw batch gradient平均cosine分别.123965/.144627，低相似度本身不证明reference错误，但没有提供与clean目标一致的证据。编辑后/原始方向范数比均值Filter.925812、Flip1.16616，故Flip不能简单归因于“正负抵消导致梯度范数消失”。Adam可抵消部分整体缩放，范数比不等于实际参数步长比。所有reference_gain最小为0符合代数构造，却没有带来Flip泛化优势。
- **离线误干预下界（新推导与验证条件）：** 利用先前本机已验证的/private/tmp/dpco-cifar-real/prepared/labels.npz，核对prepared manifest哈希1432cf...、labels.npz哈希与本次观察标签哈希4eeae1...逐项一致。按同一代码seed42/epoch-shuffle/drop-last重建200轮每批实际错标数n_t；共9984000次出现，错标4013550、正确标签5970450次。若日志负数a_t，则该批正确标签编辑数至少max(0,a_t−n_t)。逐批求和，Filter至少606666次正确标签出现被过滤（正确标签出现次数的10.1611%），Flip至少262987次被翻转（4.4048%）；相应噪声识别precision至多86.2389%/93.4700%。这些是条件于已核对批顺序的保守下/上界，不是实测precision/recall或独立图片占比，不识别具体被编辑的样本；真实误伤可能更多。它证明存在误干预，尚未证明该因素解释全部性能损失。
- **reference精确定义与纠正：** G_t为当前有效batch所有原始观察标签梯度均值，H_t=beta_ref H_{t-1}+(1−beta_ref)G_t，r_t=H_t/(1−beta_ref^t)，H0=0。本次metadata确认beta_ref=.99，故历史状态99%+当前原始梯度1%，不是beta2=.999。历史状态包含更早梯度且在各自旧参数处计算，不保存/重算旧batch；当前batch包含在reference。bias修正后r1=G1，r2约.49749G1+.50251G2；正标量修正不改分数符号。q_i=r_t^T g_i，负分数权重Filter0/Flip−1，其余1；D_t用原始B分母聚合。被过滤/翻转样本原始梯度仍通过G_t进入H，且过滤非永久删除。
- **Adam两个beta与理论边界：** beta1=.9：m_t=.9m_{t-1}+.1D_t；beta2=.999：v_t=.999v_{t-1}+.001(D_t⊙D_t)，再分别偏差修正、按m_hat/(sqrt(v_hat)+eps)更新。故用户当前/历史权重理解反了；v为编辑后方向的逐坐标二阶原始矩，不是reference、有符号方向或每样本平方梯度的平均。本次三个状态独立；beta_ref名义时间尺度约100步，beta2约1000步不是同一平均。依据代码dpco_history.py:66–81和updates.py:102–104/124–133及Adam原论文 https://arxiv.org/pdf/1412.6980 。raw带噪梯度EMA平滑波动不自动去偏、旧参数梯度滞后、正确难样本梯度冲突、−1强干预与Adam坐标预条件化均为合理机制假设，尚不能据当前汇总日志完成因果分解。r^T(D−G)≥0不保证clean目标或Adam实际更新下降。
- **产物与复核：** 在DPCO/results/files/cifar100n_review_20261030_07oqs01k/生成analysis.md、final_comparison.csv、epoch_metrics.csv、dpco_epoch_stats.csv、intervention_bounds.csv、analysis_manifest.json；同名results/figures目录保存accuracy_and_memorization和reference_and_interventions两套真实数据PNG/PDF，已视觉检查轴、标签和颜色。原始输入前后SHA256逐项相同，记录在manifest。统计核对全部78000步连续性、窗口总步数、元信息一致性与分组节点完整性，独立计算首次阈值到达轮数作交叉检查；doc diff检查通过，不运行训练或更改绘图程序。
- **未完成项与建议：** 单seed、未调优、官方test已监测；不能给出显著性、最优超参数或所有设置的算法失败结论。没有逐样本scores与checkpoint，无法重算实际混淆矩阵、clean目标梯度或实际更新投影。下一步优先拟定只读的C/N负alignment诊断和独立validation方案，再由用户授权实施与对照强度/时间尺度实验；本轮未实施、提交、推送或更改原始Results/。


### 2026-10-30 / DPCO-0025：重读组会，校正对教授小规模flip验证及正确标签编辑的解释

- **用户请求与授权边界：** 用户指出教授已在小数据集/MLP上做过小规模正面验证，要求重读新放入文件夹的两份组会MD并回忆原实验要求。本轮为阅读、理论解释和追加更正；不授权更改算法、配置、脚本或启动训练。开始时本文件已有未提交记录，完整保留。
- **涉及文件与核对：** 重读上级AGENTS.md、本目录AGENTS.md及近期开发记录；完整阅读项目根目录《教授周会_10.27_转写校对稿.md》《教授周会_10.27_新项目实验重点总结.md》，核对dpco_history.py:66–81与前轮派生final_comparison.csv。仅追加本文件与results/files/cifar100n_review_20261030_07oqs01k/analysis.md的第9节，不改原始会议记录或Results输入。
- **组会证据与边界：** 转写27:59–29:19提出batch mean的历史衰减signal；31:27–31:44明确确认换reference后继续flip；32:16–35:24先做noisy数据的controlled verification，观察clean loss低/下降与corrupted loss高，之后才scale up；33:40–33:52教授明确报告MNIST简单实验已完成，33:52–34:21建议先Adam并讨论flip频率。MLP背景由用户本轮补充，记录未给模型结构。两份MD没有教授实验代码、精确r、beta、噪声比例/机制、损失、初始化/归一化/LO细节，亦不能确认“每轮”是step还是epoch；因此当前含当前batch、raw EMA、beta_ref=.99、每step全参数flip的实现属于已授权原型，不能宣称严格复现其MNIST配方。
- **理论更正：** 对DPCO-0024及analysis.md中“正确标签误干预”“证明存在误干预”的解释追加收紧：逐批计数推导仅证明原标注一致样本被编辑，不能由标签正确推出其对给定reference的贡献一定有利，故不能证明贡献优化意义上的误判。Filter10.1611%/Flip4.4048%仍为正确标签样本出现次数被编辑的下界；相应precision上界只是在将负alignment作为错标识别预测时的指标，不是flip最优性的反证，也没有完成性能损失的因果分解。此前过强用语以本条追加更正为准，原数值及历史文本保留。
- **条件性教学推导：** 固定r及g_i，对w_i∈[-1,1]独立约束下最大化r^T(Σ_i w_i g_i/B)，每项为w_i q_i，故q_i>0取1、q_i<0取−1，q_i=0任意。这只是与当前实现一致、便于解释的子问题，不能代替录音未完整给出的教授定理及其假设。该局部子问题最优、r对关心的学习目标是否合适、多步Adam轨迹是否改善，是三个不同问题。教授报告的MNIST正面实验应保留为其条件下的实验证据；当前单seed的CIFAR结果既不能否定该报告，也不能证明普遍成功。
- **按教授目标重述实验：** 最终clean CE为Adam0.000167929、Filter0.000403484、Flip2.683918；corrupted观察错标签CE为0.001030090/0.001556779/3.963198。Flip的clean CE随训练也下降，不能称为完全没学；但同预算clean拟合显著弱于对照，尚未得到所希望的选择性改善。单看高corrupted loss或低整体train CE均不足判断。Filter最终test top1与Adam近似持平，不将两种干预笼统判为失败。
- **后续建议及未完成项：** 优先对齐教授小实验的r精确公式、原始/编辑梯度、评分参数范围、噪声设置、损失、Adam参数及flip频率，再做MNIST/MLP最小复现并逐步改变数据/模型以定位差异。此前三组是按用户后来确认的范围实现，未增加batch-only基线；历史signal净收益需另作消融，不能把原会后计划当作本轮新增实现授权。BN、真实噪声、多类别、reference滞后等仅为待验证候选因素；本轮无新因果归因。
- **验证结果：** 对照原文时间戳、当前reference实现和已有派生CSV，表内数值一致；文档diff检查通过。未运行模型测试、修改代码/配置/依赖、启动训练、提交或推送；教授最小实验的精确配方仍待取得与核验。


### 2026-10-30 / DPCO-0026：评估MNIST接入范围、CIFAR后续定位与历史reference的会议符合性

- **用户请求与边界：** 用户更正MLP可能记错，只确认教授说过MNIST，具体模型未知；要求评估MNIST所需代码改动、不做MNIST时如何继续CIFAR-100N，以及当前指数衰减reference是否满足教授要求。仅评估和理论澄清，未授权实现。本轮只追加开发记录，不改代码、配置、依赖或启动实验；DPCO-0025中MLP作为用户补充的描述以本条撤回其确定性，不能把MLP当作已知教授设置。
- **读取与保护：** 阅读两级AGENTS、最近记录、config.py、data/classification.py、data/images.py、data/cifar100n.py、models/resnet.py、tasks/classification.py、training/evaluation.py、training/launch.py、training/results.py、scripts/train_classification.py及相关EMA测试；核对会议27:59–29:19、31:27–31:44、33:40–34:21。已有未提交记录保留。一次读取dpco_history.py时工作目录少一层导致未找到文件；其路径已在上一轮核验，未据该失败推断文件缺失。
- **MNIST工作量评估：** 当前没有MNIST loader/模型预设，不能只改数据集名。原生28×28灰度接入需处理evaluation_batches与模型initialize的三通道硬编码；无BN小模型还需独立adapter/初始化，不能套用强制batch_stats的ResNet adapter。完整规范接入包括下载/校验/缓存、固定训练标签污染及原标签审计、数据分发/配置校验、模型选择、分组评价、训练/启动CLI与元信息、噪声身份/run命名、配置文档和必要测试。按独立小模型、复用现有结果/恢复体系的设计，粗估修改7–10个现有文件并新增5–8个文件（含测试、预设和文档），不是已实现或承诺精确diff；最终取决于模型、单通道方案和噪声接口。EMA/flip/filter、Adam、CE任务、通用训练循环和checkpoint主体可以复用，无需重写优化器。小CNN/MLP均只能是我们自主选择的验证模型，缺教授配方时称MNIST机制验证而非严格复现。
- **符合性结论：** 当前G_t为原始batch梯度均值，H_t=beta_ref H_{t-1}+(1-beta_ref)G_t，r_t=H_t/(1-beta_ref^t)，再依负alignment编辑并交Adam；这直接落实会议提出的batch mean、历史beta衰减、继续flip三个要点，属于符合明确构造方向的合理实现，不应因单次结果差认定偏离教授要求。它借鉴的是Adam式一阶历史累计，不要求把Adam二阶矩或预条件化也放入r。beta_ref=.99为我们具体选值，并非教授指定；正标量bias correction在非退化精确算术下不改变评分符号，不能把是否bias correction本身列作本次sign-only性能差异的主要解释。精确数值/频率和MNIST配置尚未知；实现符合方向不等于已达到受控验证预期。
- **继续CIFAR的建议（未执行）：** 保留当前三组和原始结果，先用已有clean/corrupted_noisy/corrupted_original轨迹评价选择性学习。首选在同一ResNet34上追加clean100对照，比较Adam与Flip是否在无训练标签污染时仍出现学习阻碍；当前CLI已支持clean100/0断言，无需实现新数据集。clean100下现有C/N分组仍按原human reference划分，组名不是当前训练的实际污染状态，clean训练分析须用原标签评价，不能混淆corrupted_noisy的反事实标签。随后固定flip=-1、Adam参数和其他条件，只比较beta_ref=.9/.99/.999；阶段性实验需共享总预算与lr调度，短预算cosine不能直接同原200轮前段视为完全同设置。新增干净对照或消融均建议从共同初始化新run，不修改现有run配置续训。ResNet18已可配置，可作后续模型敏感性而非教授模型复现。
- **诊断与噪声接口边界：** 如需定位机制，另行授权增加周期性C/N alignment分布/负数比例、贡献大小，以及固定clean目标梯度与实际Adam参数增量的内积；真值仅进入观察者，不进入训练reference或权重。现有dpco_steps总计数不足以恢复实际逐样本归属，旧observer在EMA/Adam配置被禁用且不直接适用，不直接打开旧probe。CIFAR当前noise_percent是实际噪声比例断言，no-is-human是按人类标签经验转移矩阵采样；两者都不是任意20%等污染强度的生成接口。自行引入污染比例旋钮需另行授权，并保留官方40.2%基准的原含义。
- **验证结果与未完成项：** 静态确认上述配置/数据/模型/评价硬编码和既有可调入口，文档diff检查通过；没有声称MNIST新路径运行通过或给出服务器训练时长。模型未知、教授配方未知、候选失败机制尚无因果确认；本轮没有修改源代码、生成正式配置、运行训练、提交或推送。


### 2026-10-30 / DPCO-0027：核对ResNet型号并提供三档reference beta串行后台命令

- **用户请求与边界：** 用户询问为何ResNet34、能否用50，并决定先固定Flip−1、Adam/模型/数据，仅比较beta_ref=.9/.99/.999，要求启动命令，由用户在服务器执行；随后另一台服务器的MNIST等研究是后续计划。本轮只核验入口、提供命令并追加记录，没有修改源代码/配置/脚本、连接服务器或启动正式训练，不据后续计划实现MNIST。
- **模型事实与解释：** 重读两级协议、最近记录、CIFAR模型与配置校验、训练launcher和导入metadata。三个既有长程run均为cifar_resnet34，并非resnet50。沿用34是为了保持本轮beta消融的模型与既有对照一致，不是理论上必须用34或已证实34优于50。ResNet50原则上可以开展此类实验，但当前CIFAR分支仅实现native32的cifar_resnet18/34；已有resnet50是ImageNet分支的模型入口，配置校验拒绝CIFAR+resnet50，不能仅换CLI参数。若以后引入CIFAR版50需另行授权适配并重建同模型对照。
- **命令方案（提供，未执行）：** 从服务器/home/jason_chia925_gmail_com/Project_DPCO/DPCO运行；使用绝对Python /home/jason_chia925_gmail_com/Project_DPCO/.venv/bin/python；外层nohup bash按.9/.99/.999顺序调用scripts/run_suite.py --wait --mode train，每组只有dpco_flip、seed42、negative_weight−1。明确cifar100n/cifar_resnet34、noisy100/human/actual40.2%、78000步/B128、cosine3e-4→1e-6、Adam(.9,.999,1e-8)、L2=0、eval390步、checkpoint1950步且开启保存。不使用resume，从共同seed重新开始；已有Adam作对照无需按reference beta重复训练Adam，三组beta均新建run且保留原.99结果。
- **后台与输出：** 外层stdin=/dev/null、stdout/stderr统一进入results/logs下mktemp生成的独立sweep子目录/sweep.log，保存sweep.pid；各beta独立launcher日志。建议用set -euo pipefail及管道tee同时记录launcher输出到每组日志和sweep.log；任意组退出失败则停止后续组。run_suite子进程本身也用nohup，保持逐run的files/runs/logs输出，并等待实际退出/TPU锁释放后进入下一beta。提供PID、ps与tail方式；这是终端断开保护，不声称机器重启恢复或自动续训。
- **验证结果：** 本地现有解释器对三档完整CLI分别dry-run并解析JSON，逐组断言model、EMA beta、负权重−1、Adam、78000步、human40.2和wait；检查子命令透传reference_beta/negative_weight及Adam三个参数，均通过。另通过resolve_config确认CIFAR+resnet50确实被拒绝。没有创建训练run或调用JAX/TPU执行。一次外层目录git status因外层非Git根返回失败，已在DPCO内正确检查，仅本开发记录有未提交改动。文档diff检查通过；没有新增理论性能结论，三档能否改善仍待用户实验。


### 2026-10-30 / DPCO-0028：区分官方ResNet34基线与本项目18/34的实现范围

- **用户请求与授权边界：** 用户追问本项目为何只支持CIFAR ResNet18/34，是否官方既定标准。本轮为只读源码/官方来源核验与解释；没有授权适配新模型。只追加本记录，不修改源代码、配置或训练状态。
- **来源与验证：** 读取两级AGENTS、最近记录、src/models/cifar_resnet.py、src/models/resnet.py、src/config.py及docs/cifar100n.md。浏览官方仓库 https://github.com/UCSC-REAL/cifar-10-100n ，其固定版本main.py https://raw.githubusercontent.com/UCSC-REAL/cifar-10-100n/49df7d8a69e355470c77c1c2f2424916325a394b/main.py 明确model=ResNet34(num_classes)，并使用SGD；当前官方main分支模型文件 https://raw.githubusercontent.com/UCSC-REAL/cifar-10-100n/main/models/resnet.py 同时定义ResNet18/34/50/101/152，其中18/34为BasicBlock，50/101/152为Bottleneck。固定版本models/resnet.py一次网页读取cache miss，未将失败页面当证据，后改用成功读取的main分支文件并明确版本范围。
- **解释与更正范围：** 官方公开训练入口采用ResNet34，作为本项目34模型选择的基线依据；不存在由这些来源得出的“CIFAR-100N只允许18或34”的要求，官方自身也提供50等模型定义。当前18/34限制来自本项目CIFAR专用模块只实现BasicBlock及工厂中的两个stage映射，并在配置层显式限制；18提供同一结构族的较小选项。ImageNet分支已有50/101的Bottleneck与7×7 stride2/maxpool入口，尚未接成CIFAR模型。此为本项目工程支持范围，不能表述为数据集或官方模型白名单，更不能从中推断34性能必优于50。当前JAX/Adam训练亦不等同完整官方PyTorch/SGD配方复现。
- **对当前实验的影响：** 已提供的beta消融继续固定cifar_resnet34，以仅改变reference beta；以后若研究50，应明确适配及模型定义并重建同模型对照。没有改动或重新启动用户可能正在执行的任务。
- **涉及文件、检查与未完成项：** 仅本文件追加；git diff --check通过。未运行算法测试、实现CIFAR50、启动正式训练、提交或推送。实际50模型的接入仍未实现，且本轮未讨论其性能保证。


### 2026-10-30 / DPCO-0029：按模型参数复用ResNet50并接入MNIST三组Adam实验

- **用户授权依据：** 用户明确要求“现在改代码，用参数来控制使用那个model，并且加入minist”。工作中用户进一步选择“小CNN，20%合成错标签”。授权涵盖模型选择、既有ResNet50复用、MNIST准备/加载/训练接入、必要配置/文档/检查；没有授权启动服务器正式训练、推送或改变EMA/flip公式。开始时仅本文件有未提交历史追加记录，全部保留。
- **模型选择与语义：** 新增src/models/classification.py，以明确模型名分发，训练入口不再按CIFAR数据集强行选择CIFAR工厂。--model resnet50/resnet101直接复用既有ImageNet结构（7×7 stride2及maxpool）；CIFAR分类头100类，原生32输入及原预处理保留。--model cifar_resnet18/34保留原结构，新增cifar_resnet50使用3×3 stride1入口并复用既有Bottleneck类；既有Bottleneck的stride位置及最后BN零scale初始化均保留，不宣称完整复刻官方PyTorch模型。配置与CLI允许显式选择这些模型；CIFAR预设默认34不变。MNIST另提供mnist_cnn、mnist_mlp，均无BN/dropout；默认CNN为Conv16/pool、Conv32/pool、Dense64、10类头，MLP为128/64两隐藏层。MNIST也可显式选择现有ResNet，输入通道由数据确定为1，不暗中改stem。
- **数据准备：** 新增src/data/mnist_prepare.py及scripts/prepare_mnist.py，提供plan/download/verify。沿用完整文件校验、TLS、准备锁与原子发布辅助函数；四份原始IDX gzip采用torchvision官方MNIST loader列出的HTTPS镜像及MD5（https://raw.githubusercontent.com/pytorch/vision/main/torchvision/datasets/mnist.py），严格检查magic、60000/10000计数、28×28形状、长度与0–9标签范围；NumPy缓存另有SHA256 manifest及complete标记。缓存只含干净来源，下载/加载不依赖Torch或TensorFlow。现有坏文件不覆盖；已完成下载复用，单个.partial重试从头下载，不新增断点续传承诺。默认数据路径../data/mnist。
- **MNIST噪声定义与研究边界：** 新增src/data/mnist.py。--label-noise-percent是专属生成参数，0–100百分数；固定noise_seed先产生训练索引permutation，再生成全体1–9偏移，选择floor(N*p/100+.5)个索引，将标签偏移模10，保证被选标签改变且在另外9类均匀采样。完整数据20%恰为12000/60000；训练seed与noise_seed独立，三个方法共享固定标签，不每batch/epoch重生成。noise_percent继续为实际比例断言，CIFAR官方40.2%接口不改义。0%自动clean，其他自动noisy；只改变data_mode=clean亦清零MNIST生成比例。记录生成算法版本、实际比例、观察标签hash、分组与视图计数，配置/噪声变动导致不同数据指纹。使用合成污染属于新的机制验证，教授MNIST模型与配方仍未知，无理论/实证性能保证。
- **输入、评价与训练连接：** 原生28×28×1 float32/255，无随机裁剪/翻转。ImageBatchSource复用原shuffle/drop-last/恢复；evaluation_batches按reader.channels分配padding，原数据默认3不变。initialize新增可选channels=3；model_adapter同时支持BN状态和空状态小模型。训练batch仍仅images/观察labels/valid_mask，原标签和污染mask只用于固定审计。复用GroupedEvaluation，记录clean、corrupted_noisy、corrupted_original与不加噪的官方test；空组记录0及缺失指标，不用test选best。训练、timing、分组CE、EMA状态、Adam moments及checkpoint延续现有files/runs/logs协议，旧observer保持禁用。
- **配置与兼容：** 新增configs/tpu/mnist/dpco_adam.toml，用户选定CNN/20%/noise_seed0，探索性seed42/B128、Adam(.9,.999,1e-8)、lr.001/cosine至1e-6、beta_ref.99、L2=0、9360步（20个drop-last数据遍历）、eval468、latest2340；不是教授配方或已优化超参数。run_name包含模型、生成比例及noise seed。共享launcher、child与配置检查CLI透传--model、--label-noise-percent等；dataset切换清理不兼容标签配置。DataConfig新增字段默认0，旧恢复metadata缺失该字段时仅内存补0比较，不改写旧metadata。
- **涉及文件：** 新增src/data/mnist.py、mnist_prepare.py，src/models/classification.py、mnist.py，scripts/prepare_mnist.py，configs/tpu/mnist/dpco_adam.toml，docs/mnist.md，tests/test_mnist.py、test_model_selection.py；修改src/config.py、cli.py、data/classification.py、data/images.py、models/cifar_resnet.py、models/resnet.py、training/launch.py、training/evaluation.py、training/experiment.py、training/results.py，scripts/launch_tpu.py、train_classification.py，tests/test_cifar100n.py，README.md、docs/cifar100n.md及本文件。未修改src/methods/dpco_history.py、Adam更新公式或旧结果。
- **本地验证：** 定向运行test_model_selection、test_cifar100n、test_mnist、test_config、test_suite、test_classification、test_dpco_history、test_checkpoint_controls、test_optimizer_options、test_results，共82项CPU检查通过（33.377秒）。覆盖模拟四原始IDX文件完整60000/10000下载/解析、校验拒绝/缓存复用、固定噪声精确计数、单通道padding、固定分组CE独立NumPy核对、MNIST三组真实训练入口2步及checkpoint精确恢复；两种50完整模型eval_shape确认stem及2048维head，并用缩小Bottleneck骨干经真实入口训练/恢复。早期61项检查有1项沿用旧“CIFAR必须拒绝resnet50”断言失败，按新授权改成拒绝MNIST-only模型后，上述82项全部通过。
- **额外兼容与并行验证：** 对CIFAR旧metadata人为移除新增字段后，三组从p50恢复的state逐项精确一致且metadata字节不变，定向检查通过（4.483秒）。与HEAD的旧实现比较缩小ResNet及CIFAR BasicBlock，初始化参数/BN、train logits及更新BN逐项精确相同。全部15份TOML通过配置校验；CIFAR34/既有50/native50及MNISTCNN/MLP/既有50各三组dry-run通过，子命令参数回传一致；MNIST source plan通过。另在四个模拟CPU设备执行灰度CNN/EMA/Flip/Adam真实入口2步，分组评价padding与checkpoint计数正确；不把CPU模拟称为TPU实机验证。git diff --check通过。
- **文档、输出与未完成项：** docs/mnist.md提供绝对项目Python路径的nohup下载与串行三组训练命令、stdin=/dev/null、独立日志/PID和查看方式，说明新服务器需匹配execution拓扑；README与CIFAR文档说明两个50名称的结构区别。所有本地训练/下载检查均在临时fixture目录，未下载真实MNIST、启动正式服务器训练、改写原始Results、提交或推送。完整真实数据准备、TPU实机执行、长程收敛与方法优劣尚待用户验证；当前CIFAR beta消融不改模型或配置，不因本功能接入自动切换到50。


### 2026-10-30 / DPCO-0030：制定MNIST三方法配对机制验证参数与启动命令

- **用户请求与授权范围：** 用户要求给出一组合理MNIST参数，检验能否出现教授描述的DPCO效果。本轮读取两级协议、最近记录、MNIST预设/实现/文档和launcher，提供实验方案与nohup命令；仅追加本研究记录，不修改源代码、预设配置或启动服务器任务。
- **外部依据与边界：** 核对Adam原论文Algorithm1（https://arxiv.org/pdf/1412.6980）给出的通用起点alpha=.001、beta1=.9、beta2=.999、epsilon1e-8；核对Keras官方MNIST CNN示例（https://keras.io/examples/vision/mnist_convnet/）采用原生28×28×1、uint8/255、Adam/B128及15轮干净训练。Keras示例网络大小、dropout、validation划分与本项目不同，不能转用其99%性能或15轮结论作为本项目带噪DPCO保证。教授完整模型/噪声/超参数未知，本次是其选择性学习现象的机制验证，不称严格配方复现。
- **预先固定的首轮方案：** 使用用户已选择的mnist_cnn无BN/dropout模型、60000训练/10000官方test、20%精确固定对称错标（12000条，其余48000），noise_seed=0独立于训练seed。三方法adam/dpco_filter/dpco_flip，贡献权重分别全部保留/负align0/负align−1；三个训练seed42/43/44，共九个串行run，各seed的方法共享初始参数/数据顺序/污染图。B128，50个drop-last遍历=468×50=23400步，Adam(.9,.999,1e-8)、峰值lr.001/cosine至1e-6、L2=0、eval每468步、checkpoint每2340步并开启保存。50轮是为同时观察初期学习与后期错标记忆的预设探索预算，不是论文规定或保证充分收敛。不按test峰值早停选模型。
- **reference选择说明：** 本轮命令显式覆盖预设beta_ref=.99为.9，采用名义约10步的较短历史作首轮起点，以减少历史滞后的可能影响；这是设计判断而非MNIST性能证据或教授指定值。Adam beta1亦为.9，但reference与Adam moments仍为独立状态；不因此把两者合并。仅一个beta下的结果不能断言DPCO在所有历史设置中成功或失败；后续敏感性另行预先设计，不反复按官方test调参。
- **评价判据：** 优先查看group_evaluation.csv中固定clean原标签CE下降且学习未被明显牺牲；corrupted_noisy对错误标签CE较普通Adam维持较高、错误记忆较少；同时corrupted_original对原标签的CE/accuracy表现更好或保留有效学习，以区分选择性抑噪与整体欠拟合。官方test CE/top1为辅助泛化结果，报告固定最终预算和完整曲线，三训练seed做配对均值/波动；不能只凭整体train CE高或corrupted_noisy高判成功，也不要求clean训练CE必须低于已近零的过拟合Adam才承认选择性现象。固定noise_seed0的重复只覆盖该污染图下的初始化/顺序波动，不覆盖不同污染实现的方差；单组不出现现象不反驳教授其他条件下的报告。
- **启动与输出：** 提供绝对服务器Python /home/jason_chia925_gmail_com/Project_DPCO/.venv/bin/python，配置configs/tpu/mnist/dpco_adam.toml，显式模型/生成比例/实际20%断言/noise_seed与训练参数；--download在首次运行准备和校验缓存，后续复用。外层nohup、stdin=/dev/null、stdout/stderr到results/logs独立套件日志、后台&、保存PID并提供查看命令；run_suite --wait串行九任务并保留每run files/runs/logs与子进程日志。三方法套件不共用--negative-weight -1选项，以免与filter的0别名冲突。假定沿用现有四本地TPU拓扑，异机路径/拓扑需匹配实际环境，不隐式GPU/CPU回退。
- **验证与未完成项：** 本地完整CLI加--dry-run解析九份plan，逐一断言seed顺序、方法负权重None/0/−1、DPCO beta .9、CNN、23400步/B128、Adam/lr、20%生成与断言、noise_seed0、download、eval468、checkpoint2340及关键child参数透传，全部通过；核算floor(60000/128)=468及23400/468=50。文档diff检查通过。没有下载真实数据、运行模型测试或正式训练、改变预设、提交或推送；有效性结论待用户实际实验。


### 2026-10-30 / DPCO-0031：澄清accuracy最终目标与CE代理/贡献目标，调整MNIST评价优先级

- **用户请求与范围：** 用户指出不能只比较loss，认为本身优化目标是acc。本轮核对两级协议、最近记录、组会转写05:17–11:42及当前任务/EMA/评价源码，作概念澄清并记录研究评价优先级；未获得新代码修改授权，仅追加本文件，不改算法、命令或正在运行的任务。
- **会议与实现事实：** 组会09:42–10:48强调loss低未必效果好；10:48–11:17明确指出accuracy不可直接作为通常的可微目标，需要surrogate。当前tasks/classification.py计算逐样本CE及预测错误/accuracy统计；methods/dpco_history.py的g_i来自CE梯度，r是raw CE batch-gradient EMA，评分r^Tg_i决定权重；更新仍是编辑后梯度交Adam，未对accuracy求梯度。给定r的独立贡献子问题可写为max_{w_i∈[-1,1]} r^T(Σw_i g_i/B)，它不等于max accuracy，也没有保证多步test accuracy单调提高。0–1 top1在预测类别不变区域对参数局部为常数、通常梯度为0，在决策切换处可不连续/不可微，不能把现有CE梯度叫accuracy梯度。
- **解释与研究边界：** 最终任务追求更准确分类，可以把accuracy视为任务层面的优化目标；代码层面的可微代理、给定reference的贡献优化和最终评价指标必须区分。CE下降与accuracy提高不等价，正确类别置信度变化而argmax不变时CE可变、accuracy不变。DPCO也不保证是某个固定普通CE的标准下降法。各方法不同signed/加权训练目标值不宜直接排序，但同一固定数据/标签上的普通CE仍是可比的概率预测质量度量，无需丢弃。此前CIFAR Flip较低test CE伴随明显较差top1说明二者不能互代，不能据低CE宣称分类性能成功。
- **追加调整DPCO-0030评价表述：** 其“官方test CE/top1为辅助”作为整体算法优劣排序过弱，按用户强调的任务目的修正为：固定最终预算下干净官方test top1及三训练seed配对结果是总体分类效果主指标；不按test峰值选checkpoint或据test调参。教授controlled verification仍需分组机制证据：clean原标签accuracy保持良好，corrupted_original accuracy/CE说明是否保留真实类别学习，corrupted_noisy accuracy/CE说明错误标签记忆；低噪声标签accuracy本身也可能来自整体欠拟合，必须联合clean与test判断。train观察标签accuracy越高未必越好，因为含12000个错标签。只复现选择性现象与证明总体泛化优于Adam为不同结论，需分别报告。
- **现有输出与验证：** evaluation.csv已含val_top1（当前为官方test）、val_ce；group_evaluation.csv已含各组top1/ce；train_steps.csv已有train_top1。无需改动上一轮MNIST启动命令或新增记录功能，即可按上述优先级分析。静态核对字段与源码一致，文档diff检查通过；没有运行新测试/训练、提出新的性能保证、提交或推送。原标签仍仅用于观察，不进入训练reference或权重。


### 2026-10-30 / DPCO-0032：核实教授MNIST口头报告与flip的证据层级

- **用户请求与范围：** 用户要求再次回看组会，概括教授已做的MNIST结果、是否使用flip。本轮重读两级协议、近期记录及两份组会MD的相关段落，仅追加核对记录，不修改代码/配置、实验命令或原会议文件，不启动训练。
- **明确记录：** 转写31:27–31:44（第147行）对“reference借鉴Adam确定后，闭式解还是flip，所以保持flip去做？”明确回答“对”；这证明教授认可后续方法保留flip。32:30–33:26（第155/159行）提出controlled verification希望clean loss低、corrupted loss高；33:40–33:52（第163行）说“这些实验我已经做完了……在MNIST上已经跑完了”，确认其MNIST简化实验已经做过。33:52–34:21（第165/167行）讨论SGD交替flip与建议先Adam，34:35–35:10（第171/173行）布置discard/flip和不同signal对照。
- **上下文推断与限制：** 围绕flip及clean/corrupted受控行为讨论后报告MNIST完成，可合理推断其小实验与该贡献干预方向相关，flip很可能是其中操作；但“已完成MNIST实验”的一句话没有逐项列出本人实际使用的reference、flip频率、optimizer或baseline，不能将上下文推断升级为完整配方事实。尤其不能断言已验证的就是当前raw含当前batch EMA+每step整梯度Flip+Adam，或宣称已证明该组合在accuracy上优于Adam。记录也没有明确逐指标公布其MNIST成功程度、数值或曲线；“clean低、corrupted高”首先是明确实验要求，其已完成相应现象验证的理解来自语境。
- **未知结果与避免混淆：** MNIST具体模型、噪声类型/比例、beta、lr、训练轮数、clean/corrupted loss标签口径、实际accuracy及相对Adam提升幅度均未记录。建议先Adam不等于其本人已完成的全部MNIST实验必用Adam；后续引入历史signal不等于本人此前MNIST必用该历史版本。本文此前“小规模正面验证”的说法应按此口头报告和上下文推断理解，不能作为已经取得原始数值结果的表述。两份MD是同次会议的转写与整理，不算两次独立实验佐证。
- **验证结果及未完成项：** 已逐项核对原转写时间戳与总结中的来源注记，最终回答明确区分记录/推断/未记录；git diff --check通过。仅本文件追加，无代码修改、模型测试、训练、提交或推送；教授实际运行配方和结果仍需原始代码/图表或进一步信息才能确认。


### 2026-10-30 / DPCO-0033：读取MNIST九组CSV，分析train accuracy与选择性抑噪

- **用户请求与范围：** 用户导入Results/Minist结果，要求先读数据分析，更多关注train acc，初步认为Flip未达到教授预期，之后自行画图。本轮只读分析及生成研究报告/派生JSON，不修改训练/绘图源代码、配置或原始CSV，不启动训练。读取两级协议与近期记录，应用Spreadsheets技能的只读/科学数据分析规范，原始记录保留；初次外层git status失败后在DPCO内核对状态，已有本文件未提交记录完整保留。
- **输入完整性：** 目录只有51份CSV，无metadata/log/checkpoint或原标签缓存。九组为Adam/Filter/Flip×seed42/43/44，均summary completed，23400连续更新、2995200样本出现；合计210600行train_steps、459行evaluation、1377行固定分组、140400行dpco_steps。每步B128，lr逐项符合cosine.001→1e-6，51个评价节点为0至23400每468步，50个drop-last数据遍历；clean48000、corrupted12000、test10000。实际负权重日志0/−1、EMA计数随step正确；同seed三组的初始test及分组指标完全一致。目录标记CNN/20%对称污染/noise_seed0/beta_ref.9与命令一致，但不能仅由命名认证模型、代码版本、完整优化器设置、噪声指纹或硬件；无完整配置元信息的限制已明确记录。
- **最终accuracy（3训练seed均值）：** 末468步有效样本加权online观察标签train acc为Adam83.3561%、Filter80.2311%、Flip78.6425%。23400步冻结模型全训练集观察标签acc为83.3644%/80.2372%/78.6494%；clean原标签acc99.2611%/99.4340%/98.2139%；corrupted错误标签acc19.7778%/3.4500%/.3917%；corrupted原标签acc75.5139%/94.5361%/97.7889%；全训练集原标签acc94.5117%/98.4544%/98.1289%。固定最终test为93.3533±1.1705%、97.7333±.0643%、98.1267±.1401%（±样本标准差ddof=1，不是CI）。当前Flip相对Adam总体原标签训练和test均改善，不能概括为方法完全未产生预期抗噪效果；clean及全原标签训练acc的最优方法并非Flip。
- **train acc精确分解：** 对同一冻结模型，观察标签acc=.8×clean_acc+.2×corrupted_noisy_acc；原标签acc=.8×clean_acc+.2×corrupted_original_acc。Flip观察标签acc比Adam低4.7150个百分点，其中clean代价贡献−.8378个百分点、减少匹配错误标签贡献−3.8772个百分点，约82.2%的表面下降来自后者；这是指标恒等式分解，非因果归因。完美预测原标签的分类器在20%强制错标下观察标签acc为80%，这是参照值而非观察标签acc上限，记住错标签可以更高。用户train曲线较低的观感在观察标签口径成立，不能直接作为真实分类能力差的证据。
- **配对与阶段变化：** Flip最终test相对Adam在42/43/44种子分别+5.41/+3.57/+5.34个百分点（均值+4.7733），相对Filter+.23/+.61/+.34（均值+.3933）；三次方向一致，但不能由三训练seed宣称普遍显著性或跨污染图稳健性。第5轮平均test：Adam98.55%、Flip94.27%；第10轮98.5433%/95.6833%；第50轮93.3533%/98.1267%。Adam观察标签train acc持续升高同时corrupted原标签acc从第5轮98.2472%降至最终75.5139%，与后期增加错误记忆/泛化变差一致；Flip明显学习慢，clean最终较Adam低1.0472个百分点、较Filter低1.2201个百分点。仅描述事后均值曲线：Adam峰98.6567%在第8轮、Filter98.5167%在第15轮、Flip98.1367%在第47轮；不能用这些test峰值选模型。当前最终预算优势不证明优于有独立validation停止/正则化的Adam。
- **loss与教授机制：** 最终clean CE均值Adam/Filter/Flip=.17350/.22895/.31749；corrupted错误标签CE=2.29435/3.11023/3.74913；corrupted原标签CE=.79408/.44120/.34167。Flip保留较高正确类别accuracy、几乎不匹配污染标签且最终test改善，为选择性学习提供正面证据；同时clean CE与clean acc未最优，不声称全面超越或严格复现教授未知配方。全程负alignment平均Filter38.2880%、Flip41.8589%，明显不是只处理20%错标的分类器；正确标签编辑不自动等于贡献优化错误。Flip编辑方向范数/原始范数均值约2.0695，不能以梯度范数抵消消失解释变慢。无逐样本分数及checkpoint，不能识别precision/recall、每次编辑净收益或唯一失败/成功机制。
- **研究产物与来源：** 在results/files/mnist_review_20261030_fhcubve_/新增analysis.md、analysis_data.json，含最终/逐seed/逐轮accuracy、CE、配对差异、干预统计和来源链接；JSON保留459条派生逐轮记录、51份输入的相对路径/SHA256/行数与限制。未生成图表、XLSX或改原CSV；临时分析代码未写入项目源文件。报告表格结构已校验，原数据前后SHA256全部一致。
- **验证及后续边界：** 独立将group top1×sample_count还原整数正确数，重算全train两口径；将末轮逐batch top1×128还原整数后重算online acc，均与主计算一致。summary final字段逐项等于最终evaluation，组节点完整、lr全23400步、dpco计数与窗口总步数检查通过，git diff --check通过。后续优先画固定分组accuracy和test完整过程，同时标明online观察标签口径；如新增独立validation或历史/编辑消融需另行授权。没有运行模型、启动训练、提交或推送；不据此改掉Flip或追逐test调参。


### 2026-10-31 / DPCO-0034：澄清MNIST两套训练accuracy及教授clean subset与validation的区别

- **用户请求与范围：** 用户批注前轮accuracy表，询问为何Adam train acc高而Filter/Flip“全部训练集按原标签”更好，且教授要求clean loss是否指clean validation。重读两级协议、最近记录、组会原文及总结，核对当前评价/指标源码与已有MNIST分析报告。本轮只解释和追加记录，不修改源代码、配置、原始CSV或实验方案，不启动训练。
- **两个标签口径：** 本次60000张MNIST训练图中48000个标签保留、12000个标签被固定替换。online train_top1使用加噪后的实际训练标签，模型匹配错标签也计正确。“全部训练集按原标签”是冻结最终模型后，对同样60000张训练图片按加噪前原始MNIST标签作离线评价，由clean和corrupted_original的正确数合并，不是额外数据集、重新训练或训练reference使用真值，也不等同未见数据的泛化accuracy。clean组只指未污染的48000个训练样本，不能把60000张按原标签评价都称为clean subset。
- **指标核对与例子：** 一张原标签7、训练标签被改成2的图片，预测7在观察标签train acc中算错、在原标签accuracy中算对；预测2则相反。冻结最终模型的观察标签acc=.8*clean_acc+.2*corrupted_noisy_acc，原标签acc=.8*clean_acc+.2*corrupted_original_acc。Flip两者约78.65%/98.13%；Adam83.36%/94.51%，排名不同源于答案标签不同，不是数据矛盾。前轮表第一行使用末468步online均值（Flip78.64%），与最终模型完整评价78.65%的小差异另来自时间口径；本轮明确说明两点。
- **教授原话与未知划分：** 转写32:30–33:26及34:25–34:35要求clean subset loss低/下降、corrupted subset loss高，未明确说必须为独立clean validation，也没有完整规定clean subset来自train还是held-out集。当前以污染训练集内未污染48000样本实现，是具体落实选择，不应冒充会议已指定。全文唯一validation出现在15:43–16:24的DIVE reference来源介绍，不能据此推成此次实验必须用clean validation。独立validation用于调参/早停是助手额外建议，应与教授明确布置区分。
- **按教授clean-loss要求收紧评价：** 最终clean CE为Adam.17350、Filter.22895、Flip.31749，clean accuracy为99.2611%/99.4340%/98.2139%。因此就“同样未污染训练子集上Flip的loss是否低于两个对照”而言，当前最终结果没有胜出；Flip的clean loss下降且错标签记忆较少、最终test准确率更高属于其他明确观察，不能替代clean loss比较。教授原话“低/降低”未给出精确数值阈值或普遍相对优势承诺，不把末点比较扩展为整个理论被否定。此前“部分机制现象得到支持”不能解释成已经证明教授要求的全部比较均成立。
- **验证与未完成项：** 核对noisy_classification_evaluation三组均使用split=train、primary使用官方test，以及train_top1来自观察标签预测。现有evaluation.csv的val_top1为历史字段名，当前实际含义是官方test，未单独留出clean validation；其命名不能证明存在验证集。数值沿用前轮已独立复核的报告，无新增CSV处理或模型测试；git diff --check通过。仅本文件追加，未绘图、训练、提交或推送。


### 2026-10-31 / DPCO-0035：讨论clean训练CE三图数据来源与原标签accuracy的定期评价

- **用户请求与边界：** 用户拟画clean训练子集CE对step、对wallclock，以及全部训练集原标签accuracy对step，明确先讨论、不改代码，并询问原标签acc是否随每一步validate。本轮重读两级协议、近期记录，核对experiment.evaluate、评价触发、evaluation/recording字段及当前MNIST实际CSV，仅追加研究记录；不修改训练/绘图代码、配置或原始结果，不生成图。
- **评价频率与含义：** MNIST本次记录节点为0、468、936、…、23400，共51次，每次对冻结的当前参数作完整固定分组前向评价，不更新模型参数、Adam moments、EMA reference或BN状态；不是每个训练step都对60000张原标签做评价。每步记录的train_steps.train_top1是当前batch按观察标签的online指标，不能替代原标签训练accuracy。此处validate指训练数据审计评估，不代表独立validation集。
- **整体原标签accuracy重建：** group_evaluation每节点记录clean的48000张及corrupted_original的12000张完整原标签评价；二者分组互斥且覆盖60000张。按实际sample_count加权：(n_C*acc_C+n_N*acc_N_original)/(n_C+n_N)，本次为.8*acc_C+.2*acc_N_original，再乘100画百分数。整体值由已有分组准确合并，不是现有CSV里直接名为original_train_acc的一列，也无需重跑训练/模型。不得将corrupted_noisy误并入此图，亦不得把原标签评估理解为模型训练用原标签。
- **三张拟议图：** ①横轴记录step，纵轴group=clean的普通CE均值；②相同clean CE，横轴训练循环累计wall-clock分钟；③相同step节点，纵轴上述全训练集原标签accuracy。三者是训练集审计曲线，不冒称验证/测试集曲线；评价样本和标签固定，CE不使用signed/贡献权重。已有数据只能画51个真实节点及连接线，不插值宣称每步全量评估；当前先保留原始节点，平滑如后续加入应按评价点计并明确窗口，不照搬每步train曲线的100点窗口。
- **时间来源与范围：** group_evaluation没有elapsed_wall_s，需要同一run按step与evaluation.csv严格一一对应，取后者elapsed_wall_s/60。experiment.evaluate在同一state完成primary及全部group评价后记录该elapsed，表示这批评价指标可获得的累计时间，避免以train_steps的host dispatch时间冒充相应全量评价完成时间。横轴包括循环内JIT、评价、保存及训练开销，不包括进入实验循环前的TPU启动/下载准备/模型初始化；step0实际评价完成时间可大于0，不私自逐组平移清除开销。若要active训练时间需另用timing的train_window累计，属于另一时间口径，不能混标wallclock。
- **多seed统计建议与验证：** step图可在相同节点对42/43/44求均值±样本标准差；各seed墙钟节点不同，后续实现需明确采用各seed原时间线、平均节点时间还是同时间网格重采样，不能把同step误称同wallclock。静态核对当前Adam42的CSV为153条group与51条evaluation，字段/节点与上述一致；无需新测试或正式运行。git diff --check通过；未实现新图、改算法、启动训练、提交或推送。


### 2026-10-31 / DPCO-0036：讨论四张分组评价图与三seed显式路径接口

- **用户请求与授权边界：** 用户在上一轮明确先讨论、不改代码的基础上，补充全训练集原标签accuracy对wallclock图，询问现有plots脚本如何传入每方法三个seed目录，并贴出原nohup命令。本轮只读现有入口和协议、提出待实现接口并追加本记录；未将“可以接入”的讨论解释为新增绘图功能的明确代码授权。
- **现有能力核对：** plots/plot_dpco_training.py目前每方法一个--adam-dir/--flip-dir/--filter-dir字符串，读取train_steps.csv与timing.csv，画观察标签下的online训练指标；不读取group_evaluation.csv，也不汇总seed。当前argparse默认为store，重复同一参数只保留最后一个值，不能直接复制三次旧参数后声称已经画了三seed。路径解析现支持绝对路径、相对DPCO根目录路径和results/files下单个run名。Git起始只有本文件的历史追加变动，保留全部原文。
- **建议接口（尚未实现）：** 保留三个单数参数名，改为可重复收集显式run路径，每方法传42/43/44三个目录；单次传入仍兼容原命令。不按最新时间或最佳结果自动选run，不要求搬动或重命名原始目录。建议增加--plot-set clean-original选择新的四图组，保留旧训练指标入口；--eval-smooth-window 1按评价节点计且默认不平滑，独立于旧--smooth-window按训练更新计的定义。上述新选项及多路径语义在当前代码不可用，给用户的参数片段是拟定接口，不是可立即运行的命令。
- **四图定义和输入：** clean_train_ce_vs_step/time与original_train_accuracy_vs_step/time，纵轴分别为固定clean训练子集普通CE、全训练集原标签accuracy百分数，横轴为step或训练循环wall分钟。每run读取group_evaluation.csv，按sample_count合并clean与corrupted_original的top1，再与同run的evaluation.csv按step严格匹配elapsed_wall_s/60，不使用corrupted_noisy或train_top1替代。当前MNIST每run为51个真实评价节点，无需重训练；原标签指标是训练集审计而非独立validation。
- **三seed统计建议：** 每seed先独立重建完整原标签accuracy，再对同step取等权均值及ddof=1样本标准差。墙钟图建议在该方法三个seed的实际时间共同覆盖区间上对记录点作分段线性插值后计算等权均值及样本标准差；每处统计保持n=3，不外推、不把训练时长归一化成相同终点，明确插值只服务对齐而非新增测量。可保留三个seed原始淡线帮助核对；标准差阴影仅描述这三个训练seed的离散度，不是置信区间、不包含未运行的新噪声划分。数据/噪声/方法/seed配置核查应尽量使用metadata，缺失时说明目录名与显式参数的证据限制；不按输入顺序自动断言seed配对。
- **输出与未完成项：** 拟沿用Adam蓝、Flip红、Filter橙虚线、5×4英寸与axes高宽比.8，PNG/PDF及派生曲线和manifest输出DPCO/results/figures/<comparison_name>/，保留原始CSV与既有产物。原nohup后台包装在实现后可沿用，但当前没有执行依赖安装、绘图或服务器任务。仅静态接口核对与文档diff检查，不运行算法或渲染测试；待明确授权后再实现、验证并提供可执行九run命令。


### 2026-10-31 / DPCO-0037：实现多seed固定分组四图，并用MNIST真实结果验证

- **用户授权依据：** 用户明确要求“按照沟通来进行代码修改”，授权落实DPCO-0035/0036讨论的四图、显式多run输入、三seed统计、评价点平滑和原有绘图兼容。授权不扩展为训练算法、评价数据生产或实验超参数变更。本轮先读两级协议及近期记录；起始只有本文件历史追加改动，全部保留。
- **涉及文件：** 修改plots/plot_dpco_training.py、plots/README.md，新增tests/test_dpco_evaluation_plots.py，追加本文件；真实派生图保存在下述results/figures新目录。没有修改src、configs、依赖声明、既有结果或历史绘图入口scripts/plot_training_results.py。
- **入口与兼容：** --adam-dir/--flip-dir/--filter-dir改为可重复收集路径。新增--plot-set clean-original与--eval-smooth-window（默认1，不平滑），旧命令默认--plot-set training仍每方法一个run、生成原五图；旧模式传多run明确报错，避免静默只用最后一个。路径解析仍支持绝对路径、相对DPCO根路径及results/files下单个run名；重复实际路径拒绝，输入选择完全显式。
- **指标与输入校验：** 新模式只读group_evaluation.csv与evaluation.csv，不需要train_steps/timing。clean普通CE取未污染训练子集；全训练集原标签accuracy按clean和corrupted_original的实际sample_count加权再乘100，排除corrupted_noisy，比例不硬编码。要求label_source=original、分组完整且唯一、同step样本出现数精确匹配、step/samples_seen/wall严格递增、固定组大小一致、有限数值及accuracy为0–1比例。clean为空报错；显式零样本corrupted允许空指标，不伪造缺组。各比较run的固定组大小必须一致。同方法重复run的step/samples_seen网格必须完全相同，拒绝因缺失节点而悄悄减少参与数。
- **统计、时间与平滑：** 每run先重建指标，再在run内按最近E个评价节点作后向等权平滑（前缀不足时用已有记录），跨run等权取均值和ddof=1样本标准差，阴影非CI；单run标准差导出约定0，不表示不确定性已估计。Step图仅使用真实节点。时间图取评价完成时elapsed_wall_s/60，同方法所有run时间范围的交集内，以记录时间并集及交集端点为网格，逐run分段线性插值后统计，保持每处全部run参与；无外推、时长归一化或虚构更密的真实评价。原始淡线保留各run完整实际记录范围，--no-raw可隐藏。保留非零step0时间，包含循环内训练/JIT/评价/保存，排除循环前准备初始化；新模式只接受wall。旧--smooth-window在新模式不使用。样本标准差带完整显示，未在0/100边界裁剪。
- **元信息与可追溯性：** 有对应metadata时核验方法/Adam/EMA/负权重并使用配置seed；从标准run名读出的seed标为directory_name_unverified，元信息与目录seed矛盾或同方法重复已识别seed报错。元信息缺失、身份未认证、重复数/seed集合或配置/数据指纹不一致明确写入提示和manifest；不同训练seed不会再被误当不匹配训练设置。没有从输入顺序虚构seed或进行配对显著性推断。导出evaluation_runs.csv、evaluation_step_curves.csv、evaluation_time_curves.csv以及最终完成manifest，保留源文件SHA256、样本数、实际节点/seed来源、插值/平滑/SD定义、共同时间范围和脚本哈希；输入改变时拒绝完成manifest。
- **绘图与运行文档：** 新增clean_train_ce_vs_step/time和original_train_accuracy_vs_step/time，各PNG/PDF，仍为5×4英寸、PNG220DPI、axes高宽比.8，Adam蓝实线、Flip红实线、Filter橙虚线。输出results/figures/<新名称>/，拒绝覆盖。README说明两种模式、九个精确run名和完整服务器nohup命令，明确base可指向另一CSV根目录，提供日志/PID/查看方式与绝对服务器Python；没有擅自运行该服务器命令。
- **验证过程与结果：** 新增7项有独立数值预期的分组/多seed测试，加既有8项DPCO绘图及10项历史绘图，共25项全部通过（9.672秒）。覆盖非等大小分组的原标签权重、评价平滑、空corrupted、ddof=1、共同时间区间与插值边界、缺组/重复/标签口径/单位/非有限/样本数/时间倒退拒绝、重复seed/网格不齐/时间无交集、元信息身份、九目录真实CLI渲染、四PNG/PDF、导出行数/seed、输出防覆盖、源字节不变、颜色比例、原五图兼容及无第三方依赖help。初轮环境缺matplotlib，另有测试fixture目录编号被误作seed导致身份检查失败；已修正fixture名称并复用已有/private/tmp/sage-plotting-venv，不安装或修改依赖。Python AST、README两段bash -n及git diff --check通过。
- **真实MNIST产物与独立复核：** 读取外层Results/Minist/files九run，在results/figures/mnist_clean_original_3seeds_20261031_114630_957697/生成四PNG、四PDF、三CSV及manifest。逐张查看四图，无标签/图例裁剪，颜色与比例正确。独立将源top1×组样本数还原整数正确数，复核全部459个实际评价节点的整体原标签accuracy及时间、153个step汇总点的均值/样本标准差；18个输入CSV的当前SHA256与绘图前记录完全一致。末节点Adam/Flip/Filter clean CE=.17350320095/.31749141439/.22894647217，原标签train acc=94.5116667%/98.1288889%/98.4544444%，与既有分析一致。每run51评价点，三seed阴影不增加独立观测或新污染图证据。
- **理论边界与未完成项：** 本次只改变离线画图及其派生数据，无训练目标、reference、翻转逻辑或泛化保证新结论。clean子集与全部训练集原标签评价均非独立validation；真实输入无metadata，方法/seed/模型配置认证限制已写入manifest。没有启动训练、重新生成噪声、覆盖旧产物、提交或推送；用户同步修改后的代码到服务器后可运行README命令。未实现多seed旧online训练五图或active时间分组图，超出本轮约定范围。


### 2026-10-31 / DPCO-0038：解释MNIST Flip学习较慢与固定终点抗噪收益

- **用户请求与边界：** 用户报告服务器生成同样曲线，观察Flip学习较慢、最终可剔除noise影响并高于普通Adam。本轮核对两级协议、近期记录与既有MNIST分析报告，澄清观察和机制推断；只追加本记录，不修改代码、配置、数据或图，不启动任何任务。起始Git工作区干净。
- **当前数据支持：** 本次MNIST小CNN、固定20%对称强制错标、50轮、三个训练seed的设定下，Flip前期clean学习较慢，固定最终预算下全训练集原标签accuracy为98.1289%、Adam94.5117%，官方干净test为98.1267%、Adam93.3533%。污染训练子集按错误标签准确率Flip.3917%、Adam19.7778%；同一批图片按原标签准确率Flip97.7889%、Adam75.5139%。这些联合现象支持“较少记忆错误标签并保留真实类别学习”的抗噪解释，用户的主要趋势判断成立。
- **对剔除表述的限定：** 当前Flip没有删除污染样本，也没有获得标签真值来决定权重；它翻转负alignment样本梯度。负alignment不是错误标签的可靠等价标记，现有聚合结果不能证明每次操作精准识别错标、全部噪声影响被消除，或该机制具有普遍保证。研究表述宜为“抑制错误标签记忆/减轻噪声影响”，其中作用机制仍是由联合指标支持的解释而非已完成逐样本因果识别。
- **收益与代价共同报告：** clean未污染训练子集最终accuracy为Flip98.2139%、Adam99.2611%，clean CE为Flip.31749、Adam.17350，不能将整体原标签收益说成clean子集也全面胜出。Filter全训练集原标签98.4544%略高于Flip98.1289%，但最终test为97.7333%低于Flip98.1267%；评价指标决定排序，不能泛称Flip在三组所有指标最好。Adam早期三seed平均test曲线峰约98.6567%，高于Flip平均曲线峰约98.1367%；当前同预算终点优势主要体现后期较少噪声记忆，不证明优于有独立validation选停止时间的Adam，更不能用test峰值选模型。
- **验证与后续：** 本轮数值引用先前完整CSV及独立整数正确数复核结果，已对照analysis.md中的终点、分组及过程统计，没有重新计算或重画；git diff --check通过。结果限定于当前数据、污染图、模型及训练预算；教授未知实验配方的严格复现与更大数据集收益仍未完成。若后续需展示机制，可在已有记录上补充corrupted_noisy和corrupted_original曲线，但本轮没有实施新增绘图或改变实验。


### 2026-10-31 / DPCO-0039：仅比较imagenet目录中CIFAR-100N的reference beta消融

- **用户请求与范围：** 用户新增results/imagenet/files，要求只比较files，分析beta调整和后续方向，询问相较MNIST失败是否因为40.2%噪声太高。本轮按两级协议读取近期记录，应用Spreadsheets只读科学分析规范；只读该files内35个CSV，没有读取同级logs/metadata/runs，没有连接服务器、修改训练或绘图代码、改变参数或启动新实验。开始时本文件已有上轮未提交追加，完整保留。
- **首先纠正对象和beta口径：** 实际六run均命名cifar100n_noisy_cifar_resnet34，固定分组29900/20100、train50000/test10000，故本轮讨论CIFAR-100N而非ImageNet；目录外壳名字不改变数据含义。run名标记Adam、Filter ref beta=.99、原始/复跑Flip ref beta=.99、Flip ref beta=.9/.999；这里是reference beta消融，不能混同Adam二阶矩beta2。用户要求仅files，故未借现存元信息认证命名中的架构/beta/seed；CSV本身没有Adam beta2等完整配置。两种大小写Results/results在本机为同一文件对象，未重复计数或挪动目录。
- **输入与过程核对：** 六run均summary completed，78000连续更新、B128、9984000样本出现，201评价节点为0至78000每390步，每次clean/corrupted_noisy/corrupted_original三组。nominal200个drop-last遍历对应epoch_progress199.68。每个更新lr逐项符合cosine .0003到.000001；分组数、标签来源、样本出现数、有限值、整数正确数、summary终点、dpco权重/计数与timing窗口连续覆盖核对通过。初始test及分组数值完全一致；35个CSV前后SHA256不变。只有seed42，两个ref beta=.99的所有非计时训练、测试、分组指标完全相同，不能当作两个独立训练seed或计算有效标准差。
- **固定78000步终点（accuracy均为百分数）：** Adam test51.24、clean100、N错误标签99.9602、N原标签.01990、全训练原标签59.808；Filter .99为51.20、99.9967、99.9502、.02985、59.810；Flip .9为48.66、99.9465、99.8408、.04975、59.788；Flip .99原始与复跑均为26.10、33.9097、9.6866、17.1542、27.174；Flip .999为20.81、26.9699、8.6070、13.8806、21.708。全原标签acc由两个互斥组的整数正确数独立合并，而非观察标签train_top1。Filter最终较Adam仅差.04个百分点（10000测试图的4张），不能描述为两种方法都最终远低于Adam。Flip .9比.99提高22.56个百分点、比.999提高27.85个百分点，但仍比Adam低2.58个百分点。
- **与MNIST机制的差别：** .9虽然恢复大部分分类能力，但最终几乎完全记住污染标签，N原标签只10/20100正确；未复现MNIST中N原标签高、N错误标签低的组合。高beta两组不匹配错误标签的同时，clean也仅学到33.91%/26.97%，说明当前预算下有明显学习受阻与选择性不足，不能直接称抗噪成功。Adam和Filter全训练原标签约59.8%与其记住观察标签一致；不能因其普通训练loss接近0就当作已解决错标影响。
- **过程与reference证据：** 第10轮test：Adam48.58、Filter34.79、Flip .9 16.92、Flip .99 4.84、Flip .999 5.06；第50轮分别47.74、47.94、50.04、9.04、8.79。Adam事后最高test51.82在第22轮，Flip .9同为51.82在第47轮；峰值只是描述，不能按test选checkpoint或调参。Flip .9/.99/.999全程ref/raw余弦均值约.4029/.1446/.0484，负alignment比例33.329%/40.338%/43.835%，方向/raw范数比1.0411/1.1662/1.1672；余弦对象是当前带噪batch而非clean oracle，范数未经过Adam。结果支持测试reference时效性/当前batch占比/编辑强度假设，尚不能隔离唯一机制；不是梯度范数接近0的直接证据。
- **理论解释补充：** EMA记忆尺度约1/(1-beta)，.9/.99/.999约10/100/1000步，为教学近似而非硬窗口。更大beta可降平稳随机方差，但可能增加表示/参数非平稳变化下的滞后。原始梯度EMA仍含错误标签梯度，不自动产生clean参考方向；当前batch被纳入reference时，H_t^Tg_i展开含(1-beta)||g_i||^2/B的正自项，因此减小beta既改变历史平滑，也增强self成分，不能仅由.9表现变好证明历史reference更准确识噪。r^TD的贡献目标也不自动保证经Adam后的clean CE或accuracy改善。
- **40.2%因果边界与外部依据：** 本批20100/50000为参考标签与original不一致，按run名noisy100 human用于训练；不是已认证的绝对语义错标比例。MNIST20%均匀强制错标与CIFAR100N40.2%human噪声，同时改变类别数、图像、模型、BN/增强和噪声结构，无法归结单一噪声率。核对官方原论文 https://arxiv.org/html/2110.12088v2 Table1及§3.2/4.2，fine噪声40.20%、human具有instance-dependent结构且不同于常用合成模式；官方发布 https://github.com/UCSC-REAL/cifar-10-100n 亦提供human与经验类别转移矩阵合成对照。不据此宣称40.2%不可学习或某方案已有收益保证。
- **后续优先级建议（讨论，未执行）：** 优先补充负alignment在clean/N中的计数与分布，获取P(q<0|C)、P(q<0|N)、P(N|q<0)，真值只审计、不作训练信号；当前总负数不能回推识噪精度。固定ref beta=.9，复用已有w=-1、增加w=0/−.25与Adam小对照，检查能否兼顾clean学习和N原类别保留，而非盲目扩beta网格。为区分噪声率和任务，现有MNIST接口可比较20%与40.2%；现有CIFAR clean100可作零训练噪声控制。CIFAR现支持--no-is-human经验类别转移合成控制，实际比例随采样变动，非均匀对称20%生成器；更多同图像的固定20/40.2%对称噪声须另授权实现，noise-percent仍只是实际比例断言。若诊断显示早期误翻有效信号，再考虑明确的Adam预热后启用Flip、EMA持续累积及状态保留策略，或冻结Adam尺度的reference评分变体，这些不是当前代码已验证能力。新增策略和诊断均不因本轮分析自动获得代码修改授权。
- **研究产物与验证结果：** 在results/files/cifar100n_beta_review_20261031_gpo7zrz9/保存analysis.md、analysis_data.json，包含六run完整201节点轨迹、逐阶段干预统计、终点/过程/峰值表、非计时重复检测、35原始CSV链接/行数/哈希、理论与未来实验边界；没有新增xlsx、图或代码文件。文档数字与JSON逐项对照，源哈希再次复核不变，git diff --check通过。未完成项是新对照实验、分组alignment诊断、多seed稳健性及真实ImageNet结果，而非把当前CIFAR结果当作ImageNet证据。


### 2026-10-31 / DPCO-0040：澄清污染子集原标签accuracy的分母及整体排序

- **用户请求与边界：** 用户批注DPCO-0039终点表，询问Flip ref beta=.99的17.15%是否高于Adam的.02%，以及是否意味着Adam按原标签总体准确率只有.02%。本轮只解释并追加研究记录，不修改源代码、配置、图或输入CSV；起始已有本文件未提交追加，保留原文。
- **重新定位与数值核对：** 原先results/imagenet/files已不在原位置；通过文件清单定位到外层Results/Cifar100N/files（本轮未移动目录），读取Adam与Flip .99复跑的group_evaluation.csv中step78000行。污染子集均为20100张，按原标签正确数量Adam4、Flip3448，分别.0199005%/17.1542289%；clean子集29900张，正确数量Adam29900、Flip10139，即100%/33.909699%。同一污染子集按human错误标签正确数量分别20092/1947，即99.960199%/9.686567%。
- **解释与证据范围：** 用户对“只在污染20100张训练图片、按原标签评价”这一项的比较理解正确，不能把它推广为整个数据集或测试集的Adam准确率。示例原标签狗、观察标签被改猫时，预测猫在观察标签评价算对、按原标签算错；同一训练图片被记住错误标签与新测试图片分类表现是不同口径。未污染29900张按原标签正确数与污染组相加，得到全50000张原标签accuracy：Adam29904/50000=59.808%，Flip13587/50000=27.174%；对应独立官方test为51.24%/26.10%（沿用前轮已核对evaluation终点）。
- **研究判断及验证：** Flip在污染子集保留原类别方面好于Adam这一有限观察成立，同时其clean组明显受损，故未转化为整体准确率优势；17.15%不能单独证明已经有效识别噪声或算法整体更好。整数正确数合并与此前完整分析一致，git diff --check通过；没有新实验、训练、绘图、提交或推送。先前报告源路径保留为历史记录，本条记录当前实际位置。


### 2026-10-31 / DPCO-0041：讨论以reference beta=.9为起点补齐Filter及分阶段细化beta

- **用户请求与范围：** 用户认为Flip beta=.9的clean accuracy99.95%是有效起点，希望平衡clean和污染样本原标签表现，询问能否先关注beta=.9的Flip/Filter、是否应在.9与.99之间微调。本轮按协议阅读近期记录，仅提出具体实验设计、澄清判据并追加本条，不修改代码、配置、启动脚本或原数据，不运行训练。已有未提交开发记录保留。
- **起点判断：** .9下clean99.9465%证明当前设置能够充分拟合未污染训练样本，但N原标签.04975%、N错误标签99.8408%，所以“可学习”与“抗噪有效”仍需区分。现有Filter仅有ref beta=.99，不能替代同beta=.9的Filter；补齐.9两种干预对照具有辨识价值，不承诺Filter一定改善。clean准确率接近饱和时，仍需同时观察普通CE、学习速度及N原类别保留，不能只比较末点99.95%。
- **分阶段小实验建议（未执行）：** 第一阶段固定模型、数据/噪声图、B、lr调度、Adam参数、总步数、评价协议与seed，比较beta_ref={.9,.95} × negative_weight={−1,0}，并保留Adam；已有.9 Flip及匹配Adam可复用，因此seed42需要新增.9 Filter、.95 Flip、.95 Filter三run。先用这一小对照判断增大历史权重是否开始改善N原标签acc而clean仍学得好。若.95呈现有益趋势，再补.98 Flip/Filter；.99已有结果作历史锚点，.999暂不重复。不将.9到.99之间默认存在成功/最优点；若中间设置只破坏clean学习而不形成N原类别保留，优先审计reference区分力/贡献强度，而非继续密扫。
- **为何中间值值得测：** 教学近似记忆尺度1/(1-beta)：.9约10步、.95约20步、.98约50步、.99约100步，故.9与.99相隔的是十倍时间尺度，不能因beta小数相近视为微小变化。该尺度不是硬窗口或独立有效样本数；beta调节历史平均、时效性和当前batch自项，不是直接控制clean/noisy两组权重，效果不保证连续、单调或线性插值。
- **量化权衡与选择边界：** 本次全训练原标签A=.598*A_C+.402*A_N，其中A_N按污染子集原标签而非human错标签评价；若A_C减少d个百分点，A_N需增加超过(.598/.402)*d≈1.49d个百分点才使该总体训练accuracy提高。这是固定分组指标恒等式，并非测试泛化保证或用真值定义训练reference。对候选同时报告clean CE/acc、N原标签CE/acc、N错误标签acc及完整训练过程；机制诊断不以总负alignment比例冒充噪声识别精度。seed42小扫描只作探索，候选还需其他seed和独立验证选择，避免据官方test反复选参数。
- **验证及未完成项：** 数值沿用DPCO-0039/0040已复核记录，本轮无新增CSV分析、模型检查或绘图；git diff --check通过。所有上述run均是建议，未发起、未改变正在运行实验，也未把讨论当作代码或训练授权。


### 2026-10-31 / DPCO-0042：提供一次后台启动三个CIFAR-100N补充实验的命令

- **用户请求与边界：** 用户批注“只需要新增3个run：.9 Filter、.95 Flip、.95 Filter”，明确要求一次性启动命令。本轮提供可复制服务器命令、核对参数并追加记录，不新增或修改脚本/配置/算法文件，不替用户连接服务器或启动正式训练。此前本文件未提交追加完整保留。
- **命令组织：** 从/home/jason_chia925_gmail_com/Project_DPCO/DPCO运行，单个nohup bash后台任务内设set -euo pipefail，显式Python /home/jason_chia925_gmail_com/Project_DPCO/.venv/bin/python。第一条run_suite调用--methods dpco_filter --reference-beta .9；第一组完成退出后，第二条调用--methods dpco_flip dpco_filter --reference-beta .95。两者均--mode train --wait --seeds42，合计正好三个run，顺序为.9 Filter→.95 Flip→.95 Filter，无并发抢TPU；任一失败停止后续。别名自动确定negative_weight=0/−1，不向混合Flip/Filter套件共传一个冲突权重。
- **固定设置与产物：** configs/tpu/cifar100n/dpco_adam.toml；显式dataset=cifar100n、model=cifar_resnet34、noisy100/human/noise_seed0、actual40.2%断言且no-download复用既有数据，steps78000、B128、cosine3e-4→1e-6、Adam(.9,.999,1e-8)、L2=0、eval390步、checkpoint1950步且开启保存。不传resume，从共同seed初始化开始新run，继承原TPU拓扑与已关闭的旧probes。顶层stdout/stderr独立写results/logs/cifar100n_beta090_095_<时间戳>.log，stdin=/dev/null，&后台启动，保存外层PID到同名.pid并输出PID/日志；每run沿用results/files、runs、logs自动唯一目录，旧结果不覆盖。
- **验证结果：** 用本地依赖轻量run_suite --dry-run解析两次入口，合计三计划精确为(beta,weight)=(.9,0)、(.95,−1)、(.95,0)，核对模型、数据、步数、batch、Adam子进程数值参数、noise断言、checkpoint、评价及wait均符合预期；dry-run不保留run目录、不接触TPU或数据。完整拟发服务器命令bash -n通过。首次数值参数检查因epsilon字符串1e-08与1e-8格式不同失败，改为按数值核验后通过；未修改程序。git diff --check通过。
- **理论与未完成项：** 本轮没有新实验结果或收益保证，仅落实已讨论的小消融命令。服务器真实运行由用户执行，数据路径/四本地TPU环境沿用此前实验，结果仍待训练完成后比较clean及污染组原标签行为。没有安装依赖、下载数据、提交或推送。


### 2026-10-31 / DPCO-0043：核对ImageNet-1K既有支持与ImageNet受控标签噪声路线

- **用户请求与授权边界：** 用户已做MNIST和CIFAR-100N，询问ImageNet能否加噪、下一步选择ImageNet-100还是1K，并认为当前只接入普通100。本轮按协议只读代码、检索原始资料和讨论实验路线；仅追加本记录，不修改数据/训练/绘图源代码、配置、脚本或依赖，不准备数据或启动训练。起始本文件已有未提交研究追加，保留全部历史。
- **现有能力核对：** src/config.py已有imagenet100/imagenet1k，num_classes100/1000；src/data/imagenet_hf.label_mapping在1K使用0至999恒等映射，在100使用固定类表；共享prepare可完整缓存/校验100和1K，src/data/classification.open_training_images已有两分支，共享ResNet/Adam/EMA DPCO训练。现成DPCO preset为configs/tpu/dpco/imagenet100_resnet50.toml，但通过--dataset imagenet1k可解析为1K。因此当前“只有100 preset”和“底层不支持1K”应区分，不能说1K必须从零接入。
- **明确缺失：** PreparedImages缓存读取只有既有单标签get接口，没有ImageNet原标签/观察标签双视图、加噪标签映射、clean/corrupted分组。现CLI/config的label-noise-percent仅允许MNIST；ImageNet非clean模式在train_classification显式拒绝，noise-percent不是ImageNet生成器。固定三组评价目前只在MNIST/CIFAR分支组装。故干净1K入口存在，不等于带噪1K和现有四图所需分组指标已可用；不提供会默默保持clean的数据命令。
- **规模与预算：** 项目当前固定ImageNet-100类表预期train126689、validation5000，不能泛称所有ImageNet-100拆分都同样大小；1K预期train1281167、validation50000，和官方HF数据卡一致。相同输入尺寸/模型、batch与遍历数，1K约10.1倍样本/更新预算，非已测量的10.1倍wallclock保证。当前prepare磁盘预估100约19e9、1K约170e9字节另3e9保留，是代码保守检查而非真实下载体积/可用空间认证；100流式筛选也可能扫描较大1K来源，不能承诺下载成本仅十分之一。没有检查服务器数据缓存、授权、磁盘或设备性能。
- **噪声设计建议（待授权实现）：** 第一优先为固定ImageNet-100原训练图和原标签、随机初始化ResNet50，比较0%基线与20%固定对称强制错标；明确选中round(p*N)个训练样本，从另外K−1类均匀选错误类别，noise_seed独立于训练seed，跨方法和epoch复用同一映射；验证集不额外加噪。100子集应先按固定manifest映射为0至99，再在这100类内改标，不能产生分类头之外的标签。保存原标签/观察标签/污染mask、实际噪声率及映射哈希，作为原缓存上只读标签视图/sidecar，保证恢复和跨方法配对一致。沿用clean、corrupted_noisy、corrupted_original三组及全训练原标签评价。初步有稳定机制收益再做40%及类别依赖/语义近邻噪声，后者需预先固定有意义类对，不能把随意相邻class id当语义噪声。原标签只是数据集基准标签，不认证其语义绝对无误。
- **100与1K定位：** 100先解决224分辨率/ResNet50上机制可学习、识别/编辑是否具有选择性，便于补对照和多seed；1K用于在候选固定后验证类别/样本规模扩展。规模更大提供不同范围证据，不保证方法更好或clean/noisy梯度更易区分；当前CIFAR问题不因升1K自动解决。建议100先固定噪声/模型/训练预算，与Adam/Filter/Flip对比，随后在1K做少量固定候选；相同标签视图方案可共享，主要新增工作在数据标签、配置校验、分组评价及指纹，不需重写ResNet/Adam/DPCO。若1K采用固定分层审计子集降评价开销，必须标明估计范围并按总体组权重合并，不把子集accuracy冒称完整训练集全量测量。
- **已核对公开基准及区别：** CNWL官方 https://google.github.io/controlled-noisy-web-labels/ 提供Blue Mini-ImageNet合成噪声、Red Mini-ImageNet真实web噪声、0–80%多等级及共同clean validation；它们是另一ImageNet衍生数据，不能等同项目当前固定100类图像拆分。WebVision原论文 https://arxiv.org/abs/1708.02862 为对应ILSVRC1000概念的超过240万web图片及人工验证/测试，可作为后续真实web噪声评估；它不是将原1K训练图逐个替换标签的同一数据，不能默认所有训练图都有完整原标签可用于同样C/N原类别审计。官方数据卡 https://huggingface.co/datasets/ILSVRC/imagenet-1k 核实1K规模。ImageNet-C官方 https://github.com/hendrycks/robustness 是图像corruption鲁棒性评价，非本项目当前研究的训练标签错标协议。未声称存在已接入/统一官方的ImageNet-N human40.2%接口，也未承诺URL图像当前全部可获取。
- **验证结果与未完成项：** 本地对ImageNet DPCO preset加--dataset imagenet1k --model resnet50 --methods adam dpco_filter dpco_flip --seeds42 --mode train --dry-run，三计划均正确解析1000类、clean、Adam及DPCO EMA(.9)权重0/−1，未读取图像/下载/访问TPU或创建run。此为配置/分派静态验证，未验证服务器真实完整1K训练成功。代码核对与git diff --check通过；本轮没有新增实验结果、改动模型/噪声或给出未经测量的收敛/时间保证。


### 2026-10-31 / DPCO-0044：澄清CNWL作者官方基准与ImageNet原项目标签噪声协议

- **用户请求与边界：** 用户批注CNWL Blue/Red说明，询问该论文加噪方式是否有ImageNet官方加噪方式。本轮只读协议、近期记录并查原论文与官方项目网页，解释发布主体及噪声定义；仅追加本条，不修改代码、配置、原始数据、脚本或正在运行实验。已有未提交文档记录保留。
- **官方一词的区分：** ImageNet/ILSVRC原项目提供原始图片、标注和挑战评价资料；在本轮可检索的官方发布中未查到统一指定20%/40%训练标签噪声生成协议。此为检索范围内结论，不将未查到写成不存在任何ImageNet衍生噪声基准。CNWL为Jiang等ICML2020论文作者发布的公开噪声基准，是作者官方发布，不是ImageNet团队制定的标准；CIFAR-100N的“官方数据/接口”同样指其噪声基准作者发布，不能把二者与母数据集创建方混同。
- **原论文噪声定义核对：** https://proceedings.mlr.press/v119/jiang20c/jiang20c.pdf §3.1及脚注2明确Blue采用对称标签翻转，每样本以p概率变成另外K−1个类别之一，排除原标签；转移概率对角1−p、非对角p/(K−1)。p表示标签改错概率而非从含原标签的全部K类重新抽样的概率；有限样本Bernoulli抽样的实际计数仍需核验，不能把本项目拟用round(p*N)固定总量选择与论文作者发布的具体split视为逐样本完全相同。Red保持类别标签、将所选干净图片替换为已人工核实不符合该类别的web图片，可能包含既有类表之外的内容，不是仅把同一张ImageNet图片标签改错。
- **公开协议与迁移边界：** 原论文Table1给出Blue/Red Mini-ImageNet均100类，Blue60000训练、Red50000训练、共同5000验证，多档p=0,5,10,15,20,30,40,50,60,80%；这不是本项目固定ImageNet-100的126689训练图，也不是全ImageNet-1K。作者项目 https://google.github.io/controlled-noisy-web-labels/ 及download页提供标注/分割说明。若要严格benchmark优先复用其发布split；若在本项目100/1K上采用相同对称噪声模型，应表述为“采用CNWL/相关论文的噪声模型在ImageNet上构造受控实验”，同时公开类表、采样、seed、映射和实际比例，不能称ImageNet官方噪声或现成Blue数据集的精确复现。
- **来源与验证：** 核对PMLR论文入口 https://proceedings.mlr.press/v119/jiang20c.html 、上述原PDF与CNWL作者官网。ImageNet官方网页直接访问超时，使用搜索返回的官方ILSVRC2012下载页 https://www.image-net.org/challenges/LSVRC/2012/2012-downloads.php 与 https://www.image-net.org/download-images.php 的发布内容作有限核查；没有编造官方背书、默认噪声标准或声称完成全网站审计。未运行代码/下载数据或生成新研究结果；git diff --check通过。


### 2026-10-31 / DPCO-0045：核实近期顶会对CNWL基准及衍生设置的实际使用

- **用户请求与授权边界：** 用户询问CNWL加噪方式是否被近两年顶会论文使用。本轮检索正式会议论文入口并核对实验段落，追加研究记录；没有获得或使用新的代码修改授权，不修改源代码、配置、脚本、依赖或实验数据，不启动下载/训练、提交或推送。保留本文件已有未提交记录。
- **2026年明确实例：** CARE: Class-Adaptive Expert Consensus for Reliable Learning with Long-Tailed Noisy Labels，ICML2026，PMLR306:68314–68334，正式入口 https://proceedings.mlr.press/v306/li26cy.html 。作者全文 https://arxiv.org/html/2605.23254v1 §3.1明确以Jiang等2020（参考文献即CNWL论文）的mini-ImageNet为基础，经指数下采样形成长尾分布并注入真实web噪声，命名ImageNet-LTN^r；Table4使用NR=.4、IF=10/100。此为CNWL来源/真实web噪声路线的衍生实验使用，不是仅在related work引用，也不能冒称未经改变的原始平衡Red split。主设置为预训练CLIP ViT-B/16+AdaptFormer、SGD微调20epoch，与本项目随机初始化ResNet+Adam的准确率不能直接横比。正式PMLR PDF的raw GitHub链接被浏览工具拒绝octet-stream，实验细节据作者arXiv正文、会议归属据PMLR正式条目交叉核验。
- **较早明确实例（单列2024，不能冒充2025–2026）：** CVPR2024 Learning with Structural Labels for Learning with Noisy Labels，官方PDF https://openaccess.thecvf.com/content/CVPR2024/papers/Kim_Learning_with_Structural_Labels_for_Learning_with_Noisy_Labels_CVPR_2024_paper.pdf 的§4.1明确使用CNWL Red Mini-ImageNet，20/40/60/80%噪声并缩放至32×32；从官方PDF的搜索提取正文核实，直接open曾返回403。ECCV2024 An accurate detection is not all you need to combat label noise in web-noisy datasets，正式入口 https://www.ecva.net/papers/eccv_2024/papers_ECCV/html/6511_ECCV_2024_paper.php ，作者全文 https://arxiv.org/html/2407.05528v1 §4.4、§6.1明确CNWL20/40/60/80% web噪声、替换图片的协议、32×32 PreActResNet18训练；作者官方代码 https://github.com/PaulAlbert31/LSA 同时列出CNWL下载与训练。两篇均为2024会议背景证据，按当前2026-10-31不归入2025–2026年份范围。
- **结论与证据边界：** 可确认CNWL真实web噪声基准及其衍生设置近期仍有顶会实际采用，不能从一个2026衍生实例推断它是2025–2026最主流或每篇直接复用原始split。本轮未核实2025–2026直接使用未经改变的Blue Mini-ImageNet的正式顶会实例；不将普通few-shot mini-ImageNet、像素Gaussian noise、仅引用CNWL、under-review ICLR2026稿件或2025公布的旧NCR专利当作该证据。未查到不等于证明不存在。
- **对DPCO的研究含义：** Red可作为真实web噪声外部验证；受控机制诊断仍优先能保留每张图原标签/污染mask的合成错标设置，以便复用clean训练子集loss及污染组原标签accuracy审计。Red的替换图可能含类表外样本，不能默认每个污染样本都有100类内的完整原标签。若选择CNWL用于可比benchmark，需固定作者split、分辨率、初始化/预训练及评价协议；若在项目现有ImageNet100/1K上自行加噪，应明确称自建受控设置而非原始CNWL复现。此为实验设计判断，不构成效果保证或实现授权。
- **验证及未完成项：** 按正式入口和实验段落区分会议年份、数据实际使用与衍生协议；未进行数据可下载性或官方代码运行验证，未新增算法实验证据。文档差异检查通过；是否接入CNWL或自建ImageNet噪声仍待用户决定并另行授权。


### 2026-10-31 / DPCO-0046：核对CARE公开数据构造实现及mini-ImageNet与项目100/1K的区别

- **用户请求与授权边界：** 用户批注CARE ICML2026，询问是否公开加噪方式、能否采用、mini-ImageNet与普通100/1K的差别。本轮阅读两级协议、近期记录、作者论文/仓库及项目ImageNet加载计数；仅追加研究解释，不修改代码、配置、脚本、依赖、数据或启动正式任务。已有未提交记录保留。
- **比上一轮更具体的公开实现证据：** 通过GitHub连接器读取qwq123-study/CARE的datasets/lt_mini_imagenet.py（blob160991e9aa04bf70621393fb7cb3f15defc41771）、datasets/mini_imagenet.py及configs/data/mini_imagenet_ir100_nr40.yaml、mini_imagenet_ir10_nr40.yaml。作者论文 https://arxiv.org/html/2605.23254v1 §3.1与Table4公开长尾+web噪声和40%、IF10/100；代码提供更具体、可审计的构造流程，但本轮未执行或验证数据下载可用性。
- **流程与追加澄清：** LT_Dataset读取split/blue_noise_nl_0.0为干净训练池；读取red_noise_nl_0.8，并按image id不匹配^n.*筛出web图，使用其观察标签组成噪声池并打乱。干净组按n_c=floor(n_max*a^(c/(K-1)))、K100指数采样，配置IF10对应a=.1、IF100对应a=.01；论文的IF为头尾数量比，代码imb_factor为其倒数。设保留干净图M，追加噪声图数量int(M/(1-p)-M)，p=.4时约为2M/3，使最终混合集合噪声占比约40%；不是把M张内40%随机改标签。red_noise_nl_0.8是噪声候选来源，不代表最终80%。若候选池不足，代码切片不会自动补齐，应核验实际样本数和比例；比例为总体目标，不保证各类同为40%。该实现是先长尾下采样、再追加web图，不能直接等同原始Red保持总量的替换流程；本条细化DPCO-0045的高层描述，保留原文。
- **可采用范围与可复现边界：** 可复用其数据构造设置来比较Adam/DPCO Filter/Flip，并引用CARE及CNWL；复用数据不要求采用CARE的CLIP多专家纠标算法。主实验CARE使用预训练CLIP/AdaptFormer，不能把其准确率直接与随机初始化ResNet对照。公开代码依赖已有split/all_images/validation_all布局及本机绝对class name路径，没有据README自动下载CIFAR的说明推断mini-ImageNet也能一键下载。采样含set转换及默认random_seed0，严格配对需保存实际样本清单/顺序、标签、seed、版本和实际比例；本轮未认证跨进程逐图复现。原标签字段返回同一label不能被当成web图正确类别oracle。
- **数据区别：** CNWL官网 https://google.github.io/controlled-noisy-web-labels/ 指向的mini工具 https://github.com/yaoyao-liu/mini-imagenet-tools 描述经典mini为100类、每类600、总60000、常用84×84，并说明few-shot的64/16/20类拆分；这不等于CNWL/CARE普通100类分类评价。CNWL原论文 https://proceedings.mlr.press/v119/jiang20c/jiang20c.pdf Table1的Blue训练60000、Red50000、共同validation5000；CARE衍生训练量随长尾采样和追加比例变化，不能写死60000或50000。项目src/data/imagenet_hf.py固定类表ImageNet100预期train126689/val5000，100类映射由manifest指定；1K为train1281167/val50000，和 https://huggingface.co/datasets/ILSVRC/imagenet-1k 一致。普通ImageNet100的类表是具体实验约定，不能只因同为100类就认为与mini相同或图像/分割可交换。普通100/1K保留原图尺寸，224通常是训练裁剪设置而非原数据统一分辨率；mini也可重采样/放大但不能恢复已丢失细节。mini默认不自带标签噪声，噪声来自Blue/Red或后续构造。
- **DPCO路线判断与限制：** 若复现CARE数据设置，应完整使用其40% web噪声及IF10/100，保持同数据跨方法配对。若当前只想隔离抗噪机制，先做类别较平衡的CNWL Red或已有ImageNet100上的受控合成错标，可避免同时引入长尾造成混淆；这些是不同实验，不能统一称CARE精确复现。CNWL100类web池不能未经对应类映射就当完整1K噪声池；100/1K若采用随机翻标签，应称相应合成噪声协议而非CARE真实web噪声。Red/web图可有类表外内容，clean loss与干净val可用，污染图全量100类内原标签acc不保证有定义。
- **验证与未完成项：** 作者四份源码/配置只读核验，核对项目计数，无运行作者程序、下载数据或创建新实验；git diff --check通过。尚需用户选择机制诊断还是CARE长尾真实web噪声协议，具体接入及数据可用性验证均未实施，本轮讨论不构成代码授权。


### 2026-10-31 / DPCO-0047：按用户自然噪声目标澄清CARE沿用CNWL的范围

- **用户请求与偏好：** 用户明确看重CNWL自然噪声，询问CARE是否沿用自然噪声。本轮只核对和解释并追加本记录，无代码修改授权，不修改程序、配置、数据，不下载或训练。后续数据方案优先围绕用户的真实web错标目标，不继续默认要求以自行均匀随机改标替代该目标。
- **核对证据：** 重读 https://arxiv.org/html/2605.23254v1 §3.1及 https://google.github.io/controlled-noisy-web-labels/ ，通过GitHub连接器再次读取作者datasets/lt_mini_imagenet.py第24–70行，blob160991e9aa04bf70621393fb7cb3f15defc41771。CARE的mini-ImageNet实验确实使用CNWL Red的web错标图片和既有观察标签，在干净部分长尾采样后追加噪声图片，不是重新均匀随机生成错误类别；其CIFAR合成实验另有对称/非对称/joint噪声，不能把所有CARE实验统称自然噪声。
- **核心解释：** 随机抽取哪些既有自然错标样本进入训练集，与随机生成样本的错误标签是不同操作。前者控制比例/组成而仍沿用自然来源的错误；人工控制比例及长尾后也不应称原始未筛选网络分布。自行组装数据不必等于均匀随机翻标签，CARE就是复用自然错标池的例子。
- **路线调整与边界：** 若用户主要验证DPCO对自然噪声的效果，优先直接采用CNWL Red官方split、共同干净验证集及同split的Adam/Filter/Flip对照；20/40%可作为建议起点，并不要求先做合成错标，也不需因引用CARE而同步引入长尾或其CLIP纠标方法。CARE长尾版本可作为后续额外难度，若精确采用则保持其样本构造/IF与实际比例。上述建议未实施且不保证DPCO性能改善；web噪声样本仍不保证具备闭集正确类别标签。
- **验证及未完成项：** 文献与作者源码只读交叉核对，git diff --check通过。自然噪声数据的下载可用性、具体split选择与接入仍未执行；未新增实验结果、提交或推送。


### 2026-10-31 / DPCO-0048：按CNWL作者发布划分接入Red Mini-ImageNet自然噪声训练

- **用户明确授权与目的：** 用户批注CNWL自然错标及可控比例，要求“按照cnwl的mini-imagenet数据集的论文官网的方式，将该噪声数据集加入训练……按照论文作者定义的数据情况，修改接入现在的dpco的训练代码，并将这个cnwl的数据集的基本描述计入开发训练md文档”。本轮授权覆盖数据准备/加载、必要配置与CLI、共享训练评价接入和文档/验证；不扩展为CARE长尾算法、Blue随机错标、DPCO/Adam公式变更或正式服务器训练。先读两级AGENTS及最新记录；起始只有本文件已有历史追加，完整保留，无提交/推送。
- **数据基本描述和前文精度补充：** 来源Jiang、Huang、Liu、Yang，ICML2020，Beyond Synthetic Noise: Deep Learning on Controlled Noisy Labels。官网 https://google.github.io/controlled-noisy-web-labels/index.html 、下载说明 https://google.github.io/controlled-noisy-web-labels/download.html 、论文 https://proceedings.mlr.press/v119/jiang20c.html 。Red Mini-ImageNet是100类、84×84 RGB的真实web检索错标基准，原论文以人工3–5人核验的不符合检索类别图片替换部分干净图，按作者发布的固定split控制0/5/10/15/20/30/40/50/60/80%档位。Blue是对称合成错标，非本轮目标；不自行改标、不引入CARE长尾、不将本项目另一份ImageNet100/1K视为同一数据。所有档位共用5000张clean_validation。补充DPCO-0044至0046中的“Red50000”概括：官方TFDS目录给出的精确训练数为0/5/10/15/20/60档50000，30档49985、40档50010、50档49962、80档50008，不能为凑整数比例调整发布成员；本轮按该公开基数校验并记录加载后的实际错标率。来源 https://www.tensorflow.org/datasets/catalog/controlled_noisy_web_labels 。
- **作者/官方接口语义核对：** 读取官方TFDS builder（tensorflow/datasets的controlled_noisy_web_labels.py，blob bbbc776dca8a8e704a8651831d0e1fd700665419）、其dummy标注schema及发布说明；采用image_id/class_id两列split、mini-imagenet-annotations.json的data列表/每图record列表及image/id、image/uri、image/class/label、image/class/label/is_clean字段。类别名接受官网class_names.txt与TFDS class_name.txt变体，保留原行号标签0–99。干净图原标签只用于确认Red未改变其类别；web图确认来自已发布错误标注，训练时仅使用split观察标签。metadata来源文件内容SHA256用于配对/追溯，官网未提供本轮可核实的固定zip校验签名，不能把本地哈希当作作者真实性签名。
- **新增文件：** src/data/cnwl_prepare.py（官方元数据、ImageNet/Web图片准备及按档位不可变缓存）；src/data/cnwl.py（只读数据/增强和audit分组）；scripts/prepare_cnwl.py（plan/prepare/verify）；configs/tpu/cnwl/dpco_adam.toml；run_cnwl_suite.sh；docs/cnwl.md（完整基本描述、布局、指标、nohup命令和限制）；tests/test_cnwl.py。修改src/config.py、src/data/classification.py、src/training/launch.py、src/cli.py、scripts/launch_tpu.py、scripts/train_classification.py、src/training/evaluation.py、src/training/results.py、pyproject.toml、README.md及本文件。未修改既有原始结果、模型实现或方法更新公式。
- **准备与读取实现：** 数据名cnwl，Red-only，按作者split保留行顺序/ID/观察标签；严格检查100类名、clean Blue0来源、web错误标注、train/val分离、唯一ID及公开基数，拒绝不完整/自定义划分冒充官方。原始ImageNet训练tar内每类按JPEG数字编号排序，再用mini ID后八位的1-based位置取图，不能把mini序号直接当原图文件名后缀；验证图片按原validation ID匹配。也支持已合法取得且保留官方ID的clean_images/all_images、noisy_images与validation_all目录。按官方TFDS采用OpenCV color decode、INTER_AREA84、JPEG quality72；运行时训练用ImageNet归一化及随机resized-crop/flip，干净评价/组审计使用完整84、无随机增强。只声明数据及预处理兼容，不声称复现MentorMix训练超参数/模型/方法。
- **下载、失败和恢复边界：** 默认本地源，显式--download才抓取官网zip及当前split需要的web URI，不自动下载需要同意ImageNet条款的train/val tar，不自动镜像/重新检索/替图。并行下载有界，全部图片缺失/解码失败有明确报错与失败ID清单，不静默删样本或生成随机标签；SQLite暂存按已完成行续做、成功文件复用，单个中断HTTP请求重下而非字节续传。metadata解压只读取指定成员，避免路径越界；中断后能从已有zip补齐元数据。完成后存prepared/red_20或red_40等独立目录，manifest含源metadata哈希、归档位置/大小/mtime、类别、实际计数、处理方式、成品DB哈希和completion标记，训练只读并校验DB哈希；每run数据fingerprint纳入恢复检查。原始源文件可能随web变化，成品哈希保证当前实际输入可追溯，不保证所有历史URI长期可用。
- **参数和启动贯通：** data.cnwl_noise_percent / --cnwl-noise-percent选择官方整数档位，默认20；已有--noise-percent仍是实际率断言，--label-noise-percent仍MNIST-only。固定Red要求noise_type=red、is_human=true（人工核验发布数据，观察标签仍源自web）、noise_seed0；0档clean，其余noisy，CLI同步mode。父套件/子进程/配置检查入口均传递新参数，run名包含red20_official_split等档位。支持既有resnet50/101及native-stem cifar_resnet18/34/50，输入固定84；默认ResNet50随机初始化、batch128、Adam3e-4 cosine→1e-6、78000步、评价390、latest1950、reference beta=.9，Filter0/Flip−1，均是沿用探索预设而非经过CNWL调优或论文最优配置。非CNWL的as_dict不添加新参数，保留原有metadata/恢复配置身份；切换数据集重置专属噪声参数，不改变原数据算法。
- **评价与研究边界：** 沿用train_steps.csv/timing.csv/evaluation.csv及checkpoint/恢复。group_evaluation.csv只含clean（已知原标签）和corrupted_noisy（web观察标签）两组，空组显式空指标。is_clean只划分审计组，不进入batch、不用于reference/编辑选择。网络替换图可来自100类外，正确闭集类别未知，因此不生成corrupted_original或全部训练集原标签acc，不用观察标签冒充真值。主评价为官方共同clean_validation，沿用不自动存best的协议；clean train loss与验证acc可用于研究，未把训练audit称独立validation。旧training绘图可用；原clean-original四图依赖完整真值三组，不能直接用于CNWL，新增CNWL专用图不属于本轮实现。
- **依赖与输出：** 新增cnwl可选OpenCV依赖并纳入test extra，运行时JAX训练不依赖TensorFlow/PyTorch；data extra供准备阶段NumPy/Pillow/certifi。为本地验证仅在/private/tmp/dpco-cnwl-testdeps装OpenCV4.14，不改用户全局或服务器环境。docs/cnwl.md给出安装、准备和三组训练的nohup后台命令，stdin/dev/null、独立results/logs日志及PID/查看方式、显式项目Python；代码开发没有执行服务器正式命令。准备报告位于results/files/cnwl_prepare_<时间>；训练继续files/runs/logs三级同run名。
- **验证结果：** 55项相关测试通过（含9项CNWL测试及原config/suite/MNIST/CIFAR测试），共约18秒；本地原始tar与canonical图片两种准备路径逐图像素/标签一致、数字排序而非字典序/文件名后缀、metadata zip读取及中断补齐、错误标签/重复ID/越界/篡改拒绝、web URI下载模拟及403报错、缺图不发布与299行暂存后仅重做1行、nominal选择与actual断言区分、训练batch排除audit真值、分组CE与独立NumPy核对、3种方法真实共享runner/updater/EMA/CSV/checkpoint及p50到final逐项精确恢复。训练集成测试使用CPU小模型和明确合成夹具验证通路，不声称ResNet50 TPU性能或真实自然噪声学习结果。首轮一个CE断言仅差5.72e-7浮点累加误差，改成显式float32合理容差后通过；没有调整算法。shell bash -n、官方40档prepare plan（50010/5000）、三组Red20 wrapper dry-run、CLI父子传递和git diff --check通过。
- **验证产物与真实数据限制：** results/files/cnwl_integration_check_20261031_155223/保存validation.json和three_method_plan.json，results/logs/同名目录保存tests.log。官网zip通过浏览和获批curl实测均HTTP403，故未完成真实标注包/全量图片获取或完整Red准备；原始ImageNet归档也未在本次任务获取。人工取得原官方材料后可按docs/cnwl.md运行准备，旧web失效图仍须恢复同一图片，不能静默删除后宣称原benchmark。未启动正式训练、未测TPU、未产生CNWL研究准确率，不作DPCO收益保证。代码接入及本地验证完成，后续真实源可用性/服务器准备与实验结果尚待实际执行。


### 2026-10-31 / DPCO-0049：提供CNWL Red20、ResNet50、reference beta=.9三组一次启动命令

- **用户请求与边界：** 用户要求reference beta=.9，给出CNWL20%噪声的Adam、DPCO Filter、DPCO Flip训练代码，其他参数基本沿用之前CIFAR100N，并确认是否ResNet50。本轮只读协议与两份preset，核对命令及追加记录；不修改源代码/配置/脚本、不替用户启动服务器正式训练。起始Git干净，前轮修改已在用户现有状态中保留。
- **选定设置及模型说明：** 使用configs/tpu/cnwl/dpco_adam.toml，显式--dataset cnwl --model resnet50，随机初始化、输入84×84、100类；这是当前CNWL preset的既有ResNet50。沿用用户此前CIFAR正式长实验命令（而不是CIFAR TOML中的100步pilot）：seed42、B128、78000步、lr3e-4 cosine到1e-6、Adam beta1=.9/beta2=.999/epsilon1e-8、L2=0、无SGD momentum/Nesterov、390步评价、1950步存latest并开启checkpoint。Red20的50000张训练图每drop-last遍历390步，78000步为200次drop-last遍历，样本出现进度约199.68epoch。此为保持可比训练预算的探索设置，不宣称CNWL最优。
- **方法/噪声语义：** 同一套件--methods adam dpco_filter dpco_flip --wait，依次训练3run，Filter/Flip自动对应weight0/−1，不共传冲突negative-weight。--reference-beta .9只作用于两种DPCO的raw batch-gradient EMA，普通Adam没有该reference；Adam自身两矩betas单独给出。--cnwl-noise-percent20选择官方Red档位，--noise-type red --is-human --noise-seed0固定发布标签，--no-download复用完整cache，不把--noise-percent20实际率断言误作生成器。
- **后台与准备前置检查：** 一条nohup bash -c中set -euo pipefail，显式Python /home/jason_chia925_gmail_com/Project_DPCO/.venv/bin/python，先scripts/prepare_cnwl.py --stage verify --data-dir /home/jason_chia925_gmail_com/Project_DPCO/data/cnwl --cnwl-noise-percent20，再exec scripts/run_suite.py，校验失败停止且不开始TPU训练。不认为普通ImageNet缓存等于CNWL prepared/red_20；此前官方zip403未被本轮证明恢复可用。外层stdout/stderr写results/logs/cnwl_red20_resnet50_b09_<时间>.log、stdin/dev/null、&后台、同名.pid与echo PID/LOG；提供tail -f查看方式。每run仍分别写results/files、runs、logs同名目录。
- **验证与未完成项：** 本地run_suite --dry-run核验精确3计划、Red20/ResNet50/100类、预算/lr/eval/checkpoint、方法权重与reference beta、Adam子进程参数及wait；完整拟发命令bash -n通过、git diff --check通过。没有下载源数据、安装服务器依赖、连接TPU、启动训练、提交或推送；数据真实准备状态和实验收益待用户服务器实际校验/运行。


### 2026-10-31 / DPCO-0050：解释Red20缓存缺失并提供后台下载/准备命令

- **用户请求与边界：** 用户服务器报prepared/red_20/manifest.json不存在，要求服务器自动下载数据集命令。本轮读取协议、prepare入口/实现和最新记录，并核对官方数据说明，只提供现有程序的使用命令及追加文档；不将命令请求扩展成新数据源适配/下载器修改授权，不在本机或服务器执行全量准备/训练。保留本文件已有未提交DPCO-0049。
- **报错含义：** 上轮脚本先运行--stage verify，它只读完成缓存而不下载/构建，因此缺少manifest即尚未在该路径发布完整Red20缓存（或data-dir指错），不是Adam/ResNet/EMA训练错误。此前套件set -e，在校验失败后不继续启动三组训练；不建议删除检查或伪造manifest绕过数据准备。
- **实际命令：** 同一nohup bash后台任务中set -euo pipefail，显式项目Python先pip install -e .[data,cnwl]，再scripts/prepare_cnwl.py --stage prepare --data-dir /home/jason_chia925_gmail_com/Project_DPCO/data/cnwl --manual-dir <同目录>/raw --cnwl-noise-percent20 --download --workers8，成功后--stage verify。stdout/stderr写results/logs/cnwl_red20_prepare_<时间>.log，stdin/dev/null、&后台，保存.pid并输出PID/LOG及tail -f命令；prepare/verify报告由入口写results/files/cnwl_prepare_<时间>。这一步没有自动串接正式训练，准备确认成功后再运行DPCO-0049三组命令。
- **自动下载范围和必要源文件：** --download仅下载CNWL官方metadata zip、该Red20 split所需的原始web URI并准备缓存；干净图片仍需按官方流程先取得ILSVRC2012_img_train.tar和ILSVRC2012_img_val.tar，默认放data/cnwl/raw，已有完整官方源目录可用--manual-dir避免复制，也可按既有接口提供保留官方ID的clean_images/validation_all。官方 https://www.tensorflow.org/datasets/catalog/controlled_noisy_web_labels 明确列为manual download；https://google.github.io/controlled-noisy-web-labels/download.html 发布URI/标注/split，不是一个无需ImageNet原图即可完整下载的成品。普通ImageNet100或现有HF SQLite缓存不被当前CNWL raw适配器直接读取，不能只改路径就宣称兼容。若原始ImageNet源尚无，当前命令不能从空目录无条件完成整个数据集，不作相反承诺。
- **外部可用性与恢复限制：** 重新查看作者下载页，网页链接仍指向https://storage.googleapis.com/cnlw/dataset_no_images.zip，本轮浏览工具仍无法访问该zip，之前实际curl403的状态尚未获得恢复证据。若服务器也HTTP403，需取得原作者发布包后放raw/或恢复官方来源，重复verify不会下载解决；不把未验证镜像作为同一发布。已完成文件/SQLite行可复用，单个中断HTTP文件不承诺字节续传；旧web链接失效仍明确报错，不能静默删图或随机改标签。
- **验证结果及未完成项：** 完整拟发命令bash -n通过；现有prepare --stage plan解析相同data/manual目录、Red20/50000训练/5000验证、84像素、download=true及workers8，无网络/数据写入/TPU访问。git diff --check通过。尚未确认服务器是否已有原始ImageNet归档及官网zip在其网络下可访问；没有修改程序、安装服务器环境、生成真实CNWL缓存、启动训练、提交或推送。


### 2026-10-31 / DPCO-0051：实测CNWL标注包403权限响应并核对替代来源边界

- **用户请求与范围：** 用户服务器执行DPCO-0050准备命令后出现urllib HTTPError403，要求排查。本轮阅读协议/记录、核对官方来源与后续作者发布入口，执行本地有大小/时间限制的网络诊断并追加本记录；不修改代码/配置/脚本、不改数据定义或分辨率、不下载全量数据、不启动服务器训练。保留本文件此前未提交追加。
- **实际故障证据：** 对https://storage.googleapis.com/cnlw/dataset_no_images.zip重新发出诊断请求，得到HTTP403、379字节XML。GCS Code=AccessDenied，Details明确匿名caller没有storage.objects.get权限，同时保留“or it may not exist”的可能性；不能进一步断言文件已删除或任意Google登录即可恢复权限。对应代码下载路径在metadata_directory下载官方zip时会直接传播HTTPError；网络图片单图403会被捕获汇总，故用户目前未捕获的403高度符合首个metadata包失败，非Adam/ResNet参数或GPU问题。前轮本地通路检查不等于真实源可用性，当前84像素raw准备路线尚不可从官网无条件完成。
- **来源检索与替代候选：** 官网下载页、官方TFDS仍引用同一个受拒zip。核对Google Research/TFDS问题检索及多个后续项目，没有核实可直接替换该84像素原始元数据包的完整可用镜像。CVPR2021 FaMUS作者仓库 https://github.com/youjiangxu/FaMUS README（blob79c351272c2e097d9b535098a8feccad4690c291）明确提供32×32 CNWL TFRecord成品，链接 https://drive.google.com/file/d/12KLkFaIDLlQ4bYIQL7xVeqX3H1d0r4_o/view?usp=sharing 。作者含CNWL原作者Lu Jiang，是有明确论文作者来源的候选，不将其与未经核实网盘混同。baselines/code_mentormix_r32/README.md列出20/40/60/80档位目录；其dataset parser读取image/encoded、image/class/label，验证读取image/class/fine_label。现读代码未使用is_clean/id字段，不据此证明成品一定包含可还原clean mask的全部元数据。
- **替代可用性和兼容性限制：** 该Drive网页可识别文件名red_mini_imagenet_s32.zip，但本地对作者公布文件的usercontent下载端点仅请求前1KB、30秒超时且未取得数据字节；不能声称已验证可下载或断言它已失效。该包32像素TFRecord不同于当前84像素raw适配器，不能只替换zip URL直接训练；即使下载成功仍需核对实际记录/划分/clean标识并明确授权新增导入和配置，不能上采样后冒称原始84信息。自然错标来源可以沿用CNWL，但不保证当前分组审计所需字段齐全。
- **下一步研究/操作边界：** 保持当前84设置的路线是取得作者原metadata包或由发布方恢复链接权限（官网提供controlled-noisy-labels@googlegroups.com联系方式），不建议反复运行同一403命令、删除校验或重新随机造标签。FaMUS32成品为可考虑的另一条路线，先确认用户网络/浏览器能下载及包内信息，再讨论相应导入，不默认用户已同意改变实验输入分辨率。未通过工具给作者/其他人发消息，未提出已成功的一键替代命令。
- **验证与产物：** 诊断JSON存入results/files/cnwl_download_diagnosis_<本轮时间>/，官方响应XML及header存results/logs/同名目录；只有379字节错误正文和只读源码/网页，未取得数据图片。git diff --check通过。真实84源的可用性、FaMUS文件下载与字段完整性、服务器数据准备和训练仍未完成，不产生新实验结论或收益保证。

### 2026-10-31 / DPCO-0052：确认用户Mac可下载FaMUS成品包及后续检查边界

- **用户依据与范围：** 用户确认该Google Drive链接在本机Mac可以下载，服务器尚不清楚。本轮读取协议、开发记录和现有CNWL输入限制，仅核对与讨论获取路径并追加记录；该确认不构成修改数据读取器、依赖或实验分辨率的授权。
- **可用性与建议：** 将Mac可下载视为用户当前网络环境的报告，不外推服务器直连Drive也可用。可先在Mac完整下载作者发布的red_mini_imagenet_s32.zip，再沿用户现有SSH传输通道上传服务器；服务器地址、SSH别名、云项目和区域未知，不用内部TPU主机名编造可执行上传命令。下载完成后先取得本机实际文件路径进行只读检查，再确定导入工作。检索Downloads文件名未匹配到该包，不能据此断言用户未下载或其他目录不存在。
- **兼容性与证据边界：** 当前CNWL配置和读取器要求84×84准备缓存；FaMUS作者发布的是32×32 TFRecord包，取得文件本身不等于现有训练命令已可读取。需实际检查压缩包完整性、20%划分、样本数、字段以及clean标识/样本ID的可追踪性；不能预先保证clean训练子集曲线可恢复，不能把上采样称为原始84像素数据。自然噪声与具体发布版本的描述沿用0051，本轮没有新的算法理论或实验收益结论。
- **涉及文件、验证与未完成项：** 仅追加DPCO_dev.md；源码、脚本、配置、依赖和数据未修改。完成只读接口核对，git diff --check通过。实际成品包尚未由本代理取得或检查，服务器下载/上传可用性和适配范围待核实；未启动全量下载或训练，未提交或推送。

### 2026-10-31 / DPCO-0053：低开销检查用户下载的FaMUS CNWL32包

- **用户依据、目的与范围：** 用户告知已将数据放入可访问目录，并明确要求控制usage。本轮不联网、不启用代理、不安装依赖、不修改代码；用Python标准库查看ZIP目录、先抽查9条记录，再仅顺序读取0%、20%和clean_validation三个成员，未解压全包或读取其他噪声档位。追加本记录及小型检查报告，保留已有修改。
- **实际文件与划分：** 项目根目录red_mini_imagenet_s32.zip为1433495917字节，目录包含0/5/10/15/20/30/40/50/60/80%以及clean_validation。实际遍历确认0%和20%各50000条，验证集5000条，各含100类、标签范围0–99。三个成员均读至结尾并通过ZIP成员CRC检查，TFRecord长度边界检查通过；未执行TFRecord逐条CRC检查或全包所有成员完整性检查。三个目标成员顺序检查约1.7秒。
- **字段与重要限制：** 三个划分的全部记录仅含image/encoded、image/format、image/class/label、image/class/fine_label；format=raw、像素3072字节，与作者32×32×3说明一致。未发现is_clean或样本ID；全部记录fine_label与label相同。因此不能将fine_label误读为噪声图片的独立原始真值，无法直接复用MNIST按原标签准确率或官方clean训练子集审计。
- **有限匹配诊断而非噪声率估计：** 以原始像素SHA256匹配0%数据，20%中36892条图像可匹配，其中36891条还具有同样标签，1条匹配像素但标签不同，13108条像素未匹配。0%含49993种像素哈希，6个哈希关联多个类别，存在重复/冲突。匹配覆盖率不等于作者标注的clean比例，不能把13108/50000解释为实际26.216%噪声，也不能凭相同像素就承诺完整准确恢复clean mask。需要作者来源信息或进一步核实生成过程，不能将此启发式冒充发布标注。
- **产物与后续边界：** 检查报告为results/files/cnwl_archive_inspect_20261031_183507/inspection.json。本轮仅新增该诊断JSON及DPCO_dev.md记录，git diff --check通过。包可作为后续32像素TFRecord适配的本地来源，尚不被现有84像素缓存读取器直接支持；模型输入/增强、准备导入及分组指标的调整须在明确修改授权后实施。未上传服务器、下载其他文件、启动训练、提交或推送。

### 2026-10-31 / DPCO-0054：检索Hugging Face原始CNWL84来源并区分普通Mini-ImageNet

- **用户授权与目的：** 用户希望保留原始84像素CNWL路径，明确要求去HF寻找下载来源，继续控制usage。本轮仅查询公开目录API、少量候选数据卡/文件列表及官方说明，不下载大数据、不安装依赖、不修改程序或配置、不启动训练。网络查询遇沙箱DNS失败后依规则申请联网，随后使用系统可信证书解决Python默认证书链问题；未关闭TLS校验。
- **HF检索范围与结果：** API名称查询cnwl、cnlw、controlled_noisy、controlled-noisy、redmini均为空；imagenet-red/imagenet_red仅返回若干名称含reduced/redo的其他数据，mini-imagenet返回31个候选。此前mini_imagenet/miniimagenet也作同类检索。公开Web精确检索没有补出可验证的CNWL84成品源。结论限于本轮公开检索“未找到可核实镜像”，不声称整个HF绝对不存在、私有/未索引仓库不存在。最终8组目录查询保存results/files/cnwl_hf_search_20261031_184130/hf_search.json。
- **候选核对与排除边界：** Artonix/Mini-imagenet-84文件表仅见miniimagenet_train_84.npy、val_84.npy、test_84.npy，总约3.37GB且无数据卡，无法确认包含CNWL自然噪声档位/is_clean，不推荐当同一基准。timm/mini-imagenet数据卡明确是原分辨率普通ImageNet100类子集，50000/10000/5000，作者还说明类别/划分不匹配常引用Mini-ImageNet，不是CNWL替代。niuniandaji/mini-imagenet-c为ImageNet-C像素扰动鲁棒性子集，保留原标签，非自然错标训练集。nickypro/mini-imagenet页面为空；SKNahin/mini-imagenet-84by84页面本轮浏览不可访问，未据名称认定其来源或可用性。没有下载这些候选。
- **原始协议澄清：** 官方TFDS https://www.tensorflow.org/datasets/catalog/controlled_noisy_web_labels 再次确认84×84为预处理尺寸，Red包含10个噪声档位及共享clean validation，输出id/image/is_clean/label，标明Manual download required和Auto-cached:No。不是承诺官方有可直接取得的完整84像素ZIP；当前代码的84缓存属于按此流程生成的本地缓存。官方 https://google.github.io/controlled-noisy-web-labels/download.html 实际提供URL/标注/split元数据，仍需原ImageNet干净图及web图片。仅补普通84 Mini-ImageNet不能补回CNWL自然错标和官方clean标识；找到官方元数据镜像或已生成的原协议完整缓存才可解决对应缺口，且新缓存格式仍需检查兼容。
- **验证及未完成项：** 仅新增检索报告并追加本文件，git diff --check通过；保持0051的官方GCS403既有证据，本轮未重下载验证其恢复。没有找到可保证直接下载/直接训练的原始84成品URL，没有取得缺失元数据、发邮件联系作者、上传服务器、提交或推送；不将同分辨率数据或32像素上采样描述成原始CNWL84。

### 2026-10-31 / DPCO-0055：澄清mini-imagenet-tools可补干净图片但不能补CNWL自然噪声

- **用户请求与操作边界：** 用户提供yaoyao-liu/mini-imagenet-tools的Usage及链接，询问其数据是否可用。本轮只读该仓库README、生成器、官方TFDS说明及本项目既有准备接口，追加说明；未克隆仓库、下载ImageNet、修改代码/配置或启动训练。
- **可用部分与更正表述：** 可以将该工具及其依赖的ILSVRC2012_img_train.tar作为普通Mini-ImageNet干净图来源。工具描述100类、每类600张，默认84像素，64/16/20类为few-shot任务的训练/验证/测试划分；它不是CNWL作者的自然噪声数据发布页。TFDS的CNWL实现引用该工具仓库CSV选择干净图片，故两者确有来源关联，不能笼统表述为“该数据不能用”；但这种关联不赋予它CNWL web错标、噪声档位及is_clean标注。
- **协议差异与实际缺口：** 生成器只从ImageNet训练归档选图、重命名并缩放，不读取CNWL自然噪声标注/Red split，也不提供CNWL独立clean validation所需的原ImageNet验证图。生成器的few-shot val/test不应直接冒充CNWL clean validation。20%Red仍需CNWL元数据及官方指定web图；因此即使获得138GB训练归档，原先元数据403缺口仍在。官方Red20训练50000/验证5000不等同于该工具60000张的64/16/20类别划分。
- **接入建议与验证边界：** 当前准备器已经支持直接读取ILSVRC2012_img_train.tar和ILSVRC2012_img_val.tar；若两者已有，无需先运行该工具再缩放。若改用工具产物作为clean_images需保留并核对canonical ID/类别，默认JPEG与再次预处理可能不同，不能保证逐像素等同；未对实际产物做匹配或声明已即插即用。仅追加本开发文档，git diff --check通过，完整84像素自然噪声来源仍未补齐。

### 2026-10-31 / DPCO-0056：核对近期CNWL论文作者仓库是否发布完整数据

- **用户请求与授权边界：** 用户质疑仅检索HF不充分，要求核对近期引用CNWL的论文是否公开数据。本轮查询论文、作者README、有限目录/数据加载器及相关公开Issues/Releases；不下载图片、不安装环境、不修改代码、配置或依赖、不启动训练、不联系作者。控制范围，不将“查到使用数据”写成“查到完整数据下载”。
- **CARE（ICML2026）：** 作者仓库qwq123-study/CARE的README标明ICML2026，公开主分支22a43ddfaac13dc1625572cfd52f598274505e7c。本轮README、完整文件树、空Issues与空Releases未找到完整CNWL图片/标注包链接。datasets/lt_mini_imagenet.py（blob160991e9aa04bf70621393fb7cb3f15defc41771）从root/all_images、validation_all和split读取，干净池来自blue_noise_nl_0.0，web池从red_noise_nl_0.8按ID筛选后重组长尾；这说明代码依赖预先整理的CNWL，不证明下载源公开，也不等于直接沿用标准Red20训练集。原图实际尺寸无法仅由该加载器确认。
- **CLIPCleaner（ACM MM2024）：** MrChenFeng/CLIPCleaner_ACMMM2024 README（blob569c2ab5f2b69866300c4c6a412d4a4e4a635222）给出red_imagenet本地dataset_path及noise_ratio示例；README、文件树、全部5个公开Issues和空Releases未找到完整CNWL下载链接。datasets/dataloader_redimagenet.py（blob09fff2c16ada0d902de8f72b43de69928d7c8a36）1072行读取mini-imagenet-annotations.json，1084行明确使用image/class/label/is_clean，1090行使用split/red_noise_nl_<ratio>，1101行读取all_images。该项目保留分组真值的接口，比仅有32TFRecord更适合作为索取官方标注/图像对应关系的线索；未确认其本地原图分辨率，不因后续transform尺寸推断原始尺寸。
- **其他近期核对：** PASS作者仓库arpit2412/PASS-NoisyLabel当前树0573db04aef0ae5c686fa74dee678f481db835f4与README只提供CIFAR训练相关公开实现，未找到Red Mini-ImageNet下载。其论文2025年12月在线、2026卷期可证实使用Red基准，但不能推定复现数据也公开。meruemon/ACD-U（2026预印本）当前树1dd839c7c5eb989a93c6c29bf749e157c86dc931、README明确限量发布，数据/训练模型/完整文档拟待评审后补充，未找到CNWL数据。ECCV2024 arpit2412/NoiseRateLearning README列Red实验但当前主目录仅LICENSE、NoiseRateEstimator.py、README，未给完整数据包。更早InstanceGM（WACV2023）README明确要求本地已备数据并指回CNWL官网；PLS/SNCF的README未补出原始84完整镜像，SNCF的miniImageNet Drive链接被说明为预训练权重/噪声检测产物，不误当图片集。
- **已验证与未找到的区别：** FaMUS（CVPR2021）仍是本次链路中明确公开CNWL成品包的作者来源，但为32像素，且用户实包经0053确认缺is_clean/id；不能用它证明84原始包已找到。近期项目“发表实验/公开代码”与“公开完整数据”分别判断。对于CARE、CLIPCleaner，只报告在所检查公开位置未见链接，不断言作者无数据、不能分享或全网绝对不存在。可向其作者索取保留ID的all_images、validation_all、官方split/class_names/annotations以及图像处理说明，从而避免强制重新取得全量ImageNet和失效web URI；这仍是待取得的路线，未发送任何消息。
- **涉及文件及验证：** 仅追加本开发文档；原代码、32像素ZIP及实验结果保持不变，git diff --check通过。尚未找到经验证可下载的84像素完整自然噪声包，也未核实候选私有分享/数据尺寸和映射；研究结论为来源调查，不产生算法实验结果或收益保证。

### 2026-10-31 / DPCO-0057：区分GCS身份认证与授权并提供登录浏览器检查入口

- **用户请求与范围：** 用户询问Anonymous caller拒绝能否通过变为正常caller解决。只核对Google Cloud官方认证、请求端点、公开访问与403排障说明，追加文档；不修改代码、切换用户账号、读取凭据、修改IAM或执行下载/训练。
- **技术结论及边界：** 可以使用Google账号/服务账号身份请求，但身份认证不等于拥有该cnlw桶内对象的storage.objects.get权限。若发布方允许已认证用户或已授权该账号，认证可能解决；否则仍需发布方授予读取权限、恢复公开访问或提供签名链接。匿名403只能证实该匿名请求失败，不能证实认证后必失败，亦不能证实对象确实存在/已删除。给用户自己项目授予角色不赋予作者项目资源权限，服务器在GoogleCloud上也不意味着urllib自动携带其服务账号令牌。
- **低成本检查办法：** 官方 https://docs.cloud.google.com/storage/docs/request-endpoints 明确cookie登录下载入口为https://storage.cloud.google.com/BUCKET_NAME/OBJECT_NAME，因此可由用户在Mac浏览器打开https://storage.cloud.google.com/cnlw/dataset_no_images.zip并选择其Google账号，实际检验该账号是否可读。本代理未代为登录或测试该身份，不声称成功。若仍报账号无get权限，客户端改变User-Agent/重装下载器不能自行获得授权；若成功，仍只补回标注/划分包，完整图片准备另需完成。
- **涉及文件、验证与未完成项：** 仅追加DPCO_dev.md，git diff --check通过。官方依据另含https://docs.cloud.google.com/storage/docs/authentication及https://docs.cloud.google.com/storage/docs/troubleshooting（403排障检查实际caller与目标资源授权）。用户账号的真实读取权限、文件当前存在状态及认证下载结果均未知；没有执行长任务或改变已有实验。

### 2026-10-31 / DPCO-0058：核对近年顶会加噪协议并建议ImageNet受控机制验证

- **用户请求、范围与授权：** 用户询问其他适合数据集、ImageNet100/1K手动加噪是否可行以及近两年顶会采用的方式。本轮读取协议、查2025/2026会议原文及作者噪声生成代码，2024自然数据工作仅作补充候选。只提出研究设计并记录，不将讨论视为新增ImageNet加噪功能授权；不改源代码/配置/依赖、不下载大数据或启动训练。
- **近期直接先例：** NeurIPS2025 Enhancing Sample Selection Against Label Noise by Cutting Mislabeled Easy Examples（Early Cutting），官方论文https://proceedings.neurips.cc/paper_files/paper/2025/file/3e826f682178d9830a3b704141b4989e-Paper-Conference.pdf，第4.2节/表5在完整ImageNet1K使用40%合成对称标签噪声、ResNet50；附录D.2比较Symmetric/Instance-dependent并描述Asymmetric/Pairflip，主要CIFAR比较20/40%，另用CIFAR-N与WebVision自然噪声。作者tmllab/2025_NeurIPS_MEE/noise_build.py（blob49c7d4d3e8ae8541e98229211c393a148da6bd1a）实际包含dataset_split_imagenet及对称转移矩阵，矩阵对角1-r、非对角r/(K-1)，返回actual_noise。其训练主要采用SGD，不将其lr/优化器直接移植为DPCO+Adam最优配置，也不声称已复现该论文成绩。
- **其他论文核实：** ICCV2025 Joint Asymmetric Loss for Learning with Noisy Labels，https://arxiv.org/html/2507.17692v1 的B.1与表3/4/5：CIFAR对称20/40/60/80%、非对称10/20/30/40%、IDN20/40/60%，非对称CIFAR10采用TRUCK→AUTOMOBILE、BIRD→AIRPLANE、DEER→HORSE、CAT↔DOG，CIFAR100在superclass内循环，IDN沿PDN，另有CIFAR-N。ICLR2026 Resurfacing the Instance-only Dependent Label Noise Model through Loss Correction，https://proceedings.iclr.cc/paper_files/paper/2026/file/a92200bd6703e81346b0f3c043aabba4-Paper-Conference.pdf，使用Xia2020协议的IDN；实验为二分类子任务，28/44%且另有Clothing1M，不能当作ImageNet多分类直接基线。上述为核对的代表性先例，未做全领域频次统计，不宣称一种协议是唯一标准。
- **噪声定义与可追踪性：** y_i为基准数据原标签、tilde_y_i为固定污染训练标签、m_i=1[tilde_y_i!=y_i]。对称错标从其余K-1类选取，避免把包含原类的重采样概率等同实际错误率；非对称/Pairflip限制错误目标类别，随意按类别编号循环不自动等于语义相似；IDN使P(tilde_y|x,y)随样本特征变化，属于合成噪声而非自然错标，不局限于均匀随机。若采用已发表IDN生成器应固定源版本、生成方式与seed，不能按DPCO自身align动态制造噪声。固定比例选样与Bernoulli选样也需区分，并报告实际错标率。原始ImageNet标签仍可能有残余错误，所谓原标签指标是相对基准标签，不保证每张语义真值正确。
- **面向DPCO的建议而非论文既定要求：** 优先复用已有ImageNet100做0/20/40%对称噪声，再在20%增加已发表IDN协议；固定100类列表、样本/划分和噪声manifest，在Adam/Filter/Flip之间配对复用，训练seed和noise seed分开记录。模型先保持现有ResNet50及一致初始化/增强，ref beta=.9只作为此前候选而非新数据最优值。待机制现象稳定再扩ImageNet1K 20/40%，不因类别/规模大就推定更适合机制验证。评估clean训练子集按原标签CE/acc、污染子集按原标签与污染标签acc、全部训练集按原标签acc、干净验证集CE/acc，并审计负align在污染/clean上的比例及检测precision/recall；污染mask/原标签仅用于离线评价，不输入reference、样本权重或优化器。三seed/超参选择需保持干净验证集与最终测试用途区分，此轮未生成新启动命令。
- **自然数据候选及限制：** 保留CIFAR100N，CIFAR10N可补人类错标控制验证；WebVision/Clothing1M可测自然噪声泛化，但不能假设全部噪声训练图都有配对真值。补查NeurIPS2024 Datasets&Benchmarks Noisy Ostracods，作者H-Jamieu/Noisy_ostracods README明确final为原噪声标签、clean为专家清洗且仍更新，提供SharePoint图像/标签链接；当前公开树仅明确见clean_val.csv与clean_test.csv，不能据此承诺全训练集clean真值或直接替代CNWL审计，未下载验证链接。CNWL32仍是自然噪声泛化补充，保留0053已确认的缺失clean mask限制。
- **验证与未完成项：** 仅追加本开发文档，git diff --check通过。CVF部分PDF入口本轮403，JAL的具体协议改由作者arXiv完整文本核对；其ICCV归属来自CVF检索与会议条目。未完整核对当前ImageNet读取器改动量、复现IDN生成器或确认全部候选下载可用；研究方案不保证DPCO优于Adam，亦不将合成噪声结果外推为自然噪声结论。

### 2026-10-31 / DPCO-0059：按用户偏好改为优先研究固定类别映射的非对称错标

- **用户依据、目的与边界：** 用户选中非对称噪声及ICCV2025 JAL示例，希望先研究“人为指定成某类、持续出现”的错标。本轮将0058优先对称的建议调整为优先固定类别映射的非对称控制验证，仅讨论定义并记录；按AGENTS明确修改要求的约定，未把偏好表述延伸为源代码/配置修改授权，未启动正式实验。
- **定义与持续性：** 预先给定源类别到错误目标的映射f(a)，要求目标属于固定ImageNet100类别且f(a)!=a；在每个选定源类按比例r_a选样，改标后整个训练固定，三方法使用同一标签manifest。固定错误去向不意味着将源类100%样本全改错，也不意味着每个epoch重新采样；未映射类别默认不改。单向A→B、双向A↔B及多源→同一目标是不同设置，需分别声明，不能将任意编号循环叫作语义混淆。
- **噪声比例语义：** 定义T[a,a]=1-r_a、T[a,f(a)]=r_a（对于映射源类），其余未映射行T[a,a]=1。r_a为该源类内部错标比例，全局期望错误率为sum_a (N_a/N)*r_a；实际率以保存后的tilde_y!=y计数。例子为均衡100类中10个源类各改20%，全局约2%，不能报告全局20%。建议先用类内20/40%保留源类正确监督；100%整类错标可能使语义恢复缺乏监督辨识，属于另一困难设置，不作为自然噪声的同义词。
- **论文先例与ImageNet边界：** 再核对https://arxiv.org/html/2507.17692v1#A2.SS1，JAL示例为CIFAR10特定单/双向类别混淆，CIFAR100在superclass内循环。把其思路应用于当前ImageNet100是自定义、需公开的映射协议，不是论文已定义的ImageNet官方映射。当前manifest固定100个synset与原ILSVRC索引，尚未核对全部类别自然名称并选定语义对应；正文只用A/B说明，不编造实际选中类别。现有config的label_noise_percent限MNIST，ImageNet不支持该生成器，不能仅改启动参数宣称已支持。
- **DPCO机制与评价：** 保持基准原标签、固定污染标签和mask只用于离线审计，模型训练仅接触污染标签；在源类/目标类分别评价原标签acc与混淆矩阵，辅以clean训练子集loss、污染原标签acc、干净验证acc及负align检测precision/recall。固定方向错误可产生群体一致梯度并污染EMA reference，因此不保证比随机噪声更易识别或DPCO必优于Adam；用于检验系统偏差下的稳健性。未确定单向/双向/多源映射的最终实验、覆盖类数及实际率。
- **涉及文件、验证与未完成项：** 只追加DPCO_dev.md，读取现有ImageNet接口/manifest确认上述边界，git diff --check通过。未新增噪声manifest、实现映射、改模型或绘图、下载数据、运行训练、提交或推送。

### 2026-10-31 / DPCO-0060：将非对称噪声目标明确为全局10%/20%

- **用户依据与更正：** 用户认为0059举例的全局2%偏低，明确希望全局至少10%–20%，询问是否难实现。将后续建议目标调整为全局10%和20%；此前2%仅为比例换算例子，不作为正式实验推荐。仅讨论并追加记录，不修改代码或生成训练数据。
- **定义、推导与示例：** 设可被改标的源类样本占全部训练样本比例为c、这些类共享类内错误率r，则全局期望率q=c*r，故r=q/c，须q<=c。只有均衡类数时c等于源类数/K。均衡100类中50源类各改20%/40%分别对应全局10%/20%；全部100源类各改10%/20%也可达到相同目标。10源类即使全部改错全局也最多10%，无法得到20%。实际不均衡ImageNet应按样本数核算，按固定名额取整分配并保存实际率，不能仅凭类数估算后直接标称精确比例。
- **实现与实验难点区分：** 依据固定映射、全局名额和noise seed生成一次manifest在算法上直接，真正需审查的是当前100类能否形成足够覆盖的合理错误目标映射，以及类频变化的影响。50源类单向映射是可行的数量示例，未核实能找到50对互不重叠且语义相近的真实类别；不为凑覆盖强称任意映射自然。可按语义组定义多个映射，检查覆盖样本是否足够，再推导类内率。建议保留多数源类正确监督，优先约50%样本覆盖、r约20%/40%实现q10%/20%；不承诺此覆盖在当前manifest已成立或DPCO必受益。
- **文件、验证与未完成项：** 仅追加DPCO_dev.md，比例由上述代数推导验证，git diff --check通过。原标签/mask仍仅供离线评价，各方法复用同一固定污染标签，0%对照保留。映射表、全局名额接口和生成器尚未实施；未改配置、启动实验、下载、提交或推送。

### 2026-10-31 / DPCO-0061：核对实际ImageNet100类别及语义非对称噪声覆盖可行性

- **用户请求与授权边界：** 用户认为ImageNet100可混淆类不足，要求先分析，若不可行再考虑其他方式，并希望可复用到1K、合理模拟生活中常见错标。本轮仅阅读、映射名称和研究定义；不修改代码/配置、不生成污染标签、不下载图像或模型、不启动实验。保留既有未提交文档。
- **实际类别核对：** 读取configs/manifests/imagenet100_classes.txt，以raghakot/keras-vis/resources/imagenet_class_index.json逐一核对全部100个原ILSVRC索引与synset一致，保留原顺序。按名称筛选的示例候选组为19种家犬（原index151–268内本项目选中类别）、3种蛇green_mamba/garter_snake/hognose_snake、2蟹rock_crab/fiddler_crab、2灵长类langur/gibbon、2真菌gyromitra/stinkhorn，共28类。家犬组内也不应任意互改；Walker_hound/English_foxhound、Doberman/Rottweiler等只是潜在混淆关系，未测人类/模型混淆率。类别语义相关不等于视觉易混淆，不能用这28个候选推断全部均有可靠错误目标，也不声称28是全100类的覆盖上限。
- **数量可行性与修订边界：** 若这28类全部可映射且样本均衡，仅作示例c=.28，则q10%需r约35.7%，q20%需r约71.4%。若限制源类内r<=40%以保留多数正确监督，q10/20%分别要求至少25/50%的样本覆盖。此前0060的50类可行只是数量例子，本轮未证明实际manifest有50类可靠近邻；不建议为凑全局20%把无合理邻居的类别强行配对或集中改掉少数类大多数标签。data/、DPCO/data/、DPCO/results/imagenet三个检查位置均不存在，未取得本地ImageNet图像与真实类样本计数，因此10%有希望但未获充分覆盖证据，20%目前不应承诺语义自然性。
- **优先方案与1K复用：** 先在实际100类中构造可审核的语义近邻候选图，用代表图片或独立干净开发数据的混淆统计核查，只保留合理目标、允许无近邻类不改，固定方向及污染样本；报告覆盖样本比c再推导能否达到全局10/20%。1K复用的是候选筛选/审核、全局名额、固定noise seed及记录规则，不是强制使用同一数值映射矩阵。100类之外的目标不能直接作为100分类器的标签；1K候选更丰富通常提供更多细粒度近邻，但未量化可达覆盖率。若静态语义映射覆盖不足，再讨论语义约束下按图片难度生成IDN：困难/模糊图更易错，错误集中于合理近邻，由独立固定生成器确定，仍为合成且不能宣称等同真实人工噪声，不使用DPCO align反向塑造噪声。
- **外部证据与附带线索：** NeurIPS2024 Datasets&Benchmarks论文dopanim: A Dataset of Doppelganger Animals with Noisy Annotations from Multiple Humans（https://proceedings.neurips.cc/paper_files/paper/2024/file/5b44b99d012922011f0be1031a98c4f9-Paper-Datasets_and_Benchmarks_Track.pdf）实际采集15类相似动物、20人、约52000个标注，提供基准真值，人类混淆集中于相似动物组，支持从语义相近组出发的设计动机；不证明本项目28候选类映射或设定10/20%真实。其数据doi10.5281/zenodo.11479589与作者ies-research/multi-annotator-machine-learning的dopanim分支作为额外自然噪声候选，尚未核实下载可用性或训练真值覆盖，不擅自换数据集。CVPR2024 workshop主动清洗论文检索片段同样提及WordNet层级模拟，但正文访问403，不据该片段认定顶会主会协议或复现细节。
- **产物、验证与未完成项：** 全100类名称、synset、局部/原索引、候选组和检查限制保存results/files/imagenet100_asymmetric_feasibility_20261031/class_audit.json；仅新增诊断JSON和追加本开发文档，git diff --check通过。候选计数28与synset逐项校验由脚本完成；无图像级混淆、语义映射定稿、样本覆盖精确统计、生成器或实验结论，不保证DPCO收益。

### 2026-10-31 / DPCO-0062：降低人工映射优先级并讨论自动模型诱导噪声

- **用户依据与目的：** 用户认为手工寻找合理相似类别费时且效果可能一般。本轮认可人工审核成本，但不把“DPCO效果一般”作为已有实验事实；噪声模拟是否合理与DPCO是否获益须分开验证。追加研究取舍，不修改代码、数据标签、模型或依赖。
- **建议调整与具体含义：** 降低强行构造50类人工映射的优先级。可考虑固定、独立于Adam/DPCO训练的生成模型为每张图片提供候选错误类和混淆程度，以模糊/难分图片更容易被选中的规则生成10/20%目标全局噪声；目标限当前100或1000类，标签一次生成后固定，保留原标签和mask供离线评价。此为待验证的模型诱导实例依赖合成协议，模拟图片难度与错误去向的关联，不宣称模型错误等同人工错误、不声称为JAL已经给出的ImageNet标准。没有足够合理候选时不能为凑20%保证自然性。
- **标准协议与自定义协议区分：** 0058查到的作者公开IDN生成器可作为可复现对照，但实例依赖本身不保证错误目标语义相近；若增加独立预训练模型/特征及混淆筛选即需公开新的生成细节。生成模型、标签空间、数据使用/预训练来源、置信度/难度定义、noise seed、名额和实际率必须固定记录；不得使用DPCO当前align或依据DPCO成绩反复重造噪声。100与1K可复用流程，生成成本和候选覆盖尚未测量。
- **涉及文件、验证与未完成项：** 仅追加DPCO_dev.md，git diff --check通过；没有生成模型选型、权重下载、前向推理、加噪实现或训练结果。后续需先决定采用公开标准IDN还是单独定义模型诱导协议并检查可行性；不作收益保证，不将讨论视为代码修改授权。

### 2026-10-31 / DPCO-0063：说明错误目标、样本难度与精确全局名额的示意实现

- **用户请求及范围：** 用户询问模型诱导噪声如何编码、如何识别难预测图片，并提出“最大概率且非正确label”的理解。本轮讲解与内存示例，不修改项目代码/配置/依赖；仅追加记录，没有实际生成训练标签、运行生成模型或启动训练。
- **区分两个量：** 对固定独立生成器概率p_i(k)，错误目标j_i=argmax_{k!=y_i}p_i(k)；该目标对每个样本都存在，不能单凭它断言样本难。示意难度d_i=max_{k!=y_i}p_i(k)-p_i(y_i)，越大表示相对该生成器越难/更偏向错误类别。p真=.95、p错最大=.03得到d=-.92；.45/.40得到-.05；.15/.70得到+.55。只挑生成器原本top1预测错误的图片会将可加噪比例受限于其错误率，不能无条件承诺全局20%。难度是生成模型的相对代理，不是已测人类困难程度或已校准的人工错误概率。
- **自定义示意协议：** 对全部样本保存j_i、p真、p错最大，设固定tau=.2示例，以exp(d_i/tau)归一化为权重，用固定seed不放回抽取round(rho*N)个样本，改为j_i。tau控制抽样偏向难度，非Adam/DPCO beta；权重不是精确的最终边际入选概率。无候选合理性过滤的示意版可保证round名额且全部确实改标，但不能保证所有改标符合人类视觉混淆。正式协议若增加合理性候选门槛，必须检查候选数是否足够，不足时不能以随机无关目标静默补满。round引起实际率与目标至多约1/N的偏差应报告。
- **可复用及数据隔离：** ImageNet100先限制生成器输出为manifest对应100类，再匹配局部ID；1K对应1000类。分批推理只保留上述逐样本摘要即可，不要求在内存常驻N×1000概率矩阵。原标签与mask只用于离线生成和审计，训练Adam/Filter/Flip使用同一份固定污染标签；不从DPCO align/实验成绩反馈调整生成规则。冻结生成器的架构、权重/预训练来源、推理预处理、温度和seed均待明确，不称为已发表ImageNet官方噪声标准。
- **验证、涉及文件与限制：** 使用现有本地Python/NumPy在内存计算上述3例，再平铺为300样本验证固定seed、不放回抽60条、实际改标60条=20%，无代码文件或数据标签落盘。NumPy权重与不放回接口依据https://numpy.org/doc/stable/reference/random/generated/numpy.random.Generator.choice.html。只修改DPCO_dev.md，git diff --check通过；尚未确定正式噪声协议、模型选型或部署实现，示例不证明噪声自然性或DPCO收益。

### 2026-10-31 / DPCO-0064：核对2025/2026顶会模型标注先例、IDN差异及CLIP候选

- **用户请求与授权范围：** 用户希望寻找可作为固定标杆的模型，同时判断哪些图易混淆及易错成何类，明确要求先搜索梳理、不改代码。本轮查询官方会议页、论文正文/附录、作者公开预印本及少量作者代码；不修改程序、配置、脚本、依赖，不下载模型/图像，不运行推理或训练。仅追加研究记录，保留已有修改。
- **关键更正：** IDN只要求标签噪声分布随实例变化，不自动意味着由强分类器估计难度，也不保证实例翻转概率随视觉困难上升。0062/0063的d=max错误概率-真类概率以及exp(d/tau)加权定额抽样是本项目讨论中的自定义原型，并非已确认的近两年统一协议。查到的近期相关文献存在模型伪标注与随机特征式IDN两条路线，不将二者混称为“模型模拟人工标注”。
- **AAAI2025最直接分类先例：** Pre-Trained Vision-Language Models as Noisy Partial Annotators，官方DOI https://doi.org/10.1609/aaai.v39i20.35417 ，官方摘要/已索引PDF明确用预训练CLIP为图像自动标注，多prompt各给预测，组成可能不含真类的候选标签集合，研究noisy partial label learning。对应同作者公开预印本标题Pre-Trained Vision-Language Models as Partial Annotators，https://arxiv.org/html/2406.18550v1，4.1明确生成模型CLIP ViT-B/32；PreAct ResNet18是下游学习骨干，不是噪声生成模型。预印本还明确描述另一单标签路线：对多prompt预测概率取平均再argmax；论文重点采用候选集合。正式AAAI PDF本轮访问被BotStopper拒绝，ViT-B/32细节由同作者预印本核实，不能伪称逐项核对最终版本。多prompt个数本轮未可靠核实，故不引用二手来源的27个数值。该工作噪声来自模型自然预测错误，没有查到它规定ImageNet100/1K精确10/20%或使用我们的margin采样。
- **ICML2026模型诱导噪声先例及领域边界：** MIND: Decoupling Model-Induced Label Noise via Latent Manifold Disentanglement，正式会议记录https://proceedings.mlr.press/v306/ren26i.html，正文https://arxiv.org/html/2605.16081v1。区分CIFAR100合成IDN验证与S3DIS/ScanNet三维结构噪声，后者列KPConv/MPRM/PCAM来源，并在OpenSeg实验直接将VLM预测当有噪伪标签。它支持固定模型的系统性实例依赖错误这一动机，但OpenSeg为分割语境，不能直接当作ImageNet1K分类噪声标准，亦不能把引言提及CLIP/SAM说成实验统一采用两者标注。未查到可直接复用的ImageNet分类固定错标率协议。
- **近年标准IDN对照：** NeurIPS2025 Early Cutting的官方论文https://proceedings.neurips.cc/paper_files/paper/2025/file/3e826f682178d9830a3b704141b4989e-Paper-Conference.pdf及tmllab/2025_NeurIPS_MEE/noise_build.py 99–132行（blob49c7d4d3e8ae8541e98229211c393a148da6bd1a）实际采截断正态flip_rate，采随机高斯W，对输入x计算x@W[y]，屏蔽原标签后softmax决定错误目标，保留原标签概率为1-flip_rate。该代码中flip_rate并非由语义模型难度预测，实例依赖来自错误目标分布等，不保证错误目标人类看来相近。其ImageNet1K主实验为40%对称噪声，不能说在1K使用CLIP造IDN。ICCV2025 JAL https://arxiv.org/html/2507.17692v1#A2.SS1明确沿PDN生成IDN、CIFAR非对称用预定类别映射，未给出本用户设想的ImageNet标杆模型。
- **与用户设想最接近的明确算法来源（超出近两年，单列）：** ICML2022 From Noisy Prediction to True Label: Noisy Prediction Calibration via Generative Model，https://proceedings.mlr.press/v162/bae22a/bae22a.pdf，附录D.1.1 Algorithm2名为Similarity Reflected Instance Dependent Noise (SRIDN)：先训练分类器，按f_i[y_i]从低置信度开始排序，依次将约n*tau个样本改为argmax_{j!=y_i}f_i[j]。这为“哪些难/错成啥/固定全局名额”提供直接算法依据，但不是2025/2026新协议，不应把其一般训练骨干说明自动认定为噪声生成器架构。采用CLIP替换该生成分类器属于明确需披露的组合适配，不是原论文ImageNet实验复现。没有证据证明近两年存在统一、唯一的ImageNet100/1K标杆模型。
- **针对DPCO的建议与未定项：** 首个值得评估的固定生成器候选为CLIP ViT-B/32（按上述近期分类标注先例），对固定100/1000类别名称和固定prompt提供图像-文本分数，类别空间切换不要求重新训练分类头。OpenAI官方README https://github.com/openai/CLIP （blobdb56b56e29258cc871fe0e6297bde00436d9180b）证实该型号和对候选类别做零样本softmax的接口。该推荐是有先例的起点，不是已证实最贴近人类或最优模型。需区分直接使用模型top1伪标签（实际率内生，可能不足20%）与受控地选择最难10/20%并取最大非真类（主动合成）；后者可按SRIDN思路公开适配，原margin加权版作为另外自定义协议。先检查噪声转移矩阵、类内错误率、错误样例与prompt稳定性，再确定正式协议，不能按DPCO收益选生成器。softmax数值不是自动校准的人类错误概率，模型易混淆不等于人类易混淆；模型权重/预训练来源、prompt/类别名/预处理、使用训练数据生成噪声的规则和noise seed均需记录，原标签/mask只用于离线构造/评价。
- **验证与文件范围：** 仅追加本开发文档，git diff --check通过。MIND官方PDF链接为application/octet-stream导致浏览工具未解析，实施细节使用作者arXiv版，不声称已核实代码重现；AAAI与部分CVF入口受访问限制，未将二手搜索页作为技术结论唯一依据。另检索到的AEON当前作者说明为投稿/预印本，partial-label、图数据及无关像素噪声论文不冒充ImageNet单标签主会协议。未生成新数据或运行模型，没有算法收益结论。

### 2026-10-31 / DPCO-0065：说明CLIP型号、AAAI生成模型定位及选型依据

- **用户请求与范围：** 用户先询问是否需两个模型分别判断难度/产生错误标签，后询问CLIP型号和AAAI使用型号是否已足够强。本轮核对OpenAI模型清单、原始CLIP论文Table11、OpenCLIP公开评测和同作者预印本；仅解释并记录，不修改代码、配置或依赖，不下载权重、不做本地性能或显存测试。
- **角色澄清：** 一个冻结生成器的同一预测向量即可同时给出原标签置信度/竞争间隔和最大非原类，不需两个独立噪声标注器。CLIP可加载现成预训练权重，随后DPCO/Adam所训练的ResNet50为另一用途的模型；AAAI的双网络属于下游Co-Reg净化算法，不是分别完成两项标注职责，也不要求本项目移植该算法。
- **官方原版型号：** OpenAI/CLIP clip/clip.py _MODELS（blob398a6282cc243e449430d91c2562491fc799929d）列RN50、RN101、RN50x4、RN50x16、RN50x64、ViT-B/32、ViT-B/16、ViT-L/14、ViT-L/14@336px。B/L表示Base/Large，斜线后32/16/14为图像patch边长，不是总输入尺寸；336px版本为更高分辨率。以原论文https://arxiv.org/pdf/2103.00020 Table11（PDF43页）同表ImageNet零样本结果示意，B32为63.2%、B16为68.6%、L14为75.3%、L14-336为76.2%；不把公开验证评测数字当本项目ImageNet100训练表现或概率校准。OpenCLIP README对原CLIP L14另外报告75.5%，存在评测实现/协议差异，最终答复不混用两来源得出精确横向差值。
- **开放实现与权重区别：** https://github.com/mlfoundations/open_clip 维护更多模型/不同预训练来源，包括ViT-H-14、ViT-bigG-14、DataComp/LAION/DFN等，README列原CLIP L14约75.5%、DataComp1B L14为79.2%等标准ImageNet零样本结果，表明同架构不同权重可有明显差异。其接口也支持SigLIP/SigLIP2等相关但训练目标不同的模型，不能都视为AAAI所用同一原版CLIP。选择时须完整记录架构、权重来源、分辨率、预处理和prompt，而不是只记CLIP或ViT-B32。
- **AAAI与实验判断边界：** https://doi.org/10.1609/aaai.v39i20.35417 对应论文，型号仍以同作者公开预印本https://arxiv.org/html/2406.18550v1 4.1明确的CLIP ViT-B/32为依据。它是成熟且有相关标注先例的基础型号，并非当前最强。原论文patch更小/模型更大在整体分类评测更强，不自动证明其错误更符合人类、难度排序更好或给DPCO带来更大收益。AAAI实验适用其所列数据集，不构成在本项目ImageNet100上的性能保证。
- **建议与验证：** 先用固定OpenAI原版ViT-B/32权重建立可复现生成器，必要时以ViT-L/14在同一小样本核查困难排序、错误去向与稳定性；若B32明显产生不合理目标再决定更换，不能根据DPCO收益择优造噪声。该为选型建议，尚无实际错误率、推理耗时或资源实测，不承诺B32足够或大模型必优。仅追加DPCO_dev.md，git diff --check通过，未启动推理/训练或提交推送。

### 2026-10-31 / DPCO-0066：区分CLIP标注器、ResNet预测模型与DPCO训练规则的比较职责

- **用户请求与授权范围：** 用户询问CLIP是否也属于图像分类模型，以及采用CLIP造噪声后是否必须将ResNet上的DPCO与CLIP直接比较。本轮只解释实验设计并追加文档，不修改代码、配置或依赖，不下载权重或运行模型。
- **概念澄清：** CLIP为图文对齐模型，可用类别文本与图像相似度进行零样本分类；ResNet为本项目下游预测骨干，DPCO为调整样本梯度贡献的训练规则，三者并非同层级替代项。冻结CLIP用于离线生成固定污染标签，不要求把CLIP引入训练期reference或直接与ResNet比赛。主要机制对照保持同数据、同ResNet、同初始化/训练预算与Adam设置，仅改变普通Adam、Filter、Flip的梯度贡献规则；原标签与mask只用于离线生成及诊断，训练输入使用污染标签。
- **比较范围与证据边界：** 为回答DPCO是否改善同骨干有噪训练，CLIP零样本成绩不是替代主要Adam对照的必要条件；报告同一干净评估集上的冻结CLIP成绩可作为生成器能力参考。若进一步主张学生超越标注器或优于直接使用CLIP，则必须实际测量对应CLIP基线，并披露外部预训练、输入分辨率、标签空间、prompt和额外资源差异，不能将该比较归因于DPCO单一因素。若目标扩大至噪声学习方法竞争力，另需合适的已有噪声学习方法对照，不等于单纯更换骨干。
- **避免循环论证：** 以真实标签置信度/间隔选样并强制改为最大非原类的受控协议，不等于完全照抄CLIP的自然top1错误，CLIP正确率也不是学生不可超越的上界。噪声来自一个模型会引入该生成器特有的错误结构，不能因此声称符合人类自然噪声；后续可用另一生成器或另一类噪声协议检验泛化，不能根据DPCO收益反复改造同一数据。
- **涉及文件、验证与未完成项：** 仅追加DPCO_dev.md，内容依据0063至0065既有已核实模型接口及研究设计推论，未产生实验结果。本轮不新增文献性能主张；尚未测量任何CLIP或新噪声训练结果，比较范围需依论文主张进一步确定。

### 2026-10-31 / DPCO-0067：按用户统一覆盖ImageNet100与1K的目标建议固定CLIP ViT-L/14

- **用户依据及范围：** 用户希望选型一步到位，并考虑未来ImageNet1K，询问是否应使用ViT-L/14。本轮调整0065中以低成本试探为优先的选型建议，仅讨论和记录；不视为代码修改、权重下载、数据生成或训练授权。
- **建议及依据：** 在用户优先统一长期协议、接受更高离线推理成本的条件下，建议固定OpenAI原版CLIP ViT-L/14、官方224像素预处理、冻结权重作为生成器，而非先B32后更换。原CLIP论文Table11 L14为75.3%、B32为63.2%，支持整体分类能力更强，不证明其噪声更像人工或DPCO收益更大。336像素版本可用但本轮不建议默认增加该成本，未测本项目吞吐、显存或TPU兼容性。
- **类别规模与协议边界：** B32同样可直接比较1000条类别文本，1K不构成必须L14的技术要求。100与1K可复用同一权重、文本模板和生成流程，各自候选类别空间需限于本数据集且固定类别名称与索引；扩充候选类别会改变最大错误类别、softmax归一化与难度分布，不能直接将100类的概率阈值或已生成噪声映射当作1K协议。目标10/20%可各自按固定规则定额生成，仍须审核合理候选覆盖与报告实际率。
- **比较及资源设计：** CLIP仅离线前向，保存可复用预测摘要与固定污染标签，三种ResNet50训练共同使用同一份标签；不同训练seed不必重新运行CLIP，noise seed需另行记录。完整记录架构、checkpoint来源/哈希、预处理、类别文本、prompt聚合、难度与选样规则，避免仅写ViT-L14导致权重混用。需要时同一干净评估集报告冻结CLIP的零样本成绩作附加参考，不替代Adam与DPCO的同骨干对照。
- **文件、验证及未完成项：** 仅追加DPCO_dev.md；复核https://github.com/openai/CLIP和https://arxiv.org/pdf/2103.00020的既有官方接口与研究依据，git diff --check通过。暂无本项目模型推理、自然性审核、资源实测或DPCO收益证据，具体生成算法仍待用户授权实现。

### 2026-10-31 / DPCO-0068：实现冻结OpenAI CLIP ViT-L/14的ImageNet固定比例噪声、人工抽查及训练接入

- **用户明确授权：** 本轮用户要求“完成OpenAI已经训练好的CLIP ViT-L/14权重的代码和实现对现有imagenet100的固定比例加噪，固定比例可由参数控制”，同时要求可复现、保留原标签/噪声标签并支持人工抽样与原训练集acc等指标。授权限实现、必要本地验证与文档，不扩展为正式权重/图片下载、全量推理、服务器操作或正式训练；保留此前未提交的开发文档变更，无提交/推送。
- **生成模块与官方来源：** 新增src/data/imagenet_clip_noise.py和scripts/prepare_imagenet_clip_noise.py，提供score/generate/verify/audit/all阶段。OpenAI/CLIP固定commit d05afc436d78f1c48dc0dbf8e5980a9d471f35f6（通过作者GitHub API核实），使用官方ViT-L-14.pt、SHA256 b8cca3fd41ae0c99ba7e8951adf17d267cdb84cd88be6f7c2e0eca1737a03836和官方224预处理。核对https://raw.githubusercontent.com/openai/CLIP/main/clip/clip.py中的下载校验/加载接口，以及README的零样本用法；CLIP不训练、不微调，eval、冻结参数、inference_mode、FP32和确定性选项。CPU/CUDA可选，未声称支持TPU推理。1K候选文本按64条分批编码以限制显存；图片batch可控。
- **固定比例协议及与前期讨论的关系：** 沿用0063的候选j=argmax非原类概率、难度d=p(j)-p(y)、权重exp(d/tau)，默认tau=.2、noise_seed=0。将示意numpy.choice实现为显式PCG64随机数的Gumbel top-k排序，无放回抽floor(N*r/100+.5)条并强制改为j；是同类加权不放回采样，完整排序使同seed/温度的10%污染集合包含在20%中。比例为全局，记录各类改标计数和实际整数比例；126689条的20%为25338条，约20.000158%。tau为未调优原型默认值；其权重不是最终边际入选概率。这是项目自定义受控模型诱导合成协议，不是AAAI/官方ImageNet原样协议，更不等于自然人工噪声。没有证据承诺合理候选足够、DPCO更优或L14最接近人的错误。
- **不可变产物、复现和断点：** 读取已完成images.sqlite，不改原库，不在训练时下载图片或运行CLIP。每batch预测事务提交SQLite，可中断续跑，拒绝来源/模型/prompt/软件版本/device/batch等身份不一致的旧缓存。发布labels.npz、labels.csv、transition.csv、summary.json、noise_manifest.json，保留sample_id、source_index、图片SHA256、原/污染/候选标签、mask、概率和难度，以及权重/实现哈希、类别文本、源数据身份和生成参数。文件带校验、manifest最后发布，已有产物拒绝覆盖；同一CLI请求可校验复用。verify重新从分数/seed/规则重建标签并比较。跨硬件浮点预测不保证逐位相同，以保存后的标签及manifest哈希为复现依据。官方模型下载器本身不保证断点续传；分batch评分续跑不应误称权重下载续传。发布阶段若异常留下半成品需换新输出目录、复用已完成评分缓存，失败关闭。
- **人工抽查：** 新增离线HTML、缩略图、review.csv、audit.json；默认独立audit_seed=42，从污染与未污染组各均匀抽最多100张，并记录具体ID和被审manifest哈希。展示原/训练/候选类别、概率和难度，预留人工合理性/备注列，不读取人工意见自动改训练标签。图片导出时核对字节SHA；展示全图缩略图并明确CLIP中心裁剪视野不同。保护已有人工抽查目录；需要新抽样可指定新audit-dir。不能将分组等额抽样未经加权当总体估计，不按DPCO收益选择噪声。
- **训练和指标接入：** src/config.py、src/training/launch.py新增noise_manifest及父子CLI透传，--noise-manifest自动设ImageNet noisy/clip_idn/非人工模式；训练端不重生成标签，生成seed/比例从manifest读取，原--noise-percent仍仅断言实际率。旧无manifest配置序列化不新增字段，保留旧checkpoint恢复兼容。src/data/classification.py使用全量已准备源并核对artifact来源/原标签/source indices，smoke仅裁切读视图。NoisyImageNetImages的训练batch仍仅图片/污染标签/valid_mask，原标签与mask只用于评价，不进入梯度/EMA/Adam。scripts/train_classification.py接入既有clean、corrupted_noisy、corrupted_original分组；src/training/evaluation.py可选新增all_original，将两个原标签组按样本数加权，不重复推理。完整原训练集CE/acc直接记录于group_evaluation.csv；干净validation、step/timing、Adam/DPCO指标沿用原流，best checkpoint仍按独立干净validation选择。旧定理及实时observer对此协议暂拒绝启用，避免误套假设。现有evaluation绘图接口可直接读取。src/training/results.py为新run增加clip_idn标识；scripts/launch_tpu.py在计划中区分artifact内固定参数，避免把训练配置的占位0误报为实际生成参数。
- **依赖及文档：** pyproject.toml新增可选clip依赖（固定官方Git commit、torch/torchvision、filelock等）；src/data/images.py将JAX batch导入推迟到实际迭代时，因此离线准备/验证无需导入JAX，不改变训练变换/排序行为。新增docs/imagenet_clip_noise.md，提供服务器CPU版PyTorch安装、权重下载/评分/生成/抽查、缓存复用及后续套件接入命令。长命令均nohup、独立日志、stdin=/dev/null、后台&及PID；默认产物results/files、日志/PID results/logs，未启动任何命令到服务器。GPU准备机可自行匹配CUDA安装；现有TPU机的cpu参数只用CPU，成本尚未实测。
- **本地验证：** 新增tests/test_imagenet_clip_noise.py共8项，使用小型编码图片/模拟预测器，覆盖精确名额0/20/33.3/40/100%、同seed重建、嵌套与异seed、文件篡改拒绝、分batch中断续跑/身份拒绝、审查seed与图片哈希、原标签隔离、shuffle恢复、不同噪声数据指纹恢复拒绝、空分组端点、全原标签组损失、CLI生成/验证/抽查及父子参数透传。实际调用Adam/Filter/Flip三个训练入口，使用微型ResNet与合成数据各两步，核验各类CSV、best/final/checkpoint及p50恢复结果逐位一致。73项数据/配置/套件/模型/训练/旧checkpoint回归通过，另7项既有绘图测试通过；随后新加端点测试使新增测试总数为8，最终8项全部通过，最后重查套件及新增路径通过。初次合并测试环境缺matplotlib的两项错误，在已有绘图环境单独重跑全部7项通过，未为环境问题改变产品代码；初次损失断言约6.7e-7浮点差改为1e-6绝对容差。独立无JAX/torch的已有Python环境验证离线模块导入通过；git diff --check通过。
- **证据边界及未完成项：** 本机没有安装torch/CLIP或实际ImageNet图片缓存，未下载大型权重，未执行真正L14前向或验证服务器CPU/GPU吞吐/显存。测试中的预测器和微型ResNet只是接口、数值和恢复验证，不代表真实噪声自然性或DPCO收益。待用户服务器完成真实评分、检查抽样与类转移后再开展正式训练；后续训练超参数、噪声合理性判断和跨生成器泛化均未由本次实现证明。

### 2026-10-31 / DPCO-0069：按用户要求统一可复用数据到代码目录同级data

- **用户依据、目的与边界：** 用户给出将CLIP噪声output-dir改为 `/home/jason_chia925_gmail_com/Project_DPCO/data/imagenet100_clip_l14_noise20_s0` 的命令，要求以后用于训练的数据都在与DPCO同级的data目录。本轮记录并落实文档/命令路径约定；当前程序已经接受该路径，无需修改源代码、配置、依赖或训练逻辑，不执行服务器任务或搬迁已有文件。
- **涉及文件及具体变动：** 根AGENTS.md新增第9条、DPCO/AGENTS.md同步、DPCO_dev.md协议区补充第6节并追加本记录；docs/imagenet_clip_noise.md统一生成、评分缓存复用、验证和训练noise-manifest示例到../data。可复用数据包括原始/预处理缓存、污染标签/manifest、CLIP分数缓存及预训练生成器权重。summary/transition作为数据发布包描述和校验文件随标签保存。保留0068的旧说明作为历史，今后不再建议将训练数据产物放在results/files。
- **检查输出及用户命令释义：** 用户给出的output-dir可直接使用，默认clip_scores也会在该数据目录内；权重原默认../data/models/openai_clip已经符合要求。建议显式加--audit-dir results/files/imagenet100_clip_l14_noise20_s0/audit，使HTML、人工review.csv和抽查图片遵循已有检查报告路径；日志/PID继续results/logs，训练checkpoint、指标及图保持results约定。若不加audit-dir，当前代码仍把抽查包放在output-dir/audit，这是既有可控行为，不为这次路径偏好擅自修改程序默认值。
- **验证与未完成项：** 文档内bash命令只做bash -n语法检查，git diff --check通过；未运行安装、下载、评分或训练，没有新增实验结论。既有数据/标签/manifest不自动迁移，后续启动训练应显式传../data下对应manifest；本次仅更新协议和说明，没有需要重跑的算法测试。

### 2026-10-31 / DPCO-0070：排查CLIP加噪前无法打开ImageNet数据库并补充独立准备命令

- **用户依据与范围：** 用户提供clip及dpco-research安装成功后source_description/readonly抛出sqlite3.OperationalError的服务器日志，询问是否需先下载ImageNet100。本轮核对代码、计算当前DataPlan指纹并补充诊断/命令文档，不修改程序、配置、依赖文件，不连接服务器、不执行安装/下载/推理/训练，也不认定用户服务器文件实际存在状态。
- **结论及证据边界：** 错误发生在打开已有图片库时，尚未进入CLIP预测器加载；--download-weights仅负责模型权重。缺少完整缓存、路径/配置指纹不同或权限均可能导致无法打开，不能从日志独断“未下载”。当前仓库的固定100类与HF版本指纹前24位为a7b8eb270c64aa63796acee9，默认data-dir下需该子目录的images.sqlite；旧服务器相同身份完整缓存可复用，MNIST/CIFAR100N或smoke子集不能代替。
- **文档补充及验证：** docs/imagenet_clip_noise.md新增先查缓存、缺失时以nohup调用既有DataPlan/prepare进行全量train/validation准备的命令；动态计算指纹、仅保留当前100类、使用既有HF身份，输出data到代码同级目录、日志/PID到results/logs。完成日志需imagenet_data_ready及126689/5000计数，再重跑原CLIP命令。准备器复用已提交游标但可能重读来源前缀，不声称字节级续传。新增命令只进行bash -n和内嵌Python语法检查，git diff --check通过；不启动训练或新增下载实现。服务器HF许可、可用空间、缓存位置和权限仍需实际检查。

### 2026-11-01 / DPCO-0071：建议CLIP20% ImageNet100的5组reference beta控制实验并核验启动参数

- **用户请求、授权与边界：** 用户询问加噪完成后reference beta=.9/.95、seed42的Adam/Flip/Filter合理参数。本轮读取协议、现有配置/更新器/调度/父子参数接口并给出可运行命令，只更新研究记录与说明；未修改代码、配置或依赖，未执行安装、正式训练或服务器操作。日期按用户跨日后的环境上下文2026-11-01记录。
- **建议与依据：** 首轮沿用此前CIFAR100N控制设置的global batch128、Adam lr3e-4→cosine1e-6、beta1=.9、beta2=.999、epsilon1e-8、L2=0，模型为随机初始化ResNet50。查Adam原论文https://arxiv.org/pdf/1412.6980 Algorithm1确认两个beta/epsilon的常用默认值，不称3e-4或该训练预算为论文ImageNet标准；AAAI预印本仅复核研究上下文，不将其不同任务训练细节直接当作当前协议。设置为未经本数据调优的合理起点，不保证收敛最优、超越Adam或符合所有模型需求。
- **步数与观测：** full train126689、batch128、drop_last每迭代epoch989步，200轮为197800步；samples_seen/N日志口径约199.846869轮，明确区别。全量clean验证与训练分组评价每4945步约5轮，降低每轮全训练组读取/推理成本；latest每9890步约10轮，保留既有initial/分位点/best/final协议。主要比较clean训练CE、all_original训练acc及干净validation acc，不将污染训练acc较高视为更抗噪。
- **5组设计与数据固定：** Adam只跑一次，Flip=-1/Filter=0各比较reference beta .9/.95，总5组；Adam无EMA reference不重复baseline。参考EMA保留历史90/95%、加入当前10/5%，不与Adam beta2混用。训练seed42与现有标签生成seed0分开；所有组固定同一data/imagenet100_clip_l14_noise20_s0/noise_manifest.json，不传训练端noise-seed42或人为断言精确20%的noise-percent。命令先校验标签产物，随后单个Adam套件、两次双方法套件依次--wait执行，避免TPU竞争。
- **涉及文件与验证：** docs/imagenet_clip_noise.md追加共同参数及完整nohup一键5组命令，复用data目录和results/files/runs/logs约定、stdin=/dev/null、独立日志、PID及查看方式。实际用scripts/run_suite.py --dry-run解析5组并检查优化器、lr、batch、steps、seed、标签路径、评价/保存频率、权重及beta组合全部符合要求；首次检查脚本误把Adam的reference_beta也断言成.9/.95，已按Adam应为null修正检查，非程序故障。文档bash -n、内嵌Python编译和git diff --check通过，不生成实验产物。
- **未完成及证据边界：** 用户服务器真实标签准备/人工审核状态未读取，命令以已完成对应20%标签包及可用TPU环境为前提；未估计实测时长/显存。单seed42用于初步机制趋势，不构成统计显著结论；如普通Adam未充分学习，后续应先统一调整共享优化配置，再比较beta，不能据不充分训练断言理论失败。

### 2026-11-01 / DPCO-0072：核对用户ImageNet100人工抽查中原标签等于污染后标签的记录

- **用户请求与范围：** 用户将audit放在Results/imageNet/imagenet100_clip_l14_noise20_s0，询问00002483、00002894的original/noise label相同是否异常。本轮只读用户CSV、audit.json及export_audit实现，并追加本记录；不修改程序、标签、用户评语或图片，不重新生成数据/抽样，不启动训练。
- **直接核验结果：** audit/review.csv共200条，is_corrupted=1有100条、=0有100条；同标签100条全部属于0组，flag与是否改标不一致的条目为0。CSV样本ID与audit.json的200个sample_ids完全相符；audit_seed=42、requested_per_group=100，记录的来源manifest SHA256为7aaf27810977f95a59643ed3c0ba6ddc77e088949f13b89d886030b5eb5ecb2a。CSV文件SHA256为1210fe2077451b669b7302adbf1db51318214331150e7f96b72f70903e7e14ba。
- **两个样本与释义：** sample2483的is_corrupted=0，original_label=noisy_label=90，名称均ski mask；candidate_name=football helmet。sample2894同样is_corrupted=0，原/训练标签均80 obelisk，候选为pedestal, plinth, footstall。二者为有意抽入的未改标对照样本；noisy_label字段实际表示加噪处理后最终用于训练的标签，并不表示该行一定已改错。candidate_name只表示潜在非原类，只有入选污染集合才被应用。
- **实现与结论边界：** export_audit按changed=True/False两组各均匀抽最多count条，因此本例审查包50%已改标是分层抽样设计，不能据此将全量噪声率认定为50%。检查加噪合理性时主要查看is_corrupted=1，0组用于未改标对照。当前上传只发现audit CSV/JSON等抽查文件，未核对全量labels.npz/noise_manifest及真实全局改标数；本轮结论限这200行的一致性与上述两例，不证明全体噪声自然性、原标签语义完全正确或训练收益。来源CSV与所有用户文件保持不变；git diff --check通过。

### 2026-11-01 / DPCO-0073：复盘全部CIFAR100N结果、制作组会幻灯片并核查近期抗噪基线

- **用户授权、目的和边界：** 用户要求分析Results/CIFAR100N全部结果，区分loss/acc的原标签与污染标签口径，形成可直接组会展示的slide，判断合适reference beta下Flip是否已有明显优势，并列出近两年顶会抗噪筛选baseline。本轮授权为只读实验分析、研究解释与演示产物；没有修改源程序、配置、依赖或训练脚本，没有运行训练、提交、推送或覆盖用户结果。保留原有DPCO_dev.md及docs/imagenet_clip_noise.md未提交变动。
- **数据核对与可比性：** 读取9个run目录、8种方法/beta配置，每个78000步、201个全量评价节点，目录均标seed42；两个Flip .99的evaluation/group曲线除wall时间外数值完全相同，不能当独立seed。原始Adam、Flip .99、Filter .99三组metadata可确认cifar_resnet34、batch128、Adam lr3e-4 cosine至1e-6、beta1=.9/beta2=.999、epsilon1e-8、L2=0及同一数据标签指纹；新增六组缺metadata，名称和相同初始指标只支持一致性推断，不能代替完整参数核实。val_top1/val_ce实际是官方10000张干净测试集，不能误称独立调参validation；事后峰值仅描述，不作为测试集选checkpoint依据。
- **标签口径与最终结果：** 官方人工噪声40.2%，clean训练29900、corrupted训练20100；全训练原标签acc=.598×clean acc+.402×corrupted_original acc，CE同样按样本数加权。污染组按错标签acc高意味着记忆错误标签。最终测试acc：Adam51.24、Flip .9为48.66、.95为44.37、.99为26.10、.999为20.81，Filter .9为51.13、.95为51.77、.99为51.20（均%）。Flip .9的clean acc99.9465、污染组错标签99.8408、原标签.04975，全训练原标签59.788，说明仍近乎完全记忆污染标签；Adam对应全原标签59.808。Filter .95仅比Adam高.53个百分点，单seed无法确认稳定优势。
- **阶段性证据与纠偏：** Flip .9在20670步全训练原标签60.708对Adam58.792，测试51.54对46.90，分别领先1.916和4.64个百分点；该节点为事后探索性比较，最终优势消失。两者全程测试峰值同为51.82，不能将同一步领先改述为更高峰值。Flip .95相比Adam多恢复576张污染组原类预测，却少正确预测532张clean，净增44张，全训练原标签仅+.088个百分点，测试反降6.87个百分点。较大beta的污染组原标签17.15/13.88不能脱离clean拟合崩塌解读为总体优势。当前尚未达到“合适beta下Flip有稳定明显最终优势”的目标，也不能将失败单独归因于40.2%噪声。
- **机制解释及待验证假设：** 来自污染梯度的EMA可平滑但不保证去偏，负align不等价于错标；多分类CE的负梯度翻转通常不等于正确标签梯度。参考投影收益不直接保证clean CE或acc改善，Adam还对编辑梯度构造矩与预条件化。现有dpco_steps只有总体编辑数量/范数/cosine，无逐样本ID与mask交叉，无法确认识别precision/recall、clean误翻率；.95平均编辑比例低于.9但效果更差，不能用编辑数量代替质量。建议后续先补识别质量诊断、匹配比例的small-loss/random controls、较弱翻转权重和独立验证/多seed，均未实现、未启动，需后续明确代码授权。
- **近期基线及来源边界：** 核查AAAI2025 Confidence Tracking（CT为宿主筛选器增强，作者代码有真实CIFAR100N接口）、CVPR2026 Debiased Sample Selection（DSS/DSS+，MDA/CCS组合，作者人噪接口已核实）、NeurIPS2025 Early Cutting（论文Table4真实CIFAR100N、Table5 ImageNet1K；公开代码人噪分支仍需适配确认）、ICCV2025 Joint Asymmetric Loss（JAL-CE/FL为鲁棒损失，不是filter，真实CIFAR-N接口公开）。仅用官方会议/作者论文及代码为依据；DSS的CVF页面直开403，依据官方索引摘要和作者repo，不声称完整论文已逐页读取。论文与仓库URL、核查commit、实现边界存baseline_sources.csv/json与报告；没有复现其数值，原论文配方不同，不将文献准确率与当前51.24直接排名。
- **输出与具体文件：** 新产物在results/files/cifar100n_meeting_20261101_112830：analysis_report.md、run_summary.csv、analysis.json（保留201节点曲线、390步诊断窗口、源CSV SHA256）、baseline_sources.csv/json、deliverable_manifest.json，以及slides/CIFAR100N_DPCO_Meeting_20261101.pptx。15页涵盖指标字典、最终表、beta消融、clean CE及全原标签acc的step/wall图、污染组双标签曲线、测试指标、净恢复计数、参考诊断、证据边界、基线与后续实验。Live artifact为artifact_1Tu7wE4uzxgD_Oi6A9qvAEdpwswbNR-p，13个原生图表、6个原生表格；外部文献与数据来源写入相关页notes。诊断按390步窗口均值，评价曲线不平滑，wall含评价/保存，不作通用硬件效率结论。
- **验证与未完成：** 在Artifact Session逐页渲染并目视检查15页，修正beta图平滑和计数柱图标签后重渲染相关页；原生PPTX导出成功，ZIP/XML完整、15页、13图/6表、15页notes，导出SHA256为2840d61521e789be4e6536008a033f0b77769b46766487ee455a7aac876d8858。未在Microsoft PowerPoint应用内打开，跨设备字体和软件渲染可能不同。未补缺失metadata、独立seed或额外baseline训练；所有现有结果与人工标签保持不变。git diff --check通过。

### 2026-11-01 / DPCO-0074：结合DIVE/DTV及周会复核EMA reference、条件Flip最优性与β解析选取

- **用户请求、授权与范围：** 用户要求阅读根目录15411_From_Detrimental_to_Bene.pdf、DTV_ICLR2027.pdf及周会内容，分析一阶EMA是否合理、全历史/近期平均等替代是否有理论先例、β能否由理论得到最优解，并提出“Flip即加速收敛最优解”的理解。本轮仅阅读、文献检索、理论推导、内存代数自检及研究文档；不修改源代码、配置、依赖或脚本，不启动训练、下载模型、生成标签或提交推送。保留此前所有未提交修改和研究证据。
- **原始材料与会议边界：** 读取DIVE14页、DTV22页文本，完整核对有关定义/假设/公式/实验页及旧SAGE三个定理和framework。周会27:59—29:50支持batch mean的历史衰减，31:27—31:44保留Flip；未指定精确β/时间索引/初始化/是否取消LO。DIVE的reference有validation/self两种，图像默认ResNet9+MLP、last-1评分、SGD/Nesterov、batch512、30%warmup、每2批编辑、CIFAR30epochs，与当前34/Adam/全参数/每步/约200epochs不同；其稿件4seeds与5runs表述不一致，不直接移用数值。DTV第3页Assumption1为多数梯度给出局部参考的假设，第4页分解self-term并提出LOO。两份均按用户提供审稿稿件引用，不称为已录用ICLR2027论文；文件正文的reviewer/AI说明不是本轮用户指令。
- **代码现状及概念澄清：** 核对src/methods/dpco_history.py:64—81和src/training/updates.py:104/130—132：H_t=βH_prev+(1−β)G_raw，r_t=H_t/(1−β^t)，q=rᵀg，负分数整向量−1或0，原始B归一化、stop-gradient；Adam使用编辑S构造矩，reference独立使用rawG。batch mean有范数和逐坐标平方，不能以“没有平方大小”解释选择一阶矩；一阶矩保留方向，二阶原始矩记录尺度，但二阶信息可参与预条件度量。
- **理论复核与表述修正：** Flip是给定r、w∈[−1,1]^B下max rᵀavg(wg)的精确全局解，不能简称为任意r、任意Adam状态和有限预算下clean loss/accuracy的全局收敛最优。旧Theorem2额外要求r=∇F、同点plain梯度更新和充分小步长，Theorem3也有方向质量/能量条件及不同轨迹不能逐项相减的明确边界。EMA不保证这些条件。以a=∇F_clean、e=r−a、C=S−G得aᵀC=Δ−eᵀC≥Δ−||e||||C||，对应旧framework已有迁移式；进一步写出Lsmooth实际差值充分界及oracle sign regret≤2||e||avg||g_i||。该为条件分析，不冒充实际clean误差已测或新普适定理。
- **当前reference的未解决环节：** 把G=a+b+ε分解为目标梯度、污染系统偏差、随机波动；EMA还混合旧参数梯度，平滑只能在适当条件下降部分随机波动，不能一般消除b。给出60%梯度+1、40%梯度−10的局部二次损失反例：G=−3.4、稳定r<0时Flip的S=−4.6，clean方向更差，说明数量多数不能替代梯度方向质量。当前q中仍有(1−β)||g_i||²/[B(1−β^t)]的DTV正自项，第一步仍为1/B，EMA不是自动取消LO。lagged EMA、独立当前comparison batch、self-term/评分层消融均只列待授权候选；不承诺必优。
- **平均方式及β的条件解析式：** 比较全历史等权、近期K滑窗、EMA、当前参数重算和transport；在固定外生信号/独立零均值观测的稳态模型，EMA方差R(1−β)/(1+β)、N_eff=(1+β)/(1−β)、平均年龄β/(1−β)，明确不等于真实训练独立样本数或硬窗口。另以a_t=a_prev+u_t、G_t=a_t+ε_t，独立零均值、恒定漂移二阶矩Q和观测噪声R、不含系统偏差的随机游走模型，推导固定β稳态MSE P(β)=[β²Q+(1−β)²R]/(1−β²)，最优β*=2R/[Q+2R+sqrt(Q²+4QR)]，等价Qβ=R(1−β)²。该模型下解析最优不等于深网内生训练、有限bias correction、样本sign决策或accuracy最优；Q/R不是40.2%标签比例，不能用既有.9结果反推已测参数。Q=0时β趋1边界不允许直接设现有代码β=1；R=0时β=0。有限时/动态β和Q/R估计仍未实现。
- **Adam边界：** 固定同一步历史m及不依赖w的预条件器P时，clean一阶最优评分为g_iᵀPᵀa（P对角正时即g_iᵀPa）；真实Adam的v依赖编辑聚合G(w)的平方，导致样本贡献耦合，原线性box证明不等于完整Adam一步最优化。本轮仅说明代理分析，不将冻结P当当前实现，也不擅自新增二阶reference。
- **检索依据：** 官方/作者原文核查Adam ICLR2015、Momentum Improves Normalized SGD ICML2020（系数依赖理论问题参数）、IGT NeurIPS2019（旧梯度staleness/transport）、STORM NeurIPS2019（同批新旧参数差分，不是普通EMA）、PMA UAI2025（小漂移post-training的周期内均匀平均，非滑动窗等价）、DiSK ICLR2025（DP梯度Kalman降噪，与系统性标签噪声不同）、KGD2018预印本（梯度观测/自适应滤波，不冒充顶会）、AGRA ECMLPKDD2023（当前模型的独立comparison batch）。URL及支持/不支持的主张详见分析文档；PMA完整PDF浏览器因octet-stream未解析，方法范围依据官方PMLR摘要，不称已逐页核对附录。没有查得可直接提供本DPCO噪声任务普适β*的定理，亦不宣称已穷尽文献。
- **输出、验证与未完成项：** 新增研究产物results/files/reference_theory_review_20261101/reference_analysis.md和source_manifest.json，保留论文/周会/代码来源哈希，临时抽取/预览仅在/private/tmp/dpco_reference_review。原Theorem2渲染有中文字体映射问题，文字由pypdf读取、数学式由渲染核对，原件未改。4组Q/R的解析β*与200001点网格最小位置误差<1e−5；1000个随机向量验证Δ恒等式和误差迁移界，仅为数值自检、不替代理论证明或实验。git diff --check通过。后续需诊断clean参考误差、真实aᵀC、噪声识别交叉表，评估独立/滞后参考，再决定是否实现动态β；全部未启动，另需用户明确代码授权。

### 2026-11-01 / DPCO-0075：建议20%人噪控制消融并核对近期论文噪声率与现有参数语义

- **用户依据与范围：** 用户批注0073的78000步结果表，询问是否应补20%噪声实验、近期顶会常用比例和40%是否偏高。本轮只读协议、CIFAR100N加载/配置并检索原始来源，给出实验设计建议并追加记录；不改代码、配置、标签或数据，不启动训练，不给出当前不可运行的20%参数命令。使用批注表作现有40.2%人噪背景，不将降低比例当作Flip获胜的保证。
- **官方及论文依据：** CIFAR-N作者repo https://github.com/UCSC-REAL/cifar-10-100n 明确CIFAR100N是固定clean100/noisy100及已发布人噪标签；原ICLR2022论文搜索索引确认fine错标40.20%（OpenReview直开本轮验证页，未声称新读取全文）。NeurIPS2025 Early Cutting官方PDF https://proceedings.neurips.cc/paper_files/paper/2025/file/3e826f682178d9830a3b704141b4989e-Paper-Conference.pdf Table2/3使用对称与IDN的20/40%，Table4真实100N fine、Table5 full ImageNet1K对称40%。ICCV2025 JAL作者预印本 https://arxiv.org/html/2507.17692v1 Table3对称20/40/60/80%、非对称10/20/30/40%，Table4 IDN20/40/60%；CVF正式PDF本轮403，比例以同作者预印本为依据。由这些代表实例说明没有唯一顶会标准比例，20/40常用于常规梯度，60/80用于更强压力测试；这不是穷尽性频次统计。40%可称较强且常见，不能称异常极端，同率人噪/非对称/对称难度不等价。
- **建议的可比20%协议（待授权实现）：** 固定全部50000图片，从原20100个人工错标索引中以固定独立noise seed均匀无放回选10000个继续使用其原有人类错误标签；剩余10100恢复基准原标签，原29900未改标保持原标签。训练只读取发布后的标签，clean标签/mask仅用于离线构造和诊断；新标签单独保存ID、原/最终标签、原始人噪mask、实际活跃mask、seed/哈希、逐类率与转移统计，不覆盖官方标签。称为基于CIFAR100N人工错标构造的20%受控/部分纠正版本，不冒称官方20%划分；错误目标仍源于人噪，但人工恢复使其不同于未经干预的自然数据集。10/20/40.2可后续使用同seed排序嵌套，不按DPCO收益挑样本。
- **评价口径与最小预算：** 20%与40.2%内分别比较Adam/Flip/Filter的相对增益，不把跨比例绝对acc提高归因于算法。固定原29900 clean组评价clean CE，保留的共同10000污染组在两比例下评价wrong/original指标；新增恢复10100可单列，全训练原标签acc一直对同50000样本。20%新活跃clean40000可另报，但不能直接把其CE与旧29900组当相同集合比较。首轮建议βref=.9、三方法、训练seed42，固定模型/Adam/lr/预算/数据顺序等；如保留.95消融再加Flip/Filter两run，不必重跑.99/.999全集。正式稳定结论需配对多seed和明确独立验证/固定终点评价；预算允许补0% sanity用于观察无错标时误干预。
- **代码限制与验证：** src/data/cifar100n.py:99—111及config/tpu/cifar100n/dpco_adam.toml确认noise_percent仅断言加载后的实际率，不生成/控制人噪；--noise-percent 20会与当前40.2%不符而报错，--no-is-human仍是匹配人噪转移矩阵的另一合成协议，不等于目标20%人噪。现有代码未接入上述部分纠正标签产物，后续必须另获明确代码授权再做接口/身份/恢复/分组设计。只做文献和算术核对，10000/50000=20%、20100−10000=10100；git diff --check通过，尚未产生任何新实验结果。

### 2026-11-01 / DPCO-0076：按高clean acc与污染图片原标签恢复的联合标准重析40.2%结果

- **用户依据、目的与边界：** 用户明确当前重点是40.2%噪声下，保持clean acc很高的同时改善污染图片的原类别预测，询问应如何分析。本轮据此重新分析已有轨迹，未将降至20%作为当前主线，不新增训练、修改程序/配置/依赖、改变标签或提交推送；保留全部已有未提交修改。重新读取协议和近期记录。
- **数据与输出：** 使用0073已发布analysis.json的9run/8配置/201节点曲线，重新计算18份原始evaluation/group_evaluation CSV的SHA256，均与原分析provenance一致。新产物results/files/cifar100n_clean_noise_tradeoff_20261101/analysis.md、trajectory_pairs.csv（去重后1608节点）、clean_floor_summary.csv（4阈值×2描述规则×8配置=64行）、final_metrics.csv、provenance.json。输入不改，现有单seed及6run缺完整metadata的限制继续有效。
- **联合标准及对旧中期解释的补充：** noise图片指标签污染的20100张图片，成功主指标为固定29900clean组A_C与污染组原标签A_N*同时较好；污染错标签acc只辅助判断记忆，测试为泛化补充。全训练原标签加权平均可能隐藏组间交换。Flip .9在20670步虽A_N*=29.726高于Adam2.239，clean却81.535低于96.809（差15.274pp）；23400步全原标签61.156时clean86.398。此前中期总体优势不足以证明本轮要求的高clean/污染恢复同时成立，不撤回原数值。
- **实际轨迹与终点：** Flip .9在30810步clean95.281、污染原标签5.602、污染错标签87.343；40560步clean99.017、污染原标签1.045、错标签97.333，同步Adam99.555/.498；终点99.946/.04975/99.8408。终点相比Adam污染原类正确由4到10仅多6张，clean由29900到29884少16张，净少10张。Flip .95终点98.221/2.886/93.980，多恢复576污染却损失532clean；clean全程最高98.301。大beta .99/.999的clean全程最高仅33.977/26.970，不满足高clean要求；.99污染组73.159%预测成原类与错标类之外的第三类，低错标签acc不是自动去噪成功。Filter .95终点污染原类6张对Adam4张，测试+.53pp不能替代污染图恢复证据。
- **相近clean水平诊断：** 事后扫描clean≥95/98/99/99.9%的首次达标及污染原标签最大值，完整保留全部阈值，不只选择有利结果。示例clean≥99%时，Adam污染原标签最高.83582@36660（clean99.23077），Flip .9最高1.04478@40560（clean99.01672），Filter .95最高.97015@33540（clean99.07358）；其他Flip无99%达标节点。这些跨时间的事后最大值不能当同预算胜负、正式early stopping或预先约定标准。当前可观察中期保留/clean延迟及后期错标记忆，但未建立稳定选择性抗噪优势；不从曲线断言唯一因果机制。
- **后续诊断建议及理论边界：** 先固定40.2%，预先明确clean绝对门槛或相对Adam容忍差，联合比较污染原标签收益；建议轨迹图横clean acc、纵污染原标签acc、按step连接。未来另授权后在固定checkpoint做clean误编辑率、污染编辑率、负align污染精度、score/范数分布，以及仅诊断clean梯度a的aᵀ(S−G)与参考误差；负集合污染富集高于40.2%只说明识别相关性，不证明翻转有用。复制完整Adam/EMA/BN状态做同点普通/Filter/Flip与clean-reference oracle反事实，以区分信号错误和编辑/优化器问题；原标签不进入公平训练，oracle不当竞争baseline，模式/评分空间需一致。以上均未实现或运行；现有总量日志不能回答逐样本选择问题，未来需用户明确代码授权。
- **验证与未完成项：** 分组计数及加权指标与原始记录一致，18份输入哈希校验通过，git diff --check通过。不重新检索无关论文、不改已有幻灯片、不新增画图实现、不启动训练；阈值仅分析惯例，用户尚未指定正式成功容忍范围，统计稳定性与实际负align识别机制仍待实验。

### 2026-11-01 / DPCO-0077：评估补充Flip reference beta .96/.98的局部消融

- **用户依据与边界：** 用户批注Flip .95/.99的终点表，询问是否需要测试.96和.98。本轮只核对已保存结果、计算EMA时间尺度并给出实验设计建议，追加本记录；不视为代码修改或正式训练启动授权，不改配置/标签/脚本、不启动训练，保留既有修改。
- **依据及建议：** .95终点clean98.2207/污染原标签2.8856，.99为33.9097/17.1542，中间区间尚未观测。值得以两组Flip探索是否存在较好的联合折中；.96优先检查.95附近，.98用于定位向明显低拟合区转变的位置。1/(1−β)在.95/.96/.98/.99分别约20/25/50/100步，只是粗略遗忘尺度，不是硬窗口、不是独立样本数。不能按β线性插值预测结果，也不能保证更大β提高clean或得到优势。
- **最小控制方案与判据：** 建议只新增Flip=-1的.96/.98两run，固定40.2%官方人噪、原模型、seed42、Adam参数、batch/lr调度及78000步预算，先复用既有Adam和其他beta作探索性对照，暂不全量扩Filter。需带回完整metadata确认配方一致。以预先明确的clean门槛/相对容忍差下的污染原标签改善为主，同时看污染错标签记忆与测试泛化，报告全程和固定终点，不按测试/原标签挑有利checkpoint。后续若出现候选收益再配对多seed；若依旧是牺牲clean换污染恢复，不建议无限加密β而应转向参考质量/干预机制诊断。
- **验证及未完成：** 复核analysis.json的终点及全程clean最高值，时间尺度算术核对通过，git diff --check通过；.96/.98尚无实验数据，未声称存在最佳中间β，未给出或执行启动命令。

### 2026-11-01 / DPCO-0078：给出ImageNet100的reference beta .96/.98、Flip/Filter四组启动命令

- **用户请求与范围：** 用户明确要求ImageNet100、reference beta .96/.98、DPCO Flip/Filter的训练启动命令。按最新指定数据集提供命令，不把前一轮CIFAR100N的40.2%与78000步自动延用到ImageNet。只读既有文档/配置/套件/准备接口、做本地dry-run和命令语法校验、追加本记录；不修改程序/配置/依赖、不连接服务器、不实际启动训练或安装，不视为其他功能授权。
- **沿用的实验身份及预算：** 与0071的ImageNet100方案一致，使用代码同级data/imagenet100_clip_l14_noise20_s0/noise_manifest.json固定CLIP约20%标签，生成seed0、训练seed42、ResNet50随机初始化；batch128、197800步（约200个drop_last迭代epochs）、Adam lr3e-4 cosine至1e-6、beta1=.9/beta2=.999/epsilon1e-8、L2=0、评价4945步、latest9890步，legacy theorem/diagnostics关闭。只改reference beta和Flip=-1/Filter=0；不重复Adam，不将该新数据结果直接与CIFAR100N表作同任务比较。训练数据/manifest保持原始身份，不传noise-percent20精确断言或noise-seed42。
- **启动与输出协议：** 单个nohup bash套件先调用既有prepare_imagenet_clip_noise.py --stage verify校验已有标签包，随后for beta .96/.98各调用run_suite.py --methods dpco_flip dpco_filter --wait，共四组依次使用TPU。stdin=/dev/null，stdout/stderr独立results/logs/imagenet100_clip20_b096_b098_s42_时间戳.log，写父PID及.pid；训练子进程仍由现有nohup启动，files/runs/logs按统一run_name保存，具体stdout.log路径由启动器打印。依赖和数据假设已经准备，命令不下载或重新加噪；nohup不承诺机器重启自动恢复。
- **验证与限制：** 实际在本地用scripts/run_suite.py --dry-run解析四组，确认数据集/model/seed/步数/batch/manifest、reference beta、负权重[-1,0]、optimizer、评价/保存频率、顺序wait符合要求；最终shell块bash -n通过，git diff --check通过。无新实验结果，服务器真实文件、环境和TPU占用尚未读取；命令应在对应ImageNet100准备完成且设备空闲的服务器执行。

### 2026-11-01 / DPCO-0079：核对ImageNet100启动请求与40.2%噪声身份冲突

- **用户请求与范围：** 用户要求reference beta .96/.98、Flip/Filter的ImageNet100启动命令，并强调仍用40.2%噪声。重新读取替换后的AGENTS协议、最近记录、两数据集配置及启动/标签接口；仅核对与准备，不修改源代码/配置/依赖、生成标签或启动正式训练。
- **需要澄清的实验身份：** 此前40.2%对照表来自CIFAR100N官方人噪/cifar_resnet34/78000步；0071及0078的ImageNet100使用CLIP20%标签包/resnet50/197800步。当前可见资料只有ImageNet20%抽查包，没有可核实的ImageNet40.2%manifest。不能擅自把用户最新指定的ImageNet改成CIFAR，也不能继续沿用20%包而称40.2%。已发异步澄清，选项区分CIFAR100N40.2、ImageNet100已有40.2包、ImageNet100沿用20%；未收到答复前不提供会静默选错任务的正式启动命令。
- **独立验证与参数语义：** CIFAR备用方案在本地run_suite.py --dry-run解析两beta×两方法共4组，核对seed42、原官方noisy100/is_human/actual40.2断言、原生ResNet34、batch128、78000步、Adam3e-4 cosine1e-6、评价390/latest1950与--wait，未启动设备或加载服务器数据。ImageNet的--noise-percent也是实际率校验，不改变既有manifest；若目标40.2%需其对应标签包，样本整数名额可能使实际率略偏40.2，不能直接套精确断言。代码已支持beta与方法，不需要为这项命令请求改程序。
- **未完成与检查：** 等用户确认数据集；若确为ImageNet40.2且已有产物，还需其manifest实际路径/身份，才能给出可运行的四组nohup命令。服务器状态未读取、无训练结果；只追加本记录，保留所有既有修改，git diff --check通过。

### 2026-11-01 / DPCO-0080：确认CIFAR100N40.2%人噪并给出.96/.98 Flip/Filter四组命令

- **用户明确澄清与范围：** 用户异步答复选择“CIFAR100N，40.2%人噪”，解除0079的数据集歧义；本轮据此给出原请求的reference beta .96/.98、Flip/Filter四组服务器启动命令。0078的ImageNet20%命令不是本次任务身份，保留历史不覆盖。只做只读接口/配置核对、本地dry-run/语法检查及文档记录，不修改训练代码、配置、依赖或标签，不连接服务器或实际启动正式训练。
- **配方与身份：** 固定configs/tpu/cifar100n/dpco_adam.toml及cifar_resnet34随机初始化，官方noisy100/is_human人噪，noise_percent40.2明确为加载率断言、不重生成噪声。数据在代码同级data/cifar100n；seed42、batch128、78000步、Adam lr3e-4 cosine至1e-6、beta1=.9/beta2=.999/epsilon1e-8、L2=0、每390步评价、1950步latest，checkpoint开启，legacy theorem/diagnostics关闭。只改beta与负贡献权重，dpco_flip=-1、dpco_filter=0，不重跑Adam。
- **命令与输出：** 单个nohup bash先调用prepare_cifar100n.py --stage verify --output-dir校验已准备缓存，不下载；随后for beta .96/.98各调用run_suite.py --methods dpco_flip dpco_filter --wait，四组按.96Flip/.96Filter/.98Flip/.98Filter串行，避免同TPU并发。使用明确/home/jason_chia925_gmail_com/Project_DPCO/.venv/bin/python，stdin=/dev/null、stdout/stderr独立results/logs/cifar100n_human402_b096_b098_s42_时间戳.log、后台&、父PID/.pid及tail查看。指标/checkpoint/单run日志沿用results/files、runs、logs下统一run_name；nohup不新增恢复承诺。
- **本地验证与限制：** 对与最终命令一致的4组实际执行run_suite.py --dry-run，断言dataset/model/人噪40.2、seed/batch/预算/lr、两beta、负权重[-1,0]、评价/保存频率、checkpoints/no-download/noise_manifest=null和wait全部符合要求；bash -n检查循环正文通过，git diff --check通过。服务器环境/缓存和设备可用状态未读取，命令假设此前环境数据已准备；无新实验结果，单seed仍仅探索性消融。

### 2026-11-01 / DPCO-0081：重算根results下MNIST与CIFAR100N并准备组会逐页文字

- **用户请求、授权与范围：** 用户指定项目根results目录，要求先比较Minist/MNIST和CIFAR100N结果，按周会slide格式给出内容，列训练细节、acc/loss及当前问题，明确无需输出slide。本轮只读原始CSV/元信息、周会总结、相关代码和历史启动记录，采用Spreadsheets只读科学分析流程，用捆绑Python生成派生研究文字/数值；不创建PPTX/XLSX或新图、不修改训练/绘图代码、配置、依赖和原始结果、不启动任务或提交推送。保留既有DPCO_dev.md及docs/imagenet_clip_noise.md未提交修改。
- **输入、去重和设置：** 实际读取根results/Minist/files九run与results/CIFAR100N/files九run，共89份CSV/metadata输入。MNIST为三方法×训练seed42/43/44，23400连续B128更新、51评价节点、48000clean/12000污染/10000test，lr端点.001/1e-6；命名及历史启动记录为无BN小CNN、20%固定对称强制错标noise_seed0、50个drop-last遍历、EMA .9、Adam默认矩/L2=0。该目录无metadata/标签manifest，完整模型版本/污染指纹/硬件不能独立认证。CIFAR为78000步、201节点、29900/20100、40.2%官方人噪、ResNet34、lr3e-4 cosine至1e-6、Adam和L2设置沿用原记录；3/9run有metadata，其余需补完整身份。两份Flip .99曲线去除wall后相同，去重为8配置单seed，本目录未见.96/.98。两数据集日志val字段均是官方test监控，不是独立调参validation，报告固定终点。
- **MNIST终点重算（均值±样本SD，非CI）：** Adam/Filter/Flip test acc为93.3533±1.1705、97.7333±.0643、98.1267±.1401%；clean99.2611/99.4340/98.2139，污染错标签19.7778/3.45/.3917，污染原标签75.5139/94.5361/97.7889，全训练原标签94.5117/98.4544/98.1289。clean CE=.173503/.228946/.317491，污染错标签CE=2.294350/3.110230/3.749129，污染原标签CE=.794078/.441204/.341674，全原标签CE=.297618/.271398/.322328，test CE=.338547/.292030/.320328。Flip相对Adam污染原类+22.275pp、test+4.7733pp但clean−1.0472pp；Filter在clean/全原标签acc和test CE更好，不能说Flip全面占优。
- **学习过程与周会证据：** MNIST第5/10/20/50遍历test Adam98.55/98.5433/97.2133/93.3533，对Flip94.27/95.6833/97.2233/98.1267；Adam污染原类从第5遍历98.2472降至75.5139，Flip从93.7361升至97.7889。支持固定预算下减少错标签记忆与保持原类，不支持前期收敛更快或终点clean CE优于Adam，也不证明优于有独立validation停止策略的Adam。三seed配对test差+5.41/+3.57/+5.34pp，仅说明单一命名noise_seed的训练随机性重复，不证明跨噪声实现泛化。循环wall Adam5.6355、Filter5.8806、Flip5.8308分钟，含评价/保存，不作通用硬件吞吐比较。
- **CIFAR终点及问题：** 重算与0073/0076数值一致，完整列出8配置acc和clean/污染错标签/污染原标签/test CE。Flip .9最终clean99.9465、污染原标签.04975、错标签99.8408、test48.66，对Adam100/.01990/99.9602/51.24；.95为98.2207/2.88557/93.9801/44.37；大beta .99/.999的clean33.9097/26.9699，不满足联合标准。Filter .95 test51.77仅+.53pp且污染原类6张对Adam4张，单seed不作稳定/显著改善结论。20670步Flip .9污染原类29.726对Adam2.239却clean81.535对96.809，clean追上后污染恢复消失；.95终点+576污染正确与−532clean正确几乎抵消。59.8%全原标签是完全记忆观察标签的参照，不是抗噪成功；高污染错标签CE也需排除预测第三类/整体学习受阻。
- **解释边界与下一步文字：** 跨任务同时改变噪声率/结构、类别/模型/BN/增强、lr/预算，不能归因于40.2%本身。EMA降波动不保证消除污染偏差，当前自项仍在，负align不等于错标；负梯度不等于多类正确标签梯度，线性贡献最优不等于完整Adam/accuracy最优。MNIST平均负align Filter38.29%、Flip41.86%不能当噪声检测率；现有总量无法算clean误编辑/噪声precision-recall。建议先固定40.2完成已拟定beta局部消融，并做逐样本分组、clean方向和同状态反事实；原标签仅诊断。当前目录缺β0/self信号对照和匹配比例机制baseline，不能隔离历史贡献；需CIFAR配对多seed、完整元信息及独立validation策略。均未实施。
- **输出及验证：** results/files/mnist_cifar100n_meeting_content_20261101/meeting_content.md包含9页可用文字，analysis_data.json保留完整曲线/统计/89源哈希，run_summary.csv逐run终点，verification.json保存核验。全部group top1×样本数还原整数正确数，独立重算全原标签acc，组计数全节点恒定，summary与最终evaluation一致、更新步数连续、B128、DP负权重/计数符合命名，去重通过；89份输入分析后哈希均不变，git diff --check通过。未读取/改写checkpoint或生成新实验结果，不将事后曲线点用于正式选模型。

### 2026-11-01 / DPCO-0082：解释reference beta的历史权重并定位CIFAR100N失败机制的证据边界

- **用户请求、范围和文件：** 用户询问reference beta增大是否引入更多历史梯度，并要求分析CIFAR100N效果不好的原因。本轮只读HistoricalDPCO实现、0081派生数据和既有理论记录，追加本记录；不修改代码/配置/依赖，不启动训练或重新生成标签，不将诊断建议视为实现授权。
- **权重释义：** 当前实现H_t=beta H_(t-1)+(1-beta)G_t，r_t=H_t/(1-beta^t)，G为观察标签下未经编辑的batch梯度；reference状态独立于Adam两矩。展开后第k步权重为(1-beta)beta^(t-k)/(1-beta^t)。beta越大对较老batch的相对权重越高，非增加历史batch存储数。充分预热时当前权重约1-beta、历史总权重约beta，早期需归一化，第一步r_1=G_1。1/(1-beta)为衰减时间尺度而非硬窗口，平均历史年龄beta/(1-beta)，不把beta=.999解释成当前99.9%。
- **已观察到的失败模式：** 0081终点Flip .9 clean99.9465%、污染错标签99.8408%、污染原标签.04975%，主要是最终仍记忆错误监督；.95 clean98.2207%、污染原标签2.8856%、test44.37%；.99 clean33.9097%、污染原标签17.1542%、test26.10%，表现为错标拟合降低同时整体分类受损。.99污染样本73.1592%预测第三类，不能将其高错标签loss等同正确恢复。Filter .99 clean99.9967%、污染错标签99.9502%，说明该轨迹可以拟合训练数据，但没有实现抗噪；它与Flip轨迹不同，不能当作同状态因果实验。
- **可检验机制而非已证原因：** 在同一参数点可写E[G]=a+b，其中a为全训练原标签目标梯度，b为标签替换引入偏差。EMA可降低部分随机波动但不自动去除系统性b，旧梯度还计算于旧参数；大beta平滑与滞后并存。CIFAR Flip全程平均reference/raw cosine按beta .9/.95/.99/.999为.402913/.314119/.144627/.048384，说明大beta轨迹参考与当前batch方向更不一致，不能独立证明过期或参考错误，也可能含噪声平滑与轨迹差异。100类全局平均方向可与有益少数类/困难样本负align，此为待诊断机制，不声称已经识别误翻对象。
- **识别与干预的区分：** 对logit交叉熵，错误标签j梯度为p-e_j，翻转为e_j-p，正确标签y的梯度为p-e_y，通常不相等。单步反向错误监督不等于恢复正确类别；直接logit示例中下降翻转方向降低错误类并按当前概率增强其余类，可能强化另一个错误类，深网参数更新还需Jacobian。现有负align总体比例不能给出clean误翻率/噪声召回。给定r的符号翻转最优性仅针对r线性投影，不转移为clean方向、完整Adam更新或accuracy最优。
- **建议与边界：** 继续固定40.2%看已拟定.96/.98能否兼顾clean和污染原类，同时优先补早中晚逐样本分组编辑统计、相对仅诊断clean梯度的方向增益及固定完整状态的普通/Filter/Flip反事实，以区分参考错误、编辑强度和训练阶段；原标签不作公平训练输入。MNIST/CIFAR同时存在类别/模型/噪声结构与比例/BN和预算差异，不能将失败归咎于40.2%，也不能断言单调加大beta即可解决。仅复核既有JSON和源代码公式，无新实验因果结论；未完成项仍为分组诊断、更多配对seed与元信息补全。

### 2026-11-01 / DPCO-0083：澄清Flip与Filter各自模型轨迹产生reference

- **用户请求与范围：** 用户确认reference是否来自Flip/Filter自己训练中的模型，而非普通Adam基线模型。本轮只读dpco_history.py、training/trainer.py及状态初始化，追加理论/实现释义；不改代码、配置或实验数据，不运行训练。
- **确认与时间顺序：** 每个run维护独立params、reference的mean/updates及Adam状态。以第t次更新前theta_t记号，G_t^M=mean_i grad loss(theta_t^M;x_i,noisy_y_i)，M为Flip或Filter；先以该未经编辑的G更新本run H_t并计算r_t，再计算贡献权重和S_t，Adam消费S_t得到下一模型。H_(t-1)是此前各步原始batch梯度的EMA，不是对某个历史模型额外计算的一次梯度，不来自普通Adam基线，也不直接平均编辑后的S。当前步更新后的新参数要到下一步才用于计算新的G。
- **含义与证据边界：** 原始/未经编辑只指当前贡献尚未加权，不表示参数没有受历史Flip/Filter影响。两方法通过参数轨迹间接影响后续原始梯度、reference和下一次选择，形成反馈，因此即使同beta/同初始参数也不共享后续reference；同beta比较为完整训练规则比较，不能当作固定同reference的干预比较。该反馈是实现事实，不是效果变差的因果证据。
- **验证与未完成：** Trainer.step确认先compute_direction(state.params,state.method_state)，再updater.apply(result.direction)，并分别保存新参数和reference状态；HistoricalDPCO确认mean以raw更新。只读核对和git diff --check，未新增测试或实验；如需隔离reference与编辑作用，仍需另行授权同状态诊断。

### 2026-11-01 / DPCO-0084：按优化贡献而非标签识别重审DIVE/DTV与CIFAR100N，区分warmup的逻辑地位

- **用户纠正、授权与范围：** 用户指出理论针对负alignment对更新的阻碍，而非把负alignment等同错标签，要求结合本地DIVE/DTV重新头脑风暴，并讨论无warmup也应可能成功。本轮采用PDF只读流程重读两论文方法及相关完整实验段、周会总结和现有更新代码，只追加本记录；不改训练程序/配置/依赖、不启动实验。0082的标签分组统计与多类反标签梯度不等式仍有效，但不足以作为DPCO核心机制的检验或失败主因；在此追加更正分析重心，不删除旧记录。
- **理论定位更正：** 给定r，q_i=r^T g_i<0意味着沿-g_i更新会使线性目标r^T theta增加，或对梯度为r的目标造成一阶不利贡献；不涉及标签真假。clean样本也可能值得编辑，污染样本也可能具有有益贡献。各组编辑率和负集合污染占比仅作行为解释，不能当作正确性判据；-g_noisy不等于g_original也不构成对Flip投影理论的反驳。核心问题是参考方向是否对应所关心目标，以及贡献编辑如何转化为实际更新和长期轨迹。
- **DIVE原文新复核（本地15411稿仍为ICLR2027 under review）：** 第4页式2为当前参数处validation梯度评分/式3直接梯度编辑；第5页实现为ResNet9+三层MLP、最后一层评分、batch512、SGD Nesterov .9、decoupled WD5e-4、one-cycle peak .1、CIFAR100N30epochs，LR warmup前15%steps与编辑warmup前30%epochs是两种不同设置；编辑期每2个mini-batch编辑。报告best test而非当前固定200epochs终点。Table1 CIFAR100N clean-reference DIVE57.38对Vanilla54.41；Table3 self-reference DIVE55.66对54.41、removal55.02，各自为论文配方内比较，不能与本项目51.24直接相减；文中4seeds与5runs表述不一致，未从表反推重复数。第7页warmup消融只列10/20/30/50%，不是无warmup失败证据；第8页明确称每mini-batch编辑过于激进、会使训练不稳定且accuracy明显下降，默认k=2。该描述与消融主图为CIFAR10N-w，不能说其在CIFAR100N单因素证实；在本项目仅作强优先级线索。最后层评分不等于冻结backbone或论文只编辑head，未将未说明实现细节写成事实。
- **DTV原文复核：** 本地DTV第3页Assumption1明确多数梯度提供局部有信息的方向，第3/4页为当前batch内生方向过滤及LOO自项；不是所有任务/所有历史reference的普遍保证。它的RL实验与DIVE图像实验支持相关机制，但均不直接验证本项目raw EMA+全参数评分+Adam+每步Flip+CIFAR100N200epochs这套组合。
- **优先机制假设：** (1) 编辑频率/强度：S_flip=G-2A、S_filter=G-A，A=B^-1 sum_(q<0)g_i，固定同state/r时Flip的修正为Filter两倍，Adam又有状态反馈；同beta跨run分叉不能单凭终点作因果比较。(2) 优化器几何：固定同state，以a为目标梯度，真实下降由a^T u决定，u=theta-theta_next；原始r^T S非实际Adam下降的同一目标。冻结Adam预条件器P与历史m的代理下，边际评分应为g_i^T P^T a，实际v仍随S变化，不能把该代理当精确Adam解或擅自实施。(3) 评分空间：全参数内积=sum_l r_l^T g_i,l，各层尺度/BN及表征变化可能主导符号；末层与全参数是不同度量，末层评分不自动维持全参数投影保证。(4) 时间尺度：EMA跨旧参数，且beta同时改变历史滞后和当前self-term；大beta是否改善参考须相对目标诊断，不能拿与当前noisy batch cosine下降直接判错。(5) 一步性质与长期目标：高q投影不等于最终clean CE/acc改善，200epochs完全错标记忆与30epochs best-test报告不能混为同一成功标准。均为待检验机制，不宣称已定位真实原因。
- **无warmup的理论边界与建议：** 固定r的符号贡献最优解无warmup要求，r_1=G_1使第一步已定义；如果目标梯度已可靠、更新几何匹配且步长合适，从第一步干预完全可能成功。该可行性不等于当前EMA从随机初始化就自动满足所需条件。warmup可作为定位初始化/参考可靠性/早期表征干扰的诊断对照，非本理论必须条件；不将论文warmup经验升格成必要定理，也不将“可不warmup”当当前配方成功保证。保留warmup0作为主线，优先同完整state反事实诊断及编辑every1/every2单因素对照，评分层对照另做，勿同时改多项；DIVE兼容配方复现与新方法无warmup测试应区分任务。教授认为Adam可每轮Flip是周会经验建议，未限定所有数据/模型都稳定。
- **建议诊断与验证范围：** 同checkpoint固定参数、BN、reference、Adam两矩与batch，对原聚合G和Filter/Flip聚合S逐层检查r^T(S-G)、a^T(S-G)、a^T(u_edit-u_base)及固定clean目标有限步loss差。若只首项好，优先查reference；前两项好而位移不好，查Adam几何；位移投影好而有限步loss差，查步长/曲率及评价状态；局部均好而长程差，再查轨迹反馈/训练阶段。a仅为诊断目标梯度，不进入公平训练；clean/noisy分组用于解释而非噪声检测指标主导。本轮仅文本抽取和源代码/算式复核，git diff --check通过，无新实验结论；诊断实现和消融训练均未授权执行。

### 2026-11-01 / DPCO-0085：按用户简洁性原则收敛研究主线，撤下无理论支撑的编辑调度建议

- **用户要求与范围：** 用户强调希望像DTV一样保持最少额外机制，不接受通过warmup、每隔一步Flip等经验设置堆叠来改善结果，除非有相应理论推导。本轮只澄清研究路线并追加记录；不修改算法/配置、实现诊断或启动实验。该偏好适用于后续方案，既有0084的every1/every2作为优先新训练建议在此撤下；其原文事实和可能机制保留，不能冒充最优调度证明。
- **研究原则：** 保留当前EMA reference+符号贡献处理+原更新器作为待解释的最小原型，先检验其中理论桥接是否成立，不将局部失败默认转化为新增频率、warmup、权重、阈值或评分层模块。诊断只观察同一算法的目标投影及实际位移/有限步loss，不构成新训练策略或调参方案。模型选择、优化器常规训练设置与额外贡献干预机制应区分；简洁性是用户的研究约束及方法优势，不表述为参数越少必然数学更优。
- **理论界限：** 固定r的线性box问题的符号解无需warmup/间歇调度；单靠它不能推出每两步Flip最优，也不能推出每步Flip的长期clean loss/acc最优。固定目标F、a=grad F、L-smooth时F(theta-eta S)<=F(theta)-eta a^T S+L eta^2||S||^2/2；投影增大未控制方向大小/曲率就不自动给出有限步下降排序，实际Adam还需分析其位移。r不等于a时，a^T(S-G)=Delta-(r-a)^T(S-G)，Delta=r^T(S-G)>=0，需研究参考误差与贡献增益的竞争，不以误翻clean样本率替代该检验。没有给定目标、参考误差、曲率及更新状态的模型，就没有理由声称固定隔一步具有普遍最优性。
- **收敛后的待办：** 首先明确所研究固定目标及现有贡献目标/实际更新关系，其次分析EMA在内生轨迹上是否满足所需方向质量，最后用固定完整state诊断区分reference、优化器几何和有限步近似失效。若某一环不成立，应修正理论适用范围或从明确目标推导必要的最小规则，而非继续经验叠加；如无稳定优势需如实报告失败边界。当前没有新的最优beta、无warmup成功定理或固定编辑频率最优定理。只追加文档、git diff --check验证，无新实验结果。

### 2026-11-01 / DPCO-0086：提供ImageNet100旧套件停止与50000步、LR6e-4、倒序beta重启命令

- **用户请求与范围：** 用户贴出此前ImageNet100 CLIP20% suite命令，要求先停当前训练，将每run预算197800缩至约50000步、提高LR，reference beta按.99/.95/.9倒序，重新启动。本轮只读启动器/配置/调度实现，提供服务器命令并本地dry-run、shell语法检查、追加记录；不修改程序/配置/依赖/数据，不连接服务器实际发信号或启动训练。用户请求不扩展为其他机制开发授权。
- **停止协议核实：** run_suite等待的train_classification子进程由start_new_session=True启动，仅停止外层nohup bash不能确保训练终止。命令查找用户所贴旧前缀最新日志及其.pid，验证PID格式和旧命令噪声目录/197800身份；递归先SIGSTOP父进程防继续派发、停止子树后SIGTERM及SIGCONT完成终止。另从同日志最后Started行提取训练PID/run_name，匹配真实命令后处理父套件已退出的孤儿训练。仅作用指定旧套件及记录中的当前run，不提供全局pkill python/删除数据/默认SIGKILL；最后列出相关进程便于核对已释放。服务器实际PID和日志路径未读取，选择最新匹配日志需与用户当前任务一致。
- **新统一配方：** 保持ImageNet100、ResNet50随机FP32、同一CLIP约20%固定manifest/noise seed0、训练seed42、batch128、Adam moments .9/.999/eps1e-8、L2=0。每run50000更新（按旧每epoch989步约50.56个遍历）、初始LR6e-4为3e-4两倍的短预算试验值，cosine在本run第50000步降至1e-6；每1000步评价、每5000步latest/checkpoints开启。普通Adam一次，然后.99Flip/Filter、.95Flip/Filter、.9Flip/Filter，共7组串行，每组50000合计350000更新，不是套件总计50000。不resume旧checkpoint，保留旧输出，新run自动新名字；无warmup或间隔编辑新机制。
- **推断与限制：** 旧cosine在20000/197800附近仍约2.925e-4，故仅凭loss4.5降到1.0后变慢不能归因为学习率过小，也不保证加倍LR提升acc/泛化。新预算同时改变LR与退火时长，因此是用户授权新pilot配方；新7组内部统一公平，不能将对旧终点差异全部归为beta。50k只是短预算机制测试，不是充分收敛保证。
- **验证与输出：** 以现有run_suite --dry-run实际解析7组，核对数据/model/manifest、seed/batch、50000、6e-4 cosine至1e-6、beta倒序/权重[-1,0]、无warmup/legacy probes/diagnostics、checkpoint及wait；停止块bash -n通过，未执行停止逻辑。新任务按nohup/stdin=/dev/null/stdout+stderr独立results/logs/imagenet100_clip20_50k_lr6e4_b099_b095_b09_s42_时间戳.log及.pid后台，子run仍写files/runs/logs统一目录，数据保持../data。git diff --check通过；未产生新训练结果，服务器设备释放需用户执行后检查。

### 2026-11-01 / DPCO-0087：精确分解EMA评分的历史/自身/交叉项，提出最小诊断保存方案

- **用户请求与边界：** 用户要求参照DTV self-term/LOO发现路径，先从数学公式逐项拆解beta、batch mean及clean/noise关系，再判断训练须保存的数据，明确先不猜结论。本轮只读当前HistoricalDPCO、记录/评价/数据/快照实现和既有数值，作研究推导及数值恒等式校验，追加本记录；不修改代码/配置/依赖、不新增训练机制或启动训练，也未授权实现后述诊断。此前简洁性原则继续有效，采样诊断频率不是新贡献干预频率。
- **有限步精确展开：** 记t从1开始、B为全局有效batch大小，g_ti是该run当前模型及同一实际batch上下文中观察标签loss梯度。alpha_t=(1-beta)/(1-beta^t)=1/(1+beta+...+beta^(t-1))，对t>1令r_prev=H_prev/(1-beta^(t-1))，有r_t=(1-alpha_t)r_prev+alpha_t G_t。t=1取r_prev=0、alpha=1。评分q_i=h_i+s_i+c_i，其中h=(1-alpha)r_prev^Tg_i，s=alpha||g_i||²/B>=0，c=alpha sum_(j!=i)g_j^Tg_i/B。第一步所有beta均r=G，自项系数1/B；beta趋1且t有限时alpha趋1/t，不可从开头就用1-beta近似。固定t/梯度时beta减小增加alpha及显式self系数，同时改变整个当前cross和历史权重；实际跨beta run的g/H还随轨迹变化，self大小、负align率和acc不随beta必然单调。
- **自保护可检验事件：** d_i=q_i-s_i=h_i+c_i，事件d_i<0且q_i>=0表示当前显式正self-term改变了负分数判断。该事件只识别自项对决定的影响，不能称应被删除或错误保留，不将clean/noise成员身份当贡献真值；需按两组报告比例、范数及score边际。self主导需比较s与h+c的抵消，不能从系数小认定作用小。历史含同一ID重复出现时还存在旧梯度与当前梯度的内积，可能正或负；当前自项剔除不移除历史重复样本或参数轨迹/BN间接依赖。
- **EMA中的两种LOO必须区分：** 仅扣当前自项得到q_sub=q-s=h+c。若按保留历史、当前改用其余B-1样本均值定义r_LOO=(1-alpha)r_prev+alpha(BG-g_i)/(B-1)，则q_LOO=h+B*c/(B-1)，B>1。存在历史时两者不是整体正比例，符号可不同；beta=0/首步h=0时才有传统DTV扣自项与LOO的符号等价。若写h+c+lambda*s，只是当前self衰减族，不可直接宣称lambda=0即上述规范化EMA-LOO或历史全轨迹LOO。该比较仅诊断候选评分，不改变当前训练，不套用单一共同r的贡献最优证明到每样本不同r而不重新说明目标。
- **clean/noise五项展开：** 在原始训练标签固定划分C/N，定义G_C=B^-1 sum_C g_i、G_N=B^-1 sum_N g_i（按原B，空组为0），G=G_C+G_N；在同一模型轨迹上用相同beta分别维护诊断H_C/H_N，则H=H_C+H_N、r=r_C+r_N。评分可写h_C+h_N+s+c_C+c_N，c_C=alpha G_C^Tg_i-s*1(i in C)，c_N=alpha G_N^Tg_i-s*1(i in N)，h_C=(1-alpha)r_prev,C^Tg_i、h_N同理。按原B缩放保留实际batch组占比，不把两组均值各乘一半；噪声组方向可以有益、clean组也可与某样本冲突，不依据来源直接判方向好坏。H_C仅供诊断且需额外参数维向量状态，不能从现有未分组H快照唯一恢复。
- **最小逐样本数据与计算成本：** 同一个实际训练batch记录step/batch_id/sample_id及有效B、beta、method、seed等身份，配只读固定标签/分组映射；核心仅需q_i=r^Tg_i、b_i=G^Tg_i、n_i=||g_i||²三个标量，即可离线恢复s=alpha*n/B、c=alpha*b-s、h=q-alpha*b、q_sub及q_LOO，不必保存完整每样本梯度。扩展组来源仅再加q_C=r_C^Tg_i和b_C=G_C^Tg_i两个标量，即能恢复全部五项。当前JVP流程可得到q但仅写总体，b可额外JVP；精确n不是现有aggregate范数可恢复，可能需逐样本VJP/其他经核实等价计算，不能宣称几乎零成本。优先在固定诊断batch/既有评价节点及初始少量步精确计算并保存标量，避免每步物化B×参数维Jacobian，也不把last-layer范数冒充全参数范数。BN下须用同一整batch函数的梯度，不能把图片逐张单独前向当作等价per-sample梯度。
- **连接贡献与预测的保存建议：** 同诊断batch保存观察/原标签普通CE、predicted_class及group供只读join；固定无增强eval节点另保留sample_id、predicted_class、ce_original/ce_observed，并保留现有全量clean/污染双标签acc/CE与test曲线，明确train_aug与eval_fixed视图及pre/post-update索引。组编辑数/率、self-shield率、规范LOO符号变更率、q/h/s/c分位数和group reference分量为派生统计，不作噪声检测正确率。第二阶段在固定完整state比较G、Filter、Flip实际Adam位移与固定目标梯度/有限步loss，属于不提交参数的诊断；不得根据单样本编辑标签或相关性直接声称长期accuracy因果改善。
- **可复现性、beta隔离与已有保存缺口：** 保留数据/噪声指纹、源码/config、batch顺序/augmentation RNG、模型/BN、Adam m/v、H/update_count及采样状态，分组H若启用也须保存。现有快照槽initial/p25/p50/p75/final/latest（best依评价策略）不等于每个latest都永久留存，unreferenced快照会清理，需要明确保留诊断节点的完整状态，不能假定1950间隔覆盖全部历史可离线恢复。现有CSV仅总负数、r/G/S范数、cosine和reference_gain及分组acc/CE，不能恢复逐样本三项，更不能验证self主导。跨beta训练轨迹不同；若要隔离beta本身，可在同一轨迹维护只读影子EMA或完整重放，额外内存/计算需披露，不作为第一轮必须增加的训练规则。当前根CIFAR目录仍为9目录8唯一配置，未见.96/.98，沿用0081终点关系但不由其断言self或历史过时为主因。
- **验证与未完成项：** 捆绑NumPy在B=2/4/128、beta=0/.9/.95/.96/.98/.99/.999、t=1/2/5/100共84随机向量case核对h+s+c、规范化LOO、扣self及Flip投影gain恒等式，最大绝对浮点误差1.57e-10；这是公式实现核验而非训练证据/数学证明。B128稳态self系数按.9/.95/.99/.999为7.8125e-4/3.90625e-4/7.8125e-5/7.8125e-6，未用其估计实际self主导比例。git diff --check通过，只追加本文件，无新实验数据；诊断接口/存储实现、性能开销和具体观测计划均待另行授权。

### 2026-11-01 / DPCO-0088：确认DTV自项是研究方法示例，DPCO分析不预设self-term或LOO为主线

- **用户明确纠正与范围：** 用户要求保留0087关于batch内样本自身梯度影响的分解与评估，但澄清DTV由公式发现self/cross再实验形成LOO只是研究路径示例，DPCO应通过整体公式发现不同影响，而非预设评估self-term。本轮仅修正研究定位并追加文档，不修改代码/配置/数据，不实施诊断或启动训练。
- **保留与调整：** 0087公式、数值核验及标量保存建议保留为可选分析分支；撤下self-term优先和LOO候选必需性的解读，不把三个标量记录直接定为最终诊断规格。用户未认定历史滞后、self保护、噪声组主导或Adam几何任何一项为真实主因，均需从明确推导与可区分实验建立证据。
- **后续方法：** 从r_beta到评分q、贡献决策w、聚合S、实际Adam位移u及固定评价目标的完整链条展开；可分别分析历史时间权重及旧参数差异、内积的方向/尺度来源、零阈值附近符号决策、被编辑梯度的合力及抵消、更新器几何和轨迹反馈。先写恒等式/必要假设，形成能解释现有beta-clean/noise关系的竞争假设，再确定最少可区分观测，最后由实验决定是否修订算法；不事先引入lambda、LOO、warmup或编辑频率，不要求所有候选观测一起上线。相同beta不同方法/不同beta均可能轨迹不同，不能把跨run相关性直接作单因素因果。
- **验证与未完成：** 本轮没有新数学定理或实验结论；仅追加本文件并git diff --check。尚未完成整体公式系统分解与诊断方案定稿，后续分析须按本澄清继续，保留原始记录及用户既有修改。

### 2026-11-01 / DPCO-0089：对照教授英文定位核查DPCO实现与现有实验证据

- **用户材料、任务与范围：** 用户直接提供教授关于data valuation/data intervention两缺口及Data–Parameter Co-Learning的英文定位，要求总结并结合现有实验核查代码是否偏离预期。本轮读取当前EMA方法、工厂/CLI、Trainer、Adam updater、分类任务/数据及历史周会总结，复核0081数值；仅分析并追加文档，不把所贴理论文字当作代码修改指令，不修改实现/配置/依赖或启动训练，保留既有修改。
- **教授主张提炼：** 传统聚合没有显式决定每个datum应如何贡献；valuation缺有益学习信号，intervention缺从价值到行动的原则。DPCO用学习过程产生的内生signal确定条件贡献优化，以同一问题同时给出valuation及desirable contribution，通过theta->signal->w->theta形成闭环。该英文段落是框架和动机，未唯一指定EMA、current inclusion、bias correction、beta、梯度空间/约束集或完整Adam最优性，不将本文自行选择的实例细节冒充教授唯一规定。self-influence术语有不同定义，不能把该概念段或现有batch-mean alignment一概等同单独||g_i||²。
- **实现映射与已核对事实：** HistoricalDPCO以本run当前参数的观察标签raw batch mean更新独立H、做bias correction得r，以q=r^Tg评分、按q<0给negative_weight、按原有效B聚合后送Adam；均stop_gradient冻结本步r/w，不对权重决策或EMA未来轨迹反传。下一步模型与raw gradient受此前贡献更新影响，构成真实闭环。没有独立普通Adam教师、clean验证梯度或原标签/mask进入贡献选择；分类batch只含图像、观察标签和valid mask。w每步闭式重算，无跨epoch永久样本权重，这可符合逐步条件贡献优化，不必额外建立可训练权重网络/持久w或bilevel微分。
- **同一贡献问题统一valuation/intervention的精确形式：** 给定theta/r/g，max_(w in C) B^-1 sum_i w_i q_i，q为未加权贡献评价，w*决定干预。C=[-1,1]^B时q<0取-1、q>=0取1即当前Flip；C=[0,1]^B时负取0即当前Filter，零点评分时+1是可选最优解。故两者均可为各自可行集下闭式优化实例，而非只能把Filter称heuristic或仅把Flip称optimization。对同一点同r，有r^T S_flip=sum|q|/B>=r^T S_filter=sum max(q,0)/B>=r^T G=sum q/B；不能转为不同轨迹最终loss/acc排序。优化目标/可行集仍是明确建模选择；接口允许任意有限负权重不意味着每个值都是上述问题的最优解，尤其范围外需另说明理论。
- **主要未完成桥接，而非确认代码bug：** (1) EMA提供endogenous信号，但尚未证明/实验证实它在CIFAR100N代表desirable learning；平均历史不自动补齐importance到有益贡献的缺口。(2) 给定r的贡献投影问题可精确求解，不能据此声称r/beta也最优，或原标签目标/全轨迹/accuracy最优。(3) 当前实际Adam变换S并更新m/v；如果理论定义优化贡献投影则实现吻合，若声称最优实际Adam一步则当前闭式解未覆盖该非线性带状态目标，需补理论而非擅自判为必须更改的代码错误。(4) raw而非edited梯度、current inclusion等是实例选择，教授该段未排除其他选择，不能凭段落判偏离。
- **实验对应与证据边界：** MNIST三seed固定终点Flip污染原标签97.7889/test98.1267对Adam75.5139/93.3533有正面结果，但clean CE .317491高于.173503且clean acc98.2139低于99.2611，未验证周会clean loss相对基线更低。CIFAR单seedFlip .9 clean99.9465/污染原标签.04975/test48.66；.99 clean33.9097/污染原标签17.1542/test26.10，仍无兼顾证据。两任务结果不能直接证明历史EMA机制或统一框架普遍优势；当前上传配方缺beta0同配方控制以隔离历史增量、逐样本贡献/固定目标/真实位移诊断，不能将噪声识别率当主要目标，也不预设self为主因。reference_gain>=0由构造保证，只能作实现一致性检查，不是信号有益或实际loss更优的证据。
- **结论与验证：** 结构上符合学习产生signal、贡献优化、参数反馈闭环；现有实现应称EMA signal+线性贡献目标+标准Adam的一个具体实例，未发现与该英文定位明确冲突的主要路径错误，但两缺口中贡献到干预的条件优化已具体化，signal到desirable learning及实际更新收益仍需研究证明。只读源码行号和既有JSON核对、git diff --check通过；无新实验/文献主张，不实现任何新参数、warmup、频率或LOO。后续先明确框架对应的数学目标和条件，再按整体公式分解决定最小诊断。

### 2026-11-01 / DPCO-0090：按六节点展开公式/源码并排序CIFAR100N机制突破点

- **用户任务、材料与授权边界：** 用户引用0088的r(beta)->q->w->S->Adam位移->目标表现链条，要求逐节点数学与训练代码对应并分析可能突破点。本轮重读EMA方法、全局mesh、分类任务、CIFAR模型/BN适配、CLI、Adam、训练记录和分组评价；复核0081派生曲线，只追加理论/分析记录，不改代码/配置/依赖或数据，不实现诊断或启动训练，不调用外部论文替代本地代码证据。DTV self项仍为备选分支，不预设结论或新增机制。
- **节点1：** r_t=sum_s omega_ts G_s，omega=(1-beta)beta^(t-s)/(1-beta^t)，G_s来自本run theta_s及当时训练batch；同一目标在当时状态的诊断梯度记a_s，则恒等式r_t-a_t=sum omega(G_s-a_s)+sum omega(a_s-a_t)，区分当时信号与目标差异及目标方向随参数/状态演化的漂移，不假定误差独立/零均值。代码先raw VJP、EMA、bias correction，r被冻结；修正分母为正，不改变固定H下选择符号，因此单纯r范数缩放/bias correction不是实质决策机制。beta既影响时间权重又影响后续轨迹，不能跨run直接归因；第一步所有beta同r=G。
- **节点2：** q_i=r^Tg_i=||r||||g_i||cos(angle)，也等于sum_l r_l^T g_i,l及历史pairwise内积的加权和。代码jvp(losses_fn,params,reference)精确得到全参数同batch评分，与audit Jacobian定义一致；全局B不是每芯片B。固定r时单独正缩放g_i不改变自身评分符号，但norm可改变其进入reference和聚合的影响；全参数层项可相互抵消。单纯将同一q除以正范数转cosine不改变w，不能作为新的修复方法。self/cross为另一种合法展开，不宣称其主要性。
- **节点3：** z_i=1(q_i<0)，w_i=1+(a_neg-1)z_i，q=0保留1；Flip a_neg=-1、Filter0。max_(w in [-1,1]^B)sum wq/B的闭式解为Flip，非负盒约束为Filter。固定g比较r/r'，符号改变必满足|r^Tg_i|<=|(r'-r)^Tg_i|，故接近零的评分可能把平滑参考变化放大为离散决策变化；这是可能性不是当前日志已观察的margin分布。每步stop_gradient r/w为条件贡献优化，不对选择未来轨迹反传。当前精确闭式求解本身不是优先怀疑环节。
- **节点4：** P=B^-1 sum_(q>=0)g、N=B^-1 sum_(q<0)g，G=P+N，Filter=P，Flip=P-N，修正C_filter=-N/C_flip=-2N。r^T C_flip=2sum_neg|q|/B>=0；||S_flip||²-||G||²=-4P^TN可正可负，不从“修正两倍”推断总norm必变大。令v=r/||r||，C=(v^TC)v+C_perp，投影优化只控制平行收益，不限制正交变化。给定目标a，a^TC=Delta-(r-a)^TC；对同点二次目标，真实plain一步差=-eta a^TC+eta²(S^THS-G^THG)/2，局部一般光滑目标需Taylor余项，不把近似冒充精确比较。全向量符号编辑如何改变有用/无用合力与正交部分，是从数学结构直接得到的新候选突破点，非建议新增梯度投影/裁剪模块。
- **节点5：** 当前L2=0时m_t=beta1 m_prev+(1-beta1)S_t，v_t=beta2 v_prev+(1-beta2)S_t²，u_t=eta mhat/(sqrt(vhat)+eps)，theta_next=theta-u。EMA的线性性给m=EMA_beta1(G)+EMA_beta1(C)；当beta_ref=beta1且都零初始化，有mhat=r+hatEMA_beta1(C)。v=EMA_beta2(G²)+2EMA_beta2(G*C)+EMA_beta2(C²)逐坐标精确成立，中间交叉项可负、总v非负。故raw reference与编辑后Adam矩为不同历史；beta_ref .9/.99/.999与固定beta1 .9的时间尺度关系也是可检查因素，不预先判错。实际局部目标由a^Tu而非a^TS决定，固定历史m并冻结预条件P的代理评分为g_i^T P^T a，真实v仍随w变化、不能把代理说成完整Adam最优解。源码用标准Optax scale_by_adam，未发现多除B或误将per-sample square mean当v等代码路径错误。
- **节点6：** 固定分组目标F_C、F_N_original、F_N_observed及原标签top1需分别定义，argmax accuracy与CE不同；第一阶损失变化由-a^Tu决定，非r投影值。代码train_ce/train_top1是更新前增强train-mode下观察标签普通指标，不是加权贡献目标；group_evaluation为更新后固定无增强eval-mode分组。CIFAR BN使真实学习状态还含running buffers z_t，z_next由当前整batch forward生成，不受该步w直接筛除；Filter不是从BN前移除图片。同state同batch一步候选需固定同起点BN并一致处理next buffers，跨步则影响反馈；此为次级待检机制，不建议擅自改BN。raw/EMA/Adam/BN均进入完整状态，观察目标需明确pre/post步及视图。
- **CIFAR证据及排序：** 既有JSON复核Flip .99在1950/7800步clean4.398/5.8395%，对Flip .9为11.4314/36.8595，说明大beta训练受阻早已存在，不能仅用晚期错标记忆解释；.9在20670步clean81.535/污染原类29.726，到40560为99.017/1.045，最后99.946/.04975，体现另一种后期变化。Flip .99全程r/G cosine均值.14463，对.9 .40291，但不是oracle方向质量证明；同beta .99 Filter终点clean99.997对Flip33.910支持优先检查干预到真实更新的连接，不能因轨迹不同作单因素因果。优先级为：reference是否对齐目标及时间漂移、贡献投影到实际Adam位移的传递（含两套矩历史）、被编辑合力/正交变化；其次阈值margin及层间抵消，BN/评价语义作必要排查；self仅为候选，w闭式代数本身低优先。排序依解释力和可辨识性，不是已证原因或概率估计。
- **最小分层观测与可检验决策树：** 第一层同完整checkpoint比较普通/Filter/Flip的r^TC、a_K^TC、a_K^T(u_edit-u_base)、固定目标实际一步loss差，保留参数/BN/Adam/H、原batch和增强身份；不提交反事实模型，也不用原标签决定训练。若reference投影好但目标投影差，查节点1/2；目标投影好但实际位移差，查节点5；位移投影好但有限步loss差，查曲率/步长及状态一致性；局部好长期差，再查反馈/阶段。第二层按结果选q与margin、层项、历史年龄项或合力/正交量等，不一次保存全部或先实现LOO。现有csv总量不足以区分，完整逐样本梯度不作为默认保存方案；影子beta须同轨迹才隔离beta自身，成本另核。以上诊断实现仍未授权。
- **本地数学核验与限制：** 捆绑NumPy100随机向量case检查投影gain、P/N范数恒等式、正交投影及目标误差迁移；另100递推步检查m/v分解，最大绝对误差1.78e-15。该检查不构成模型实验因果证据或收敛证明。git diff --check通过，只追加本文件；没有新增最优beta、调度、正交投影训练算法或新超参，也未声称CIFAR失败源于40.2%比例。后续需在明确目标下设计最少诊断再请求相应实现授权。

### 2026-11-01 / DPCO-0091：读取CIFAR100N新增.96/.98终点并核算逐步贡献编辑比例

- **用户任务及范围：** 用户称将reference beta .96/.98结果放入results/cigar100n/files，要求结合旧结果比较，并统计每步Flip/Filter比例评估侵入强度。实际定位为根results/CIFAR100N/files；采用Spreadsheets只读科研分析，读取CSV、不改源数据、训练/绘图代码、配置或依赖，不运行训练，不导出工作簿/slide或新图。派生核算保存于DPCO/results/files/cifar100n_beta096_098_intervention_20261101，追加本记录。
- **输入及完整性：** 13个run目录包含重复的Flip .99，去重为12配置（Adam1、Flip6、Filter5），均seed42，summary completed/78000，group/evaluation均201节点步距390、clean29900/noise20100/test10000；可见train B128、初始LR3e-4、命名ResNet34/noisy100/human/cosine与原配方一致，但新四组无metadata，完整源码/环境/数据指纹不能认证。初检时新train/dpco CSV内容持续增长，不能将本地截断归因为训练失败。对每份文件捕获一次bytes和SHA，截掉未完成尾行，不修复或补行。最终快照64输入，捕获后复核64哈希均一致；此前观察到增长的事实与尚未齐全的记录仍保留，不能把捕获后短时稳定说成完整上传。
- **新增终点（acc为%）：** Flip .96 clean88.207358、污染错标签52.646766、污染原标签18.378109、全原标签60.136、test46.05、clean CE1.650888；clean全程最高88.444816。Flip .98为51.725753/13.199005/24.995025/40.98/38.40、clean CE2.177741，全程clean最高51.839465。Filter .96为100/99.955224/.0199005/59.808/51.05，Filter .98为99.993311/99.945274/.0348259/59.810/51.86，clean CE分别.000351/.000426。Flip .96比Adam多正确3690张污染原类、少正确3526张clean，净164张，全原标签+.328pp但test−5.19pp；.98污染原类25%是当前最高仍伴随clean约52%，未达联合目标。Filter .98 test比Adam+.62pp、比.95+.09pp，单seed不称稳定提升；污染原类仅7张对Adam4张，仍几乎完全记忆错误标签。
- **比例定义与验证：** p_t=edited_count/valid_batch_size，逐步数量比例；各run实际negative_weight为Flip−1/Filter0、edited_count=negative_count、B128、0<=count<=128、reference_updates=step且有效记录从1连续无重复。均值以sum edited/sum B计算，与B恒定时逐步均值相同；不是唯一图片比例、noise检测率或实际梯度/参数位移改变比例。Flip/Filter相同p时平均系数改变量mean|w−1|分别2p/p；真实梯度改变量为−2N/−N取决于合力，现有范数和cosine不足恢复||S−G||或实际Adam扰动。
- **可完整比较的共同前7800步（20遍历）比例：** Flip按beta .9/.95/.96/.98/.99/.999为25.7379/32.0687/34.2727/37.7878/39.5987/39.7906%；Filter按.9/.95/.96/.98/.99为23.6668/29.0736/30.9360/34.5901/36.8635%。新.96/.98 Flip约每128样本44/48个、Filter40/44个，非稀疏干预。此早期窗口随beta增大编辑率增加只是本套轨迹观察，不推为普遍单调性质。
- **全程旧组及新前缀：** 旧Flip .9/.95/.99/.999完整78000步均值33.3293/28.6940/40.3385/43.8353%，末7800步43.4552/30.2680/40.1646/44.7586%；旧Filter .9/.95/.99完整均值38.4509/40.5422/44.1561%，末段44.7749/45.5669/46.6376%。新组完整有效dpco快照为.96Flip前73430步29.0826%、.96Filter前64846步40.3538%、.98Flip前14767步37.8442%、.98Filter前14951步33.3451%；这些是不同区间前缀均值，不标作全程或完整末段，勿与旧全程直接横排判断beta作用。全程Flip .95编辑率低于.9但test更低，数量强度不能独立解释结果；Filter后期近45–47%仍记住错标签，不能把高编辑率当抗噪成功。
- **派生输出和验证：** comparison.csv为12配置终点/覆盖/干预统计，run_summary.csv保留13目录及duplicate_of，intervention_phases.csv分阶段覆盖与比例，intervention_count_snapshot.npz保留本次实际分析的step/edited_count数组以应对源文件后续增长，analysis.json列201点分组轨迹/源SHA/缺失说明，analysis_report.md为可读解释，verification.json为64输入复核与去重状态。group top1×计数均还原整数，summary与末次evaluation对齐，全部评价节点连续完整；源CSV只读，未恢复逐样本清噪成员的编辑率。git diff --check通过；后续若同步齐全，应重算新四组全程和末段比例，不覆盖本次分析快照。

### 2026-11-01 / DPCO-0092：核对近期过滤数量口径，推导保持投影收益的最小梯度干预候选

- **用户请求与范围：** 用户确认.96/.98日志未下载完整、后续再补，本轮只讨论40–50%干预是否高于顶会常规，以及能否无新增调参地自动控制。读取协议及最近记录，检索近期主会原始论文，作条件优化推导和NumPy恒等式核验；只追加本记录，不改代码/配置/依赖、不下载实验数据/模型、不启动训练。不再尝试将本地不完整逐步日志视为完整；用户确认作为0091完整性说明的直接依据。
- **论文核对与比较界限：** NeurIPS2025 Early Cutting官方论文 https://proceedings.neurips.cc/paper_files/paper/2025/file/3e826f682178d9830a3b704141b4989e-Paper-Conference.pdf 第6页Table1明确比较使用60%原有noisy训练样本的选择方法（余下约40%未进入所选训练集合）；其额外切割在已选子集进行，不等于每batch40%整向量flip。AAAI2025 Confidence Tracking作者正文 https://arxiv.org/html/2504.17474v1 附录F所复现Co-teaching的R(T)=1-min(T/Twarmup*epsilon,epsilon)，稳态不选比例为epsilon，40%噪声先验时可40%；这是该论文baseline设置，不能写成CT自身固定过滤40%。同附录GMM阈值从.5/.7/.9/.95/.99按validation选，DIST也调momentum；EarlyCutting第5/6页用loss top10%、confidence top20%、输入梯度norm bottom20%及cutting1.5，参数在validation确定，不是无参数方法。ICCV2025 JAL https://arxiv.org/html/2507.17692v1 式8/9为鲁棒loss而非二元过滤，其alpha/beta/a有数据集设置；本轮未把更换loss的覆盖率与flip数量直接比较。CVPR2026 DSS官方摘要也仅支持按类别/实例去偏的selector模块，不提供统一侵入安全线。没有查到可将40–50%判为超过顶会公认阈值的标准，不能虚构常规10/20%。
- **数量与幅度：** 当前每步样本数比例p是数量维度，Filter全向量改变量为||g_i||、Flip为2||g_i||（对被选样本），数量上大范围、单样本Flip改动大，但不单凭p判定实际梯度合力或Adam位移过强。严格原问题max_(w in [-1,1]^B)sum_i w_i q_i在非零q时唯一符号端点；若保持同信号、同可行集和精确最优目标，不能额外要求自动减小负贡献幅度/数量而还保持全部最优性。缩减样本比例需要预算/置信假设或改变优化目标，固定cap20%/设权重-.5并非由现有理论推出。
- **本轮条件推导（非文献性能结论/非新颖性主张）：** 令q=r^Tg、r!=0，原Flip给目标投影|q|。允许贡献向量不必平行于原g后，考虑min_d .5||d-g||² subject to r^T d>=|r^Tg|，正q原g已可行，负q最小范数修正由Cauchy-Schwarz/半空间投影唯一取平行r方向。闭式d=g-2min(q,0)r/||r||²：只反射沿r分量，保留正交分量，r^Td=|q|与原全Flip同值，且||d-g||=2||g||||cos(r,g)||<=2||g||；cos=-.05时改变量.1||g||，原全flip为2||g||。这里2由目标从q变成-q决定，不是新调参。r=0时所有q=0，定义不编辑，无需引入数学epsilon超参。
- **Filter对应与聚合最小性：** 若约束换为r^Td>=max(q,0)，得d=g-min(q,0)r/||r||²，保留原Filter的参考投影，移除负向平行分量而非整梯度归零；与投影类gradient surgery相关。对每个batch，同r下定义原全Flip/Filter聚合S_old、G原均值、Delta=r^T(S_old-G)>=0，则上述候选聚合S_new=G+Delta*r/||r||²，C_new=Proj_r C_old，故||S_new-G||<=||S_old-G||，且r^TS_new=r^TS_old。这也是min_S .5||S-G||² subject r^TS>=r^TS_old的唯一解。它在指定欧氏梯度距离和投影约束下最小，并非最优clean acc/Adam位移定理；无需保存全样本梯度矩阵来计算该聚合，因为G、r、负q之和已可得，具体数值开销/性能尚未实测。
- **重要边界与研究定位：** 此候选仍处理所有q<0的样本，数量p不会因此变小；自动变小的是每样本及聚合的欧氏梯度改动，特别是弱负align。它将贡献空间从scalar w*g扩展为vector d，是明确理论模型改变，不是原scalar DPCO闭式解换个实现，也不是已获授权要并入代码的模块。没有纠正reference自身错误，不保证clean/noise性能、实际Adam位移变化更小或持续训练更好。原始投影方法PCGrad（NeurIPS2020）https://proceedings.neurips.cc/paper_files/paper/2020/hash/3fe78a8acf5fda99de95303940a2420c-Abstract.html 已有相关gradient surgery先例；其多任务投影不是本项目EMA反射的现成实验验证，须后续系统查重，不能宣称新算法或近期通用标准。保持投影的反射为本轮针对现有目标的推导；提出候选不等于认定当前失败因高侵入或该法应取代Flip。
- **验证与待办：** NumPy1000随机batch、投影/反射两个版本共2000case核对逐样本投影相等、改变量不增、聚合变化为原变化在r的正交投影，及反射保范数；最大浮点恒等误差7.11e-15量级，另cos=-.05二维例精确比较。只是代数检查，不是训练/收敛/新颖性证据。git diff --check通过；当前仍需实际记录原算法梯度改变量/评分边际与真实更新诊断，确认有无必要改变贡献空间。未添加固定侵入上限、warmup、编辑频率或新的alpha/lambda。

### 2026-11-01 / DPCO-0093：纠正20%启动参数语义，提供独立受控人噪缓存准备及六组训练命令

- **用户请求和范围：** 用户要求CIFAR100N20%噪声、reference beta .95/.96/.98、其余与40.2%实验一致的Flip/Filter启动命令，并贴出直接noise-percent20的写法。本轮只读接口、研究数据构造、验证既有缓存API和给服务器命令；不修改程序/配置/依赖，不连接服务器执行数据生成或正式训练。按请求提供一次性离线数据准备命令，不创建新的项目脚本文件；原40.2%缓存/结果保留。
- **关键纠正与可复用接口：** noise_percent只校验加载率，官方human固定20100/50000=40.2%，原data目录改20会在加载时失败，--no-is-human也不是定额20生成器，noise_manifest当前仅ImageNet。进一步核对发现现有cifar100n_prepare.publish_arrays明确支持发布自带provenance/哈希的独立缓存，verify_prepared和CIFAR100NImages接受该自洽格式，因此可以用一次性数据准备命令复用它，而无需修改训练加载器或伪改官方manifest。这与覆盖原官方标签或跳过校验不同；新缓存必须明确标为controlled_human_error_retention，不能称官方20%发布版。
- **数据协议与路径：** 原data/cifar100n只读，核对50000训练及20100原人错标。用numpy.default_rng(0)从这些错标ID均匀无放回选择10000个，保留其原人类错误标签，其余10100恢复基准原标签；不删除图片、不随机产生新错误目标，global20%并非每类固定20%。新独立缓存data/cifar100n_human20_s0/prepared使用同一50k/10k图片和原始标签，标签对/manifest留存；provenance含变体、source manifest SHA/路径/版本、selection seed/RNG/NumPy版本、保留ID摘要、原错标/保留/恢复数量。已存在完整缓存只在身份/标签/图像哈希匹配时复用；未完成目录有其他文件则退出，不覆盖数据。不把自定义变体伪称官方原始标签文件。
- **命令与实验身份：** 单一nohup bash先执行内嵌离线准备，再按.95Flip/.95Filter/.96Flip/.96Filter/.98Flip/.98Filter串行6组。固定ResNet34随机FP32、train seed42、B128、78000步、Adam3e-4 cosine至1e-6、moments .9/.999/eps1e-8、L2=0、评价390/latest1950/checkpoints、无legacy probes/diagnostics/warmup。显式data-dir指向新缓存，此时noise-percent20为正确断言。套件名human20与新数据目录区分，stdout/stderr独立results/logs/cifar100n_human20_b095_b096_b098_s42_时间戳.log、stdin/dev/null、后台&、PID/.pid和tail；单run仍在既有files/runs/logs。可选注释命令补同20%Adam基线，不默认额外启动；旧40.2%Adam不能作20%的同任务对照。
- **评价与元信息边界：** 现有分组会按新标签是否匹配原标签划分，所以20%版本clean40000、corrupted10000，与40.2%的clean29900不是同一集合；跨噪声率比较clean指标需披露此变化，原29900clean/恢复10100可由保留的源标签与新标签重建作共同组分析，当前未增加分组代码。现有run_name不含CIFAR噪声百分比，需一并保留logs/<run>/metadata.json的实际率、数据路径和指纹，不能仅凭human后缀辨20/40.2。
- **验证与未完成：** 本地10训练/2测试fixture使用真实publish_arrays和CIFAR100NImages，确认原40%缓存拒绝20断言、独立派生20%正常加载、clean8/noise2、缓存复用/标签与图像哈希及源缓存保持一致；只测既有API，不训练模型。六组按最终参数实际run_suite --dry-run核对beta顺序、负权重[-1,0]、20断言/新路径、78000/B128/3e-4及wait/无warmup；完整shell与nohup内层bash -n和内嵌Python compile通过。git diff --check通过。服务器实际50k构造尚未执行或验证，无新训练结果；缓存图片会另存一份以保持独立不可变身份，需现有数据可访问及少量额外磁盘。


### 2026-11-01 / DPCO-0094：固化可复现的固定比例人噪准备入口，区分生成参数与训练校验

- **用户授权与目的：** 用户明确要求把上一轮准备20%数据的临时代码固化为py文件，并询问之前为何没有参数。本轮据此授权实现受控人噪缓存准备及其验证/文档；不改变DPCO/Adam算法、模型、训练调度或训练端百分比语义，不启动服务器数据准备或正式训练，不覆盖现有数据。先前接入只实现官方完整标签及实际率断言，没有实现可调比例的派生数据构造；官方40.2%固定不代表不能另定义并明确标识受控版本。
- **涉及文件与接口：** 新增src/data/cifar100n_controlled.py；扩展scripts/prepare_cifar100n.py的--stage controlled，新增--source-dir、--target-noise-percent、--selection-seed（默认0）。controlled必须显式给独立output-dir及target百分比；这些生成参数在其他stage拒绝而非静默忽略。原plan/download/verify默认路径和含义保留。补充docs/cifar100n.md的协议、nohup准备命令、训练路径和比例口径，新增tests/test_cifar100n_controlled.py；追加本记录。保留原有DPCO_dev.md修改及docs/imagenet_clip_noise.md修改，后者本轮未编辑；不增加依赖。
- **固定数据协议：** 读取并验证原缓存的manifest、全部数据SHA、图片形状、标签及实测错标统计；从source中clean_label!=noise_label的ID全局均匀无放回选K=floor(N*p/100+0.5)，显式Generator(PCG64(seed))保持与上一轮default_rng(0)配方一致。保留选中ID的原人类错标签，其余恢复原标签，全量图片、原标签及test不变。目标率不得高于源实际率，支持0/全源率，不从受控派生集再次抽样；拒绝无效比例/seed及源目标相同/嵌套路径。官方50k的20%精确10000错标、恢复10100，其clean/corrupted为40000/10000；并非每类20%，不是新增随机目标，不是官方20%发布版。非整数目标数按上述规则取整，训练断言应使用manifest报告的actual率。
- **不可变性和复用：** 复用既有publish_arrays/preparation_lock格式，独立复制图片和labels.npz中的clean/noise/test标签；provenance记录variant、source路径/manifest SHA/版本、requested率、选择seed/RNG/NumPy版本、retained ID SHA及原/保留/恢复数量、取整规则/全局选择口径。已有缓存只在source/rate/seed/selection身份、图片哈希、标签内容和实测统计都匹配时复用；兼容0093一次性代码的旧provenance，不为加字段重写它。冲突、损坏、未完成目标目录退出保留；同seed跨独立输出得到相同选择，保存固定产物及摘要防止RNG环境差异被静默接受。原人类完整标签仍由源缓存保留并由source SHA连接，目标缓存保留训练需要的原/观察标签；官方完整数据预计额外约184MB像素空间。
- **训练衔接与边界：** 训练端--noise-percent仍为actual率断言，不是生成器；对新data/cifar100n_human20_s0显式--noise-type noisy100 --is-human --noise-percent20 --no-download即可直接复用现有加载/clean与corrupted双标签评价，无需修改训练流。selection seed与训练seed42独立，所有方法/beta共用同一缓存。跨40.2与20%的clean组成员不同，需披露，不直接把其clean指标当共同集合比较；应配同20%的Adam基线。run_name暂未加百分比字段，保留套件日志及每run metadata实际率/路径/manifest身份，不扩展本次授权去改命名规则。
- **验证结果：** 9项unittest全部通过，覆盖精确错标数和人类错误目标保留、原/测试标签和图片哈希、源数据不变、独立缓存同seed复现与换seed、重复复用及参数冲突拒绝、0/源率/半向上取整、非法参数/嵌套路径/派生来源拒绝、未完成/损坏目标保留、兼容旧临时代码产物及自洽哈希但错误标签内容拒绝、CLI生成/verify及必填/错误stage限制。通过现有CIFAR100NImages实际加载派生20%并核对clean8/noise2的10样本fixture，原40%fixture依然拒绝20断言；不以fixture冒充真实官方数据验证。另以阻断JAX/Torch/TF/Flax/Optax导入的独立进程完成controlled CLI；旧plan打印正常；3个Python文件AST、文档bash块bash -n、git diff --check通过。现有run_suite实际dry-run核对beta .95的Flip/Filter、独立20%数据路径/断言、78000步/B128/Adam3e-4 cosine至1e-6及原评价/保存参数，无warmup/新增训练规则。
- **未完成及证据限制：** 未读取或生成服务器真实50k新缓存，未训练模型；完整JAX训练集成本轮未重跑（可用本地测试解释器无JAX），本次仅纯数据准备和现有读入接口验证。服务器运行准备命令后需以controlled_human_ready和manifest的10000/50000、20.0确认，再使用原六组训练参数启动。数据构造是受控实验协议，不是降低噪声即可改善DPCO或证明Flip优势的理论/实验结论。


### 2026-11-02 / DPCO-0095：核对ImageNet100 50k套件运行耗时来源与评价/训练口径

- **用户请求及范围：** 用户贴出ImageNet100 CLIP20%、ResNet50、Adam6e-4、每run50000步、eval1000、latest25000、beta倒序.99/.95/.9的启动命令，询问为何运行更慢。本轮只读配置/数据加载/梯度/实验循环/评价/保存实现，提供条件性诊断及追加本记录；不修改代码/配置/依赖，不连接服务器，不停止或启动训练。保留已有全部未提交工作。
- **可确定的命令开销：** 此套件为Adam1组+3beta各Flip/Filter共7组串行，每组50000、总350000更新；wait控制等待，不让7组同时争用设备。lr增大不直接减少每步算量，beta仍为定长EMA递推，不因.99比.9而保存/重算更多历史batch。no-theorem-probes/no-diagnostics并不关闭正常全量分组评价。CLIP只用于事先固定标签生成；训练读取manifest/标签和身份验证，不在每batch运行ViT-L/14。
- **评价路径核对：** train_classification对noise_manifest选择noisy_classification_evaluation(include_all_original=True,select_best=True)，每节点先clean validation，再clean训练组、corrupted按观察标签、corrupted按原标签三次分组遍历。当前两个corrupted视图分别SQL取图/解码/transform/前向，没有复用同一logits；all_original只加权已有组指标，不额外前向。设N训练数、V验证数，20%噪声每评价约处理V+0.8N+0.2N+0.2N=V+1.2N张视图。50000步/eval1000加step0共51轮；原197800/eval4945加step0为41轮。单位步数评价频率约4.945倍，总预算缩短但每run评价轮数反而增加，不由此断言具体耗时倍率。训练约每989步遍历一次的原数据规模下，目前几乎每个训练遍历再跑上述全量评价，可能形成明显停顿，尤其初始化先评价再做compile_warmup。
- **与CIFAR比较的计算/输入区别：** ImageNet预设224输入/ResNet50 FP32，CIFAR既有32输入/native ResNet34；输入像素比49不是端到端耗时49倍（两者stem/stage结构、CPU/GPU/TPU执行不同）。ImageNet训练当前逐样本sqlite查询压缩bytes、PIL解码RGB、random resized crop/resize/flip，Python串行构造batch，无异步worker/prefetch；CIFAR准备缓存为解码uint8数组、32像素crop/flip。由代码可定位CPU/I/O潜在瓶颈，不能在无当前timing/设备利用率下断言其占主导。DPCO jvp路径比普通Adam多raw VJP、评分JVP、编辑方向VJP，放大大模型成本，但同路径不同beta并无历史长度级复杂度差异。
- **保存及如何分辨：** latest25000不等于全程只存两次，initial/p25/p50/p75/final固定节点以及ImageNet验证提升的best也可保存；需以timing的checkpoint累计为准。timing.csv内train_window的duration_s/window_steps给训练窗口平均步耗时（包含输入准备/等待和窗口同步，不是纯TPU kernel），evaluation累计给全量评价开销，compile_warmup表示训练编译及候选执行而不等于全部评价编译，checkpoint单列保存时间。若仅总墙钟慢而train_window稳定，优先查看evaluation/checkpoint；若训练窗口也慢，继续分辨输入/模型/硬件/并发。当前未收到该新run timing/服务器运行状态，无法给出实测归因或倍率，不借用旧CIFAR日志冒充ImageNet测量。
- **建议边界与验证：** 若实测评价占大头，后续可仅将eval-every-steps从1000改为5000，50000步变为含step0共11轮；这是减少观测频率，DPCO更新公式不变，但曲线采样及best checkpoint选择更稀疏。本轮未更改/执行命令。源码只读核对计数和路径，git diff --check通过；未新增性能测试或研究性能结论，待该run timing/metadata及硬件信息确认具体瓶颈。
