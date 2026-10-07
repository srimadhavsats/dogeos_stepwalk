# 03 · Tokenomics ($TREAT)

> **Principle:** every reward is a **pro-rata share of a fixed pool**. No mechanic mints "X tokens per step". As a result, emissions can never exceed the schedule, however many users or bots show up.
> All amounts are integers. TREAT has 18 decimals and uses `bigint` (wei) in TS and `uint256` in Solidity. Multipliers are **basis points (bps, 10,000 = 1.0)**. Always use floor division.
> Testnet numbers match mainnet's so the economy can be rehearsed. Testnet TREAT has **no value**. Mainnet uses fresh contracts.

## 1. Token
| Field | Value |
|---|---|
| Name / symbol | MuchWalk Treat / `TREAT` |
| Decimals | 18 |
| Max supply | 1,000,000,000 TREAT (hard cap enforced in `TreatToken`) |
| Standard | ERC-20 + EIP-2612 permit + burnable |

## 2. Allocation
| Bucket | % | Amount | Mechanism |
|---|---|---|---|
| Move-to-Earn rewards | 50% | 500,000,000 | Minted **only** by `RewardsDistributor` on the §3 schedule |
| Community & Shelter | 10% | 100,000,000 | Treasury Safe: Moon Parties, events, shelter donations |
| Ecosystem & partners | 10% | 100,000,000 | Treasury Safe, released by governance |
| Liquidity | 8% | 80,000,000 | DEX liquidity at mainnet launch |
| Treasury / DAO | 10% | 100,000,000 | Timelock + Safe |
| Team | 12% | 120,000,000 | OZ `VestingWallet`: 1-year cliff, then linear over 3 years |

Everything except the Move-to-Earn bucket is minted once at deployment (see `05-SMART-CONTRACTS.md` §3).

## 3. Emission schedule (on-chain)
- **Epoch** = one UTC day. `epochId = floor((timestamp − GENESIS_TS) / 86400)`, where `GENESIS_TS` is a UTC midnight fixed at deploy.
- `E0 = 273_972 × 10^18` (273,972 TREAT per day in year 0).
- `year = epochId / 365`. **`dailyEmission(epochId)`**: start with `b = E0`, then repeat `b = b × 4 / 5` once per year that has passed (floor each step). If `year ≥ 30`, return 0.
  - Year 0 ≈ 100.0M · year 1 ≈ 80.0M · year 2 ≈ 64.0M … The asymptotic total is ≈ 499.99M, which is under the 500M bucket. ✅
- Each epoch can mint **at most** `dailyEmission(epochId)`. Anything not allocated is **never minted**: there is no rollover.
- **Bonus top-ups** (Moon Party, events): the treasury transfers TREAT into the distributor with `fundBonus`. An epoch may then spend up to `bonusBalance` on top of the mint cap.

### Daily budget split
`D = mintedThisEpoch + bonusUsedThisEpoch`, planned off-chain before posting:
| Pool | Share of D | Use |
|---|---|---|
| **W**: Walk rewards | 75% | Pro-rata by Walk Points (§4) |
| **B**: Walk Blocks | 15% | 144 block rewards of `floor(B / 144)` (§6) |
| **Q**: Quests & Leagues | 10% | 70% accrues to the weekly League pool and 30% goes to quest points (§5) |

## 4. Walk Points (per user, per UTC day)
Inputs: `su` is verified step units for the UTC day, after anti-cheat removals. `packSU` is the SU inside verified pack sessions, and `packSize` is the largest verified pack size that day.

```
base      = min(su, 10_000) + floor(max(0, min(su, 20_000) − 10_000) / 2)      // max 15,000
packBps   = {2: 2000, 3: 3000, 4: 4000, ≥5: 5000}[packSize] or 0
packExtra = floor(min(packSU, 10_000) × packBps / 10_000)
compBps   = min(3_000, 40 × equippedPupLevel + rarityBps)  // ≤ +30%; rarityBps from 02 §10 (starter 0)
streakBps = min(2_500, 100 × streakDays)                 // ≤ +25%
multBps   = floor((10_000 + compBps) × (10_000 + streakBps) / 10_000)  // ≤ 16,250
trustBps  = trust score in [0, 10_000] from 07-ANTI-CHEAT
WP        = floor((base + packExtra) × multBps × trustBps / 10^8)
```
- Users with `trustBps < 2_000` get WP = 0. The UI shows "Under review 🔍" with no accusation.
- **Per-user cap:** `reward_walk = min( floor(W × WP / ΣWP), floor(W × 50 / 10_000) )`, which caps any single user at 0.5% of W. The excess is not redistributed, so it is simply never minted.
- If `ΣWP = 0`, then W is not minted.

## 5. Quests & Leagues pool (Q)
- `Qq = floor(Q × 25 / 100)` is split pro-rata by **quest points** (easy 1, medium 2, hard 3).
  - The UI shows quest TREAT as "≈ estimate" until the epoch posts.
- `Qg = floor(Q × 20 / 100)` accrues into `gamesPool`. It pays the weekly Fetch Frenzy top 100 (02 §20) in the **Monday epoch**.
- `Ql = Q − Qq − Qg` (55%) accrues into `leaguePool`. The **Monday epoch** pays out the previous week's league ranks (`02-GAME-DESIGN.md` §8) from the accrued pool. Ineligible or unclaimed shares stay in the pool for next week.
  - This is off-chain accounting. Only the final per-user totals go into the Merkle tree.

## 6. Walk Blocks (Proof-of-Walk mining)
- **Windows:** block `k ∈ [0, 143]` of epoch `e` covers `[GENESIS_TS + e×86400 + k×600, +600)` UTC. Global block number = `e × 144 + k`.
- **Hashes:** `hashes(u, k) = floor(min(SU of u in window k, 2_000) × trustBps / 10_000)`, and only for users with `trustBps ≥ 5_000`. SU comes from minute buckets (07 §2).
- **Finality:** a window is final 6 hours after it closes. Epoch `e` is built at **06:30 UTC on day e+1**.
- **Randomness (commit–reveal + L2 entropy):**
  1. When posting epoch `e−1`, we include `seedCommit[e] = keccak256(secret[e])`, where `secret[e]` is 32 random bytes from KMS/CSPRNG.
  2. When posting epoch `e`, we reveal `secret[e]` in the epoch metadata file.
  3. `entropy[e]` = the hash of the **first DogeOS block with timestamp ≥ end of day e + 6h**.
  4. `r(k) = uint256(keccak256(abi.encode(secret[e], e, k, entropy[e])))`.
- **Draw:** sort participants of block k by `participantKey` ascending (lowercase wallet address, or `acct:` + sha256(accountId) for users without a wallet). Build cumulative hashes, set `target = r(k) mod totalHashes(k)`, and pick the first participant whose cumulative sum is greater than `target`.
- **Reward:** `floor(B / 144)` goes to the finder. If `totalHashes(k) = 0`, the block is **orphaned** and its reward is never minted.
- **Transparency:** publish `epochs/{e}/blocks.json` (participants, hashes, winners, secret, entropy) to public storage and record its sha256 in the epoch metadata. Anyone can re-run the draw. The script is `packages/shared/src/blocks/verify.ts`.

## 7. Moon Party and other bonus events
- On a Moon landing, the treasury calls `fundBonus(dailyEmission(e+1))`, and epoch `e+1` uses the bonus, so D is doubled. Other events (holidays, partner days) work the same way. Bonus spending is always bounded by `bonusBalance`.

## 8. Users without a wallet ("walk first, wallet later")
- Allocations accrue off-chain in `pending_rewards` against the account. They are **not minted** until a wallet is linked.
  - When a wallet is linked, the next epoch adds that account's pending total to the address's cumulative leaf.
- Pending rewards for accounts that never link a wallet **expire after 180 days** and are never minted.

## 9. Claiming
- Claims use a cumulative Merkle tree: one leaf per address, `(account, cumulativeAmount)`. Claiming pays out `cumulative − alreadyClaimed`.
- `claim(account, cumulative, proof)` is **permissionless**, because the tokens always go to `account`. That lets our relayer run **gasless batched claims** with no user signature at all.

## 10. Sinks (testnet prices; final prices set by governance)
| Sink | Price (TREAT) | Destination |
|---|---|---|
| Pup evolve (→ Shibe / Doge / Moon Doge) | 100 / 500 / 2,000 | burn |
| **Genesis Forge** (plus a consumed item Collection) | 2,000 | burn |
| Streak Shield (max 1 per week) | 50 | burn |
| Item shop (Normal / Rare cosmetics only) | 40–400 | 50% burn · 50% treasury |
| Create a Pack | 200 | burn |
| Coach Premium (+50 msgs/day for 30 days) | 300 | 50% burn · 50% treasury (pays AI costs) |
| Name tag / rename | 25 | burn |
| Battle pass premium (per season) | 500 | burn |
| Walk Bet fee | 10% of the **forfeited** stakes | 5% burn · 5% Shelter Fund |
| Cheer tip fee | 2% of the tip | Shelter Fund |
| **Market sale fee** (TREAT or DOGE) | 5% of price. This is the only fee in our market; on other marketplaces the ERC-2981 royalty (5%) goes to the Shelter Fund | TREAT: 2.5% burn · 2.5% Shelter Fund. DOGE: 2.5% treasury · 2.5% Shelter Fund |
| **Rental fee** | 5% of rent | Same split as sales |
| **Genesis mint sale** (mainnet only, 150 NFTs) | Price set by governance before mainnet | 70% treasury · 30% Shelter Fund |

Every TREAT sink except market and rental fees runs through **`TreatSink.spend(amount, purpose, ref)`** (05 §2.7). The contract applies the split for each purpose and emits an event, and the indexer credits the off-chain action (evolve, shield, shop item, forge, pack, coach premium, rename, battle pass).
**Loot boxes and game tickets are never sold**, for money or for TREAT.

**Health target:** burned ÷ minted ≥ 40% by month 6 of mainnet. If the ratio stays below 25% for 4 weeks, governance raises sink prices or lowers W's share.

## 11. Walk Bets math (enforced in `WalkBetPool`)
For one challenge: `S` = stake, `N` = participants, `Wn` = winners, `L = N − Wn`.
```
F            = L × S                        // forfeited
fee          = F × 1_000 / 10_000           // 10%
burnAmt      = fee / 2
shelterAmt   = fee − burnAmt
distributable= F − fee
perWinner    = S + distributable / Wn       // for Wn > 0
dust         = distributable − (distributable / Wn) × Wn   → Shelter Fund
If Wn == 0:  all of F → Shelter Fund (no burn); badge 703 for all
If cancelled: every participant gets S back
```
Challenge limits (testnet): `S ∈ [10, 1_000]` TREAT, `N ∈ [2, 500]`, duration 3–30 days, results posted no earlier than end + 6h, and a 24h dispute window.

## 12. Parameters table (`packages/shared/src/econ/params.ts`)
`E0, DECAY_NUM=4, DECAY_DEN=5, MAX_YEARS=30, SPLIT_W=7500, SPLIT_B=1500, SPLIT_Q=1000, Q_QUEST_SHARE=25, Q_GAMES_SHARE=20, COMP_CAP_BPS=3000, MARKET_FEE_BPS=500, RENT_FEE_BPS=500, BLOCKS_PER_DAY=144, BLOCK_SECONDS=600, BLOCK_HASH_CAP=2000, BLOCK_FINALITY_S=21600, USER_CAP_BPS=50, TRUST_MIN_REWARD=2000, TRUST_MIN_BLOCKS=5000, PENDING_EXPIRY_DAYS=180, BET_FEE_BPS=1000, TIP_FEE_BPS=200`.

## 13. ⚠️ Before mainnet (needs a human, not code)
Get legal review covering: token classification; Walk Bets (contest and skill-game rules vary by jurisdiction); Walk Blocks and the Genesis Draw as free-entry prize draws; loot boxes (earned only, odds published, but some prizes are tradable); the NFT marketplace and rentals; tipping and money-transmission; and health-data law (GDPR Art. 9 and others). Geo-fence features where needed. These are flagged for counsel, and these docs are not legal advice.

## 14. Anti-death-spiral safeguards (why TREAT is not built to be "down only")
**What killed STEPN's GST:**
- Every step minted new GST, with no cap. More users meant more printing.
- New users had to buy sneaker NFTs to earn, so demand depended on a constant stream of newcomers.
- Rewards were fixed in tokens regardless of price. When growth stopped, sell pressure had no floor.

| Lever | Rule | Effect |
|---|---|---|
| **Fixed daily pool** (§3) | Steps earn a *share* of the pool, never newly minted tokens per step. The pool shrinks 20% a year, and anything not allocated is never minted | More users or bots never means more printing |
| **Emission circuit breaker** | Every week the epoch planner checks the 7-day burned ÷ minted ratio. Under 25%, next week's mint is cut 15%. Each further week under 25% cuts it another 15%, down to a **floor of 40% of the schedule**. The cut is lifted once the ratio is above 35% | Issuance follows real demand automatically. It's off-chain policy: the contract only ever allows minting *less* than its cap |
| **Revenue buyback and burn** | **50% of protocol revenue in DOGE** (DOGE market fees, mint sale, sponsor quests, battle pass, B2B challenges) buys TREAT on the DEX every week and burns it. A public dashboard shows it | Demand from outside the system, not from new players |
| **Treat Jar (lock for perks, no yield)** | Lock claimed TREAT for 30, 90 or 180 days. You get cosmetics, +5/10/15% XP and higher coach limits, but **never more TREAT** | Less circulating supply without paying people to stay |
| **Patient claim** (decide before C-02 is built) | Claimers choose: **instant** with a 10% fee (burned), or **free** but unlocked after 7 days. This needs a small RewardsDistributor change | Softens the daily "claim and dump" and adds a sink. A sell fee alone could be bypassed by trading on any other DEX |
| **Bones (soft currency)** | Most everyday rewards are **Bones**: off-chain, can't be traded, and spent in the app on snacks, cosmetics and rerolls. Only the pool share is TREAT | Fewer tokens to sell, and nothing tradable that can crash in price the way GST did |
| **Spend reasons that aren't "earn more"** | Cosmetics, battle pass, Pup evolution, Walk Bet stakes, tipping, Arena seasons, sponsored challenges | People spend TREAT for fun and status, not only to farm |
| **Supply hygiene** | No private or VC sale. Team tokens unlock only after a 1-year cliff (then 3-year linear). LP tokens are burned at launch (like our Kennel launchpad). The treasury keeps **24 months of runway in DOGE/stables** so the team keeps shipping through a bear market | No cliff dumps, no rug-pulled liquidity |
| **Health metrics in public** | A live dashboard of minted, burned, net issuance, revenue, buybacks, active earners and rewards per user | Trust comes from showing the numbers |

**What this can't promise:** no token design can guarantee the price. These rules remove the *mechanical* reasons STEPN-style tokens fall. Everything else depends on the product being fun with TREAT at zero.
