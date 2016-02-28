
def genArchOld():
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
            hinge1 = bpy.context.scene.objects.active
            hinge1.name = ("even empty."+str(i)+".1")
            hinge1.parent = obj
            hinge1.location = (x,0,-z/2)
            hinge1.select = False

            bpy.ops.object.add(type='EMPTY')
            hinge2 = bpy.context.scene.objects.active
            hinge2.name = ("even empty."+str(i)+".2")
            hinge2.parent = obj
            hinge2.location = (-z/2,0,x)
            hinge2.select = False

            bpy.ops.object.add(type='EMPTY')
            hinge3 = bpy.context.scene.objects.active
            hinge3.name = ("even empty."+str(i)+".3")
            hinge3.parent = obj
            hinge3.location = (-x,0,z/2)
            hinge3.select = False

            bpy.ops.object.add(type='EMPTY')
            hinge4 = bpy.context.scene.objects.active
            hinge4.name = ("even empty."+str(i)+".4")
            hinge4.parent = obj
            hinge4.location = (z/2,0,x)
            hinge4.select = False

        else:
            bpy.ops.object.add(type='EMPTY')
            hinge1 = bpy.context.scene.objects.active
            hinge1.name = ("odd empty."+str(i)+".1")
            hinge1.parent = obj
            hinge1.location = (x,0,-z/2)
            hinge1.select = False

            bpy.ops.object.add(type='EMPTY')
            hinge2 = bpy.context.scene.objects.active
            hinge2.name = ("odd empty."+str(i)+".2")
            hinge2.parent = obj
            hinge2.location = (-z/2,0,x)
            hinge2.select = False

            bpy.ops.object.add(type='EMPTY')
            hinge3 = bpy.context.scene.objects.active
            hinge3.name = ("odd empty."+str(i)+".3")
            hinge3.parent = obj
            hinge3.location = (-x,0,z/2)
            hinge3.select = False

            bpy.ops.object.add(type='EMPTY')
            hinge4 = bpy.context.scene.objects.active
            hinge4.name = ("odd empty."+str(i)+".4")
            hinge4.parent = obj
            hinge4.location = (z/2,0,-x)
            hinge4.select = False

        obj.select = True
        bpy.context.scene.objects.active = obj
        obj.location = cartesianVerts[i]
        obj.rotation_euler = (tau/4,-(4*tau)/12-(tau/12)*i,0)
        bpy.ops.rigidbody.object_add(type='ACTIVE')
        obj.select = False

        vert_objs.append((obj, (hinge1, hinge2, hinge3, hinge4)))
