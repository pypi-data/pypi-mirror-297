import pathlib



def voxel_sizes(recipe_path):
    import yaml

    with open(str(recipe_path), "r") as stream:
        try:
            params = yaml.safe_load(stream)
            return params["VoxelSize"]
        except yaml.YAMLError as exc:
            print(exc)


def get_brain_paths(
    mouse_id,
    brain_dir,
):
    p=pathlib.Path(brain_dir) / mouse_id / "stitchedImages_100"
    return list(p.glob("*"))


def brainreg_command(mouse_directory_derivatives, serial2p_directory_raw, function="brainreg", atlas="allen_mouse_10um", additional=None):
    input_paths = get_brain_paths(mouse_directory_derivatives.stem, serial2p_directory_raw)
    brainreg_commands = []
    for input_path in input_paths:
        output_path = mouse_directory_derivatives / "histology" / atlas / input_path.stem
        print(input_path)
        print(output_path)
        recipe_path = list(input_path.parent.parent.glob("recipe*"))[0]
        voxels = voxel_sizes(recipe_path)
        additional = f"--additional {input_path.parent / additional}" if additional is not None else ""
        cmd = f"{function} {input_path} {output_path} {additional} -v {voxels['Z']} {voxels['X']} {voxels['Y']} --orientation psr --atlas {atlas}"
        brainreg_commands.append(cmd)
    return brainreg_commands


def brainreg_commandline(
     mouse_directory_derivatives, serial2p_directory_raw, function="brainreg", atlas="kim_mouse_10um", logs_path=None, additional=None
):
    brainreg_commands = brainreg_command(mouse_directory_derivatives, serial2p_directory_raw,
                                         function=function, atlas=atlas, additional=additional)
    # subprocess.run(command,
    #                executable="/bin/bash",
    #                shell=True,
    #                )
