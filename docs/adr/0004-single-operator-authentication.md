# One Operator account with real authentication; no other roles

The prototype left the catalog admin open or behind a shared password. On a public URL that is unsafe, so the Rails build uses Rails 8's built-in authentication with exactly one Operator whose credentials come from environment/credentials. No sign-up, no roles, no Visitor accounts. Multi-user roles are deferred until a real need appears.
