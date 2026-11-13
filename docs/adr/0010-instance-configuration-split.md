# Instance configuration: structure in a file, content in the database

Settings that shape the system (available languages, default language, Visit retention, minimum group size in the Visit export) live in Rails configuration and change with a deploy. Settings the Operator should edit without a deploy (museum name, tagline, privacy notice text, Ask more prompt template and provider link) live in the database and are edited in the Operator panel. This stops a mistake in the panel from breaking languages or retention, while keeping day-to-day content editable.
