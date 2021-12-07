import numpy as np
import matplotlib.pyplot as plt


def pie(srs, title=""):
    """Plot donut shaped pie chart.

    Args:
        srs (pd.Series): same sign data with labels in index.

    Returns:
        p (Figure): generated plot.
    """
    if srs.min() < 0:
        raise ValueError(f"Negative values in series {srs}")
    # is is dataframe, check one dimension is 1, and squeezee()
    # TODO check if values are all positive or all negative (warn & convert)
    # TODO accept one dimensional dataframes and covert.

    cmap = plt.get_cmap("Dark2")
    clrs = [cmap(i) for i in range(len(srs))]

    r = .7          # circle radious
    lbld = 1.1      # label distance
    pctd = ((r + 1) / 2) * .98    # percent number distance

    fig, ax = plt.subplots(figsize=[8, 10], dpi=100)
    ax.set_title(title)
    names = [i.title() for i in srs.index]

    ax.pie(srs, labels=names, colors=clrs,
            autopct="%1.0f%%", pctdistance=pctd, 
            wedgeprops={'linewidth':7, 'edgecolor':'white'},
            textprops={"fontsize": 17})
    hole = plt.Circle((0,0), r, color="white")
    ax.add_artist(hole)

    plt.show()
    return fig

def bars(srs, title=""):
    # TODO
    # fix multiindex to get good lables
    height = srs
    bars = srs.index
    #print(bars)
    ind = np.arange(len(bars))

    fig, ax = plt.subplots(figsize=[12, 8], dpi=100)

    ax.bar(bars, height, color = (0.5,0.1,0.5,0.6), width=40)

    ax.set_title(title)
    ax.set_xlabel("Time [months]")
    ax.set_ylabel("Amount [€]")
    #ax.set_xticks(ind)
    #ax.legend()

    # Create bars and choose color

    # Add title and axis names
    #plt.xlabel('categories')

    # Create names on the x axis

    # Show graph
    plt.show()
    return

def sbars(df):
    pass
    #stacked bars

if __name__ == "__main__":
    import budget
    budget.main()
