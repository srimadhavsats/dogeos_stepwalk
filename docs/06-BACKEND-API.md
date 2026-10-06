# 06 · Backend: DB schema, API, jobs

> API: `apps/api` (Hono + `@hono/zod-openapi`, OpenAPI served at `/v1/openapi.json`). Worker: `apps/worker` (BullMQ). Schema: `packages/db` (Drizzle, PostgreSQL 17).
> Every request and response schema lives in `packages/shared/src/schemas/` and is shared with the apps.

## 1. Database tables (Drizzle)
Conventions:
- `id uuid default gen_random_uuid()` and `created_at timestamptz default now()`.
- Token amounts are `numeric(78,0)`, mapped to `bigint` in TS.
- Addresses are stored lowercase.

| Table | Key columns |
|---|---|
| `accounts` | id, handle (citext unique, `^[a-z0-9_.]{3,20}$`), tz, height_cm?, roll_mode, level, xp (bigint), goal_mode (`adaptive`/`pinned`), goal_pinned?, streak_days, streak_best, shields, trust_bps (default 5000), status (`active`/`review`/`banned`/`deleted`), referral_code, referred_by?, age_confirmed_at, consent_health_at, deleted_at? |
| `devices` | id, account_id, platform (`ios`/`android`), attest_key_id, attest_public_key (bytea), attest_counter (bigint), integrity_verdict (jsonb), push_token?, last_seen_at, revoked_at? |
| `refresh_tokens` | id, account_id, device_id, token_hash (sha256), family_id, expires_at, revoked_at?, replaced_by? |
| `wallets` | account_id (unique), address (unique), linked_at |
| `siwe_nonces` | nonce (pk), account_id?, expires_at, used_at? |
| `activity_minutes` | **pk (account_id, minute_ts)**, su, kind (`step`/`push`), source (`phone`/`watch`/`other`), recording (`auto`/`active`), flagged, received_at. Monthly range partitions |
| `sessions` | id, account_id, type (`walk`/`run`/`roll`/`pack`), started_at, ended_at?, distance_m, su, status (`active`/`completed`/`rejected`), flags text[], h3_cells text[], pack_walk_id?, live |
| `session_points` | session_id, ts, lat, lng, acc_m, speed_mps, is_mock. **Purged after 30 days** |
| `packs`, `pack_members` | id, name, owner_id, member_count / pack_id, account_id, role |
| `pack_walks`, `pack_walk_members` | id, leader_session_id, qr_nonce, expires_at / pack_walk_id, account_id, session_id, overlap_bps, verified |
| `user_days` | **pk (account_id, local_date)**, su_raw, su_verified, goal, goal_met, xp_earned, quests jsonb, chest_opened, rest_day, flags text[] |
| `utc_days` | **pk (account_id, epoch_id)**, su_verified, pack_su, pack_size, trust_bps, wp (bigint), quest_points |
| `block_hashes` | **pk (epoch_id, block_k, account_id)**, su, hashes |
| `walk_blocks` | **pk (epoch_id, block_k)**, global_no, total_hashes, finder_account_id?, reward_wei, status (`open`/`final`/`orphaned`) |
| `epochs` | epoch_id (pk), status (`building`/`posted`/`active`/`vetoed`), root, mint_wei, bonus_wei, metadata_hash, files_url, tx_hash, seed_commit, secret_enc, season_meters, posted_at, active_at |
| `allocations` | **pk (epoch_id, account_id)**, walk_wei, blocks_wei, quests_wei, league_wei, total_wei |
| `pending_rewards` | account_id (pk), pending_wei, since |
| `cumulative` | address (pk), cumulative_wei, last_epoch |
| `proofs` | **pk (epoch_id, address)**, cumulative_wei, proof text[]. Keep the latest 3 epochs |
| `claims` | tx_hash, log_index, address, amount_wei, cumulative_wei, epoch_id, block_number (from indexer) |
| `xp_events` | id, account_id, local_date, source, amount, ref. Audit trail; XP is always derivable from it |
| `badges_earned` | account_id, badge_id, earned_at, mint_tx? |
| `league_cohorts`, `league_members` | id, iso_week, tier / cohort_id, account_id, week_xp, rank, outcome, reward_wei |
| `seasons`, `season_contrib` | id, name, started_at, ended_at?, meters_total, checkpoints jsonb / season_id, account_id, meters |
| `companions` | account_id (pk), starter_coat, starter_name, starter_xp, starter_level, starter_stage, equipped_genesis_pup?, equipped_genesis_walker?, equipped_relics int[] (≤ 2) |
| `genesis_tokens` | token_id (pk), kind, rarity, channel, seed, traits jsonb, owner_address, user_address?, user_expires?, locked_until?, pup_xp, pup_level, pup_stage, level_onchain, needs_sync. Mirrors the chain via the indexer |
| `genesis_vouchers` | voucher_id (pk), account_id, channel, kind, rarity, seed, lock_days, price_wei, expires_at, status (`issued`/`minted`/`expired`), token_id? |
| `genesis_pool` | (season, channel) pk, allocated, issued, minted. Exact numbers from 02 §19 |
| `avatars` | account_id (pk), base (`standing`/`wheelchair`), skin_tone, slots jsonb |
| `item_catalog` (seeded from shared) · `inventory` | id, owner, slot, rarity, sources, set_id / (account_id, item_id) pk, acquired_at, source |
| `shards` · `loot_boxes` | account_id, balance / id, account_id, type, earned_at, opened_at?, rolls jsonb, expires_at |
| `pity` | account_id (pk), since_rare, since_super_rare |
| `genesis_draw_entries` | (epoch_id, account_id) pk, entries |
| `sink_quotes` | id (= ref), account_id, purpose, amount_wei, payload jsonb, expires_at, credited_tx? |
| `game_tickets` · `game_runs` | account_id, balance / id, account_id, game, seed, run_token, inputs bytea, score, validated, xp, shards, created_at |
| `derby_entries` · `derby_heats` | (week, account_id) pk, pup_ref, tier / id, week, tier, entrants jsonb, result jsonb, luck_seed |
| `market_listings` · `market_sales` · `swaps` · `rentals` | mirrors of the MuchMarket and RentalHouse events (indexer) |
| `bets`, `bet_participants` | id (on-chain id), stake_wei, start_at, end_at, rules jsonb, rules_hash, status, winners_root? / bet_id, account_id, address, progress jsonb, result (`pending`/`won`/`lost`) |
| `live_sessions` | id, session_id, account_id, visibility (`friends`/`public`), last_progress jsonb, ended_at? |
| `cheers` | id, live_id, from_account?, to_account, kind (`free`/`tip`), emoji?, message?, amount_wei?, token?, tx_hash?, status (`pending`/`final`/`rejected`), spoken_at? |
| `friendships` | a_id, b_id, status, created_at (store with a_id < b_id) |
| `coach_threads`, `coach_messages`, `coach_usage` | … / role, content, tokens_in, tokens_out / (account_id, date) count. **Messages purged after 90 days** |
| `notifications` | id, account_id, type, payload, sent_at |
| `chain_cursor` | name (pk), last_block |
| `audit_log` | id, actor, action, target, meta jsonb, at. Admin and signer actions only |

## 2. Auth model
1. **Register** (first launch):
   - The app gets a device attestation: an App Attest key + attestation on iOS, a Play Integrity token on Android.
   - It calls `POST /v1/auth/register`. The server verifies the attestation and creates the account + device.
   - The server returns an **access JWT (EdDSA, 15 min)** and an **opaque refresh token (30 days, rotating)**. The app stores both in `expo-secure-store`.
2. **Refresh** rotates the token on every use. Presenting a revoked token **revokes the whole family**, which is how reuse is detected.
3. **Wallet link (SIWE / EIP-4361):**
   - `GET /siwe/nonce` returns a nonce valid for 10 minutes.
   - The app signs a message with `domain = muchwalk.app`, `uri = https://muchwalk.app`, `chainId = 6281971`, `nonce`, `issuedAt` and `expirationTime ≤ 10 min`.
   - The server verifies it with viem `verifySiweMessage`, which also handles ERC-1271/6492 smart wallets. A nonce can be used once.
4. **Recovery on a new device:** `POST /v1/auth/siwe/login` plus a new device attestation.
5. **Sensitive endpoints** (`activity/sync`, `sessions/*/end`, `pups/starter`, `rewards/claim-relay`) also need a fresh **App Attest assertion / Play Integrity token** bound to `sha256(requestBody)`. See 07 §3.

## 3. Endpoints (`/v1`)
| Method & path | Auth | Purpose |
|---|---|---|
| POST `/auth/register` | attest | Create account + device. Body: `{platform, attestation, tz, consent:{health, terms, ageConfirmed}}` |
| POST `/auth/refresh` · `/auth/logout` | refresh | Rotate / revoke |
| GET `/auth/siwe/nonce` · POST `/auth/siwe/link` · POST `/auth/siwe/login` | jwt / attest | Wallet link / recover |
| GET `/me` · PATCH `/me` · DELETE `/me` · GET `/me/export` | jwt | Profile, GDPR erase (soft now, hard after 30 days), data export |
| POST `/activity/sync` | jwt+assert | ≤ 4,320 minutes (72h), body ≤ 256 KB. Returns `{accepted, rejected, today}` |
| POST `/sessions/start` · `/sessions/:id/points` · `/sessions/:id/end` | jwt (+assert on end) | GPS sessions. Points come in batches of ≤ 120 every 30–60 s |
| GET `/today` | jwt | Ring, goal, quests, streak, XP and level, Pup mood, estimated pending treats, current block |
| GET `/history?from&to` | jwt | Daily history |
| GET `/quests/today` · POST `/quests/chest/open` | jwt | Quests + chest |
| POST `/streak/rest-day` · `/streak/injury` | jwt | Healthy-design tools |
| GET `/leagues/current` | jwt | Cohort table with promote/demote zones |
| GET `/leaderboards/:scope?period=` | jwt | `friends`, `global`, `pack`, `city` |
| GET `/badges` · GET `/moon/season` · GET `/blocks/recent` · GET `/blocks/:globalNo` | jwt | Trophy case, Moon, block feed |
| friends: GET/POST/DELETE `/friends…` · packs: `/packs…` | jwt | Social graph |
| POST `/pack-walks` · POST `/pack-walks/join` | jwt | QR payload = `{pwId, nonce, exp}` signed by the server (Ed25519), valid 10 min |
| POST `/live/start` · `/live/:id/progress` · `/live/:id/end` | jwt | Runner side. Progress every 15 s |
| GET `/live/:id/stream` (SSE) | jwt | Spectators: `progress` and `cheer` events |
| GET `/live/:id/cheers?since=` | jwt | Runner background polling |
| POST `/live/:id/cheer` · `/live/:id/tip-message` | jwt | Free emoji cheer (1 per 10 s per spectator, 30 per session) / tip plaintext (`keccak256` must match the on-chain hash) |
| GET `/rewards/summary` · GET `/rewards/proof` · POST `/rewards/claim-relay` | jwt (+assert) | Claiming. Relay limited to 1 per day per account |
| GET `/den` · POST `/den/equip` · PATCH `/avatar` · GET `/inventory` | jwt | Companion, Walker, items and equipped Genesis tokens. Equipping a Genesis token checks `owner` or an active `user` on-chain |
| GET `/loot` · POST `/loot/:id/open` · GET `/loot/odds` | jwt | Verifiable rolls (02 §17). The response includes `rollProof` (inputs to recompute after the reveal) |
| POST `/forge/item` · `/forge/box` · `/forge/genesis` | jwt (+assert on genesis) | Genesis Forge returns a `sink_quote` for 2,000 TREAT. Items are consumed only when the `Spent` event is indexed |
| GET `/genesis/tickets` · POST `/genesis/tickets/:id/claim` | jwt (+assert) | Signed `MintVoucher`. Gasless claim through the relayer, or the user submits it |
| POST `/sink/quote` | jwt | `{purpose, ref}` → `{amount, expiresAt}` for every TreatSink purpose |
| GET `/games/tickets` · POST `/games/:game/start` · POST `/games/:game/finish` | jwt | `start` → `{seed, runToken}`. `finish` takes the inputs log, which the server re-simulates |
| GET `/games/leaderboard?game&period` · POST `/derby/enter` · GET `/derby/:week` | jwt | Derby replay data |
| GET `/market/listings` · `/market/swaps` · `/market/rentals` · `/market/history/:tokenId` | none | Read-only views from the indexer. Writes happen on-chain |
| GET `/public/passport/:tokenId` | none | The cross-game Pup Passport (02 §20) |
| GET `/bets` · GET `/bets/:id` · POST `/bets/:id/joined` | jwt | `joined` is only a hint. The indexer is the source of truth |
| POST `/coach/chat` (SSE) · GET `/coach/threads/:id` · POST `/coach/cue-pack` · GET `/coach/plan/today` | jwt | See 08 |
| GET `/public/moon` · `/public/blocks/recent` · `/public/leaderboard/global` | none | Cached 30 s. Shows handles only |
| GET `/nft/pup/:id` · `/nft/pup/:id.svg` · `/nft/badges/:id.json` | none | NFT metadata |
| GET `/healthz` · `/readyz` | none | Probes |

Error envelope: `{ error: { code, message } }`. Codes: `VALIDATION`, `UNAUTHENTICATED`, `FORBIDDEN`, `NOT_FOUND`, `RATE_LIMITED`, `ATTESTATION_FAILED`, `CONFLICT`, `UNDER_REVIEW`, `INTERNAL`.
Rate limits (Redis sliding window): default 60/min per account; register 5/hour per IP; sync 30/hour; coach per 08 §5.

## 4. Jobs (`apps/worker`)
| Job | Schedule | Notes |
|---|---|---|
| `score-user-day` | on sync, debounced 60 s per account | Anti-cheat (07) → `user_days`, `utc_days`, `block_hashes`, XP, quests, boards |
| `finalize-local-day` | hourly | For accounts whose local day just ended: streak, shields, goal recalculation, badges |
| `blocks-ticker` | every 1 min | Live (non-final) totals for the ticker, cached in Redis |
| `epoch-build` | 06:30 UTC | 03 §3–6 → allocations → Merkle → R2 files. **Idempotent by epochId** |
| `epoch-post` | after build | Check chain `lastEpoch` first, then send the tx. Single-concurrency queue per signer key, to avoid nonce races |
| `root-activate` | every 5 min | Detect activation and push "treats ready" |
| `relayer-claims` | every 30 min | `claimMany` in batches of ≤ 100, with fresh proofs |
| `pup-sync` · `badge-mint` | 07:00 UTC | `syncPups` (≤ 200) / `airdrop` (≤ 300) |
| `genesis-draw` | inside `epoch-build` | 02 §17. Issues vouchers and decrements `genesis_pool` |
| `voucher-expiry` · `quote-expiry` | hourly | Unclaimed tickets go back to the pool after 30 days. Expired quotes are released |
| `games-weekly` · `derby-run` | Mon 00:10 UTC · Sun 18:00 UTC | Games pool ranks (03 §5) / heat simulation + Box rewards |
| `league-snapshot` · `league-rollover` | every 5 min · Mon 00:05 UTC | Ranks cache / cohorts, outcomes and rewards |
| `bets-progress` · `bets-results` · `bets-finalize` | hourly · end+6h · after the dispute window | Oracle uses verified `user_days` only |
| `indexer` | every 5 s | `getLogs` from the cursor. Final at 5 confirmations |
| `notifications` | every 5 min | Rules in 02 §13 (Expo Push API) |
| `moon-aggregate` | every 10 min | Season meters and checkpoints |
| `coach-weekly` | Mon 07:00 UTC | Anthropic **Message Batches** (50% cheaper) |
| `privacy-purge` · `pending-expiry` | daily | Retention rules (09 §6) / 180-day pending expiry |
| `chain-monitor` | every 1 min | Alerts listed in 04 §8 |

## 5. Performance targets (testnet)
- p95 API latency < 200 ms, excluding coach and SSE. Sync handles 50k minutes per minute.
- The epoch build finishes in under 10 minutes for 100k accounts.
- Leaderboards use Redis ZSET keys `lb:{scope}:{period}:{id}`, rebuilt from Postgres on a cache miss.
