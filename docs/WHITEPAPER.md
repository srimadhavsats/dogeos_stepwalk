# MuchWalk Whitepaper

> **Draft v0.2 · October 2026 · for discussion.** MuchWalk is an independent community project building on DogeOS. It is not affiliated with or endorsed by DogeOS, MyDoge or Layer 69 Foundation. Everything described here is in design or prototype, and every number is a proposal.
> Economy details: [Tokenomics](TOKENOMICS.md) · Try it: [clickable prototype](https://srimadhavsats.github.io/dogeos_stepwalk/)

## Summary
MuchWalk is a game for people who walk their dogs.
- Every verified dog walk fills a shared daily **Treat Bowl**, grows your Pup companion and earns cards for your crew.
- Walks also push your faction up the weekly race.
- Around that sit the things that keep people coming back: streaks, leagues, card battles, mini-games, friends cheering you on live, and an AI coach with a sense of humour.

The economy is built so it doesn't repeat what happened to earlier move-to-earn tokens:
- **Rewards follow real money.** Each day's rewards are sized by yesterday's spending and revenue.
- **Paid items are priced in DOGE or stablecoins.** Half of that revenue buys back and burns the token.
- **Sponsors pay for themed walks.**
- **Taking rewards early costs half. Waiting costs nothing.**

And we start with **points, not a token**. TREAT launches only after the app has proven real revenue and real retention.

## 1. Why this, and why now
- **Dog owners already walk every day.** It's one of the most reliable daily habits there is, and nobody needs convincing to start. We don't have to create the habit, just make it more fun and more social.
- **Move-to-earn proved demand and then broke its economy.** Those tokens printed rewards per step and relied on new players to buy them. When growth slowed, prices only went down. We keep the fun parts and fix the money parts.
- **DogeOS gives Doge a home on-chain.** Fast, cheap transactions paid in DOGE, a community that loves dogs, and a wallet (MyDoge) people already use. A dog-walking game fits that community naturally.
- **Fitness apps are lonely and dull.** Ours has a dog with a personality, friends who cheer, a crew to fight for and loot to open.

## 2. How it works
1. **Walk your dog** with the app. It runs a quick check that it was a real dog walk (§3).
2. **Fill the Treat Bowl.** Your verified steps earn a share of the day's shared reward pool.
3. **Level up:**
   - Your Pup companion grows.
   - You earn cards and gear.
   - Your faction climbs the weekly race.
   - Quests, streaks and leagues move forward.
4. **Play:** card battles, the Fat Cat Vault, mini-games, the Wild.
5. **Choose how to take rewards:** half now, or all of it over 21 days.

All your steps during the day still count for XP, cards, quests and the faction race. Only dog walks earn Treats.

## 3. Walking a real dog
**The dog-walk check** runs when a walk ends:
- **Session length:** at least 10 minutes.
- **Pace:** dog-walking pace of 2–6 km/h.
- **Sniff-stops:** dogs stop to sniff every few minutes, and a fake walk doesn't.
- **GPS path:** continuous and natural.
- **Steps and distance agree.**

A phone strapped to a fan or a car fails. A walk that doesn't pass simply counts as a solo walk: no accusation, no penalty.

**Your dog's profile** holds its name, breed and photo. Your Pup companion carries your dog's name, and a Genesis Pup NFT can be its collectible companion.

**Privacy:**
- Step counts come from Apple Health or Health Connect.
- GPS is used only during walks you start.
- Your map is never public. Friends see your pace, never your route.
- Sponsors only see anonymous totals.

## 4. The game
- **Your Pup and Walker:** a dog companion that evolves (Puppy → Shibe → Doge → Moon Doge), plus a Walker avatar with a closet of unlockable items.
- **Pack Battles, the card game:**
  - Dog cards come in Bronze, Silver, Gold (Basic, Challenge, Premium) and Diamond.
  - They level to 100 and fuse up to F10.
  - Gear goes from Common to Legendary, and support cards can also be fused.
  - Battles are 5v5, with league caps so paying can't buy a win.
  - Battles are friendly. Dogs that lose get tuckered out and nap.
- **The Grand Heist factions:**
  - Players join the **Demolition Dogs**, **Kernel Crew** or **Barkitects**. These are the factions from the DogeOS Grand Heist story, used as a community concept.
  - Each faction has its own powers, weaknesses and missions.
  - Factions race each other on total steps every week.
  - Everyone can break into the **Fat Cat Vault**, 10 floors guarded by cartoon cats in suits.
  - **Squirrels** stand for distractions, and they make dogs lose a turn.
- **The Wild:** meet dogs on your route, build trust with them, fill an 18-breed Pawdex and add them to your crew.
- **Mini-games:** Fetch Frenzy and the Doge Derby. Tickets come only from walking.
- **Social:**
  - Go Live on a walk so friends can cheer in real time.
  - Tips in DOGE.
  - Pack walks with friends.
  - Walk Bets (stake-free challenges until TREAT launches).
- **Progress:**
  - Daily quests and streaks with Streak Shields.
  - Weekly leagues from Kibble to Moon.
  - Badges, plus a community "walk to the Moon" goal (384,400 km).
- **Loot:** loot boxes are **earned only, never sold**, with published odds.

## 5. Coach Bark, the AI coach
Coach Bark is a cheerful AI coach that knows your walking history:
- It suggests realistic goals, plans walks around your day and nudges you at the right moment.
- It celebrates your dog's milestones.
- It's funny on purpose ("much stride, very proud").
- It never gives financial advice.
- It runs on a modern Claude model, with strict limits on cost and content.

The premium tier (Ð 10 a month) covers the AI costs.

## 6. The economy in brief
The full model is in [Tokenomics](TOKENOMICS.md).

| Piece | How it works |
|---|---|
| **Phase 1: Points First** | Treats are in-app points with no money value. Treats only buy things that stay in your account. Anything tradable is priced in DOGE |
| **Treat Bowl** | Each day's rewards ≈ 90% of yesterday's spending and revenue, plus a small base, under a hard ceiling. When walking slows, minting slows |
| **Real-money items** | The Heist Pass, shop deals and the Genesis Pup mint are priced in DOGE or stablecoins. 50% of that revenue buys back and burns TREAT (or saves for launch liquidity in Phase 1) |
| **Claim with commitment** | Instant: you get 50% and 50% is burned. Vested: you get 100% over 21 days |
| **Staking** | Boosts your earn rate (up to +20%), adds leash energy and unlocks the top leagues. **No interest is ever paid** |
| **Leash energy** | A free daily tier covers about a 45-minute dog walk. A leashed Genesis Pup or staked TREAT raises it |
| **Sponsored walks** | Pet brands and ecosystem apps pay stablecoins. That money tops up the bowl without minting |
| **Launch** | TREAT has a 1B hard cap. It launches only after the launch gate, with protocol-owned liquidity, a locked team and no presale. The long-run goal is burns ≥ mints |

## 7. NFTs
- **1,000 Genesis NFTs, ever:** 500 Pups, 350 Walkers and 150 Relics, in rarities from Normal to Much Wow.
  - They come from the nightly Genesis Draw (earned entries), the Forge, and a small fixed-price mint sale in DOGE.
  - A Genesis Pup can be **leashed** to your dog's profile for extra energy. A leashed Pup can't be sold or rented.
- **Cards** stay in your account until you choose to **mint** them as NFTs. The first 1,000 Diamonds minted get a Founders foil.
- **Trade, rent and lend:**
  - The market supports buying, selling, swaps and rentals (ERC-4907): the owner keeps the NFT, and the renter uses it for a while.
  - Phase 1 is DOGE only.
  - A 5% fee is split between the treasury or burns and the Shelter Fund.

## 8. Fair play and security
- **Anti-cheat:**
  - the dog-walk check
  - device and motion signals
  - per-user caps (no one takes more than 0.5% of the walk share)
  - a trust score that quietly removes suspicious steps
  - Walk Blocks drawn with public, re-runnable randomness
- **Contracts:**
  - OpenZeppelin v5.
  - Admin is a multisig with a timelock.
  - Minting is capped on-chain both by the ceiling and by last epoch's burns.
  - Claims use a cumulative Merkle tree with gasless batching.
  - Two independent audits before TREAT launches.
- **Openness:**
  - A public dashboard of minted, burned, revenue, buybacks, reserve and walkers.
  - Open-source contracts.
  - Every epoch's data is published so anyone can check it.
- **Keys:** we never ask for seed phrases. You can walk first and connect a wallet later.

## 9. Technology
| Layer | What we use |
|---|---|
| Chain | DogeOS (Chikyū testnet now, chain 6281971), with DOGE as gas |
| Contracts | Solidity with Foundry and OpenZeppelin v5. TreatToken, RewardsDistributor, TreatStaking, GenesisNFT, BadgeSBT, MuchMarket, RentalHouse, BuybackBurner, SponsorVault |
| Backend | TypeScript (Hono), Postgres, Redis, BullMQ and viem. A daily epoch planner and the anti-cheat pipeline |
| Apps | A mobile app (Expo / React Native) and a web app (Next.js with wagmi), with MyDoge, MetaMask and WalletConnect |
| Games | Phaser web games with deterministic replays checked on the server |
| AI | Coach Bark on the Claude API, with cost caps and safety filters |

## 10. Roadmap
| Stage | What ships |
|---|---|
| **0 · Prototype** (now) | Clickable prototype builds v1–v6, game design, tokenomics v2 |
| **1 · Testnet beta** | Dog-walk check, Treats as points, Genesis NFTs and the market on Chikyū, a DOGE shop (testnet DOGE), Pack Battles, the Heist factions |
| **2 · Public launch (Points First)** | Mobile and web apps, real DOGE revenue, a sponsored-walk pilot, the public health dashboard |
| **3 · Launch gate review** | 90 days of revenue, 5,000+ weekly dog walkers, simulated burns ≥ mints, two audits |
| **4 · TREAT** | Token launch with protocol-owned liquidity, commitment claims, staking and buyback-and-burn |
| **5 · Grow** | Pet-brand and insurer partners, a deeper MyDoge integration, new games and seasons |

## 11. Risks we take seriously
- **Nobody walks for the game.** Then no token design matters. That's why we prove retention with points first.
- **Fake walks.** The dog-walk check, energy caps and per-user caps limit what a cheater can take, and a failed check costs honest users nothing.
- **Regulation.** We get legal review for the token, the points, sponsored rewards, the marketplace and health data before launch. Loot boxes are never sold.
- **Too few sponsors.** The bowl still works without them, with sponsors only adding on top.
- **Partner IP.** The Heist faction names belong to their owners. We use them only as a community concept, always with a clear not-affiliated notice, and never imply the project is official.

## 12. Who builds it
MuchWalk is built by **srimadhavsats**, who also built Kennel (a token launchpad on the DogeOS testnet). It's built in public: every prototype build stays online, and the code and docs are open on GitHub.

*Not financial advice. Treats in Phase 1 are points with no cash value. TREAT may never launch if the launch gate isn't met. Product details may change. MuchWalk is an independent community project, not affiliated with or endorsed by DogeOS, MyDoge or Layer 69 Foundation.*
