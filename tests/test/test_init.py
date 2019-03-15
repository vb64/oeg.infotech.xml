"""
make test T=test_init
"""
from . import TestInfotech


class TestInit(TestInfotech):
    """
    Infotech core function
    """
    def test_reverse_orient(self):
        """
        reverse_orient
        """
        from oeg_infotech import reverse_orient

        self.assertEqual(reverse_orient(''), '')
        self.assertEqual(reverse_orient('0'), '0,0')
        self.assertEqual(reverse_orient('6.0'), '6,0')
        self.assertEqual(reverse_orient('3.0'), '9,0')
        self.assertEqual(reverse_orient('3.5'), '8,5')
        self.assertEqual(reverse_orient('9.0'), '3,0')
        self.assertEqual(reverse_orient('9.5'), '2,5')

    def test_infotech(self):
        """
        package
        """
        from oeg_infotech import Infotech

        info = Infotech.from_file(self.fixture('1736.xml'))
        self.assertEqual(info.total_dist(), 17727)

        self.assertEqual(len(info.obj_dict), 15)
        self.assertEqual(len(info.defects.items), 10)
        self.assertEqual(len(info.lineobjects.items), 6)
        self.assertEqual(len(info.welds.items), 23)
        # cached access
        self.assertEqual(len(info.defects.items), 10)
        self.assertEqual(len(info.lineobjects.items), 6)

        self.assertIn('IPL_INSPECT', "{}".format(info))

    def test_navigation(self):
        """
        navigation
        """
        from oeg_infotech import Infotech

        info = Infotech.from_file(self.fixture('navigation.xml'))
        self.assertIn('IPL_INSPECT', info.reverse())

    def test_orient_to_str(self):
        """
        orient_to_str
        """
        from oeg_infotech import orient_to_str

        self.assertEqual(orient_to_str(-1), '')
        self.assertEqual(orient_to_str(0), '0.0')
        self.assertEqual(orient_to_str(617), '10.3')
        self.assertEqual(orient_to_str(72), '1.2')
