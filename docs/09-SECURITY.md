# 09 · Security, Privacy & Testing

Baselines we follow: **OWASP ASVS 5.0 (Level 2)** for the API · **OWASP API Security Top 10 (2023)** · **OWASP MASVS v2 / MASTG** for the mobile app · **OWASP Top 10 for LLM Applications (2025)** for the coach · the **SCSVS** and **SWC** checklists for contracts · **SLSA**-style supply-chain hygiene.

## 1. Assets and threats
| Asset | Worst case | Key controls |
|---|---|---|
| TREAT emission | A stolen poster key mints and steals | On-chain daily mint cap, claim delay + guardian veto, KMS keys, chain monitor |
| Walk Bet stakes | The oracle posts false winners | Per-challenge accounting (`paidCount ≤ winners`), 24h dispute window, guardian cancel, oracle timeout |
| User accounts / tokens | Account takeover | Rotating refresh tokens with family revocation, attestation on sensitive calls, SIWE nonce/domain binding |
| Health and location data | Privacy breach | Minimise, encrypt, retention limits, no raw GPS in public data, access logging |
| Reward fairness | Bot farms | 07 anti-cheat, pro-rata budgets, caps |
| Coach | Prompt injection, harmful advice, cost runaway | Frozen prompt, data tagging, deterministic safety layers, spend cap |
| Admin powers | A rogue or compromised admin | Timelock, multisig (mainnet), role separation, `audit_log` |
| Genesis NFTs (1,000) | Over-minting, forged vouchers, rarity manipulation | On-chain cell caps, single-use EIP-712 vouchers, deck draw from commit-reveal seeds, KMS signer |
| Market / rentals | Theft through listings or swaps, rental rug-pulls | Escrow-less atomic trades, expected-price guards, transfer blocked while rented or locked, ERC-4907 (no custody) |

## 2. Smart contracts
- **Design:**
  - non-upgradeable
  - minimal roles, with separate keys for poster, relayer, oracle, syncer and guardian
  - pull payments
  - CEI ordering and `nonReentrant`
  - no `delegatecall`, no `selfdestruct`, no unbounded loops (every batch is capped)
- **Testing:**
  - unit, fuzz and invariant tests, with the coverage targets in 05 §4
  - mutation testing on RewardsDistributor and WalkBetPool (Gambit or vertigo-rs); surviving mutants must be killed or justified in writing
  - **Medusa** or Echidna campaigns for the two 🔴 contracts (nightly)
- **Static analysis** in CI: **Slither** (fail on high or medium) and **Aderyn**. Optional: **Halmos** symbolic checks of invariants 1–3 of the Distributor.
- **Process:** two-person review on every contract PR. Before mainnet: an **external audit**, a public contest (Code4rena, Cantina or Sherlock) and a **bug bounty** (Immunefi).
- **Keys:**
  - Testnet: separate EOAs per role.
  - Mainnet: **AWS KMS secp256k1** (never exported) for poster, relayer, oracle and syncer; admin = Safe 2-of-3 with hardware signers, behind a 48h Timelock; guardian = a separate 1-of-2 Safe that can only pause or veto.
  - Rotation is a scripted runbook (`grantRole` new → `revokeRole` old, through the Timelock).

## 3. Backend API
- **Authentication:**
  - EdDSA JWT (15 min) with `aud`/`iss`/`exp` checked; refresh tokens are opaque, rotating, stored as sha256 and detect reuse.
  - SIWE: one-time nonce, `domain` and `chainId` pinned, expiry ≤ 10 min, and smart-wallet signatures checked through viem.
- **Authorization:** every query is scoped by `account_id` taken from the JWT, never from the request body. This prevents BOLA/IDOR (OWASP API1). Each route has an ownership test.
- **Input:** zod on every body, query and parameter, with body size limits. Drizzle is parameterised, and raw SQL is banned unless reviewed.
- **Abuse:**
  - Redis sliding-window rate limits per account and per IP
  - attestation on sensitive calls
  - an idempotency key on POSTs that cause side effects
  - SSE connection limit: 3 per account
- **Headers:** HSTS, `Content-Security-Policy` on web, `X-Content-Type-Options`, and strict CORS (only web origins, never `*` when credentials are involved).
- **Secrets:** a platform secret store, never in the repo. `gitleaks` runs as a pre-commit hook and in CI, plus GitHub push protection.
- **Logging:** pino redaction (04 §8). No health payloads in logs. Admin actions are written to `audit_log`.
- **Transactions:** one signer key per queue with concurrency 1, nonces tracked in Redis, receipts awaited, and a stuck tx is replaced at +20% gas. Every chain write is idempotent and checks chain state before sending.

## 4. Mobile app (MASVS)
- **Storage:** tokens only in `expo-secure-store` (Keychain / Keystore). No secrets in the bundle, and no API keys apart from the public Reown project ID.
- **Integrity:** App Attest and Play Integrity (07 §3). Jailbreak or root signals lower trust but don't block the app. Hermes bytecode is used for production builds.
- **Network:** TLS only. Certificate pinning is **optional and off by default**, because a wrong pin bricks the app.
- **Deep links and QR codes:** validate the scheme and host. The pack QR is a server-signed payload that expires after 10 minutes. Never auto-open URLs that come from cheers.
- **Wallet:** never ask for or handle seed phrases. All signing happens in the user's wallet through Reown. Show human-readable transaction previews (amount, recipient, contract name).
- **Permissions:** request health, location and notification access **just in time**, with an explanation screen first. Background location is used only during an active session.

## 5. Web (Next.js)
- Strict CSP with nonces, no `dangerouslySetInnerHTML`, and Next middleware headers.
- wagmi for wallet calls, with the chain ID enforced, and a warning shown on the wrong network.
- Share pages are server-rendered from public data only.

## 6. Privacy and data retention
| Data | Retention | Notes |
|---|---|---|
| Minute buckets | 13 months, then aggregated to daily | Needed for audits and appeals |
| GPS session points | **30 days** | After that only distance, duration and H3 res-7 cells are kept |
| Coach messages | 90 days | Processed by Anthropic (disclose this in the privacy policy) |
| Deleted accounts | Soft delete, then hard delete after 30 days | On-chain data can't be erased; disclose that |
| Device and attestation records | While the account is active | Device hash is peppered |

- Users must be **13+** to use the app and **18+** for any on-chain value feature (claiming, bets, tips). Age is self-declared at signup; on mainnet, gate it through the jurisdiction review.
- Health data counts as **special-category data** (GDPR Art. 9): it needs explicit consent, and we offer `/me/export` and `/me` deletion. Follow Apple HealthKit and Google Health Connect policies: never use health data for ads, and declare its use in the store listings.
- Public surfaces show only the handle, level, Pup and badges. City boards are **opt-in** and use H3 res-5 cells.

## 7. AI (OWASP LLM Top 10)
- LLM01 prompt injection: data is wrapped in `<athlete_card>` and flagged as data, and cheers never reach the model.
- LLM02 sensitive information: no PII goes to the model.
- LLM05 output handling: the post-check filter, and model output is never executed or rendered as HTML.
- LLM06 excessive agency: the only "action" tool is a proposal that the user must confirm.
- LLM10 unbounded consumption: per-user limits plus the global USD cap.

## 8. Supply chain and CI (`.github/workflows/`)
- **pnpm 10:**
  - lifecycle scripts are blocked by default (allow-list them in `onlyBuiltDependencies`)
  - set `minimumReleaseAge: 1440` in `pnpm-workspace.yaml`, so no npm version younger than 24 hours is installed (protects against worm-style hijacks)
- **Dependencies:** Renovate with grouped weekly updates; `osv-scanner` and `pnpm audit --prod` fail the build on high or critical findings; optionally Socket.dev on PRs.
- **SAST:** CodeQL (JS/TS) and Semgrep (`p/owasp-top-ten`, `p/typescript`, `p/react`, `p/secrets`).
- **Containers:** Trivy image scan, distroless/Node 24 slim base, non-root user, read-only filesystem.
- **GitHub Actions:**
  - pin every action to a full commit SHA
  - `permissions: read-all` by default
  - use OIDC to reach the cloud, with no long-lived cloud keys
  - restrict `pull_request_target`
  - protect the main branch with required checks and one review
- **SBOM:** generate CycloneDX on release. Sign images with cosign (mainnet).

## 9. Test pyramid
| Layer | Tool | Gate |
|---|---|---|
| Contracts | Foundry unit, fuzz and invariant; Medusa; Slither; Aderyn | 05 §4 |
| Shared logic (formulas, merkle, block draw) | Vitest + fast-check property tests | 100% branches on `econ/` and `anticheat/` |
| API | Vitest + **Testcontainers** (Postgres, Redis) + supertest-style Hono client | Every route: authz, validation, happy path |
| Worker | Vitest with golden fixtures (07 §8) and a full epoch dry run on anvil | Epoch build output matches the fixtures |
| Mobile | Jest + React Native Testing Library; **Maestro** E2E flows (onboarding, sync, walk, claim) | Must pass on an iOS simulator and an Android emulator |
| Web | Playwright (claim flow on anvil, a11y with axe) | — |
| Load | k6: sync 500 RPS, SSE 2k concurrent | p95 < 200 ms |
| Security | DAST with OWASP ZAP baseline against staging | No high findings |

## 10. Incident response (runbook in `docs/runbooks/`)
1. **Detect** (chain monitor, Sentry, user reports).
2. **Contain:** the guardian pauses or vetoes; rotate the role keys; cut off relayer funds.
3. **Assess** using the audit logs and the chain.
4. **Communicate** within 24 hours (status page and community channels).
5. **Fix**, then redeploy or migrate (cumulative claims carry balances over).
6. **Post-mortem** within 7 days.

## 11. Marketplace, loot and app-store policy
- **Loot odds are always visible** (`GET /loot/odds`, shown on every box). Boxes and tickets are never sold. Genesis Draw entry is free.
- **App stores:** Apple's rules (App Review Guidelines 3.1.1 / 3.1.5) restrict NFT and crypto features. For example, owning an NFT may not be allowed to unlock app features, and in-app NFT sales must use In-App Purchase. Google Play has its own blockchain-content policy.
  - Ship the mobile apps with **remote feature flags**: `market`, `rentals`, `genesisPerks`, `mintSale`.
  - By default the **iOS build shows owned NFTs only** (view and equip cosmetics). Trading, renting and the mint run in the **web dapp**. Android can enable more once its policy review is done.
  - Re-check the current store rules before every submission. They change often.
- The market and rentals get an **external audit** together with the other value-bearing contracts before mainnet.
