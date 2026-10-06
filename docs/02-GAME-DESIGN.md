# 02 · Game Design (progression, leagues, badges, Pup)

> Every number here is a **constant in `packages/shared/src/game/constants.ts`**. Code reads the constants and never hardcodes a value.
> XP, levels, streaks, quests and leagues are **off-chain** and non-transferable. Only badges, Pups and TREAT are on-chain.

## 1. Core loop
```
Move (steps / pushes / sessions)
  → verified by anti-cheat (07)
  → Walk Points (WP)  → daily TREAT share (03)
  → XP                → levels, unlocks, league rank
  → Pup XP            → Pup levels / evolution
  → hashes            → Walk Block finder draws
  → distance          → Moon Mission progress
Daily: goal ring, 3 quests, chest, streak
Weekly: league result, coach review
Seasonal: Moon Mission, battle pass
```

## 2. Activity units
- **Step unit (SU):** 1 verified step, **or** 1 verified wheelchair push in Roll Mode. Everything below says SU.
- **Session:** a GPS-tracked activity the user starts manually. Types are `walk`, `run`, `roll` and `pack`. A session must last at least 5 minutes to count.
- **Distance:** comes from GPS during a session. Outside a session it's estimated as `SU × stride`, where `stride = heightCm × 0.00415 m` (default 0.72 m when height is unknown) and a push counts as `1.2 m`.

## 3. Daily goal (adaptive)
- New users start at **5,000 SU**.
- After 7 days with data, the goal becomes `clamp(roundTo500(median(last14DaysSU) × 1.05), 3000, 15000)`. It's recomputed at local midnight.
- Users may pin a manual goal between 3,000 and 25,000. The pin lasts until they unpin it.
- **Goal met** means daily SU ≥ goal. That's what counts for the streak, gives +50 XP, and makes the Pup happy.

## 4. XP sources (per local day)
| Source | XP | Daily cap |
|---|---|---|
| Steps | 1 XP per 100 SU | 250 XP (25k SU) |
| Daily goal met | 50 | 1× |
| Quest done (easy / medium / hard) | 20 / 35 / 50 | 3 quests |
| Session ≥ 15 min | 20 | 2× |
| Pack Walk completed | 40 | 1× |
| Walk Block found | 30 | none |
| Walk Bet completed | 200 | per bet |
| Streak milestone 7 / 30 / 100 / 365 | 100 / 300 / 1,000 / 3,000 | once each |

A typical active day (8k SU, goal met, 2 quests, 1 session) earns about **200 XP**.

## 5. Levels (user)
- `cumulativeXp(L) = floor(50 × (L − 1)^1.8)` for L = 1…100.
- **Precompute a table `LEVEL_XP[1..100]` once, commit it, and use only the table.** Floating-point `pow` can differ between JS engines, so we never call it at runtime. A unit test regenerates the table and compares.
- Reference values: L2 = 50 · L5 ≈ 606 · L10 ≈ 2,610 · L20 ≈ 10,016 · L35 ≈ 28,537 · L50 ≈ 55,050 · L75 ≈ 115,600 · L100 ≈ 195,250.

| Levels | Title | Unlocks |
|---|---|---|
| 1–4 | Sniffer | Walk, Pup, Coach (10 msgs/day), quests, league |
| 3 | — | **Go Live (Cheer Lane)**, sending tips |
| 5–9 | Trotter | **Walk Bets** (also needs account age ≥ 7 days) |
| 8 | — | Join packs |
| 10–19 | Strider | Create packs, Coach 25 msgs/day, custom goal |
| 20–34 | Zoomer | Second Relic slot, pack captain badge frame |
| 35–49 | Pack Leader | Profile flair |
| 50–74 | Alpha Walker | Animated profile frame |
| 75–99 | Legend | Legendary frame |
| 100 | **Moon Walker** | Mythic frame + "Moon Walker" SBT (id 199) |

Every level-up gives 1 chest. Every 5th level also gives a cosmetic.

## 6. Streaks
- A day counts when the daily goal is met. Days are local, using the `tz` stored on the user. A tz change takes effect from the next day.
- **Streak Shield:** if a day is missed and a shield is held, the shield is used up automatically and the streak survives. You earn 1 shield per 7 consecutive goal days and can hold at most 2. You can also buy one for **50 TREAT (burned)**, at most once a week.
- **Rest Day:** users may mark up to 3 rest days per calendar month, any time before 23:59 local on that day. The streak is frozen and no shield is used.
- **Injury Mode:** pauses the streak for up to 14 days, once per calendar quarter.
- Streak bonus to Walk Points: `+1% per streak day, max +25%`. Details in 03 §4.

## 7. Daily quests
Each day a user gets 1 easy, 1 medium and 1 hard quest. They're picked deterministically: `seed = sha256(userId + localDate)`, index = seed mod pool size. Social quests are only assigned to users with at least one friend.

| ID | Tier | Text (UI) | Rule |
|---|---|---|---|
| Q_MORNING_2K | easy | "2,000 steps before 10am" | SU with local timestamp < 10:00 ≥ 2,000 |
| Q_GOAL_40 | easy | "Reach 40% of your goal" | daily SU ≥ 0.4 × goal |
| Q_CHEER_1 | easy (social) | "Cheer a friend" | ≥ 1 cheer sent |
| Q_SESSION_15 | medium | "Take a 15-min walk session" | a session ≥ 15 min |
| Q_BRISK_5 | medium | "5 brisk minutes (110+ steps/min)" | ≥ 5 minutes with cadence ≥ 110 |
| Q_GOAL | medium | "Hit your daily goal" | goal met |
| Q_BLOCKS_6 | medium | "Add hashes to 6 Walk Blocks" | SU in ≥ 6 distinct block windows |
| Q_GOAL_120 | hard | "Hit 120% of your goal" | SU ≥ 1.2 × goal |
| Q_RUN_3K | hard | "Run 3 km in one session" | run session distance ≥ 3,000 m |
| Q_PACK | hard (social) | "Finish a Pack Walk" | a verified pack session |
| Q_EVENING_3K | hard | "3,000 steps after 6pm" | SU with local ts ≥ 18:00 ≥ 3,000 |

**Quest Box:** finishing all 3 quests awards a Quest Box. See §17 for loot boxes.

## 8. Leagues (weekly, Duolingo-style)
- The week runs **Mon 00:00 UTC to Sun 23:59:59 UTC**. Score = XP earned that week.
- Tiers, low to high: **Kibble → Biscuit → Bone → Bacon → Steak → Golden Bone → Diamond Paw → Moon**.
- Cohorts hold **30 users** of the same tier, filled in order of the week's first activity. Users with 0 XP last week aren't placed until they're active again.
- **Top 7 promote** (except in Moon). **Bottom 5 demote** (except in Kibble). Ties are broken by who reached the score first.
- **TREAT rewards** come from the weekly League pool (03 §3):
  - Cohort pool = `weeklyPool × tierWeight / Σ(tierWeight of all cohorts)`, with tierWeight = [1, 1.2, 1.4, 1.7, 2, 2.5, 3, 4].
  - Within a cohort: rank 1 gets 20%, rank 2 14%, rank 3 10%, ranks 4–10 4% each, ranks 11–20 2.8% each, ranks 21–30 nothing.
  - Only users with trust ≥ 0.5 are eligible. Shares nobody can take roll into next week's pool.
- **Medals:** ranks 1–3 earn Gold, Silver and Bronze medals. These are off-chain collectibles shown in the trophy case. Medals can be minted monthly into a **Medal Case SBT** (ids 801–803, with the amount as the balance).

## 9. Badges (BadgeSBT token IDs, soulbound ERC-1155)
Rarity: N = Normal, R = Rare, SR = Super Rare, L = Legendary, M = Much Wow (mythic). The Genesis NFTs and items use the same scale.

| ID | Name | Criteria | Rarity |
|---|---|---|---|
| 101 | First Paw | First verified day ≥ 1,000 SU | N |
| 102 | Ten-K Club | First day ≥ 10,000 SU | N |
| 103 | 100K Paws | 100,000 lifetime SU | N |
| 104 | Millionaire Paws | 1,000,000 lifetime SU | R |
| 105 | Ten Million Wow | 10,000,000 lifetime SU | SR |
| 106 | Marathon Doge | A single session ≥ 42,195 m | SR |
| 199 | Moon Walker | User level 100 | M |
| 201 | Week Streak | 7-day streak | N |
| 202 | Month Streak | 30-day streak | R |
| 203 | Century Streak | 100-day streak | SR |
| 204 | Year of the Doge | 365-day streak | L |
| 301 | ISS Reached | Contributed ≥ 5 km before the ISS checkpoint | N |
| 302 | Geo Reached | Contributed ≥ 5 km before the GEO checkpoint | R |
| 303 | Moon Lander | Contributed ≥ 5 km before the Moon landing | SR |
| 401 | Block Finder | Found the first Walk Block | R |
| 402 | Lucky Shibe | Found 10 Walk Blocks | SR |
| 403 | Such Miner | Hashes in 1,000 distinct blocks | R |
| 501 | Pack Pup | First Pack Walk | N |
| 502 | Pack Leader | 25 Pack Walks | R |
| 601 | First Cheer | Sent the first tip | N |
| 602 | Crowd Favourite | Received 100 cheers | R |
| 701 | Bet on Me | Completed the first Walk Bet | N |
| 702 | Iron Will | Completed 10 Walk Bets | SR |
| 703 | Shelter Hero | Was in a bet pool that went to the Shelter Fund | R |
| 801–803 | Gold / Silver / Bronze Medal Case | League podium medals (balance = count) | R |
| 851 | Chikyū Pioneer | Active on ≥ 7 days during the testnet | L |
| 901 | Rolling Thunder | 100,000 lifetime pushes | R |
| 902 | Early Bird | 30 days with 2,000 SU before 7am | R |
| 903 | Night Owl | 30 days with 2,000 SU after 9pm | R |
| 904 | Explorer | Sessions in 10 distinct H3 res-7 cells | R |

The Pioneer badge is **recognition only**. We never promise it will have mainnet token value, both for legal reasons and to avoid attracting farmers.

## 10. Pup (companion)
**Two kinds of Pup:**
- **Starter Pup:** free, lives in the app (off-chain), one per account. Every user gets one at onboarding.
- **Genesis Pup:** one of the 500 Pup NFTs (§19). It can be owned, bought, traded or rented.

**What applies to both:**
- **Equipping:** one Pup is equipped at a time. A Genesis Pup only counts while you're its *user*: the owner when it isn't rented out, or the renter while a rental is active.
- **Pup XP** = 1 per 100 SU walked while that Pup is equipped. No other bonuses apply to Pup XP.
  - **A Genesis Pup's level belongs to the token**, so it carries over when the Pup is sold or rented. The worker syncs it on-chain.
- **Pup level:** `cumulativePupXp(L) = floor(60 × (L − 1)^1.6)`, max level 50, using a precomputed `PUP_LEVEL_XP` table. L5 ≈ 551, about one week of walking.
- **Stages:** Puppy (L1–9) → Shibe (L10–24) → Doge (L25–49) → Moon Doge (L50).
  - At L9, L24 and L49 the level **stops rising until the user taps Evolve**, which burns **100 / 500 / 2,000 TREAT** through `TreatSink`. XP keeps building up in the meantime.
- **Companion bonus** (the only NFT-linked reward bonus): `companionBps = min(3_000, 40 × pupLevel + rarityBps)`.
  - `rarityBps`: Starter 0 · Normal 200 · Rare 400 · Super Rare 700 · Legendary 1,000 · Much Wow 1,500.
  - Pups never stack.
- **Mood** (cosmetic only, never punishing):
  - Happy: goal met today
  - Content: ≥ 50% of goal
  - Sleepy: < 50% of goal
  - Missing you: no SU for 2+ days
- **Traits**, from `traitsSeed`:
  - Coat: Classic Red 50%, Sesame 20%, Black & Tan 15%, Cream 12%, Galaxy 2.5%, Gold 0.5%
  - Eyes ×5, markings ×4, tail curl ×3
  - A **starter** Pup's coat is picked by the user from the 4 common coats. Galaxy and Gold appear only on Genesis Pups.
- **Pup item slots:** hat, eyewear, collar and shoes. Items are off-chain and purely cosmetic (§16).

## 11. Moon Mission (seasons)
- Checkpoints: ISS **408 km** → GEO **35,786 km** → Moon **384,400 km**. Progress = Σ verified distance from users with trust ≥ 0.5.
- A season ends at the Moon landing or after 120 days, whichever comes first. The next season starts again from Earth with a new theme.
- Checkpoint badges (301–303) go to users who contributed ≥ 5 km to the season before that checkpoint was reached.
- **Moon Party:** on landing, the next UTC day's walk budget is doubled, funded from the Community allocation (03 §7).

## 12. Walk Blocks (UX side; the economics are in 03 §6)
- **Home ticker:** "Block #N closes in mm:ss · your hashes: X".
- **Moon tab feed:** the last 20 finalized blocks, showing finder, hashes and reward.
- When a block finalizes in your favour: a push notification, confetti, a "wow" word burst, and Block Finder badge progress.

## 13. Notifications policy
- At most **3 per day**, with quiet hours from 21:30 to 08:00 local.
- Priority order:
  1. Block found
  2. Streak at risk (19:30 local, if under 60% of goal and no shield held)
  3. A friend is live (max 2 per day)
  4. Overtaken in league (max 1 per day, Thu–Sun only)
  5. Weekly league result (Mon 09:00)
  6. Coach morning plan (opt-in, 08:00)

## 14. Healthy-design guardrails (non-negotiable)
- No rewards for SU above 20k per day (see the 03 curve). Coach Bark never shames anyone, and Rest Days and Injury Mode exist.
- No loss mechanics on the Pup. No infinite feeds. No push notifications during quiet hours.
- Show **"time to go outside" prompts**, not "time in app". Our KPI is goal days, not session length.

## 15. Walker (player avatar)
- Every account has a **Walker**, an off-chain avatar shown walking its Pup on Home, in leagues, on Pack Walk cards and in the games.
- **Base:** standing, or **wheelchair** (Roll Mode users get this by default but can change it). Choice of 6 skin tones, all free.
- **Slots:** hair · top · bottom · shoes · headwear · eyewear · accessory (leash style, backpack, …).
- **Starter kit:** 2 Normal items per slot, free.
- A **Genesis Walker** NFT (§19) is a complete, unique look. While equipped it replaces the base and slots, and you can switch back any time.
- Renderer: `packages/shared/src/avatar/render.ts` (layered SVG, same style as the Pup). The same output is used in the app, the web, the games and NFT metadata.

## 16. Items, rarity and inventory
**Rarity scale** (used for items, badges and Genesis NFTs):
| Tier | Colour token | Feel |
|---|---|---|
| Normal | `mint` | everyday |
| Rare | `sky` | nice find |
| Super Rare | `moon` | brag-worthy |
| Legendary | `gold` | very few exist |
| Much Wow | rainbow | mythic |

**Catalog v1:** 118 off-chain items. Rarity split: 50 Normal · 35 Rare · 20 Super Rare · 10 Legendary · 3 Much Wow.
| Owner | Slot counts | Total |
|---|---|---|
| Walker | hair 16, top 16, bottom 10, shoes 10, headwear 10, eyewear 8, accessory 10 | 80 |
| Pup | hat 10, eyewear 8, collar 12, shoes 8 | 38 |

The catalog lives in `packages/shared/src/items/catalog.ts`. Each entry has `id, owner (walker|pup), slot, rarity, sources[], setId?`.

**Rules:**
- **Unlocked gradually:**
  - Each level from 2 to 100 unlocks **one item from a fixed unlock track** (99 items, alternating Walker and Pup).
  - Track rarity rises with level: L2–19 Normal · L20–49 Rare · L50–79 Super Rare · L80–99 Legendary · L100 Much Wow.
  - Other items come only from loot (§17), the Forge (§18), events, or the TREAT shop (Normal/Rare cosmetics only, 03 §10).
- **Off-chain and not tradable.** You can hold one copy of each item. A **duplicate becomes shards** automatically: Normal 5 · Rare 15 · Super Rare 40 · Legendary 100 · Much Wow 300.
- Items are **cosmetic only** in the walk economy. Some give small, capped perks in the mini-games (§20).
- **Collections:** 6 themed sets of 6 items each, all Rare or above:
  - Moon Set → Relic
  - Mining Set → Relic
  - Shelter Set → Pup
  - Doge Classic Set → Pup
  - Pack Set → Walker
  - Marathon Set → Walker

  A completed set can be forged into a Genesis NFT of the kind shown (§18).

## 17. Loot boxes (earned only, never sold)
| Box | How you earn it | Rolls | Loot table | Genesis Draw entries |
|---|---|---|---|---|
| Daily Box | Daily goal met | 1 | D | 1 |
| Quest Box | All 3 quests done (+1 game ticket) | 2 | Q | 2 |
| Streak Box | Every 7-day streak milestone | 3 (at least one Rare+ guaranteed) | S | 5 |
| Season Box | Moon checkpoints, league podium, Derby win | 3 | S | 20 |
| Forge Box | Crafted for 100 shards | 2 | Q | 2 |

**Loot tables** (odds per roll; shown in-app on every box):
| Outcome | D | Q | S |
|---|---|---|---|
| XP (+30 / +50 / +100) | 45% | 35% | 20% |
| Shards (5–15 / 10–25 / 25–60) | 27% | 30% | 25% |
| Normal item | 18% | 18% | — |
| Rare item | 7% | 12% | 38% |
| Super Rare item | 2.5% | 4% | 13% |
| Legendary item | 0.45% | 0.9% | 3.5% |
| Much Wow item | 0.05% | 0.1% | 0.5% |

**Pity timer:** after 10 boxes with no Rare+ item, the next roll is forced to Rare. After 50 boxes with no Super Rare+ item, the next roll is forced to Super Rare. A rolled item is picked uniformly from loot-eligible items of that rarity.

**Limits:**
- At most 6 boxes can be opened per day. Extras are stored for up to 30 days.
- Boxes can't be transferred, and **can never be bought with money or TREAT**.

**Verifiable rolls:**
- `roll = keccak256(secret[e], accountId, boxId, rollIndex)`, using the same daily `secret[e]` that is committed for Walk Blocks (03 §6).
- Once the secret is revealed, users can re-check every roll in their box history.

**Genesis Draw (nightly):**
- Every box opened today counts as entries (column above) into tonight's draw.
- **Eligible** accounts: trust ≥ 7,000, account age ≥ 14 days, wallet linked, and no Genesis win yet this season.
- Number of winners: `drawsToday = min(poolLeft, ceil(poolLeft / max(1, 120 − seasonDay)))`.
- It's a weighted draw without replacement, using the same algorithm as Walk Blocks, with `r = keccak256(secret[e], "genesis", e, i)`.
- **Winners get a Genesis Ticket:** a signed voucher valid for 30 days. Tickets not claimed in time go back to the pool.
- This guarantees the season's drop count is exact, however many people play.

## 18. Forge (crafting)
| Recipe | Cost | Result |
|---|---|---|
| Item | 25 / 75 / 200 / 600 shards | A random unowned item of Normal / Rare / Super Rare / Legendary rarity (refunded if you already own them all) |
| Forge Box | 100 shards | 1 Forge Box |
| **Genesis Forge** | A complete Collection (6 items, **consumed**) + **2,000 TREAT** burned through `TreatSink` | A Genesis NFT of the set's kind. Rarity is drawn from the remaining supply, weighted Normal 55 · Rare 30 · Super Rare 12 · Legendary 3 |

The Genesis Forge is limited per season (§19). When a season's Forge allocation runs out, the Genesis Forge closes until the next season.

## 19. Genesis Collection (the only tradable NFTs; hard cap 1,000)
**Supply matrix** (enforced on-chain per cell):
| Kind | Normal | Rare | Super Rare | Legendary | Much Wow | Total |
|---|---|---|---|---|---|---|
| Pup | 250 | 140 | 75 | 30 | 5 | **500** |
| Walker | 175 | 100 | 50 | 20 | 5 | **350** |
| Relic | 75 | 40 | 25 | 10 | 0 | **150** |
| **Total** | 500 | 280 | 150 | 60 | 10 | **1,000** |

**Distribution by season.** Unused allocation rolls over into the same channel next season. After S4, any leftovers move to Achievements.
| Channel | Total | S1 | S2 | S3 | S4 |
|---|---|---|---|---|---|
| Loot (Genesis Draw) | 300 | 75 | 75 | 75 | 75 |
| Forge | 250 | 63 | 62 | 63 | 62 |
| Achievements (Moon top contributors, Moon-league podiums, Derby champions, Pioneer raffle) | 200 | 50 | 50 | 50 | 50 |
| Mint sale (mainnet; free claim on testnet) | 150 | 38 | 37 | 38 | 37 |
| Shelter Pups (charity auction, all Pups) | 50 | 13 | 12 | 13 | 12 |
| Partners & giveaways | 50 | 13 | 12 | 13 | 12 |
| **Total** | **1,000** | 252 | 248 | 252 | 248 |

There is **no team allocation**.
The testnet collection is a **rehearsal on its own contract**. Mainnet mints a fresh 1,000.

**Kind and rarity assignment:**
- Channels other than the Forge pick the kind weighted by remaining supply. The Forge kind comes from the set.
- Rarity is a **deck draw** weighted by the remaining count in each (kind, rarity) cell. The seed comes from the voucher, which comes from commit-reveal.
- As a result, the final distribution always matches the matrix exactly.

**Traits and art:**
- Pups: coat, eyes, markings, tail, plus a signature accessory. Walkers: a full outfit plus a pose. Relics: an item with an effect.
- No two tokens share a trait combination.
- **The 70 Legendary and Much Wow pieces are hand-designed.** The rest are generated by the shared renderers.

**Leash lock:** tokens from Loot, Forge or Achievements are `lockedUntil = mintTime + 14 days`. A locked token can't be transferred, listed or rented. Mint-sale, Shelter and Partner tokens have no lock.

**Perks** (they apply to the token's *user*: the renter if rented, otherwise the owner):
| Kind | Walk economy | Mini-games | Social |
|---|---|---|---|
| Pup | Companion `rarityBps` (§10). Pup level travels with the token | Fetch Frenzy: magnet +1 s per tier above Normal · Derby: rarity flair (§20) | Unique art everywhere |
| Walker | — | Fetch Frenzy: +1 life at Legendary or above | Captain frame on Pack Walks |
| Relic | — | One signature effect each (e.g. Moon Boots = double jump, Golden Leash = Derby start +2%) | Equippable on the Walker or the Pup |

Equip limits per account: 1 Genesis Pup, 1 Genesis Walker and 2 Relics at a time.

## 20. Mini-games (walk-to-play)
- **Tickets:** 1 per 2,000 verified SU per day (max 5), plus 1 from each Quest Box. You can hold up to 10. **Tickets can't be bought.**
- **Architecture:**
  - Game logic is a **pure, deterministic TS engine** (`packages/games-core`: fixed 60 Hz timestep, seeded RNG). Phaser only draws it.
  - The server re-runs submitted inputs with the same engine to validate scores (07 §9).

**Fetch Frenzy** (solo arcade, ~90 s per run)
- An endless three-lane runner through Doge City. Your Walker and Pup run together, collecting bones and dodging puddles and squirrels.
- Score = bones × combo multiplier.
- **Rewards per run:**
  - XP = `min(50, floor(score / 100))`
  - shards: 2 at score ≥ 2,000 · 4 at ≥ 5,000 · 6 at ≥ 10,000
  - daily caps from games: 150 XP and 20 shards
- **Weekly global top 100** (trust ≥ 5,000, validated runs only) shares the Games pool (03 §5):
  - rank 1: 10%
  - rank 2: 7%
  - rank 3: 5%
  - ranks 4–10: 3% each
  - ranks 11–50: 1% each
  - ranks 51–100: 0.34% each

**Doge Derby** (weekly async race, a spectator event)
- **Entering:** equip any Pup (starter or Genesis) by **Thursday 23:59 UTC**. The race runs **Sunday 18:00 UTC** in heats of 8 Pups from the same league tier.
- `speed = 1000 + stepsPts + flair + luck`, where:
  - `stepsPts = floor(400 × heatRank / 7)`, with heatRank = 0–7 by verified weekly SU (higher SU ranks higher)
  - `flair`: Starter 0 · Normal 5 · Rare 10 · Super Rare 15 · Legendary 20 · Much Wow 25
  - `luck`: 0–60 from a commit-reveal roll

  **Walking is what wins.** Rarity is mostly for show.
- The final order follows speed (ties broken by luck, then entry time). The replay animation adds drama, but the order is fixed.
- **Rewards:** 1st → Season Box · 2nd → Streak Box · 3rd → Quest Box · everyone +20 XP. Friends can cheer during the replay.

**Later: Bark Cards** (Phase 4, not in v1) — async card duels using items and Genesis NFTs as cards.

**Pup Passport API** (cross-game): `GET /public/passport/:tokenId` returns the kind, rarity, traits, level, SVG URL and a `perksSchemaVersion`. Any DogeOS game can show or use MuchWalk Genesis NFTs.
