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


BASE_PROPS = ('rotation', 'model')  # properties on MapObjectModelGeneral.classnames


def _selection(rect, z):
    from modules.commonModels.SelectionRange import SelectionRange
    x, y, w, h = rect
    return SelectionRange(x, y, x + w - 1, y + h - 1, z if z is not None else 0)


def _parse_kv(items):
    result = {}
    for item in items or []:
        if "=" not in item:
            sys.exit("Error: expected key=value, got: " + item)
        key, value = item.split("=", 1)
        result[key] = value
    return result


def _find_generator(loader, name):
    for gen_name, _order, plugin in loader.generators:
        if name in (gen_name, plugin.childPluginClassName):
            return plugin
    available = ", ".join(n for n, _o, _p in loader.generators)
    sys.exit("Error: generator not found: %s\nAvailable: %s" % (name, available))


def save_model(model, path):
    with _stdout_to_stderr():
        model.saveMap(path)


def _fill_cells(model, selection, model_name, rotation):
    """Position-preserving fill: for each cell, reuse the square already there
    (delete any extra stacked layers), and create one only for empty cells.
    Keeps the squares array order stable so diffs stay minimal - cells that
    already hold the target model+rotation produce no change at all."""
    z = selection.zLevel
    rot = str(rotation) if rotation is not None else '0'
    with _stdout_to_stderr():
        for y in range(selection.startRow, selection.endRow + 1):
            for x in range(selection.startCol, selection.endCol + 1):
                existing = model.getSquareItems(x, y, z)
                if existing:
                    keep = existing[0]
                    for extra in existing[1:]:
                        model.deleteSquareById(extra.id)
                else:
                    keep = model.createObjectAt(x, y, z)
                keep.setModel(model_name)
                keep.setProperty('rotation', rot)
                model.updateModelSize(keep)


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
# Mutating commands (load -> one op -> save in place, or --out)
# --------------------------------------------------------------------------- #

def cmd_new(args):
    _, model = build_model(None, base_prefab=args.base_prefab)
    width, height = args.size
    model.newMap(width, height)
    out = args.out or args.map
    save_model(model, out)
    print("created %dx%d map (basePrefab=%s) -> %s" % (width, height, model.basePrefab, out))


def cmd_fill(args):
    _require_map(args.map)
    _, model = build_model(args.map)
    sel = _selection(args.rect, args.z)
    _fill_cells(model, sel, args.model, args.rotation)
    out = args.out or args.map
    save_model(model, out)
    n = len(model.getAllObjectOfType(args.model, sel))
    print("filled %d cells with %s in rect %s -> %s" % (n, args.model, args.rect, out))


def cmd_border(args):
    _require_map(args.map)
    _, model = build_model(args.map)
    x, y, w, h = args.rect
    bw = args.width
    z = args.z if args.z is not None else 0
    strips = [
        [x, y, w, bw],                 # top
        [x, y + h - bw, w, bw],        # bottom
        [x, y, bw, h],                 # left
        [x + w - bw, y, bw, h],        # right
    ]
    for strip in strips:
        sel = _selection(strip, z)
        _fill_cells(model, sel, args.model, args.rotation)
    out = args.out or args.map
    save_model(model, out)
    print("drew %s border (width %d) around rect %s -> %s" % (args.model, bw, args.rect, out))


def cmd_place(args):
    _require_map(args.map)
    _, model = build_model(args.map)
    x, y = args.at
    z = args.z if args.z is not None else 0
    obj = model.createObjectAt(x, y, z)
    obj.setModel(args.model)
    if args.rotation is not None:
        obj.setProperty('rotation', str(args.rotation))
    model.updateModelSize(obj)
    for key, value in _parse_kv(args.prop).items():
        obj.setAdditioanalProperty(key, value)
    out = args.out or args.map
    save_model(model, out)
    print("placed %s at (%d,%d,%d) -> %s" % (args.model, x, y, z, out))


def cmd_delete(args):
    _require_map(args.map)
    _, model = build_model(args.map)
    sel = _selection(args.rect, args.z)
    count = len(model.getAllObjectOfType(args.model, sel))
    model.deleteObjectsInSelection(sel, args.model)
    out = args.out or args.map
    save_model(model, out)
    what = args.model if args.model else "all models"
    print("deleted %d squares (%s) in rect %s -> %s" % (count, what, args.rect, out))


def cmd_setprop(args):
    _require_map(args.map)
    _, model = build_model(args.map)
    sel = _selection(args.rect, args.z)
    kv = _parse_kv(args.prop)
    # Count matches BEFORE mutating: if a --prop changes 'model', the filter would
    # no longer match afterwards and the report would wrongly say 0.
    n = len(model.getAllObjectOfType(args.model, sel))
    additional = {}
    for key, value in kv.items():
        if key in BASE_PROPS:
            model.setGroupProperty(sel, args.model, key, value)
        else:
            additional[key] = value
    if additional:
        model.setGroupProperty(sel, args.model, 'additionalProperties', additional)
    out = args.out or args.map
    save_model(model, out)
    changes = ", ".join("%s=%s" % (k, v) for k, v in kv.items())
    print("updated %d %s squares (%s) in rect %s -> %s" % (n, args.model, changes, args.rect, out))


def cmd_wall_frame(args):
    _require_map(args.map)
    _, model = build_model(args.map)
    from modules.commonModels.EditorHelper import EditorHelper
    sel = _selection(args.rect, args.z)
    EditorHelper(model).generateWallFrame(sel)
    out = args.out or args.map
    save_model(model, out)
    print("generated wall frame in rect %s -> %s" % (args.rect, out))


def cmd_roof_frame(args):
    _require_map(args.map)
    _, model = build_model(args.map)
    from modules.commonModels.EditorHelper import EditorHelper
    sel = _selection(args.rect, args.z)
    helper = EditorHelper(model)
    if args.half:
        helper.generateRoofFrameHalf(sel)
    else:
        helper.generateRoofFrame(sel)
    out = args.out or args.map
    save_model(model, out)
    kind = "half-roof" if args.half else "roof"
    print("generated %s frame in rect %s -> %s" % (kind, args.rect, out))


def cmd_generate(args):
    _require_map(args.map)
    _, model, loader = build_model(args.map, need_generators=True)
    plugin = _find_generator(loader, args.name)
    for key, value in _parse_kv(args.set).items():
        plugin.settings[key] = value
    with _stdout_to_stderr():
        plugin.generate()
    out = args.out or args.map
    save_model(model, out)
    print("ran generator %s -> %s" % (args.name, out))


def cmd_clear(args):
    _require_map(args.map)
    _, model, loader = build_model(args.map, need_generators=True)
    plugin = _find_generator(loader, args.name)
    with _stdout_to_stderr():
        plugin.clear_generated()
    out = args.out or args.map
    save_model(model, out)
    print("cleared generator %s output -> %s" % (args.name, out))


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

    # --- mutating commands --- #
    outparent = argparse.ArgumentParser(add_help=False)
    outparent.add_argument("--out", help="write result here instead of editing in place")

    p = sub.add_parser("new", parents=[outparent],
                       help="create a new empty map of the given size")
    p.add_argument("map", help="path to the map JSON file to create")
    p.add_argument("--size", type=int, nargs=2, required=True, metavar=("W", "H"))
    p.add_argument("--base-prefab", default=None,
                   help="root prefab for the runtime loader (e.g. House); omit for terrain")
    p.set_defaults(func=cmd_new)

    p = sub.add_parser("fill", parents=[outparent],
                       help="replace everything in a rect with one model (z-correct)")
    p.add_argument("map")
    p.add_argument("--rect", type=_rect, required=True, metavar='"x y w h"')
    p.add_argument("--z", type=int, default=None)
    p.add_argument("--model", required=True)
    p.add_argument("--rotation", type=int, choices=(0, 90, 180, 270), default=None)
    p.set_defaults(func=cmd_fill)

    p = sub.add_parser("border", parents=[outparent],
                       help="draw a ring of one model around a rect")
    p.add_argument("map")
    p.add_argument("--rect", type=_rect, required=True, metavar='"x y w h"')
    p.add_argument("--z", type=int, default=None)
    p.add_argument("--model", required=True)
    p.add_argument("--width", type=int, default=1, help="border thickness (default 1)")
    p.add_argument("--rotation", type=int, choices=(0, 90, 180, 270), default=None)
    p.set_defaults(func=cmd_border)

    p = sub.add_parser("place", parents=[outparent],
                       help="add a single object (a layer) at one cell")
    p.add_argument("map")
    p.add_argument("--at", type=int, nargs=2, required=True, metavar=("X", "Y"))
    p.add_argument("--z", type=int, default=None)
    p.add_argument("--model", required=True)
    p.add_argument("--rotation", type=int, choices=(0, 90, 180, 270), default=None)
    p.add_argument("--prop", action="append", metavar="KEY=VALUE",
                   help="additional property (repeatable)")
    p.set_defaults(func=cmd_place)

    p = sub.add_parser("delete", parents=[outparent],
                       help="delete squares in a rect (optionally only one model)")
    p.add_argument("map")
    p.add_argument("--rect", type=_rect, required=True, metavar='"x y w h"')
    p.add_argument("--z", type=int, default=None)
    p.add_argument("--model", default=None, help="only delete this model; omit to delete all")
    p.set_defaults(func=cmd_delete)

    p = sub.add_parser("setprop", parents=[outparent],
                       help="set properties on all squares of one model in a rect")
    p.add_argument("map")
    p.add_argument("--rect", type=_rect, required=True, metavar='"x y w h"')
    p.add_argument("--z", type=int, default=None)
    p.add_argument("--model", required=True, help="only squares of this model are changed")
    p.add_argument("--prop", action="append", required=True, metavar="KEY=VALUE",
                   help="property to set (repeatable); rotation/model are base props, "
                        "anything else is an additionalProperty")
    p.set_defaults(func=cmd_setprop)

    p = sub.add_parser("wall-frame", parents=[outparent],
                       help="generate walls + corners around a rect (House)")
    p.add_argument("map")
    p.add_argument("--rect", type=_rect, required=True, metavar='"x y w h"')
    p.add_argument("--z", type=int, default=None)
    p.set_defaults(func=cmd_wall_frame)

    p = sub.add_parser("roof-frame", parents=[outparent],
                       help="generate a pitched roof frame around a rect (House)")
    p.add_argument("map")
    p.add_argument("--rect", type=_rect, required=True, metavar='"x y w h"')
    p.add_argument("--z", type=int, default=None)
    p.add_argument("--half", action="store_true", help="use the half-height roof variant")
    p.set_defaults(func=cmd_roof_frame)

    p = sub.add_parser("generate", parents=[outparent],
                       help="run a generator (see list-generators)")
    p.add_argument("map")
    p.add_argument("--name", required=True, help="generator name or class")
    p.add_argument("--set", action="append", metavar="KEY=VALUE",
                   help="override a generator option (repeatable)")
    p.set_defaults(func=cmd_generate)

    p = sub.add_parser("clear", parents=[outparent],
                       help="clear a generator's output (see list-generators)")
    p.add_argument("map")
    p.add_argument("--name", required=True, help="generator name or class")
    p.set_defaults(func=cmd_clear)

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
