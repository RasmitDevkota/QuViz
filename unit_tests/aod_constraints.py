import numpy as np

import matplotlib.pyplot as plt
import matplotlib.animation as animation

##############################################################
def sign(num):
    return -1 if num < 0 else 1
##############################################################

n_particles = 2
n_movements = 100
step_size = 0.5

positions_initial = [
    np.random.random(size=2) for p in range(n_particles)
]

##############################################################

positions = [positions_initial]
movements = []
positions_x = []
positions_y = []
positions_z = []

for m in range(n_movements):
    positions.append([])
    movements.append([])
    positions_x.append([])
    positions_y.append([])
    positions_z.append([])

    for p in range(n_particles):
        updated_position = positions[-2][p] + (2 * (np.random.random(size=2) - 0.5) * 0.1)
        while updated_position[0] < 0 or updated_position[0] > 1 or updated_position[1] < 0 or updated_position[1] > 1:
            updated_position = positions[-2][p] + (2 * (np.random.random(size=2) - 0.5) * step_size)

        positions[-1].append(updated_position)
        positions_x[-1].append(updated_position[0])
        positions_y[-1].append(updated_position[1])
        positions_z[-1].append(0)

##############################################################

# @TODO - Verify conflicts
for i in range(len(positions) - 1):
    for p in range(n_particles - 1):
        for q in range(p+1, n_particles):
            for c in [0, 1]:
                orientation_before = sign(positions[i][p][c] - positions[i][q][c])
                orientation_after = sign(positions[i+1][p][c] - positions[i+1][q][c])

                if orientation_before != orientation_after:
                    print(f"conflict from frame {i} to frame {i+1}!")

##############################################################

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.set_xlim([-1.5, 1.5])
ax.set_ylim([-1.5, 1.5])

points, = ax.plot([], [], [], 'o')

def update(n):
    print(n)
    points.set_data(np.array([positions_x[n], positions_y[n]]))
    points.set_3d_properties(positions_z[n], "z")

    return points, 

ani = animation.FuncAnimation(fig=fig, func=update, frames=n_movements, interval=100, blit=True, repeat=True)

plt.show()

