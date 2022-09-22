"""Demo models to use for testing"""
from ...interfaces import *

EXAMPLE_MODELS = {
    "TJoint": Model(
        name="TJoint",
        joint=Joint(
            name="TJoint",
            master=Tubular(
                name="Vertical",
                axis=Axis3D(
                    point=Point3D(x=0, y=0, z=0), vector=Vector3D(x=0, y=0, z=5)
                ),
                diameter=0.5,
            ),
            slaves=[
                Tubular(
                    name="Horizontal",
                    axis=Axis3D(
                        point=Point3D(x=0.25, y=0, z=3), vector=Vector3D(x=3, y=0, z=0)
                    ),
                    diameter=0.25,
                ),
            ],
        ),
    ),
    "KJoint": Model(
        name="KJoint",
        joint=Joint(
            name="KJoint",
            master=Tubular(
                name="Chord",
                axis=Axis3D(
                    point=Point3D(x=0, y=0, z=0), vector=Vector3D(x=0, y=0, z=5)
                ),
                diameter=0.6,
            ),
            slaves=[
                # Tubular(
                #     name="Brace1",
                #     axis=Axis3D(
                #         point=Point3D(x=0, y=0, z=3.5), vector=Vector3D(x=2, y=2, z=2)
                #     ),
                #     diameter=0.25,
                # ),
                # Tubular(
                #     name="Brace2",
                #     axis=Axis3D(
                #         point=Point3D(x=0, y=0, z=3.5), vector=Vector3D(x=2, y=-2, z=2)
                #     ),
                #     diameter=0.25,
                # ),
                # Tubular(
                #     name="Brace3",
                #     axis=Axis3D(
                #         point=Point3D(x=0, y=0, z=2.5), vector=Vector3D(x=2, y=2, z=-2)
                #     ),
                #     diameter=0.4,
                # ),
                Tubular(
                    name="Brace4",
                    axis=Axis3D(
                        point=Point3D(x=0, y=0, z=2.5), vector=Vector3D(x=2, y=-2, z=-2)
                    ),
                    diameter=0.4,
                ),
            ],
        ),
    ),
}
