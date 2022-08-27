# AUTOGENERATED! DO NOT EDIT! File to edit: ../../notebooks/clustering.ipynb.

# %% auto 0
__all__ = ['BaseClustering', 'HierarchicalClustering', 'KMeansClustering', 'HDBSCANClustering', 'ButinaClustering']

# %% ../../notebooks/clustering.ipynb 3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
from collections import defaultdict
from tqdm.auto import tqdm
import optuna

from fastcore.basics import *
from fastcore.foundation import *
from fastcore.meta import *
from ..typing_basics import *

from sklearn.cluster import KMeans, AgglomerativeClustering
from rdkit.ML.Cluster import Butina
from sklearn.metrics import silhouette_score, silhouette_samples
import hdbscan

from rdkit import Chem
from rdkit import DataStructs
from rdkit.Chem import AllChem, Descriptors
from rdkit.Chem import MACCSkeys
from rdkit.Chem.AtomPairs import Pairs

from kneed import KneeLocator

# %% ../../notebooks/clustering.ipynb 5
class BaseClustering:
    
    """Base class to perform clustering on a collection of molecules. 
    Use children classes `KMeansClustering`, `HDBSCANClustering`, `ButinaClustering` to cluster molecules
    
    """
    
    def __init__(self):
        pass
    
    def cluster(self):
        pass
                
    @property
    def clusterer(self):
        return self._clusterer
    
    @clusterer.setter
    def clusterer(self, i):
        self._clusterer = i
        
    @property
    def labels(self):
        return self._labels
    
    @labels.setter
    def labels(self, i):
        if isinstance(i, Sequence) and not isinstance(i, str):
            self._labels = i

# %% ../../notebooks/clustering.ipynb 7
class HierarchicalClustering(BaseClustering):
    
    """Performs agglomerative hierarchical clustering on a dataset of molecules
    
    Attributes:

    dataset : numpy.array
        An array of features with shape (n,p), where n is the number of molecules and p is the number of descriptors.
        
        
    Methods:

    cluster(n_clusters:int)
        Performs k-means clustering on ´self.dataset´
        
             
    """
    
    def __init__(self, dataset : ArrayLike):
        
        """
        Parameters:

            dataset : numpy.array
        
        """
        self.dataset = dataset
            
    def cluster(self,n_clusters:int=2,
                affinity:str='euclidean', 
                memory=None, 
                connectivity=None,
                compute_full_tree='auto',
                linkage='ward',
                distance_threshold=None,
                compute_distances=False):
        
        """Clustering molecules using different hierarchical methods available on scikit-learn.
        
    Arguments:

        n_clusters : int or None, default=2
            The number of clusters to find. It must be ``None`` if
            ``distance_threshold`` is not ``None``.

        affinity : str or callable, default='euclidean'
            Metric used to compute the linkage. Can be "euclidean", "l1", "l2",
            "manhattan", "cosine", or "precomputed".
            If linkage is "ward", only "euclidean" is accepted.
            If "precomputed", a distance matrix (instead of a similarity matrix)
            is needed as input for the fit method.

        memory : str or object with the joblib.Memory interface, default=None
            Used to cache the output of the computation of the tree.
            By default, no caching is done. If a string is given, it is the
            path to the caching directory.

        connectivity : array-like or callable, default=None
            Connectivity matrix. Defines for each sample the neighboring
            samples following a given structure of the data.
            This can be a connectivity matrix itself or a callable that transforms
            the data into a connectivity matrix, such as derived from
            `kneighbors_graph`. Default is ``None``, i.e, the
            hierarchical clustering algorithm is unstructured.

        compute_full_tree : 'auto' or bool, default='auto'
            Stop early the construction of the tree at ``n_clusters``. This is
            useful to decrease computation time if the number of clusters is not
            small compared to the number of samples. This option is useful only
            when specifying a connectivity matrix. Note also that when varying the
            number of clusters and using caching, it may be advantageous to compute
            the full tree. It must be ``True`` if ``distance_threshold`` is not
            ``None``. By default `compute_full_tree` is "auto", which is equivalent
            to `True` when `distance_threshold` is not `None` or that `n_clusters`
            is inferior to the maximum between 100 or `0.02 * n_samples`.
            Otherwise, "auto" is equivalent to `False`.

        linkage : {'ward', 'complete', 'average', 'single'}, default='ward'
            Which linkage criterion to use. The linkage criterion determines which
            distance to use between sets of observation. The algorithm will merge
            the pairs of cluster that minimize this criterion.
            - 'ward' minimizes the variance of the clusters being merged.
            - 'average' uses the average of the distances of each observation of
              the two sets.
            - 'complete' or 'maximum' linkage uses the maximum distances between
              all observations of the two sets.
            - 'single' uses the minimum of the distances between all observations
              of the two sets.

        distance_threshold : float, default=None
            The linkage distance threshold above which, clusters will not be
            merged. If not ``None``, ``n_clusters`` must be ``None`` and
            ``compute_full_tree`` must be ``True``.

        compute_distances : bool, default=False
            Computes distances between clusters even if `distance_threshold` is not
            used. This can be used to make dendrogram visualization, but introduces
            a computational and memory overhead.
            
            
        Returns:
    
            labels : np.array
                Clustering labels
        
        """

        cls = AgglomerativeClustering(n_clusters=n_clusters,
                affinity=affinity, 
                memory=memory, 
                connectivity=connectivity,
                compute_full_tree=compute_full_tree,
                linkage=linkage,
                distance_threshold=distance_threshold,
                compute_distances=compute_distances)

        cls.fit(self.dataset)
        
        self._clusterer = cls
        self._labels = cls.labels_
        return self._labels
    
    def plot_dendogram(self, n_clusters:List, figsize:Tuple=(12,9), **kwargs):
        raise NotImplementedError

#         self.inertias = []
#         for n in n_clusters:
#             self.cluster(n, **kwargs)   
#             inertia = self.clusterer.inertia_
#             self.inertias.append(inertia)
            
#         # Find elbow
#         params = {"curve": "convex",
#                     "direction": "decreasing"}
        
#         knee_finder = KneeLocator(n_clusters, self.inertias, **params)
#         self.elbow_value = knee_finder.elbow
        
#         # Plot Elbow
#         sns.set_context('paper',font_scale=2.0)
#         sns.set_style('whitegrid')
        
#         fig = plt.figure(figsize=figsize)
#         # Dendogram for Heirarchical Clustering
#         import scipy.cluster.hierarchy as shc
#         dend = shc.dendrogram(shc.linkage(cluster_df, method='ward'))


#         ax.set_xlabel('Number of clusters (K)')
#         ax.set_ylabel('Distortion')
#         sns.despine(right=True,top=True)
#         plt.title('K-means Elbow method',fontweight='bold',fontsize=22)
        
#         if self.elbow_value is not None:
#             elbow_label = "Elbow at $K={}$".format(self.elbow_value)      
#             ax.axvline(self.elbow_value, c='k', linestyle="--",label=elbow_label)
#             ax.legend(loc="best", fontsize=18, frameon=True)
#         for i in ax.spines.items():
#             i[1].set_linewidth(1.5)
#             i[1].set_color('k')

#         plt.tight_layout()
#         plt.show()

# %% ../../notebooks/clustering.ipynb 8
class KMeansClustering(BaseClustering):
    
    """Performs k-means clustering on a dataset of molecules
    
    Attributes:

    dataset : numpy.array
        An array of features with shape (n,p), where n is the number of molecules and p is the number of descriptors.
        
        
    Methods:

    cluster(n_clusters:int)
        Performs k-means clustering on ´self.dataset´
        
        
    elbow_method(n_clusters:List, figsize:Tuple)
        Uses the elbow method to find the optimal number of clusters
             
    """
    
    def __init__(self, dataset : ArrayLike):
        
        """
        Parameters:

            dataset : numpy.array
        
        """
        self.dataset = dataset
            
    def cluster(self, n_clusters:int=10, **kwargs):
        
        """Run k-means on the dataset
        
        Arguments:

            n_clusters : int (default=10)
                Number of clusters

        Keyword arguments:
            max_iter : int (default=5)
            n_init : int (default=5)
            init : str (default='k-means++')
            random_state : int (default=None)
            
            
        Returns:
    
            labels : np.array
                Clustering labels
        
        """
        
        max_iter = kwargs.get('max_iter', 500)
        n_init = kwargs.get('n_init', 10)
        init = kwargs.get('init', 'k-means++')
        random_state = kwargs.get('random_state', None)
        
        cls = KMeans(n_clusters=n_clusters, init=init, n_init=n_init, max_iter=max_iter, random_state=random_state)
        cls.fit(self.dataset)
        
        self._clusterer = cls
        self._labels = cls.labels_
        return self._labels
    
    def elbow_method(self, n_clusters:List, figsize:Tuple=(12,9), **kwargs):

        self.inertias = []
        for n in n_clusters:
            self.cluster(n, **kwargs)   
            inertia = self.clusterer.inertia_
            self.inertias.append(inertia)
            
        # Find elbow
        params = {"curve": "convex",
                    "direction": "decreasing"}
        
        knee_finder = KneeLocator(n_clusters, self.inertias, **params)
        self.elbow_value = knee_finder.elbow
        
        # Plot Elbow
        sns.set_context('paper',font_scale=2.0)
        sns.set_style('whitegrid')
        
        fig = plt.figure(figsize=figsize)
        ax=sns.lineplot(x=n_clusters, y=np.array(self.inertias), linewidth=2.5, marker='o', color='blue', markersize=7)

        ax.set_xlabel('Number of clusters (K)')
        ax.set_ylabel('Distortion')
        sns.despine(right=True,top=True)
        plt.title('K-means Elbow method',fontweight='bold',fontsize=22)
        
        if self.elbow_value is not None:
            elbow_label = "Elbow at $K={}$".format(self.elbow_value)      
            ax.axvline(self.elbow_value, c='k', linestyle="--",label=elbow_label)
            ax.legend(loc="best", fontsize=18, frameon=True)
        for i in ax.spines.items():
            i[1].set_linewidth(1.5)
            i[1].set_color('k')

        plt.tight_layout()
        plt.show()

# %% ../../notebooks/clustering.ipynb 11
class HDBSCANClustering(BaseClustering):
    
    """Performs HDBSCAN clustering on a dataset of molecules
    
    
    Attributes:

        dataset : numpy.array
            An array of features with shape (n,p), where n is the number of molecules and p is the number of descriptors.


    Methods:

        cluster(n_clusters:int)
            Performs k-means clustering on ´self.dataset´
            
        validate_clustering(X, labels)
            Compute the density based cluster validity index for the clustering specified by labels and for each cluster in labels.

    
    
    """
    
    def __init__(self, dataset : ArrayLike):
        self.dataset = dataset
            
            
    def cluster(self, min_cluster_size:int=5, min_samples:int=None, metric:str='jaccard', **kwargs):
        
        """Run HDBSCAN clustering on the dataset
        
        Arguments:


           min_cluster_size : int, optional (default=5)
               The minimum size of clusters; single linkage splits that contain
               fewer points than this will be considered points "falling out" of a
               cluster rather than a cluster splitting into two new clusters.

           min_samples : int, optional (default=None)
               The number of samples in a neighbourhood for a point to be
               considered a core point.

           metric : string, or callable, optional (default='euclidean')
               The metric to use when calculating distance between instances in a
               feature array. If metric is a string or callable, it must be one of
               the options allowed by metrics.pairwise.pairwise_distances for its
               metric parameter.
               If metric is "precomputed", X is assumed to be a distance matrix and
               must be square.
                              
        Keyword arguments:
        
            See HDBSCAN documentation (https://hdbscan.readthedocs.io/en/latest/index.html)
            
        Returns:
        
            labels : np.array
                Clustering labels
        
        """
        
        cls = hdbscan.HDBSCAN(min_cluster_size=min_cluster_size, min_samples=min_samples, metric=metric, **kwargs)
        cls.fit(self.dataset)
        
        self._clusterer = cls
        self._labels = cls.labels_
        return self._labels
    
    @staticmethod
    def validate_clustering(X, labels, metric='euclidean', d=None, per_cluster_scores=False, **kwargs):
        
        """
        
        Arguments:
        
            X :array (n_samples, n_features) or (n_samples, n_samples)
                The input data of the clustering. This can be the data, or, if metric is set to precomputed the pairwise distance matrix used for the clustering.
            labels :array (n_samples)
                The label array output by the clustering, providing an integral cluster label to each data point, with -1 for noise points.

            metric :optional, string (default ‘euclidean’)
                The metric used to compute distances for the clustering (and to be re-used in computing distances for mr distance). If set to precomputed then X is assumed to be the precomputed distance matrix between samples.
            d :optional, integer (or None) (default None)
                The number of features (dimension) of the dataset. This need only be set in the case of metric being set to precomputed, where the ambient dimension of the data is unknown to the function.

            per_cluster_scores :optional, boolean (default False)
                Whether to return the validity index for individual clusters. Defaults to False with the function returning a single float value for the whole clustering.

        Returns:
            validity_index : float
                The density based cluster validity index for the clustering. This is a numeric value between -1 and 1, with higher values indicating a ‘better’ clustering.
        """
        
        return hdbscan.validity_index(X, labels, metric=metric, d=d, per_cluster_scores=per_cluster_scores, **kwargs)
    
    

# %% ../../notebooks/clustering.ipynb 14
class ButinaClustering(BaseClustering):
    
    """Performs Butina clustering
    
    See original publication at: https://github.com/PatWalters/clusterama
    
    Attributes:

        dataset : list
            A list of SMILES.


    Methods:

        cluster(sim_cutoff:float, nbits:int, radius:int)
            Performs Butina clustering on ´self.dataset´.
            
        get_fps(mol_list:list, nbits:int, radius:int)
            Generate descriptors for ´self.dataset´.
         
        cluster_mols(mol_list, sim_cutoff:float, nbits:int, radius:int)
            Cluster molecules.
        
    

    
    """
    def __init__(self, dataset:List, fp_type="rdkit"):
        self.dataset = dataset
        self.fp_type = fp_type

    def cluster(self,sim_cutoff:float, nbits:int=2048, radius:int=2):
        
        """Run Butina clustering on the dataset
        
        Arguments:


            sim_cutoff : float
                The minimum Tanimoto similarity to consider for putting compounds in the same cluster
                
            nbits : int, optional (default=2048)
                Number of bits of the fingerprints if ´fp_type´ is 'morgan2'
                
            radius : int, optional (default=2)
                Radius of the fingerprints if ´fp_type´ is 'morgan2'
                
                
            
        Returns:

            labels : np.array
                Clustering labels
        
        """        
        
        
        mol_list = [Chem.MolFromSmiles(x) for x in tqdm(self.dataset,desc="Calculating Fingerprints")]
        return self.cluster_mols(mol_list, sim_cutoff, nbits, radius)

    def get_fps(self, mol_list, nbits:int, radius:int):
        
        
        fp_dict = {
            "morgan2" : [AllChem.GetMorganFingerprintAsBitVect(x,radius,nbits) for x in mol_list],
            "rdkit" : [Chem.RDKFingerprint(x) for x in mol_list],
            "maccs" : [MACCSkeys.GenMACCSKeys(x) for x in mol_list],
            "ap" : [Pairs.GetAtomPairFingerprint(x) for x in mol_list]
            }
        if fp_dict.get(self.fp_type) is None:
            raise KeyError(f"No fingerprint method defined for {self.fp_type}")

        return fp_dict[self.fp_type]
    
    def cluster_mols(self, mol_list, sim_cutoff:float, nbits:int, radius:int):
        dist_cutoff = 1.0 - sim_cutoff
        fp_list = self.get_fps(mol_list, nbits, radius)
        dists = []
        nfps = len(fp_list)
        for i in range(1, nfps):
            sims = DataStructs.BulkTanimotoSimilarity(fp_list[i],fp_list[:i])
            dists.extend([1-x for x in sims])
        mol_clusters = Butina.ClusterData(dists,nfps,dist_cutoff,isDistData=True)
        cluster_id_list = [0]*nfps
        for idx,cluster in enumerate(mol_clusters,1):
            for member in cluster:
                cluster_id_list[member] = idx
        self._labels = [x-1 for x in cluster_id_list]
        return self._labels
