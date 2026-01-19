import genesis as gs
import threading

# Initialize Genesis
gs.init(backend=gs.gpu) # uses Metal on MacOS

# Create the scene
scene = gs.Scene()

scene.build()

# Function to run the simulation in a separate thread
def run_simulation(scene):
    for i in range(1000):
        scene.step()

# Start the simulation in a separate thread
simulation_thread = threading.Thread(target=run_simulation, args=(scene,))
simulation_thread.start()

# Start the viewer
scene.viewer.start()