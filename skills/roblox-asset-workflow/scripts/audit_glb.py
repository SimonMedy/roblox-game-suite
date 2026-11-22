#!/usr/bin/env python3
"""Read-only glTF 2.0 GLB preflight; never a substitute for Roblox Studio import."""
from __future__ import annotations

import argparse
import json
import math
import struct
from pathlib import Path
from urllib.parse import unquote, urlsplit

JSON_CHUNK = 0x4E4F534A
BIN_CHUNK = 0x004E4942
COMPONENTS = {5120: "b", 5121: "B", 5122: "h", 5123: "H", 5125: "I", 5126: "f"}
BYTES = {5120: 1, 5121: 1, 5122: 2, 5123: 2, 5125: 4, 5126: 4}
MAX_MESH_TRIANGLES = 20_000


def read_glb(path: Path) -> tuple[dict, bytes]:
    raw = path.read_bytes()
    if len(raw) < 20:
        raise ValueError("File too short for GLB")
    magic, version, length = struct.unpack_from("<4sII", raw)
    if magic != b"glTF" or version != 2 or length != len(raw):
        raise ValueError("Invalid GLB magic, version or declared length")
    offset, json_bytes, binary = 12, None, b""
    while offset < len(raw):
        if offset + 8 > len(raw):
            raise ValueError("Incomplete GLB chunk header")
        chunk_len, chunk_type = struct.unpack_from("<II", raw, offset)
        offset += 8
        if chunk_len % 4 or offset + chunk_len > len(raw):
            raise ValueError("Invalid GLB chunk length")
        chunk = raw[offset:offset + chunk_len]
        offset += chunk_len
        if chunk_type == JSON_CHUNK and json_bytes is None:
            json_bytes = chunk
        elif chunk_type == BIN_CHUNK and not binary:
            binary = chunk
    if json_bytes is None:
        raise ValueError("Missing JSON chunk")
    document = json.loads(json_bytes.decode("utf-8").rstrip(" \t\r\n\0"))
    if not isinstance(document, dict) or document.get("asset", {}).get("version") != "2.0":
        raise ValueError("Missing glTF 2.0 metadata")
    return document, binary


def _values(document: dict, binary: bytes, accessor_id: int, components: int):
    """Iterate only supported dense BIN-backed accessors; fail safely on broken bounds."""
    acc = document["accessors"][accessor_id]
    if ("sparse" in acc or "bufferView" not in acc or
            acc.get("type") != ("VEC2" if components == 2 else "SCALAR")):
        raise ValueError("unsupported sparse or missing bufferView/accessor type")
    kind = acc["componentType"]
    if kind not in COMPONENTS or (components == 1 and kind not in (5121, 5123, 5125)):
        raise ValueError("unsupported accessor component type")
    view = document["bufferViews"][acc["bufferView"]]
    buffers = document.get("buffers", [])
    if view.get("buffer", 0) != 0 or not buffers or buffers[0].get("uri"):
        raise ValueError("accessor does not reference embedded BIN chunk")
    count = acc["count"]
    if not isinstance(count, int) or count < 0:
        raise ValueError("invalid accessor count")
    width = components * BYTES[kind]
    stride = view.get("byteStride", width)
    start = view.get("byteOffset", 0) + acc.get("byteOffset", 0)
    end = view.get("byteOffset", 0) + view["byteLength"]
    if (stride < width or start < view.get("byteOffset", 0) or
            (count and start + (count - 1) * stride + width > min(end, len(binary)))):
        raise ValueError("accessor outside its buffer view or binary chunk")
    fmt = "<" + components * COMPONENTS[kind]
    for i in range(count):
        yield struct.unpack_from(fmt, binary, start + i * stride)


def uv_bounds(document: dict, binary: bytes, accessor_id: int) -> tuple[float, float] | None:
    """UV0 bounds for dense VEC2 BIN-backed accessors (sparse: manual review)."""
    try:
        kind = document["accessors"][accessor_id]["componentType"]
        normalized = document["accessors"][accessor_id].get("normalized", False)
        values = []
        for pair in _values(document, binary, accessor_id, 2):
            if normalized and kind != 5126:
                bits = BYTES[kind] * 8
                signed = kind in (5120, 5122)
                top = float((1 << (bits - int(signed))) - 1)
                values.extend(max(float(v) / top, -1) if signed else float(v) / top for v in pair)
            else:
                values.extend(pair)
        return (min(values), max(values)) if values else None
    except (IndexError, KeyError, TypeError, ValueError, struct.error):
        return None


def _inspect_indices(doc: dict, binary: bytes, accessor_id: int, vertex_count: int) -> str | None:
    """Return a blocking index error, or None; unsupported sparse indices are reported."""
    acc = doc["accessors"][accessor_id]
    if "sparse" in acc:
        return "sparse indices not decoded; verify with glTF validator"
    try:
        for (index,) in _values(doc, binary, accessor_id, 1):
            if index >= vertex_count:
                return f"index {index} outside POSITION count {vertex_count}"
    except (IndexError, KeyError, TypeError, ValueError, struct.error) as exc:
        return f"invalid index accessor: {exc}"
    return None


def _node_warnings(node: dict, ordinal: int) -> list[str]:
    name = node.get("name") or f"node_{ordinal}"
    result = []
    scale = node.get("scale")
    if scale is not None:
        if len(scale) != 3:
            return [f"{name}: malformed node scale"]
        if any(v < 0 for v in scale):
            result.append(f"{name}: negative scale/mirroring; check winding and normals in Studio")
        if any(abs(abs(v) - 1.0) > 1e-5 for v in scale):
            result.append(f"{name}: non-unit scale {scale}; verify export pivots and size")
    matrix = node.get("matrix")
    if matrix is not None:
        if len(matrix) != 16:
            return [f"{name}: malformed node matrix"]
        a, b, c = (matrix[0:3], matrix[4:7], matrix[8:11])
        dot = lambda u, v: sum(x*y for x, y in zip(u, v))
        cross = (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
        if dot(cross, c) < -1e-6:
            result.append(f"{name}: mirrored node matrix; check winding and normals in Studio")
        if any(abs(math.sqrt(dot(col, col)) - 1.0) > 1e-5 for col in (a, b, c)):
            result.append(f"{name}: non-unit node matrix scale; verify export pivots and size")
    return result


def audit(document: dict, binary: bytes, asset_path: Path | None = None) -> dict:
    """Errors block --strict; warnings only request review, including extensions and tiling."""
    errors: list[str] = []
    warnings: list[str] = []
    meshes = []
    uv_checked = 0
    for ordinal, mesh in enumerate(document.get("meshes", [])):
        name = mesh.get("name") or f"mesh_{ordinal}"
        triangles = 0
        materials: set[int] = set()
        primitives = mesh.get("primitives", [])
        for p, primitive in enumerate(primitives):
            label = f"{name}: primitive {p}"
            mode = primitive.get("mode", 4)
            attributes = primitive.get("attributes", {})
            position = attributes.get("POSITION")
            indices = primitive.get("indices")
            try:
                vertex_count = document["accessors"][position]["count"] if position is not None else 0
                count = document["accessors"][indices]["count"] if indices is not None else vertex_count
                if position is None or not isinstance(count, int) or count < 0:
                    raise ValueError("missing POSITION or invalid element count")
                if indices is not None:
                    issue = _inspect_indices(document, binary, indices, vertex_count)
                    if issue:
                        if issue.startswith("sparse"):
                            warnings.append(f"{label} {issue}")
                        else:
                            errors.append(f"{label} {issue}")
            except (IndexError, KeyError, TypeError, ValueError) as exc:
                errors.append(f"{label} missing/invalid accessor: {exc}")
                continue
            if mode == 4:
                triangles += count // 3
                if count % 3:
                    errors.append(f"{label} has incomplete triangle indices")
            elif mode in (5, 6):
                triangles += max(0, count - 2)
            else:
                warnings.append(f"{label} uses non-triangle mode {mode}")
            if "material" in primitive:
                materials.add(primitive["material"])
            if "TEXCOORD_0" not in attributes:
                warnings.append(f"{label} missing TEXCOORD_0 (check paint/skins)")
            else:
                bounds = uv_bounds(document, binary, attributes["TEXCOORD_0"])
                if bounds is None:
                    warnings.append(f"{label} UV0 could not be decoded; verify manually")
                else:
                    uv_checked += 1
                    if bounds[0] < -1e-5 or bounds[1] > 1 + 1e-5:
                        warnings.append(f"{label} UV0 outside [0,1]: {bounds}")
        if len(primitives) > 1:
            warnings.append(f"{name}: {len(primitives)} glTF primitives; verify Studio splitting/names")
        if len(materials) > 1:
            warnings.append(f"{name}: {len(materials)} materials; separate customizable parts or atlas")
        if triangles > MAX_MESH_TRIANGLES:
            errors.append(f"{name}: {triangles} triangles exceeds {MAX_MESH_TRIANGLES} per glTF mesh")
        meshes.append({"name": name, "triangles": triangles, "primitives": len(primitives),
                       "material_count": len(materials)})
    embedded = 0
    for i, item in enumerate(document.get("images", [])):
        if "bufferView" in item or item.get("uri", "").startswith("data:"):
            embedded += 1
            continue
        uri = item.get("uri", "")
        if not uri:
            errors.append(f"image {i}: no data URI or bufferView")
            continue
        parsed = urlsplit(uri)
        if parsed.scheme or parsed.netloc or not asset_path:
            warnings.append(f"image {i}: external URI not packed; verify availability: {uri}")
            continue
        image_path = asset_path.parent / unquote(parsed.path)
        if not image_path.is_file():
            errors.append(f"image {i}: referenced local texture missing: {uri}")
        else:
            warnings.append(f"image {i}: external local texture exists but is not packed: {uri}")
    for ext in document.get("extensionsUsed", []):
        warnings.append(f"Extension {ext}: verify import/appearance in Roblox Studio")
    for i, node in enumerate(document.get("nodes", [])):
        warnings.extend(_node_warnings(node, i))
    return {"mesh_count": len(meshes),
            "mesh_triangles_total": sum(m["triangles"] for m in meshes),
            "max_triangles_per_mesh": max((m["triangles"] for m in meshes), default=0),
            "uv_primitives_checked": uv_checked, "images_embedded": embedded,
            "images_total": len(document.get("images", [])),
            "extensions_used": document.get("extensionsUsed", []),
            "meshes": meshes, "errors": errors, "warnings": warnings,
            "limitations": "GLB preflight only; importer splits, visual fidelity, animation, pivots, and performance untested"}


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect GLB for Roblox handoff")
    parser.add_argument("file", type=Path, help="Exported .glb")
    parser.add_argument("--output", type=Path, help="Optional JSON report")
    parser.add_argument("--strict", action="store_true", help="Exit 1 for errors only, not review warnings")
    args = parser.parse_args()
    try:
        report = audit(*read_glb(args.file), asset_path=args.file)
    except (OSError, ValueError, KeyError, IndexError, TypeError, UnicodeError, struct.error) as exc:
        parser.exit(2, f"Invalid or unreadable GLB: {exc}\n")
    rendered = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        try:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(rendered, encoding="utf-8")
        except OSError as exc:
            parser.exit(2, f"Could not write report: {exc}\n")
    else:
        print(rendered, end="")
    if args.strict and report["errors"]:
        parser.exit(1)


if __name__ == "__main__":
    main()
