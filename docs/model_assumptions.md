# Model Assumptions

## Agent Types
系统内置六类公众画像：
- 技术乐观型
- 风险敏感型
- 制度信任型
- 权益保护型
- 功利效率型
- 中立观望型

这些画像通过初始态度、制度信任、风险敏感度、收益敏感度、从众倾向、开放性和表达强度进行区分。

## Attitude Score
`attitude` 取值范围为 `[-1, 1]`：
- `-1` 表示非常反对
- `0` 表示中性或态度不明确
- `1` 表示非常支持

## Stance Labels
- `attitude > 0.2`：支持
- `attitude < -0.2`：反对
- 其余：中立

## Scenario Parameters
每个政策场景使用以下参数描述：
- `policy_valence`：议题在初始讨论中的总体正负方向
- `risk_level`：议题触发风险感知的强度
- `benefit_level`：议题带来的潜在收益强度
- `trust_relevance`：制度信任在该议题中的重要程度

## Intervention Parameters
每类信息干预使用以下参数描述：
- `trust_shift`：对制度信任的影响方向和强度
- `risk_shift`：对风险感知的影响方向和强度
- `benefit_shift`：对收益感知的影响方向和强度
- `social_temperature`：对群体互动活跃程度的影响

## Social Influence
每轮模拟中，Agent 会从邻域样本中感知周围平均态度，并结合自身从众倾向与画像差异进行有限调整。更新机制包含阻尼和单轮变化上限，用于避免所有个体迅速收敛到极端位置。

## Limitations
该模型是解释性模拟，而不是预测模型。它用于帮助观察异质性公众在政策议题和信息干预下的态度变化方向，不代表真实人口结构、真实社交网络或真实舆情传播过程。

