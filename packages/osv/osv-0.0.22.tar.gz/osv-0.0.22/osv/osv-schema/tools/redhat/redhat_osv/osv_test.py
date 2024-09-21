"""Test Intermediate OSV object creation"""
import unittest

from redhat_osv.csaf import CSAF
from redhat_osv.osv import OSV, Event


class ScoreTest(unittest.TestCase):
    """Tests OSV vulnerability scores"""

    def test_missing_cvss_v3(self):
        """Test parsing a CSAF file with missing CVSSv3 score"""
        csaf_file = "testdata/rhsa-2015_0008.json"
        with open(csaf_file, "r", encoding="utf-8") as fp:
            csaf_data = fp.read()
        csaf = CSAF(csaf_data)
        assert csaf
        assert len(csaf.vulnerabilities) == 1
        assert not csaf.vulnerabilities[0].cvss_v3_base_score

        osv = OSV(csaf, "test_date")
        assert not hasattr(osv, "severity")


class EventTest(unittest.TestCase):
    """ Tests OSV affected range events"""

    def test_init_event(self):
        """Test parsing various Events"""
        event = Event("introduced")
        assert event.event_type == "introduced"
        assert event.version == "0"

        event = Event("fixed", "1")
        assert event.event_type == "fixed"
        assert event.version == "1"

        with self.assertRaises(ValueError):
            Event("test")


if __name__ == '__main__':
    unittest.main()
