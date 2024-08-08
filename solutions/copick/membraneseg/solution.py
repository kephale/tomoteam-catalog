###album catalog: membraneseg

from album.runner.api import get_args, setup

env_file = """
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.10
  - pip
  - mrcfile
  - numpy
  - pip:
    - album
    - "git+https://github.com/czimaginginstitute/pipeline-membrane-seg"
"""

args = [
    {
        "name": "project_path",
        "description":"The path to the project JSON file, e.g., /hpc/projects/group.czii/krios1.processing/aretomo3/24jul24a/run001/vol002/",
        "type": "string",
        "required": True, 
    },  
    {
        "name": "session",
        "description":"Session from Experiment, e.g., 24jul24a",
        "type": "string",
        "required": True, 
    },  
    {
        "name": "run",
        "description":"Run for Segmentation Output, e.g., run001",
        "type": "string",
        "required": False, 
        "default": "run001",
    }, 
    {
        "name": "model_path",
        "description":"The path to pre-trained network weights",
        "type": "string",
        "required": False, 
        "default": 'MemBrain_seg_v10_alpha.ckpt',
    },
    {
        "name": "segmentation_threshold",
        "description": "Segmentation Threshold",
        "type": "integer",
        "required": False,
        "default": -5,
    },
    {
        "name": "save_segmentation_scores", 
        "description": "Flag to save segmentation scores.",
        "type": "boolean",
        "required": False,
        "default": False
    },
    {
        "name": "invert_mask",
        "description": "Flag to Save Inverted Segmentation Mask",
        "type": "boolean",
        "required": False,
        "default": True
    }    
]

def run():
    # Imports 
    import tomo_segment.my_membrane_seg as segmentor
    import glob, os 

    # Parse Arguments
    args = get_args()

    project_path = args.project_path
    session = args.session
    run = args.run
    model_path = args.model_path
    segmentation_threshold = args.segmentation_threshold
    save_segmentation_scores = args.model_path
    invert_mask = args.model_path

    availableTomos = glob.glob( os.path.join(project_path, '*.mrc') )
    availableTomos = [f for f in availableTomos if 'ODD' not in f and 'EVN' not in f]

    mySegment = segmentor.segment_membranes(mySession=session, myRun=run, 
                                  invert_mask=invert_mask, modelPath = model_path )

    for tomoPath in availableTomos:

        mySegment.segment(tomoPath, segmentation_threshold, save_segmentation_scores)

setup(
    group="copick",
    name="membraneseg",
    version="0.1.0",
    title="Segment Membranes",
    description="This solution calls Membrane-Seg to Segment Membranes in Tomograms.",
    solution_creators=["Jonathan Schwartz"],
    tags=["copick", "points"],
    license="MIT",
    album_api_version="0.5.1",
    args=args,
    run=run,
    dependencies={"environment_file": env_file},
)