# SQLite on a single machine, deployed with Kamal

An Instance runs on one VPS: Rails 8 with SQLite for data, Solid Queue, Cache and Cable, deployed by Kamal, with backups of the database and uploaded photos (Litestream or cron; chosen in the deployment spec). Expected load is tens to hundreds of Visitors, and the matching rule stays the same at 100×. Horizontal scaling is out of scope; moving to PostgreSQL later would be a real migration, which is why it is recorded. The prototype's Fly.io deployment is dropped.
