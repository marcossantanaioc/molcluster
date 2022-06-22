# molcluster
> Cluster molecules using kmeans, butina or HDBSCAN.


## How to use

You can use anyfunction to generate descriptors for the molecules in the dataset. For instance, we could use morgan fingerprints from RDkit to generate a vector of 1024 bits for each molecule. 

```python
from rdkit import Chem
import numpy as np
from molcluster.unsupervised_learning import KMeansClustering, HDBSCANClustering, ButinaClustering
```

```python
mol_list = ['CCCCCCC','c1ccccc1', 'c1ccccn1', 'c1cc(O)ccn1', 'c1cc(Cl)c(C(=O))cn1']
```

```python
X = np.array([Chem.AllChem.GetMorganFingerprintAsBitVect(x, radius=1024) for x in list(map(Chem.MolFromSmiles, mol_list))])
```

## Kmeans clustering with 10 clusters

```python
clustering_kmeans = KMeansClustering(X)
labels = clustering_kmeans.cluster(n_clusters=2)
labels[0:5]
```




    array([1, 1, 1, 1, 0], dtype=int32)



## Butina clustering with similarity threshold > 0.7

```python
clustering_butina = ButinaClustering(mol_list)
labels = clustering_butina.cluster(sim_cutoff=0.7)
labels[0:5]
```




    [4, 3, 2, 1, 0]



## HDBSCAN clustering

```python
clustering_hdbscan = HDBSCANClustering(X)
labels = clustering_hdbscan.cluster(min_cluster_size=5,min_samples=1,metric='euclidean')
```

```python
labels[0:5]
```




    array([-1, -1, -1, -1, -1])


