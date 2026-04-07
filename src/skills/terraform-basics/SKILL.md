---
apiVersion: processkit.projectious.work/v1
kind: Skill
metadata:
  id: SKILL-terraform-basics
  name: terraform-basics
  version: "1.1.0"
  created: 2026-04-06T00:00:00Z
spec:
  description: "Infrastructure-as-code with Terraform/OpenTofu — resources, state, modules, plan/apply."
  category: infrastructure
  layer: null
  when_to_use: "Use when writing `.tf` files, managing cloud infrastructure with Terraform or OpenTofu, handling state and backends, or reviewing IaC code."
---

# Terraform Basics

## Level 1 — Intro

Terraform (and OpenTofu) describes cloud infrastructure declaratively
and reconciles reality with `plan` and `apply`. Pin provider versions,
use a remote state backend, and never edit state by hand — get those
three right and the rest is just resource documentation.

## Level 2 — Overview

### Resources and providers

Every project starts with a provider configuration. Pin provider
versions in a `required_providers` block:

```hcl
terraform {
  required_version = ">= 1.5"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "eu-central-1"
}
```

Resources are the core building blocks. Use descriptive names and set
critical arguments explicitly rather than relying on defaults.

### Variables and outputs

Use typed variables with descriptions and validation where
appropriate:

```hcl
variable "instance_type" {
  type        = string
  default     = "t3.micro"
  description = "EC2 instance size"
  validation {
    condition     = can(regex("^t3\\.", var.instance_type))
    error_message = "Only t3 instance types are allowed."
  }
}

output "instance_ip" {
  value       = aws_instance.web.public_ip
  description = "Public IP of the web server"
}
```

Variable types: `string`, `number`, `bool`, `list(type)`, `map(type)`,
`object({...})`. Use `terraform.tfvars` or `-var-file` for
environment-specific values. Never hardcode secrets — use environment
variables or a secrets manager data source.

### Data sources

Use data sources to reference existing infrastructure without
managing it:

```hcl
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }
}
```

### State management

State tracks the mapping between config and real infrastructure.
Configure a remote backend for team use:

```hcl
terraform {
  backend "s3" {
    bucket         = "myproject-tfstate"
    key            = "prod/terraform.tfstate"
    region         = "eu-central-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}
```

Never edit state files manually. Use `terraform state list`,
`terraform state show`, and `terraform state mv` for inspection and
refactoring. Use `terraform import` to bring existing resources under
management.

### Modules

Modules group related resources for reuse. Keep modules focused on a
single concern:

```hcl
module "vpc" {
  source  = "./modules/vpc"
  cidr    = "10.0.0.0/16"
  azs     = ["eu-central-1a", "eu-central-1b"]
}
```

Public modules from the registry use
`source = "terraform-aws-modules/vpc/aws"` with a `version` pin.
Always pin module versions in production.

### Plan / apply / destroy

Always preview before applying:

```bash
terraform init               # download providers and modules
terraform fmt -check         # check formatting
terraform validate           # syntax and internal consistency
terraform plan -out=tfplan   # preview changes, save plan
terraform apply tfplan       # apply the saved plan exactly
```

Use `terraform destroy` with extreme caution — review the plan
output first. For targeted operations, use `-target=resource.name`
sparingly and only for debugging.

## Level 3 — Full reference

### Best practices

- One state per environment (dev/staging/prod) via workspaces or
  separate directories
- Use `lifecycle { prevent_destroy = true }` on critical resources
  (databases, S3 buckets holding data you cannot recreate)
- Tag all resources with project, environment, and owner
- Run `terraform fmt` and `terraform validate` before committing
- Use `moved` blocks for refactoring instead of destroy/recreate
- Keep modules small and focused — a module for VPC, another for
  IAM, another for RDS, rather than one "everything" module

### Worked example: EC2 with security group

```hcl
resource "aws_security_group" "web" {
  name_prefix = "web-"
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "web" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = var.instance_type
  vpc_security_group_ids = [aws_security_group.web.id]
  tags = {
    Name        = "web-server"
    Environment = "prod"
  }
}
```

### Migrating state from local to S3

```bash
# 1. Add backend config to the terraform block
# 2. Run init with migration flag
terraform init -migrate-state
# 3. Verify state is accessible
terraform state list
# 4. Delete local terraform.tfstate after confirming
```

### Importing an existing resource

```bash
# Find the resource ID in the cloud console or CLI
terraform import aws_s3_bucket.logs my-existing-log-bucket
# Write the matching resource block in .tf
terraform plan  # should show no changes if config matches
```

### State surgery with `state mv`

When you rename a resource or move it into a module, Terraform sees
it as "destroy old, create new" unless you update state:

```bash
terraform state mv aws_instance.web module.web.aws_instance.this
terraform state mv aws_instance.old aws_instance.new
```

Prefer a `moved` block in config when possible — it is checked into
version control and replayed automatically:

```hcl
moved {
  from = aws_instance.old
  to   = aws_instance.new
}
```

### Anti-patterns

- **Hardcoded secrets in `.tf` files** — use env vars, `-var`, or a
  secrets manager data source
- **Unpinned providers or modules** — `version = "~> 5.0"` minimum;
  prefer exact pins in production
- **Blind `terraform apply` without a saved plan** — apply the plan
  you reviewed, not a fresh one
- **`terraform state rm` to "fix" drift** — you are lying to
  Terraform about what exists; reach for `import` or `moved` instead
- **`-target` as normal workflow** — it bypasses graph analysis and
  produces partial applies
- **Committing `terraform.tfstate`** — remote backend only; local
  state is a collaboration hazard
- **Monolithic root module** — split by lifecycle (network rarely
  changes, app changes daily); separate state per lifecycle
- **Destroy/recreate when a `moved` block would do** — destructive
  changes should be explicit, not accidental
