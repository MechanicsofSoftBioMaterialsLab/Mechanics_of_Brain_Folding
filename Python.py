x1=0
x2=60
y1=0
y2=60
z1=0
z2=60
t=1.5
Mesh_Size=0.4




#import ...............................................................
from abaqus import *
from abaqusConstants import *
from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from optimization import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *
import __main__
import section
import regionToolset
import displayGroupMdbToolset as dgm
import part
import material
import assembly
import step
import interaction
import load
import mesh
import optimization
import job
import sketch
import visualization
import xyPlot
import displayGroupOdbToolset as dgo
import connectorBehavior
import os
import random
import math
import numpy as np
import shutil
def positive_or_negative():
    return 1 if random.random() < 0.5 else -1

cwd = os.getcwd()
Name="Base"
os.makedirs(cwd+'/'+Name)
os.chdir(cwd+'/'+Name)
#Create Model
s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
    sheetSize=200.0)
g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
s1.setPrimaryObject(option=STANDALONE)
s1.rectangle(point1=(x1, y1), point2=(x2, y2))
p = mdb.models['Model-1'].Part(name='Brain', dimensionality=THREE_D, 
    type=DEFORMABLE_BODY)
p = mdb.models['Model-1'].parts['Brain']
p.BaseSolidExtrude(sketch=s1, depth=z2-z1)
s1.unsetPrimaryObject()
p = mdb.models['Model-1'].parts['Brain']
del mdb.models['Model-1'].sketches['__profile__']
p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=z2-t)
c = p.cells
pickedCells = c.getSequenceFromMask(mask=('[#1 ]', ), )
d1 = p.datums
p.PartitionCellByDatumPlane(datumPlane=d1[2], cells=pickedCells)
s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
    sheetSize=200.0)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=STANDALONE)
s.rectangle(point1=(x1, y1), point2=(x2, y2))
p = mdb.models['Model-1'].Part(name='Part-2', dimensionality=THREE_D, 
    type=DISCRETE_RIGID_SURFACE)
p.BaseShellExtrude(sketch=s, depth=2*z2)
s.unsetPrimaryObject()
session.viewports['Viewport: 1'].setValues(displayedObject=p)
del mdb.models['Model-1'].sketches['__profile__']
v1, e, d2, n = p.vertices, p.edges, p.datums, p.nodes
p.ReferencePoint(point=v1[1])
#Material Properties
p = mdb.models['Model-1'].parts['Brain']
mdb.models['Model-1'].Material(name='Cortex')
mdb.models['Model-1'].materials['Cortex'].Density(table=((1e-9, ), ))
mdb.models['Model-1'].materials['Cortex'].Hyperelastic(materialType=ISOTROPIC, 
    testData=OFF, type=NEO_HOOKE, volumetricResponse=VOLUMETRIC_DATA, 
    table=((100e-6, 3500), ))
mdb.models['Model-1'].materials['Cortex'].Expansion(type=ORTHOTROPIC, table=((
    0.005, 0.005, 0.0), ))
mdb.models['Model-1'].Material(name='White_Matter')
mdb.models['Model-1'].materials['White_Matter'].Density(table=((1e-9, ), ))
mdb.models['Model-1'].materials['White_Matter'].Hyperelastic(
    materialType=ISOTROPIC, testData=OFF, type=NEO_HOOKE, 
    volumetricResponse=VOLUMETRIC_DATA, table=((100e-6, 3500), ))
mdb.models['Model-1'].materials['White_Matter'].Expansion(table=((0.0, ), ))
mdb.models['Model-1'].HomogeneousSolidSection(name='Cortex', material='Cortex', 
    thickness=None)
mdb.models['Model-1'].HomogeneousSolidSection(name='White_Matter', 
    material='White_Matter', thickness=None)
c = p.cells
cells = c.findAt((((x2-x1)/2.,(y2-y1)/2.,(z2-z1)/2.),))
region = p.Set(cells=cells, name='White_Matter')
p.SectionAssignment(region=region, sectionName='White_Matter', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)
c = p.cells
cells = c.findAt((((x2-x1)/2.,(y2-y1)/2.,z2-t/2.),))
region = p.Set(cells=cells, name='Cortex')
p.SectionAssignment(region=region, sectionName='Cortex', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)
region = p.sets['Cortex']
orientation=None
mdb.models['Model-1'].parts['Brain'].MaterialOrientation(region=region, 
    orientationType=GLOBAL, axis=AXIS_1, 
    additionalRotationType=ROTATION_NONE, localCsys=None, fieldName='', 
    stackDirection=STACK_3)
#Mesh
e = p.edges
pickedEdges = e.findAt(((x1,y1,(z2-t/2.)),), ((x2,y1,(z2-t/2.)),), ((x1,y2,(z2-t/2.)),), ((x2,y2,(z2-t/2.)),) )
p.seedEdgeByNumber(edges=pickedEdges, number=3, constraint=FINER)
e = p.edges
pickedEdges2 = e.findAt(((x1,y1,(z2-t)/2.),), ((x2,y1,(z2-t)/2.),), ((x1,y2,(z2-t)/2.),), ((x2,y2,(z2-t)/2.),) )
p.seedEdgeByBias(biasMethod=SINGLE, end2Edges=pickedEdges2, minSize=Mesh_Size, 
    maxSize=10, constraint=FINER)
p.seedPart(size=Mesh_Size, deviationFactor=0.1, minSizeFactor=0.1)
elemType1 = mesh.ElemType(elemCode=C3D8R, elemLibrary=STANDARD, 
    kinematicSplit=AVERAGE_STRAIN, secondOrderAccuracy=OFF, 
    hourglassControl=DEFAULT, distortionControl=DEFAULT)
elemType2 = mesh.ElemType(elemCode=C3D6, elemLibrary=STANDARD)
elemType3 = mesh.ElemType(elemCode=C3D4, elemLibrary=STANDARD)
c = p.cells
cells = c.getSequenceFromMask(mask=('[#3 ]', ), )
pickedRegions =(cells, )
p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, 
    elemType3))
p.generateMesh()
p = mdb.models['Model-1'].parts['Part-2']
p.seedPart(size=12.0, deviationFactor=0.1, minSizeFactor=0.1)
p.generateMesh()
elemType1 = mesh.ElemType(elemCode=C3D8R, elemLibrary=EXPLICIT, 
    kinematicSplit=AVERAGE_STRAIN, secondOrderAccuracy=OFF, 
    hourglassControl=DEFAULT, distortionControl=DEFAULT)
elemType2 = mesh.ElemType(elemCode=C3D6, elemLibrary=EXPLICIT)
elemType3 = mesh.ElemType(elemCode=C3D4, elemLibrary=EXPLICIT)
p = mdb.models['Model-1'].parts['Brain']
c = p.cells
cells = c.getSequenceFromMask(mask=('[#3 ]', ), )
pickedRegions =(cells, )
p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, 
    elemType3))
#Assembly
a = mdb.models['Model-1'].rootAssembly
a.DatumCsysByDefault(CARTESIAN)
p = mdb.models['Model-1'].parts['Brain']
a.Instance(name='Brain-1', part=p, dependent=ON)
p = mdb.models['Model-1'].parts['Part-2']
a.Instance(name='Part-2-1', part=p, dependent=ON)
#Step
mdb.models['Model-1'].ExplicitDynamicsStep(name='Step-1', previous='Initial', 
    timePeriod=0.6, improvedDtMethod=ON)
mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValues(variables=(
    'MISES', 'U', 'EVF','COORD'), timeInterval=0.6)
mdb.models['Model-1'].historyOutputRequests['H-Output-1'].setValues(variables=(
    'ALLAE', ), timeInterval=0.6)
#Interaction
mdb.models['Model-1'].ContactProperty('IntProp-1')
mdb.models['Model-1'].interactionProperties['IntProp-1'].TangentialBehavior(
    formulation=FRICTIONLESS)
mdb.models['Model-1'].interactionProperties['IntProp-1'].NormalBehavior(
    pressureOverclosure=HARD, allowSeparation=ON, 
    constraintEnforcementMethod=DEFAULT)
a = mdb.models['Model-1'].rootAssembly
s1 = a.instances['Brain-1'].faces
side1Faces1 = s1.findAt((((x2-x1)/2.,(y2-y1)/2.,z2),))
region=a.Surface(side1Faces=side1Faces1, name='Surface')
mdb.models['Model-1'].SelfContactExp(name='Int-1', createStepName='Initial', 
    surface=region, mechanicalConstraint=KINEMATIC, 
    interactionProperty='IntProp-1')
s1 = a.instances['Part-2-1'].faces
side2Faces1 = s1.findAt(((x1,(y2-y1)/2.,(z2-z1)/2.),), ((x2,(y2-y1)/2.,(z2-z1)/2.),), (((x2-x1)/2.,y1,(z2-z1)/2.),), (((x2-x1)/2.,y2,(z2-z1)/2.),) )
region1=regionToolset.Region(side2Faces=side2Faces1)
a = mdb.models['Model-1'].rootAssembly
s1 = a.instances['Brain-1'].faces
side1Faces1 = s1.findAt((((x2-x1)/2.,(y2-y1)/2.,z2),))
region2=regionToolset.Region(side1Faces=side1Faces1)
mdb.models['Model-1'].SurfaceToSurfaceContactExp(name ='Int-2', 
    createStepName='Initial', master = region1, slave = region2, 
    mechanicalConstraint=KINEMATIC, sliding=FINITE, 
    interactionProperty='IntProp-1', initialClearance=OMIT, datumAxis=None, 
    clearanceRegion=None)
#Boundary_Condition
a = mdb.models['Model-1'].rootAssembly
r1 = a.instances['Part-2-1'].referencePoints
refPoints1=(r1[2], )
region = regionToolset.Region(referencePoints=refPoints1)
mdb.models['Model-1'].DisplacementBC(name='Rigid_Body', 
    createStepName='Initial', region=region, u1=SET, u2=SET, u3=SET, 
    ur1=SET, ur2=SET, ur3=SET, amplitude=UNSET, distributionType=UNIFORM, 
    fieldName='', localCsys=None)
f1 = a.instances['Brain-1'].faces
faces1 = f1.findAt(((x1,(y2-y1)/2.,(z2-z1)/2.),), ((x2,(y2-y1)/2.,(z2-z1)/2.),), ((x1,(y2-y1)/2.,z2-t/2.),), ((x2,(y2-y1)/2.,z2-t/2.),) )
region = regionToolset.Region(faces=faces1)
mdb.models['Model-1'].XsymmBC(name='X_symm', createStepName='Initial', 
    region=region, localCsys=None)
f1 = a.instances['Brain-1'].faces
faces1 = f1.findAt((((x2-x1)/2.,y1,(z2-z1)/2.),), (((x2-x1)/2.,y1,z2-t/2.),), (((x2-x1)/2.,y2,(z2-z1)/2.),), (((x2-x1)/2.,y2,z2-t/2.),))
region = regionToolset.Region(faces=faces1)
mdb.models['Model-1'].YsymmBC(name='Y_symm', createStepName='Initial', 
    region=region, localCsys=None)
f1 = a.instances['Brain-1'].faces
faces1 = f1.findAt((((x2-x1)/2.,(y2-y1)/2.,z1),))
region = regionToolset.Region(faces=faces1)
mdb.models['Model-1'].ZsymmBC(name='Z_symm', createStepName='Initial', 
    region=region, localCsys=None)
a = mdb.models['Model-1'].rootAssembly
c1 = a.instances['Brain-1'].cells
cells1 = c1.getSequenceFromMask(mask=('[#3 ]', ), )
f1 = a.instances['Brain-1'].faces
faces1 = f1.getSequenceFromMask(mask=('[#7ff ]', ), )
e1 = a.instances['Brain-1'].edges
edges1 = e1.getSequenceFromMask(mask=('[#fffff ]', ), )
v1 = a.instances['Brain-1'].vertices
verts1 = v1.getSequenceFromMask(mask=('[#fff ]', ), )
region = regionToolset.Region(vertices=verts1, edges=edges1, faces=faces1, 
    cells=cells1)
mdb.models['Model-1'].Temperature(name='Predefined Field-1', 
    createStepName='Initial', region=region, distributionType=UNIFORM, 
    crossSectionDistribution=CONSTANT_THROUGH_THICKNESS, magnitudes=(0.0, 
    ))
mdb.models['Model-1'].EquallySpacedAmplitude(name='Amp-2', timeSpan=STEP, 
    smooth=SOLVER_DEFAULT, fixedInterval=1.0, begin=0.0, data=(0.0, 1.0))
mdb.models['Model-1'].predefinedFields['Predefined Field-1'].setValuesInStep(
    stepName='Step-1', magnitudes=(250.0, ), amplitude='Amp-2')
#Create_Set
p = mdb.models['Model-1'].parts['Brain']
n = p.nodes
nodes = n.getByBoundingBox(x1-t/2.,y1-t/2.,z2-Mesh_Size/2.,x2+t/2.,y2+t/2.,z2+Mesh_Size/2.)
p.Set(nodes=nodes, name='Surface')
#Job
Job_Name="inp"
mdb.Job(name=Job_Name, model='Model-1', description='', type=ANALYSIS, 
    atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=80, 
    memoryUnits=PERCENTAGE, getMemoryFromAnalysis=False, 
    explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
    modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
    scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=1, 
    numDomains=1, numGPUs=0)
mdb.jobs[Job_Name].submit(consistencyChecking=OFF, datacheckJob=True)
mdb.jobs[Job_Name].waitForCompletion()

for i in range(1):
    os.chdir(cwd+"/Base")
    modelName1 = 'Model-1'
    modelName2 = 'Model-2'
    partName = 'Brain'
    instName = 'Brain-1'
    stepName1='Step-1'
    odb = openOdb(path='inp.odb')
    Frame1 = odb.steps[stepName1].frames[0]
    displacement=Frame1.fieldOutputs['U']
    fieldValues=displacement.values
    modelName2 = 'Model-2'
    mdb.Model(name=modelName2, objectToCopy=mdb.models[modelName1])
    del mdb.models[modelName2].steps[stepName1]
    Coor = [[0 for col in range(3)] for row in range(len(mdb.models[modelName2].parts[partName].nodes))]
    NSurfElm=0
    NAmp=random.randint(10,15)
    for j in mdb.models[modelName2].parts[partName].nodes:
        Coor[j.label-1][0]=j.coordinates[0]
        Coor[j.label-1][1]=j.coordinates[1]
        Coor[j.label-1][2]=j.coordinates[2]
    for k in range(NAmp):
        A=random.uniform(1.5,2.5)
        A1=positive_or_negative()
        x0=random.uniform(x1,x2)
        y0=random.uniform(y1,y2)
        sigx=random.uniform(15,60)
        sigy=random.uniform(15,60)
        for j in mdb.models[modelName2].parts[partName].nodes:
            #if round(j.coordinates[2]*1000)/1000==z2:
            #Zimp=sin(rnd1*Coor[j.label-1][0]+rnd3)*cos(rnd2*Coor[j.label-1][1]+rnd4)*(j.coordinates[2]/z2)
            Zimp=A*A1*exp(-((Coor[j.label-1][0]-x0)**2/(2*sigx)+(Coor[j.label-1][1]-y0)**2/(2*sigy)))*(j.coordinates[2]/z2)
            Coor[j.label-1][2]=Coor[j.label-1][2]+Zimp
    mdb.models[modelName2].parts[partName].editNode(nodes=mdb.models[modelName2].parts[partName].nodes,coordinates=Coor)
    odb.close()
    mdb.models[modelName2].rootAssembly.regenerate()
    #Step
    mdb.models['Model-2'].ExplicitDynamicsStep(name='Step-1', previous='Initial', 
        timePeriod=0.6, improvedDtMethod=ON)
    mdb.models['Model-2'].fieldOutputRequests['F-Output-1'].setValues(variables=(
        'MISES', 'U', 'EVF','COORD'), timeInterval=0.06)
    mdb.models['Model-2'].historyOutputRequests['H-Output-1'].setValues(variables=(
        'ALLAE', ), timeInterval=0.06)
    #Load
    mdb.models['Model-2'].predefinedFields['Predefined Field-1'].setValuesInStep(stepName='Step-1', magnitudes=(250.0, ), amplitude='Amp-2')
    Name="Case-"+str(i+1)
    os.makedirs(cwd+'/'+Name+'-Temp')
    os.chdir(cwd+'/'+Name+'-Temp')
    #Job
    Job_Name=Name
    mdb.Job(name=Job_Name, model='Model-2', description='', type=ANALYSIS, 
        atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=80, 
        memoryUnits=PERCENTAGE, getMemoryFromAnalysis=False, 
        explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
        modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
        scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=1, 
        numDomains=1, numGPUs=0)
    mdb.jobs[Job_Name].submit(consistencyChecking=OFF)
    mdb.jobs[Job_Name].waitForCompletion()
    #Name2="Case-"+str(i+1)
    os.makedirs(cwd+'/'+Name)
    Original=cwd+'/'+Name+"-Temp/"+"Case-"+str(i+1)+".odb"
    Target=cwd+'/'+Name+"/"+"Case-"+str(i+1)+".odb"
    shutil.copyfile(Original, Target)
    os.chdir(cwd+'/'+Name)
    #session.mdbData.summary()
    o3 = session.openOdb(name=cwd+'/'+Name+'/'+Name+'.odb')
    session.viewports['Viewport: 1'].setValues(displayedObject=o3)
    session.viewports['Viewport: 1'].makeCurrent()
    session.linkedViewportCommands.setValues(_highlightLinkedViewports=True)
    leaf = dgo.LeafFromNodeSets(nodeSets=("BRAIN-1.SURFACE", ))
    session.viewports['Viewport: 1'].odbDisplay.displayGroup.replace(leaf=leaf)
    #session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=1)
    odb = session.odbs[cwd+'/'+Name+'/'+Name+'.odb']
    for k in range (11):
        File_Name='Surface_'+str(k)+'.rpt'
        session.writeFieldReport(fileName=File_Name, append=ON, 
            sortItem='Node Label', odb=odb, step=0, frame=k, outputPosition=NODAL, 
            variable=(('COORD', NODAL), ), stepFrame=SPECIFY)
    shutil.rmtree(cwd+'/'+Name+"-Temp")
    del mdb.models['Model-2']
    #Mdb()
    #t=t+0.01

