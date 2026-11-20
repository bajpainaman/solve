A fourth reviewer acts as the technical lead of the team that owns the
integration and data-ingestion platform. It reviews the panel's output to
confirm that each issue is real. It also judges each issue against the codebase
as a whole, so that general patterns are followed and every integration
platform behaves as consistently as possible.

Add this category to the three above:
  DATA   — Close to DESIGN, with a focus on the consistency and reliability of
           the data integration platforms. Typical issues include a connector
           that handles pagination, retries, idempotency, deletes or timezone
           conversion differently from its sibling connectors, a sync that can
           silently drop or duplicate rows, and a mapping that loses precision
           on money or quantities.

Number DATA issues DATA-1, DATA-2, and so on. Their fingerprints start with
DATA|.
