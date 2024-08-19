###album catalog: czii

from album.runner.api import get_args, setup

env_file = """
channels:
  - conda-forge
  - defaults
dependencies:
  - python>3.10
  - pip
  - numpy
  - mrcfile
  - pip:
    - album
    - copick
    - "git+https://github.com/jtschwar/cryoet-deepfinder"
"""

args = [
    {
        "name": "config_path",
        "description":"Path to Configuration file for Output Copick Project",
        "type": "string",
        "required": True, 
    },  
    {
        "name": "membrane_seg_path",
        "description":"Path to where the membrane-seg experiment exits.",
        "type": "string",
        "required": True, 
    },  
    {
        "name": "export_membrane_seg",
        "description":"Flag to Determine whether to export segmentation results",
        "type": "boolean",
        "required": False, 
        "default": True,
    }  
]

def run():
    # Imports 
    import deepfinder.utils.copick_tools as tools
    import copick, glob, mrcfile, os
    from tqdm import tqdm

    # Parse Arguments
    args = get_args()

    config_path = args.config_path
    membrane_seg_path = args.membrane_seg_path
    export_membrane_seg = args.export_membrane_seg

    print(f'\nPARAMETERS: config-path: {config_path}\nmembrane-seg-path: {membrane_seg_path}\nexport_membrane_seg: {export_membrane_seg}\n')
    
    # Load CoPick root
    copickRoot = copick.from_file(config_path)

    # Load tomo_ids
    tomo_ids = [run.name for run in copickRoot.runs] 

    if len(tomo_ids) == 0:
        tomo_ids = glob.glob( os.path.join( membrane_seg_path, '*_Vol.mrc') )
        tomo_ids = [path[path.rfind('/') + 1:path.rfind('.mrc')] for path in tomo_ids]
        create_run = True
    else:
        create_run = False

    # Iterate Through All Runs
    for tomoID in tqdm(tomo_ids):

        if create_run: run = copickRoot.new_run(tomoID)
        else:          run = copickRoot.get_run(tomoID)

        vol = mrcfile.read( os.path.join(membrane_seg_path, tomoID + '.mrc') )
        tools.write_ome_zarr_tomogram(run, vol)

        if export_membrane_seg:
            vol = mrcfile.read( os.path.join(membrane_seg_path, tomoID + '_Segment_mask.mrc') )
            tools.write_ome_zarr_segmentation(run, vol)

setup(
    group="czii",
    name="membraneseg2copick",
    version="0.1.0",
    title="Export MembraneSeg2Copick",
    description="This solution calls IMOD model2point to convert Model Coordinate Files to Copick.",
    solution_creators=["Jonathan Schwartz"],
    tags=["Membrane-seg", "Copick", "Convert"],
    license="MIT",
    album_api_version="0.5.1",
    args=args,
    run=run,
    dependencies={"environment_file": env_file},
)