shader_type spatial;

void fragment() {
	ALBEDO = vec3(0.0,0.0,0.0);
}

void light() {
	float l = DIFFUSE_LIGHT.g + (clamp(dot(NORMAL, LIGHT), 0.0, 1.0) * vec3(0.,ATTENUATION.g, 0.)).g;
	DIFFUSE_LIGHT = vec3(1.0,l,0.0);
}