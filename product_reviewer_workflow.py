# Temporal Workflow and Activities for the e-commerce product review generator.

from temporalio import workflow, activity
from datetime import timedelta
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

MODEL_NAME = "meta-llama/Meta-Llama-3-8B-Instruct"

print("Loading LLaMA 3 model...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    device_map="auto"
)

def llama_generate(prompt: str, max_new_tokens: int = 256) -> str:
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(**inputs, max_new_tokens=max_new_tokens, temperature=0.7, do_sample=True)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

PRODUCT_DATA = {
    "specs": {
        "product_id": "PRD-123",
        "name": "Bluetooth Noise-Cancelling Headphones",
        "features": ["Active Noise Cancellation (ANC)", "40-hour battery life", "Comfortable over-ear design"],
    },
    "reviews": [
        "The noise cancellation is incredible! Blocks out all the chatter at my coffee shop. Highly recommend.",
        "Sound quality is good, but the headband feels a bit tight after a few hours of use.",
        "I love the battery life. I only charge these once a week. Amazing!",
        "The audio quality is decent, but the bass feels a bit flat compared to other headphones I've tried."
    ]
}

@activity.defn
async def retrieve_related_reviews(product_specs: dict) -> list[str]:
    print(f"Retrieving existing reviews for product: '{product_specs['name']}'...")
    return PRODUCT_DATA["reviews"]

@activity.defn
async def generate_product_review(product_specs: dict, reviews: list[str]) -> str:
    print("Generating product review with LLaMA 3...")

    if not reviews:
        return f"Could not generate a review. No existing reviews found for {product_specs['name']}."

        review_context = "\n".join(reviews)
        features = ", ".join(product_specs['features'])

        prompt = f"""
        You are an expert product reviewer.

        Product: {product_specs['name']}
        Features: {features}

        Here are some customer reviews:
        {review_context}

        Write a new, balanced review that highlights strengths and weaknesses.
        """

        generated_review = llama_generate(prompt, max_new_tokens=300)
        return generated_review


@workflow.defn
class ProductReviewWorkflow:
    @workflow.run
    async def run(self, product_specs: dict) -> str:
        print(f"Starting workflow for product: '{product_specs['name']}'")

        reviews = await workflow.execute_activity(
            retrieve_related_reviews,
            product_specs,
            schedule_to_close_timeout=timedelta(seconds=30),
        )

        review_text = await workflow.execute_activity(
            generate_product_review,
            args=[product_specs, reviews],
            schedule_to_close_timeout=timedelta(seconds=30),
        )

        print("Product review generation workflow completed.")
        return review_text
