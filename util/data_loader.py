import os
import json
import pickle

def load_name_data(directory):
    print(directory)
    sex_dict = {}
    total = 0
    male = 0
    female = 0
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
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
                    total += 1
        else:
            continue
    with open('gender.pickle', 'wb') as f:
        pickle.dump(sex_dict, f, pickle.HIGHEST_PROTOCOL)
        print('dictionary has been saved in root directory')
        print('{:d} names loaded, {:d} males, {:d} females'.format(total,male, female)
    return sex_dict

