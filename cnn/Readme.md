## Text CNN
This is the [CNN for text classification](https://github.com/shadowgamefly/osf_analysis/blob/master/cnn) built upon Kim's [Convolutional Neural Networks for Sentence Classification](http://arxiv.org/abs/1408.5882) and [dennybritz's work](https://github.com/dennybritz/cnn-text-classification-tf).

### Train
For detailed parameter reference can be found [here](https://github.com/shadowgamefly/osf_analysis/blob/master/cnn). If you are using fix pre-trained word embeddings, the `embedding-dim` parameter should match the pre-trained embedding size. The data currently is saved in root directory, so if you are using the text cnn along you need to change the route to those files. Once data is read, a training-data cache will be saved in `cnn`.

To start training do
``` bash
python train.py
```

The training log is also saved in `cnn` named as train_log.

### Eval
For Evaluation the data is also loaded from root directory so might need minor change for usage.

To eval do
``` bash
./eval.py --checkpoint_dir="./runs/1459637919/checkpoints/"
```

For all data route change you can do that in `data_helpers.py`
