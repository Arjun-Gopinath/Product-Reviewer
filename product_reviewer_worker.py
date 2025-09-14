# Temporal Worker for the product review generator.

import asyncio
from temporalio.client import Client
from temporalio.worker import Worker
from product_reviewer_workflow import ProductReviewWorkflow, retrieve_related_reviews, generate_product_review

async def main():
    """
    The main function to set up and start the Temporal Worker.
    """

    client = await Client.connect("temporal:7233")
    print("Connected to Temporal server.")

    worker = Worker(
        client,
        task_queue="product-review-task-queue",
        workflows=[ProductReviewWorkflow],
        activities=[retrieve_related_reviews, generate_product_review],
    )

    print("Starting worker...")
    await worker.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Worker stopped.")
