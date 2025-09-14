# Temporal-based E-commerce Product Review Generator

## The Business Problem

Creating detailed and persuasive product reviews or descriptions can be time-consuming, requiring manual synthesis of a product's technical specifications and a large volume of existing customer feedback. This leads to a bottleneck in content creation and can result in generic or inconsistent product information.

The Solution: Automated Product Review Generation

This Temporal-based application automates the process of generating a new product review. It works by:

Ingestion: Product specifications (e.g., from an internal database or an API) are submitted to the system.

Retrieval: The system searches a database of historical product reviews to find relevant feedback (e.g., common complaints, praised features, usage scenarios). It retrieves key information like customer sentiments and pros/cons.

Generation: The retrieved review data, along with the product's technical specifications, is fed into a Large Language Model (LLM). The LLM is then prompted to generate a new, concise, and balanced review.

Delivery: The generated review is provided for immediate use, helping to accelerate marketing efforts or internal reporting.

## Why Temporal?

Temporal ensures that this entire process is reliable and durable.

- Automatic Retries: If the API call to the LLM or the database fails (due to a network glitch, for example), Temporal automatically retries the failed step until it succeeds.

- Durability: The state of the workflow is saved. If the worker process crashes or the server goes down, the workflow will resume exactly where it left off once the worker is back online. This means no reviews are lost or left unprocessed.

- Scalability: You can easily scale the system by running more workers. Temporal handles the distribution of tasks automatically.

- Architectural Components
  Workflow (ProductReviewWorkflow): The main orchestrator. It receives a new product's details and schedules the activities to retrieve historical review data and generate the summary.

Note: Temporal Sample env will be present in `./sample_env`
