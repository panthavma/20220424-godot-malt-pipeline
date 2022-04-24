from os import path

from Malt.GL.GL import *
from Malt.GL.Mesh import Mesh
from Malt.GL.RenderTarget import RenderTarget
from Malt.GL.Shader import Shader, UBO
from Malt.GL.Texture import Texture

from Malt.Pipeline import *
from Malt.Render import Lighting

class PipelineMaltToGodot(Pipeline):
    DEFAULT_SHADER = None

    def __init__(self, plugins=[]):
        super().__init__(plugins)

        if PipelineMaltToGodot.DEFAULT_SHADER is None:
            source = '''
            #include "Common.glsl"

            #ifdef VERTEX_SHADER
            void main()
            {
                DEFAULT_VERTEX_SHADER();
            }
            #endif

            #ifdef PIXEL_SHADER
            layout (location = 0) out vec4 RESULT;
            void main()
            {
                PIXEL_SETUP_INPUT();
                RESULT = vec4(1);
            }
            #endif
            '''
            PipelineMaltToGodot.DEFAULT_SHADER = self.compile_material_from_source('mesh', source)
        self.default_shader = PipelineMaltToGodot.DEFAULT_SHADER

        # Load the lights
        self.lights_buffer = Lighting.get_lights_buffer()

        # Add the material to hold the second pass's shader
        self.parameters.world['Second Pass Material'] = MaterialParameter('', '.screen.glsl')

    def compile_material_from_source(self, material_type, source, include_paths=[]):
        return {
            'MAIN_PASS' : self.compile_shader_from_source(
                source, include_paths, ['MAIN_PASS']
            )
        }

    def setup_render_targets(self, resolution):
        self.t_pgbuffer_depth = Texture(resolution, GL_DEPTH_COMPONENT32F)
        self.t_pgbuffer = Texture(resolution, GL_RGBA32F)
        self.rt_pgbuffer = RenderTarget([self.t_pgbuffer], self.t_pgbuffer_depth)

        self.t_secondpass = Texture(resolution, GL_RGBA32F)
        self.rt_secondpass = RenderTarget([self.t_secondpass])

    def do_render(self, resolution, scene, is_final_render, is_new_frame):
        shader_resources = { 'COMMON_UNIFORMS' : self.common_buffer }

        self.rt_pgbuffer.clear([(0,0,0,0)], 1)
        self.rt_secondpass.clear([(0,0,0,0)])

        # **First pass**
        # Load the lights (Sun CSM Count, Sun CSM Distribution, Sun Max Distance)
        self.lights_buffer.load(scene, 4, 0.9, 100.0)
        shader_resources['SCENE_LIGHTS'] = self.lights_buffer

        self.draw_scene_pass(self.rt_pgbuffer, scene.batches, 'MAIN_PASS', self.default_shader['MAIN_PASS'], shader_resources)

        # **Second Pass**
        SecondPassMaterial = scene.world_parameters['Second Pass Material']
        if SecondPassMaterial and SecondPassMaterial.shader:
            SecondPassMaterial.shader['MAIN_PASS'].textures['samplerPGBuffer'] = self.t_pgbuffer

            self.draw_screen_pass(SecondPassMaterial.shader['MAIN_PASS'], self.rt_secondpass, shader_resources)
        else:
            return { 'COLOR' : self.t_pgbuffer}

        return { 'COLOR' : self.t_secondpass }


PIPELINE = PipelineMaltToGodot
