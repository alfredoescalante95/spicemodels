import numpy as np
import subprocess
import sys
import os
import pygame
from pygame.constants import *
from OpenGL.GLU import *
from OpenGL.GL import *

def process_obj(inputfile, displacement=[0,0,0]):
    dx, dy, dz = displacement
    f = open(inputfile)
    outputfile = 'vertex_facet_input_file.obj'
    lines = f.readlines()
    vertex = []
    facets = []
    for line in lines:
        if line[0:2] == 'v ':
            words = line.split("\n")[0].split()
            line = words[0] + ' ' + str(float(words[1])+dx) + ' ' + str(float(words[2])+dy) + ' ' + str(float(words[3])+dz) + '\n'
            vertex.append(line)
        elif line[0] == 'f':
            words = line.split("\n")[0].split()
            if len(words) == 4:
                line = words[0] + ' ' + words[1].split('/')[0] + ' ' + words[2].split('/')[0] + ' ' + words[3].split('/')[0] + '\n'
                facets.append(line)
            elif len(words) == 5:
                line1 = words[0] + ' ' + words[1].split('/')[0] + ' ' + words[2].split('/')[0] + ' ' + words[3].split('/')[0] + '\n'
                line2 = words[0] + ' ' + words[1].split('/')[0] + ' ' + words[3].split('/')[0] + ' ' + words[4].split('/')[0] + '\n'
                facets.append(line1)
                facets.append(line2)
            elif len(words) == 6:
                line1 = words[0] + ' ' + words[1].split('/')[0] + ' ' + words[2].split('/')[0] + ' ' + words[3].split('/')[0] + '\n'
                line2 = words[0] + ' ' + words[1].split('/')[0] + ' ' + words[3].split('/')[0] + ' ' + words[4].split('/')[0] + '\n'
                line3 = words[0] + ' ' + words[1].split('/')[0] + ' ' + words[4].split('/')[0] + ' ' + words[5].split('/')[0] + '\n'
                facets.append(line1)
                facets.append(line2)
                facets.append(line3)
            else:
                raise ValueError('Not supported obj file, only triangles, squares and pentagons supported')
    verfacet = vertex
    for line in facets:
        verfacet.append(line)
    print('number of vertex: ', len(vertex))
    print('number of facets: ', len(facets))
    f = open(outputfile, 'w')
    for item in verfacet:
        f.write("%s" % item)
    print('vertex-facet input file created for DSK generation')
    return outputfile

def create_setupfile(outputfile):
    leapseconds = input('Introduce path for Leapseconds kernel: ')
    frames = input('Introduce path for Frames kernel: ')
    dskname = input('Introduce path for generated DSK: ')
    print('Introduce the following parameters: ')
    surfname = input(' - Surface name: ')
    centername = input(' - Center name: ')
    refframe = input(' - Body reference frame: ')
    distunits = input(' - Units of distance of OBJ file: ')
    naifname = input(' - Naif Surface Name: ')
    naifcode = input(' - Naif Surface Code: ')
    naifbody = input(' - Naif Surface Body (float): ')
    file = open("setup.txt", "w")
    file.write("\\begindata\n")
    file.write("\n")
    file.write("    INPUT_SHAPE_FILE    = '" + outputfile + "'\n")
    file.write("    OUTPUT_DSK_FILE     = '" + dskname + "'\n")
    file.write("    COMMENT_FILE        = ' '\n")
    file.write("    KERNELS_TO_LOAD     = ( '" + leapseconds + "',\n")
    file.write("    					   '" + frames + "')\n")
    file.write("    SURFACE_NAME        = '" + surfname + "'\n")
    file.write("    CENTER_NAME         = '" + centername + "'\n")
    file.write("    REF_FRAME_NAME      = '" + refframe + "'\n")
    file.write("    START_TIME          = '1950-JAN-1/00:00:00'\n")
    file.write("    STOP_TIME           = '2050-JAN-1/00:00:00'\n")
    file.write("    DATA_CLASS          = 1\n")
    file.write("    INPUT_DATA_UNITS    = ( 'ANGLES    = DEGREES'\n")
    file.write("                            'DISTANCES = " + distunits + "' )\n")
    file.write("    COORDINATE_SYSTEM   = 'LATITUDINAL'\n")
    file.write("    MINIMUM_LATITUDE    =  -90.0\n")
    file.write("    MAXIMUM_LATITUDE    =   90.0\n")
    file.write("    MINIMUM_LONGITUDE   = -180.0\n")
    file.write("    MAXIMUM_LONGITUDE   =  180.0\n")
    file.write("    DATA_TYPE           = 2\n")
    file.write("    PLATE_TYPE          = 3\n")
    file.write("    NAIF_SURFACE_NAME   += '" + naifname + "'\n")
    file.write("    NAIF_SURFACE_CODE   += " + naifcode + "\n")
    file.write("    NAIF_SURFACE_BODY   += " + naifbody + "\n")
    file.write("\n")
    file.write("\\begintext\n")
    file.close()
    return

def obj2dsk():
    inputfile = input('Introduce .OBJ file to process: ')
    dx = input('Introduce x displacement (int): ')
    dy = input('Introduce y displacement (int): ')
    dz = input('Introduce z displacement (int): ')
    displacement = [float(dx), float(dy), float(dz)]
    try:
        outputfile = process_obj(inputfile, displacement=displacement)
        print('Processing of OBJ file successful!!')
    except:
        print('Something went wrong.')
    print('creating setup file for DSK generation')
    create_setupfile(outputfile)
    print('setup file created successfully!!')
    print('creating DSK file')
    print('Please, to finish introduce: setup.txt ')
    subprocess.call('mkdsk')
    print('Process finished.')
    return

def dsk2obj(title='', winwidth=1024, winheight=800, plotaxis=0):
    """
    :param title: title to be displayed in the visualization window
    :type title: str
    :param winwidth: width of the visualization window. Example: 1200
    :type winwidth: int
    :param winheight: height of the visualization window. Example: 900
    :type winheight: int
    :param plotaxis: if set equal to 1, it displays a reference frame in the visualization window
    :type plotaxis: int

    :return:
    """

    inputfile = input('Introduce input file name: ')
    filename = input('Introduce output file name: ')
    factor = int(input('Factor to dimension the displayed model: '))
    zpos = 3  # like distance from camera to object

    generateOBJ = "dskexp -dsk " + inputfile + " -text " + filename + " -format obj -prec 10"

    command = (generateOBJ)
    os.system(command)

    pygame.init()
    viewport = (winwidth, winheight)
    hx = viewport[0] / 2
    hy = viewport[1] / 2
    pygame.display.set_mode((winwidth, winheight), pygame.DOUBLEBUF | pygame.OPENGL)
    pygame.display.set_caption(title)

    # Function checker
    glDisable(GL_TEXTURE_2D)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glEnable(GL_CULL_FACE)
    #
    glMatrixMode(GL_PROJECTION)
    gluPerspective(90.0, float(800) / 600, 1, 1000.)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # LOAD OBJECT AFTER PYGAME INIT
    obj = OBJ(filename, factor)

    if plotaxis == 1:
        xaxis = OBJax('xaxis.obj', 1.0, 0.0, 0.0, -1, -2, 2, factor)
        yaxis = OBJax('yaxis.obj', 0.0, 1.0, 0.0, -1, -2, 2, factor)
        zaxis = OBJax('zaxis.obj', 0.0, 0.0, 1.0, -1, -2, 2, factor)

    clock = pygame.time.Clock()

    rx, ry = (0, 0)
    tx, ty = (0, 0)
    rotate = move = False
    while 1:
        clock.tick(30)
        # print(tx, ty, rx, ry, zpos)
        for e in pygame.event.get():
            if e.type == QUIT:
                sys.exit()
            elif e.type == KEYDOWN and e.key == K_ESCAPE:
                sys.exit()
            elif e.type == MOUSEBUTTONDOWN:
                if e.button == 4:
                    zpos = max(1, zpos - 1)
                elif e.button == 5:
                    zpos += 1
                elif e.button == 1:
                    rotate = True
                elif e.button == 3:
                    move = True
            elif e.type == MOUSEBUTTONUP:
                if e.button == 1:
                    rotate = False
                elif e.button == 3:
                    move = False
            elif e.type == MOUSEMOTION:
                i, j = e.rel
                if rotate:
                    rx += i
                    ry += j
                if move:
                    tx += i
                    ty -= j

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glClearColor(0.902, 0.902, 1, 0.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # RENDER OBJECT
        glTranslate(tx / 20., ty / 20., - zpos)
        glRotate(ry, 1, 0, 0)
        glRotate(rx, 0, 1, 0)
        glCallList(obj.gl_list)
        if plotaxis == 1:
            glCallList(xaxis.gl_list)
            glCallList(yaxis.gl_list)
            glCallList(zaxis.gl_list)

        pygame.display.flip()

    return

class OBJ:
    def __init__(self, filename, factor, swapyz=False):
        """Loads a Wavefront OBJ file. """
        self.vertices = []
        self.normals = []
        self.faces = []

        material = None
        for line in open(filename, "r"):
            if line.startswith('#'): continue
            values = line.split()
            if not values: continue
            if values[0] == 'v':
                values[1] = str(factor * float(values[1]))
                values[2] = str(factor * float(values[2]))
                values[3] = str(factor * float(values[3]))
                v = list(map(float, values[1:4]))
                if swapyz:
                    v = v[0], v[2], v[1]
                self.vertices.append(v)
            elif values[0] == 'f':
                face = []
                norms = []
                for v in values[1:]:
                    w = v.split('/')
                    face.append(int(w[0]))
                self.faces.append(face)

        self.gl_list = glGenLists(1)
        glNewList(self.gl_list, GL_COMPILE)
        glDisable(GL_TEXTURE_2D)
        glFrontFace(GL_CCW)

        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glBegin(GL_TRIANGLES)
        for face in self.faces:
            for f in face:
                vertexDraw = self.vertices[int(f) - 1]
                if int(f) % 3 == 1:
                    glColor4f(0.282, 0.239, 0.545, 0.35)
                elif int(f) % 3 == 2:
                    glColor4f(0.329, 0.333, 0.827, 0.35)
                else:
                    glColor4f(0.345, 0.300, 0.145, 0.35)
                glVertex3fv(vertexDraw)
        glEnd()
        glDisable(GL_TEXTURE_2D)
        glEndList()

class OBJax:
    def __init__(self, filename, R, G, B, X0, Y0, Z0, factor, swapyz=False):
        """Loads a Wavefront OBJ file. """
        self.vertices = []
        self.normals = []
        self.faces = []

        material = None
        for line in open(filename, "r"):
            if line.startswith('#'): continue
            values = line.split()
            if not values: continue
            if values[0] == 'v':
                values[1] = str(X0 + factor*float(values[1]))
                values[2] = str(Z0 + factor* float(values[2]))
                values[3] = str(Y0 + factor* float(values[3]))
                v = list(map(float, values[1:4]))
                if swapyz:
                    v = v[0], v[2], v[1]
                self.vertices.append(v)
            elif values[0] == 'f':
                face = []
                norms = []
                for v in values[1:]:
                    w = v.split('/')
                    face.append(int(w[0]))
                self.faces.append(face)

        self.gl_list = glGenLists(1)
        glNewList(self.gl_list, GL_COMPILE)
        glDisable(GL_TEXTURE_2D)
        glFrontFace(GL_CCW)

        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glBegin(GL_TRIANGLES)
        for face in self.faces:
            for f in face:
                vertexDraw = self.vertices[int(f) - 1]
                if int(f) % 3 == 1:
                    glColor4f(R, G, B, 0.35)
                elif int(f) % 3 == 2:
                    glColor4f(R, G, B, 0.35)
                else:
                    glColor4f(R, G, B, 0.35)
                glVertex3fv(vertexDraw)
        glEnd()
        glDisable(GL_TEXTURE_2D)
        glEndList()
