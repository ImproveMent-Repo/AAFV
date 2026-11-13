"""Assemble references.bib for AAFV-05.
- Entries reused verbatim from the audited AAFV-04 bibliography (AAFV-04_revision/manuscript/references.bib).
- Entries added in the 2026-11-13 redesign, each checked against the publisher page, CVF open access or arXiv
  (sources listed in CVPR_redesign/phase5_literature/RELATED_WORK.md, Section 12). Fields not confirmed are omitted, not guessed.
Usage: python scripts/build_bib.py   (from publication_AAFV-05/)"""
import re
from pathlib import Path

PUB = Path(__file__).resolve().parent.parent
OLD = (PUB.parent / "AAFV-04_revision/manuscript/references.bib").read_text(encoding="utf-8")

REUSE = ["wang2018oecnn", "wang2019dal", "huang2021mtlface", "wang2025ordcon", "zhao2022aim", "bestrowden2018longitudinal",
         "alaluf2021sam", "karras2020stylegan2", "huang2021pfagan", "tang2018ipcgan", "deng2019arcface", "kim2022adaface",
         "meng2021magface", "shi2019pfe", "poh2009quality", "chow1970reject", "geifman2017selective", "vovk2005alrw",
         "angelopoulos2024crc", "tibshirani2019covshift", "hanley1983rule3", "clopper1934", "bolle2004subsets", "schuckers2010book",
         "ricanek2006morph", "lanitis2002fgnet", "moschoglou2017agedb", "zheng2017calfw", "chen2014cacd", "grother2019frvt_part3",
         "deb2018child", "dosovitskiy2021vit", "parkhi2015vgg", "tan2019efficientnet", "zhang2018lpips", "wang2004ssim",
         "platt1999", "iso19795_1", "guo2017calibration", "chopra2005siamese"]

NEW = r"""
@inproceedings{chang2020dul,
  author    = {Jie Chang and Zhonghao Lan and Changmao Cheng and Yichen Wei},
  title     = {Data Uncertainty Learning in Face Recognition},
  booktitle = {Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR)},
  pages     = {5710--5719},
  year      = {2020}
}

@inproceedings{kendall2017uncertainty,
  author    = {Alex Kendall and Yarin Gal},
  title     = {What Uncertainties Do We Need in {Bayesian} Deep Learning for Computer Vision?},
  booktitle = {Proc. Adv. Neural Inf. Process. Syst. (NIPS)},
  year      = {2017}
}

@article{huang2022mtlfacetpami,
  author  = {Zhizhong Huang and Junping Zhang and Hongming Shan},
  title   = {When Age-Invariant Face Recognition Meets Face Age Synthesis: A Multi-Task Learning Framework and A New Benchmark},
  journal = {IEEE Trans. Pattern Anal. Mach. Intell.},
  year    = {2022},
  note    = {arXiv:2210.09835}
}

@inproceedings{banerjee2023aging,
  author    = {Sudipta Banerjee and Govind Mittal and Ameya Joshi and Chinmay Hegde and Nasir Memon},
  title     = {Identity-Preserving Aging of Face Images via Latent Diffusion Models},
  booktitle = {Proc. IEEE Int. Joint Conf. Biometrics (IJCB)},
  year      = {2023},
  note      = {arXiv:2307.08585}
}

@inproceedings{chen2023fading,
  author    = {Xiangyi Chen and St{\'e}phane Lathuili{\`e}re},
  title     = {Face Aging via Diffusion-based Editing},
  booktitle = {Proc. British Mach. Vis. Conf. (BMVC)},
  year      = {2023},
  note      = {arXiv:2309.11321}
}

@inproceedings{luevano2025aging,
  author    = {Luis S. Luevano and Pavel Korshunov and S{\'e}bastien Marcel},
  title     = {Identity-Preserving Aging and De-Aging of Faces in the {StyleGAN} Latent Space},
  booktitle = {Proc. IEEE Int. Joint Conf. Biometrics (IJCB)},
  year      = {2025},
  note      = {arXiv:2508.08808}
}

@inproceedings{deng2020subcenter,
  author    = {Jiankang Deng and Jia Guo and Tongliang Liu and Mingming Gong and Stefanos Zafeiriou},
  title     = {Sub-center {ArcFace}: Boosting Face Recognition by Large-Scale Noisy Web Faces},
  booktitle = {Proc. Eur. Conf. Comput. Vis. (ECCV)},
  pages     = {741--757},
  year      = {2020}
}

@misc{dahan2023wasserstein,
  author       = {Eran Dahan and Yosi Keller},
  title        = {Age-Invariant Face Embedding using the {Wasserstein} Distance},
  howpublished = {arXiv:2305.02745},
  year         = {2023}
}
"""


def entry(key):
    m = re.search(r"@\w+\{" + re.escape(key) + r",.*?\n\}", OLD, flags=re.S)
    if not m:
        raise SystemExit(f"missing in AAFV-04 bibliography: {key}")
    return m.group(0)


out = "% AAFV-05 bibliography. Reused entries: audited AAFV-04 bibliography. New entries: verified 2026-11-13 (see build_bib.py).\n\n"
out += "\n\n".join(entry(k) for k in REUSE) + "\n" + NEW
(PUB / "references.bib").write_text(out, encoding="utf-8")
print(f"references.bib: {len(REUSE)} reused + {NEW.count('@')} new entries")
