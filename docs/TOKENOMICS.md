# MuchWalk Tokenomics v2: the dog-walk economy

> **Draft v0.2 · October 2026 · for discussion.** Every number here is a proposal and can change before launch. This replaces the economy model in [03-TOKENOMICS](03-TOKENOMICS.md). The contract-level details in 03 (Merkle claims, Walk Blocks, Walk Bets math) still apply unless this page says otherwise.
> Read the [Whitepaper](WHITEPAPER.md) for the product side.

## At a glance

| | |
|---|---|
| **Token** | TREAT, hard cap **1,000,000,000**, launched only after Phase 1 proves real revenue |
| **Phase 1 (now)** | **Points First:** Treats are in-app points with **no money value** |
| **Who earns** | People walking a **real dog**. Each walk passes a dog-walk check |
| **Daily rewards** | The **Treat Bowl**, sized by yesterday's money in: ≈ 90% of yesterday's sink spend and revenue, plus a small base |
| **Paid items** | Priced in **DOGE or stablecoins**. 50% of that revenue buys TREAT and burns it |
| **Claiming** | **Instant:** you get 50% and the other 50% is burned. **Vested:** you get 100%, unlocked over 21 days |
| **Earning limits** | **Leash energy**: a free daily tier, then more energy for a leashed Genesis Pup or staked TREAT |
| **Sponsors** | Pet brands and ecosystem apps pay stablecoins for sponsored walks, so someone else pays for those rewards |
| **Long-run target** | TREAT burned ≥ **100%** of TREAT minted |
| **Launch** | Protocol-owned liquidity, locked team tokens, no presale |

## 1. The problem we're solving
Most move-to-earn tokens failed for the same reason. The only buyers were players spending what they had just earned, so every token sold needed a new user to absorb it. When growth slowed, the rewards were dumped and the price only went one way.

Our first design already fixed the worst part:
- Steps never mint tokens.
- A fixed daily pool is shared out, so more users or bots never print more.
- Spending burns TREAT.

That still wasn't enough. Burning 40% of what is minted means 60% of every day's rewards still hits the market. Version 2 adds the missing pieces:
1. Money from outside the game.
2. Rewards that are tied to that money.
3. A reason for earners to hold.

## 2. Design rules
1. **Outside money pays for rewards.** Real revenue (DOGE, stablecoins, sponsors) has to flow in, not only players' own earnings.
2. **Never print more than comes in.** Each day's rewards follow yesterday's spending and revenue. When walking slows, minting slows.
3. **Reward patience.** Taking rewards early costs half, waiting costs nothing, and staking earns perks, never interest.
4. **Every Treat is about walking a real dog.** Dog walks are a habit people already have, and they are hard to fake at scale.
5. **Prove it before there's a price.** Treats run as points first. TREAT launches against real revenue, not hype.

## 3. Phase 1: Points First (where we are now)
In Phase 1, Treats are **points with no money value**:
- They live in your account. No wallet is needed, they can't be transferred and they can't be sold.
- **Treats only buy things that stay in your account:** Pup evolution, Streak Shields, the Heist Pass, training items, cosmetics.
- **Anything tradable is priced in DOGE:** minting a card NFT, the Genesis Forge, marketplace sales and rentals, cheer tips. That way points can never leak out as value.
- Walk Bets run as **stake-free challenges** until TREAT exists.
- **Paid items are priced in DOGE or stablecoins from day one**, so real revenue exists before any token does.
- The full Phase 2 machine (Treat Bowl, commitment claims, staking, leash energy, health metrics) runs on points. Revenue counts at a fixed reference rate of **1 DOGE = 10 Treats**. Before any price exists, we can see whether burns keep up with rewards.

### Launch gate: when TREAT can launch
TREAT launches only when **all** of these are true. The targets are proposals.

| Gate | Target |
|---|---|
| Real revenue | 90 days in a row of DOGE or stablecoin revenue |
| Revenue per daily walker | Trending up in at least 8 of the last 12 weeks |
| Walkers | 5,000+ weekly verified dog walkers, with 30-day retention ≥ 25% |
| Simulated burns | Burned ÷ minted ≥ 1.0 for 8 weeks in a row, measured on points |
| Security | Two independent audits of every token contract |
| Liquidity | The TREAT launch reserve (below) holds enough DOGE for protocol-owned liquidity |

### What happens to Phase 1 money
- **50% of revenue goes into the TREAT launch reserve.** In Phase 2 this share buys back and burns TREAT. In Phase 1 it saves up for the launch, then becomes the DOGE side of protocol-owned liquidity.
- **40%** goes to the treasury: servers, AI coach costs, audits and a 24-month runway.
- **10%** goes to the Shelter Fund, which pays real dog shelters.

### Do points turn into TREAT?
**Not 1:1.** Points stay points. Our proposal is a capped **Walkers Drop** of **3% of supply (30M TREAT)**:
- It is shared by **verified dog-walk days** in Phase 1, not by points, so farming points doesn't pay.
- It comes with sybil checks.
- It is claimed under the same commitment rules (§6).

This is open for discussion and subject to legal review. It is not a promise.

## 4. Supply and allocation
| Bucket | % | TREAT | How it's released |
|---|---|---|---|
| Walk rewards (Treat Bowl ceiling) | 45% | 450,000,000 | Minted only by the RewardsDistributor, never above the ceiling in §5 |
| Walkers Drop (Phase 1 dog walkers) | 3% | 30,000,000 | At launch, under the commitment rules in §6 |
| Liquidity (protocol-owned) | 10% | 100,000,000 | Paired with the launch reserve. LP tokens are held by a timelocked treasury for at least 4 years |
| Ecosystem and sponsors | 10% | 100,000,000 | Partner quests and integrations, released by governance over 4 years |
| Community and Shelter | 8% | 80,000,000 | Events, Moon Parties and shelter donations |
| Treasury | 12% | 120,000,000 | Multisig plus timelock, spent against a published budget |
| Team | 12% | 120,000,000 | On-chain vesting: a 1-year cliff, then linear over 3 years |
| Investors | 0% | 0 | No presale or VC round at launch. Any future strategic round comes out of the treasury, with the team's locks, and is announced first |

## 5. The Treat Bowl (daily rewards)
Each day (one UTC epoch) the bowl is sized by **yesterday's money in**:

```
inflow(d-1)   = Treats burned on sinks + TREAT bought back with revenue and burned
minted(d)     = min( ceiling(d),  base(d) + k × inflow(d-1) )
bowl(d)       = minted(d) + sponsor top-ups (bought on the market, not minted)
```

- **k = 0.9.** The allowed range is 0.8–1.0.
- **base = 12,000 a day in year 1**, about 5% of the ceiling. It shrinks with the ceiling. It keeps rewards alive on quiet days and while revenue ramps up.
- **The ceiling is the old fixed schedule: 246,575 a day in year 1, shrinking 20% a year.** It sums to the 450M bucket, so the hard cap can never be broken.
- Anything not handed out is **never minted**.
- **The contract enforces it.** TreatToken counts every burn. The distributor can never mint more in an epoch than `base + 1.0 × last epoch's burns`, and never more than the ceiling. Even a broken off-chain planner can't over-mint.

**How the bowl is split** (same as before; all three count only verified dog-walk steps):

| Pool | Share | How it's paid |
|---|---|---|
| Walk share | 75% | Pro-rata by Walk Points (§7) |
| Walk Blocks | 15% | 144 blocks a day, drawn by hashes from dog-walk steps |
| Quests and leagues | 10% | Quest points, weekly league prizes, game prizes |

### Worked example (yesterday → today)
| Line | Amount |
|---|---|
| Treats spent on sinks yesterday (burned) | 148,200 |
| DOGE revenue yesterday: Ð 5,130. Half (Ð 2,565) buys back TREAT at an example price of 10 TREAT per DOGE, and it's burned | 25,650 |
| **Inflow** | **173,850** |
| Minted today = 12,000 + 0.9 × 173,850 | **168,465** (ceiling: 246,575) |
| Sponsor top-ups (1,200 USDC of sponsored walks, bought on the market) | 12,000 |
| **Today's bowl** | **180,465** |
| Walk share 75% / Walk Blocks 15% / Quests and leagues 10% | 135,348 / 27,069 / 18,046 |
| **Burned ÷ minted** | 173,850 ÷ 168,465 = **1.03** ✅ |

## 6. Claim with commitment
You decide how to take your rewards:

| Choice | You get | What happens to the rest |
|---|---|---|
| **⚡ Instant** | 50% now | The other 50% is burned. On-chain it's simply never minted, which has the same effect and costs less gas |
| **🌱 Vest** | 100% | Unlocks in a straight line over **21 days**. Unlocked Treats can be claimed any time, gasless |
| **Leave vesting early** | 50% of whatever is still locked | The other 50% of the locked part is burned |

- The 21 days is a proposal; anything from 14 to 28 days works.
- This replaces the old "patient claim" (a 10% fee, or wait 7 days). Daily claim-and-dump becomes expensive, and holders win by default.
- In Phase 1 the same rule applies to points, so we can measure how people choose before it matters.

## 7. Earning: Walk Points and leash energy
### Only real dog walks earn Treats
- Start a walk in the app with **🐕 Dog walk** on.
- When it ends, the **dog-walk check** looks at:
  - **Session length:** at least 10 minutes.
  - **Pace:** an average of 2–6 km/h, with no long stretches above 9 km/h.
  - **Sniff-stops:** short stops of 5–90 seconds, about one every 5 minutes. A 20-minute walk with no stops gets flagged.
  - **GPS path:** continuous and natural, with no teleports. A phone moving with no GPS movement ("a phone on a fan") fails.
  - **Steps and distance agree:** the step cadence matches the distance covered.
- Your dog has a profile with name, breed and photo. A Bluetooth collar tag could add an extra check later.
- If a walk doesn't pass, it **counts as a solo walk**, with no accusation and no penalty.
- **Solo walks and all-day steps still count for everything else:** XP, Bones, cards, the Heist signal race, quests and leagues. They just don't earn Treats.

### Leash energy (the free tier and above)
**1 ⚡ = 1,000 dog-walk steps that earn Treats.** Steps beyond your energy still count for the game.

| Source | Energy |
|---|---|
| Free tier: everyone, every day | **5 ⚡**, about a 45-minute dog walk |
| A leashed Genesis Pup NFT, by rarity: Normal / Rare / Super Rare / Legendary / Much Wow | +2 / +3 / +4 / +5 / +6 ⚡ |
| Staked TREAT, by tier (§8) | +1 to +4 ⚡ |
| **Maximum** | **15 ⚡** |

- A leashed Pup is your real dog's companion.
- A leashed Pup can't be sold or rented. Unleashing takes effect the next day.
- **There's no repair cost and no energy you have to buy.** Energy refills every day for free.

### Walk Points
```
earningSteps = min(verified dog-walk steps, energy × 1,000)
multiplier   = 1 + min(0.5, streak (≤ 0.15) + companion Pup (≤ 0.15) + stake tier (≤ 0.20))
WP           = earningSteps × multiplier × trust
yourShare    = min( walkShare × WP ÷ ΣWP,  0.5% of walkShare )
```
**Example:** 3,120 dog-walk steps × 1.21 = 3,775 WP. Out of 1,290,000 WP in total, that's 0.29% of 135,348, or **≈ 396 Treats**.

## 8. Staking: hold for perks, not interest
Staking **never pays new tokens**. There's no APY, so we never print to keep people staked. It gives you:

| Tier | Staked | Earn boost | Leash energy | Unlocks |
|---|---|---|---|---|
| Leash | 1,000 | +5% | +1 ⚡ | Staker badge |
| Harness | 5,000 | +10% | +2 ⚡ | Golden Bone league |
| Pack Leader | 20,000 | +15% | +3 ⚡ | Diamond Paw league, top-100 prizes |
| Alpha | 50,000 | +20% | +4 ⚡ | Moon league |

- Unstaking takes **7 days**. You get no boost during that time.
- The per-user cap (0.5% of the walk share) still applies, so whales can't take the bowl.

## 9. Where money comes from (real-money sinks)
| Item | Price | Notes |
|---|---|---|
| Heist Pass premium (each season) | Ð 25, or 500 Treats | Mostly cosmetics |
| Fixed-content shop deals (cards, gear, skins) | Ð 8–150, or the Treat price | You always see exactly what you get. A weekly cap applies to power deals |
| Genesis Pup mint (the sale portion of the 500 Pups) | Set before mainnet | A fixed price, not an auction |
| Card NFT mint and the Genesis Forge | DOGE in Phase 1, TREAT or DOGE in Phase 2 | Phase 1 keeps points from turning into tradable items |
| Coach Premium | Ð 10 a month | Covers AI costs |
| Marketplace and rental fee | 5% | Phase 1 is DOGE only |
| **Sponsored walks** | Stablecoins | §10 |

**Random loot boxes and card packs are never sold, for money or for Treats.** They cost Bones you earn by playing.

**Revenue split (DOGE and stablecoins):**

| Share | Phase 1 | Phase 2 |
|---|---|---|
| 50% | TREAT launch reserve | **Buys TREAT on the market and burns it** (weekly, with price-impact limits, on a public dashboard) |
| 40% | Treasury and runway | Treasury and runway |
| 10% | Shelter Fund | Shelter Fund |

**Treat sinks** (spending Treats burns them):
- Pup evolution: 100, 500 or 2,000
- Streak Shield: 50
- Heist Pass: 500
- Cosmetics and training items: 40–400
- Rename: 25
- The forfeited half of instant claims

All of these are **100% burned**. The fee on Treat marketplace sales (Phase 2) is 5%: half is burned and half goes to the Shelter Fund.

## 10. Sponsored walks
- Pet brands and ecosystem apps pay **stablecoins** for themed walks. Examples: a dog-park loop, "five dog walks this week", or a partner's quest.
- **80%** of the money buys TREAT on the market for the Treat Bowl (in Phase 1 it goes to the launch reserve), and **20%** covers operations.
- These are rewards someone else pays for: they add to the bowl without minting anything.
- Sponsors get anonymous, aggregated reach reports. **We never sell location data.**

## 11. Health metrics (shown on a public dashboard)
| Metric | Healthy | What happens if it isn't |
|---|---|---|
| **Burned ÷ minted** (7-day) | ≥ 1.0 over the long run | Below 0.8 for 2 weeks: k drops to 0.8. Below 0.6 for 4 weeks: base is paused. Above 1.2 for 4 weeks: k can go back up, never above 1.0 |
| **Revenue per daily walker** (30-day) | Trending up | Falling for 3 months triggers a public review of pricing, sponsors and features |
| **Claimed instantly vs vested** | More vested is healthier | Shown weekly. If most people claim instantly, holding isn't attractive enough |

Also on the dashboard:
- minted, burned and net issuance
- revenue and buybacks
- the size of the launch reserve
- active verified dog walkers
- the average reward per walker

## 12. Launch carefully (Phase 2)
- **Protocol-owned liquidity:** the launch reserve's DOGE plus the 10% liquidity allocation seed the DEX pool. The LP tokens sit with a timelocked treasury for 4+ years. There's no liquidity mining and no rented LPs that leave once incentives stop.
- **Locked team:** a 1-year cliff, then 3 years linear, enforced on-chain.
- **No presale and no VC allocation at launch.**
- **The long-run target is burns ≥ 100% of emissions**, up from 40% in v1.
- If the launch gate (§3) isn't met, TREAT doesn't launch, and the game keeps running on points.

## 13. Compared with what came before
| | Typical move-to-earn | MuchWalk v1 | **MuchWalk v2** |
|---|---|---|---|
| New tokens per step | Yes, uncapped | No, a fixed pool | No. The pool follows yesterday's inflow |
| Who pays rewards | New players | Mostly new players | **Revenue, sponsors and burns** |
| Burn target | None | 40% | **≥ 100%** |
| Claim and dump | Free | 10% fee, or wait 7 days | **50% burned, or vest 21 days** |
| Need to buy before earning | Yes (NFT) | No | **No.** The free tier covers a daily dog walk |
| Token at launch | Day 1 | Day 1 | **Only after the launch gate** |

## 14. What changes for builders
Phase 1 needs **no token contracts**. It runs on points off-chain, plus GenesisNFT, the market and DOGE payments. That cuts the first build a lot.

For Phase 2:
- **TreatToken:** add a `totalBurned()` counter.
- **RewardsDistributor:**
  - an epoch mint cap of `min(ceiling, base + kMax × burnedLastEpoch)`
  - `claimInstant` (mints 50%, and the rest is never minted)
  - `claimVested` (21-day linear)
  - `exitVesting`
- **TreatStaking:** stake, 7-day unbonding, and tier lookup.
- **Genesis leash lock:** use it to grant energy (the lock already exists).
- **BuybackBurner:** swaps DOGE for TREAT with TWAP and slippage limits, then burns. In Phase 1 it holds the launch reserve instead.
- **SponsorVault:** stablecoin escrow for sponsored walks.

[05-SMART-CONTRACTS](05-SMART-CONTRACTS.md) and [11-BUILD-PLAN](11-BUILD-PLAN.md) will be updated once this model is agreed.

## 15. Open questions
1. Do only verified dog walks earn Treats, or do solo walks earn at a reduced rate?
2. What's the vesting period: 14, 21 or 28 days?
3. Are the launch gate numbers right? Should anything be added?
4. Walkers Drop: yes or no, and is 3% the right size?
5. Allocations: is 45% for walk rewards right with revenue-linked emissions, or should more go to liquidity or ecosystem?
6. Which stablecoin should be accepted on DogeOS for sponsors?

*Not financial advice. Treats in Phase 1 are points with no cash value and can't be redeemed for money. TREAT may never launch if the launch gate isn't met. MuchWalk is an independent community project, not affiliated with or endorsed by DogeOS, MyDoge or Layer 69 Foundation.*
