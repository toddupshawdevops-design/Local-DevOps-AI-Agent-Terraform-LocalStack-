# Local DevOps AI Agent (Terraform + LocalStack)

A lightweight, rule-based Python CLI agent that automates local AWS infrastructure provisioning using Terraform and LocalStack. It translates natural language prompts into Infrastructure-as-Code (IaC) configurations and interacts directly with an emulated local AWS environment—allowing you to build, test, and verify cloud workflows on Windows without incurring real AWS costs.

---

## Architecture & Tech Stack

* **Language:** Python 3.13
* **Infrastructure as Code:** Terraform (`v1.15.8+`)
* **AWS Provider:** HashiCorp AWS Provider pinned to `~> 5.0` (ensures stability and prevents live API hangs with LocalStack)
* **Cloud Emulator:** LocalStack (Community Edition via Docker on port `4566`)
* **OS / Shell:** Windows (PowerShell with Python `venv`)

---

## Project Structure

```text
aws_agent_project/
├── agent_workspace/          # Terraform working directory
│   ├── main.tf               # Generated AWS/LocalStack HCL configuration
│   ├── terraform.tfstate     # Local infrastructure state file
│   └── .terraform.lock.hcl   # Pinned provider dependency lock file
├── scripts/
│   └── agent.py              # Main CLI agent script
├── venv/                     # Python virtual environment
└── README.md                 # Project documentation
```

---

## Prerequisites

Before starting, ensure you have the following installed on your Windows machine:

1. **Docker Desktop** (must be open and running in the background)
2. **Python 3.13+**
3. **Terraform CLI** (`v1.15.8` or newer)
4. **AWS CLI v2** (for verifying provisioned resources)

---

## Step-by-Step Setup & Deployment Guide

### Step 1: Start LocalStack via Docker
To avoid LocalStack CLI authentication prompts and license errors, start the community container directly using raw Docker:

```powershell
docker run -d --name localstack_main -p 4566:4566 localstack/localstack
```

Verify that the container is running and wait ~10–15 seconds for it to initialize:
```powershell
docker ps
docker logs localstack_main
```
*(Wait until you see `Ready.` in the logs before proceeding).*

---

### Step 2: Configure Mock AWS Credentials
LocalStack accepts any dummy credentials, provided they are exported in your active PowerShell session:

```powershell
$env:AWS_ACCESS_KEY_ID="mock_access_key"
$env:AWS_SECRET_ACCESS_KEY="mock_secret_key"
$env:AWS_DEFAULT_REGION="us-east-1"
```

Test connectivity to your local endpoint:
```powershell
aws --endpoint-url=http://localhost:4566 s3 ls
```
*(If it returns with no output and no errors, LocalStack is online and ready).*

---

### Step 3: Activate the Python Virtual Environment
Navigate to your project root and activate your virtual environment:

```powershell
cd C:\Users\Owner\aws_agent_project
.\venv\Scripts\Activate.ps1
```

---

### Step 4: Generate Infrastructure Using the DevOps Agent
Launch the interactive CLI agent from the project root:

```powershell
python scripts/agent.py
```

Inside the `DevOps-Agent>` prompt, use the supported commands:
* `generate s3 terraform` — Creates `agent_workspace/main.tf` configured for `http://localhost:4566` with `s3_use_path_style = true` and the target bucket `devops-agent-bucket-xyz`.
* `list buckets` — Queries the local S3 endpoint and lists active buckets.
* `exit` or `quit` — Exits the agent back to your PowerShell prompt.

> **Important:** Always type `exit` to close the Python agent before running Terraform or AWS CLI commands. Do not paste terminal output directly into the `DevOps-Agent>` prompt.

---

### Step 5: Initialize and Apply Terraform
Navigate into the Terraform workspace directory, initialize the pinned provider (`~> 5.0`), and provision your infrastructure:

```powershell
cd C:\Users\Owner\aws_agent_project\agent_workspace
terraform init -upgrade
terraform apply
```

When prompted (`Do you want to perform these actions?`), type **`yes`** and press Enter.

*Expected Output:*
```text
Apply complete! Resources: 1 added, 0 changed, 0 destroyed.

Outputs:

bucket_name = "devops-agent-bucket-xyz"
```

---

### Step 6: Verify the Provisioned Bucket
Confirm that the S3 bucket is live inside your LocalStack container using the AWS CLI or by running `list buckets` inside `agent.py`:

```powershell
aws --endpoint-url=http://localhost:4566 s3 ls
```

*Expected Output:*
```text
2026-11-12 18:30:00 devops-agent-bucket-xyz
```

---

## Troubleshooting & Common Fixes

### 1. `Could not connect to the endpoint URL: "http://localhost:4566/"`
* **Cause:** The `localstack_main` Docker container is stopped or exited.
* **Fix:** Clean up any stale containers and restart LocalStack:
  ```powershell
  docker stop localstack_main
  docker rm localstack_main
  docker run -d --name localstack_main -p 4566:4566 localstack/localstack
  ```

### 2. `Inconsistent dependency lock file` or Provider Version Conflicts (`6.73.0` vs `~> 5.0`)
* **Cause:** Terraform's `.terraform.lock.hcl` file is locked to AWS provider `v6.x`, which hangs when communicating with LocalStack.
* **Fix:** Ensure `required_providers` in `main.tf` specifies `version = "~> 5.0"` and run:
  ```powershell
  terraform init -upgrade
  ```

### 3. `Unable to locate credentials` when running AWS CLI
* **Cause:** PowerShell environment variables reset when opening a new terminal window.
* **Fix:** Re-run the credential exports from **Step 2**.

### 4. LocalStack CLI `License activation failed` or `requires an account`
* **Cause:** Newer versions of the `localstack` CLI wrapper enforce account tokens.
* **Fix:** Bypass the `localstack` CLI wrapper completely and use the `docker run` command in **Step 1**.

### 5. `Plugin did not respond` / `GRPCProvider` Error during `terraform apply`
* **Cause:** Terraform was interrupted mid-refresh or lost connection to LocalStack while querying state.
* **Fix:** Confirm LocalStack is healthy (`docker ps`), allow `Refreshing state...` a few seconds to complete without pressing `Ctrl+C`, and re-run `terraform apply`.