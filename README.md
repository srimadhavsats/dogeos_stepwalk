# 🐕 MuchWalk — *much walk. very health. wow.*

A move-to-earn dapp for the Dogecoin community, built on **DogeOS** and starting on the **Chikyū testnet**.

Walk, run or roll (wheelchair pushes count). Your verified steps **mine Walk Blocks** and earn **$TREAT**. Raise your Pup and dress up your Walker. Open loot boxes you earned by walking. Collect, trade and rent **Genesis NFTs** (only 1,000 will ever exist), and play mini-games that run on your real steps. **Coach Bark**, the AI coach, cheers you on along the way.

📄 [Whitepaper](docs/WHITEPAPER.md) · 💰 [Tokenomics v2](docs/TOKENOMICS.md) · ▶ [Live prototype](https://srimadhavsats.github.io/dogeos_stepwalk/) (both docs are also readable on the live site)

**Live prototype:** https://srimadhavsats.github.io/dogeos_stepwalk/

> Status: specs and prototype are done; the build is next. See `docs/PROGRESS.md`.

## What makes it different
| Feature | One-liner |
|---|---|
| **Proof-of-Walk Mining** | Your steps are your hashrate. A Walk Block is found every 10 minutes, and the live feed shows who found it |
| **Moon Mission** | The community walks 384,400 km to the Moon each season. Landing triggers a Moon Party |
| **Cheer Lane** | Friends tip DOGE or TREAT mid-run, and Coach Bark reads each tip aloud in your earbuds |
| **Pack Walks** | Group walks in real life, verified by QR + GPS. They earn a bonus and double as anti-cheat |
| **Walk Bets** | Stake on your own goal. Finishers split the quitters' stakes. If nobody finishes, the pool goes to dog shelters |
| **Genesis 1,000** | 500 Pups, 350 Walkers and 150 Relics, graded Normal → Much Wow. Mostly earned, never inflated |
| **Market: sell, trade, rent** | Fixed-price sales, NFT↔NFT swaps, and rentals that never take custody of your NFT (ERC-4907) |
| **Loot you earn** | Daily, quest, streak and season boxes with published odds and verifiable rolls. A nightly Genesis Draw. Never sold |
| **Walk-to-play games** | Fetch Frenzy (runner) and Doge Derby (weekly Pup race), with tickets earned by walking |
| **Points First economy** (v6) | Treats start as no-value points. Real dog walks fill a revenue-linked daily Treat Bowl, paid items are priced in DOGE, instant claims burn half (or vest 21 days), leash energy sets a free tier, and sponsors pay for themed walks. TREAT launches only after a revenue gate. See [`docs/TOKENOMICS.md`](docs/TOKENOMICS.md) |
| **Grand Heist alignment** (concept test) | Built around the DogeOS Grand Heist: Demolition Dogs, Kernel Crew and Barkitects as card factions, a Fat Cat Vault, squirrel distractions, faction missions and a weekly faction step race. Community concept, not affiliated with DogeOS. See [`docs/15`](docs/15-CONCEPT-GRAND-HEIST.md) |
| **Pack Battles** (concept test) | Dog card battler: 5v5 teams, Bronze → Silver → Gold → Diamond cards, fusion F0–F10, level 100, support cards, gear, a 10-hour shop and a season pass. See [`docs/14`](docs/14-CONCEPT-PACK-BATTLES.md) |
| **Wild: Sniffari** (concept test) | Meet dogs on your walks (6k ★ Golden Hour), befriend them with a trust meter, fill the 18-breed Pawdex, and battle in the Arena. See [`docs/13`](docs/13-CONCEPT-SNIFFARI.md) |
| **Walk first, wallet later** | Day 1 needs no wallet. Connect one only when you want to claim |
| **Roll Mode** | Wheelchair pushes earn the same as steps, and Walkers have a wheelchair base |

Full details: [`docs/01-VISION-AND-INNOVATIONS.md`](docs/01-VISION-AND-INNOVATIONS.md).

## Builds (switch any time)
| Build | Live link | Git tag |
|---|---|---|
| **v6 · Points First** (latest) | [open](https://srimadhavsats.github.io/dogeos_stepwalk/builds/v6/) | `v0.6-points-first` |
| v5 · Grand Heist | [open](https://srimadhavsats.github.io/dogeos_stepwalk/builds/v5/) | `v0.5-grand-heist` |
| v4 · Pack Battles | [open](https://srimadhavsats.github.io/dogeos_stepwalk/builds/v4/) | `v0.4-pack-battles` |
| v3 · Sniffari | [open](https://srimadhavsats.github.io/dogeos_stepwalk/builds/v3/) | `v0.3-sniffari` |
| v2 · Collect & Play | [open](https://srimadhavsats.github.io/dogeos_stepwalk/builds/v2/) | `v0.2-collect-and-play` |
| v1 · First prototype | [open](https://srimadhavsats.github.io/dogeos_stepwalk/builds/v1/) | `v0.1-first-prototype` |

All builds: https://srimadhavsats.github.io/dogeos_stepwalk/builds/ · To get an older build's code and docs locally, run `git checkout v0.3-sniffari` (and `git checkout main` to come back).

## Repo map
```
CONTRIBUTING.md        workflow, stack, conventions, doc map
docs/                  specs 01–15, build plan, progress tracker, decisions log
docs/WHITEPAPER.md     the product and the plan, for partners and players
docs/TOKENOMICS.md     economy v2 (Points First, Treat Bowl, claims, energy, sponsors)
prototype/index.html   clickable UI prototype (source of truth for look & feel)
prototype/*.html       whitepaper and tokenomics reading pages, built by scripts/build_docs.py
apps/ packages/        created during the build (docs/04-ARCHITECTURE.md §3)
```

## Build plan at a glance
65 task cards in [`docs/11-BUILD-PLAN.md`](docs/11-BUILD-PLAN.md), each tagged by complexity: 🔴 Critical (6) · 🟠 Complex (11) · 🟡 Standard (35) · 🟢 Simple (13).
Milestones: **M1** local loop → **M2** internal testnet → **M2b** Collect & Play → **M3** public testnet beta → **M4** mainnet.

## Steps only the team can do
- Get testnet DOGE from the DogeOS faucet (one claim per 24h), and keep deploy keys in a hardware wallet.
- Open the accounts: Apple Developer, Google Play Console, Expo/EAS, Anthropic API, Reown, hosting (Railway or Fly.io, Neon, Upstash, Cloudflare R2) and Vercel.
- Before mainnet: a legal review (token, Walk Bets, loot and draws, marketplace, health data), an external audit, and a bug bounty. See `docs/12-LAUNCH.md`.
