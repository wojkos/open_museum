# One Operator account with real authentication; no other roles

The prototype left the catalog admin open or behind a shared password. On a public URL that is unsafe, so the Rails build uses Rails 8's built-in authentication with exactly one Operator whose credentials come from environment/credentials. No sign-up, no roles, no Visitor accounts. Multi-user roles are deferred until a real need appears.

The catalog admin UI uses a ready-made admin gem (not hand-built CRUD); it must work behind this single Operator authentication, so gems that force their own user system (e.g. Devise-based) are disfavoured. Gem choice (Administrate, Avo, ...) is settled in the spec.

Provisional gem choice: Administrate, validated by a spike (language tabs, Active Storage). Fallbacks: Avo (free tier), or a hand-built form for Exhibits only.

Confirmed by the user: Administrate; no password reset by email (recovery = change credentials and restart).

The Administrate spike (Mobility language tabs, Active Storage uploads) runs before `/to-spec`; its result feeds the spec.
