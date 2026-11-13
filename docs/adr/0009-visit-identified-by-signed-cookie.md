# A Visit is identified by a random id in a signed session cookie

The Visit id is a random value kept in Rails' signed, strictly necessary session cookie, so no consent banner is needed and no personal data is stored (ADR 0003). It survives language switches and page reloads. Trade-off: a Visit cannot be reopened on another device or shared by link, and clearing cookies starts a new Visit. A shareable URL token was considered and rejected. Visits expire under the Instance's retention policy.
