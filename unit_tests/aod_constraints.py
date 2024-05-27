import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation

##############################################################

# Helper functions
def sign(num):
    return -1 if num < 0 else 0 if num == 0 else 1

def orientation_str(orientation):
    return "more positive than" if orientation == 1 else "less positive than" if orientation == -1 else "adjacent to"

# Assertions on helper functions
assert(sign(-1) == -1)
assert(sign(0) == 0)
assert(sign(1) == 1)

assert(orientation_str(-1) == "less positive than")
assert(orientation_str(0) == "adjacent to")
assert(orientation_str(1) == "more positive than")

##############################################################

# Enumerating particle positions
setting = "manual"

if setting == "random":
    # Random positions
    n_particles = 100
    n_movements = 100
    step_size = 0.1

    positions_initial = [
        np.random.random(size=2) for _ in range(n_particles)
    ]

    positions = [positions_initial]
    positions_x = []
    positions_y = []
    positions_z = []

    for m in range(n_movements):
        positions.append([])
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
elif setting == "manual":
    # Manually-set movements
    positions = [
        [[0, 0], [1, 0]],
        [[1, 0.5], [2, 0.5]],
        [[1, 1], [2, 0.5]],
        [[1, 1], [0, 1.5]],
    ]

    positions_x = [
        [position[0] for position in positions_i] for positions_i in positions
    ]

    positions_y = [
        [position[1] for position in positions_i] for positions_i in positions
    ]

    positions_z = [
        [0 for _ in positions_i] for positions_i in positions
    ]

    n_particles = 2
    n_movements = len(positions)
    step_size = 0.5

movements = [np.array(positions[i+1]) - np.array(positions[i]) for i in range(n_movements - 1)]

print(movements)

# return

##############################################################

def find_conflicts():
    n_conflicts = 0
    for i in range(len(positions) - 1):
        for p in range(n_particles - 1):
            for q in range(p+1, n_particles):
                for c in [0, 1]:
                    orientation_before = sign(positions[i][p][c] - positions[i][q][c])
                    orientation_after = sign(positions[i+1][p][c] - positions[i+1][q][c])

                    axis_str = "x" if c == 0 else "y"
                    ob_str = "more positive than" if orientation_before == 1 else "less positive than" if orientation_before == -1 else "adjacent to"
                    oa_str = "more positive than" if orientation_after == 1 else "less positive than" if orientation_after == -1 else "adjacent to"

                    print(f"frame {i}: {p} is {ob_str} {q} along {axis_str}, afterwards it is {oa_str} {q}")

                    if orientation_before != orientation_after:
                        print(f"conflict from frame {i} to frame {i+1}!")
                        n_conflicts += 1

    badness = n_conflicts/(n_movements * n_particles * 2)
    return n_conflicts, badness

def correct_conflicts():
    n_conflicts = 0
    corrected_movements = []

    corrected_movements.append(positions[0])

    for i in range(len(positions) - 1):
        conflicts = []
        corrected_movements.append([])

        for p in range(n_particles - 1):
            for q in range(p+1, n_particles):
                needs_correction = False

                for c in [0, 1]:
                    orientation_before = sign(positions[i][p][c] - positions[i][q][c])
                    orientation_after = sign(positions[i+1][p][c] - positions[i+1][q][c])

                    axis_str = "x" if c == 0 else "y"
                    ob_str = "more positive than" if orientation_before == 1 else "less positive than" if orientation_before == -1 else "adjacent to"
                    oa_str = "more positive than" if orientation_after == 1 else "less positive than" if orientation_after == -1 else "adjacent to"

                    print(f"frame {i}: {p} is {ob_str} {q} along {axis_str}, afterwards it is {oa_str} {q}")

                    if orientation_before != orientation_after:
                        print(f"conflict from frame {i} to frame {i+1}!")
                        n_conflicts += 1

                        needs_correction = True
                
                if needs_correction:
                    conflicts.append([i, p, q])
                    
                    for _ in range(p, n_particles):
                        corrected_movements[-1].append(np.array([0, 0]))
                    
                    corrected_movements.append([])

                    corrected_movements[-1].append(movements[i][p])
                else:
                    corrected_movements[-1].append(movements[i][p])

    badness = n_conflicts/(n_movements * n_particles * 2)
    return n_conflicts, badness

# Check for row/column crossings pre-correction
n_conflicts_pre, badness_pre = find_conflicts()
print(f"before correction: {n_conflicts_pre} conflicts found (badness score {badness_pre} conflicts per movement/particle/dimension)")

# Correct!


# Check for row/column crossings post-correction
n_conflicts_post, badness_post = find_conflicts()
print(f"after correction: {n_conflicts_post} conflicts found (badness score {badness_post} conflicts per movement/particle/dimension)")

##############################################################

fig = plt.figure()
ax = fig.add_subplot(projection="3d")
ax.set_xlim([-2, 2])
ax.set_ylim([-2, 2])

points, = ax.plot([], [], [], "o")

def update(n):
    points.set_data(np.array([positions_x[n], positions_y[n]]))
    points.set_3d_properties(positions_z[n], "z")

    return points, 

ani = animation.FuncAnimation(fig=fig, func=update, frames=n_movements, interval=100, blit=True, repeat=False)

plt.show()
