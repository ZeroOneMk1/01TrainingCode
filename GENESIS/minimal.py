import genesis as gs
gs.init(backend=gs.cpu)
scene = gs.Scene(show_viewer=True)
scene.build()
scene.viewer.start()