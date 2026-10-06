# 10 · UI/UX & Design System

> The **look-and-feel source of truth is `prototype/index.html`**. Open it in a browser, and copy its tokens and component shapes.
> Style name: **"Sticker Pop"**. It uses chunky rounded cards, thick ink outlines and hard offset shadows (neo-brutalist), a sunny Doge gold, and playful motion. It should feel like a sticker book, not a bank.

## 1. Principles
1. **Joy first:** every completed action gets feedback (haptic, motion, or a "wow").
2. **One glance:** the Home screen answers *"How am I doing today?"* in under 2 seconds.
3. **Crypto invisible until wanted:** no hex addresses or gas talk on core screens. Wallet language only appears in Claim, Tips and Bets.
4. **Kind:** no shaming, no red "failure" screens, and rest is a feature.
5. **Accessible:** meet WCAG 2.2 AA and support Reduce Motion.

## 2. Tokens (`packages/ui-tokens`)
| Token | Light | Dark ("Moon mode") |
|---|---|---|
| `bg` | `#FFF6E5` | `#14112A` |
| `surface` | `#FFFFFF` | `#221D40` |
| `surface2` | `#FFF0CC` | `#2C2652` |
| `text` | `#1F1A33` | `#FFF6E5` |
| `text2` | `#5B5470` | `#B9B2D9` |
| `outline` | `#1F1A33` | `#05040C` |
| `gold` (primary) | `#FFC531` | `#FFC531` |
| `goldDeep` | `#F2A900` | `#F2A900` |
| `shiba` | `#F08A24` | `#FF9A3D` |
| `moon` | `#6C5CE7` | `#8B7CFF` |
| `mint` (success) | `#22C997` | `#2EE6AE` |
| `pink` (cheers) | `#FF5C8A` | `#FF6E98` |
| `sky` (info) | `#3BA7FF` | `#5BB8FF` |
| `danger` | `#FF4D4F` | `#FF6B6B` |

- **Type:**
  - Display: **Baloo 2** (700/800)
  - Body: **Nunito** (400/600/800)
  - Meme words: **Comic Neue** 700, only for "wow" bursts, as a nod to the classic Doge meme
  - Sizes: 34 / 28 / 22 / 17 / 15 / 13
- **Shape:**
  - Radii: cards 24, buttons 18, chips pill
  - Borders: **3 px `outline`**
  - Shadow: `0 5px 0 outline`. Pressed state: `translateY(3px)` and shadow `0 2px 0`
- **Spacing:** 4, 8, 12, 16, 20, 24, 32. Screen gutter 16.
- **Icons:** Phosphor (duotone) plus custom stickers. The prototype uses emoji as stand-ins.

## 3. Motion and feedback
| Moment | Motion | Haptic | Sound (opt-in) |
|---|---|---|---|
| Button press | spring (stiffness 300, damping 18) | light | — |
| Goal reached | ring pulse + confetti 1.2 s + 3 "wow" words | success | bork |
| Level up | full-screen sticker modal, number roll | success | fanfare |
| Walk Block found | rocket zoom + gold shower | heavy | coin |
| Cheer received | bubble pops up from the bottom, auto-dismissed after 4 s | light | chirp |
| Pup idle | blink every 4–6 s, ear twitch, head bob | — | — |

With Reduce Motion on: no confetti, no floating words, no bob. Fades and haptics stay.

## 4. Navigation
Bottom tab bar: **Home · Ranks · [WALK, a big centre button] · Play · Den**.
- **Play** holds the Moon Mission banner and Walk Block feed, then Fetch Frenzy, Doge Derby and Walk Bets.
- **Den** holds your Pup and Walker side by side, plus the Closet (items), Loot, Forge, Genesis NFTs and the Market.
- **Coach Bark** is a floating bubble, bottom-right above the tab bar, on Home, Play and Den.
- Prototype v1 still shows the older tabs (Home · Moon · Walk · Ranks · Pup). The tab bar above is the target.
- The header holds the avatar (Profile, Badges, Settings), the streak flame, and a TREAT chip that opens the Wallet/Claim sheet.

## 5. Screens (prototype shows each one)
| Screen | Must show | States |
|---|---|---|
| **Onboarding** (4 steps) | 1 "Walk. Earn treats. Raise a Shibe." · 2 pick a coat (4 commons) + name your Pup · 3 permission explainer, then the OS prompt (health, notifications) · 4 "Walk first, wallet later" | Permission denied → manual explainer + retry |
| **Home** | Pup card (mood bubble) · steps ring + goal · XP bar + level title · streak + shields · 3 quests + chest · Walk Block ticker · Moon mini-progress · pending treats | Syncing shimmer · "Under review" banner · rest day |
| **Walk** | Mode chips: Walk / Run / Roll / Pack · big Start · active: time, distance, pace, steps, cadence, stylised path · **Go Live** toggle · cheers feed · coach cue line | GPS weak · paused · finished → recap card (meme caption + share) |
| **Pack** | Show my QR / scan a friend · members joined list | QR expired |
| **Moon** | Rocket on the Earth → ISS → GEO → Moon path, with % · community km · my contribution · live Walk Block feed · season timer | Landing party state |
| **Ranks** | League banner (tier, days left) · 30-row cohort with green promote zone and red demote zone (also shown with icons) · tabs: League / Friends / Packs / City | Not placed yet ("walk to join this week's league") |
| **Pup** | Big Pup · stage track (Puppy → Shibe → Doge → Moon Doge) · level + XP · bonus % · Earn Your Leash progress · traits · gear slots · Evolve button (TREAT cost) | At cap → Evolve CTA glows |
| **Coach** | Chat with streaming bubbles · quick replies ("Plan my week", "I'm tired", "Roast my steps 🔥") · goal proposal card (Confirm / No thanks) | Limit reached · napping (spend cap) |
| **Walk Bets** | Challenge cards (stake, pool, participants, days, rule) · my bets with progress · join sheet (stake, rules, "If nobody finishes, shelter dogs win 🐶") | Results pending · claim |
| **Badges** | Trophy grid by category, rarity colours, locked ones shown in grey with criteria | — |
| **Wallet / Claim** | Pending (needs wallet) vs Claimable · "Gasless claim" · connect wallet (Reown) · recent claims | Wrong network |
| **Profile / Settings** | Handle, units, height, Roll Mode, quiet hours, rest/injury mode, data export/delete, privacy links | — |
| **Den** | Walker walking the Pup (animated) · equip slots · Genesis tokens (owned / rented, with expiry chip) · shortcuts to Closet, Loot, Forge, Market | Nothing owned → "Earn your first Genesis in the nightly draw" |
| **Avatar studio** | Base (standing/wheelchair), skin tone, slot tabs, live preview of the Walker and Pup together, locked items show the level that unlocks them | — |
| **Closet** | Items grid filtered by slot and rarity, rarity frame colours (02 §16), shards balance, Collections progress (x/6) | — |
| **Loot opening** | Box shakes → bursts → cards flip one by one, Legendary/Much Wow get a full-screen moment + haptic · "View odds" link on every box · pity meter | Daily limit reached |
| **Forge** | Recipes list, a shard cost bar, Genesis Forge needing a complete Collection + a 2,000 TREAT confirm (shows the burn) | Season Forge sold out |
| **Genesis ticket** | "You won tonight's Genesis Draw!" → reveal kind and rarity → Claim (gasless) → 14-day leash countdown | Ticket expiring soon |
| **Market** | Tabs: Buy · Sell · Trade · Rent. Filters (kind, rarity, price, pay token). Token page: art, traits, Pup level, owner, history, rental status. Sell sheet (price + token + expiry) · Trade builder (pick yours, pick theirs, add TREAT) · Rent sheet (price/day, days, reserved-for friend) | Wrong network · token locked or rented · feature flag off (iOS: "Trade on the web") |
| **Play hub** | Moon banner · block feed · game cards with ticket count · Derby countdown and your heat · Walk Bets | No tickets → "Walk 2,000 steps for a ticket" |
| **Fetch Frenzy** | Phaser canvas in a WebView, 3 lanes, bones counter, combo, end card (score, XP, shards, rank) | Run rejected → "Couldn't verify that run" |
| **Doge Derby** | Entry card (equip Pup by Thu), heat line-up with Pups and league tiers, Sunday replay with cheer buttons, podium + box rewards | Not entered |
| **Spectator** (deep link / web) | Runner's live pace and distance (no map) · cheer buttons · tip sheet | Ended |

## 6. Tone of voice
- Short and warm. **At most one Doge-ism per screen** ("wow", "much", "very", "such", "so").
- Celebrate effort: *"9 days in a row, very consistent 🔥"*, not *"You only walked 3,000 steps"*.
- Rest is good: *"Rest day logged. Your Pup is napping too 💤"*.
- Errors are honest and light: *"Couldn't sync, the sky must be cloudy. Tap to try again."*
- Never say "earn money" or "profit". Say "treats", "rewards", "claim".

| ✅ Do | ❌ Don't |
|---|---|
| "Goal crushed! Much walk. 🎉" | "WOW MUCH SUCH VERY AMAZING!!!" |
| "Under review 🔍 Usually done in 72h." | "Cheating detected." |
| "Connect a wallet to claim your 1,240 treats." | "Sign tx 0x9f… to mint ERC-20." |

## 7. Accessibility
- Contrast ≥ 4.5:1 for text. Touch targets ≥ 44 pt. Support Dynamic Type / font scale up to 200%.
- The ring needs an accessibility label like "6,240 of 8,000 steps, 78 percent".
- League zones use an icon as well as colour (▲ promote, ▼ demote).
- Every animation respects Reduce Motion. Haptics can be switched off in Settings.

## 8. Pup art pipeline
- Layered SVG: `body`, `coat`, `mask`, `eyes`, `markings`, `accessory` slots. Each stage has its own proportions: Puppy has a bigger head and eyes, and Moon Doge adds an astronaut helmet.
- Renderers (`packages/shared/src/pup/render.ts`, `avatar/render.ts`, `relic/render.ts`) produce SVG strings. The 70 Legendary and Much Wow Genesis pieces are hand-drawn SVGs, loaded by token ID.
- The Pup renderer produces the SVG string. It's used by **the API** (NFT image) and **the app** (react-native-svg), so the Pup looks identical everywhere.
- The prototype's `pupSVG()` function is the reference for shapes and colours.
