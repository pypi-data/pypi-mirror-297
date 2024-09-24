import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import itertools
import numpy as np

def visualize_tesseract():
    """
    Function to visualize a 4D tesseract projected into 3D space.
    """
  
    vertices = list(itertools.product([1, -1], repeat=4))

   
    def project_to_3d(vertex, angle1=0.5, angle2=0.5):
        sin_angle1, cos_angle1 = np.sin(angle1), np.cos(angle1)
        sin_angle2, cos_angle2 = np.sin(angle2), np.cos(angle2)

        x, y, z, w = vertex
        x_new = cos_angle1 * x + sin_angle1 * w
        w_new = -sin_angle1 * x + cos_angle1 * w
        y_new = cos_angle2 * y + sin_angle2 * w_new
        z_new = -sin_angle2 * y + cos_angle2 * w_new

        return [x_new, y_new, z_new]

    projected_vertices = [project_to_3d(vertex) for vertex in vertices]

   
    edges = []
    for i in range(len(vertices)):
        for j in range(i + 1, len(vertices)):
            if sum(a != b for a, b in zip(vertices[i], vertices[j])) == 1:
                edges.append((i, j))

   
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    
    xs, ys, zs = zip(*projected_vertices)
    ax.scatter(xs, ys, zs, color='r')

   
    for edge in edges:
        points = [projected_vertices[edge[0]], projected_vertices[edge[1]]]
        xs, ys, zs = zip(*points)
        ax.plot(xs, ys, zs, color='b')

   
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.title('Tesseract (4D Hypercube) Projection')

    plt.show()


