import bpy
import math

tau = 2 * math.pi

def createMesh(name, verts, edges, faces):
    # create mesh and object
    me = bpy.data.meshes.new(name+'Mesh')
    # Create mesh from give verts, etc
    # either faces or edges should be []
    me.from_pydata(verts, edges, faces)

    # Update mesh with new data
    me.update(calc_edges=True)
    return me

def createPlusMesh(x, y, z):
    verts = []
    for yy in (y/2, y*(-1/2)):
        verts.extend(((-(x+z/2), yy, z/2), (-z/2, yy, z/2), (-z/2, yy, (z/2)+x),
        (z/2, yy, (z/2)+x), (z/2, yy, z/2), ((x+z/2), yy, z/2),
        ((x+z/2), yy, -z/2), (z/2, yy, -z/2), (z/2, yy, -((z/2)+x)),
        (-(z/2), yy, -((z/2)+x)), (-(z/2), yy, -z/2), (-(x+z/2), yy, -z/2)
        ))
    edges = ((0,1),(1,2), (2,3), (3,4), (4,5), (5,6), (6,7), (7,8), (8,9), (9, 10), (10, 11), (11, 0))
    faces = ( (0,1,2,3,4,5,6,7,8,9,10,11)
            , (12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 12)
            , (0, 1, 13, 12)
            , (1, 2, 14, 13)
            , (2, 3, 15, 14)
            , (3, 4, 16, 15)
            , (4, 5, 17, 16)
            , (5, 6, 18, 17)
            , (6, 7, 19, 18)
            , (7, 8, 20, 19)
            , (8, 9, 21, 20)
            , (9, 10, 22, 21)
            , (10, 11, 23, 22)
            , (11, 0, 12, 23)
            )
    mesh = createMesh ('plus', verts, [], faces)
    return mesh

def createObject(name, origin, rotation, me):
    ob = bpy.data.objects.new(name, me)
    ob.location = origin
    ob.rotation_euler = rotation
    ob.show_name = True
    # Link object to scene
    bpy.context.scene.objects.link(ob)
    return ob

def polarPolygonVerts(numSides, radius):
    verts = []
    for n in range (0, numSides):
        verts.append((radius, (tau / numSides)*n))
    return verts

def polarRotate(verts, radians):
    newVerts = []
    for vert in verts:
        newVerts.append((vert[0], vert[1]+radians))
    return newVerts

def polarToCartesian(polarVerts):
    cartesian = []
    for pvert in polarVerts:
        cartesian.append((pvert[0] * math.cos(pvert[1]), 0, pvert[0] * math.sin(pvert[1])))
    return cartesian

def cartesianSubdivide(verts):
    newVerts = []
    numVerts = len(verts)
    for n in range(0,numVerts):
        newVerts.append(verts[n])
        newVerts.append(( (verts[n][0] + verts[(n + 1) % numVerts][0]) / 2
                        , (verts[n][1] + verts[(n + 1) % numVerts][1]) / 2
                        , (verts[n][2] + verts[(n + 1) % numVerts][2]) / 2
                        ))
    return newVerts

def drawSquareTube(name, width, vert1, vert2):
    return

def drawPoly(name, origin, verts):
    edges = []
    numVerts = len(verts)
    for n in range(0, numVerts):
        edges.append((n, (n + 1) % numVerts))
    me = createMesh(name, verts, edges, [])
    createObject(name, origin, me)
    return

def intersectRadius(numSides, radius):
    return ((math.cos(tau/(numSides*2)) / math.cos(tau/(numSides * 4)))  * radius)

def runOld(origin):
    (x,y,z) = (0.707107, 0.258819, 0.965926)
    verts1 = ((x,x,-1), (x, -x, -1), (-x, -x, -1), (-x, x, -1), (0, 0, 1))
    faces1 = ((1,0,4), (4,2,1), (4,3,2), (4,0,3), (0,1,2,3))
    me1 = createMesh('Solid', origin, verts1, [], faces1)
    obj1 = createObject('Solid', origin, me)
    verts2 = ((x, x, 0), (y, -z, 0), (-z, y, 0))
    edges2 = ((1,0), (1,2), (2,0))
    me2 = createMesh('Edgy', verts2, edges2, [])
    ob2 = createObject('Edgy', origin, me)

    # Move second object out of the way
    ob1.select = False
    ob2.select = True
    bpy.ops.transform.translate(value=(0,2,0))
    return

def add_bar(origin, length):
    x = 2.54/200
    y = 2.54/200
    z = length
    verts = [(x, -y, 0), (x, y, 0), (-x, y, 0), (-x, -y, 0),
             (x, -y, z), (x, y, z), (-x, y, z), (-x, -y, z)]
    faces = [(0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    mesh = createMesh('Bar', verts, [], faces)
    ob = createObject('Bar', origin, mesh)
    return ob

def add_joint (origin, angle):
    return

def runBar(origin):
    bpy.ops.object.select_all(action='DESELECT')
    bar = add_bar(origin, 1)
    bar.select = True
    bpy.ops.transform.rotate(value=Math.pi,axis=(1,0,0))
    bar.select = False

def runPolyOld():
    numSides = 6
    radius = 1
    origin = (0,0,0)
    polar = polarPolygonVerts(numSides, radius)
    verts1 = cartesianSubdivide(polarToCartesian(polar))
    verts2 = cartesianSubdivide(polarToCartesian(polarRotate(polar, tau/(numSides * 2))))
    drawPoly('one', (0, -0.25 ,0), verts1)
    drawPoly('two', (0,0.25,0), verts2)
    polarIntersect = polarRotate(polarPolygonVerts(numSides*2, intersectRadius(numSides, radius)), (tau/(numSides*4)))
    drawPoly('intersect', (0,0,0), polarToCartesian(polarIntersect))

def genArch():
    numSides = 6
    radius = 10
    origin = (0,0,0)

    x = 0.5
    y = 0.5
    z = 0.2

    plusMesh = createPlusMesh(x,y,z)

    polarVerts = polarRotate(polarPolygonVerts(numSides, radius), tau/(numSides * 2))
    cartesianVerts = cartesianSubdivide(polarToCartesian(polarVerts))

    bpy.ops.object.select_all(action='DESELECT')
    bpy.types.SpaceView3D.cursor_location =  (0,0,0)

    vert_objs = []

    for i in (range(0,len(cartesianVerts))):
#        obj = createObject('vert ' + str(i), cartesianVerts[i], (tau/4,-(4*tau)/12-(tau/12)*i,0), createPlusMesh())
        obj = createObject('vert ' + str(i), (0,0,0), (0,0,0), plusMesh)

        if (i % 2 == 0):
            bpy.ops.object.add(type='EMPTY')
            empty1 = bpy.context.scene.objects.active
            empty1.name = ("even empty."+str(i)+".1")
            empty1.parent = obj
            empty1.location = (x,0,z/2)
            empty1.select = False

            bpy.ops.object.add(type='EMPTY')
            empty2 = bpy.context.scene.objects.active
            empty2.name = ("even empty."+str(i)+".2")
            empty2.parent = obj
            empty2.location = (-z/2,0,x)
            empty2.select = False

            bpy.ops.object.add(type='EMPTY')
            empty3 = bpy.context.scene.objects.active
            empty3.name = ("even empty."+str(i)+".3")
            empty3.parent = obj
            empty3.location = (-x,0,-z/2)
            empty3.select = False

            bpy.ops.object.add(type='EMPTY')
            empty4 = bpy.context.scene.objects.active
            empty4.name = ("even empty."+str(i)+".4")
            empty4.parent = obj
            empty4.location = (z/2,0,-x)
            empty4.select = False

        else:
            bpy.ops.object.add(type='EMPTY')
            empty1 = bpy.context.scene.objects.active
            empty1.name = ("odd empty."+str(i)+".1")
            empty1.parent = obj
            empty1.location = (x,0,-z/2)
            empty1.select = False

            bpy.ops.object.add(type='EMPTY')
            empty2 = bpy.context.scene.objects.active
            empty2.name = ("odd empty."+str(i)+".2")
            empty2.parent = obj
            empty2.location = (-z/2,0,x)
            empty2.select = False

            bpy.ops.object.add(type='EMPTY')
            empty3 = bpy.context.scene.objects.active
            empty3.name = ("odd empty."+str(i)+".3")
            empty3.parent = obj
            empty3.location = (-x,0,z/2)
            empty3.select = False

            bpy.ops.object.add(type='EMPTY')
            empty4 = bpy.context.scene.objects.active
            empty4.name = ("odd empty."+str(i)+".4")
            empty4.parent = obj
            empty4.location = (z/2,0,-x)
            empty4.select = False

        obj.select = True
        bpy.context.scene.objects.active = obj
        obj.location = cartesianVerts[i]
        obj.rotation_euler = (tau/4,-(4*tau)/12-(tau/12)*i,0)
        bpy.ops.rigidbody.object_add(type='ACTIVE')
        obj.select = False

        vert_objs.append((obj, (empty1, empty2, empty3, empty4)))

#    barBetween((

#        bpy.ops.transform.translate(value=cartesianVerts[i])
#        bpy.ops.transform.rotate(value=(tau/4,-(4*tau)/12-(tau/12)*i,0))

if __name__ == "__main__":
    genArch()
