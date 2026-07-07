---
name: terraspace-interconnect
description: Use when wiring Terraspace stacks together with output() references, depends_on() ordering, mock outputs, or output-driven stack dependency graphs.
---

# Terraspace Interconnect

Use this skill when a Terraspace stack needs values from another stack or must run after another stack.

## Workflow

1. Put Terraspace dependency helpers in stack tfvars files, not Terraform `.tf` files, when the graph must affect Terraspace ordering.
2. Reference upstream stack outputs with `output()` in tfvars:

   ```hcl
   vpc_id = "<%= output('vpc.vpc_id') %>"
   ```

   Terraspace infers the dependency from the `output()` call.
3. Use `depends_on()` in tfvars only when ordering matters but no output value is needed:

   ```erb
   <% depends_on("vpc") %>
   <% depends_on("network", "security") %>
   ```

4. For `terraspace all plan` before upstream state exists, provide mock values:

   ```hcl
   vpc_id = "<%= output('vpc.vpc_id', mock: 'vpc-123') %>"
   ```

## Constraints

- Do not recommend `terraform_remote_state` as the Terraspace stack-interconnect pattern unless the project already uses it intentionally.
- Do not invent cross-region or cross-account parameters for `output()`. Same-code multi-region/account deployments are handled through Terraspace layering and backend expansion.
- Helpers in `.tf` files may render values, but they are not used for Terraspace graph calculation.
