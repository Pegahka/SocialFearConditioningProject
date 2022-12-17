from matplotlib.patches import PathPatch
import numpy as np

def significance(axis, tick_value, data_ratio, max_value, text='***',offset=0.10,fontsize=14,whisker=0.06):
    hanbun_min = tick_value - data_ratio/2
    hanbun_max = tick_value + data_ratio/2
    axis.text(tick_value,max_value+0.12,text,bbox={'facecolor':'white','alpha':0,'edgecolor':'none','pad':0.8},
          ha='center', va='center',fontsize=fontsize)
    axis.plot([hanbun_min,hanbun_max],[max_value+offset-0.03,max_value+offset-0.03],'k',linewidth=1)
    axis.plot([hanbun_min,hanbun_min],[max_value+offset-0.03,max_value+offset-whisker],'k',linewidth=1)
    axis.plot([hanbun_max,hanbun_max],[max_value+offset-0.03,max_value+offset-whisker],'k',linewidth=1)


def adjust_box_widths(g, fac):
    """
    Adjust the withs of a seaborn-generated boxplot.
    """
    # iterating through Axes instances
    for ax in g.axes:

        # iterating through axes artists:
        for c in ax.get_children():

            # searching for PathPatches
            if isinstance(c, PathPatch):
                # getting current width of box:
                p = c.get_path()
                verts = p.vertices
                verts_sub = verts[:-1]
                xmin = np.min(verts_sub[:, 0])
                xmax = np.max(verts_sub[:, 0])
                xmid = 0.5*(xmin+xmax)
                xhalf = 0.5*(xmax - xmin)

                # setting new width of box
                xmin_new = xmid-fac*xhalf
                xmax_new = xmid+fac*xhalf
                verts_sub[verts_sub[:, 0] == xmin, 0] = xmin_new
                verts_sub[verts_sub[:, 0] == xmax, 0] = xmax_new

                # setting new width of median line
                for l in ax.lines:
                    if np.all(l.get_xdata() == [xmin, xmax]):
                        l.set_xdata([xmin_new, xmax_new])

