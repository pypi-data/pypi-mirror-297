from fuxion.pipelines import DatasetPipeline
from rich import print

output_structure = {
    'user_input': str,
    'emotional_tone': str,
    'response': str,
}
emotion_chain = DatasetPipeline(
    generator_template="emotion/generator.template",
    few_shot_file="emotion/emotion.json",
    output_structure=output_structure,
    dataset_name=f"emotions_dataset3",
    k=5,
    model_name="gpt-4o",
    verbose=True,
    temperature=0.1,
    cache = False,
    manual_review = True
)

result = emotion_chain.execute()
print(result)
