---
name: terraspace-secrets
description: Use when retrieving AWS Secrets Manager or SSM Parameter Store values from Terraspace tfvars with aws_secret(), aws_ssm(), :ENV expansion, or expand: false.
---

# Terraspace Secrets

Use this skill when a Terraspace project needs AWS secret or parameter values during tfvars generation.

## Workflow

1. Use AWS Secrets Manager values with `aws_secret()`:

   ```hcl
   password = "<%= aws_secret('db/:ENV/password') %>"
   ```

2. Use AWS SSM Parameter Store values with `aws_ssm()`:

   ```hcl
   ami_id = "<%= aws_ssm('/aws/service/ami-amazon-linux-latest/amzn2-ami-hvm-x86_64-gp2') %>"
   ```

3. Use `:ENV` expansion when the secret or parameter path should follow `TS_ENV`.
4. Use `expand: false` when a literal path contains Terraspace expansion tokens that must not be substituted:

   ```hcl
   value = "<%= aws_secret('literal/:ENV/path', expand: false) %>"
   ```

## Constraints

- Treat helper-expanded values as sensitive. They can appear in `.terraspace-cache` generated tfvars and in Terraform state.
- `.terraspace-cache` is normally ignored and not committed. Terraspace Cloud/Enterprise TFC VCS workflows can be an exception when the generated cache must be committed for Terraform Cloud.
- Keep IAM guidance as a baseline only. Verify project-specific least-privilege permissions before granting actions such as `secretsmanager:GetSecretValue` or `ssm:GetParameter`.
- Do not claim Azure or GCP secret helper support unless official project documentation verifies those helpers.
