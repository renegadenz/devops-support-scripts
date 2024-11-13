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

# Create README.md
cat > README.md << EOF
# Terraform Module: ${MODULE_NAME}

## Overview

Brief description of what this module does.

## Usage

\`\`\`hcl
module "${MODULE_NAME}" {
  source = "path/to/module"

  # Required variables
  vpc_id            = "vpc-xxxxxx"
  private_subnets   = ["subnet-xxxxx", "subnet-yyyy"]
  
  # Optional variables
  environment       = "production"
  tags = {
    Environment = "production"
    Team        = "platform"
  }
}
\`\`\`

## Requirements

| Name | Version |
|------|---------|
| terraform | >= 1.0.0 |
| aws | >= 4.0.0 |

## Providers

| Name | Version |
|------|---------|
| aws | >= 4.0.0 |

## Resources

| Name | Type |
|------|------|
| [resource_name.resource](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/resource) | resource |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| vpc_id | The ID of the VPC | \`string\` | n/a | yes |
| private_subnets | List of private subnet IDs | \`list(string)\` | n/a | yes |
| environment | Environment name | \`string\` | \`"development"\` | no |
| tags | Additional tags | \`map(string)\` | \`{}\` | no |

## Outputs

| Name | Description |
|------|-------------|
| resource_id | The ID of the created resource |
| resource_arn | The ARN of the created resource |

## Examples

See the [examples](./examples) directory for working examples to reference:

- [Complete](./examples/complete) - Complete example with all features enabled

## Development

### Prerequisites

- [Terraform](https://www.terraform.io/downloads.html) >= 1.0
- [AWS CLI](https://aws.amazon.com/cli/) >= 2.0

### Testing

1. Clone the repository
2. Initialize Terraform workspace: \`terraform init\`
3. Run Terraform commands: \`terraform plan\`

## License

Apache 2 Licensed. See [LICENSE](LICENSE) for full details.
EOF

# Initialize Terraform
terraform init

# Initial commit
git add .
git commit -m "Initial commit: Basic module structure"

echo "
Terraform module repository '${MODULE_NAME}' has been created successfully!

Directory structure:
${MODULE_NAME}/
├── main.tf
├── variables.tf
├── outputs.tf
├── versions.tf
├── examples/
│   └── complete/
├── test/
│   └── fixtures/
└── README.md

Next steps:
1. cd ${MODULE_NAME}
2. Add your Terraform configuration in main.tf
3. Update the README.md with specific module documentation
4. Create example implementations in examples/complete/
5. Add tests in the test directory

Happy coding!"