import matplotlib.pyplot as plt

def plot(data):
    if 'key' not in data:
        raise KeyError("x-axis label needs to be named as key in the data dict.")
    key = data['key']
    fig, ax1 = plt.subplots()
    ax1.set_xlabel('Threshold of possibility to categorize')
    ax1.set_ylabel('Percentage in total population')
    # ax2 = ax1.twinx()
    # ax2.set_ylable('ratio of male to female user')

    for lines in data:
        if lines == 'key':
            continue
        else :
            line_name = lines
            line_value = data[lines]
            ax1.plot(key, line_value, '-o', label=line_name)


    plt.legend(loc='best')
    plt.show()
