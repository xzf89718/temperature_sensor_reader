import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def to_percent(temp, position):
    return "{:.2f}%".format(temp * 100)


def makeCurve(X, Ys, legends, xlabel, ylabel, title, outfile="MUX64BatchTest.png", make_percentage=False, make_scatter=False, xlim=None, ylim=None, Xerror=None, Yerrors=None, fontsize=10):
    """

    """
    fig, ax = plt.subplots()
    if legends == None:
        for Y in Ys:
            if(make_scatter):
                ax.scatter(X, Y)
            else:
                ax.plot(X, Y, linewidth=2, markersize=12)
    else:
        for legend, Y in zip(legends, Ys):
            if(make_scatter):
                ax.scatter(X, Y, label=legend)
            else:
                ax.plot(X, Y, linewidth=2, markersize=12, label=legend)

    if(make_percentage):
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(to_percent))
    mylegend = ax.legend(fontsize=fontsize)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    if (xlim is not None):
        ax.set_xlim(xlim)
    if (ylim is not None):
        ax.set_ylim(ylim)
    fig.savefig(outfile)
    plt.close(fig=fig)

def makeTemperatureAndHumidity(list_time, list_temp, list_humidity, figsize=(100, 30), title=None, outfile="temperature_humidity.png"):
    fig, ax = plt.subplots(2, 1, figsize=figsize)
    # plot temperature at ax[0]
    ax[0].set_ylabel("Temperature/$^\circ$C")
    ax[0].set_xlim(list_time[0], list_time[-1])
    # ax[0].set_xlabel("Time")
    ax[0].plot(list_time, list_temp, label="Temperature")
    # plot humidity at ax[1]
    ax[1].set_ylabel("Relative humidity/%")
    ax[1].set_xlim(list_time[0], list_time[-1])
    ax[1].set_xlabel("Time")
    ax[1].plot(list_time, list_humidity, label="Humidity")
    fig.savefig(outfile)
    plt.close(fig=fig)

