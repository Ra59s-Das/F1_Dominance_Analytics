import matplotlib.pyplot as plt
import seaborn as sns

def plot_team_performance(df, x, y, hue, title, save_path=None):
    """Plots team dominance trends."""
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df, x=x, y=y, hue=hue)
    plt.title(title)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.grid(True)
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
    plt.show()
