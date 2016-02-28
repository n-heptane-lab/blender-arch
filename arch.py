import bpy
import math
from mathutils.geometry import intersect_line_line

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

def createPlusMesh(connectorWidth, connectorThickness, connectorLength):
    verts = []
    iv = connectorThickness/2
    ov = connectorLength+iv
    for x in (-(connectorWidth/2), connectorWidth/2):
        verts.extend(((x, ov, iv) ,  (x, iv, iv),   (x, iv, ov),
                      (x, -iv, ov),  (x, -iv, iv),  (x, -ov, iv),
                      (x, -ov, -iv), (x, -iv, -iv), (x, -iv, -ov),
                      (x, iv, -ov),   (x, iv, -iv),  (x, ov, -iv)))

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

def createPlusMesh2(x, y, z):
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

def createBarMesh(width, depth, length):
    x = width / 2
    y = depth / 2
    z = length
    verts = [(x, -y, 0), (x, y, 0), (-x, y, 0), (-x, -y, 0),
             (x, -y, z), (x, y, z), (-x, y, z), (-x, -y, z)
             ]
#    faces = [(0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    faces = [(3, 0, 4, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), ]
    mesh = createMesh('Bar', verts, [], faces)
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

def polarToCartesianConnectors(connectors):
    for connector in connectors:
        connector['cartCoord'] = (connector['polarCoord']['r'] * math.cos(connector['polarCoord']['theta']), connector['y'], connector['polarCoord']['r'] * math.sin(connector['polarCoord']['theta']))

#        cartesian.append('cartCoord' : (pvert['polarCoord'][0] * math.cos(pvert['polarCoord'][1]), 0, pvert['polarCoord'][0] * math.sin(pvert['polarCoord'][1])),
#                         'rotation'  : pvert['rotation']);

    return

def rotateConnectors(connectors, offset):
    for connector in connectors:
        connector['polarCoord']['theta'] = connector['polarCoord']['theta'] + offset
        connector['rotation'] = connector['rotation'] - offset
    return

def translateConnectors(connectors, offset):
    for connector in connectors:
        connector['y'] = connector['y'] + offset
    return

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

def genPolarConnectorVerts(name, numSides, apothem, radius):
    verts = []
    for n in range (0, numSides):
        verts.append({ 'type' : 'apothem', 'name' : ((str(2*n))), 'polarCoord' : { 'r' : apothem, 'theta' : ((tau / (numSides*2))*(2*n)) } , 'y' : 0, 'rotation' : (tau - (tau / (numSides*2))*(2*n)) })
        verts.append({ 'type' : 'radius', 'name' : (str((2*n)+1)), 'polarCoord' : { 'r' : radius, 'theta' : ((tau / (numSides*2))*((2*n)+1)) }, 'y' : 0, 'rotation' : (tau - (tau / (numSides*2))*((2*n)+1)) })
    return verts

def createPlusObjs(name, connectors, barWidth, connectorWidth, connectorLength):
    # ensure that nothing is select and the 3D cursor is at the origin
    bpy.ops.object.select_all(action='DESELECT')
    bpy.types.SpaceView3D.cursor_location =  (0,0,0)

    hc = connectorLength/2
    hd  = connectorWidth/2

    for connector in connectors:
        plusMesh = createPlusMesh(barWidth, connectorWidth, connectorLength)
        obj = createObject(name + '.' + 'vert ' + connector['name'], (0,0,0), (0,0,0), plusMesh)
        if (connector['type'] == 'apothem'):
            bpy.ops.object.add(type='EMPTY')
            hinge1 = bpy.context.scene.objects.active
            hinge1.name = ("even hinge."+connector['name']+".1")
            hinge1.parent = obj
            hinge1.location = (0,-hd, -hc)
            hinge1.rotation_euler = (tau/4, 0, 0)
            bpy.ops.rigidbody.constraint_add(type='HINGE')
            hinge1.select = False

            bpy.ops.object.add(type='EMPTY')
            hinge2 = bpy.context.scene.objects.active
            hinge2.name = ("even hinge."+connector['name']+".2")
            hinge2.parent = obj
            hinge2.location = (0, -hc, hd)
            hinge2.rotation_euler = (tau/4, 0, 0)
            bpy.ops.rigidbody.constraint_add(type='HINGE')
            hinge2.select = False

            bpy.ops.object.add(type='EMPTY')
            hinge3 = bpy.context.scene.objects.active
            hinge3.name = ("even hinge."+connector['name']+".3")
            hinge3.parent = obj
            hinge3.location = (0, hd, hc)
            hinge3.rotation_euler = (tau/4, 0, 0)
            bpy.ops.rigidbody.constraint_add(type='HINGE')
            hinge3.select = False

            bpy.ops.object.add(type='EMPTY')
            hinge4 = bpy.context.scene.objects.active
            hinge4.name = ("even hinge."+connector['name']+".4")
            hinge4.parent = obj
            hinge4.location = (0, hc, hd)
            hinge4.rotation_euler = (tau/4, 0, 0)
            bpy.ops.rigidbody.constraint_add(type='HINGE')
            hinge4.select = False

        else:
            bpy.ops.object.add(type='EMPTY')
            hinge1 = bpy.context.scene.objects.active
            hinge1.name = ("odd hinge."+connector['name']+".1")
            hinge1.parent = obj
            hinge1.location = (0, hd, -hc)
            hinge1.rotation_euler = (tau/4, 0, 0)
            bpy.ops.rigidbody.constraint_add(type='HINGE')
            hinge1.select = False

            bpy.ops.object.add(type='EMPTY')
            hinge2 = bpy.context.scene.objects.active
            hinge2.name = ("odd hinge."+connector['name']+".2")
            hinge2.parent = obj
            hinge2.location = (0, -hc, hd)
            hinge2.rotation_euler = (tau/4, 0, 0)
            bpy.ops.rigidbody.constraint_add(type='HINGE')
            hinge2.select = False

            bpy.ops.object.add(type='EMPTY')
            hinge3 = bpy.context.scene.objects.active
            hinge3.name = ("odd hinge."+connector['name']+".3")
            hinge3.parent = obj
            hinge3.location = (0,-hd, hc)
            hinge3.rotation_euler = (tau/4, 0, 0)
            bpy.ops.rigidbody.constraint_add(type='HINGE')
            hinge3.select = False

            bpy.ops.object.add(type='EMPTY')
            hinge4 = bpy.context.scene.objects.active
            hinge4.name = ("odd hinge."+connector['name']+".4")
            hinge4.parent = obj
            hinge4.location = (0, hc, -hd)
            hinge4.rotation_euler = (tau/4, 0, 0)
            bpy.ops.rigidbody.constraint_add(type='HINGE')
            hinge4.select = False

        obj.select = True
        bpy.context.scene.objects.active = obj
        obj.location = connector['cartCoord']
        obj.rotation_euler = (0, connector['rotation'], 0)
#        obj.rotation_euler = (tau/4,-(4*tau)/12-(tau/12)*i,0)
        bpy.ops.rigidbody.object_add(type='ACTIVE')
        bpy.ops.rigidbody.shape_change(type='MESH')
        obj.select = False
        connector['object'] = obj
        connector['hinge1'] = hinge1
        connector['hinge2'] = hinge2
        connector['hinge3'] = hinge3
        connector['hinge4'] = hinge4

def linkConnectors(name, connectors, barWidth, barDepth, barLength):
    bpy.ops.object.select_all(action='DESELECT')

#    bpy.types.SpaceView3D.cursor_location =  (0,0,-10)
    for i in (range(0, len(connectors))):
        nextI = (i+1)%len(connectors)
        x = connectors[i]['hinge3'].matrix_world[0][3]
        y = connectors[i]['hinge3'].matrix_world[1][3]
        if (i % 2 == 0):
         y = y + barWidth/2
        else:
         y = y - barWidth/2

        z   = connectors[i]['hinge3'].matrix_world[2][3]
        barMesh = createBarMesh(barWidth, barDepth, barLength)
        obj = createObject(name +'.bar ' + str(i), (0,0,0), (0,0,0), barMesh)
        connectors[i]['bar1']     = obj
        connectors[nextI]['bar2'] = obj
        obj.select = True
        bpy.context.scene.objects.active = obj
        bpy.ops.rigidbody.object_add(type='ACTIVE')
        bpy.ops.rigidbody.shape_change(type='MESH')
        if (i == 0):

#        bpy.types.SpaceView3D.cursor_location =  (0.0,0.0,0.0)
            bpy.context.scene.cursor_location = (0.0,0.0,barWidth/2)
            bpy.ops.object.mode_set(mode = 'OBJECT')
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        obj.select = False
        obj.location       = (x,y,z)
#        print(connectors[(i+1)%(len(connectors))]['hinge1'].matrix_world[2][3] - connectors[i]['hinge3'].matrix_world[2][3])
        angle = math.atan2((connectors[nextI]['hinge1'].matrix_world[2][3] - connectors[i]['hinge3'].matrix_world[2][3]),
                           (connectors[nextI]['hinge1'].matrix_world[0][3] - connectors[i]['hinge3'].matrix_world[0][3]))
        print(angle)
        obj.rotation_euler = (0.0, (tau/4)-angle, 0.0)
        connectors[i]['hinge3'].rigid_body_constraint.disable_collisions = False
        connectors[i]['hinge3'].rigid_body_constraint.object1     = obj
        connectors[i]['hinge3'].rigid_body_constraint.object2     = connectors[i]['object']
        connectors[nextI]['hinge1'].rigid_body_constraint.disable_collisions = False
        connectors[nextI]['hinge1'].rigid_body_constraint.object1 = obj
        connectors[nextI]['hinge1'].rigid_body_constraint.object2 = connectors[nextI]['object']

def linkLayers(layer1, layer2):
    for i in range(0, len(layer1)):
        nextI = (i + 1)%len(layer1)
        nextII = (i + 2)%len(layer1)
        a = mathutils.Vector((layer2[i]['hinge3'].matrix_world[0][3]     , layer2[i]['y'], layer2[i]['hinge3'].matrix_world[2][3]))
        b = mathutils.Vector((layer2[nextI]['hinge1'].matrix_world[0][3] , layer2[i]['y'], layer2[nextI]['hinge1'].matrix_world[2][3]))
        c = mathutils.Vector((layer1[nextI]['hinge3'].matrix_world[0][3] , layer2[i]['y'], layer1[nextI]['hinge3'].matrix_world[2][3]))
        d = mathutils.Vector((layer1[nextII]['hinge1'].matrix_world[0][3], layer2[i]['y'], layer1[nextII]['hinge1'].matrix_world[2][3]))
        print(a, b, c, d)
        (v1, v2) = intersect_line_line(a, b, c, d)
        print (v1, v2)

        bpy.ops.object.select_all(action='DESELECT')
        bpy.types.SpaceView3D.cursor_location =  (0,0,0)
        bpy.ops.object.add(type='EMPTY')
        hinge = bpy.context.scene.objects.active
        hinge.name = ("mid hinge")
        hinge.location = v1
        hinge.rotation_euler = (tau/4,0,0)
        bpy.ops.rigidbody.constraint_add(type='HINGE')
        hinge.rigid_body_constraint.disable_collisions = False
        hinge.rigid_body_constraint.object1     = layer1[nextI]['bar1']
        hinge.rigid_body_constraint.object2     = layer2[nextI]['bar2']
        hinge.select = False

def crossLinkLayers(name, connectors1, connectors2, connectors3, connectors4, radiusMinusApothem, barWidth, barDepth, barLength):
    for i in range(0, len(connectors1)):
        nextI = (i+1)%len(connectors1)
        nextII = (i + 2)%len(connectors1)
        barMesh = createBarMesh(barWidth, barDepth, barLength)
        barObj = createObject(name+'.crossbar '+str(i), (0,0,0), (0,0,0), barMesh)
        connectors1[i]['bar1']     = barObj
        barObj.select = True
        bpy.context.scene.objects.active = barObj
        bpy.ops.rigidbody.object_add(type='ACTIVE')
        bpy.ops.rigidbody.shape_change(type='MESH')
        if (i == 0):
            bpy.context.scene.cursor_location = (0.0, 0.0, barWidth/2)
            bpy.ops.object.mode_set(mode = 'OBJECT')
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        barObj.select = False

        angle = math.atan2((connectors1[nextI]['hinge1'].matrix_world[2][3] - connectors1[i]['hinge3'].matrix_world[2][3]),
                           (connectors1[nextI]['hinge1'].matrix_world[0][3] - connectors1[i]['hinge3'].matrix_world[0][3]))

        x = connectors1[i]['hinge4'].matrix_world[0][3]
        y = connectors1[i]['hinge4'].matrix_world[1][3]
        z = connectors1[i]['hinge4'].matrix_world[2][3]
#        if (i % 2 == 0):
#         y = y + barWidth/2
#        else:
#         y = y - barWidth/2

        barObj.location = (x, y, z)
        barObj.rotation_euler = (-(tau/4)-(tau/24), connectors1[i]['rotation']+(tau/4), 0.0)
    return

def genArch():
    # settings
    barLength      = 60
    barWidth       = 1
    connectorWidth = 0.25
    rotationSafety = 0.25
    numSides       = 6

    # calculated values
    connectorLength = (barWidth * math.sqrt(2) + (connectorWidth / 2) + rotationSafety) * 2

    polarAngle          = tau/(numSides * 2)
    interiorAngle       = ((tau/2) * (numSides - 2)) / numSides
    connectorHypotenuse = connectorLength / (math.sin(interiorAngle / 2))
    connectorAdjacent   = connectorLength / (math.tan(interiorAngle / 2))
#    virtualSideLength   = (barLength - barWidth) + connectorLength + connectorHypotenuse
#    virtualSideLength   = (barLength - (4*barWidth)) + (2 * connectorHypotenuse)
    virtualSideLength    = (barLength - ((barWidth / 2) * 2)) + connectorHypotenuse
    apothem             = virtualSideLength / math.tan((tau/numSides)/2)
    radius              = (virtualSideLength / math.sin((tau/numSides)/2)) - connectorAdjacent

    # layer 1
    # generate geometry
    connectors1 = genPolarConnectorVerts('layer1', numSides, apothem, radius)
    polarToCartesianConnectors(connectors1)

    # place connectors
    createPlusObjs('layer1', connectors1, barWidth, connectorWidth, connectorLength)

    # add bars
    linkConnectors('layer1', connectors1, barWidth, barWidth, barLength)

    # layer 2
    # generate geometry
    connectors2 = genPolarConnectorVerts('layer2', numSides, apothem, radius)
    rotateConnectors(connectors2, tau/(numSides*2))
    polarToCartesianConnectors(connectors2)

    # place connectors
#    plusMesh = createPlusMesh(barWidth, connectorWidth, connectorLength)
    createPlusObjs('layer2', connectors2, barWidth, connectorWidth, connectorLength)

    # add bars
#    barMesh = createBarMesh(barWidth, barWidth, barLength)
    linkConnectors('layer2', connectors2, barWidth, barWidth, barLength)

    # linkLayers
    linkLayers(connectors1, connectors2)

    # layer 3
    # generate geometry
    connectors3 = genPolarConnectorVerts('layer3', numSides, apothem, radius)
    translateConnectors(connectors3, 50.0)
    polarToCartesianConnectors(connectors3)

    # place connectors
    createPlusObjs('layer3', connectors3, barWidth, connectorWidth, connectorLength)

    # add bars
    linkConnectors('layer3', connectors3, barWidth, barWidth, barLength)

    # layer 4
    # generate geometry
    connectors4 = genPolarConnectorVerts('layer4', numSides, apothem, radius)
    rotateConnectors(connectors4, tau/(numSides*2))
    translateConnectors(connectors4, 50.0)
    polarToCartesianConnectors(connectors4)

    # place connectors
    createPlusObjs('layer4', connectors4, barWidth, connectorWidth, connectorLength)

    # add bars
    linkConnectors('layer4', connectors4, barWidth, barWidth, barLength)

    # linkLayers
    linkLayers(connectors3, connectors4)

    # cross-link
    radiusMinusApothem = radius - apothem
    crossLinkLayers('crosses', connectors1, connectors2, connectors3, connectors4, radiusMinusApothem, barWidth, barWidth, barLength)



if __name__ == "__main__":
    genArch()
