from fuxion.pipelines import DatasetPipeline
from rich import print

output_structure = {
    "puzzle_title": str,
    "description": str,
    "difficulty": str,
    "puzzle_type": str,
     "solution": {
        "step_1": str,
        "step_2": str,
        "step_3": str,
    },
}
puzzle_chain = DatasetPipeline(
    generator_template="puzzle/generator.template",
    few_shot_file="puzzle/puzzle.json",
    output_structure=output_structure,
    dataset_name="puzzle_dataset_10",
    k=3,
    model_name="gpt-4o",
    cache=False,
    verbose=True,
    temperature=0.1,
)

result = puzzle_chain.execute()
print(result)
