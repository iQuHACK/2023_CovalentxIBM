import numpy as np  
import pandas as pd

# BEGIN COPIED CODE: from https://docs.entropicalabs.io/qaoa/notebooks/7_clusteringwithqaoa
DF = pd.read_csv('./pokemon.csv', header=0)
DF = DF.set_index('#') #index pokemon by their ID number
DF = DF.rename_axis('ID') #rename axis to 'ID' instead of '#'
DF = DF.loc[~DF.index.duplicated(keep='first')] #drop duplicates
# END COPIED CODE: from https://docs.entropicalabs.io/qaoa/notebooks/7_clusteringwithqaoa

NUM_QBITS = 7

def is_pokemon_legendary(stats) -> bool:

    # Determines whether it is a legendary
    target_stat_vector = np.array(list(stats.values()), dtype=float)
    target_stat_vector = np.hstack((np.sum(target_stat_vector), target_stat_vector))
    
    distance_matrix = np.empty((NUM_QBITS, NUM_QBITS))
    
    legendary = DF.loc[DF['Legendary'] == True].sample(3)
    non_legendary = DF.loc[DF['Legendary'] == False].sample(3)
    pokemon = pd.concat([legendary,non_legendary])
    
    numerical_columns = ['Total','HP','Attack','Defense','Sp. Atk','Sp. Def','Speed']
    
    labels = pokemon['Legendary']
    data = pokemon[numerical_columns].copy().to_numpy()
    data = np.vstack((data,target_stat_vector))

    for i in range(len(data)):
        for j in range(len(data)):
            distance_matrix[i, j] = np.linalg.norm(data[i] - data[j])

    # Run the quantum algorithm
    clusters = [[0,1,2,6], [3,4,5]]

    target_cluster = clusters[0] if NUM_QBITS-1 in clusters[0] else clusters[1]
    target_cluster.remove(NUM_QBITS-1)
    return sum(labels.iloc[target_cluster]) / len(target_cluster) > 0.5

if __name__ == '__main__':
    import pdb; pdb.set_trace()
