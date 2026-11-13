# Ask more hands off to an external AI provider, grounded by an AI note

There is no in-app chat or hosted model. "Ask more" builds a prompt from the Exhibit's description and the Operator's AI note, instructs the model to rely on those facts and admit when it does not know, then opens a configurable provider link (default ChatGPT) with a visible "copy prompt" fallback, since prefilled-prompt deep links are fragile. Each click is recorded on the Visit. This addresses the "no invented facts" guardrail as far as an external provider allows; it cannot be guaranteed.

The prompt comes from an Operator-editable template with placeholders for museum, Exhibit, Gallery, description and AI note (the AI note placeholder is required), in the current UI language, with safe default texts in English and Polish. No automatic translation.

Confirmed: a single provider link from the template plus the copy-prompt button; no multi-provider buttons.
