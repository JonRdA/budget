import datetime
import numpy as np
import matplotlib.pyplot as plt

#cmap = plt.get_cmap("Dark2")
#clrs = [cmap(i) for i in range(len(srs))]

def initax(func):
    """Decorator for plot drawing functions to initialize an asex if not passed.

    Checks if an axes is passes as a keyword argument. If not it creates ones
    and passes it to the function to plot on it.
    """
    def wrapper(*args, **kwargs):
        if "ax" not in kwargs.keys():
            _, ax = plt.subplots(figsize=(16, 9))
            return func(*args, ax, **kwargs)
        else:
            return func(*args, **kwargs)
    return wrapper
            


@initax
def pie(srs, ax=None):
    """Plot donut shaped pie chart.

    Args:
        ax (AxesSubplot): axes in which to plot.
        srs (pd.Series): same sign data with labels in index.
    """
    if (srs < 0).all():
        srs = -srs

    # Pie parameters, distances.
    r = .7          # circle radious
    lbld = 1.1      # label distance
    pctd = ((r + 1) / 2) * .98    # percent number distance

    
    names = [i.title() for i in srs.index]

    ax.pie(srs, labels=names,#colors=clrs,
            autopct="%1.0f%%", pctdistance=pctd, 
            wedgeprops={'linewidth':7, 'edgecolor':'white'})

    hole = plt.Circle((0,0), r, color="white")
    ax.add_artist(hole)

@initax
def bar(srs, ax=None, days=30):
    """Bar plotting for timeline & breakdown report of transactions.

    Args:
        ax (AxesSubplot): axes in which to plot.
        srs (pd.Series): transaction summary timeline with DatetimeIndex.
        days (int): report resampling frequency in days for bar width.
    """
    x = srs.index
    w = .8

    # Correction for timeline report. Bar at beginning of freq & set width.
    if srs.index.inferred_type=="datetime64":
        x = x - datetime.timedelta(days)
        w *= days
    if (srs <= 0).all():
        ax.invert_yaxis()

    ax.bar(x, srs, w)

@initax
def sbar(df, ax=None,  days=30):
    """Stacked bar plotting for timeline report of multiple categories.

    Args:
        ax (AxesSubplot): axes in which to plot.
        df (pd.DataFrame): transaction summary timeline with DatetimeIndex.
        days (int): report resampling frequency in days for bar width.
    """
    df = df.fillna(0)
    x = df.index - datetime.timedelta(days)
    w = .8 * days
    h0 = np.zeros(len(x))

    for col in df:
        ax.bar(x, df[col], bottom=h0 , width=w, label=col)
        h0 += df[col]
        
    if (df <= 0).all().all():
        ax.invert_yaxis()

    ax.legend()


if __name__ == "__main__":
    import budget
    budget.main()
