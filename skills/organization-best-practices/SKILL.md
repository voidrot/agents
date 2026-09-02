---
name: organization-best-practices
description: Configure multi-tenant organizations, manage members and invitations,
  define custom roles and permissions, set up teams, and implement RBAC using Better
  Auth's organization plugin. Use when users need org setup, team management, member
  roles, access control, or the Better Auth organization plugin.
metadata:
  license-status: UNCONFIRMED
---
## Setup

1. Add `organization()` plugin to server config
2. Add `organizationClient()` plugin to client config
3. Run `npx @better-auth/cli@latest migrate` (built-in adapter) or generate + push for Drizzle/Prisma
4. Verify: check that organization, member, invitation tables exist in your database

```ts
import { betterAuth } from "better-auth";
import { organization } from "better-auth/plugins";

export const auth = betterAuth({
  plugins: [
    organization({
      allowUserToCreateOrganization: true,
      organizationLimit: 5, // Max orgs per user
      membershipLimit: 100, // Max members per org
    }),
  ],
});
```

### Client-Side Setup

```ts
import { createAuthClient } from "better-auth/client";
import { organizationClient } from "better-auth/client/plugins";

export const authClient = createAuthClient({
  plugins: [organizationClient()],
});
```

## Creating Organizations

The creator is automatically assigned the `owner` role.

```ts
const createOrg = async () => {
  const { data, error } = await authClient.organization.create({
    name: "My Company",
    slug: "my-company",
    logo: "https://example.com/logo.png",
    metadata: { plan: "pro" },
  });
};
```

### Controlling Organization Creation

Restrict who can create organizations based on user attributes:

```ts
organization({
  allowUserToCreateOrganization: async (user) => {
    return user.emailVerified === true;
  },
  organizationLimit: async (user) => {
    // Return true when the user has reached their organization limit.
    const plan = await getUserPlan(user);
    return plan.name !== "premium";
  },
});
```

### Creating Organizations on Behalf of Users

Administrators can create organizations for other users (server-side only):

```ts
await auth.api.createOrganization({
  body: {
    name: "Client Organization",
    slug: "client-org",
    userId: "user-id-who-will-be-owner", // `userId` is required
  },
});
```

**Note**: The `userId` parameter cannot be used alongside session headers.


## Active Organizations

Stored in the session and scopes subsequent API calls. Set after user selects one.

```ts
const setActive = async (organizationId: string) => {
  const { data, error } = await authClient.organization.setActive({
    organizationId,
  });
};
```

Many endpoints use the active organization when `organizationId` is not provided (`listMembers`, `listInvitations`, `inviteMember`, etc.).

Use `getFullOrganization()` to retrieve the active org with all members, invitations, and teams.

## Members

### Adding Members (Server-Side)

```ts
await auth.api.addMember({
  body: {
    userId: "user-id",
    role: "member",
    organizationId: "org-id",
  },
});
```

For client-side member additions, use the invitation system instead.

### Assigning Multiple Roles

```ts
await auth.api.addMember({
  body: {
    userId: "user-id",
    role: ["admin", "moderator"],
    organizationId: "org-id",
  },
});
```

### Removing Members

Use `removeMember({ memberIdOrEmail })`. The last owner cannot be removed — assign ownership to another member first.

### Updating Member Roles

Use `updateMemberRole({ memberId, role })`.

### Membership Limits

```ts
organization({
  membershipLimit: async (user, organization) => {
    if (organization.metadata?.plan === "enterprise") {
      return 1000;
    }
    return 50;
  },
});
```

## Invitations

### Setting Up Invitation Emails

```ts
import { betterAuth } from "better-auth";
import { organization } from "better-auth/plugins";
import { sendEmail } from "./email";

export const auth = betterAuth({
  plugins: [
    organization({
      sendInvitationEmail: async (data) => {
        const { email, organization, inviter, invitation } = data;

        await sendEmail({
          to: email,
          subject: `Join ${organization.name}`,
          html: `
            <p>${inviter.user.name} invited you to join ${organization.name}</p>
            <a href="https://yourapp.com/accept-invite?id=${invitation.id}">
              Accept Invitation
            </a>
          `,
        });
      },
    }),
  ],
});
```

### Sending Invitations

```ts
await authClient.organization.inviteMember({
  email: "newuser@example.com",
  role: "member",
});
```

### Shareable Invitation URLs

Better Auth does not generate invitation URLs. Construct your application's
acceptance URL from the invitation ID returned by `inviteMember` or passed to
`sendInvitationEmail`, then deliver it through your own channel:

```ts
const { data } = await authClient.organization.inviteMember({
  email: "newuser@example.com",
  role: "member",
});

const invitationUrl = `https://yourapp.com/accept-invite?id=${data?.id}`;
// Share invitationUrl through your own email or messaging channel.
```

The acceptance page should call the `acceptInvitation` endpoint with the invitation ID.

### Invitation Configuration

```ts
organization({
  invitationExpiresIn: 60 * 60 * 24 * 7, // 7 days (default: 48 hours)
  invitationLimit: 100, // Max pending invitations per org
  cancelPendingInvitationsOnReInvite: true, // Cancel old invites when re-inviting
});
```

## Roles & Permissions

Default roles: `owner` (full access), `admin` (manage members/invitations/settings), `member` (basic access).

### Checking Permissions

```ts
const { data } = await authClient.organization.hasPermission({
  permission: {
    member: ["write"],
  },
});

if (data?.hasPermission) {
  // User can manage members
}
```

Use `checkRolePermission({ role, permissions })` for client-side UI rendering (static only). For dynamic access control, use the `hasPermission` endpoint.

## Teams

### Enabling Teams

```ts
import { organization } from "better-auth/plugins";

export const auth = betterAuth({
  plugins: [
    organization({
        teams: {
            enabled: true
        }
    }),
  ],
});
```

### Creating Teams

```ts
const { data } = await authClient.organization.createTeam({
  name: "Engineering",
});
```

### Managing Team Members

Use `addTeamMember({ teamId, userId })` (member must be in org first) and `removeTeamMember({ teamId, userId })` (stays in org).

Set active team with `setActiveTeam({ teamId })`.

### Team Limits

```ts
organization({
  teams: {
      maximumTeams: 20, // Max teams per org
      maximumMembersPerTeam: 50, // Max members per team
      allowRemovingAllTeams: false, // Prevent removing last team
  }
});
```

## Dynamic Access Control

### Enabling Dynamic Access Control

```ts
import { organization } from "better-auth/plugins";

export const auth = betterAuth({
  plugins: [
    organization({
      dynamicAccessControl: {
        enabled: true,
      },
    }),
  ],
});
```

### Creating Custom Roles

```ts
await authClient.organization.createOrgRole({
  role: "moderator",
  permission: {
    member: ["read"],
    invitation: ["read"],
  },
});
```

Use `updateOrgRole({ roleId, permission })` and `deleteOrgRole({ roleId })`. Pre-defined roles (owner, admin, member) cannot be deleted. Roles assigned to members cannot be deleted until reassigned.

## Lifecycle Hooks

Execute custom logic at various points in the organization lifecycle:

```ts
organization({
  organizationHooks: {
    beforeCreateOrganization: async ({ organization: data, user }) => {
      // Validate or modify data before creation
      return {
        data: {
          ...data,
          metadata: { ...data.metadata, createdBy: user.id },
        },
      };
    },
    afterCreateOrganization: async ({ organization }) => {
      // Post-creation logic (e.g., send welcome email, create default resources)
      await createDefaultResources(organization.id);
    },
    beforeDeleteOrganization: async ({ organization }) => {
      // Cleanup before deletion
      await archiveOrganizationData(organization.id);
    },
    afterAddMember: async ({ organization }) => {
      await notifyAdmins(organization.id, `New member joined`);
    },
    afterCreateInvitation: async ({ invitation }) => {
      await logInvitation(invitation);
    },
  },
});
```

## Schema Customization

Customize table names, field names, and add additional fields:

```ts
organization({
  schema: {
    organization: {
      modelName: "workspace", // Rename table
      fields: {
        name: "workspaceName", // Rename fields
      },
      additionalFields: {
        billingId: {
          type: "string",
          required: false,
        },
      },
    },
    member: {
      additionalFields: {
        department: {
          type: "string",
          required: false,
        },
        title: {
          type: "string",
          required: false,
        },
      },
    },
  },
});
```

## Security Considerations

### Owner Protection

- The last owner cannot be removed from an organization
- The last owner cannot leave the organization
- The owner role cannot be removed from the last owner

Always ensure ownership transfer before removing the current owner:

```ts
// Transfer ownership first
await authClient.organization.updateMemberRole({
  memberId: "new-owner-member-id",
  role: "owner",
});

// Then the previous owner can be demoted or removed
```

### Organization Deletion

Deleting an organization removes all associated data (members, invitations, teams). Prevent accidental deletion:

```ts
organization({
  disableOrganizationDeletion: true, // Disable via config
});
```

Or implement soft delete via hooks:

```ts
organization({
  organizationHooks: {
    beforeDeleteOrganization: async ({ organization }) => {
      // Archive instead of delete
      await archiveOrganization(organization.id);
      throw new Error("Organization archived, not deleted");
    },
  },
});
```

### Invitation Security

- Invitations expire after 48 hours by default
- Only the invited email address can accept an invitation
- Pending invitations can be cancelled by organization admins

## Complete Configuration Example

```ts
import { betterAuth } from "better-auth";
import { organization } from "better-auth/plugins";
import { sendEmail } from "./email";

export const auth = betterAuth({
  plugins: [
    organization({
      // Organization limits
      allowUserToCreateOrganization: true,
      organizationLimit: 10,
      membershipLimit: 100,
      creatorRole: "owner",

      // Invitations
      invitationExpiresIn: 60 * 60 * 24 * 7, // 7 days
      invitationLimit: 50,
      sendInvitationEmail: async (data) => {
        await sendEmail({
          to: data.email,
          subject: `Join ${data.organization.name}`,
          html: `<a href="https://app.com/invite/${data.invitation.id}">Accept</a>`,
        });
      },

      // Hooks
      organizationHooks: {
        afterCreateOrganization: async ({ organization }) => {
          console.log(`Organization ${organization.name} created`);
        },
      },
    }),
  ],
});
```
