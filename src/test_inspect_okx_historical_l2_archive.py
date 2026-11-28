import io
import tarfile
import tempfile
import unittest
from pathlib import Path

from inspect_okx_historical_l2_archive import _first_member_preview


class HistoricalL2ArchiveTests(unittest.TestCase):
    def test_inspects_tar_gz_member_prefix(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.tar.gz"
            data = b'ts,bids,asks\n1000,"[[1,2]]","[[3,4]]"\n'
            with tarfile.open(path, "w:gz") as archive:
                info = tarfile.TarInfo("sample.csv")
                info.size = len(data)
                archive.addfile(info, io.BytesIO(data))
            result = _first_member_preview(path)
        self.assertEqual(result["member_count"], 1)
        self.assertEqual(result["first_member_name"], "sample.csv")
        self.assertEqual(result["preview_field_counts"], [3, 3])


if __name__ == "__main__":
    unittest.main()
