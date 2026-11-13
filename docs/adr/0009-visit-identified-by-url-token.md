# A Visit is identified by an unguessable token in its URL

The Visit link carries a long random token (about 22 characters), with no Visitor cookie beyond Rails' standard session/CSRF handling. This survives language switches, closing the tab and opening on another device, lets a family share the Match list, and avoids a cookie-consent banner. Trade-off: anyone with the link sees that Visit's answers, which contain no personal data (ADR 0003). Visits expire under the Instance's retention policy.
