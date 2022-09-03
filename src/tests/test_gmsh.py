import sys
sys.path.append("/src")

from app.joint_model.geometry.mesh import make_mesh

class TestGmshAccess:

    def test_test():
        assert 1 == 1

    def test_make_mesh():
        make_mesh()