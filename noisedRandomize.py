
bl_info = {
	"name": "Noised Randomize",
	"description": "Noised Randomize",
	"author": "io",
	"version": (0, 0, 1),
	"blender": (2, 80, 0),
	"location": "Object Settings",
	"warning": "",
	"wiki_url": ""
				"",
	"category": "Scene",
}


import bpy

import random
import math
import mathutils
#from math import ceil, floor, sqrt, radians
from math import radians
from bpy.types import Panel, Operator, Scene, PropertyGroup
from bpy.app.handlers import persistent, frame_change_pre
from bpy.props import (
		BoolProperty,
		EnumProperty,
		FloatProperty,
		IntProperty,
		IntVectorProperty,
		StringProperty,
		PointerProperty,
		)
	
	
#def countEnum(en):
#	prop = rna_type.bl_rna.properties[prop_str]
#	return [e.identifier for e in nrs.NRgrpSet]

#def nrAddGroup(nrs):
#	print("nrAddGroup")
#	scn = bpy.context.scene
#	nrs = scn.nrsettings
#	
#	#salva i valori in una custom property della scena
##	bpy.context.scene["NRsettings.001"]={'var1':1,'var2':'ciao','var3':[1,2,3]}
#	#che si legge: bpy.context.scene["NRsettings.001"]['var1']
#	
#	#cerca nelle custom property
#	if len(scn.keys()) > 1:
#		print("Scene custom properties:")
#		for K in scn.keys():
#			if K not in '_RNA_UI':
#				if K.startswith('NRsettings'):
#					print("***********")
#					print( K , "-" , scn[K] )
#					print("+++++++++++")
#					print(bpy.context.scene[K]['var1'])
#					print(bpy.context.scene[K]['var2'])
#					print(bpy.context.scene[K]['var3'])
#	
##	argrp = [e for e in nrs.NRgrpSet]
##	ngrp=len(argrp)
##	ngrp=ngrp+1
##	rName="NRset."
##	newName=rName+str(ngrp)
##	print(newName)
#	
#def nrChangedGroup(self, context):
#	print("nrChangedGroup")
#	scn = bpy.context.scene
#	nrs = scn.nrsettings
#	print(nrs.NRgrpSet)
##	if nrs.NRtype=="RANDOM":
##		nrval=mathutils.noise.random()
##	else:
##		nrval=mathutils.noise.noise((vX,vY,vZ), noise_basis=nrs.NRtype)
##	

def nrUpdate(self, context):
#	print("nrUpdate")
	if nrUpdate.level is False:
		nrUpdate.level = True
#		print("update")
		#cicla per le custom properties cercando "NRsetting..."
			#prende il valore active
				#se True
					#prende tutti i valori
		scn = bpy.context.scene
		nrs = scn.nrsettings
		if nrs.NR_is_hide==False:
			setNRtransform()
		nrUpdate.level = False

nrUpdate.level = False

@persistent 
def nr_animation_update(scn):
	""" Function for updating the effects when the scene update """    
	setNRtransform()

def setNRtransform():
#	print("setNRtransform")
	scn = bpy.context.scene
	frame = scn.frame_current
	nrs = scn.nrsettings
	#controlla tutti gli oggetti della collezione
	if nrs.NR_enabled==True:
		collName=nrs.NR_collName
#		print("ready "+collName)
		nrColl = bpy.data.collections[collName]
		for ob in nrColl.objects:
#			ob.select_set(state=False)
			nrval=getNRval(ob,nrs)
			
			#loc
			ob.delta_location.x=nrval*nrs.NR_trsf_locx_s
			ob.delta_location.y=nrval*nrs.NR_trsf_locy_s
			ob.delta_location.z=nrval*nrs.NR_trsf_locz_s
#			#rot
			ob.delta_rotation_euler.x=radians(nrval*nrs.NR_trsf_rotx_s)
			ob.delta_rotation_euler.y=radians(nrval*nrs.NR_trsf_roty_s)
			ob.delta_rotation_euler.z=radians(nrval*nrs.NR_trsf_rotz_s)
#			#scl delta_scale
			ob.delta_scale.x=1+(nrval*nrs.NR_trsf_sclx_s)
			ob.delta_scale.y=1+(nrval*nrs.NR_trsf_scly_s)
			ob.delta_scale.z=1+(nrval*nrs.NR_trsf_sclz_s)
			
	else:
		print("NR not ready")

def copyNRtransform(nrs,removeNR):
	collName=nrs.NR_collName
	if bpy.data.collections.get(collName) is None:
		print("NR - nothing to copy")
		nrs.NR_enabled=False
	else:
		nrColl = bpy.data.collections[collName]
		for ob in nrColl.objects:
			#loc
			ob.location.x=ob.location.x+ob.delta_location.x
			ob.location.y=ob.location.y+ob.delta_location.y
			ob.location.z=ob.location.z+ob.delta_location.z
			#rot
			ob.rotation_euler.x=ob.rotation_euler.x+ob.delta_rotation_euler.x
			ob.rotation_euler.y=ob.rotation_euler.y+ob.delta_rotation_euler.y
			ob.rotation_euler.z=ob.rotation_euler.z+ob.delta_rotation_euler.z
			#scl
			ob.scale.x=ob.scale.x*ob.delta_scale.x
			ob.scale.y=ob.scale.y*ob.delta_scale.y
			ob.scale.z=ob.scale.z*ob.delta_scale.z
		
		if removeNR:
			delNRtransform(nrs)

def hideNRtransform(self, context):
#	print("hideNRtransform")
	scn = bpy.context.scene
	frame = scn.frame_current
	nrs = scn.nrsettings
	collName=nrs.NR_collName
	if bpy.data.collections.get(collName) is None:
		print("NR - nothing to hide or show")
		nrs.NR_enabled=False
	else:
		nrColl = bpy.data.collections[collName]
		if nrs.NR_is_hide:
			for ob in nrColl.objects:
	#			ob.select_set(state=False)
				#loc
				ob.delta_location.x=0
				ob.delta_location.y=0
				ob.delta_location.z=0
				#rot
				ob.delta_rotation_euler.x=0
				ob.delta_rotation_euler.y=0
				ob.delta_rotation_euler.z=0
				#scl
				ob.delta_scale.x=1
				ob.delta_scale.y=1
				ob.delta_scale.z=1
		else:
			setNRtransform()
			
	
def selNRtransform(nrs):
	collName=nrs.NR_collName
	if bpy.data.collections.get(collName) is None:
		print("NR - nothing to select")
		nrs.NR_enabled=False
	else:
		nrColl = bpy.data.collections[collName]
		for ob in nrColl.objects:
			ob.select_set(state=True)
			
def delNRtransform(nrs):
	collName=nrs.NR_collName
	if bpy.data.collections.get(collName) is None:
		print("NR - nothing to delete")
		nrs.NR_enabled=False
	else:
		nrColl = bpy.data.collections[collName]
		for ob in nrColl.objects:
#			ob.select_set(state=False)
			#loc
			ob.delta_location.x=0
			ob.delta_location.y=0
			ob.delta_location.z=0
			#rot
			ob.delta_rotation_euler.x=0
			ob.delta_rotation_euler.y=0
			ob.delta_rotation_euler.z=0
			#scl
			ob.delta_scale.x=1
			ob.delta_scale.y=1
			ob.delta_scale.z=1
			nrColl.objects.unlink(ob)
			
		bpy.context.scene.collection.children.unlink(nrColl)
		bpy.data.collections.remove(nrColl)
		nrs.NR_enabled=False
		nrs.NR_is_hide=False

def getNRval(ob,nrss):
#	print("getNRval")
	scn=bpy.context.scene
	rnd = bpy.context.scene.render
	frame = scn.frame_current
	nrs = scn.nrsettings
	ret=0
	nS=0
	nrval=0

	#controlla la dimensione dell'immagine noise
#	nS=nrs.NRscl/100
	nS=((nrs.NRscl*-1)+1000)/100

	#posizione dell'immagine noise
	nX=nrs.NRposx
	nY=nrs.NRposy
	nZ=nrs.NRposz

	#posizione oggetto
	sX=ob.location.x
	sY=ob.location.y
	sZ=ob.location.z
	 
	#valori posizione
	vX=(nX-sX)*nS
	vY=(nY-sY)*nS
	vZ=(nZ-sZ)*nS

	if nrs.NRtype=="RANDOM":
		nrval=mathutils.noise.random()
	else:
		nrval=mathutils.noise.noise((vX,vY,vZ), noise_basis=nrs.NRtype)
		
	return nrval


class NRSettings(PropertyGroup):
	NR_enabled: BoolProperty(
		name="NR ready",
		default=False,
		description="NR enabled",
		)
#	NR_is_animated: BoolProperty(
#		name="NR animated",
#		default=False,
#		description="NR animated",
#		update=followAnimation,
#		)
	NR_is_hide: BoolProperty(
		name="NR hidden",
		default=False,
		description="NR hidden",
		update=hideNRtransform,
		)
		
	NR_active: BoolProperty(
		name="NR active",
		default=False,
		description="NR active",
		)
	
#		dimensione img noise
	NRscl: FloatProperty(
		name="noise scale",
		default=550,
		min=0,
		max=1000,
		description="Scale of noise",
		update=nrUpdate
		)

#		posizione img noise xyz
	NRposx: FloatProperty(
		name="nrlX",
		default=0,
		min=-10000,
		max=10000,
		description="Position X of noise",
		update=nrUpdate
		)
	NRposy: FloatProperty(
		name="nrlY",
		default=0,
		min=-10000,
		max=10000,
		description="Position Y of noise",
		update=nrUpdate
		)
	NRposz: FloatProperty(
		name="nrlZ",
		default=1,
		min=-10000,
		max=10000,
		description="Position Z of noise",
		update=nrUpdate,
		)

#		tipo noise
	NRtype: EnumProperty(
		name="",
		description="Noise type",
		items=(
			("BLENDER", "BLENDER","BLENDER"),
			("PERLIN_ORIGINAL","PERLIN_ORIGINAL","PERLIN_ORIGINAL"),
			("PERLIN_NEW","PERLIN_NEW","PERLIN_NEW"),
			("VORONOI_F1","VORONOI_F1","VORONOI_F1"),
			("VORONOI_F2","VORONOI_F2","VORONOI_F2"),
			("VORONOI_F3","VORONOI_F3","VORONOI_F3"),
			("VORONOI_F4","VORONOI_F4","VORONOI_F4"),
			("VORONOI_F2F1","VORONOI_F2F1","VORONOI_F2F1"),
			("VORONOI_CRACKLE","VORONOI_CRACKLE","VORONOI_CRACKLE"),
			("CELLNOISE","CELLNOISE","CELLNOISE"),
			("RANDOM","Random","pure random")

		),
		default="BLENDER",
		update=nrUpdate,
		)
#		nome collezione
	NR_collName:StringProperty(
		name = "nrCollName",
		description = "The name of the new NR Collection",
		default = "_NRcoll_")
		
	#################################
		
	NR_trsf_locx_s: FloatProperty(
		name="nrlXs",
		default=0,
		min=-10000,
		max=10000,
		description="strength location X",
		update=nrUpdate
		)
	NR_trsf_locy_s: FloatProperty(
		name="nrlYs",
		default=0,
		min=-10000,
		max=10000,
		description="strength location Y",
		update=nrUpdate
		)
	NR_trsf_locz_s: FloatProperty(
		name="nrlZs",
		default=0,
		min=-10000,
		max=10000,
		description="strength location Z",
		update=nrUpdate
		)
	##################################
		
	NR_trsf_rotx_s: FloatProperty(
		name="nrrXs",
		default=0,
		min=-10000,
		max=10000,
		description="strength rotation X",
		update=nrUpdate
		)
	NR_trsf_roty_s: FloatProperty(
		name="nrrYs",
		default=0,
		min=-10000,
		max=10000,
		description="strength rotation Y",
		update=nrUpdate
		)
	NR_trsf_rotz_s: FloatProperty(
		name="nrrZs",
		default=0,
		min=-10000,
		max=10000,
		description="strength rotation Z",
		update=nrUpdate
		)
	
	#####################################
		
	NR_trsf_sclx_s: FloatProperty(
		name="nrsXs",
		default=0,
		min=-10000,
		max=10000,
		description="strength scale X",
		update=nrUpdate
		)
	NR_trsf_scly_s: FloatProperty(
		name="nrsYs",
		default=0,
		min=-10000,
		max=10000,
		description="strength scale Y",
		update=nrUpdate
		)
	NR_trsf_sclz_s: FloatProperty(
		name="nrsZs",
		default=0,
		min=-10000,
		max=10000,
		description="strength scale Z",
		update=nrUpdate
		)
	#######################################


class NOISED_PT_Random(Panel):
	bl_label = "Noised randomize"
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = "scene"
	
	def draw(self, context):
		layout = self.layout
		scn = context.scene
		nrs = scn.nrsettings
		
		label_save="label"
		rowList=[]
		row1 = layout.row(align=True)
		rowList.append(row1)
		row2 = layout.row(align=True)
		rowList.append(row2)
		row3 = layout.row(align=True)
		rowList.append(row3)
		row4 = layout.row(align=True)
		rowList.append(row4)
		row5 = layout.row(align=True)
		rowList.append(row5)
		row6 = layout.row(align=True)
		rowList.append(row6)
		row7 = layout.row(align=True)
		rowList.append(row7)
		row8 = layout.row(align=True)
		rowList.append(row8)
		row9 = layout.row(align=True)
		rowList.append(row9)
		row10 = layout.row(align=True)
		rowList.append(row10)
		row11 = layout.row(align=True)
		rowList.append(row11)
		row12 = layout.row(align=True)
		rowList.append(row12)
		row13 = layout.row(align=True)
		rowList.append(row13)
		row14 = layout.row(align=True)
		rowList.append(row14)
		row15 = layout.row(align=True)
		rowList.append(row15)
		row16 = layout.row(align=True)
		rowList.append(row16)
		
		rn=0
		rowList[rn].label(text="Noise settings")
		rn+=1
		rowList[rn].prop(nrs, "NRscl")
		rn+=1
		rowList[rn].prop(nrs, "NRposx",text="loc X")
		rowList[rn].prop(nrs, "NRposy",text="loc Y")
		rowList[rn].prop(nrs, "NRposz",text="loc Z")
		rn+=1
		rowList[rn].label(text="Noise type")
		rowList[rn].prop(nrs, "NRtype")
		rn+=1

#		rowList[rn].label(text="Collection name")
#		rowList[rn].prop(nrs, "NR_collName")
		
		rowList[rn].label(text="Multiplier for Transformation")
		rn+=1

		rowList[rn].label(text="loc")
		rowList[rn].prop(nrs, "NR_trsf_locx_s",text="X")
		rowList[rn].prop(nrs, "NR_trsf_locy_s",text="Y")
		rowList[rn].prop(nrs, "NR_trsf_locz_s",text="Z")
		rn+=1
		
		rowList[rn].label(text="rot")
		rowList[rn].prop(nrs, "NR_trsf_rotx_s",text="X")
		rowList[rn].prop(nrs, "NR_trsf_roty_s",text="Y")
		rowList[rn].prop(nrs, "NR_trsf_rotz_s",text="Z")
		rn+=1
		
		rowList[rn].label(text="scl")
		rowList[rn].prop(nrs, "NR_trsf_sclx_s",text="X")
		rowList[rn].prop(nrs, "NR_trsf_scly_s",text="Y")
		rowList[rn].prop(nrs, "NR_trsf_sclz_s",text="Z")
		rnmin=rn
		rn+=1

		if nrs.NR_is_hide:
			icon = 'HIDE_OFF'
			txt = 'Show'
		else:
			icon = 'HIDE_ON'
			txt = 'Hide'
		rowList[rn].prop(nrs, 'NR_is_hide', text=txt, icon=icon, toggle = True)
		rn+=1
		
		rowList[rn].label(text="Copy to transform")
		
		rn+=1
		
		rowList[rn].operator("noised.randomcopy", text="Copy", icon="FORWARD")
		rowList[rn].operator("noised.randomcopydel", text="Copy and remove", icon="FORWARD")
		rn+=1
		
		row14.separator()
		rn+=1
		
		rowList[rn].operator("noised.randomsel", text="Select all Object", icon="ARROW_LEFTRIGHT")
		rn+=1
		rowList[rn].operator("noised.randomdel", text="Remove", icon="CANCEL")
		rn+=1
		rnmax=rn
#		
		if nrs.NR_enabled:
			icon="PLUS"
			txt="Add object"
		else:
			icon="TRIA_RIGHT"
			txt="Activate"
		rowList[rn].operator("noised.random", text=txt, icon=icon)
		
		
		for rnn in range(0,rnmax):
			rowList[rnn].active = nrs.NR_enabled
			if rnn>rnmin:
				rowList[rnn].enabled = nrs.NR_enabled
		
#		rn+=1	
#		rowList[rn].label(text="Noise settings groups")
#		rowList[rn].operator("noised.randomaddgroup", text="Add new setting group", icon="ADD")
		
##		row16.prop(nrs, "NRframe")

class NRClassOpAddgrp(Operator):
	bl_idname = "noised.randomaddgroup"
	bl_label = "add setting group"
	bl_description = "noised random add a new setting group"

	bl_options = {'REGISTER', 'UNDO'}
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = "scene"
	
	def execute(self, context):
		scn = context.scene
		rnd = context.scene.render
		nrs = scn.nrsettings
		nrAddGroup(nrs)
		return {'FINISHED'}
				
class NRClassOpSel(Operator):
	bl_idname = "noised.randomsel"
	bl_label = "Noised random select all"
	bl_description = "noised random select all"

	bl_options = {'REGISTER', 'UNDO'}
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = "scene"
	
	def execute(self, context):
		scn = context.scene
		rnd = context.scene.render
		nrs = scn.nrsettings
		selNRtransform(nrs)
		return {'FINISHED'}

class NRClassOpDel(Operator):
	bl_idname = "noised.randomdel"
	bl_label = "Noised random delete"
	bl_description = "noised random delete"

	bl_options = {'REGISTER', 'UNDO'}
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = "scene"
	
	def execute(self, context):
		scn = context.scene
		rnd = context.scene.render
		nrs = scn.nrsettings
		delNRtransform(nrs)
		return {'FINISHED'}

class NRClassOpCopy(Operator):
	bl_idname = "noised.randomcopy"
	bl_label = "Noised random copy to transform"
	bl_description = "noised random copy to transform"

	bl_options = {'REGISTER', 'UNDO'}
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = "scene"
	
	def execute(self, context):
		scn = context.scene
		rnd = context.scene.render
		nrs = scn.nrsettings
		copyNRtransform(nrs,False)
		return {'FINISHED'}

class NRClassOpCopyDel(Operator):
	bl_idname = "noised.randomcopydel"
	bl_label = "Noised random copy to transform and remove NR"
	bl_description = "noised random copy to transform and remove NR"

	bl_options = {'REGISTER', 'UNDO'}
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = "scene"
	
	def execute(self, context):
		scn = context.scene
		rnd = context.scene.render
		nrs = scn.nrsettings
		copyNRtransform(nrs,True)
		return {'FINISHED'}

class NRClassOpHide(Operator):
	bl_idname = "noised.randomhide"
	bl_label = "Hide Noised random"
	bl_description = "Hide noised random"

	bl_options = {'REGISTER', 'UNDO'}
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = "scene"
	
	def execute(self, context):
		scn = context.scene
		rnd = context.scene.render
		nrs = scn.nrsettings
		hideNRtransform()
		return {'FINISHED'}

class NRClassOp(Operator):
	bl_idname = "noised.random"
	bl_label = "Noised random"
	bl_description = "noised random description"

	bl_options = {'REGISTER', 'UNDO'}
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
#	bl_context = "object"
	bl_context = "scene"

#	@classmethod
#	def poll(clss, context):
#		return {'poll'}

	def execute(self, context):

		scn = context.scene
		rnd = context.scene.render
		nrs = scn.nrsettings
		collName=nrs.NR_collName
		
		if len(bpy.context.selected_objects)==0:
			self.report({'WARNING'}, "Nothing selected")
		else:
			if nrs.NR_enabled==False:
				#create collection
				
				if bpy.data.collections.get(collName) is None:
					nrColl =  bpy.data.collections.new(collName)
					bpy.context.scene.collection.children.link(nrColl)
					
					#excude new collection from all view layer
					vlayer_collection = scn.view_layers
					for vlay in vlayer_collection:
						vlay.layer_collection.children[collName].exclude=True
					
				else:
					nrColl = bpy.data.collections[collName]
				nrs.NR_enabled=True
			else:
				nrColl = bpy.data.collections[collName]

			#selected in collection
			selection_names = bpy.context.selected_objects
			for obsel in selection_names:
#				print(nrColl.all_objects[i.name])
				#check if is already in the collection
				alreadyIn=False
				for i in obsel.users_collection:
					if i.name == collName:
						alreadyIn=True
						break
				if alreadyIn==False:
					nrColl.objects.link(obsel)
				else:
					print("already in")

			setNRtransform()

		return {'FINISHED'}
		

classes = (
	NRSettings,
	NOISED_PT_Random,
	NRClassOp,
	NRClassOpSel,
	NRClassOpDel,
	NRClassOpCopy,
	NRClassOpCopyDel,
	NRClassOpHide
	)



def register():
	from bpy.utils import register_class
	for cls in classes:
		register_class(cls)

	bpy.types.Scene.nrsettings = PointerProperty(type=NRSettings)
	bpy.app.handlers.frame_change_pre.append(nr_animation_update)

def unregister():
	from bpy.utils import unregister_class

	del bpy.types.Scene.nrsettings
	for cls in classes:
		unregister_class(cls)

	bpy.app.handlers.frame_change_pre.remove(nr_animation_update)

if __name__ == "__main__":
	register()


