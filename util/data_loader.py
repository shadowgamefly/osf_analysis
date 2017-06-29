import os
import json
import pickle

def load_name_data(data_dir):
    try :
        with open('gender.pickle', 'rb') as f:
            sex_dict = pickle.load(f)
            print('pickle data found and loaded')
            
    except (EOFError, FileNotFoundError) as e:
        if e == EOFError:
            print('current pickle data is broken')
            print('reloading...')
        elif e == FileNotFoundError:
            print('no loaded data found')
            print('loading...')
        sex_dict = process_name_data(data_dir)
        
    return sex_dict

def process_name_data(directory):
    directory = os.path.join(directory, 'names')
    print(directory)
    sex_dict = {}
    total = 0
    people = 0
    male = 0
    female = 0
    files = 0
    count = 0
    print("Loading", end = "")
    for file in os.listdir(directory):
        if count % 10 == 0:
            print(".", end = "")
        count += 1
        filename = os.fsdecode(file)
        files += 1
        if filename.endswith(".txt"): 
            with open(os.path.join(directory, file), 'rb') as f:
                content = f.readlines()
                for line in content:
                    result = line.decode().split(',')
                    name, gender, num = result[0].lower(), int(result[1] == 'F'), int(result[2])
                    if gender:
                        female += 1
                    else :
                        male += 1
                    if name in sex_dict:
                        sex_dict[name][gender] += num
                    else :
                        sex_dict[name] = [0, 0]
                        sex_dict[name][gender] += num
                    people += num
                    total += 1
        else:
            continue
    with open('gender.pickle', 'wb') as f:
        pickle.dump(sex_dict, f, pickle.HIGHEST_PROTOCOL)
        print('\n')
        print('dictionary has been saved in root directory as gender.pickle')
        print('{:d} files found, {:d} names among {:d} people loaded, {:d} male names, {:d} females names'.format(files, total, people, male, female))
    
    return sex_dict