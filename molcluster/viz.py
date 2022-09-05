# AUTOGENERATED! DO NOT EDIT! File to edit: ../notebooks/viz.ipynb.

# %% auto 0
__all__ = ['ChemVisualiser']

# %% ../notebooks/viz.ipynb 2
import pandas as pd

import numpy as np

import matplotlib.pyplot as plt

import seaborn as sns

# %% ../notebooks/viz.ipynb 3
class ChemVisualiser:
    
    def __init__(self, data: pd.core.frame.DataFrame, id_col:str, smiles_col: str):
        self.data = data
        self.id_col = id_col
        self.smiles_col = smiles_col
        
        
        
    def plot_simple_chemical_space(x: str=None, y: str=None, figsize:tuple=(12,9),color_label=None,cmap='Spectral',**kwargs):
        
        x = kwargs.get('x',None)
        y = kwargs.get('y',None)
        xlabel = kwargs.get('xlabel','X')
        ylabel = kwargs.get('ylabel','Y')
        title = kwargs.get('title',None)
        color_label = self.id_col if color_label is None else color_label
        
        # Set context
        sns.set_context('paper',font_scale=2.0)
        sns.set_style('whitegrid')
        
        fig = plt.figure(figsize=figsize)

        
        ax = sns.scatterplot(data=self.data, x=x,y=y, c=color_label, s=point_size, cmap=cmap,**kwargs)
        
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        
        sns.despine(right=True,top=True)
        
        if title:
            plt.title(title,fontweight='bold',fontsize=22)
        
        for i in ax.spines.items():
            i[1].set_linewidth(1.5)
            i[1].set_color('k')
      

        plt.tight_layout()
        
        return fig
        

#     def plot_chemical_space(self, x: str, y: str, labels: str=None, size: str=None, height:int=200, width:int=100):
#         # TODO
# IMPLEMENT INTERACTIVE PLOT with dash
#         raise NotImplementedError
#         # generate a scatter plot
#         fig = px.scatter(self.data, x=x, y=y, color=labels,size=size, **kwargs)

#         # add molecules to the plotly graph - returns a Dash app
#         app = molplotly.add_molecules(fig=fig,
#                                     df=self.data,
#                                     smiles_col=self.smiles_col,
#                                     title_col=id_col)
        
#         # run Dash app inline in notebook (or in an external server). The plotting height is set to 50 + height (recommended by developers)
#         app.run_server(mode='inline', height=50+(height), width=width)

