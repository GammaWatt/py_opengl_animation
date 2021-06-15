import pygame
# from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import math

from tkinter import *

d = { "window": Tk() }
d["window"].title("HYOOME")

lpad = lambda x: " {:2f}".format(x) if x >= 0 else "{:2f}".format(x)

def main():
    frame = Frame(d["window"])
    frame.grid()
    d["window"].update() # spawns tkinter window

    count = 0
    pygame.init()
    pygame.display.set_mode((800,600), pygame.DOUBLEBUF|pygame.OPENGL)

    glEnable(GL_DEPTH_TEST)

    # (this is actually just a quadric passed to the function that actually draws the sphere)
    quadric = gluNewQuadric() # Create new sphere

    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, 800/600, 0.1, 2000) # (fov (in degrees), aspect ratio, near, far)

    glMatrixMode(GL_MODELVIEW)
    gluLookAt(0, -8, 0, 0, 0, 0, 0, 0, 1) # camera options (eyex, eyey, eyez, centerx, centery, centerz, upx, upy, upz)
    viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
    glLoadIdentity()

    # -5 zooms out a little
    # glTranslatef(0.0, 0.0, -5) # x, y, z params for moving arouad the object

    # glRotatef(0, 0, 0, 0)

    spherePosition = {"x": -1.5, "y": 0, "z": 0}

    upz = 1
    upx = 0
    upy = 0

    eyex = 0
    eyey = -8
    eyez = 0

    centerx = 0
    centery = 0
    centerz = 0

    autorotate = False

    cameraOrbitAngle = 0
    rotation = 0
    while True:
        for child in frame.winfo_children():
            child.destroy()

        rotation = rotation + 1 if rotation < 360 else 0
        cameraOrbitAngle = cameraOrbitAngle + 1 if cameraOrbitAngle < 360 else 0
        count += 1
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        if autorotate:
            rad = math.radians(cameraOrbitAngle)
            eyex = math.cos(rad) * -8
            eyey = math.sin(rad) * -8
            cameraOrbitAngle += 1

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(eyex, eyey, eyez, centerx, centery, centerz, upx, upy, upz) # camera options (eyex, eyey, eyez, centerx, centery, centerz, upx, upy, upz)
        viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)

        keypress = pygame.key.get_pressed()
        if keypress[pygame.K_d]:
            spherePosition["x"] += 0.1
        if keypress[pygame.K_a]:
            spherePosition["x"] -= 0.1

        if keypress[pygame.K_w]:
            spherePosition["z"] += 0.1
        if keypress[pygame.K_s]:
            spherePosition["z"] -= 0.1

        if keypress[pygame.K_e]:
            spherePosition["y"] += 0.1
        if keypress[pygame.K_q]:
            spherePosition["y"] -= 0.1

        if keypress[pygame.K_RIGHT]:
            upz += 0.1
        if keypress[pygame.K_LEFT]:
            upz -= 0.1

        if keypress[pygame.K_m]:
            upx += 0.1
        if keypress[pygame.K_n]:
            upx -= 0.1

        if keypress[pygame.K_UP]:
            upy += 0.1
        if keypress[pygame.K_DOWN]:
            upy -= 0.1

        if keypress[pygame.K_t]:
            eyez += 0.1
        if keypress[pygame.K_g]:
            eyez -= 0.1

        if keypress[pygame.K_h]:
            eyex += 0.1
        if keypress[pygame.K_f]:
            eyex -= 0.1

        if keypress[pygame.K_y]:
            eyey += 0.1
        if keypress[pygame.K_r]:
            eyey -= 0.1

        if keypress[pygame.K_i]:
            centerz += 0.1
        if keypress[pygame.K_k]:
            centerz -= 0.1

        if keypress[pygame.K_j]:
            centerx += 0.1
        if keypress[pygame.K_l]:
            centerx -= 0.1

        if keypress[pygame.K_o]:
            centery += 0.1
        if keypress[pygame.K_u]:
            centery -= 0.1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                d["window"].quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                    pygame.quit()
                    d["window"].quit()
                    quit()
                if event.key == pygame.K_p:
                    # KEYDOWN means the event is only triggered once, when key is pressed.
                    # Instead of like a turbo button when held. Like the buttons above
                    # for moving the sphere and camera around.
                    autorotate = not autorotate
                if event.key == pygame.K_BACKSLASH:
                    # Reset camera position
                    upz = 1
                    upx = 0
                    upy = 0
                    eyex = 0
                    eyey = -8
                    eyez = 0
                    centerx = 0
                    centery = 0
                    centerz = 0
                if event.key == pygame.K_EQUALS:
                    # Reset sphere position
                    spherePosition["x"] = -1.5
                    spherePosition["y"] = 0
                    spherePosition["z"] = 0


        # glRotatef(2, 0.3, 0.5, 1)


        # init model view matrix
        glLoadIdentity()

        # init the view matrix
        glPushMatrix()
        glLoadIdentity()

        # multiply the current matrix by the get the new view matrix and store the final vie matrix
        glMultMatrixf(viewMatrix)
        viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)

        # apply view matrix
        glPopMatrix()
        glMultMatrixf(viewMatrix)

        # glRotatef(1, 3, 1, 1)

        # Each object requires its own matrix, so we push a new one onto the stack
        glPushMatrix()

        # glTranslatef(-1.5, 0, 0) #Move to the place
        glTranslatef(spherePosition["x"], spherePosition["y"], spherePosition["z"]) #Move to the place
        glRotatef(-rotation, 0, 0, 1) # rotate
        glColor4f(0.5, 0.2, 0.2, 1) #Put color
        # (quadric, radius, slices, stacks)
        gluSphere(quadric, 1.0, 32, 16) #Draw sphere

        # Since the matrices are stacked
        # Rotations and translations to this one carry over to the ones that get pushed later
        # Hence, why rotating this matrix also rotates the next matrix, making it look like the cylinder is orbiting the sphere

        glPopMatrix()

        # Matrices can be thought of like states.
        # Popping the matrix applies the pushed state to the rendered image.
        # Independent matrices can be treated like independent objects, which, when popped, merge into the rendered image

        # Which means that stacked matrices can be treated like planets, object groups, or parent/child.
        # A pushed matrix is an exact copy of the previous one, so it inherits colors, translations, rotations, etc...
        # Changes to it do not affect the previous/parent matrices.
        # So a stack of matrices could be thought of like a group of objects that will recursively orbit the parent objects.
        # Imagine the first pushed matrix is the sun. Then you push another, which is earth. Then another, which is the moon.
        # All of them are rooted at the sun, and all transformations will be relative to the sun.
        # but if you push one, making it the sun, then another, making it earth, pop, and then push again, you have mars instead of the moon.
        # So, since we popped what we already had, here, (we made the sun, then popped the matrix) we now have two completely independent objects.

        glPushMatrix()

        glTranslatef(2, 0, 0) #Move to the place
        glRotatef(rotation, 0.9, 0.7, 0.3) #Move to the place
        glColor4f(0.5, 0.5, 0.5, 1) #Put color
        # (quadric, baseradius, topradius, height, slices, stacks)
        gluCylinder(quadric, 0.5, 0.1, 0.4, 28, 12) #Draw cylinder

        # Changes to this matrix do not affect earlier matrices.


        glPopMatrix()
        glPolygonMode( GL_FRONT_AND_BACK, GL_LINE ); # makes objects render as wireframes
        # glPolygonMode( GL_FRONT_AND_BACK, GL_FILL ); # Makes objects render normally


        stats = """{}: {} {}: {}
{}: {} {}: {} {}: {}
{}: {} {}: {} {}: {}
{}: {} {}: {} {}: {}
{}: {} {}: {} {}: {}
""".format(
            "count".rjust(11, " "), lpad(count),
            "autorotate".rjust(11, " "), autorotate,
            "eyex".rjust(11, " "), lpad(eyex),
            "eyey".rjust(11, " "), lpad(eyey),
            "eyez".rjust(11, " "), lpad(eyez),
            "centerx".rjust(11, " "), lpad(centerx),
            "centery".rjust(11, " "), lpad(centery),
            "centerz".rjust(11, " "), lpad(centerz),
            "upx".rjust(11, " "), lpad(upx),
            "upy".rjust(11, " "), lpad(upy),
            "upz".rjust(11, " "), lpad(upz),
            "spherex".rjust(11, " "), lpad(spherePosition["x"]),
            "spherey".rjust(11, " "), lpad(spherePosition["y"]),
            "spherez".rjust(11, " "), lpad(spherePosition["z"]),
        )
        Label(frame, text=stats, font="TkFixedFont").pack(side = LEFT)


        d["window"].update() # spawns tkinter window

        pygame.display.flip()
        pygame.time.wait(10)

main()
