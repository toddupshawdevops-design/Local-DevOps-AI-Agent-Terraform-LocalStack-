# Local DevOps AI Agent (Terraform + LocalStack)

A lightweight, rule-based Python CLI agent that automates local AWS infrastructure provisioning using Terraform and LocalStack. It translates natural language prompts into Infrastructure-as-Code (IaC) configurations and interacts directly with a local emulated AWS environment—allowing you to test cloud workflows without incurring real AWS costs.

---

## Architecture & Tech Stack

* **Language:** Python 3.13
* **Infrastructure as Code:** Terraform (`v1.15.8+`)
* **AWS Provider:** HashiCorp AWS Provider pinned to `~> 5.0` (for LocalStack stability)
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
