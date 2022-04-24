#include "Common.glsl"

uniform sampler2D samplerPGBuffer;
uniform vec3 litColor = vec3(1,0.2,0.2);
uniform vec3 unlitColor = vec3(0.8,0,0);
uniform vec3 backgroundColor = vec3(0.7);

#ifdef VERTEX_SHADER
void main()
{
	DEFAULT_SCREEN_VERTEX_SHADER();
}
#endif

#ifdef PIXEL_SHADER

layout (location = 0) out vec4 RESULT;
void main()
{
	PIXEL_SETUP_INPUT();

	vec4 pgbufferSample = texture(samplerPGBuffer, UV[0]);

	RESULT = vec4(mix(backgroundColor, mix(unlitColor, litColor, step(0.2, pgbufferSample.g)), pgbufferSample.r), 1);
}
#endif
