"""
make test T=test_danger
"""
from . import TestInfotech


class TestDanger(TestInfotech):
    """Defects danger stuff."""

    def check_stats(self, info, val_types, val_methods, counts):
        """Test check_stats."""
        from oeg_infotech.base import DistItem
        from oeg_infotech import defect

        stats_values, stats_counts = info.defects.danger_stats()

        self.assert_list(stats_values[DistItem.field_typeobj], val_types)
        self.assert_list(stats_values[defect.Item.field_method_id], val_methods)
        for item in counts:
            assert stats_counts[item] == counts[item]

    def test_danger_stats(self):
        """Test danger_stats."""
        from oeg_infotech import Infotech, defect, codes

        self.check_stats(
          Infotech.from_file(self.fixture('1827.xml')),
          [
            codes.Feature.METALL_LOSS,
            codes.Feature.KANAVKA_HOR,
            codes.Feature.CAVERNA,
            codes.Feature.KANAVKA_VERT,
          ],
          [
            codes.MethodsKBD.GAZNADZOR2013,
          ],
          {
            defect.Item.field_kbd: 136,
            defect.Item.field_safe_pressure: 0,
            defect.Item.field_time_limit: 136,
            defect.Item.field_safe_pressure_persent: 0,
            defect.Item.field_method_id: 136,
          }
        )
