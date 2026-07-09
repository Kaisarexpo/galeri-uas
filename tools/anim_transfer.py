import argparse
import sys
from pathlib import Path

import bpy


def parse_args():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--avatar", required=True)
    parser.add_argument("--anim", required=True)
    parser.add_argument("--out", required=True)
    return parser.parse_args(argv)


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()


def import_glb(path):
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=str(path))
    return [obj for obj in bpy.data.objects if obj not in before]


def import_fbx(path):
    before = set(bpy.data.objects)
    bpy.ops.import_scene.fbx(filepath=str(path))
    return [obj for obj in bpy.data.objects if obj not in before]


def first_armature(objects):
    for obj in objects:
        if obj.type == "ARMATURE":
            return obj
    raise RuntimeError("No armature found")


def action_fcurves(action):
    if hasattr(action, "fcurves"):
        return action.fcurves
    curves = []
    for layer in action.layers:
        for strip in layer.strips:
            for channelbag in strip.channelbags:
                curves.extend(channelbag.fcurves)
    return curves


def main():
    args = parse_args()
    avatar_path = Path(args.avatar).resolve()
    anim_path = Path(args.anim).resolve()
    out_path = Path(args.out).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    clear_scene()
    avatar_objects = import_glb(avatar_path)
    avatar_armature = first_armature(avatar_objects)

    anim_objects = import_fbx(anim_path)
    anim_armature = first_armature(anim_objects)
    for obj in anim_objects:
        if obj != anim_armature:
            bpy.data.objects.remove(obj, do_unlink=True)

    # ponytail: bone names match; bake FBX pose onto Avaturn's own armature so
    # the skin keeps its original inverse bind pose.
    action = anim_armature.animation_data.action
    frame_start, frame_end = [int(v) for v in action.frame_range]
    bpy.context.scene.frame_start = frame_start
    bpy.context.scene.frame_end = frame_end

    bpy.ops.object.mode_set(mode="OBJECT")
    for bone in avatar_armature.pose.bones:
        if bone.name not in anim_armature.pose.bones:
            continue
        constraint = bone.constraints.new(type="COPY_TRANSFORMS")
        constraint.target = anim_armature
        constraint.subtarget = bone.name
        constraint.target_space = "WORLD"
        constraint.owner_space = "WORLD"

    bpy.ops.object.select_all(action="DESELECT")
    avatar_armature.select_set(True)
    bpy.context.view_layer.objects.active = avatar_armature
    bpy.ops.nla.bake(
        frame_start=frame_start,
        frame_end=frame_end,
        only_selected=False,
        visual_keying=True,
        clear_constraints=True,
        use_current_action=True,
        bake_types={"POSE"},
    )

    baked_action = avatar_armature.animation_data.action
    for curve in action_fcurves(baked_action):
        if curve.data_path == 'pose.bones["Hips"].location' and curve.array_index in (0, 1):
            value = curve.keyframe_points[0].co.y
            for keyframe in curve.keyframe_points:
                keyframe.co.y = value
                keyframe.handle_left.y = value
                keyframe.handle_right.y = value

    bpy.data.objects.remove(anim_armature, do_unlink=True)
    for action in list(bpy.data.actions):
        if action != baked_action:
            bpy.data.actions.remove(action)

    avatar_meshes = [obj for obj in avatar_objects if obj.type == "MESH"]

    bpy.ops.object.select_all(action="DESELECT")
    for obj in [avatar_armature, *avatar_meshes]:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = avatar_armature

    bpy.ops.export_scene.gltf(
        filepath=str(out_path),
        export_format="GLB",
        use_selection=True,
        export_animations=True,
    )


if __name__ == "__main__":
    main()
