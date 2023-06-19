import numpy as np

def spherical_to_cartesian_coordinates(position):
    radius = position[2]
    theta = np.deg2rad(position[0])
    phi = np.deg2rad(position[1])
    
    y = radius * np.sin(theta) * np.cos(phi)
    z = radius * np.sin(theta) * np.sin(phi)
    x = radius * np.cos(theta)

    return x, y, z

def create_sphere_mesh(diameter=1, meshgrid_size=30, offset=[0,0,0]):
    theta = np.linspace(0, 2*np.pi, meshgrid_size)
    phi = np.linspace(0, np.pi, meshgrid_size)

    # Create the meshgrid
    THETA, PHI = np.meshgrid(theta, phi)

    # Convert to cartesian coordinates
    x = diameter*np.sin(PHI)*np.cos(THETA) + offset[0]
    y = diameter*np.sin(PHI)*np.sin(THETA) + offset[1]
    z = diameter*np.cos(PHI) + offset[2]

    return x, y, z

def plot_sphere(axes3d, offset=[0,0,0], diameter=1, meshgrid_size=30, color="red"):
    return axes3d.plot_surface(*create_sphere_mesh(diameter, meshgrid_size, offset), color=color)

def plot_time_series(axis, t, signals, labels,
                     title = None, xlabel = None, ylabel = None, ylim=None, xlim=None):
    if(title):
        axis.set_title(title)
    if(xlabel):
        axis.set_xlabel(xlabel)
    if(ylabel):
        axis.set_ylabel(ylabel)
    if(ylim):
        axis.set_ylim(ylim)
    if(xlim):
        axis.set_xlim(xlim)

    for i in range(len(signals)):
        axis.plot(t, signals[i], label=labels[i])
    axis.legend()

def plot_frequency_domain_magnitude(axis, f, signals, labels,
                                    title=None, xlabel=None, ylabel=None, ylim=None, xlim=None):
    if(title):
        axis.set_title(title)
    if(xlabel):
        axis.set_xlabel(xlabel)
    if(ylabel):
        axis.set_ylabel(ylabel)
    if(ylim):
        axis.set_ylim(ylim)
    if(xlim):
        axis.set_xlim(xlim)

    for i in range(len(signals)):
        axis.semilogx(f, signals[i], label=labels[i])
    axis.legend()