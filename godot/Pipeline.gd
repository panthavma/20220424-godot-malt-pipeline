extends "res://oddlib-shaders/pipeline/OLSPipeline.gd"

var secondPassMaterial = preload("res://SecondPassMaterial.tres")

func Setup():
	AddPGBuffer("First Pass")
	AddParameterVPTexture("Second Pass/PG Buffer", "bufferPG", "First Pass")
