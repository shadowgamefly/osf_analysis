import numpy as np
import re
import itertools
from collections import Counter
import gensim
import pickle
import json
import os
import tensorflow as tf

def clean_str(string):
    """
    Tokenization/string cleaning for all datasets except for SST.
    Original taken from https://github.com/yoonkim/CNN_sentence/blob/master/process_data.py
    """
    string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
    string = re.sub(r"\'s", " \'s", string)
    string = re.sub(r"\'ve", " \'ve", string)
    string = re.sub(r"n\'t", " n\'t", string)
    string = re.sub(r"\'re", " \'re", string)
    string = re.sub(r"\'d", " \'d", string)
    string = re.sub(r"\'ll", " \'ll", string)
    string = re.sub(r",", " , ", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r"\(", " \( ", string)
    string = re.sub(r"\)", " \) ", string)
    string = re.sub(r"\?", " \? ", string)
    string = re.sub(r"\s{2,}", " ", string)
    return string.strip().lower()

def subject_to_label(subject):
    dict = {'law' : [1, 0], 'social-and-behavioral-sciences': [0, 1]}
    return dict[subject]

# learned word vector mapping
def load_data_and_labels():
    """
    Loads MR polarity data from files, splits the data into words and generates labels.
    Returns split sentences and labels.
    """
    # Load data from files
    x_text = []
    y = []
    # model = gensim.models.KeyedVectors.load_word2vec_format('./data/GoogleNews-vectors-negative300.bin', binary=True)
    for file in os.listdir(os.getcwd() + '/data') :
        with open(os.getcwd() + '/data/' +file, 'rb') as j:
            obj = json.load(j)
            x_text.append(clean_str(obj['abstract']))
            y.append(subject_to_label(obj['subject']))

    with open('cache/x_text.pickle', 'wb') as f :
        pickle.dump(x_text, f)

    with open('cache/y.pickle', 'wb') as f :
        pickle.dump(y, f)

    return [x_text, y]

def load_data_and_labels_2():
    x_text = []
    y = []
    model = gensim.models.KeyedVectors.load_word2vec_format('../osf_analysis/data/GoogleNews-vectors-negative300.bin', binary=True)
    print('finish model loading')
    for file in os.listdir(os.getcwd() + '/data') :
        with open(os.getcwd() + '/data/' +file, 'rb') as j:
            obj = json.load(j)
            x_text.append(clean_str(obj['abstract']))
            y.append(subject_to_label(obj['subject']))

    print('finish first iter loading')
    x = []
    max_len = -1
    min_len = 1000
    for text in x_text:
        words = text.split(' ')
        embedding = []
        for word in words:
            if word in model:
                embedding.append(model[word])
        if max_len < len(embedding):
            max_len = len(embedding)
        if min_len > len(embedding):
            min_len = len(embedding)
        x.append(embedding)
    print('finish second iter loading')

    print(max_len, min_len)
    for embedding in x:
        if len(embedding) < max_len:
            embedding += [0 for i in range(300)] * (max_len - len(embedding))

    print('finish third iter loading')

    with open('cache/static_x.pickle', 'wb') as f:
        pickle.dump(x, f)

    print('finish dumping')

    return x, y

def batch_iter(data, batch_size, num_epochs, shuffle=True):
    """
    Generates a batch iterator for a dataset.
    """
    data = np.array(data)
    data_size = len(data)
    num_batches_per_epoch = int((len(data)-1)/batch_size) + 1
    for epoch in range(num_epochs):
        # Shuffle the data at each epoch
        if shuffle:
            shuffle_indices = np.random.permutation(np.arange(data_size))
            shuffled_data = data[shuffle_indices]
        else:
            shuffled_data = data
        for batch_num in range(num_batches_per_epoch):
            start_index = batch_num * batch_size
            end_index = min((batch_num + 1) * batch_size, data_size)
            yield shuffled_data[start_index:end_index]

if __name__ == '__main__':
    load_data_and_labels_2()
