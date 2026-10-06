# 11 · Build Plan (task cards)

## How to use this file
1. **One task per session or sitting.** Follow the workflow in `CONTRIBUTING.md`.
2. Each card has a **complexity tag**:

   | Tag | Meaning | Examples |
   |---|---|---|
   | 🔴 **CRITICAL** | Holds funds or decides fairness; needs the most careful work and review | RewardsDistributor, WalkBetPool, anti-cheat, security reviews |
   | 🟠 **COMPLEX** | Native integrations, value-bearing contracts, reward or loot pipelines | Health APIs, attestation, GenesisNFT, market, rentals, loot |
   | 🟡 **STANDARD** | A feature built straight from the spec | Most screens, endpoints, games |
   | 🟢 **SIMPLE** | Scaffolding, config, copy, checklists | Monorepo setup, tokens, launch kit |

3. **Escalate** a task if the same check fails twice, or if it turns out to touch money or security logic the card didn't mention.
4. Totals: 🔴 6 · 🟠 11 · 🟡 35 · 🟢 13 = **65 tasks**.

**Milestones:**
- **M1 Local loop:** P0 → C-01…C-11 → B-01…B-08 → M-01…M-05. You can sync steps, build an epoch on anvil, and claim.
- **M2 Internal testnet:** + B-09…B-16, M-06…M-13, C-08, and a deploy to Chikyū. Ship to TestFlight / Play Internal.
- **M2b Collect & Play:** + A-01, B-17…B-20, G-01…G-03, M-14…M-16. Avatars, items, loot, Forge, Genesis, market and games.
- **M3 Public testnet beta:** + W-01…W-03, Q-01, Q-02, S-01, L-01.
- **M4 Mainnet:** L-02 go/no-go after testnet season 1, an external audit, and legal review.

Card format: **Depends** · **Read** · **Paths** · **Do** · **Done when**.

---

## Phase 0 · Foundations

### P0-01 · Monorepo scaffold 🟢
- **Depends** — · **Read** CONTRIBUTING.md, 04 §3 §4 §6, 09 §8 (pnpm settings)
- **Paths** root configs, `packages/{config,shared,db,ui-tokens,contracts}`, `apps/{api,worker,mobile,web}` (package.json stubs only)
- **Do**
  - Set up pnpm 10 workspaces with `minimumReleaseAge: 1440`, Turborepo, Biome, TS strict bases, `.nvmrc` (24) and `.editorconfig`.
  - Add `docker-compose.yml` (postgres:17, redis:7), `.env.example` with every variable from 04 §6, lefthook pre-commit (biome + gitleaks), and `forge init packages/contracts --no-git` with OZ v5 installed through `forge install`.
- **Done when** `pnpm install && pnpm -w lint && pnpm -w typecheck && pnpm -w test` and `forge build` all pass on a clean clone.

### P0-02 · Verify chain facts + EVM probe 🟢 (needs HUMAN: a throwaway key funded from the faucet)
- **Depends** P0-01 · **Read** 04 §2
- **Paths** `packages/contracts/script/Probe.s.sol`, `packages/contracts/src/probe/*`, `docs/DECISIONS-LOG.md`
- **Do**
  - Confirm the RPC, explorer and faucet URLs from docs.dogeos.com.
  - Deploy tiny probe contracts compiled for `shanghai` and `cancun` (PUSH0, TSTORE, MCOPY), and call the precompiles listed in 04 §2.
  - Check whether Multicall3, the CREATE2 deployer, the Safe factory, ERC-4337 EntryPoint and EIP-7702 exist.
  - Log the balance before and after each step.
- **Done when** every VERIFY row in 04 §2 is resolved in DECISIONS-LOG and `evm_version` is chosen. Update 04 §2 in place.

### P0-03 · CI pipelines 🟡
- **Depends** P0-01 · **Read** 09 §8, §9
- **Paths** `.github/workflows/{ci,contracts,security}.yml`, `renovate.json`
- **Do** Write the jobs: lint, typecheck and test; forge test + coverage + slither + aderyn; CodeQL; Semgrep; osv-scanner; gitleaks.
- **Rule:** pin every action to a full SHA. **Never invent SHAs.** Resolve each one with `gh api repos/<o>/<r>/commits/<tag> --jq .sha`, or use `pinact`.
- **Done when** the workflows pass `actionlint` and every pinned SHA has been looked up and verified.

### P0-04 · Shared core: chains, constants, formulas 🟡
- **Depends** P0-01 · **Read** 02 §2–§8 §10, 03 §3–§6 §11–§12, 04 §2
- **Paths** `packages/shared/src/{chains.ts,game/,econ/,blocks/,schemas/}`
- **Do**
  - Write `chains.ts` (viem `defineChain`) and the constants.
  - Write a **table generator script** for `LEVEL_XP` and `PUP_LEVEL_XP`, and commit the generated tables.
  - Implement with bigint: `dailyEmission`, `walkPoints`, `proRataWithCap`, `betPayouts`, `leagueShares`, `quests.assign`, `blocks.draw`.
  - Write `blocks/verify.ts`, which recomputes the draws from a `blocks.json`.
- **Done when** Vitest + fast-check reach 100% branch coverage on `econ/` and `blocks/`, and the reference values in 02 §5 and 03 §3 match.

### P0-05 · UI tokens 🟢
- **Depends** P0-01 · **Read** 10 §2, `prototype/index.html` `:root` vars
- **Paths** `packages/ui-tokens/`
- **Do** Export the tokens as a TS object, CSS variables, a Tailwind v4 theme, and a NativeWind preset, all with light and dark.
- **Done when** a snapshot test of the token values passes.

### T-01 · Tokenomics simulator 🟡
- **Depends** P0-04 · **Read** 03 (all)
- **Paths** `packages/shared/scripts/sim.ts`, `docs/sim/README.md`
- **Do**
  - Simulate 365 days under three scenarios: slow, viral, and 30% bots.
  - Report daily mint, burn, rewards per honest user, and the per-user cap hit rate.
- **Done when** the invariants (never above the schedule, cap respected) are asserted and the summary table is written to `docs/sim/`.

## Phase 1 · Contracts (`packages/contracts`)

### C-01 · TreatToken 🟡
- **Depends** P0-02 · **Read** 05 §2.1 §4, 03 §1–§2
- **Paths** `src/TreatToken.sol`, `src/interfaces/ITreat.sol`, `test/TreatToken.t.sol`
- **Done when**
  - Tests cover the genesis sum, the cap, the minter role, permit, and burn/burnFrom.
  - Coverage ≥ 90%.

### C-02 · RewardsDistributor 🔴 CRITICAL
- **Depends** C-01 · **Read** 05 §2.2 §4, 03 §3 §7 §9, 09 §2
- **Paths** `src/RewardsDistributor.sol`, `test/RewardsDistributor.t.sol`, `test/invariant/Distributor.invariant.t.sol`, `test/fixtures/merkle-*.json`
- **Do**
  - Implement exactly to spec, including the check order.
  - Write a handler-based invariant suite covering invariants 1–7.
  - Cross-check with a TS-generated StandardMerkleTree fixture.
- **Done when**
  - Coverage ≥ 95% on lines and branches.
  - Slither is clean.
  - The doc comment on each function explains *why*, written in the team voice.

### C-03 · GenesisNFT 🟠 COMPLEX
- **Depends** C-01 · **Read** 05 §2.3 §4, 02 §10 §19
- **Paths** `src/GenesisNFT.sol`, `src/interfaces/IGenesis.sol`, `test/GenesisNFT.t.sol`, `test/invariant/Genesis.invariant.t.sol`
- **Do** Build the cap matrix in the constructor (checked to sum to 1,000), EIP-712 vouchers (including the gasless relayer path and the paid mint split), leash lock, ERC-4907 with the no-override rule, Pup sync and royalties.
- **Done when** invariants 1–6 hold under fuzzing, and coverage ≥ 95%.

### C-04 · BadgeSBT 🟢
- **Depends** P0-02 · **Read** 05 §2.4, 02 §9
- **Paths** `src/BadgeSBT.sol`, `test/BadgeSBT.t.sol`
- **Done when** transfers and approvals revert, duplicates are skipped, stackable medals work, and holders can burn.

### C-05 · WalkBetPool 🔴 CRITICAL
- **Depends** C-01 · **Read** 05 §2.5 §4, 03 §11, 09 §1–§2
- **Paths** `src/WalkBetPool.sol`, `test/WalkBetPool.t.sol`, `test/invariant/BetPool.invariant.t.sol`
- **Do**
  - Implement every path: join, permit, leave, results, dispute, finalize, claim, cancel, timeout, refund.
  - Write invariants 1–5, including isolation between challenges.
- **Done when** coverage ≥ 95% and the fuzz tests over (N, Wn, S) match the 03 §11 math exactly.

### C-06 · CheerRouter 🟡
- **Depends** C-01 · **Read** 05 §2.6
- **Paths** `src/CheerRouter.sol`, `test/CheerRouter.t.sol`
- **Done when** the fee split, native send, permit path, self-tip and minimum checks, pause, and reentrancy (malicious receiver) tests all pass.

### C-09 · MuchMarket 🟠 COMPLEX
- **Depends** C-03 · **Read** 05 §2.8 §4, 03 §10
- **Paths** `src/MuchMarket.sol`, `test/MuchMarket.t.sol`, `test/invariant/Market.invariant.t.sol`
- **Done when** listings, buy (TREAT and DOGE), the fee split, stale-listing clearing and swaps with TREAT legs are tested, along with every case in 05 §4 (malicious receiver, rejecting seller, front-run guard). Coverage ≥ 95%.

### C-10 · RentalHouse 🟠 COMPLEX
- **Depends** C-03 · **Read** 05 §2.9 §2.3 (ERC-4907 rules)
- **Paths** `src/RentalHouse.sol`, `test/RentalHouse.t.sol`
- **Done when** paid rent, free lending to a reserved friend, no override of an active rental, owner transfer blocked during a rental, expiry and the fee split are tested. Coverage ≥ 95%.

### C-11 · TreatSink 🟡
- **Depends** C-01 · **Read** 05 §2.7, 03 §10
- **Paths** `src/TreatSink.sol`, `test/TreatSink.t.sol`
- **Done when** every purpose's split sums to 10,000, burn/shelter/treasury amounts are exact (including dust), and the permit path and pause are tested.

### C-07 · Deploy + export 🟡
- **Depends** C-02…C-06, C-09…C-11 · **Read** 05 §3, 04 §2 (gas issue)
- **Paths** `script/Deploy.s.sol`, `script/export.ts`, `addresses/`, `packages/contracts/package.json` scripts
- **Do**
  - Implement the deploy script per spec, with balance logging and **on-chain role assertions**.
  - Add `pnpm dev:chain` (anvil + deploy) and generate the TS ABIs.
  - Document the testnet deploy command. **The HUMAN runs it with the real key.**
- **Done when** a local deploy passes its assertions and `addresses/31337.json` plus the ABIs are generated.

### C-08 · Contract security pass 🔴 CRITICAL
- **Depends** C-07 · **Read** 05, 09 §2 §11
- **Paths** `docs/audits/internal-01.md`, fixes in `src/`
- **Do**
  - Run Slither, Aderyn, Medusa (nightly config) and mutation testing on C-02, C-03, C-05, C-09 and C-10.
  - Do a manual review against the SCSVS checklist.
  - Fix the findings and record each one with its status.
- **Done when** there are no open high or medium findings and the report is committed.

## Phase 2 · Backend (`apps/api`, `apps/worker`, `packages/db`)

### B-01 · API + worker skeleton 🟢
- **Depends** P0-04 · **Read** 06 §3 (envelope, codes), 04 §8, 09 §3
- **Paths** `apps/api/src/{app.ts,env.ts,middleware/}`, `apps/worker/src/{index.ts,queues.ts}`
- **Do** Build Hono + zod-openapi, a zod env loader, pino with redaction, a request ID, the error envelope, a Redis rate limiter, `/healthz` and `/readyz`, and the BullMQ cron registry.
- **Done when** the tests for the envelope and the rate limiter pass.

### B-02 · DB schema + seed 🟡
- **Depends** B-01 · **Read** 06 §1
- **Paths** `packages/db/src/schema/*.ts`, `migrations/`, `seed.ts`
- **Done when** migrations apply to an empty database, the seed creates 50 accounts with 30 days of realistic minutes, and the Testcontainers test passes.

### B-03 · Auth + attestation 🟠 COMPLEX
- **Depends** B-02 · **Read** 06 §2, 07 §3, 09 §3
- **Paths** `apps/api/src/auth/`, `apps/api/src/attest/{apple.ts,google.ts}`
- **Do**
  - Implement register, refresh rotation with reuse detection, logout, and SIWE link/login (viem).
  - Write the App Attest attestation and assertion verifiers, the Play Integrity decode, the `requireAssertion` middleware, and the dev bypass guard.
- **Done when**
  - There are tests for every rejection branch, including replayed assertions and a counter that didn't increase.
  - Every route has a BOLA test.

### B-04 · Activity ingest + sessions 🟡
- **Depends** B-03 · **Read** 06 §3 (activity, sessions, today), 07 §2, R6
- **Paths** `apps/api/src/activity/`, `apps/api/src/sessions/`
- **Done when**
  - Sync stores the max per minute, enforces the bounds, and lets values change only before the day is frozen.
  - Sessions record their points.
  - `/today` returns its schema.
  - Tests use the seed data.

### B-05 · Anti-cheat engine 🔴 CRITICAL
- **Depends** B-04 · **Read** 07 (all), 03 §4
- **Paths** `apps/worker/src/anticheat/`, `fixtures/`, job `score-user-day`
- **Do**
  - Write R1–R12 as pure functions, plus the trust-score update and the pack-overlap check (R10).
  - Wire it in with the 60 s debounce.
- **Done when**
  - All golden fixtures match.
  - The property tests pass.
  - Honest fixtures get zero penalties.

### B-06 · Game engine 🟡
- **Depends** B-05 · **Read** 02 §3–§7 §9 §14
- **Paths** `apps/worker/src/game/`, `apps/api/src/game/`, job `finalize-local-day`
- **Do** XP events, levels (from the table), streak, shields, rest/injury mode, quests and the chest, and badge evaluation.
- **Done when** time-zone edge cases (DST, tz change) are tested.

### B-07 · Leagues + leaderboards 🟡
- **Depends** B-06 · **Read** 02 §8, 06 §4
- **Paths** `apps/worker/src/leagues/`, `apps/api/src/leagues/`
- **Done when** cohort fill, promote/demote, ties, and reward shares (summing to ≤ the pool) are tested, and Redis boards rebuild from Postgres.

### B-08 · Epoch pipeline + claims 🟠 COMPLEX
- **Depends** B-06, B-07, C-07 · **Read** 03 §3–§9, 04 §5B–C, 05 §2.2, 06 §4
- **Paths** `apps/worker/src/epoch/`, `apps/worker/src/chain/txQueue.ts`, `apps/api/src/rewards/`
- **Do**
  - Build allocations (W, B, Q, leagues), pending rewards for unlinked accounts, and the cumulative totals.
  - Build the StandardMerkleTree and the R2 files.
  - Implement the commit–reveal seed and `postEpoch` through a single-concurrency tx queue, plus root activation and `claimMany` relaying.
- **Done when** a full dry run on anvil (seed → epoch → claim) passes, and `blocks/verify.ts` reproduces the draws from the published file.

### B-09 · Moon Mission + blocks ticker 🟡
- **Depends** B-08 · **Read** 02 §11–§12, 03 §6–§7
- **Paths** `apps/worker/src/moon/`, `apps/api/src/{moon,blocks,public}/`
- **Done when** checkpoints trigger the badge queue, the public endpoints are cached for 30 s, and the ticker comes from Redis.

### B-10 · Chain indexer + monitor 🟡
- **Depends** C-07 · **Read** 04 §2 (finality), §8, 06 §4
- **Paths** `apps/worker/src/indexer/`, `apps/worker/src/monitor/`
- **Done when** the cursor resumes after a restart, a reorg-safe 5-confirmation finality works, every event from 05 is decoded, and the alert rules are tested.

### B-11 · Coach Bark service 🟠 COMPLEX
- **Depends** B-06 · **Read** 08 (all) and the current official Anthropic TypeScript SDK docs
- **Paths** `apps/api/src/coach/`, `apps/worker/src/coach/weekly.ts`, `apps/api/src/coach/evals/`
- **Done when**
  - The SSE chat streams.
  - The cache hit shows in `usage`.
  - The structured routes validate.
  - The safety pre- and post-checks are tested.
  - The spend cap works.
  - The eval set is ≥ 95% (safety at 100%).

### B-12 · Walk Bets backend 🟡
- **Depends** B-08, B-10 · **Read** 03 §11, 05 §2.5, 06 §3–§4
- **Paths** `apps/worker/src/bets/`, `apps/api/src/bets/`, `scripts/create-challenge.ts`
- **Done when** progress comes only from verified days, the winners Merkle tree builds, and the post → finalize flow is tested on anvil.

### B-13 · Live, cheers, pack walks 🟡
- **Depends** B-10 · **Read** 04 §5F, 06 §3 (live, pack-walks), 08 §6.2, 07 R10
- **Paths** `apps/api/src/{live,packs}/`
- **Done when**
  - SSE fan-out works (Redis pub/sub), free-cheer limits apply, and the tip-message hash is checked.
  - The moderation filter is tested.
  - Pack QR sign/verify and expiry work.

### B-14 · Genesis vouchers, metadata, Passport, mints 🟡
- **Depends** B-08, C-03, C-04, A-01 · **Read** 02 §10 §19 §20 (Passport), 05 §2.3–§2.4, 10 §8
- **Paths** `packages/shared/src/genesis/`, `apps/api/src/{genesis,nft,public}/`, jobs `pup-sync`, `badge-mint`, `voucher-expiry`
- **Do**
  - Season pools (02 §19 table) and the deck-draw rarity assignment.
  - EIP-712 voucher signing (KMS-ready interface), gasless claim, and the dynamic metadata and SVG for every kind.
  - The Pup Passport endpoint.
- **Done when** a simulation of 1,000 mints matches the matrix exactly, vouchers verify in a Foundry fork test, and the metadata validates.

### B-15 · Notifications 🟢
- **Depends** B-06 · **Read** 02 §13
- **Paths** `apps/worker/src/notify/`
- **Done when** quiet hours, the daily cap and the priority order are tested, and the Expo push receipts are handled.

### B-16 · Privacy jobs 🟢
- **Depends** B-02 · **Read** 09 §6
- **Paths** `apps/worker/src/privacy/`, `apps/api/src/me/`
- **Done when** the purge, export (JSON zip) and soft→hard delete are tested.

### B-17 · Den: inventory, avatar, sink quotes 🟡
- **Depends** B-06, B-10, A-01 · **Read** 02 §15–§16, 03 §10, 05 §2.7, 06 §3 (den, inventory, sink)
- **Paths** `apps/api/src/{den,avatar,inventory,sink}/`, `apps/worker/src/sink/`
- **Done when**
  - The unlock track grants exactly one item per level, and duplicates turn into shards.
  - Equip checks use `owner`/`userOf`.
  - A `Spent` event credits only a matching quote.

### B-18 · Loot boxes, Genesis Draw, Forge 🟠 COMPLEX
- **Depends** B-17, B-14, B-08 · **Read** 02 §17–§19, 03 §6 (commit-reveal), 07 §9
- **Paths** `apps/worker/src/loot/`, `apps/api/src/{loot,forge}/`, `packages/shared/src/loot/verify.ts`
- **Done when**
  - Statistical tests (1M rolls) match the odds tables within tolerance.
  - The pity timers work.
  - Rolls can be re-verified after the reveal.
  - The Genesis Draw issues exactly `drawsToday` tickets.
  - The Forge consumes items only after the burn is credited.

### B-19 · Games backend 🟡
- **Depends** G-01, B-06 · **Read** 02 §20, 07 §9, 06 §3 (games, derby)
- **Paths** `apps/api/src/games/`, `apps/worker/src/{games,derby}/`
- **Done when**
  - Re-simulation accepts honest runs and rejects tampered ones (fixtures).
  - The ticket economy, daily caps and Games-pool shares are tested.
  - The Derby heat simulation is deterministic.

### B-20 · Market and rental indexing 🟡
- **Depends** B-10, C-09, C-10 · **Read** 05 §2.8–§2.9, 06 §1 (market tables) §3 (market)
- **Paths** `apps/worker/src/indexer/market.ts`, `apps/api/src/market/`
- **Done when** listings, sales, swaps and rentals are mirrored correctly, stale listings are hidden, and `user_address/user_expires` stay in sync.

## Phase 2b · Collect & Play foundations

### A-01 · Items, renderers and Genesis traits 🟡
- **Depends** P0-04 · **Read** 02 §15 §16 §19, 10 §8, `prototype/index.html` (`pupSVG`)
- **Paths** `packages/shared/src/{items,avatar,relic,pup,genesis/traits}/`
- **Do**
  - Write the 118-item catalog, the 99-step unlock track and the 6 Collections.
  - Build the Walker and Relic renderers in the Pup style, with a wheelchair base.
  - Write a trait generator that produces 930 unique combinations, plus 70 slots reserved for hand-drawn pieces.
- **Done when**
  - Catalog counts match 02 §16 exactly.
  - There are no duplicate trait combos.
  - SVG snapshot tests pass.

### G-01 · Games scaffold 🟢
- **Depends** P0-01 · **Read** 04 §3 D17, 02 §20 (architecture)
- **Paths** `packages/games-core/`, `apps/games/`
- **Do** Set up a fixed-timestep loop, a seeded RNG (shared with `blocks/`), and an input-log format. Add Vite + Phaser 3, plus a postMessage bridge for WebView and iframe.
- **Done when** a demo scene runs in the browser, and the same seed + inputs give the same state in Node.

### G-02 · Fetch Frenzy 🟡
- **Depends** G-01, A-01 · **Read** 02 §20 (Fetch Frenzy), 10 §5 (Fetch Frenzy)
- **Paths** `packages/games-core/src/frenzy/`, `apps/games/src/frenzy/`
- **Done when**
  - The engine is pure and deterministic, with property tests.
  - The renderer uses the Walker, Pup and Relic SVGs.
  - Genesis perks apply.
  - A run takes about 90 s.

### G-03 · Doge Derby 🟡
- **Depends** G-01, A-01 · **Read** 02 §20 (Doge Derby)
- **Paths** `packages/games-core/src/derby/`, `apps/games/src/derby/`
- **Done when** the speed formula is exact, the replay always matches the final order, and cheer events are shown.

## Phase 3 · Mobile (`apps/mobile`)

### M-01 · App scaffold 🟢
- **Depends** P0-05 · **Read** CONTRIBUTING.md stack, 04 §6, 10 §2 §4
- **Paths** `app.config.ts`, `eas.json`, `app/(tabs)/*`, `src/api/client.ts`, `src/theme/`
- **Do** Set up Expo Router tabs per 10 §4, NativeWind with the tokens, the fonts, the permission usage strings, a typed API client with refresh, and SecureStore.
- **Done when** a dev build runs on an iOS simulator and an Android emulator.

### M-02 · UI kit 🟡
- **Depends** M-01 · **Read** 10 §2–§3, the prototype CSS
- **Paths** `src/ui/*`
- **Do** StickerCard, PopButton, Chip, ProgressRing, XPBar, Sheet, Toast, Confetti, WowBurst, haptics, and PupView (with the shared renderer).
- **Done when** the component tests pass and Reduce Motion is respected.

### M-03 · Health data + background sync 🟠 COMPLEX
- **Depends** M-01, B-04 · **Read** 07 §2, 04 §5A, 10 §5 (onboarding permissions)
- **Paths** `src/health/{ios.ts,android.ts,buckets.ts}`, `src/sync/`
- **Do** HealthKit and Health Connect reads with the manual-entry and source filters, max-per-minute bucketing, a cursor, and an `expo-background-task` sync.
- **Done when** the bucketing unit tests pass and a manual test on a real device is documented.

### M-04 · Attestation + auth 🟠 COMPLEX
- **Depends** M-01, B-03 · **Read** 06 §2, 07 §3
- **Paths** `src/attest/`, `src/auth/`
- **Done when** register, refresh and the assertion header work on real devices, and the dev bypass appears only in dev builds.

### M-05 · Onboarding + Home 🟡
- **Depends** M-02, M-03, M-04 · **Read** 10 §5 (Onboarding, Home), 02 §3–§7, 10 §6
- **Paths** `app/onboarding/*`, `app/(tabs)/index.tsx`
- **Done when** the screens match the prototype, the goal-reached celebration works, and the empty, syncing and review states are covered.

### M-06 · Walk sessions + Go Live 🟠 COMPLEX
- **Depends** M-05, B-13, B-11 · **Read** 10 §5 (Walk), 07 R9, 08 §4 (CuePack), 04 §5F
- **Paths** `app/(tabs)/walk.tsx`, `src/session/*`
- **Do**
  - Use `expo-location` in the foreground and in a background task, and capture the mock flag.
  - Batch the points, compute live stats, and play cues with `expo-speech`.
  - Go Live: poll for cheers, then TTS (background audio mode).
- **Done when** a real-device walk is tested and the battery note is documented.

### M-07 · Moon + Ranks 🟡
- **Depends** M-02, B-07, B-09 · **Read** 10 §5 (Moon, Ranks)
- **Paths** `app/(tabs)/moon.tsx`, `app/(tabs)/ranks.tsx`
- **Done when** the screens match the prototype and the a11y labels are in place.

### M-08 · Companion Pup + Badges 🟡
- **Depends** M-02, B-14, B-17, M-10 · **Read** 10 §5 (Pup, Badges), 02 §10, 05 §2.7
- **Paths** `app/den/pup.tsx`, `app/badges.tsx`
- **Done when** Evolve works through a TreatSink quote (quote → `spend` → indexed → stage up), equipping a Genesis Pup shows its rarity bonus, and the badges grid matches 02 §9.

### M-09 · Coach chat 🟡
- **Depends** M-02, B-11 · **Read** 10 §5 (Coach), 08 §4
- **Paths** `app/coach.tsx`, `src/coach/`
- **Done when** SSE streaming, the quick replies, the goal-proposal confirm card, and the limit and napping states work.

### M-10 · Wallet + on-chain actions 🟠 COMPLEX
- **Depends** M-04, B-08, C-07 · **Read** 04 §4 D11 D14, 06 §2 (SIWE), 05 (ABIs), 09 §4 (wallet)
- **Paths** `src/wallet/`, `app/wallet.tsx`
- **Do** Reown AppKit RN + wagmi with the custom chain, SIWE link, claim, gasless claim, `cheer`/`cheerNative`, and `joinWithPermit`.
- **Done when** each flow works against anvil and Chikyū, and the wrong-network state is handled.

### M-11 · Walk Bets + Packs screens 🟡
- **Depends** M-10, B-12, B-13 · **Read** 10 §5 (Bets, Pack)
- **Paths** `app/bets/*`, `app/pack/*`
- **Done when** join, progress and claim work, and the QR show/scan (expo-camera) works.

### M-12 · Profile & settings 🟢
- **Depends** M-05, B-15, B-16 · **Read** 10 §5 (Profile), 02 §6, 09 §6
- **Paths** `app/profile/*`
- **Done when** push registration, quiet hours, rest/injury mode, export and delete all work.

### M-13 · Recap share card 🟢
- **Depends** M-06 · **Read** 08 §4 (RecapCaption), 10 §3
- **Paths** `src/recap/`
- **Done when** `react-native-view-shot` renders the card and the native share sheet opens.

### M-14 · Den: avatar studio, closet, loot, forge 🟡
- **Depends** M-08, B-17, B-18 · **Read** 10 §4 §5 (Den, Avatar studio, Closet, Loot opening, Forge, Genesis ticket)
- **Paths** `app/(tabs)/den.tsx`, `app/den/*`
- **Done when** the loot opening animation respects Reduce Motion, the odds are reachable from every box, and the Genesis claim and leash countdown work.

### M-15 · Play hub + games 🟡
- **Depends** M-07, G-02, G-03, B-19 · **Read** 10 §5 (Play hub, Fetch Frenzy, Doge Derby)
- **Paths** `app/(tabs)/play.tsx`, `app/games/*`, `src/games/bridge.ts`
- **Done when** the games run in a WebView with the bridge, tickets are consumed only on a validated start, and the Derby replay plays with cheers.

### M-16 · Market screens 🟡
- **Depends** M-10, B-20 · **Read** 10 §5 (Market), 09 §11 (feature flags)
- **Paths** `app/market/*`
- **Done when** buy, sell, trade and rent flows work on anvil, the flags hide trading on iOS by default, and the "Trade on the web" link works.

## Phase 4 · Web (`apps/web`)

### W-01 · Landing + public pages 🟡
- **Depends** B-09, P0-05 · **Read** 10 (all), 01 §4
- **Paths** `app/page.tsx`, `app/u/[handle]`, `app/live/[id]`
- **Done when** the live Moon counter, block feed, top 100 and the spectator page (free cheers plus wallet tips) work, Lighthouse scores ≥ 90, and the CSP is set.

### W-02 · Web dapp 🟡
- **Depends** W-01, C-07, B-08 · **Read** 05 (ABIs), 09 §5
- **Paths** `app/claim`, `app/bets`, `app/pups`
- **Done when** claim, Walk Bets, and the Pup gallery with evolve work, the Playwright tests on anvil pass, and the axe a11y check is clean.

### W-03 · Web market + mint 🟡
- **Depends** W-02, C-09, C-10, B-20 · **Read** 10 §5 (Market), 05 §2.8–§2.9, 02 §19
- **Paths** `app/market/*`, `app/mint`
- **Done when** buy, sell, swap and rent work through wagmi with the expected-price guards, Playwright tests pass on anvil, and the mint page reads live cap and cell counts.

## Phase 5 · QA, security, launch

### Q-01 · E2E suites 🟡
- **Depends** M-05…M-16, W-02, W-03 · **Read** 09 §9
- **Paths** `apps/mobile/.maestro/`, `apps/web/e2e/`, `scripts/e2e-epoch.sh`
- **Done when** the onboarding → sync → walk → epoch → claim flow passes in CI on anvil.

### Q-02 · Load + DAST 🟢
- **Depends** Q-01 · **Read** 09 §9
- **Paths** `tests/k6/`, `.github/workflows/zap.yml`
- **Done when** the k6 thresholds (09 §9) are met against staging and the ZAP baseline shows no high findings.

### S-01 · System security review 🔴 CRITICAL
- **Depends** M3 scope complete · **Read** 07, 08 §6, 09 (all), and the code
- **Paths** `docs/audits/internal-02.md`, fixes
- **Do** Threat-model the whole system as built. Review auth, attestation, the epoch builder, the signers and tx queue, the bets oracle, Genesis vouchers, loot and draw randomness, game re-simulation, the market indexer, the SSE limits, coach safety, and privacy retention.
- **Done when** every high and medium finding is fixed or formally accepted.

### L-01 · Testnet launch kit 🟢
- **Depends** S-01 · **Read** 12 (all)
- **Paths** `docs/runbooks/*`, `docs/legal/DRAFT-*` (marked "needs counsel"), `docs/launch/*`
- **Done when** the 12 §1 checklist is all ticked except the HUMAN items.

### L-02 · Mainnet go/no-go 🔴 CRITICAL
- **Depends** testnet season 1, external audit, legal sign-off · **Read** 12 §2, all the audits
- **Paths** `docs/launch/mainnet-readiness.md`
- **Done when** there is a written GO or NO-GO with evidence for each item in 12 §2.
