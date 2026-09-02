# Private development and public launch

## Current state

The repository must remain private. `project.json` has no launch date and public participation is disabled.

## Launch conditions

Before changing repository visibility:

- approve and record an ISO launch date in `project.json`;
- complete legal and citation review for every redistributed dataset;
- publish indicator definitions, normalization bounds, and sensitivity tests;
- establish issue forms for observations, corrections, replications, and causal questions;
- establish review states and an auditable decision log;
- add a code of conduct, security policy, contributor terms, and privacy notice;
- verify that community submissions cannot write directly to accepted observations;
- produce an archived, citable release and public methodology version;
- set `participation_enabled` to `true` only in the launch commit;
- change GitHub visibility only after the launch commit is verified.

The generated site checks the configured date before exposing public intake. GitHub visibility and repository permissions remain a separate administrative control and must be changed explicitly.
