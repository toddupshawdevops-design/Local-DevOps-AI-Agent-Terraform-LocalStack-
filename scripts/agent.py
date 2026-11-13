import os
import sys
import traceback
from colorama import init, Fore, Style
from tools import TOOL_REGISTRY, USE_LOCAL_AWS

init(autoreset=True)

def ensure_workspace():
    os.makedirs("agent_workspace", exist_ok=True)

def handle_command(user_input):
    ensure_workspace()
    text = user_input.lower()
    
    # Handle Terraform / S3 generation requests directly without crashing
    if "s3" in text or "terraform" in text:
        file_path = "agent_workspace/main.tf"
        hcl_content = '''provider "aws" {
  region                      = "us-east-1"
  access_key                  = "mock_access_key"
  secret_key                  = "mock_secret_key"
  s3_use_path_style           = true
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true

  endpoints {
    s3 = "http://localhost:4566"
  }
}

resource "aws_s3_bucket" "my_bucket" {
  bucket = "devops-agent-bucket-xyz"
}

output "bucket_name" {
  value = aws_s3_bucket.my_bucket.id
}
'''
        with open(file_path, "w") as f:
            f.write(hcl_content)
        
        print(Fore.GREEN + f"\n[Success] Generated Terraform configuration at: {file_path}")
        print(Fore.WHITE + hcl_content + "\n")
        return

    # Handle bucket listing tool check
    if "list" in text and "bucket" in text:
        print(Fore.MAGENTA + "\n[AI Action] Executing tool: list_s3_buckets()")
        try:
            if "list_s3_buckets" in TOOL_REGISTRY:
                res = TOOL_REGISTRY["list_s3_buckets"]()
                print(Fore.BLUE + f"[Tool Result]:\n{res}\n")
            else:
                print(Fore.RED + "Tool 'list_s3_buckets' not registered.")
        except Exception as e:
                print(Fore.RED + f"Error executing tool against LocalStack: {e}")
        return

    # General conversational fallback
    print(Fore.WHITE + f"Agent received: '{user_input}'. Type 'list buckets' or 'generate s3 terraform' to manage infrastructure.\n")

def run_agent():
    print(Fore.CYAN + "\n==============================================")
    print(Fore.CYAN + "===     Local DevOps AI Agent Online       ===")
    print(Fore.CYAN + "==============================================V2")
    print(Fore.YELLOW + f"Mode: {'LocalStack (Emulated :4566)' if USE_LOCAL_AWS else 'Live AWS'}")
    print(Fore.CYAN + "Type 'exit' or 'quit' to stop.\n")

    while True:
        try:
            user_input = input(Fore.GREEN + "DevOps-Agent> " + Style.RESET_ALL).strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit"]:
                print(Fore.CYAN + "Shutting down agent. Goodbye!")
                break

            handle_command(user_input)

        except KeyboardInterrupt:
            print(Fore.CYAN + "\nShutting down agent. Goodbye!")
            sys.exit(0)
        except Exception as e:
            print(Fore.RED + f"\n[CRITICAL AGENT EXCEPTION]: {str(e)}")
            traceback.print_exc()

if __name__ == "__main__":
    run_agent()