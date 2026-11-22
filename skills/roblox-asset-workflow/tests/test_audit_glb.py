"""GLB auditor regression tests with synthetic assets; no Blender or Roblox needed."""
import json
import struct
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.audit_glb import audit, read_glb, uv_bounds

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "audit_glb.py"


def fixture(uv=(0.0, 0.0, 1.0, 1.0, 0.2, 0.8), *,
            second_material=False, external_image=False, extension=False):
    uv_data = struct.pack("<6f", *uv)
    indices = struct.pack("<3H", 0, 1, 2)
    binary = uv_data + indices
    primitive = {"attributes": {"POSITION": 0, "TEXCOORD_0": 1},
                 "indices": 2, "material": 0}
    primitives = [primitive]
    if second_material:
        primitives.append({**primitive, "material": 1})
    doc = {"asset": {"version": "2.0"},
           "buffers": [{"byteLength": len(binary)}],
           "bufferViews": [
               {"buffer": 0, "byteOffset": 0, "byteLength": len(uv_data)},
               {"buffer": 0, "byteOffset": len(uv_data), "byteLength": len(indices)}],
           "accessors": [
               {"count": 3, "type": "VEC3", "componentType": 5126},
               {"count": 3, "type": "VEC2", "componentType": 5126, "bufferView": 0},
               {"count": 3, "type": "SCALAR", "componentType": 5123, "bufferView": 1}],
           "meshes": [{"name": "Body", "primitives": primitives}],
           "images": [{"uri": "paint.png"}] if external_image else
                     [{"bufferView": 0, "mimeType": "image/png"}]}
    if extension:
        doc["extensionsUsed"] = ["KHR_materials_emissive_strength"]
    return doc, binary


def encode_glb(doc, binary):
    payload = json.dumps(doc, separators=(",", ":")).encode("utf-8")
    payload += b" " * (-len(payload) % 4)
    binary += b"\0" * (-len(binary) % 4)
    length = 12 + 8 + len(payload) + 8 + len(binary)
    return (struct.pack("<4sII", b"glTF", 2, length)
            + struct.pack("<II", len(payload), 0x4E4F534A) + payload
            + struct.pack("<II", len(binary), 0x004E4942) + binary)


class AuditGlbTests(unittest.TestCase):
    def run_cli(self, path, *args):
        return subprocess.run([sys.executable, str(SCRIPT), str(path), *args],
                              capture_output=True, text=True)

    def test_clean_bounds_triangles_and_errors(self):
        doc, data = fixture()
        report = audit(doc, data)
        self.assertEqual(report["mesh_triangles_total"], 1)
        self.assertEqual(report["uv_primitives_checked"], 1)
        self.assertEqual(report["errors"], [])
        self.assertEqual(report["warnings"], [])
        self.assertEqual(uv_bounds(doc, data, 1), (0.0, 1.0))

    def test_informative_warnings_not_errors(self):
        doc, data = fixture(uv=(-0.5, 0, 2, 0, 0.2, 0.8),
                            second_material=True, extension=True)
        warnings = " ".join(audit(doc, data)["warnings"])
        for expected in ("outside [0,1]", "2 materials", "Extension"):
            self.assertIn(expected, warnings)
        self.assertEqual(audit(doc, data)["errors"], [])

    def test_missing_uv_is_warning(self):
        doc, data = fixture()
        del doc["accessors"][1]["bufferView"]
        self.assertIsNone(uv_bounds(doc, data, 1))
        self.assertIn("could not be decoded", " ".join(audit(doc, data)["warnings"]))

    def test_index_outside_position_is_error(self):
        doc, data = fixture()
        data = data[:24] + struct.pack("<3H", 0, 1, 4)
        self.assertIn("index 4 outside", " ".join(audit(doc, data)["errors"]))

    def test_incomplete_index_list_is_error(self):
        doc, data = fixture()
        doc["accessors"][2]["count"] = 2
        self.assertIn("incomplete triangle", " ".join(audit(doc, data)["errors"]))

    def test_over_budget_is_error(self):
        doc, data = fixture()
        doc["accessors"][2]["count"] = 60_003
        self.assertIn("20000", " ".join(audit(doc, data)["errors"]))

    def test_node_scale_and_mirrored_matrix_warnings(self):
        doc, data = fixture()
        doc["nodes"] = [{"name": "Wheel", "scale": [-1, 1.5, 1]},
                        {"name": "Body", "matrix": [-1, 0, 0, 0, 0, 1, 0, 0,
                                                    0, 0, 1, 0, 0, 0, 0, 1]}]
        messages = " ".join(audit(doc, data)["warnings"])
        self.assertIn("negative scale", messages)
        self.assertIn("non-unit scale", messages)
        self.assertIn("mirrored node matrix", messages)

    def test_external_image_exists_or_missing(self):
        doc, data = fixture(external_image=True)
        with tempfile.TemporaryDirectory() as folder:
            glb = Path(folder) / "test.glb"
            self.assertIn("texture missing", " ".join(audit(doc, data, glb)["errors"]))
            (Path(folder) / "paint.png").write_bytes(b"test")
            report = audit(doc, data, glb)
            self.assertEqual(report["errors"], [])
            self.assertIn("not packed", " ".join(report["warnings"]))

    def test_cli_strict_ignores_review_warnings_and_creates_folder(self):
        doc, data = fixture(extension=True)
        with tempfile.TemporaryDirectory() as folder:
            glb = Path(folder) / "test.glb"
            glb.write_bytes(encode_glb(doc, data))
            output = Path(folder) / "reports" / "glb-audit.json"
            result = self.run_cli(glb, "--strict", "--output", str(output))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(output.is_file())
            self.assertEqual(json.loads(output.read_text())["errors"], [])

    def test_cli_strict_fails_missing_texture_only_and_retains_report(self):
        doc, data = fixture(external_image=True)
        with tempfile.TemporaryDirectory() as folder:
            glb = Path(folder) / "test.glb"
            glb.write_bytes(encode_glb(doc, data))
            report_path = Path(folder) / "reports" / "audit.json"
            result = self.run_cli(glb, "--strict", "--output", str(report_path))
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertIn("texture missing", " ".join(json.loads(report_path.read_text())["errors"]))

    def test_roundtrip_and_invalid_file(self):
        doc, data = fixture()
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "test.glb"
            path.write_bytes(encode_glb(doc, data))
            self.assertEqual(read_glb(path)[0]["meshes"][0]["name"], "Body")
            path.write_bytes(b"invalid")
            with self.assertRaises(ValueError):
                read_glb(path)
            self.assertEqual(self.run_cli(path, "--strict").returncode, 2)


if __name__ == "__main__":
    unittest.main()
