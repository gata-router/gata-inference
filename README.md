# Gata Inference

Gata Inference is part of the [Gata Router](https://gata.works) project - an open source AI-powered support ticket triage/routing platform. This component provides a container for running inference with fine-tuned BERT models to classify support tickets.

## Prerequisites

- Python 3.14 (managed within the container)
- Docker for building and running the container
- A finetuned BERT model created by [Gata Fine Tune](https://github.com/gata-router/gata-finetune)

## Overview

The Gata Inference service server the model via a SageMaker inference endpoint. It receives ticket text and returns classification predictions using a finetuned Hugging Face BERT model. While the image is designed to run on AWS SageMaker, it can also run locally for testing and development.

## Model Requirements

The service expects a trained BERT model in the standard Hugging Face format. By default, it looks for the model in the `/opt/ml/model` directory (the standard SageMaker model location) but this can be configured via the `SM_MODEL_DIR` environment variable.

You must use a model produced by the [Gata Fine Tune](https://github.com/gata-router/gata-finetune) component, which provides the required model format and training process. The model must include:

- `config.json` with an `id2label` mapping for category labels
- Tokenizer configuration files
- Model weights in PyTorch format

## Environment Setup

The inference service runs as a Docker container, which can be deployed in various ways:

- As a SageMaker endpoint
- As a standalone container on any Docker-compatible infrastructure
- Locally for development and testing

## Building the Docker Image

Build the Docker image with:

```sh
docker build -t gata-inference .
```

The build process is optimized for runtime performance. It's deliberately thorough in its dependency handling to ensure consistent behavior across environments.

## Running Locally

To run the inference service locally:

```sh
docker run --rm -p 8080:8080 \
  -v /path/to/your/model:/opt/ml/model \
  gata-inference
```

The API will be available at http://localhost:8080.

## API Endpoints

The service provides two main endpoints:

### GET /ping

Health check endpoint for monitoring and SageMaker health verification.

**Response:**
- **200 OK** - Service is healthy (empty response body)

### POST /invocations

Prediction endpoint for ticket classification.

The application implements SageMaker's required contract for inference.

**Request Body:**

```json
{
  "text": "I'm having trouble logging into my account. It says my password is incorrect but I'm sure it's right."
}
```

**Response:**

```json
{
  "prediction": {
    "label": "1234567890",
    "probability": 0.9823
  }
}
```

**HTTP Status Codes:**
- **200 OK** - Successful prediction
- **400 Bad Request** - Invalid or malformed request (missing `text` field, invalid JSON)
- **500 Internal Server Error** - Service error (model loading failure, inference error)

**Error Handling:**

If you receive 4xx/5xx errors, check the container logs for detailed error messages and stack traces.

## Hardware Requirements

For local development and testing, the container can run on any machine with Docker installed. For production use, we recommend:

- At least 2 vCPU cores
- 1GB RAM minimum, 2GB recommended
- GPU acceleration is not required for inference

## Deployment on AWS SageMaker

To deploy as a SageMaker endpoint:

1. Push the Docker image to Amazon ECR
2. Create a SageMaker model pointing to your ECR image
3. Create the endpoint configuration
4. Deploy a Serverless Inference Endpoint

The deployment process is automated using the [Gata Infrastructure Terraform module](https://github.com/gata-router/terraform-aws-gata).


## Setting Up Continuous Deployment

The repository includes a GitHub Actions workflow (`.github/workflows/release.yaml.txt`) for automated builds and deployments to your AWS environment. This workflow is disabled by default - you must enable and configure it.

**Prerequisites:**

1. Deploy the [Gata Infrastructure](https://github.com/gata-router/terraform-aws-gata) Terraform stack, which provisions:
   - IAM role for GitHub Actions
   - OIDC provider configuration for GitHub
   - ECR repository
   - SSM parameter for image tags

**Setup Steps:**

1. Copy the workflow file to enable it:
   ```sh
   cp .github/workflows/release.yaml.txt .github/workflows/release.yaml
   ```

2. Configure the following GitHub repository variables in Settings → Secrets and variables → Actions → Variables:
   - `AWS_REGION` - Your AWS region. `us-east-1` is currently the only region supported by Gata.
   - `ECR_REPOSITORY` - Docker URL of your ECR repository

3. Configure the following GitHub repository secrets in Settings → Secrets and variables → Actions → Secrets:
   - `AWS_ROLE_ARN` - IAM role ARN from Terraform outputs (for OIDC authentication)
   - `SSM_PARAMETER_NAME` - Full path of the SSM parameter for storing the current image tag

4. Tag your release using the YYYYMMDDHH format to trigger the workflow:
   ```sh
   git tag 2026010203
   git push origin 2026010203
   ```

The workflow will build the Docker image, push it to ECR, and update the SSM parameter with the new image tag.

## Environment Variables

- `SM_MODEL_DIR` - Path to the model directory (default: `/opt/ml/model`)
- `SM_LOG_LEVEL` - Logging level (default: `INFO`)

## Development

The project uses [uv](https://github.com/astral-sh/uv) for dependency management. To set up a development environment:

```sh
uv sync
```

**Available Commands:**

```sh
# Format code
uv run ruff format .

# Lint code
uv run ruff check .

# Type check
uv run ty .

# Run tests with coverage
uv run coverage run -m pytest

# View coverage report
uv run coverage report -m
```


## Troubleshooting

### Local Development Issues

**Model path not found:**
- Ensure your model directory is correctly mounted: `-v /absolute/path/to/model:/opt/ml/model`
- Verify the model directory contains all required files (config.json, tokenizer files, model weights)

**Port already in use:**
- Check if another service is using port 8080: `lsof -i :8080`
- Use a different port mapping: `-p 8081:8080`

**Container logs:**
- View logs: `docker logs <container-id>`
- Stream logs: `docker logs -f <container-id>`

## Getting Help

If you encounter issues specific to the inference service, please open an issue in this repository. For questions about how this component integrates with the broader Gata Router platform, check out the main project documentation at https://gata.works.
