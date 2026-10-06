# Contributing to MuchWalk

MuchWalk is a move-to-earn dapp on **DogeOS**, the EVM zk-rollup for Dogecoin. It launches first on the **Chikyū testnet** (chain ID `6281971`).

Users walk, run or roll and earn `$TREAT`. Each user raises a companion Pup and a Walker avatar, collects items from loot boxes, and trades or rents Genesis NFTs. Coach Bark, the AI coach, cheers them on.

The specs in `docs/` are **final**. Build exactly what they say.

## Hard rules
1. **Never commit secrets.** That means no `.env` files, private keys, keystores or API keys. Every new variable goes into `.env.example` with a placeholder value.
2. **Comments speak as the team** ("we cap cadence here because…"). Only add a comment when the *why* isn't obvious from the code.
3. **Don't redesign.** If a spec looks wrong, follow it anyway and record the concern in `docs/OPEN-QUESTIONS.md`. The one exception: stop if following it would lose funds or leak user data.
4. **Money and security code must match the spec exactly.** This covers contracts, reward math, signers, anti-cheat, loot rolls and the marketplace. Don't round differently, reorder checks or "simplify".
5. **Chain facts live in one place:** `packages/shared/src/chains.ts`, generated from `docs/04-ARCHITECTURE.md` §2. Never hardcode an RPC URL, an address or the chain ID anywhere else.

## Task workflow
1. In `docs/PROGRESS.md`, pick the first `TODO` task whose dependencies are all `DONE`.
2. Read that task's card in `docs/11-BUILD-PLAN.md`. Then read **only** the doc sections the card lists.
3. Implement the task inside the paths the card names.
4. Run the checks below until they pass. Never skip or weaken a test to get there.
5. Mark the task `DONE` in `docs/PROGRESS.md`. If you filled a gap in a spec, log it in `docs/DECISIONS-LOG.md`.
6. Commit with a Conventional Commit message, e.g. `feat(contracts): add RewardsDistributor cumulative claims`.

## Tech stack (locked, see `docs/04-ARCHITECTURE.md`)
| Area | Choice |
|---|---|
| Monorepo | pnpm 10 workspaces + Turborepo · Node 24 LTS · TypeScript strict · Biome |
| Contracts | Foundry + OpenZeppelin Contracts v5 · Solidity pinned in `foundry.toml` · `evm_version` from DECISIONS-LOG (default `paris`) |
| API | Hono + `@hono/zod-openapi` · Drizzle on PostgreSQL 17 · Redis 7 · BullMQ · viem v2 · pino |
| Mobile | Expo (latest stable SDK) + Expo Router · NativeWind v4 · Reanimated · react-native-svg · expo-haptics · expo-speech · react-native-webview (games) |
| Web | Next.js App Router · Tailwind v4 · wagmi v2 + viem · Reown AppKit |
| Games | Vite + Phaser 3 in `apps/games`, embedded in mobile (WebView) and web (iframe) |
| AI coach | `@anthropic-ai/sdk`, server-side only, per `docs/08-AI-COACH.md` |

## Commands
```bash
pnpm install
pnpm -w lint && pnpm -w typecheck && pnpm -w test     # must pass before a task is DONE
pnpm --filter @muchwalk/contracts test                 # forge test -vvv
pnpm --filter @muchwalk/contracts analyze              # slither + aderyn
pnpm --filter @muchwalk/api dev
pnpm --filter @muchwalk/mobile start
pnpm --filter @muchwalk/games dev
```

## Conventions
- Package names are `@muchwalk/<name>`. Use named exports, and keep files under about 300 lines.
- **Money is integer math.** TREAT is an 18-decimal `bigint`. Steps are `int`. Never put token amounts in a JS `number`.
- **Times are UTC.** Use ISO strings in code and `timestamptz` in the database. A user's "day" is their local day, computed from the `tz` stored on the user.
- **Validate every external input with zod.** Responses are `{ data }` or `{ error: { code, message } }`.
- **UI copy follows the tone guide** in `docs/10-UI-UX.md` §6, with at most one "wow" per screen.
- **Tests live next to the code** (`*.test.ts`). Solidity tests go in `packages/contracts/test/`.

## Doc map
| Need | Read |
|---|---|
| What and why | `docs/01-VISION-AND-INNOVATIONS.md` |
| XP, leagues, badges, avatars, items, loot, games | `docs/02-GAME-DESIGN.md` |
| Token, emissions, reward formula, fees | `docs/03-TOKENOMICS.md` |
| Stack, repo layout, chain config | `docs/04-ARCHITECTURE.md` |
| Contract interfaces and invariants | `docs/05-SMART-CONTRACTS.md` |
| DB schema, endpoints, jobs | `docs/06-BACKEND-API.md` |
| Step verification and trust score | `docs/07-ANTI-CHEAT.md` (kept private) |
| Coach Bark | `docs/08-AI-COACH.md` |
| Threat model and security testing | `docs/09-SECURITY.md` |
| Design system and screens | `docs/10-UI-UX.md` + `prototype/index.html` |
| Tasks | `docs/11-BUILD-PLAN.md` |
| Launch checklists | `docs/12-LAUNCH.md` |
