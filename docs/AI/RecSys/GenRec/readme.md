# 生成式推荐

Ideas

- [x] T5 是 Encoder - Decoder 架构，为什么不使用 Decoder-Only 架构

- 有部分研究尝试过，效果不佳

学习大模型

- [x] 要特别学习一下 [transformer 架构](https://www.bilibili.com/video/BV1XH4y1T76e)

- [x] [_The Illustrated Transformer_](https://www.yuque.com/zhangqiang-studyisalifestyle/it-technology/transformer-the-illustrated-transformer)
- [x] [Input Embedding](https://zhuanlan.zhihu.com/p/372279569)
- [x] [注意力机制](https://zh.d2l.ai/chapter_attention-mechanisms/index.html)

- [LLM base](https://www.yuque.com/darstib/learning/ggwdt1asf91dsseh "LLM base")
- [AI 算法工程师手册 - Graph 算法、Ctr 算法以及推荐算法](https://www.huaxiaozhuan.com/applications.html)

综述阅读

- [x] [[笔记] 从 Tokenization 视角看生成式推荐（GR）近几年的发展（2025）](https://arthurchiao.art/blog/large-generative-recommendation-tokenization-perspective-notes-zh/)
- [x] [From matching to generating：生成式推荐综述](https://zhuanlan.zhihu.com/p/1909282144087441641)
- [x] [生成式推荐系统深度综述：分词、架构与优化全景解构](https://zhuanlan.zhihu.com/p/1982199755456143593)

- [ ] [超全&超细的生成式推荐业界落地实践梳理](https://zhuanlan.zhihu.com/p/1989972800342095350)

![A Survey of Generative Recommendation from a Tri-Decoupled Perspective: Tokenization, Architecture, and Optimization (2025)|600](https://raw.githubusercontent.com/darstib/public_imgs/utool/2604/23_260423-121718.png)

## Sparse ID-Based

生成式推荐的 problem setting 和传统的序列推荐是基本一致的。所以先看两篇最经典的序列推荐，了解问题的 setting 是什么～

- [[ICDM2018] (SASRec) Self-Attentive Sequential Recommendation](https://www.yuque.com/darstib/research/zvzmpn8cr33m1995 "[ICDM2018] (SASRec) Self-Attentive Sequential Recommendation")
- [[CIKM2019] BERT4Rec: Sequential recommendation with bidirectional encoder representations from transformer](https://www.yuque.com/darstib/research/svcs8iclhubk9rcu "[CIKM2019] BERT4Rec: Sequential recommendation with bidirectional encoder representations from transformer")

## SID-Based

基于SID的生成式推荐方法中普遍用到的两个技术：1. [RQ-VAE](https://www.yuque.com/darstib/learning/dnehw9ygnzhtqkl5)； 2. [beam-search](https://www.yuque.com/darstib/learning/ggwdt1asf91dsseh#YTFgi)。

- [ ] [深度剖析RQ-VAE](https://www.cnblogs.com/GlenTt/p/19094976) 从训练和代码的角度进行了分析

看论文除了看懂文章的方法是怎么做的 (how to do) 之外，还要特别注意两点

- 一个是论文的 motivation (why do so)
- 另一个是论文有没有缺点、不足和可以改进的地方 (what I can do)

- [[NIPS2023] (TIGER) Recommender Systems with Generative Retrieval](https://www.yuque.com/darstib/research/cmuxi321y4p4oa17 "[NIPS2023] (TIGER) Recommender Systems with Generative Retrieval")
- [[CIKM2024] (ColaRec) Content-based collaborative generation for recommender systems](https://www.yuque.com/darstib/research/todgmui8efunf8k6 "[CIKM2024] (ColaRec) Content-based collaborative generation for recommender systems")
- [[CIKM2024] (LETTER) Learnable Item Tokenization for Generative Recommendation](https://www.yuque.com/darstib/research/xl4b73clexnb59tq "[CIKM2024] (LETTER) Learnable Item Tokenization for Generative Recommendation")
- [[RecSys2024] CoST: Contrastive Quantization based Semantic Tokenization for Generative Recommendation](https://www.yuque.com/darstib/research/bkxrslznb50mt8se "[RecSys2024] CoST: Contrastive Quantization based Semantic Tokenization for Generative Recommendation")
- [[SIGIR2025] (ETEGRec) Generative Recommender with End-to-End Learnable Item Tokenization](https://www.yuque.com/darstib/research/prztm2w8gybvtst7 "[SIGIR2025] (ETEGRec) Generative Recommender with End-to-End Learnable Item Tokenization")
- [[KDD2025] (RPG) Generating long semantic IDs in parallel for recommendation](https://www.yuque.com/darstib/research/qeglgk7raddiy9av "[KDD2025] (RPG) Generating long semantic IDs in parallel for recommendation")

## OneRec

以下为近两年 OneRec 系列相关论文的时间线整理，所有链接均指向对应 arXiv 页面。这些论文主要由快手（Kuaishou）团队发表，覆盖从基础框架到多场景应用的技术演进，反映生成式推荐在工业落地中的关键突破。

|          |                                                                                                             |                                                                      |
| -------- | ----------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| 发表时间     | 论文标题                                                                                                        | arXiv 链接                                                             |
| 2025年2月  | 《OneRec: Unifying Retrieve and Rank with Generative Recommender and Preference Alignment》                   | [https://arxiv.org/abs/2502.18965](https://arxiv.org/abs/2502.18965) |
| 2025年6月  | 《OneRec Technical Report》                                                                                   | [https://arxiv.org/abs/2506.13695](https://arxiv.org/abs/2506.13695) |
| 2025年8月  | 《OneRec-V2 Technical Report》                                                                                | [https://arxiv.org/abs/2508.20900](https://arxiv.org/abs/2508.20900) |
| 2025年9月  | 《OneSearch: A Preliminary Exploration of the Unified End-to-End Generative Framework for E-Commerce Search》 | [https://arxiv.org/abs/2509.03236](https://arxiv.org/abs/2509.03236) |
| 2025年9月  | 《OnePiece: Bringing Context Engineering and Reasoning to Industrial Cascade Ranking System》                 | [https://arxiv.org/abs/2509.18091](https://arxiv.org/abs/2509.18091) |
| 2025年10月 | 《OneRec-Think: In-Text Reasoning for Generative Recommendation》                                             | [https://arxiv.org/abs/2510.11639](https://arxiv.org/abs/2510.11639) |
| 2025年12月 | 《OpenOneRec Technical Report》                                                                               | [https://arxiv.org/abs/2512.24762](https://arxiv.org/abs/2512.24762) |
| 2026年2月  | 《GR4AD: Generative Recommendation for Large-Scale Advertising》                                              | [https://arxiv.org/abs/2602.22732](https://arxiv.org/abs/2602.22732) |