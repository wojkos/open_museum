# Engineering Standards — Open Museum (Rails 8.1)

Source: distilled from the official *Getting Started with Rails* guide (the "Store" tutorial), adapted to this
repository. Treat it as the default way to build things here: when a task touches one of these areas, follow the
rule; if you must diverge, record why in the spec or run log.

Stack: Ruby 3.2+ (image uses 3.4), Rails 8.1, SQLite, Propshaft, importmap, Hotwire (Turbo + Stimulus),
Solid Queue / Solid Cache / Solid Cable, Kamal for deploys. Minitest + fixtures.

## 1. Philosophy

- **Convention over configuration.** Use Rails' naming and layout conventions; do not add config or `require`
  statements Rails already handles (autoloading via Zeitwerk: file `product_mailer.rb` ⇒ `ProductMailer`).
- **DRY.** One authoritative place per piece of knowledge: extract `before_action`s, partials, concerns.
- Run everything through `bin/rails` (not a global `rails`) so the app's Rails version is used.

## 2. Layout and MVC

- `app/models` data and domain logic · `app/controllers` request handling · `app/views` rendering (ERB).
- Keep controllers thin (load, authorize, call model, respond). Domain logic lives in models/concerns.
- Tests live in `test/`, fixtures in `test/fixtures/`. Scripts in `script/`, extra rake tasks in `lib/tasks/`
  (never edit `Rakefile`).

## 3. Models and database

- Generate with `bin/rails generate model Name attr:type`. Model names singular, tables plural.
- **Every schema change is a migration**; never edit `db/schema.rb` by hand. Run `bin/rails db:migrate`;
  undo the last with `bin/rails db:rollback`. Commit both the migration and `db/schema.rb`.
- Name migrations by convention (`AddInventoryCountToProducts inventory_count:integer`) so the generator
  fills in `add_column`. Add `default:` / `null: false` where a column must never be nil.
- Associations come in pairs: `belongs_to` (via `product:belongs_to`, adds an FK) and
  `has_many ..., dependent: :destroy` on the other side.
- Validate in the model (`presence`, `numericality`, …). Use `errors.full_messages` for UI messages.
- Use `generates_token_for` for signed, purpose-scoped tokens (e.g. unsubscribe links) rather than
  home-grown tokens.
- Prefer callbacks narrowly: `after_update_commit` with an `if:` guard for side effects such as sending mail.
- Use `reload!` in the console after editing code.
- **Concerns** (`ActiveSupport::Concern`) group a self-contained feature: `app/models/product/notifications.rb`
  defines `Product::Notifications`; the model does `include Notifications`. Put associations/callbacks in the
  `included do … end` block.

## 4. Routing

- Use `resources :things` for CRUD instead of hand-written verb routes; restrict with `only:`/`except:`
  when not all 8 routes apply. Use singular `resource` for things without an id (e.g. `resource :unsubscribe`).
- Nest resources only to express ownership (`resources :products do resources :subscribers, only: :create end`).
- Define `root`. Inspect routes with `bin/rails routes`.
- Always use route helpers (`product_path(p)`, `products_url`) and `link_to`, never hard-coded paths.
  `_path` in views, `_url` in mailers/anywhere the link leaves the browser.

## 5. Controllers

- Standard seven actions in order: `index show new create edit update destroy`. Public methods are actions;
  helpers go under `private` (indent private methods one level, per the omakase RuboCop style).
- Extract repeated lookups into `before_action :set_x, only: [...]`.
- **Strong parameters:** `params.expect(product: [ :name, :description, … ])`. Every new form field must be
  added to the permitted list.
- On failed save: `render :new, status: :unprocessable_entity` (422). On success: `redirect_to @record`
  (optionally with `notice:`). Flash messages: `notice` (success) / `alert` (failure), rendered in the layout.
- Share data with views via instance variables: plural for collections (`@products`), singular for one record.
- Locale: switch per request with an `around_action` + `I18n.with_locale`.

## 6. Views

- ERB: `<%= %>` outputs, `<% %>` doesn't. Use `debug @var` only for temporary diagnosis.
- Reuse markup with partials (`_form.html.erb`) and **local variables** (`render "form", product: @product`),
  not instance variables.
- Use `form_with model: …` form builders (CSRF, URL, method and button label are handled for you). Show
  validation errors inside the form.
- Destructive actions use `button_to … method: :delete, data: { turbo_confirm: "Are you sure?" }`.
- Shared chrome (nav, flash, log out button) goes in `app/views/layouts/application.html.erb`.
- Fragment-cache expensive/stable markup with `cache @record do … end`; the key tracks both the record and the
  template digest. Toggle dev caching with `bin/rails dev:cache`.
- All user-facing text goes through I18n: `t ".title"` (relative lookup ⇒ `en.products.index.title`).
  Add every key to **every** locale file in `config/locales/`.

## 7. Authentication and authorization

- Use the built-in generator: `bin/rails generate authentication` (User, Session, bcrypt), then migrate.
- **Secure by default:** all controllers require authentication; opt out explicitly per controller with
  `allow_unauthenticated_access only: %i[ index show ]`.
- Hide privileged UI with `authenticated?` in views — but never rely on hidden links as the security check;
  the controller must enforce it.
- Users in production are created via `bin/kamal console` (`User.create!`); never commit credentials.

## 8. Rich text, files, mail, jobs

- **Action Text** (`bin/rails action_text:install`): `has_rich_text :description`, `form.rich_textarea`.
- **Active Storage**: `has_one_attached :featured_image`, `form.file_field … accept: "image/*"`, guard display
  with `.attached?`. Permit the attachment param.
- **Action Mailer**: mailers in `app/mailers`, both `.html.erb` and `.text.erb` templates, `…_url` helpers,
  pass data with `Mailer.with(product:, subscriber:).action`, always send with `deliver_later`.
- Every marketing/notification email includes an unsubscribe link.
- **Background jobs** run through Active Job. `:async` in development, **Solid Queue** (DB-backed,
  `SOLID_QUEUE_IN_PUMA: true`) in production. Anything slow or fan-out (mail to many recipients) goes to a job.

## 9. Front end

- **Propshaft** serves `app/assets` (CSS, images); write plain CSS in `app/assets/stylesheets/application.css`.
- **Importmap**: JavaScript modules pinned in `config/importmap.rb`; no bundler/build step unless a spec
  requires one.
- **Hotwire first:** Turbo for navigation/forms/streams, Stimulus controllers in `app/javascript/controllers`
  for custom behavior. Avoid ad-hoc JavaScript and SPA frameworks.

## 10. Testing

- Minitest + fixtures. Every model gets fixtures with readable names (`products(:tshirt)`); reference
  associations by fixture name, never by id.
- Run: `bin/rails test` (all) or `bin/rails test test/models/product_test.rb` (one file).
- Mailer behavior: `include ActionMailer::TestHelper` and `assert_emails n do … end`; mailer tests assert
  subject, recipients, sender and body.
- A bug fix adds a regression test. A new feature adds model, controller (and mailer, when relevant) tests.

## 11. Code quality and security gates

All must pass before work is declared done (CI runs the same):

```bash
bin/rails test
bin/rubocop          # autocorrect with: bin/rubocop -a
bin/brakeman         # security scan; expect "No warnings found"
```

- Secure params (strong parameters), CSRF tokens (form builders), and escaped output (ERB default) are
  non-negotiable; never use `raw`/`html_safe` on user input.
- Secrets via Rails credentials / `.kamal/secrets` / environment, never in the repo
  (`KAMAL_REGISTRY_PASSWORD` etc. are exported, not committed).

## 12. CI/CD and deployment

- `.github/workflows` runs RuboCop, Brakeman and the test suite on push/PR; keep it green.
- Deploy with **Kamal** (Docker; production `Dockerfile` serves via Thruster): configure `config/deploy.yml`
  (`service`, `image`, `servers`, `registry`, `proxy: ssl: true, host:`), then `bin/kamal setup` the first
  time and `bin/kamal deploy` afterwards. Production console: `bin/kamal console`.
- Deployments and anything touching production, registries or credentials need explicit user approval.

## 13. Workflow checklist (per feature)

1. Spec in `.ai/specs/` (non-trivial work); read `.ai/lessons.md`.
2. Generate (model/migration/controller) with `bin/rails generate …`; `bin/rails db:migrate`.
3. Route (`resources`) → controller actions → views/partials → I18n keys.
4. Fixtures + tests; run `bin/rails test`, `bin/rubocop`, `bin/brakeman`.
5. Log the run in `.ai/runs/`, record lessons, move the spec to `specs/implemented/`.

## Reference

- Getting Started with Rails: https://guides.rubyonrails.org/getting_started.html
- Related guides: Active Record Basics, Layouts and Rendering, Testing Rails Applications, Debugging Rails
  Applications, Securing Rails Applications.
