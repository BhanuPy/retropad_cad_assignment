# profile_references.py
from retropad_common import load_reference_with_build123d

for part in ["bottom_shell", "button", "d_pad", "top_shell"]:
    mesh = load_reference_with_build123d(part)
    bbox = mesh.bounding_box()
    
    print(f"=== {part.upper()} ===")
    print(f"Size X (Width):  {bbox.size.X:.2f} mm")
    print(f"Size Y (Length): {bbox.size.Y:.2f} mm")
    print(f"Size Z (Height): {bbox.size.Z:.2f} mm")
    print(f"Center Point:    ({bbox.center().X:.2f}, {bbox.center().Y:.2f}, {bbox.center().Z:.2f})")
    print("-" * 30)