# 01 · Vision & Innovations

## 1. One-liner
**MuchWalk turns everyday movement into a Dogecoin-native game.** Your steps mine blocks, your Shiba grows, your pack walks with you, and the community walks to the Moon together.

## 2. Why now and why DogeOS
- DogeOS opened its public **Chikyū testnet on 2026-09-30**. It is EVM-compatible and uses **DOGE as gas**. There are very few consumer apps on it yet, so the first fun, daily-use app can become the ecosystem's flagship.
- The Doge community already has a culture of **tipping, memes, charity and "to the moon"**. Every core mechanic here borrows from that culture, so none of it feels bolted on.
- Earlier move-to-earn apps (2022) died from **fixed-rate emissions plus pay-to-play NFTs**: hyperinflation, followed by a death spiral. We fix that at the design level (see §5).

## 3. Who it's for
| Persona | Wants | Hook |
|---|---|---|
| **Doge holder** (core, testnet) | Something fun to *do* with DOGE on DogeOS | Walk Blocks, tipping, Moon Mission, Pioneer badge |
| **Casual walker** (growth) | Motivation, streaks, a cute pet | Pup, streaks, leagues, AI coach, no wallet needed on day 1 |
| **Runner** | Training structure, social proof | Coach plans, Cheer Lane, Walk Bets |
| **Friend groups / clubs** | Shared goals | Packs, Pack Walks, pack leaderboards |
| **Wheelchair users** | Inclusion | Roll Mode: pushes count the same as steps |

## 4. The innovations (what to tell people)

### 4.1 Proof-of-Walk Mining: "your steps are your hashrate" ⭐ flagship
- The day is split into **Walk Blocks** of 10 minutes each, 144 per day. Every verified step taken inside a block's window is one "hash" for that block.
- One **block finder** is drawn per block, weighted by hashes (capped per user, so whales can't dominate). The finder wins the block reward and gets a "block found" moment in the app.
- A live **block feed** ("Block #48,213 found by @sesame_sprint · 1,284 hashes · much luck") turns a solo walk into a shared, live, Dogecoin-flavoured event.
- Blocks finalize **6 hours after the window closes**, which leaves room for late syncs. The draw seed is committed in advance and can be verified afterwards (spec: `03-TOKENOMICS.md` §6).
- **Why it's new:** no move-to-earn app has framed movement as *mining*. For a Dogecoin audience it explains itself instantly.

### 4.2 Moon Mission: a community walk to the Moon
- Each season, the global community's verified distance moves a rocket from Earth → ISS (408 km) → GEO (35,786 km) → **Moon (384,400 km)**.
- Each checkpoint gives every contributor a soulbound badge. The landing gives all contributors a **Moon Lander** commemorative NFT plus a 24-hour **Moon Party** (2× walk rewards).
- Progress is posted on-chain with every daily epoch, so anyone can check it. This is the "to the moon" meme turned into real effort.

### 4.3 Cheer Lane: live tips read aloud mid-run
- A runner flips **Go Live**. Friends get a push notification, see live pace and distance (never the map), and send free emoji cheers or real tips in TREAT or DOGE.
- **Coach Bark speaks each tip into the runner's earbuds**: *"Wow! sesame_sprint tipped you 10 treats: 'go go go!'"*
- This takes Dogecoin's tipping culture and makes it real-time. Tip messages are moderated before they're spoken (see `09-SECURITY.md`).

### 4.4 Pack Walks: verified real-world social walking
- Two to eight friends start together by scanning one member's **Pack QR**. The server confirms their GPS tracks overlapped (≥70% of points within 30 m at the same time).
- The reward is a multiplier of up to **1.5×** on the steps walked together, plus pack XP.
- **Double duty:** mutual witnesses raise each walker's anti-cheat trust score. The social feature *is* part of the security model.

### 4.5 Walk Bets: stake on yourself
- You join a challenge (for example "7 days × 8k steps") by staking TREAT. People who finish split the stakes of people who don't, after a 10% fee.
- Commitment contracts are a well-studied behavioural-economics tool: putting something at stake helps people stick with a goal.
- **Rewards here come from quitters, not from inflation.** The yield is real.
- **If nobody finishes, the whole pool goes to the Shelter Fund.** "The shelter dogs win."

### 4.6 Earn Your Leash: free to play, scarce to own
- Every account gets a **free companion Pup and Walker avatar** that live in the app (off-chain). There's no paywall, unlike sneaker-NFT models.
- The tradable layer is the **Genesis Collection: exactly 1,000 NFTs**, capped on-chain (§4.11).
- Any Genesis NFT earned through play has a **14-day leash lock** before it can be sold or rented. Farming bots can't flip drops quickly.

### 4.7 Walk first, wallet later
- On day 1 users install the app, pick a Pup coat, and walk. Rewards build up as **pending treats**.
- They connect a wallet (MyDoge, MetaMask, or any WalletConnect wallet) only when they want to claim. This removes the biggest drop-off point in crypto onboarding.

### 4.8 Roll Mode: inclusive by default
- Wheelchair pushes (HealthKit `pushCount`, Health Connect `WheelchairPushesRecord`) convert to Walk Points 1:1. They have their own badges and their own anti-cheat thresholds.

### 4.9 Coach Bark: an AI coach with personality
- Coach Bark chats in light Doge-speak, builds adaptive daily goals and weekly plans, and gives safety-aware advice.
- **Cue packs:** at the start of a session the coach generates around 12 short motivational lines once. The app plays them offline at km splits and pace changes, so there's no latency and very little cost.
- **Meme recaps:** after each walk the coach writes a Doge-meme caption, and the app renders a shareable stats card. This drives organic growth.

### 4.10 Shelter Fund: Doge's charity DNA
- Walk Bet pools that nobody finishes, part of the shop revenue, and opt-in "round-up" tips all go to dog shelters. Recipients are chosen by community vote (Snapshot first, on-chain later).
- **Shelter Pups:** limited-edition Pups whose mint proceeds go straight to shelters (mainnet).

### 4.11 Genesis Collection: 1,000 NFTs, ever
- The hard cap is **1,000**, split into **500 Pups, 350 Walkers and 150 Relics** (legendary gear). Each is graded **Normal, Rare, Super Rare, Legendary or Much Wow (mythic)**.
- They're released over 4 seasons, mostly **earned rather than sold**: loot drops, Forge crafting, achievements, a small mint, and 50 Shelter Pups whose sale proceeds go to dog shelters.
- **Owning one gets you:**
  - a unique look for your Pup or Walker
  - a capped walk bonus (Pups only)
  - perks in the mini-games
  - bragging rights on every leaderboard

### 4.12 You *and* your dog: Walker avatars
- Everyone has a **Walker**, a customisable player avatar shown walking their Pup on the Home screen, in leagues, Pack Walks and games.
- It includes a **wheelchair base option** (Roll Mode) and 6 skin tones.
- Items unlock **gradually**: one per level, more from loot boxes and the Forge.

### 4.13 Loot boxes you earn by walking
- Boxes come from **daily goals, quest completion, streaks and seasons, or are forged from duplicate items**. **Boxes are never sold**, for money or for TREAT.
- Odds are published in-app, rolls are verifiable (the same commit-reveal as Walk Blocks), and there's a pity timer. A rare roll gives a **Genesis Ticket**, which lets you claim a Genesis NFT.

### 4.14 Market: sell, trade, rent
- **Sell** at a fixed price in TREAT or DOGE.
- **Trade** NFT-for-NFT with a friend in one atomic swap.
- **Rent** (lend) an NFT for a few days: the borrower gets the Pup's bonus and game perks, while the owner keeps the NFT and earns rent. This uses ERC-4907, so there's no collateral and nothing can be stolen.
- 5% of every sale or rental goes to the Shelter Fund and the burn.

### 4.15 Walk-to-play mini-games
- **Fetch Frenzy:** an endless runner where your Walker and Pup dash through Doge City collecting bones.
- **Doge Derby:** a weekly Pup race. Speed comes from your *real* verified steps that week, and your Pup's rarity adds flair.
- Game tickets are **earned by walking** (1 per 2,000 steps), so the games pull people outside instead of keeping them on the couch.
- Any DogeOS game can show your Genesis NFTs through our public **Pup Passport API**.

## 5. Why our economy won't death-spiral
| Classic M2E failure | MuchWalk design |
|---|---|
| Fixed tokens per step means emissions grow with users | **Fixed daily budget** shared pro-rata, so emissions never exceed the schedule |
| You must buy an NFT to earn | Free in-app Pup and Walker. Genesis NFTs give a **capped** companion boost (≤ +30% in total) plus cosmetics, and can be rented cheaply |
| NFT supply inflates forever | **1,000 Genesis NFTs, hard-capped on-chain**. Everyday items stay off-chain |
| No sinks | 10+ sinks through one TreatSink: evolution, Genesis Forge, shields, shop items, packs, coach premium, bets fee, market and rental fees |
| Bots and GPS spoofing | OS step counters + device attestation + trust score + Pack witnesses + capped per-user rewards |
| Only yield is inflation | Walk Bets pay out from quitters' stakes, not new emissions |

## 6. Also in scope (beyond the brief)
- **Seasons and a battle pass** (free track plus a TREAT-burn premium track) that line up with each Moon Mission.
- **Referrals with anti-sybil protection:** the referrer earns only after the referee's Pup reaches level 5.
- **Wearables:** Apple Watch and Wear OS come in automatically through HealthKit / Health Connect. Garmin and Fitbit are Phase 4.
- **Bring your real doggo:** tag a walk with your real dog's profile and photo for cosmetic badges ("Walked Biscuit 100 times").
- **City and pack leaderboards** at coarse location only (opt-in, H3 resolution 5, about 250 km²).
- **Partner quests** (Phase 4): walk to a partner café or event and check in.

## 7. Success metrics (testnet)
- D1 / D7 / D30 retention ≥ 45% / 25% / 12%
- ≥ 60% of DAU meet their daily goal, and median streak ≥ 4 days
- Cheat-flag rate under 3% of reward volume, with zero contract incidents
- At least one Moon checkpoint (GEO) reached in season 1
