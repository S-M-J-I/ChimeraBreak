<div align="center">

# Official repository of ChimeraBreak & SVMA<br/>[ICCV 2025 SVU workshop]

<img width="200" src="./assets/logo.png" alt="logo" />


[![Paper](https://img.shields.io/badge/arxiv-2507.11968-red.svg)](https://arxiv.org/abs/2507.11968)
[![Paper](https://img.shields.io/badge/ICCV'25-SVU-blue.svg)](https://openaccess.thecvf.com/ICCV2025)
[![HF dataset](https://img.shields.io/badge/HuggingFace-SVMA-orange.svg)](https://huggingface.co/datasets/smji/SVMA-dataset)
[![License](https://img.shields.io/github/license/sahidmustakim/SVU2025)](./LICENSE)

</div>

## 🔍 Overview

This is the official repository of the paper **Watch, Listen, Understand, Mislead: Tri-modal Adversarial Attacks on Short Videos for Content Appropriateness Evaluation**.

We present **ChimeraBreak**, a novel coordinated strategy that exposes systemic safety flaws in leading MLLMs for content appropriateness evaluation along with **SVMA**, an adversarial dataset for content moderation evaluation in short-form videos.

This repository contains:
- Links to the **SVMA (Short-Video Multimodal Adversarial) dataset**
- Code to reproduce the **ChimeraBreak tri-modal attack pipeline**
- Evaluation scripts with **ASR metrics**, **ethical reasoning scores**, and **hallucination analysis**

📝 **Accepted at the SVU Workshop @ ICCV 2025**

<div align='center'>
<img src="./assets/graphical_abstract.png" alt="logo" />
</div>


\
The repository is structured as follows:
```bash
ChimeraBreak/
├── data/                  # annotation and hf_pipeline script
├── notebooks/             # Contains all attack and judge notebooks with eval. metrics
├── utils/                 # Contains annotation prompts and synth labeller scripts
├── README.md
└── requirements.txt
```

---

## 📂 Dataset
The SVMA dataset can be accessible through: 
- 🤗 [HuggingFace](https://huggingface.co/datasets/smji/SVMA-dataset)
- <img width=16 src='https://cdn4.iconfinder.com/data/icons/logos-and-brands/512/189_Kaggle_logo_logos-512.png' /> [Kaggle](https://www.kaggle.com/datasets/smjishanulislam/svmaa-bench)

---

## 🛠️ Pipelines

The code pipelines are available [here](./notebooks/), capable of running on a single GPU. If you're working on a notebook cloud environment (Kaggle, Colab etc.), there's no need to install any libraries as they all come with the notebook environments. Some environments do need the groq cloud installation. The local pipelines for Ollama can run on a single P100 GPU.

**NOTE: For the GPT and LLaMA pipelines, you must have your API keys from the respective provider.**

---

## 📑 Citation
```
@misc{mustakim2025watchlistenunderstandmislead,
      title={Watch, Listen, Understand, Mislead: Tri-modal Adversarial Attacks on Short Videos for Content Appropriateness Evaluation}, 
      author={Sahid Hossain Mustakim and S M Jishanul Islam and Ummay Maria Muna and Montasir Chowdhury and Mohammed Jawwadul Islam and Sadia Ahmmed and Tashfia Sikder and Syed Tasdid Azam Dhrubo and Swakkhar Shatabda},
      year={2025},
      eprint={2507.11968},
      archivePrefix={arXiv},
      primaryClass={cs.CV},
      url={https://arxiv.org/abs/2507.11968}, 
}
```

---

## 👥 Collaborators
[Sahid Hossain Mustakim](https://www.linkedin.com/in/sahid-hossain-mustakim-0504691b1), [S M Jishanul Islam](https://s-m-j-i.github.io/Personal-CV/), [Ummay Maria Muna](https://scholar.google.com/citations?user=a8DjRE0AAAAJ), [Montasir Chowdhury](https://www.linkedin.com/in/montasir-chowdhury-878309297), [Mohammad Jawwadul Islam](https://scholar.google.com/citations?user=lPrFLysAAAAJ), [Sadia Ahmmed](https://github.com/sadia-ahmmed), [Tashfia Sikder](https://www.linkedin.com/in/tashfia-sikder-78b1381b4), [Syed Tasdid Azam Dhrubo](https://www.linkedin.com/in/syed-tasdid-azam-dhrubo-864791197), and [Swakkhar Shatabda](https://cse.sds.bracu.ac.bd/faculty_profile/333/dr_swakkhar_shatabda).
