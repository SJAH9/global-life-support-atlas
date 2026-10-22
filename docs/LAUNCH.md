# Open development and participation launch

## Current state

On 21 October 2026 the author authorized making the source repository public for the Open Atlas work. This supersedes the earlier requirement to keep the repository private. `project.json` still has no participation launch date and public participation remains disabled. Public source access does not constitute a scored research release or open submissions.

## Launch conditions

Before enabling public participation:

- approve and record an ISO launch date in `project.json`;
- complete legal and citation review for every redistributed dataset;
- publish indicator definitions, normalization bounds, and sensitivity tests;
- establish issue forms for observations, corrections, replications, and causal questions;
- establish review states and an auditable decision log;
- add a code of conduct, security policy, contributor terms, and privacy notice;
- verify that community submissions cannot write directly to accepted observations;
- produce an archived, citable release and public methodology version;
- set `participation_enabled` to `true` only in the launch commit;
- verify that the launch is announced as a participation release rather than merely a source-code visibility change.

The generated site checks the configured date before exposing public intake. GitHub visibility and repository permissions remain a separate administrative control and must be changed explicitly.
