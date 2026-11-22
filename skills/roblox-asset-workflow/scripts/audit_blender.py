#!/usr/bin/env python3
"""Read-only evaluated Blender mesh audit; run using Blender Python."""
from __future__ import annotations
import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

MESH_LIMIT = 20_000


def main() -> None:
    try:
        import bpy
    except ImportError as exc:
        raise SystemExit("Use Blender: blender -b FILE.blend --python scripts/audit_blender.py") from exc

    params = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    parser = argparse.ArgumentParser(description="Read-only Blender mesh audit")
    parser.add_argument("--collection", help="Limit to a collection and its child collections")
    parser.add_argument("--include-hidden", action="store_true", help="Include hidden objects (excluded by default)")
    parser.add_argument("--output", help="Optional JSON report path")
    args = parser.parse_args(params)
    scene = bpy.context.scene
    graph = bpy.context.evaluated_depsgraph_get()
    if args.collection:
        collection = bpy.data.collections.get(args.collection)
        if collection is None:
            parser.error(f"Collection not found: {args.collection}")
        objects = [obj for obj in collection.all_objects if obj.name in scene.objects]
    else:
        objects = list(scene.objects)

    meshes, warnings, skipped = [], [], []
    for obj in sorted(objects, key=lambda o: o.name):
        if obj.type != "MESH":
            continue
        if not args.include_hidden and (obj.hide_viewport or obj.hide_render or not obj.visible_get()):
            skipped.append(obj.name)
            continue
        evaluated = obj.evaluated_get(graph)
        try:
            mesh = evaluated.to_mesh(preserve_all_data_layers=True, depsgraph=graph)
        except Exception as exc:
            warnings.append(f"{obj.name}: evaluation failed: {exc}")
            continue
        if mesh is None:
            warnings.append(f"{obj.name}: evaluation returned no mesh")
            continue
        try:
            triangles = sum(max(0, len(poly.vertices) - 2) for poly in mesh.polygons)
            slots = len(obj.material_slots)
            scale = [round(float(v), 6) for v in obj.scale]
            meshes.append({"name": obj.name, "triangles_evaluated": triangles,
                           "vertices_evaluated": len(mesh.vertices), "uv_layers": len(mesh.uv_layers),
                           "material_slots": slots, "scale": scale,
                           "over_roblox_20k": triangles > MESH_LIMIT})
            if triangles > MESH_LIMIT:
                warnings.append(f"{obj.name}: {triangles} triangles exceed {MESH_LIMIT} per mesh")
            if slots > 1:
                warnings.append(f"{obj.name}: {slots} material slots; prefer separate meshes/atlas for customizable parts; inspect Studio splitting")
            if any(abs(float(v) - 1) > 1e-5 for v in obj.scale):
                warnings.append(f"{obj.name}: non-unit local scale {scale}; verify export dimensions/pivots")
            if slots and not mesh.uv_layers:
                warnings.append(f"{obj.name}: materials but no UV layers (may be intentional)")
            if mesh.uv_layers:
                uv = mesh.uv_layers.active or mesh.uv_layers[0]
                if any(value < -1e-5 or value > 1 + 1e-5
                       for loop in uv.data for value in loop.uv):
                    warnings.append(f"{obj.name}: UVs outside [0,1]; check paint masks; tiling can be intentional")
        finally:
            evaluated.to_mesh_clear()

    report = {"asset_file": bpy.data.filepath, "scene": scene.name,
              "collection": args.collection, "include_hidden": args.include_hidden,
              "skipped_hidden_meshes": skipped, "created_utc": datetime.now(timezone.utc).isoformat(),
              "method": "evaluated scene/collection mesh objects; importer splitting is not accounted for",
              "total_triangles": sum(m["triangles_evaluated"] for m in meshes),
              "max_triangles_per_mesh": max((m["triangles_evaluated"] for m in meshes), default=0),
              "mesh_count": len(meshes), "meshes": meshes, "warnings": warnings}
    rendered = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        path = Path(args.output).expanduser().resolve()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(rendered, encoding="utf-8")
        print(f"Asset audit saved: {path}")
    else:
        print(rendered, end="")
    print(f"Mesh count={report['mesh_count']}; triangles={report['total_triangles']}; max/mesh={report['max_triangles_per_mesh']}")
    for warning in warnings:
        print("WARNING:", warning)


if __name__ == "__main__":
    main()
