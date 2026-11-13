# Tests are written in RSpec, not Rails' default Minitest

The maintainer prefers RSpec. The Rails scaffold ships Minitest (`test/`, fixtures); the implementation replaces it with `rspec-rails` (`spec/`) and the CI `test` jobs run `bundle exec rspec`. Anyone expecting the Rails default will find `spec/` instead of `test/`, hence this record. Details of the toolchain (factories, system-spec driver, accessibility checks) are settled in the spec.
