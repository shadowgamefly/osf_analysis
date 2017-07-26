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
    category = ['law', 'social-and-behavioral-sciences', 'arts-and-humanities', 'education', 'medicine-and-health-sciences', \
     'life-sciences', 'physical-sciences-and-mathematics', 'engineering', 'business', 'architecture']
    l = []
    for i in range(10) :
        l.append([0 for i in range(10)])
        l[i][i] = 1
    dict = {category[i] : l[i] for i in range(10)}
    return dict[subject]

# learned word vector mapping
def load_data_and_labels(reindex = False):
    """
    Loads MR polarity data from files, splits the data into words and generates labels.
    Returns split sentences and labels.
    """
    if not reindex :
        print('loading preindexed data')
        try :
            with open('cache/new_x_text.pickle', 'rb') as f :
                x_text = pickle.load(f)

            with open('cache/new_y.pickle', 'rb') as f :
                y = pickle.load(f)

            return x_text, y

        except FileNotFoundError:
            print("preload data not found, reloading")
    # Load data from files
    x_text = []
    y = []
    data_dir = os.getcwd() + '/data/'
    for category in os.listdir(data_dir):
        if '.' in category:
            continue
        for file in os.listdir(data_dir + category):
            with open(data_dir + category + '/' +file, 'rb') as j:
                obj = json.load(j)
                x_text.append(clean_str(obj['abstract']))
                y.append(subject_to_label(obj['subject']))

    with open('cache/x_text.pickle', 'wb') as f :
        pickle.dump(x_text, f)

    with open('cache/y.pickle', 'wb') as f :
        pickle.dump(y, f)

    return [x_text, y]

def load_projects():
    print('loading projects from data/projects.json')
    x_text = []
    id = []
    with open('../data/projects_with_contributors.json', 'rb') as f:
        l = json.load(f)
    for project in l:
        if len(project['description'].split(' ')) < 10:
            continue
        else :
            x_text.append(clean_str(project['description']))
            id.append(project['_id'])
    return x_text, id


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


def inspect_projects():
    with open('../data/projects_with_contributors.json', 'rb') as f:
        l = json.load(f)
    print(l[0])

if __name__ == '__main__':
    load_projects()
