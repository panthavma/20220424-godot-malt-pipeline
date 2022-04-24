#include "Common.glsl"
#include "Lighting/Lighting.glsl"
#include "Shading/ShadingModels.glsl"

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

    LitSurface ls = lit_surface(IO_POSITION, IO_NORMAL, LIGHTS.lights[0], false);
	vec3 shading = diffuse_lit_surface(ls);
    float lightCoef = (0.2126*shading.r + 0.7152*shading.g + 0.0722*shading.b);

    RESULT = vec4(1, lightCoef, 0, 1);
}
#endif
