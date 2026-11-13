# Translated catalog fields use the Mobility gem

ADR 0006 requires per-language catalog text. We implement it with Mobility (key-value or table backend) rather than `name_pl`/`name_en` columns, so the language list comes from Instance configuration (ADR 0010) and adding a language needs no migration. If a spike with the chosen admin gem shows Mobility is awkward, this ADR is revisited before implementation.
