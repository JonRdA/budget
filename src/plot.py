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
    height = srs
    time = srs.index
    #print(bars)

    fig, ax = plt.subplots(figsize=[12, 8], dpi=100)

    ax.bar(time, height, color = (0.5,0.1,0.5,0.6), width=25)

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
    return fig

def sbars(df, title=""):
    #stacked bars
    time = df.index
    h0 = np.zeros(len(time))

    fig, ax = plt.subplots(figsize=[12, 8], dpi=100)

    for col in df:
        ax.bar(time, df[col], bottom=h0 , width=25, label=col)
        h0 += df[col]



    plt.grid()
    plt.legend()

    ax.set_title(title)
    ax.set_xlabel("Time [months]")
    ax.set_ylabel("Amount [€]")

    plt.show()

if __name__ == "__main__":
    import budget
    budget.main()
