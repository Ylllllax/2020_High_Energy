from astropy.table import Table
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter


def circle(r,center_x,center_y):
    x=[]
    y=[]
    for i in range(4096):
        for j in range(4096):
            if (i-center_x)**2+(j-center_y)**2<=r**2 and (i-center_x)**2+(j-center_y)**2>(r-1)**2:
                x.append(i)
                y.append(j)
            else:
                pass
    return np.array(x),np.array(y)
def event_time(df,r,center_x,center_y):
    x=np.array(df['X'])
    y=np.array(df['Y'])
    value=0.
    for i in range(len(x)):
        if (x[i]-center_x)**2+(y[i]-center_y)**2<=r**2:
            value=value+1.
        else:pass
    return value


if __name__=='__main__':
    sgrb=Table.read(r'D:\LiGuodong\桌面文件\课件\高能天体物理\数据处理\lgrb\lgrb\05001413001_40.fits').to_pandas()
    center_x=1562
    center_y=675
    radiu=40

    x=np.array(sgrb['X'])
    y=np.array(sgrb['Y'])
    PI=np.array(sgrb['PI'])
    data=np.zeros([4096,4096])
    for i in range(len(x)):
        data[x[i]][y[i]]=data[x[i]][y[i]]+1
    circle_x,circle_y=circle(radiu,center_x,center_y)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    im=ax.imshow(data[1000:2000,:1500].T,cmap='Greys',origin='low')
#    im=ax.imshow(data.T,cmap='Greys',origin='low')
    cbar = fig.colorbar(im, ax=ax)
    cbar.minorticks_on()
    im.set_clim(np.percentile(data.flatten(),20),np.percentile(data.flatten(),98))
    plt.scatter(circle_x-1000,circle_y,c='blue',marker='.',s=0.5)
#    plt.scatter(circle_x,circle_y,c='blue',marker='.',s=0.5)
    plt.savefig(r'D:\LiGuodong\桌面文件\课件\高能天体物理\数据处理\sgrb\image1.png')
    
    
    
    time=np.array(sgrb['TIME'])
    a=(time.max()-time.min())/20
    print(a)
    xgrade=np.arange(time.min(),time.max()+50,50.)
    value=[]
    for i in range(1,len(xgrade)):
        df=sgrb[(sgrb['TIME']>=xgrade[i-1]) & (sgrb['TIME']<xgrade[i])]
        value.append(event_time(df,radiu,center_x,center_y))
    value=np.array(value)
    xgrade=xgrade-time[0]
    value_x=(xgrade[:-1]+xgrade[1:])/2.
    fig=plt.figure(figsize=[8,6])
    ax=fig.add_subplot()
    ax.set_xlabel('time(s)',fontsize=12)
    ax.set_ylabel('counts',fontsize=12)
#    ax.scatter(value_x,value,c='blue',marker='o',s=1.5)
    ax.plot(value_x,value,'bo-',linewidth=1,markersize=4)
    plt.savefig(r'D:\LiGuodong\桌面文件\课件\高能天体物理\数据处理\sgrb\Light_curve.png')
    
    source_time=[]
    for i in range(len(x)):
        if (x[i]-center_x)**2+(y[i]-center_y)**2<=radiu**2:
            source_time.append(time[i])
        else:
            pass
    source_time=np.array(source_time)
    plt.hist(source_time-time[0], bins = xgrade)
    plt.savefig(r'D:\LiGuodong\桌面文件\课件\高能天体物理\数据处理\sgrb\histogram.png')
    plt.clf() 
    
    source_PI=[]
    for i in range(len(x)):
        if (x[i]-center_x)**2+(y[i]-center_y)**2<=radiu**2:
            source_PI.append(PI[i])
        else:
            pass
    sta=Counter(source_PI)
    energy_x=np.array(list(sta.keys()))
    energy_y=np.array(list(sta.values()))
    plt.scatter(energy_x,energy_y,c='blue',marker='o',s=1.5)
    plt.xlabel('PI',fontsize=12)
    plt.ylabel('counts',fontsize=12)
    plt.savefig(r'D:\LiGuodong\桌面文件\课件\高能天体物理\数据处理\sgrb\Energy.png')
    
    
    
    
    
    
    
    
    




