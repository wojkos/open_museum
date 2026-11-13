# SQLite on a single machine, first Instance on Fly.io

An Instance runs on one machine: Rails 8 with SQLite for data, Solid Queue, Cache and Cable. Expected load is tens to hundreds of Visitors, and the matching rule stays the same at 100×. Horizontal scaling is out of scope; moving to PostgreSQL later would be a real migration, which is why it is recorded.

The first Instance deploys to Fly.io (a volume for SQLite and uploaded photos). Automatic CD and backup tooling remain open (issue #1); CI (RSpec, RuboCop, Brakeman, bundler-audit on GitHub Actions) comes first and deploys are manual until then. The Kamal files in the scaffold are not the chosen path.
