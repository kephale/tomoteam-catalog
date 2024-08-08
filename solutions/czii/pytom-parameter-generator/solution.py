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
        "name": "file-path",
        "description":"Name for the Saved Parameter File, e.g., 24jul24a_parameters.json",
        "type": "string",
        "required": True, 
    }
]

def run():
    # Imports 
    from template_match.parse_pytom_params import create_boilerplate_json

    # Parse Arguments
    args = get_args()
    file_path = args.file_path

    create_boilerplate_json(file_path)

setup(
    group="czii",
    name="pytom-parameter-generator",
    version="0.1.0",
    title="3D Template Matching with PyTom",
    description="This solution calls PyTom to Find Proteins with Template Matching.",
    solution_creators=["Jonathan Schwartz"],
    tags=["czii", "pytom", "template match"],
    license="MIT",
    album_api_version="0.5.1",
    args=args,
    run=run,
    dependencies={"environment_file": env_file},
)