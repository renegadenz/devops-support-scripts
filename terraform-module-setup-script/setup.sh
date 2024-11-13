#!/bin/bash

# create-terraform-module.sh
set -e

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to create file with content
create_file() {
    local file_path="$1"
    local content="$2"
    echo -e "$content" > "$file_path"
}

# Check required commands
if ! command_exists "terraform"; then
    echo "Error: Terraform is not installed"
    exit 1
fi

if ! command_exists "git"; then
    echo "Error: Git is not installed"
    exit 1
fi

# Get module name from user
read -p "Enter the name of your Terraform module: " MODULE_NAME

# Create directory structure
mkdir -p "$MODULE_NAME"/{examples/complete,test}
cd "$MODULE_NAME"

# Initialize git
git init

# Create main Terraform files
touch main.tf variables.tf outputs.tf versions.tf

# Create example directory structure
mkdir -p examples/complete
touch examples/complete/{main.tf,variables.tf,outputs.tf,versions.tf}

# Create test directory
mkdir -p test/fixtures
touch test/fixtures/testing.tfvars

# Create versions.tf content
cat > versions.tf << EOF
terraform {
  required_version = ">= 1.0.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.0.0"
    }
  }
}
EOF

# Create .gitignore
cat > .gitignore << EOF
# Local .terraform directories
**/.terraform/*

# .tfstate files
*.tfstate
*.tfstate.*

# Crash log files
crash.log
crash.*.log

# Exclude all .tfvars files, which are likely to contain sensitive data
*.tfvars
*.tfvars.json

# Ignore override files
override.tf
override.tf.json
*_override.tf
*_override.tf.json

# Ignore CLI configuration files
.terraformrc
terraform.rc

# Ignore Mac/OSX system file
.DS_Store
EOF
