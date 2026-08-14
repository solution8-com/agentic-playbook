# Security pass

Hunt vulnerabilities across the scope, ranked by exploitability. Every finding needs a traced path from untrusted input to the dangerous sink — "this pattern is risky" without the path is a candidate, not a finding. (Authorization has its own dedicated pass; leave "who may do this" gaps to it and focus here on everything else.)

## Hunt

- **Injection.** SQL built by string concatenation or interpolation (with raw drivers like `pg`, every query should be parameterised — grep for template literals containing SELECT/INSERT/UPDATE/DELETE). Command execution with user-influenced arguments. Path traversal: user input joined into filesystem paths without normalisation.
- **Secrets.** Keys, tokens, connection strings, passwords in source, config committed to the repo, or build output. Check obvious history leaks (`git log -p` on env-ish files) — report the leak; rotation is the user's call.
- **Input validation at trust boundaries.** Request bodies/params used without validation of type, range, or shape; mass assignment (spreading a request body into a DB write); unbounded sizes or counts.
- **XSS and unsafe rendering.** `dangerouslySetInnerHTML`, `innerHTML`, unescaped interpolation into HTML/attributes; user-controlled URLs in `href`/`src` (`javascript:` schemes).
- **Auth plumbing.** Token storage and transmission (localStorage vs cookie flags), missing expiry/verification on tokens the code itself validates, permissive CORS, sensitive data in logs or error responses.
- **Dependencies.** `npm audit --omit=dev` (and per-package where the repo is split); report only vulnerabilities whose vulnerable path the code actually exercises, or critical-severity advisories regardless.

## Verify — the false-positive gate

For each candidate, trace and record in the evidence: where the untrusted input enters, the path to the sink, and what (if anything) sanitises it on the way. A sanitiser you actually located clears the finding; name it in your notes so the controller sees it was checked. Severity is exploitability × impact, judged on the traced path.

## Severity

Blocker: exploitable now by an unauthenticated or ordinary user (injection with a live path, leaked live secret). High: exploitable with preconditions, or a leaked secret of unknown liveness. Medium: hardening gaps — validation holes without a demonstrated exploit, risky patterns one refactor from exploitable. Low: defence-in-depth polish.

## Report

Return the JSON findings array per the schema in your dispatch prompt. `evidence` contains the traced input→sink path; `recommendation` is the concrete fix (parameterise, validate with X, move secret to Y).
