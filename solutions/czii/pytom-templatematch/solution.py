###album catalog: czii

from album.runner.api import get_args, setup

env_file = """
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.10
  - cupy
  - pip
  - mrcfile
  - numpy
  - pip:
    - album
    - "git+https://github.com/czimaginginstitute/pipeline-3D-template-match"
"""

args = [
    {
        "name": "parameter-path",
        "description":"example_parameter.json",
        "type": "string",
        "required": True, 
    },
    {
        "name": "template",
        "description":"The template string, e.g., ribosome-80S",
        "type": "string",
        "required": True, 
    }
]

def run():
    # Imports 
    from template_match import my_template_match
    from template_match import inspect_entry
    import numpy as np

    # Parse Arguments
    args = get_args()

    template = args.template
    parameter_path = args.parameter_path

    # Initialize Classes for Template Matching
    pytom_obj = my_template_match.template_match(parameter_path,template)

    # Determine How Many GPUs to Assign Per Rank..
    numGPUs = inspect_entry.count_gpus()
    availGPUs = ' '.join(map(str,np.arange(numGPUs)))
    pytom_obj.availGPUs = availGPUs
    print('Running Template Matching On Following GPU IDs: ', availGPUs)

    ### Go through the mdoc file related to each tilt series and perform alignment, reconstruction, CTF deconvolution
    while pytom_obj.experimentRunning:

        tomogramsList = pytom_obj.find_available_tomgrams()

        for tomoIndex in range(len(tomogramsList)):

            # Read fName for TS
            tomogramPath = tomogramsList[tomoIndex]
            print('Processing Dataset: {} ({}/{})'.format(tomogramPath.split('/')[-1],tomoIndex,len(tomogramsList)))        
            
            try:
                pytom_obj.run_template_match(tomogramPath)
            except Exception as e:
                print(f"Error processing label {tomogramPath}: {e}")
                pytom_obj.completedTilts.append(tomogramPath)

            # Keep Track of Completed Tomograms if Live Tomography Processing
            pytom_obj.write_completed_tomo_list()

    # Create Resulting Star Files for Relion
    pytom_obj.merge_particles_coordinates()


setup(
    group="czii",
    name="pytom-templatematch",
    version="0.1.0",
    title="3D Template Matching with PyTom",
    description="This solution calls PyTom to Find Proteins with Template Matching.",
    solution_creators=["Jonathan Schwartz"],
    cite=[{"text": "SBC-Utrecht.", "url": "https://github.com/SBC-Utrecht/pytom-match-pick"}],
    tags=["czii", "pytom", "template match"],
    license="MIT",
    album_api_version="0.5.1",
    args=args,
    run=run,
    dependencies={"environment_file": env_file},
)