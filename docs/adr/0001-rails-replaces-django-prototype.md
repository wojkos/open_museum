# Rebuild on Ruby on Rails; the Django prototype is superseded

The earlier Django + HTMX prototype (`wojkos/cnk_kompas`) proved the product. Open Museum is a full rebuild on Rails 8 (Hotwire, SQLite, Solid Queue/Cache/Cable, Kamal). The maintainer is a former Rails developer and wants to refresh that skill; Rails 8 also gives one deployable process with no Redis or separate worker. The Django repo is frozen as a reference and not maintained in parallel. Its product docs (`docs/source/cnk_kompas/`) are input only; its Django, uv, Fly and `om-*` process material is not followed.

Considered: keep Django (rejected: the prototype stack was chosen for Python familiarity, not product need; maintaining both splits effort).
