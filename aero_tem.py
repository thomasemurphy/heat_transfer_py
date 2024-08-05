import numpy as np
import matplotlib.pyplot as plot #import plotting library
from matplotlib import cm #import color for surface plot
import os, sys
import matplotlib.animation as ani #importing animation library

alpha=97 # (mm^2/s) thermal diffusivity, alluminum
#length of sides  of heated square plate
Lx=152 #(mm)
Ly=152 #(mm)
#number of points
N=50 #number of x and y points x*y = total number of points
#Discretize my space
Xvec=np.linspace(0,Lx,N)
Yvec=np.linspace(0,Ly,N)
dx=Xvec[2]-Xvec[1] #since equally spaced, i set a constant dx
dy=Yvec[2]-Yvec[1] #since equally spaced, I set a constant dy
#Discretize time
#dt=0.5*(dx**2)/(2*alpha) #dt needed for stability can do larger however good rule of thumb
dt=0.01
print(dt)
time=15 #sec, how long i want to run the simulations for
tvec=np.linspace(0,1,100) #this is how long i run my numerical approximation. 0 to 100 sec
#Inital Boundary Conditions
T=np.full((Yvec.size,Xvec.size),20.0) #entire plate is at 20 degrees C

T[:,0]=200.0 #200 degrees C applied to left side of plate
T[-1,:]=200.0 #200 degrees C applied to bottom of plate
T[0,:]=200.0 #200 degrees C applied to top of plate
T[:,-1]=200.0 #200 degrees C applied to right side of plate

for i in range (0,frn):
    Told=T


    for ty in range(1,Yvec.size-1):

        for tx in range(1,Xvec.size-1):

            du=(dt*(alpha*(Told[tx+1,ty]-2*Told[tx,ty]+Told[tx-1,ty])/dx**2+alpha*...(Told[tx,ty+1]-2*Told[tx,ty]+Told[tx,ty1])/dy**2)+Told[tx,ty])-T[tx,ty]
            #print(du)

            T[tx,ty]=T[tx,ty]+du

    #img.append((plot.contour(X,Y,T,30)))
    #Tout.append(T)
    Tout[i]=T

def frame(frame_number,Tout,plot):
    plot[0].remove()
    plot[0]=ax1.plot_surface(X,Y,Tout[frame_number,:,:],cmap=cm.jet)

fig = plot.figure()
ax1 = plot.axes(projection="3d")
ax1.set_xlabel('x axis (mm)')
ax1.set_ylabel('y axis (mm)')
ax1.set_zlabel('Temperature (C)')
ax1.set_xlim(0,Lx)
ax1.set_ylim(0,Ly)
ax1.set_zlim(0,200)
x = np.linspace(0, Lx, N)
y = np.linspace(0, Ly, N)
X, Y = np.meshgrid(x, y)
plot1=[ax1.plot_surface(X,Y,Tout[0,:,:])]


#plot=[ax1.plot_surface(X,Y,Tout[:,:,0])]
animation=ani.FuncAnimation(fig,frame,frn,fargs=(Tout,plot1),interval=60,blit=False)
#plot.show()

#save video
#path for ffmpeg using imagemagick
ff_path = os.path.join('C:/', 'ImageMagick-7.0.10-Q16', 'ffmpeg.exe')
plot.rcParams['animation.ffmpeg_path'] = ff_path
#path if i want to convert the .mp4 to a gif
#imgk_path = os.path.join('C:/', 'ImageMagick-7.0.10-Q16', 'convert.exe')
#plot.rcParams['animation.convert_path'] = imgk_path
FFwriter=ani.FFMpegWriter(fps=220) #declar my writer and frame rate
animation.save(os.path.join('C:/','Users','Michael','Desktop','video','tesst.mp4'),writer=FFwriter) #saving function