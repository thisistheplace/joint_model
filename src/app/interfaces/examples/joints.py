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
                    point=Point3D(x=0, y=0, z=-5), vector=Vector3D(x=0, y=0, z=10)
                ),
                diameter=0.5,
            ),
            slaves=[
                Tubular(
                    name="Horizontal",
                    axis=Axis3D(
                        point=Point3D(x=0.0, y=0.25, z=0),
                        vector=Vector3D(x=0, y=3, z=0),
                    ),
                    diameter=0.25,
                ),
            ],
        ),
    ),
    "TAngle": Model(
        name="TAngle",
        joint=Joint(
            name="TAngle",
            master=Tubular(
                name="Vertical",
                axis=Axis3D(
                    point=Point3D(x=0, y=0, z=-5), vector=Vector3D(x=0, y=0, z=10)
                ),
                diameter=0.5,
            ),
            slaves=[
                Tubular(
                    name="Horizontal",
                    axis=Axis3D(
                        point=Point3D(x=0.0, y=0.25, z=0),
                        vector=Vector3D(x=0, y=3, z=3),
                    ),
                    diameter=0.25,
                ),
            ],
        ),
    ),
    "TOffset": Model(
        name="TOffset",
        joint=Joint(
            name="TOffset",
            master=Tubular(
                name="Vertical",
                axis=Axis3D(
                    point=Point3D(x=0, y=0, z=-5), vector=Vector3D(x=0, y=0, z=10)
                ),
                diameter=0.5,
            ),
            slaves=[
                Tubular(
                    name="Horizontal",
                    axis=Axis3D(
                        point=Point3D(x=0.1, y=0.1, z=0), vector=Vector3D(x=0, y=3, z=0)
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
                    point=Point3D(x=0, y=0, z=-5), vector=Vector3D(x=0, y=0, z=10)
                ),
                diameter=0.6,
            ),
            slaves=[
                Tubular(
                    name="Brace1",
                    axis=Axis3D(
                        point=Point3D(x=0.3, y=0.3, z=1), vector=Vector3D(x=2, y=2, z=2)
                    ),
                    diameter=0.25,
                ),
                Tubular(
                    name="Brace2",
                    axis=Axis3D(
                        point=Point3D(x=-0.3, y=0.3, z=1),
                        vector=Vector3D(x=-2, y=2, z=2),
                    ),
                    diameter=0.25,
                ),
                Tubular(
                    name="Brace3",
                    axis=Axis3D(
                        point=Point3D(x=0.3, y=0.3, z=-1),
                        vector=Vector3D(x=2, y=2, z=-2),
                    ),
                    diameter=0.4,
                ),
                Tubular(
                    name="Brace4",
                    axis=Axis3D(
                        point=Point3D(x=-0.3, y=0.3, z=-1),
                        vector=Vector3D(x=-2, y=2, z=-2),
                    ),
                    diameter=0.4,
                ),
            ],
        ),
    ),
}
