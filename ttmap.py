#!/usr/bin/env python3
"""ttmap - headless CLI for the TrappedTogether map editor.

Drives the same model / helper / generator layer used by the GUI editor, so
maps can be inspected and edited from scripts (or by an LLM via the tt-maps
skill) without opening the Qt interface.

Invocation (from the Unity project root, via the symlink):
    python3 Assets/TtMapsEditor/ttmap.py <command> [options]

Commands are split into read-only queries (list-objects, list-generators,
describe, dump) and one-op-per-call mutating edits (added in a later step).
"""

import argparse
import contextlib
import json
import os
import sys

# Original working directory: map-file arguments are resolved against this
# BEFORE we chdir into the editor root below.
ORIG_CWD = os.getcwd()

# Real editor root (resolve symlinks so relative paths - mapObjects, generators,
# generatorsSettings.json, settings/application.json - point at the true repo).
EDITOR_ROOT = os.path.dirname(os.path.realpath(__file__))


@contextlib.contextmanager
def _stdout_to_stderr():
    """Redirect library chatter (print statements in the model/loader) to stderr
    so command output on stdout stays clean and machine-parseable."""
    old = sys.stdout
    sys.stdout = sys.stderr
    try:
        yield
    finally:
        sys.stdout = old


def _abs_from_orig(path):
    """Resolve a user-supplied path against the ORIGINAL cwd (pre-chdir)."""
    if path is None:
        return None
    return os.path.abspath(os.path.join(ORIG_CWD, path))


def build_model(map_path=None, base_prefab=None, need_generators=False):
    """Build the headless model with the unified object collection.

    Mirrors what the GUI does (showHouseEditor / Terrain.Model) minus the
    GUI-only bits: textures and loot collections are None (they only feed
    picker dialogs). basePrefab is auto-restored from the file on load.
    Returns (objectsCollection, mapModel[, generatorsLoader]).
    """
    from modules.commonModels.MapModelGeneral import MapModelGeneral
    from modules.commonModels.MapObjectModelGeneral import MapObjectModelGeneral
    from modules.commonModels.ObjectsCollection import ObjectsCollection
    from modules.ApplicationSettings.ApplicationSettingsModel import ApplicationSettingsModel

    with _stdout_to_stderr():
        settings = ApplicationSettingsModel()
        native = os.path.join(EDITOR_ROOT, 'mapObjects')
        ext = settings.getAdditionalMapObjectsDir()
        searchpaths = [native] + ([ext] if ext else [])
        oc = ObjectsCollection(searchpaths)

        model = MapModelGeneral(MapObjectModelGeneral, oc, None, None, basePrefab=base_prefab)
        model.setUpdatedCallback(lambda: None)
        if map_path is not None and os.path.exists(map_path):
            model.openMap(map_path)

    if not need_generators:
        return oc, model

    from modules.GeneratorPluginsModel.GeneratorPluginsLoader import GeneratorPluginsLoader
    with _stdout_to_stderr():
        loader = GeneratorPluginsLoader(model)
        loader.loadPluginsFrom('generators')
    return oc, model, loader


def _require_map(path):
    if not os.path.exists(path):
        sys.exit("Error: map file not found: " + path)


def _emit(obj, as_json):
    """Print a structured result: pretty JSON when as_json, else the caller has
    already printed text and passes as_json=False with obj=None."""
    if as_json:
        print(json.dumps(obj, indent=2))


# --------------------------------------------------------------------------- #
# Read-only commands
# --------------------------------------------------------------------------- #

def cmd_list_objects(args):
    oc, _ = build_model()
    rows = []
    for name in sorted(oc.objects.keys()):
        o = oc.objects[name]
        cats = [c.strip() for c in o.categories.split(',') if c.strip()]
        if args.category and args.category not in cats:
            continue
        props = [{'name': p.name, 'type': p.type, 'options': p.options} for p in o.additional_properties]
        rows.append({'name': name, 'w': o.w, 'h': o.h, 'categories': cats, 'additionalProperties': props})

    if args.json:
        _emit(rows, True)
        return

    if not rows:
        print("(no objects match)")
        return
    namew = max(len(r['name']) for r in rows)
    print("%-*s  %-5s  %-18s  %s" % (namew, 'NAME', 'WxH', 'CATEGORIES', 'ADDITIONAL PROPS'))
    for r in rows:
        size = "%dx%d" % (r['w'], r['h'])
        cats = ",".join(r['categories']) or "-"
        props = ", ".join("%s(%s)" % (p['name'], p['type']) for p in r['additionalProperties']) or "-"
        print("%-*s  %-5s  %-18s  %s" % (namew, r['name'], size, cats, props))


def cmd_list_generators(args):
    _, _, loader = build_model(need_generators=True)
    gens = []
    for name, order, plugin in loader.generators:
        static = plugin.pluginStaticSettings
        cls = plugin.childPluginClassName
        options = []
        for opt, spec in plugin.schema.items():
            options.append({
                'name': opt,
                'type': spec.get('type', ''),
                'default': spec.get('value', ''),
                'description': spec.get('description', ''),
            })
        gens.append({
            'name': name,
            'class': cls,
            'order': order,
            'description': static.get('description', ''),
            'options': options,
        })

    if args.json:
        _emit(gens, True)
        return

    for g in gens:
        header = g['name']
        if g['class'] != g['name']:
            header += " (class: %s)" % g['class']
        header += " [order %s]" % g['order']
        print(header)
        if g['description']:
            print("  " + g['description'])
        if g['options']:
            print("  options:")
            optw = max(len(o['name']) for o in g['options'])
            for o in g['options']:
                line = "    %-*s  %-6s  default=%s" % (optw, o['name'], o['type'], o['default'])
                if o['description']:
                    line += "   " + o['description']
                print(line)
        print("")


def cmd_describe(args):
    _require_map(args.map)
    _, model = build_model(args.map)
    zlevels = sorted({sq.z for sq in model._squares})
    counts = {}
    for sq in model._squares:
        counts.setdefault(sq.z, {})
        m = sq.properties.get('model')
        counts[sq.z][m] = counts[sq.z].get(m, 0) + 1

    if args.json:
        _emit({
            'map': args.map,
            'width': model.width,
            'height': model.height,
            'basePrefab': model.basePrefab,
            'zLevels': zlevels,
            'counts': {str(z): counts[z] for z in zlevels},
        }, True)
        return

    print("map:        %s" % args.map)
    print("size:       %d x %d  (width x height)" % (model.width, model.height))
    print("basePrefab: %s" % model.basePrefab)
    print("z-levels:   %s" % (zlevels or "[]"))
    for z in zlevels:
        print("counts (z=%d):" % z)
        modelw = max((len(str(k)) for k in counts[z]), default=0)
        for m in sorted(counts[z], key=lambda k: (-counts[z][k], str(k))):
            print("  %-*s  %d" % (modelw, m, counts[z][m]))


def cmd_dump(args):
    _require_map(args.map)
    _, model = build_model(args.map)

    rect = args.rect
    squares = []
    for sq in model._squares:
        if args.z is not None and sq.z != args.z:
            continue
        if rect is not None:
            x0, y0, w, h = rect
            if not (x0 <= sq.x < x0 + w and y0 <= sq.y < y0 + h):
                continue
        squares.append(sq)

    if args.json:
        _emit([sq.toSerializableObj() for sq in squares], True)
        return

    if not squares:
        print("(no squares match)")
        return
    for sq in squares:
        rot = sq.properties.get('rotation')
        rot = getattr(rot, 'value', rot)
        extra = ""
        if sq.additional_properties:
            extra = "  props={%s}" % ", ".join("%s=%s" % (p.name, p.value) for p in sq.additional_properties)
        print("x=%-3d y=%-3d z=%d  model=%-16s rot=%-3s wxh=%dx%d%s" % (
            sq.x, sq.y, sq.z, sq.properties.get('model'), rot, sq.w, sq.h, extra))


# --------------------------------------------------------------------------- #
# Argument parsing
# --------------------------------------------------------------------------- #

def _rect(value):
    parts = value.split()
    if len(parts) != 4:
        raise argparse.ArgumentTypeError("--rect expects 4 integers: 'x y w h'")
    try:
        return [int(p) for p in parts]
    except ValueError:
        raise argparse.ArgumentTypeError("--rect values must be integers")


def build_parser():
    parser = argparse.ArgumentParser(
        prog="ttmap",
        description="Headless CLI for the TrappedTogether map editor.")
    sub = parser.add_subparsers(dest="command", required=True)

    jsonparent = argparse.ArgumentParser(add_help=False)
    jsonparent.add_argument("--json", action="store_true", help="emit machine-readable JSON")

    p = sub.add_parser("list-objects", parents=[jsonparent],
                       help="list all placeable object types (name, size, categories, props)")
    p.add_argument("--category", help="only objects in this category")
    p.set_defaults(func=cmd_list_objects)

    p = sub.add_parser("list-generators", parents=[jsonparent],
                       help="list available generators, their descriptions and options")
    p.set_defaults(func=cmd_list_generators)

    p = sub.add_parser("describe", parents=[jsonparent],
                       help="summarize a map: size, basePrefab, z-levels, per-model counts")
    p.add_argument("map", help="path to the map JSON file")
    p.set_defaults(func=cmd_describe)

    p = sub.add_parser("dump", parents=[jsonparent],
                       help="list squares in a map, optionally filtered by z-level and rect")
    p.add_argument("map", help="path to the map JSON file")
    p.add_argument("--z", type=int, help="only squares at this z-level")
    p.add_argument("--rect", type=_rect, metavar='"x y w h"',
                   help="only squares inside this rectangle")
    p.set_defaults(func=cmd_dump)

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    # Resolve paths against the original cwd before chdir.
    if getattr(args, "map", None) is not None:
        args.map = _abs_from_orig(args.map)
    if getattr(args, "out", None) is not None:
        args.out = _abs_from_orig(args.out)

    os.chdir(EDITOR_ROOT)
    if EDITOR_ROOT not in sys.path:
        sys.path.insert(0, EDITOR_ROOT)

    args.func(args)


if __name__ == "__main__":
    main()
