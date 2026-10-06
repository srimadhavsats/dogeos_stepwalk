# 04 · Architecture

## 1. System overview
```
┌──────────── Mobile (Expo) ─────────────┐        ┌──────── Web (Next.js) ────────┐
│ HealthKit / Health Connect → minutes   │        │ Landing · live Moon counter   │
│ App Attest / Play Integrity            │        │ Leaderboards · share pages    │
│ GPS sessions · Pack QR · TTS cues      │        │ Claim · Walk Bets · Pup gallery│
│ Reown AppKit (MyDoge/MetaMask/WC)      │        │ wagmi + AppKit                │
└───────────────┬────────────────────────┘        └──────────────┬────────────────┘
                │ HTTPS (JWT) + SSE                               │
        ┌───────▼─────────────────────────────────────────────────▼───────┐
        │ API (Hono)  auth · sync · game · coach(SSE) · live(SSE) · proofs │
        └───────┬───────────────┬──────────────────┬─────────────────────┘
                │               │                  │
         ┌──────▼─────┐  ┌──────▼──────┐   ┌───────▼────────┐   ┌──────────────┐
         │ Postgres 17│  │  Redis 7    │   │ Worker (BullMQ)│──▶│ Anthropic API│
         │ (Drizzle)  │  │ ZSET boards │   │ scoring, epoch,│   └──────────────┘
         └────────────┘  │ rate limits │   │ blocks, leagues│   ┌──────────────┐
                         │ queues      │   │ bets oracle,   │──▶│ R2/IPFS epoch│
                         └─────────────┘   │ indexer, push  │   │ files        │
                                           └───────┬────────┘   └──────────────┘
                                                   │ viem (signer = KMS on mainnet)
                                   ┌───────────────▼────────────────────┐
                                   │ DogeOS Chikyū (EVM zk-rollup)      │
                                   │ TreatToken · RewardsDistributor ·  │
                                   │ GenesisNFT · BadgeSBT · WalkBetPool│
                                   │ CheerRouter · TreatSink · MuchMarket│
                                   │ RentalHouse · Timelock             │
                                   └────────────────────────────────────┘
```

## 2. Chain facts (single source → `packages/shared/src/chains.ts`)
Researched on 2026-10-05. Rows marked **VERIFY** must be confirmed against **docs.dogeos.com** in task P0-01 before anything is deployed.

| Field | Value | Status |
|---|---|---|
| Name | DogeOS Chikyū Testnet | ✅ |
| Chain ID | `6281971` (`0x5fdaf3`) | ✅ (chainlist.org) |
| Native / gas token | DOGE, 18 decimals | ✅ (reported) |
| RPC (primary) | `https://rpc.testnet.dogeos.com` | VERIFY |
| RPC (fallback) | `https://dogeos-testnet.drpc.org` (dRPC public) | VERIFY |
| Explorer | `https://blockscout.testnet.dogeos.com` (chainlist). One outlet also reports `https://dogeos-testnet.l2scan.co` | VERIFY which is official |
| Block time | ~3 s | reported |
| Faucet | Official DogeOS faucet, 1 claim per 24h | URL: VERIFY |
| Security model | Permissioned sequencer + TEE + validators. Proof verification by Dogecoin miners is a future upgrade | ✅ (news) |
| Mainnet | Not live, no date announced | ✅ |

**Known testnet issue:** [DogeOS69/dogeos-rollup-node#63](https://github.com/DogeOS69/dogeos-rollup-node/issues/63) reports that the sequencer debits far more DOGE than receipts' `effectiveGasPrice` implies (one 6-contract deploy burned about 41 DOGE). It was still open on 2026-10-05.
→ Deploy scripts must log the **balance before and after** each deploy rather than trusting receipts, and must abort if the balance is below a configurable floor.

**Finality policy:** the indexer treats events as final after **5 L2 confirmations**. Cheer UX may show `pending` at 1 confirmation.

**P0-01 also probes** (record the results in DECISIONS-LOG):
- Opcodes: PUSH0 (shanghai), TLOAD/TSTORE and MCOPY (cancun). This sets `evm_version`. The default is `paris` until proven otherwise.
- Precompiles: ecrecover, sha256, modexp, bn256, and P256VERIFY at `0x100` (RIP-7212).
- Whether these exist: EIP-7702 tx type 4, ERC-4337 EntryPoint v0.7/v0.8, Safe singleton factory, Multicall3 (`0xcA11bde05977b3631167028862bE2a173976CA11`), CREATE2 deployer (`0x4e59b44847b379578588920cA78FbF26c0B4956C`).

## 3. Repo layout
```
muchwalk/  (this folder)
├─ apps/
│  ├─ mobile/      Expo Router app  (@muchwalk/mobile)
│  ├─ web/         Next.js App Router (@muchwalk/web)
│  ├─ api/         Hono HTTP + SSE  (@muchwalk/api)
│  ├─ worker/      BullMQ processors (@muchwalk/worker)
│  └─ games/       Vite + Phaser 3 renderers for Fetch Frenzy and Doge Derby (@muchwalk/games)
├─ packages/
│  ├─ shared/      chains.ts, game/, econ/, schemas/ (zod), merkle/, blocks/verify.ts, items/, genesis/, pup|avatar|relic renderers
│  ├─ games-core/  deterministic game engines (fixed timestep, seeded RNG), used by the client AND server re-sim
│  ├─ db/          Drizzle schema + migrations + seed (@muchwalk/db)
│  ├─ contracts/   Foundry; `pnpm build` exports abi/*.ts + addresses/<chainId>.json
│  ├─ ui-tokens/   colors, radii, shadows, fonts (from 10-UI-UX §2)
│  └─ config/      tsconfig bases, biome.json
├─ docs/  prototype/  .github/workflows/
└─ turbo.json  pnpm-workspace.yaml  package.json  .env.example
```

## 4. Locked decisions
| # | Decision | Why |
|---|---|---|
| D1 | pnpm 10 + Turborepo monorepo, Node 24 LTS, TS strict, Biome | One toolchain. pnpm 10 blocks dependency lifecycle scripts by default |
| D2 | **Game state off-chain; value on-chain** (TREAT, Pups, badges, bets, tips) | Gas, iteration speed, privacy |
| D3 | **Cumulative Merkle claims + on-chain daily mint cap + guardian veto window** | A stolen poster key can lose at most one epoch, and that epoch can still be vetoed |
| D4 | Contracts are **non-upgradeable** in v1. Admin = `TimelockController` (testnet 1h, mainnet 48h) owned by a Safe (mainnet 2-of-3) | Smaller attack surface. Migration works through cumulative claims |
| D5 | No VRF dependency: commit-reveal + L2 block entropy (03 §6) | Oracle availability on DogeOS is unknown. Revisit if Chainlink VRF launches there |
| D6 | **Walk-first accounts:** a device-bound account key is created on first launch, and a wallet is linked later via SIWE (EIP-4361) | No wallet friction on day 1 |
| D7 | Steps come from the **OS health stores**, not the raw accelerometer | Hardware-backed counters are harder to fake, and battery-friendly |
| D8 | Hono + `@hono/zod-openapi` | TS-first, small, and generates OpenAPI from zod |
| D9 | Postgres + Redis with our own event indexer (block cursor in DB), no subgraph | No dependency on indexer support for a brand-new chain |
| D10 | Expo **dev builds** (EAS), not Expo Go | Health and attestation need native modules |
| D11 | External wallets via **Reown AppKit**. Embedded wallets (Privy) come in Phase 2, after checking that chain 6281971 is supported | Doge holders already use MyDoge or MetaMask |
| D12 | The Anthropic API is called **server-side only** | Keys never ship in apps |
| D13 | **SSE** for live features (coach stream, live runs, block ticker) | Simpler than WebSockets and proxy-friendly |
| D14 | Gasless UX via **our relayer** (permissionless `claim`, role-gated mints). 4337/7702 only if P0-01 finds support | Works on day 1 whatever AA support exists |
| D15 | **Only 1,000 NFTs exist (GenesisNFT).** Starter Pups, Walkers and items are off-chain | Scarcity for collectors, free-to-play for everyone, low gas |
| D16 | Lending = **ERC-4907 user rights** with transfers blocked while rented. No collateralised loans | No custody, no default risk, simple to audit |
| D17 | Games are **web games (Phaser) in a WebView/iframe** with a separate deterministic engine | One game build for mobile and web; scores can be verified on the server |
| D18 | Market is **our own escrow-less contract**, not a third-party protocol | Marketplace protocols may not be deployed on a brand-new chain; our scope is small (fixed price + swaps) |

## 5. Key flows
**A. Step sync**
1. The app reads HealthKit / Health Connect for the window since the last cursor (max 72h back).
2. It builds **minute buckets** `{minuteTs, su, sourceKind, recordingMethod}`.
3. It sends `POST /v1/activity/sync` with an attestation assertion over `sha256(body)`.
4. The API verifies the assertion, validates with zod, dedupes, and upserts `activity_minutes`, then enqueues `score-user-day`.
5. The worker runs anti-cheat (07) and updates `user_days`, XP, quests, streak and the Redis boards.
6. Sync triggers: app foreground, session end, and `expo-background-task` (the OS decides how often, roughly every 15–60 min).

**B. Daily epoch (worker cron 06:30 UTC)**
1. Freeze day e.
2. Compute WP and pro-rata W; run the block draws; compute quest and league payouts (Monday); apply caps.
3. Merge the results into per-address cumulative totals.
4. Build the Merkle tree and write `tree.json`, `blocks.json` and `metadata.json` to R2 (+ IPFS pin).
5. Call `postEpoch(e, root, mintAmount, bonusUsed, metadataHash, seedCommit[e+1])`.
6. Store the proofs. The root becomes claimable after `claimDelay`.

**C. Claim:** `GET /v1/rewards/proof` → the user either signs `claim()` themselves, or taps "Gasless claim", which queues a relayer batch.

**D. Pups:**
- Starter mint by the relayer (MINTER_ROLE) after the account is verified and has a wallet.
- A daily `syncLevels` batch (SYNCER_ROLE) updates only Pups whose level changed.
- Evolve is a user transaction that burns TREAT.

**E. Walk Bets:**
1. A curator creates the challenge.
2. Users `joinWithPermit`.
3. Progress is tracked off-chain.
4. The oracle posts a winners root no earlier than end + 6h.
5. 24h dispute window, then claims.

**F. Cheer Lane:**
1. `POST /v1/live/start`.
2. Spectators subscribe with `GET /v1/live/:id/stream` (SSE).
3. Free cheers go through `POST /v1/live/:id/cheer`. Paid tips are `CheerRouter.cheer*` transactions, which the indexer picks up at 1 confirmation (pending) and then 5 (final).
4. Each tip passes moderation, then reaches the runner's SSE stream, and the app speaks it with TTS.

**G. Coach:** `POST /v1/coach/chat` (SSE) → context builder (aggregates only, no PII) → Anthropic stream → client.

## 6. Environments & config
| Env | Chain | Notes |
|---|---|---|
| `local` | anvil (31337) | `pnpm dev` spins up docker-compose (pg, redis) and anvil, with contracts auto-deployed |
| `testnet` | Chikyū 6281971 | Public beta |
| `mainnet` | DogeOS mainnet (TBD) | Only after the 12-LAUNCH checklist |

`.env.example` (API/worker): `NODE_ENV, PORT, DATABASE_URL, REDIS_URL, CHAIN_ID, RPC_URL, RPC_URL_FALLBACK, POSTER_KEY|POSTER_KMS_KEY_ID, RELAYER_KEY|RELAYER_KMS_KEY_ID, ORACLE_KEY|ORACLE_KMS_KEY_ID, JWT_PRIVATE_KEY (Ed25519 PEM), ANTHROPIC_API_KEY, R2_ACCOUNT_ID, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY, R2_BUCKET, PUBLIC_FILES_BASE_URL, APPLE_TEAM_ID, APPLE_BUNDLE_ID, PLAY_INTEGRITY_SA_JSON, EXPO_ACCESS_TOKEN, SENTRY_DSN, GENESIS_TS`.
Mobile (`EXPO_PUBLIC_*` only, never secrets): `EXPO_PUBLIC_API_URL, EXPO_PUBLIC_CHAIN_ID, EXPO_PUBLIC_REOWN_PROJECT_ID`.

## 7. Hosting (testnet)
- API and worker run as Docker images on Railway (or Fly.io).
- Postgres: Neon or Railway. Redis: Railway or Upstash.
- Cloudflare R2 holds public epoch files, behind a custom domain.
- Web runs on Vercel. Mobile ships through EAS Build to TestFlight and Play Internal testing.
- Secrets live in the platform secret store (testnet). On mainnet, signer keys are **AWS KMS secp256k1** and are never exported.

## 8. Observability
- pino JSON logs with request IDs, redacting `authorization`, `cookie`, `*key*`, `*secret*`, emails and wallets (hashed).
- Sentry on API, worker, mobile and web. OpenTelemetry traces for the API.
- A **chain monitor job** (worker) alerts on: role changes, pauses, `postEpoch` totals above 95% of cap, the relayer balance dropping below its floor, and unexpected large transfers out of the distributor or the bet pool.
