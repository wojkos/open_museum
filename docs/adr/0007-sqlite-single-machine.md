# SQLite on a single machine

An Instance runs on one machine: Rails 8 with SQLite for data, Solid Queue, Cache and Cable. Expected load is tens to hundreds of Visitors, and the matching rule stays the same at 100×. Horizontal scaling is out of scope; moving to PostgreSQL later would be a real migration, which is why it is recorded. The deployment target, CD pipeline and backup tooling are deliberately left open (Fly.io was chosen for the Django prototype mainly because of Python): see issue #1.
