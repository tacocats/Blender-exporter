import bpy

def writeMap(context, filepath):

    print("running write_some_data...")
    f = open(filepath, 'w', encoding='utf-8')

    #Default map header 
    f.write("reflex map version 8\n")
    f.write("entity\n")
    f.write("\ttype WorldSpawn\n")
    f.write("\tColourXRGB32 clearColor ffffff\n")
    f.write("\tColourXRGB32 worldColor0 0\n")
    f.write("\tColourXRGB32 worldColor1 0\n")

    # Create a new brush for each seperate objext in blender scene
    for obj in bpy.data.meshes: # Get's all the objects in blender scene, each object will be a seperate brush
        # Changed this to use meshes instead of objects, to allow for a cleaner way to get the faces

        # Create a brush
        f.write("brush\n")
        
        # Create vertices
        f.write("\tvertices\n")
        #for i in obj.vertices: # Get's all the vertices for the selected object
        #    f.write("\t\t" + str(i.co.x * 100) + " " + str(i.co.y * 100) + " " + str(i.co.z * 100) +"\n") # Formats them into x, y, z
        for z in obj.vertices[:]:
            #f.write('\t\t%.6f %.6f %.6f\n' % z.co[:])
            f.write('\t\t' + str(z.co.x*40) + ' ' + str(z.co.y*40) + ' ' + str(z.co.z*40) + '\n')
        # Create faces
        f.write("\tfaces\n")

        
        # Retrieves all faces for the object 
        # for index, faces in enumerate(obj.polygons):
        #     f.write("\t\t0.000000 0.000000 0.000000 0.000000 0.000000 ")
            
        #     # This is a simple check to make sure when setting vertices it dosn't reuse one
        #     usedKey = 0

        #     for key in faces.edge_keys:
        #         if (usedKey < 3):
        #             f.write(str(key) + " ")
        #             usedKey += 1
        #         else:
        #             f.write(str(key) + " ")


        #     f.write("common/caulk\n")
            

        face_index_pairs = [(face, index) for index, face in enumerate(obj.polygons)]    
        for d, f_index in face_index_pairs:

            f.write("\t\t0.000000 0.000000 0.000000 0.000000 0.000000 ")
            f_v = [(vi, obj.vertices[v_idx], l_idx)
                for vi, (v_idx, l_idx) in enumerate(zip(d.vertices, d.loop_indices))]
          
            for vi, d, li in f_v:
                f.write(" %d" % (d.index) + " ")
            f.write("0x00000000\n")


    f.close()

    return {'FINISHED'}


# ExportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator


class ExportSomeData(Operator, ExportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "reflex.map"  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = "Reflex Export Settings"

    # ExportHelper mixin class uses this
    filename_ext = ".map"

    filter_glob = StringProperty(
            default="*.map",
            options={'HIDDEN'},
            maxlen=255,  # Max internal buffer length, longer would be clamped.
            )
    def execute(self, context):
        return writeMap(context, self.filepath)


# Only needed if you want to add into a dynamic menu
def menu_func_export(self, context):
    self.layout.operator(ExportSomeData.bl_idname, text="Reflex .map")


def register():
    bpy.utils.register_class(ExportSomeData)
    bpy.types.INFO_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_class(ExportSomeData)
    bpy.types.INFO_MT_file_export.remove(menu_func_export)


if __name__ == "__main__":
    register()