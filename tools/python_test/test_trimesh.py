import importlib.metadata
import trimesh

def main():
    # Verify Version
    version = importlib.metadata.version('trimesh')
    print(f"trimesh version: {version}")

    try:
        # Create a basic 3D primitive (Icosahedron)
        print("Generating a 3D icosahedron mesh...")
        mesh = trimesh.creation.icosahedron()
        
        # Perform a basic mesh operation (subdivision)
        print(f"Original mesh: {len(mesh.faces)} faces, {len(mesh.vertices)} vertices.")
        mesh = mesh.subdivide()
        print(f"Subdivided mesh: {len(mesh.faces)} faces, {len(mesh.vertices)} vertices.")
        
        # Check for watertightness (a core feature of trimesh)
        if mesh.is_watertight:
            print("Success: Mesh generated, manipulated, and validated as watertight.")
        else:
            print("Warning: Mesh generated but is not watertight.")
            
    except Exception as e:
        print(f"Test failed with exception: {e}")

if __name__ == '__main__':
    main()
