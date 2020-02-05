# opioids-change-detection-notebook

Opioid prescribing has risen by 127% in England between 1998 and 2016 [Curtis et al, 2018](https://doi.org/10.1016/S2215-0366(18)30471-1) which along with the US Opioid Crisis has fuelled concern over current opioid prescribing patterns and potential addiction in  England. At the direction of the Secretary of State for Health, Public Health England have produced a [report the evidence](https://www.gov.uk/government/publications/prescribed-medicines-review-report) for dependence on, and withdrawal from, prescribed medicines. The first recommendation of this report is 

  >Increasing the availability and use of data on the prescribing of medicines that can
  cause dependence or withdrawal to support greater transparency and accountability
  and help ensure practice is consistent and in line with guidance.
  
OpenPrescribing has over 70 measures of prescribing safety, effectiveness and cost including measures on opioids and opioid prescribing dashboards for every single general practice, primary care network (PCN), clinical commissioning group (CCG), sustainability and transformation partnership (STP), NHS region and for the [whole of England](https://openprescribing.net/all-england/?tags=opioids). We also have various methods for detecting changes in prescribing and highlighting to prescribers.  

This notebook seeks to implement the OpenPrescribing [Change Detection python library](https://pypi.org/project/change_detection/) which has previously been described in a [paper in the BMJ](https://doi.org/10.1136/bmj.l5205) on two specific measures (desogestrel & nitrofurantoin/trimethoprim). We aim to support the recomendations of the PHE review by  identifing clinical commissioning groups (CCG) and general practices whose prescribing data indicates they have successfully implemented an intervention to reduce prescribing of opioids.

We have also implemeted the CUSUM technique we use for powering the OpenPrescribing bespoke email alerts in [this repo](https://github.com/ebmdatalab/cusum-for-opioids-notebook) to support further investigations. 

![status](https://github.com/ebmdatalab/opioids-change-detection-notebook/workflows/Notebook%20checks/badge.svg)

## Getting started with this skeleton project

This is a skeleton project for creating a reproducible, cross-platform
analysis notebook, using Docker.  It also includes:

* configuration for `jupytext`, to support easier code review
* cross-platform startup scripts
* best practice folder structure and documentation

Developers and analysts using this skeleton for new development should
refer to [`DEVELOPERS.md`](DEVELOPERS.md) for instructions on getting
started.  Update this `README.md` so it is a suitable introduction to
your project.

## How to view the notebooks

Notebooks live in the `notebooks/` folder (with an `ipynb`
extension). You can most easily view them [on
nbviewer](https://nbviewer.jupyter.org/github/ebmdatalab/opioids-change-detection-notebook/tree/master/notebooks/),
though looking at them in Github should also work.

To do development work, you'll need to set up a local jupyter server
and git repository - see `DEVELOPERS.md` for more detail.

## How to cite

XXX
