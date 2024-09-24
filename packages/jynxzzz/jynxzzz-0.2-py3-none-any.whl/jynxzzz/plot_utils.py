import torch
import matplotlib.pyplot as plt


def plot_func(f, tx=None, ty=None, min=-2, max=2, title=None, figsize=(6, 4)):
    x = torch.linspace(min, max, 100)
    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(x, f(x))
    if title is not None:
        ax.set_title(title)
    if tx is not None:
        ax.set_xlabel(tx)
    if ty is not None:
        ax.set_ylabel(ty)
