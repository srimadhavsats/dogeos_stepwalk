# 14 · Concept C: "Pack Battles" (dog card battler)

> **Status: concept under test** (prototype build v4, Battle and Cards tabs). It builds on Sniffari (13): **you walk to find dogs, and the dogs become battle cards.**
> Influences: team-building auto-battlers and mobile collection fighters, where you collect cards, upgrade them, fuse duplicates and get new releases every season. We use generic mechanics only: none of their names, art, currencies or trademarks.

## 1. Core loop
```
WALK ──► meet dogs (Wild) ──► befriend = new card
  │                                │
  ├─► Training Treats (card XP)    ├─► level up (Bones + Treats)
  ├─► Pass XP (season pass)        ├─► fuse duplicates (F0 → F10)
  └─► daily reward chests          └─► equip gear + support card
                                         │
                     BATTLE (5v5 auto-battle with tactics) ◄─┘
                       Tower (PvE) · Friendly · Ranked (league caps)
                                         │
                     rewards: Bones, Pawprints, cards, pass XP, season prizes
```
**The free-to-play promise:** every battle card can be earned by a player who walks and plays every day. Paying saves time and buys cosmetics. It never unlocks power that free players can't reach.

## 2. Card tiers (dog cards)
| Tier | How you get it | Base stats | Special | Passives | Gear slots | Bark Points |
|---|---|---|---|---|---|---|
| 🥉 **Bronze** | Encounters, Bones packs | ×1.00 | Standard | None | 1 | 3 |
| 🥈 **Silver** | Encounters, packs, Tower | ×1.12 | Standard +10% | 1 basic (+5% main stat) | 1 | 5 |
| 🥇 **Gold · Basic** | Rare encounters, Gold packs | ×1.25 | +20% | 1 breed passive | 2 | 7 |
| 🥇 **Gold · Challenge** | **Only** from Challenge Tower and events (skill and grind) | ×1.30 | +20% | Breed passive | 2 | 8 |
| 🥇 **Gold · Premium** | Season pass, shop bundles, **or crafted with Pawprints** | ×1.30 | +20% | Breed passive | 2 | 8 |
| 💎 **Diamond** | Golden Hour encounters (rare), Tower top floor, season rank rewards, crafting, shop (1 per account) | ×1.50 | +35% | **Dual + triple synergy passives** | 3, including **Diamond-exclusive gear** | 10 |

Diamonds also get a custom animated frame and a custom display avatar.

**Season 1 catalog: 60 cards.** That's 18 breeds × (Bronze + Silver) + 18 Golds (6 Basic, 6 Challenge, 6 Premium) + **6 Diamonds**, one per class:
- Iron Fang (Doberman)
- Truffle King (Bloodhound)
- Blur (Greyhound)
- Aurora (Husky)
- Sunbeam (Golden)
- Moon Doge (Shiba)

"Collect them all" is a season-sized goal. Each new season or partner set adds cards.

## 3. Stats, levels and fusion
- **Stats:**
  - **ATK:** damage dealt
  - **HP:** health
  - **SPD:** turn order
  - **RCV:** HP recovered at the end of every round
- **Class base stats** (Level 1, F0, Bronze):
  | Class | ATK | HP | SPD | RCV |
  |---|---|---|---|---|
  | Guardian | 40 | 220 | 30 | 10 |
  | Tracker | 55 | 150 | 45 | 8 |
  | Sprinter | 50 | 140 | 70 | 6 |
  | Trekker | 35 | 240 | 25 | 18 |
  | Charmer | 35 | 170 | 40 | 25 |
  | Legend | 55 | 200 | 50 | 15 |
- **Formula:** `stat = base × tierMult × (1 + 0.02 × (level − 1)) × (1 + 0.04 × fusion) × (1 + gear% + support%)`
- **Level:** 1–100. **Level cap = 50 + 5 × fusion**, so F0 caps at 50 and **F10 caps at 100**. A fully maxed card is "Level 100 · Diamond · F10".
- **Training:** costs Bones plus **Training Treats**. Treats are earned by walking (1 per 500 steps), which makes walking the fastest way to train.
- **Fusion** merges duplicates of the same card, and the duplicates are **burned**. If they were NFTs, the burn happens on-chain, which shrinks supply.
  - Copies needed for each step from F1 to F10: 1, 1, 2, 2, 3, 3, 4, 4, 5, 5 (30 copies in total).
  - **Pawprints** can stand in for missing copies: 50 for Bronze, 100 for Silver, 250 for Gold, 1,000 for Diamond.
  - You get Pawprints by dismantling spare cards and from battles.

## 4. Support cards and equipment
- **Support cards** (one per team) boost the whole team:
  - Dog Park: +HP
  - Treat Bag: +RCV
  - Spiked Kit: +ATK
  - Zoomie Shoes: +SPD
  - Pack Banner: +ATK for one class
  - Vet Visit: heal at round 3

  Boost = `base% × (1 + 0.1 × fusion)`. **Support cards can be fused up to 10 times**, using duplicates or Pawprints.
- **Equipment tiers:** Common · Uncommon · Rare · Epic · Legendary.
  - **Slots:** Collar (ATK), Vest (HP), Boots (SPD), Charm (RCV).
  - **Boost by tier:** 3 / 5 / 8 / 12 / 18%.
  - Legendary **Diamond-exclusive** gear, such as the Moon Collar, can only be equipped on Diamond cards.
  - Gear upgrades with Bones up to +10.

## 5. Battle rules (v1)
- **5v5 + 1 support card.** The order of your cards is a tactic: the front card gets hit first.
- **Bark Points cap:** the team's total card cost has to fit under a cap. It's 30 in Ranked, and it changes in some events.
  - You **can't field five Diamonds**, so teams have to mix tiers. Smart team-building beats raw spending.
- **Rounds:**
  - Living cards act in SPD order.
  - A basic attack hits the front enemy. **Trackers target the weakest enemy.**
  - Each action fills a **special meter by 25**. At 100 the card fires its class special.
  - At the end of each round, every card heals by its RCV.
- **Class specials** (scaled by tier):
  | Class | Special | Effect |
  |---|---|---|
  | Guardian | Shield Wall | Shield worth 30% of HP, and enemies must target it for 2 rounds |
  | Tracker | Sniff Strike | 1.8× hit on the weakest enemy |
  | Sprinter | Zoomies | Two 0.8× strikes |
  | Trekker | Second Wind | Heal 35% of HP |
  | Charmer | Puppy Eyes | Stun the strongest enemy for 1 round, and heal the weakest ally 15% |
  | Legend | Much Wow | Team +15% ATK (stacks twice), plus a 1.2× hit |
- **Type wheel** (from 13 §2): ×1.5 damage against the class you beat, ×0.67 against the class that beats you.
- **Breed passives** (Gold and Diamond):
  | Breeds | Passive | Effect |
  |---|---|---|
  | Doberman, Shepherd, Rottweiler | Watchdog | First hit each round −30% |
  | Labrador, Golden, Corgi | Fetch | Heal the weakest ally 4% each round |
  | Greyhound, Whippet, Collie | Head Start | +25% SPD and +10% ATK in round 1 |
  | Beagle, Bloodhound, Dachshund | Nose | +20% damage against enemies under 50% HP |
  | Husky, Malamute, St Bernard | Howl | +6% ATK per living Trekker |
  | Shiba, Akita, Samoyed | Wow | 15% dodge chance |
- **Diamond synergies** (both stack):
  - **Dual:** +12% to all stats if 2 or more allies share the Diamond's class.
  - **Triple ("Doge Trinity"):** team +10% ATK and RCV if the team has a Legend, a Guardian and a Charmer.
- **Ending:** a side loses when all its cards are knocked out. After 20 rounds, the side with more total HP% left wins.
- **Fair and verifiable:** every battle runs on the server with a committed seed (03 §6 pattern). PvP is **async**, against a snapshot of the other player's team. That works on mobile and resists cheating.

## 6. Modes
| Mode | What | Rewards |
|---|---|---|
| 🗼 **Challenge Tower** | A weekly PvE tower of 10 floors that gets harder each floor. Some floors have special rules ("Rainy Day: SPD −20%") | Bones each floor. **Gold Challenge card at floors 5 and 10** |
| 🤝 **Friendly** | Battle a friend's team | Pass XP only |
| 🏆 **Ranked** | Async PvP ladder, 1-month seasons. **Leagues cap card power** | Bones, Pawprints, season chest. Top ranks share the Games pool (03 §5) |
| 🎪 **Events** (later) | Partner sets, limited rules, guild wars | Event cards and skins |

**League caps (our main anti-pay-to-win lever):** within a league, every card fights at no more than that league's cap. A whale's L100 F10 card fights like an L30 F3 card in Bronze League.
| League | Max level / fusion used in battle | Bark Points |
|---|---|---|
| Bronze | L30 / F3 | 30 |
| Silver | L50 / F5 | 30 |
| Gold | L70 / F7 | 30 |
| Diamond | L100 / F10 | 30 |

## 7. Economy and currencies
| Currency | On-chain? | Earned by | Spent on |
|---|---|---|---|
| **Bones** | No | Battles, quests, steps, the pass | Training, gear upgrades, **random packs** |
| **Training Treats** | No | **Walking** (1 per 500 steps) | Card XP |
| **Pawprints** | No | Dismantling spare cards, battles | Fusion stand-ins, crafting specific cards |
| **TREAT** | Yes | Daily pool share (03), Ranked season pool | Minting cards as NFTs, pass premium, shop deals, market fees |

- **Random packs cost Bones only** (earned currency, with published odds).
- **Paid deals always have exact, visible contents.** We never sell a random box for money or TREAT (same rule as 02 §17), which keeps us clear of gambling and app-store loot-box issues.
- **Shop: every 10 hours** a new set of 3 limited deals appears. Each deal can be bought once per window. Deals that add battle power are limited to 2 a week.
- **NFTs on demand:**
  - Cards live in your account for free.
  - **Gold and Diamond cards can be minted as NFTs** for a TREAT fee, which is burned. After that they can be traded, rented or sold (05 §2.8–§2.9).
  - Fusing burns the fused-in copies.
  - The **first 1,000 Diamonds ever minted** get a permanent **Founders foil**. This replaces the Genesis 1,000 idea if this concept wins.
- **Walking still matters:** battles are free to play, but the daily **reward chest** fills with steps. Training Treats come only from walking. Encounters are the main source of new cards.

## 8. Season pass (1 month, added later in production)
- 30 tiers. **Pass XP** comes from daily and weekly quests, battles, and **10 XP per 1,000 steps**.
- **Free track:**
  - Bones, Pawprints and Treats
  - Bronze and Silver cards
  - 1 Gold Basic card
  - A season frame at tier 30
- **Premium track** (500 TREAT or the DOGE equivalent):
  - Mostly **cosmetics and limited skins** (e.g. Astro Biscuit, a Moon Doge Diamond skin at tier 30)
  - 1 Gold Premium card
  - Extra Bones

  Premium gives no exclusive battle power.

## 9. Seasons and partnerships
- Each season: a new set of cards, a Tower theme, pass skins and a Ranked reset.
- **Partner sets:** mascot dogs from other DogeOS projects become cards (collab events). Each side brings its community.

## 10. Anti-pay-to-win summary
1. League caps and the Bark Points cap.
2. Every card can be earned without paying, including Diamonds (encounters, Tower, rank rewards, crafting).
3. Paid offers save time or add cosmetics, and power deals are capped weekly.
4. Skill counts: lineup order, type matchups, synergies, Tower rule sets.
5. **Walking is the grind:** the fastest progress belongs to people who walk.

## 11. Risks
- **IP:** use generic mechanics only. No other games' names, currencies (we use Bones, Pawprints and Treats), art or slogans.
- **Gambling and app stores:** odds are published and random packs cost only earned currency. Paid purchases on iOS/Android may need in-app purchase (09 §11).
- **Bots:** server-side battles, rewards gated on verified steps, and caps on daily rewards.
- **Scope:** the card game is a big build. Ship v1 as Tower, Friendly and Ranked with 60 cards, then events, guilds and real-time modes later.

## 12. Decisions needed
1. Make Pack Battles the core game, with Wild as the card source? (Recommended.)
2. Cards as NFTs only on demand (Gold+), or every card on-chain?
3. Should the Founders foil replace the Genesis 1,000?
4. The pass price, and the shop's weekly cap on power deals.
