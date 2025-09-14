# Product review generation workflow.

import asyncio
from temporalio.client import Client
from product_reviewer_workflow import ProductReviewWorkflow

async def main():
    """
    Connects to the Temporal server and starts a new workflow execution.
    """
    client = await Client.connect("temporal:7233")
    print("Connected to Temporal server.")

    product_data = {
        "product_id": "PRD-123",
        "name": "Bluetooth Noise-Cancelling Headphones",
        "features": ["Active Noise Cancellation (ANC)", "40-hour battery life", "Comfortable over-ear design"],
    }

    print(f"Starting workflow for product: '{product_data['name']}'")

    result = await client.execute_workflow(
        ProductReviewWorkflow.run,
        product_data,
        id="product-review-workflow-1",
        task_queue="product-review-task-queue",
    )

    print(f"Workflow completed. Final review:\n\n{result}")

if __name__ == "__main__":
    asyncio.run(main())