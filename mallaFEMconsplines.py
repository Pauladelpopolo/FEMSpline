"""Uso de splines para generer una malla de elementos finitos"""

#La spline qye vamos a utilizar para interpolar puntos es la de catmull-roll

import gmsh

gmsh.initialize()
gmsh.option.setNumber("General.Terminal", 1)
gmsh.model.add("modelo_6")

geom = gmsh.model.geo

"""Agregamos las variables geometricas"""

L = 1 #Longitud desde el centro de la malla interior hasta los bordes

"""Creamos la geometria"""

#Creamos nuestros puntos de control

geom.addPoint(1, 0, 0)
geom.addPoint(0, 1, 0)
geom.addPoint(0, 0, 1)
geom.addPoint(-1, 0, 0)
geom.addPoint(0, -1, 0)
geom.addPoint(0, 0, -1)


"""Se crea la B Spline con tomando los puntos anteriores como puntos de control:"""

af = geom.addBSpline([1, 1, 2, 3, 4, 5, 6, 1, 1])

"""Funcion para crear curvas transfinitas"""

geom.mesh.setTransfiniteCurve(af, 301) #301 nodos

### Curvas ###
c_int = geom.addCurveLoop([af])

#Se crea el borde de la superficie exterior
p1 = geom.addPoint(-L, -L, 0)
p2 = geom.addPoint(0.5+L, -L, 0)
p3 = geom.addPoint(0.5+L, L, 0)
p4 = geom.addPoint(-L, L, 0)

l1 = geom.addLine(p1, p2)
l2 = geom.addLine(p2, p3)
l3 = geom.addLine(p3, p4)
l4 = geom.addLine(p4, p1)

c_ext = geom.addCurveLoop([l1, l2, l3, l4])

s1 = geom.addPlaneSurface([c_ext, c_int])

"""Creacion de la superficie fisica"""

gmsh.model.addPhysicalGroup(2, [s1], 101) #grupo fisico de dimension 2, con las superficies s1, s2
                                            #El tag 101 se lo asignamos manualmente
gmsh.model.setPhysicalName(2, 101, "Volumen")

#Recombinacion para que los elementos sean cuadrilateros y no triangulos
geom.mesh.setRecombine(2, s1)

#Sincronizamos la geometria con el modelo
geom.synchronize()
gmsh.model.mesh.generate(3)

gmsh.model.mesh.setOrder(3)

gmsh.write("MallitaSpline.msh")

gmsh.option.setNumber("Mesh.SurfaceFaces", 1)
gmsh.option.setNumber("Mesh.Points", 1)

gmsh.fltk.run()

gmsh.finalize()