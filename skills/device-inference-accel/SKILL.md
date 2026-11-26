---
name: device-inference-accel
description: 在端侧设备上建立可复现基线、定位瓶颈、按代价排序并验证 LLM/AIGC 推理优化。Use when accelerating or profiling on-device LLM/AIGC inference, including quantization, fusion, KV cache, delegate, scheduling, roofline modeling, flash offloading, long-context prefill, and speculative decoding.
---

# 端侧 LLM/AIGC 推理加速

## 边界

- 以可复现证据为准，不把单次运行或估算当成收益。区分实测、模型推算与假设。
- Kirin 的 omg/opc/ccec 构建与导出必须在容器内运行，禁止宿主机直跑。
- 不虚构设备收益；拿不到真机时交付有边界的估算与复现计划。

## 工作流

1. **界定问题与指标**：模型、batch、序列长度、dtype、设备与后端；目标指标（TTFT、TPOT、吞吐、峰值内存）和达标阈值。
2. **建立可复现基线**：同输入、固定种子、预热、多次运行报分布；用 `scripts/bench.py` 记录，保存配置与命令。
3. **剖析定位 bound**：先判算力、带宽、调度还是格式转换受限，再看算子分解；用 `scripts/roofline.py` 给理论下界，解释与实测的差距。
4. **建模与候选排序**：读[技术卡](references/techniques.md)；每项给出预期收益、实现成本、精度风险和验证方式，按 ROI 排序，不做无依据的框架化。
5. **单变量实现与验证**：一次改一个变量；精度对齐用 cosine/KL/top-1/perplexity（按任务选，写明容差与参考）；性能对比同基线，退化即回退。
6. **归档**：配置、命令、原始结果、结论边界与未验证项，放入相邻 evidence 目录。

## 完成标准

- 基线可复现，每个优化有精度与性能双证据。
- 结论边界明确，未验证项已列出。
