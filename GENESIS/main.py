import genesis as gs
import threading

# Initialize Genesis
gs.init(backend=gs.cpu)

# Create the scene
scene = gs.Scene(show_viewer=False)  # Disable automatic viewer
plane = scene.add_entity(gs.morphs.Plane())
franka = scene.add_entity(
    gs.morphs.MJCF(file='xml/franka_emika_panda/panda.xml'),
)

scene.build()

# Function to run the simulation in a separate thread
def run_simulation():
    for i in range(1000):
        scene.step()

# Start the simulation in a separate thread
simulation_thread = threading.Thread(target=run_simulation)
simulation_thread.start()

# Explicitly create and initialize the viewer
viewer = gs.Viewer(scene)  # Create the viewer manually
viewer.run()  # Start the viewer