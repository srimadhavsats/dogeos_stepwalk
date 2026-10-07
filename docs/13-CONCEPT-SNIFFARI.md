# 13 · Concept B: "Sniffari" (meet, befriend and battle dogs on your walks)

> **Status: concept under test.** This doc isn't final like 01–12. The prototype has a **Wild** tab that runs this concept, so the team can try it before choosing.
> The idea came from a co-founder discussion: *walk about 6k steps and you might meet a unique dog. Start with one stock dog, find others in the wild with different classes and power-ups, battle them (friendly, 1v1, PvP), and collect them all.*

## 1. How it looks (the player's day)
1. **Morning:** you open the app, and your stock Shiba is waiting. The **Wild** tab shows today's trail: 2k · 4k · **6k ★** · 9k · 12k steps.
2. **On your walk**, each milestone you pass makes something rustle on the trail.
   - **Encounters wait for you.** You don't have to look at your phone while walking.
   - The **6k ★ "Golden Hour" encounter** is always Rare or better.
3. **After the walk:** you open an encounter and a silhouette turns into a **Labrador (Charmer · Rare)**.
   - You **befriend** it with a trust meter: tap **Offer snack** while the needle is in the green zone.
   - Rarer dogs have a smaller zone and a faster needle.
   - **Snacks** are earned by walking: one per 1,000 steps.
4. **New friends** join your **Kennel**, and their breed lights up in the **Pawdex** (18 breeds in 6 classes).
5. **Evening:** you set a lead dog and go to the **Arena**.
   - **Friendly:** play a friend, with nothing at stake.
   - **Quick 1v1:** fight another walker's saved team.
   - **Ranked (Bark League):** a weekly ladder.
6. **Rare chance:** a Legendary or Much Wow encounter leaves **Genesis tracks**, which enter you in that night's draw for one of the 1,000 Genesis NFTs.

## 2. Classes, stats and power-ups
**Stats:**
- **POW**: damage
- **SPD**: who moves first
- **STA**: HP
- **LCK**: critical hits and befriending
- **SNF**: encounter and item finds, outside battle

| Class | Breeds | Main stat | Beats | Power-up |
|---|---|---|---|---|
| 🛡️ Guardian ("bruiser") | Doberman, German Shepherd, Rottweiler | POW | Tracker | **Guard Stance:** the next hit does only 25% damage |
| 👃 Tracker | Beagle, Bloodhound, Dachshund | SNF | Sprinter | **Sniff Out:** attack with a guaranteed critical hit |
| ⚡ Sprinter | Greyhound, Whippet, Border Collie | SPD | Trekker | **Zoomies:** two quick strikes |
| 🏔️ Trekker | Husky, Malamute, Saint Bernard | STA | Charmer | **Second Wind:** heal 30% of HP |
| 💛 Charmer ("lovable, luck+") | Labrador, Golden Retriever, Corgi | LCK | Guardian ("melts the tough guy's heart") | **Puppy Eyes:** the opponent may skip a turn |
| 🌕 Legend | Shiba Inu, Akita, Samoyed | Balanced | — (neutral) | **Much Wow:** a random big effect |

**Type wheel:** Guardian → Tracker → Sprinter → Trekker → Charmer → Guardian. Each class deals ×1.5 damage to the class it beats and ×0.67 to the class that beats it.

**Rarity changes stats only a little** (Normal ×1.00 up to Much Wow ×1.25). **Level matters more, and dogs level up when you walk with them.** Steps train your dogs, so a player who walks a lot beats a player who only buys.

## 3. Battle v1 (kept simple on purpose)
- 1v1, turn-based. Each turn you choose **Bark Attack**, **Guard**, or **Power-up** (once per battle). SPD decides who acts first.
- `HP = 50 + 1.2 × STA + 3 × level` and `damage = (0.5 × POW + 6) × type × crit × guard × random(0.85–1.0)`.
- **PvP is async:** you fight a snapshot of another player's team, and the server resolves the battle with a committed seed (same pattern as 03 §6). There's no real-time netcode, and results can be verified.
- Tickets come from walking (02 §20). **No token wagering** on battles. Ranked rewards come from the fixed Games pool.
- **Later:** teams of 3, breed-specific moves, and tournaments.

## 4. How it fits what we already designed
| Existing piece | With Sniffari |
|---|---|
| Starter Pup | Your **stock Shiba** (Legend class). It stays your companion for the walk bonus |
| Loot boxes | **Encounters become the daily surprise for dogs.** Boxes stay only for items (Streak and Season Boxes) |
| Genesis 1,000 | Genesis Dogs become **rare variants of breeds** (Galaxy Husky, Golden Doberman, …), found through Genesis tracks → nightly draw. The exact supply cap stays |
| Mini-games | The Arena joins Fetch Frenzy and Derby under Play. All of them use tickets earned by walking |
| Anti-cheat | Encounters come only from **verified** steps. Battles are resolved on the server |

Proposed Genesis split if we adopt this: **600 Dogs (all 18 breeds) · 250 Walkers · 150 Relics** (was 500 / 350 / 150). That's a team decision.

## 5. Risks and how we handle them
- **Pokémon IP:**
  - Don't use "Pokémon", "Pokédex", "-mon" names, ball-shaped items, or the "Gotta catch 'em all" slogan.
  - Nintendo has sued over creature-capture game mechanics (Palworld, 2024). So we **befriend through trust and snacks instead of throwing an item to capture**.
  - Our words are *meet, befriend, Pawdex, Kennel, pack*.
- **Safety:** there are no map spawn points, so nobody is lured to an unsafe place. Encounters come from step counts only and wait up to 24h, so players can stay "eyes up, phone down".
- **Pay-to-win:** rarity adds at most +25% to stats, while levels come from walking. Ranked play uses brackets by level.
- **Gambling optics:**
  - Befriending odds are published.
  - Snacks can't be bought with money.
  - Premium snacks (TREAT burn) work **only on non-Genesis dogs**, and the Genesis draw is free to enter.
- **Scope:** battles are the biggest new build. Ship Friendly and Quick 1v1 first, and Ranked one season later.

## 6. Naming and positioning
**Positioning:** call it **"walk-to-play"**, not "move-to-earn". The move-to-earn label brings STEPN baggage, worse treatment in app reviews, and users who leave when the price drops. The game should be fun even with TREAT at zero.

Shortlist (check domain, X handle and trademark availability before deciding):
| Name | Why |
|---|---|
| **Sniffari** | sniff + safari: a dog-finding adventure. Unique and easy to remember |
| **MuchWalk** | Our current name: pure Doge meme, clearly about walking |
| **Doge Trails** | Simple and native to DogeOS |
| **Kennel Walk** | Shares a brand family with our Kennel launchpad on DogeOS |
| **Fetch Quest** | A gaming pun. Likely already taken, so check first |

Suggestion: put the top 2–3 to a quick poll in the DogeOS community.

## 7. Decisions needed
1. **Concept:** A (loot + Genesis draw), B (Sniffari), or **Hybrid** (recommended: Sniffari for dogs, small boxes for items).
2. The Genesis split (600 / 250 / 150?).
3. Name and positioning.
4. Arena v1 scope: Friendly + Quick first?
