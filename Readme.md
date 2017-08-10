# Data Analysis for OSF
This is the repository for data Analysis for [OSF](https://osf.io), [github](https://github.com/centerforopenscience/osf.io).

## Prerequisite
To run the scripts here you will have following packages installed. A recommended package manager will be [conda](https://conda.io/miniconda.html).

Packages (updating):

* Python: 3.6
* jupyter notebook: latest
* matplotlib: latest
* tensorflow: 1.*

`environment.yml` is also provided in the root directory. To quickly set up the environment, do

```bash
conda env create -f environment.yml
source activate osf
```

## Analysis

### Gender Analysis
[gender_classifier](https://github.com/shadowgamefly/osf_analysis/blob/master/gender_classifier.ipynb) is used for calculating the gender distribution of the active users in OSF.

### Taxonomy Classification
I have built a [CNN for text classification](https://github.com/shadowgamefly/osf_analysis/blob/master/cnn) upon Kim's [Convolutional Neural Networks for Sentence Classification](http://arxiv.org/abs/1408.5882) and [dennybritz's work](https://github.com/dennybritz/cnn-text-classification-tf).

Some major changes including allowing multiclass classification, adopting static word embeddings which was discussed in Kim's Paper, allowing unknown choices for classification given noisy data, etc

The training data includes more than 60000 paper abstracts in 10 categories based on the taxonomy and data crawled from [bepress](network.bepress.com), and the pre-trained word embeddings is GoogleNews-vectors-negative300 from [word2vec](https://code.google.com/archive/p/word2vec/)

crawler is available [here](https://github.com/shadowgamefly/osf_analysis/blob/master/crawler), which uses xlml to parse the page source and also has the functionality to continue crawling if halted without losing any data.

### Consistency check
[consistency_check](https://github.com/shadowgamefly/osf_analysis/blob/master/consistency_check.ipynb) is to find the consistency of a certain contributor regarding the categories of the projects he/she contributes to.
