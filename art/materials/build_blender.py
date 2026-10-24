"""Run with Blender --background --factory-startup --python this_file.py.
New file only. Cuboids and textures come from the shipped Minecraft models.
"""
import bpy, json, math
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'art/materials'
ASSETS=ROOT/'src/main/resources/assets/createindustrial'
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
scene=bpy.context.scene
scene.render.engine='CYCLES'
scene.cycles.samples=24
scene.render.threads_mode='FIXED'
scene.render.threads=4
scene.render.resolution_x=1600
scene.render.resolution_y=1900
scene.render.resolution_percentage=100
scene.world.color=(0.12,0.12,0.12)
scene.view_settings.view_transform='Standard'
mats={}
def material(texture,metal=False):
    if texture in mats:return mats[texture]
    mat=bpy.data.materials.new(texture);mat.use_nodes=True
    nodes=mat.node_tree.nodes
    bsdf=next(n for n in nodes if n.type=='BSDF_PRINCIPLED')
    bsdf.inputs['Metallic'].default_value=0
    bsdf.inputs['Roughness'].default_value=0.85
    tex=nodes.new('ShaderNodeTexImage');tex.interpolation='Closest'
    tex.image=bpy.data.images.load(str(ASSETS/'textures'/f'{texture}.png'));tex.image.pack()
    mat.node_tree.links.new(tex.outputs['Color'],bsdf.inputs['Base Color'])
    mats[texture]=mat;return mat
def cuboid(name,lo,hi,texture,origin,metal=False):
    center=[(a+b)/32 for a,b in zip(lo,hi)]
    dims=[(b-a)/16 for a,b in zip(lo,hi)]
    bpy.ops.mesh.primitive_cube_add(size=1,location=(origin[0]+center[0]-.5,origin[1]-(center[2]-.5),origin[2]+center[1]))
    ob=bpy.context.object;ob.name=name;ob.dimensions=(dims[0],dims[2],dims[1]);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    # Every flat face maps the same 16x16 texture, matching cube_all / item faces.
    uv=ob.data.uv_layers.active
    for poly in ob.data.polygons:
        for loop_index,coord in zip(poly.loop_indices,[(0,0),(1,0),(1,1),(0,1)]):uv.data[loop_index].uv=coord
    ob.data.materials.append(material(texture,metal));return ob
catalog=json.loads((ROOT/'materials.json').read_text())
names=[]
for m in catalog['materials']:
 names += [m['ore']+'_ore','deepslate_'+m['ore']+'_ore','raw_'+m['id']+'_block','block_of_'+m['id']]
names += ['block_of_'+m['id'] for m in catalog['manufactured']]
names += ['laser_printer','steel_converter','fireclay','fireclay_bricks','reinforced_concrete']
for index,name in enumerate(names):
 origin=((index%4)*1.9,-(index//4)*1.9,0)
 data=json.loads((ASSETS/'models/block'/f'{name}.json').read_text())
 elements=data.get('elements')
 textures=data['textures']
 if not elements:
  alltex=textures.get('all') or textures.get('side')
  elements=[{'from':[0,0,0],'to':[16,16,16],'faces':{f:{'texture':alltex if f not in ('up','down') else textures.get('top',alltex)} for f in ('up','down','north','south','east','west')}}]
 collection=bpy.data.collections.new(name);scene.collection.children.link(collection)
 for i,e in enumerate(elements):
  first=next(iter(e['faces'].values()))['texture']
  while first.startswith('#'):first=textures[first[1:]]
  ob=cuboid(name+f'_{i}',e['from'],e['to'],first.split(':',1)[1],origin)
  for c in list(ob.users_collection):c.objects.unlink(ob)
  collection.objects.link(ob)
  for poly in ob.data.polygons:
   normal=poly.normal
   face='up' if normal.z>.5 else 'down' if normal.z<-.5 else 'east' if normal.x>.5 else 'west' if normal.x<-.5 else 'south' if normal.y<-.5 else 'north'
   ref=e['faces'].get(face,{}).get('texture',first)
   while ref.startswith('#'):ref=textures[ref[1:]]
   ob.data.materials.append(material(ref.split(':',1)[1]));poly.material_index=len(ob.data.materials)-1
 bpy.ops.object.text_add(location=(origin[0]-.65,origin[1]-.7,.02))
 bpy.context.object.data.body=name.replace('_',' ').title();bpy.context.object.data.size=.12
# Inventory materials are PNG sprites only; no ingot/raw/crushed/nugget mesh is created.
bpy.ops.mesh.primitive_plane_add(size=200,location=(3,-1,-.025))
floor=bpy.context.object;floor.name='Preview_Floor'
mat=bpy.data.materials.new('Preview_Charcoal');mat.use_nodes=True
next(n for n in mat.node_tree.nodes if n.type=='BSDF_PRINCIPLED').inputs['Base Color'].default_value=(.032,.042,.052,1)
floor.data.materials.append(mat)
for loc,power,size in [((1,-5,9),1800,8),((8,1,7),1400,6)]:
    bpy.ops.object.light_add(type='AREA',location=loc)
    light=bpy.context.object;light.data.energy=power;light.data.shape='DISK';light.data.size=size
bpy.ops.object.camera_add(location=(11,-20,25))
cam=bpy.context.object;target=Vector((3.9,-7,.35));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=22.5
scene.camera=cam
scene.render.filepath=str(OUT/'blocks-preview.png')
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'industrial-blocks.blend'))
bpy.ops.render.render(write_still=True)
(OUT/'blender-verification.json').write_text(json.dumps({'blender':bpy.app.version_string,'inventory_meshes':0,'mesh_objects':sum(o.type=='MESH' for o in scene.objects),
    'packed_images':sum(bool(i.packed_file) for i in bpy.data.images),'ore_families':len(catalog['materials']),
    'manufactured_families':len(catalog['manufactured']),'machines':['laser_printer','steel_converter']},indent=2)+'\n')
print('Saved editable Blender scene and rendered material preview.')
