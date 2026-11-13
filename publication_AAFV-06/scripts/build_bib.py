"""Assemble references.bib for AAFV-06 (analysis of every prior list: ../REFERENCE_ANALYSIS.md).
REUSE : entries copied verbatim from the audited AAFV-04 bibliography.
NEW   : entries verified against publisher / CVF / arXiv / DBLP-type listings on 2026-11-13/14 (sources in REFERENCE_ANALYSIS.md).
KNOWN : three standard references whose details were cross-checked against the BASE_Paper list but not re-looked-up online
        (marked in REFERENCE_ANALYSIS.md; re-check before submission).
Fields that could not be confirmed are omitted rather than guessed.
Usage: python scripts/build_bib.py   (from publication_AAFV-06/)"""
import re
from pathlib import Path

PUB = Path(__file__).resolve().parent.parent
OLD = (PUB.parent / "AAFV-04_revision/manuscript/references.bib").read_text(encoding="utf-8")

REUSE = [
    # age-invariant recognition, aging, longitudinal
    "li2011aifr", "wang2018oecnn", "wang2019dal", "huang2021mtlface", "wang2025ordcon", "zhao2022aim", "bestrowden2018longitudinal",
    "deb2018child", "zhang2017caae", "tang2018ipcgan", "huang2021pfagan", "alaluf2021sam", "karras2020stylegan2",
    # recognition backbones and similarity measures used by AAFV-Net
    "wang2018cosface", "deng2019arcface", "meng2021magface", "kim2022adaface", "parkhi2015vgg", "tan2019efficientnet",
    "zhang2018lpips", "wang2004ssim", "chopra2005siamese", "dosovitskiy2021vit", "hu2022lora", "wang2024qwen2vl",
    # fusion, quality, uncertainty, calibration
    "kittler1998combining", "ross2003fusion", "nandakumar2008lr", "poh2009quality", "shi2019pfe", "ahn2024ucface", "xu2024asc",
    "platt1999", "zadrozny2002isotonic", "guo2017calibration", "naeini2015ece", "brier1950",
    # reject option, selective classification, risk control, error estimation
    "chow1970reject", "herbei2006reject", "elyaniv2010selective", "geifman2017selective", "vovk2005alrw", "angelopoulos2024crc",
    "angelopoulos2021ltt", "tibshirani2019covshift", "hanley1983rule3", "clopper1934", "bolle2004subsets", "schuckers2010book", "iso19795_1",
    # threat model, demographics, attacks, privacy
    "paone2014twins", "klare2012demographics", "grother2019frvt_part3", "krishnapriya2020race", "buolamwini2018gendershades",
    "phillips2018pnas", "scherhag2019morph", "iso30107_3", "otroshi2024inversion", "razeghi2026privacy", "zhou2024openset", "hu2025neyman",
    # datasets
    "ricanek2006morph", "lanitis2002fgnet", "moschoglou2017agedb", "chen2014cacd", "zheng2017calfw", "maze2018ijbc",
]

NEW = r"""
@inproceedings{chang2020dul,
  author = {Jie Chang and Zhonghao Lan and Changmao Cheng and Yichen Wei},
  title = {Data Uncertainty Learning in Face Recognition},
  booktitle = {Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR)}, pages = {5710--5719}, year = {2020}
}
@inproceedings{kendall2017uncertainty,
  author = {Alex Kendall and Yarin Gal},
  title = {What Uncertainties Do We Need in {Bayesian} Deep Learning for Computer Vision?},
  booktitle = {Proc. Adv. Neural Inf. Process. Syst. (NIPS)}, year = {2017}
}
@article{huang2022mtlfacetpami,
  author = {Zhizhong Huang and Junping Zhang and Hongming Shan},
  title = {When Age-Invariant Face Recognition Meets Face Age Synthesis: A Multi-Task Learning Framework and A New Benchmark},
  journal = {IEEE Trans. Pattern Anal. Mach. Intell.}, year = {2022}, note = {arXiv:2210.09835}
}
@inproceedings{banerjee2023aging,
  author = {Sudipta Banerjee and Govind Mittal and Ameya Joshi and Chinmay Hegde and Nasir Memon},
  title = {Identity-Preserving Aging of Face Images via Latent Diffusion Models},
  booktitle = {Proc. IEEE Int. Joint Conf. Biometrics (IJCB)}, year = {2023}, note = {arXiv:2307.08585}
}
@inproceedings{chen2023fading,
  author = {Xiangyi Chen and St{\'e}phane Lathuili{\`e}re},
  title = {Face Aging via Diffusion-based Editing},
  booktitle = {Proc. British Mach. Vis. Conf. (BMVC)}, year = {2023}, note = {arXiv:2309.11321}
}
@inproceedings{luevano2025aging,
  author = {Luis S. Luevano and Pavel Korshunov and S{\'e}bastien Marcel},
  title = {Identity-Preserving Aging and De-Aging of Faces in the {StyleGAN} Latent Space},
  booktitle = {Proc. IEEE Int. Joint Conf. Biometrics (IJCB)}, year = {2025}, note = {arXiv:2508.08808}
}
@inproceedings{deng2020subcenter,
  author = {Jiankang Deng and Jia Guo and Tongliang Liu and Mingming Gong and Stefanos Zafeiriou},
  title = {Sub-center {ArcFace}: Boosting Face Recognition by Large-Scale Noisy Web Faces},
  booktitle = {Proc. Eur. Conf. Comput. Vis. (ECCV)}, pages = {741--757}, year = {2020}
}
@misc{dahan2023wasserstein,
  author = {Eran Dahan and Yosi Keller},
  title = {Age-Invariant Face Embedding using the {Wasserstein} Distance},
  howpublished = {arXiv:2305.02745}, year = {2023}
}
@inproceedings{richardson2021psp,
  author = {Elad Richardson and Yuval Alaluf and Or Patashnik and Yotam Nitzan and Yaniv Azar and Stav Shapiro and Daniel Cohen-Or},
  title = {Encoding in Style: A {StyleGAN} Encoder for Image-to-Image Translation},
  booktitle = {Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR)}, pages = {2287--2296}, year = {2021}
}
@article{rothe2018dex,
  author = {Rasmus Rothe and Radu Timofte and Luc {Van Gool}},
  title = {Deep Expectation of Real and Apparent Age from a Single Image Without Facial Landmarks},
  journal = {Int. J. Comput. Vis.}, volume = {126}, year = {2018}
}
@inproceedings{guo2022scrfd,
  author = {Jia Guo and Jiankang Deng and Alexandros Lattas and Stefanos Zafeiriou},
  title = {Sample and Computation Redistribution for Efficient Face Detection},
  booktitle = {Proc. Int. Conf. Learn. Represent. (ICLR)}, year = {2022}
}
@inproceedings{orel2020lifespan,
  author = {Roy Or-El and Soumyadip Sengupta and Ohad Fried and Eli Shechtman and Ira Kemelmacher-Shlizerman},
  title = {Lifespan Age Transformation Synthesis},
  booktitle = {Proc. Eur. Conf. Comput. Vis. (ECCV)}, year = {2020}
}
@article{immerkaer1996noise,
  author = {John Immerk{\ae}r},
  title = {Fast Noise Variance Estimation},
  journal = {Comput. Vis. Image Underst.}, volume = {64}, number = {2}, pages = {300--302}, year = {1996}
}
@inproceedings{terhorst2020serfiq,
  author = {Philipp Terh{\"o}rst and Jan Niklas Kolf and Naser Damer and Florian Kirchbuchner and Arjan Kuijper},
  title = {{SER-FIQ}: Unsupervised Estimation of Face Image Quality Based on Stochastic Embedding Robustness},
  booktitle = {Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR)}, pages = {5650--5659}, year = {2020}
}
@inproceedings{boutros2023crfiqa,
  author = {Fadi Boutros and Meiling Fang and Marcel Klemt and Biying Fu and Naser Damer},
  title = {{CR-FIQA}: Face Image Quality Assessment by Learning Sample Relative Classifiability},
  booktitle = {Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR)}, year = {2023}
}
@inproceedings{qi2025mytimemachine,
  author = {Luchao Qi and Jiaye Wu and Bang Gong and Annie N. Wang and David W. Jacobs and Roni Sengupta},
  title = {{MyTimeMachine}: Personalized Facial Age Transformation},
  booktitle = {ACM Trans. Graph. (Proc. SIGGRAPH)}, volume = {44}, number = {4}, year = {2025}
}
@inproceedings{su2025timebooth,
  author = {Zepeng Su and Zhulin Liu and Zongyan Zhang and Tong Zhang and C. L. Philip Chen},
  title = {{TimeBooth}: Disentangled Facial Invariant Representation for Diverse and Personalized Face Aging},
  booktitle = {Proc. IEEE/CVF Int. Conf. Comput. Vis. (ICCV)}, pages = {12147--12157}, year = {2025}
}
@inproceedings{boutros2023idiff,
  author = {Fadi Boutros and Jonas Henry Grebe and Arjan Kuijper and Naser Damer},
  title = {{IDiff-Face}: Synthetic-based Face Recognition through Fizzy Identity-Conditioned Diffusion Models},
  booktitle = {Proc. IEEE/CVF Int. Conf. Comput. Vis. (ICCV)}, year = {2023}
}
@article{bianco2017lag,
  author = {Simone Bianco},
  title = {Large Age-Gap Face Verification by Feature Injection in Deep Networks},
  journal = {Pattern Recognit. Lett.}, volume = {90}, pages = {36--42}, year = {2017}
}
"""

KNOWN = r"""
@inproceedings{he2016resnet,
  author = {Kaiming He and Xiangyu Zhang and Shaoqing Ren and Jian Sun},
  title = {Deep Residual Learning for Image Recognition},
  booktitle = {Proc. IEEE Conf. Comput. Vis. Pattern Recognit. (CVPR)}, pages = {770--778}, year = {2016}
}
@article{king2009dlib,
  author = {Davis E. King},
  title = {Dlib-ml: A Machine Learning Toolkit},
  journal = {J. Mach. Learn. Res.}, volume = {10}, pages = {1755--1758}, year = {2009}
}
@book{efron1994bootstrap,
  author = {Bradley Efron and Robert J. Tibshirani},
  title = {An Introduction to the Bootstrap},
  publisher = {Chapman \& Hall/CRC}, year = {1994}
}
"""


def entry(key):
    m = re.search(r"@\w+\{" + re.escape(key) + r",.*?\n\}", OLD, flags=re.S)
    if not m:
        raise SystemExit(f"missing in AAFV-04 bibliography: {key}")
    return m.group(0)


out = "% AAFV-06 bibliography; see REFERENCE_ANALYSIS.md for the status of every entry.\n\n"
out += "\n\n".join(entry(k) for k in REUSE) + "\n" + NEW + KNOWN
(PUB / "references.bib").write_text(out, encoding="utf-8")
print(f"references.bib: {len(REUSE)} reused + {NEW.count('@')} new verified + {KNOWN.count('@')} standard = {len(REUSE) + NEW.count('@') + KNOWN.count('@')}")
