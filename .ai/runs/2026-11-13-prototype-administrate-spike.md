# Run: prototype administrate-spike (2026-11-13)

- **Goal:** Round 7 prerequisite: Administrate + Mobility language tabs + Active Storage on Rails 8.
- **Spec used:** none (prototype); ADR 0004, 0011.
- **Plan:** scratch copy of the scaffold in `prototype/administrate-spike`, add administrate/mobility/auth, drive via integration tests in docker.
- **Key decisions:** key_value Mobility backend; custom TranslatedField; add-on gem for Active Storage; Rails 8 `generate authentication` for the gate.
- **Verification:** `bin/rails test test/spike_test.rb` in docker: 5 runs, 0 failures (login gate, two-locale create/edit, photo, validation, sort asc/desc, search).
- **Outcome:** GO, human confirmed; ADR 0004 updated. Spike kept on branch `prototype/administrate-spike`.
- **Open questions:** real-browser check of tab JS; tab a11y.
