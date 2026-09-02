from build123d import *
from retropad_common import export_with_build123d

def build_parametric_top_shell():
    width = 135.00
    length = 53.00
    height  = 14.82
    wall_thickness = 1  
    chamfer_size = 10.0  
    
    with BuildPart() as top_shell:

        # =====================================================
        # 1. OUTER BODY
        # =====================================================
        with Locations((0, -1.0, 0)):
            with BuildSketch():
                Rectangle(width, length)
                chamfer(vertices(), length=chamfer_size)
            extrude(amount=height)

        # =====================================================
        # 1.5. TOP FACE BEVEL (3D CHAMFER)
        # =====================================================
        top_edges = [e for e in top_shell.edges() if e.center().Z > height - 0.1]
        chamfer(top_edges, length=3.2)
        
        # =====================================================
        # 2. HOLLOW BY SUBTRACTION (CORE & CAVITY)
        # =====================================================
        roof_thickness = 4.0  
        
        bottom_face = top_shell.faces().sort_by(Axis.Z)[0]
        
        with BuildSketch(bottom_face):
            offset(bottom_face, amount=-wall_thickness, kind=Kind.INTERSECTION)
            
        # The minus sign ensures it cuts UPWARD into the solid body
        extrude(amount=-(height - roof_thickness), mode=Mode.SUBTRACT)
        
                
        # =========================================================
        # ALL UI FEATURES INHERIT THE (0, -1.0) MASTER OFFSET
        # =========================================================
        inner_roof_z = height - roof_thickness  
        feature_height = 6.5  
        
        with Locations((0, -1.0, 0)):
            
            # =====================================================
            # 3. EXTERNAL BUTTON CUTOUTS 
            # =====================================================
            
            # D-Pad Cross (Cutters are 15mm tall to blast through the 4mm roof)
            with Locations((-38.0, 2, height)):
                Box(30.0, 10.0, 15.0, align=(Align.CENTER, Align.CENTER, Align.CENTER), mode=Mode.SUBTRACT)
                Box(10.0, 27.0, 15.0, align=(Align.CENTER, Align.CENTER, Align.CENTER), mode=Mode.SUBTRACT)

             # Four Button Cutouts
            vertical_btn_dist = 8.5 
            horizonatl_btn_dist = 10
            btn_radius = 5.0
            with Locations(
                (38.0, 2.0 + vertical_btn_dist, height),   
                (38.0, 2.0 - vertical_btn_dist, height),  
                (38.0 - horizonatl_btn_dist, 2.0, height), 
                (38.0 + horizonatl_btn_dist, 2.0, height)  
            ):
                Cylinder(radius=btn_radius, height=15.0, align=(Align.CENTER, Align.CENTER, Align.CENTER), mode=Mode.SUBTRACT)


            # =====================================================
            # 4. INTERNAL FEATURES (RINGS & POSTS)
            # =====================================================
            
            # 1. Create a custom drawing plane locked exactly at the D-Pad coordinates!
            # This guarantees the sketch can NEVER jump back to the center (0,0).
            dpad_plane = Plane(origin=(-38.0, 1.0, inner_roof_z))
            
            with BuildSketch(dpad_plane):
                
                # 2. Outer Wall (Notice X is wider than Y to create an oval!)
                Ellipse(x_radius=17, y_radius=15.0)
                
                # 3. Inner Hole
                Ellipse(x_radius=16.0, y_radius=14.5, mode=Mode.SUBTRACT)
                
            # 4. Extrude the 2D oval downwards into a 3D sleeve
            extrude(amount=-feature_height)    
            # Four Button Guide Rings 
            # --- 2. Four Button Guide Rings (With Anti-Rotation Slots!) ---
            with Locations(
                (38.0, 2.0 + vertical_btn_dist, inner_roof_z),   
                (38.0, 2.0 - vertical_btn_dist, inner_roof_z),  
                (38.0 - horizonatl_btn_dist, 2.0, inner_roof_z), 
                (38.0 + horizonatl_btn_dist, 2.0, inner_roof_z)  
            ):
                # 1. Base Solid Ring
                Cylinder(radius=6.0, height=feature_height, align=(Align.CENTER, Align.CENTER, Align.MAX))
                
                # 2. Hollow Inner Hole
                Cylinder(radius=btn_radius, height=feature_height, align=(Align.CENTER, Align.CENTER, Align.MAX), mode=Mode.SUBTRACT)

                # 3. The 4 Vertical Anti-Rotation Slots!
                # We subtract two crossing boxes to slice 4 gaps into the cylinder walls.
                slot_width = 2.0  
                Box(16.0, slot_width, feature_height, align=(Align.CENTER, Align.CENTER, Align.MAX), mode=Mode.SUBTRACT)
                Box(slot_width, 16.0, feature_height, align=(Align.CENTER, Align.CENTER, Align.MAX), mode=Mode.SUBTRACT)

           # Central Support Post
            central_post_plane = Plane(origin=(0.0, -11.5, inner_roof_z))
            # with Locations((0.0, , inner_roof_z)):
            with BuildSketch(central_post_plane):
                # 1. Base solid circle
                Circle(radius=4.0)
                
                # 2. Subtract the hole (Inner circle)
                Circle(radius=2.6, mode=Mode.SUBTRACT)
            
            # Extrude to make it 3D
            extrude(amount=-(feature_height+4))

            # Corner Screw Boss Receptacles
            boss_x = 52.5
            boss_y = 14.5

            with Locations(
                ( boss_x,  boss_y, inner_roof_z),
                (-boss_x,  boss_y, inner_roof_z),
                ( boss_x, -boss_y+4, inner_roof_z),
                (-boss_x, -boss_y+4, inner_roof_z),
            ):
                Cylinder(
                    radius=2.5,
                    height=feature_height+4,
                    align=(Align.CENTER, Align.CENTER, Align.MAX)
                )

                Cylinder(
                    radius=1,
                    height=feature_height+4,
                    align=(Align.CENTER, Align.CENTER, Align.MAX),
                    mode=Mode.SUBTRACT
                )
                
            # =====================================================
            # 5. CENTRAL U-SHAPE WALL ENCLOSURE
            # =====================================================

            slot_width = 37.0

            u_wall = 2.0

            # Measured from overlay
            u_gap = 31.0

            outer_width = u_gap + (u_wall * 2)

            # Reduced from 20.0
            u_length = 21.0

            internal_drop = feature_height + 4.0

            # Moved backward from Y=25.0
            u_wall_plane = Plane(
                origin=(0.0, 24, inner_roof_z)
            )

            with Locations(u_wall_plane):

                # Outer U body
                Box(
                    outer_width,
                    u_length,
                    internal_drop,
                    align=(
                        Align.CENTER,
                        Align.MAX,
                        Align.MAX
                    )
                )

                # Inner cavity
                Box(
                    u_gap,
                    u_length - u_wall,
                    internal_drop + 1.0,
                    align=(
                        Align.CENTER,
                        Align.MAX,
                        Align.MAX
                    ),
                    mode=Mode.SUBTRACT
                )
            # =====================================================
            # 6. CABLE SLOT
            # =====================================================
            slot_y = 30

            with Locations((0, slot_y, 0)):
                Box(
                    slot_width,
                    10.0,
                    height + 5.0,
                    align=(
                        Align.CENTER,
                        Align.CENTER,
                        Align.MIN
                    ),
                    mode=Mode.SUBTRACT
                )

    return top_shell.part

if __name__ == "__main__":
    shape = build_parametric_top_shell()
    export_with_build123d(shape, "top_shell")
    print("Top shell successfully generated! All features aligned and properly hollowed.")