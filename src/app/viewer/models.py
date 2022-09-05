"""Demo models to use for testing"""
from ..interfaces import *

DEMO_MODELS = {
    "TJoint":
        Joint(
            name="TJoint",
            tubes=[
                Tubular(
                    name="Vertical",
                    axis= Axis3D(
                        point=Point3D(
                            x=0,
                            y=0,
                            z=0
                        ),
                        vector=Vector3D(
                            x=0,
                            y=0,
                            z=5
                        )
                    ),
                    diameter=0.5
                ),
                Tubular(
                    name="Horizontal",
                    axis= Axis3D(
                        point=Point3D(
                            x=0,
                            y=0,
                            z=3
                        ),
                        vector=Vector3D(
                            x=3,
                            y=0,
                            z=0
                        )
                    ),
                    diameter=0.25
                )
            ]
        ),
    "Tube":
        Tubular(
            name="test",
            axis= Axis3D(
                point=Point3D(
                    x=1,
                    y=1,
                    z=1
                ),
                vector=Vector3D(
                    x=0,
                    y=0,
                    z=3
                )
            ),
            diameter=0.5
        )
}