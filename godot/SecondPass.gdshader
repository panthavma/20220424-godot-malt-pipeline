shader_type canvas_item;

uniform sampler2D bufferPG : hint_black;
uniform vec3 backgroundColor = vec3(0.7,0.7,0.7);
uniform vec3 unlitColor = vec3(0.8,0.0,0.0);
uniform vec3 litColor = vec3(1.0,0.2,0.2);

void fragment() {
	vec4 samplePG = texture(bufferPG, SCREEN_UV);
	COLOR = vec4(mix(backgroundColor, mix(unlitColor, litColor, step(0.2, samplePG.g)), samplePG.r), 1.0);
}