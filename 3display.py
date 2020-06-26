import pyglet
import ratcave as rc
from headposition import getFace
# from facerec import getFace
import threading
import time
import math

# window = pyglet.window.Window(fullscreen=True)
window = pyglet.window.Window(resizable=True)
# window.maximize()


@window.event
def on_draw():
  with rc.default_shader:
      scene.draw()


def update(dt):
    pass
pyglet.clock.schedule(update)


# def rotate_meshes(dt):
#     octo.rotation.x += 40 * dt  # dt is the time between frames
#     # torus.rotation.x += 80 * dt
#     # print(octo.rotation.y, dt)
# pyglet.clock.schedule(rotate_meshes)
#
# def inout_meshes(dt, rate = [10]):
#     octo.position.z += rate[0] * dt
#     print(octo.position.z)
#     if octo.position.z > -3:
#         rate[0] = -10
#     elif octo.position.z < -6:
#         rate[0] = 10
# pyglet.clock.schedule(inout_meshes)


from pyglet.window import key
keys = key.KeyStateHandler()
window.push_handlers(keys)

def move_camera(dt):
    camera_speed = 9
    if keys[key.LEFT]:
        scene.camera.position.x -= camera_speed * dt
    if keys[key.RIGHT]:
        scene.camera.position.x += camera_speed * dt
    if keys[key.DOWN]:
        scene.camera.position.y -= camera_speed * dt
    if keys[key.UP]:
        scene.camera.position.y += camera_speed * dt
pyglet.clock.schedule(move_camera)

def update(model, data):
    smooth = [0,0,0]
    rate = 1/4
    while True:
        smooth = [smooth[i]+ (data[0][i]-smooth[i])*rate for i in range(3)]
        model.rotation.x = -smooth[1]*5+25
        model.rotation.y = -smooth[0]
        # model.position.z = -2 # -data[0][2]/1000
        # model.position.z = -math.sqrt(18000-smooth[2])/100
        # print(smooth[2])
        time.sleep(.05)


if __name__ == "__main__":
    # print('yea')
    holder = [0]
    t1 = threading.Thread(target=getFace, args=(holder, ), daemon=True)
    t1.start()

    # print('yea')
    while not holder[0]:
        time.sleep(.1)
        print(holder)

    # print('yea')
    # # Insert filename into WavefrontReader.
    obj_filename = rc.resources.obj_primitives
    obj_reader = rc.WavefrontReader(obj_filename)
    # # Check which meshes can be found inside the Wavefront file, and extract it into a Mesh object for rendering.
    print(obj_reader.bodies.keys())
    objmesh = obj_reader.get_mesh('MonkeySmooth', scale = .7)

    # model = obj_filename
    # model = "models/dice.obj"
    # obj = rc.WavefrontReader(model)
    # print(obj.bodies.keys())

    # objmesh = obj.get_mesh("Dice", scale=.6)
    objmesh.position.xyz = 0,0, -2
    scene = rc.Scene(meshes=objmesh)

    # time.sleep(.1)
    t2 = threading.Thread(target=update, args=(objmesh,holder,))
    t2.start()

    pyglet.app.run()



