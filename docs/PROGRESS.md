# Progress Tracker

Statuses: `TODO` · `DOING` · `DONE` · `BLOCKED (reason)`. Update the row when a task finishes, and add a one-line note.

| ID | Task | Tier | Depends | Status | Note |
|---|---|---|---|---|---|
| P0-01 | Monorepo scaffold | 🟢 | — | TODO | |
| P0-02 | Verify chain + EVM probe | 🟢 | P0-01 | TODO | needs faucet DOGE (human) |
| P0-03 | CI pipelines | 🟡 | P0-01 | TODO | |
| P0-04 | Shared core formulas | 🟡 | P0-01 | TODO | |
| P0-05 | UI tokens | 🟢 | P0-01 | TODO | |
| T-01 | Tokenomics simulator | 🟡 | P0-04 | TODO | |
| C-01 | TreatToken | 🟡 | P0-02 | TODO | |
| C-02 | RewardsDistributor | 🔴 | C-01 | TODO | |
| C-03 | GenesisNFT (1,000 cap, rentals) | 🟠 | C-01 | TODO | |
| C-04 | BadgeSBT | 🟢 | P0-02 | TODO | |
| C-05 | WalkBetPool | 🔴 | C-01 | TODO | |
| C-06 | CheerRouter | 🟡 | C-01 | TODO | |
| C-09 | MuchMarket (sell + swap) | 🟠 | C-03 | TODO | |
| C-10 | RentalHouse (ERC-4907) | 🟠 | C-03 | TODO | |
| C-11 | TreatSink | 🟡 | C-01 | TODO | |
| C-07 | Deploy + export | 🟡 | C-02…C-06, C-09…C-11 | TODO | |
| C-08 | Contract security pass | 🔴 | C-07 | TODO | |
| B-01 | API + worker skeleton | 🟢 | P0-04 | TODO | |
| B-02 | DB schema + seed | 🟡 | B-01 | TODO | |
| B-03 | Auth + attestation | 🟠 | B-02 | TODO | |
| B-04 | Activity ingest + sessions | 🟡 | B-03 | TODO | |
| B-05 | Anti-cheat engine | 🔴 | B-04 | TODO | |
| B-06 | Game engine | 🟡 | B-05 | TODO | |
| B-07 | Leagues + leaderboards | 🟡 | B-06 | TODO | |
| B-08 | Epoch pipeline + claims | 🟠 | B-06, B-07, C-07 | TODO | |
| B-09 | Moon Mission + ticker | 🟡 | B-08 | TODO | |
| B-10 | Chain indexer + monitor | 🟡 | C-07 | TODO | |
| B-11 | Coach Bark service | 🟠 | B-06 | TODO | |
| B-12 | Walk Bets backend | 🟡 | B-08, B-10 | TODO | |
| B-13 | Live, cheers, pack walks | 🟡 | B-10 | TODO | |
| B-14 | Genesis vouchers, metadata, Passport | 🟡 | B-08, C-03, C-04, A-01 | TODO | |
| B-15 | Notifications | 🟢 | B-06 | TODO | |
| B-16 | Privacy jobs | 🟢 | B-02 | TODO | |
| B-17 | Den: inventory, avatar, sink quotes | 🟡 | B-06, B-10, A-01 | TODO | |
| B-18 | Loot, Genesis Draw, Forge | 🟠 | B-17, B-14, B-08 | TODO | |
| B-19 | Games backend | 🟡 | G-01, B-06 | TODO | |
| B-20 | Market + rental indexing | 🟡 | B-10, C-09, C-10 | TODO | |
| A-01 | Items, renderers, Genesis traits | 🟡 | P0-04 | TODO | |
| G-01 | Games scaffold | 🟢 | P0-01 | TODO | |
| G-02 | Fetch Frenzy | 🟡 | G-01, A-01 | TODO | |
| G-03 | Doge Derby | 🟡 | G-01, A-01 | TODO | |
| M-01 | App scaffold | 🟢 | P0-05 | TODO | |
| M-02 | UI kit | 🟡 | M-01 | TODO | |
| M-03 | Health data + bg sync | 🟠 | M-01, B-04 | TODO | |
| M-04 | Attestation + auth | 🟠 | M-01, B-03 | TODO | |
| M-05 | Onboarding + Home | 🟡 | M-02, M-03, M-04 | TODO | |
| M-06 | Walk sessions + Go Live | 🟠 | M-05, B-13, B-11 | TODO | |
| M-07 | Moon + Ranks | 🟡 | M-02, B-07, B-09 | TODO | |
| M-08 | Companion Pup + Badges | 🟡 | M-02, B-14, B-17, M-10 | TODO | |
| M-09 | Coach chat | 🟡 | M-02, B-11 | TODO | |
| M-10 | Wallet + on-chain actions | 🟠 | M-04, B-08, C-07 | TODO | |
| M-11 | Walk Bets + Packs screens | 🟡 | M-10, B-12, B-13 | TODO | |
| M-12 | Profile & settings | 🟢 | M-05, B-15, B-16 | TODO | |
| M-13 | Recap share card | 🟢 | M-06 | TODO | |
| M-14 | Den: avatar, closet, loot, forge | 🟡 | M-08, B-17, B-18 | TODO | |
| M-15 | Play hub + games | 🟡 | M-07, G-02, G-03, B-19 | TODO | |
| M-16 | Market screens | 🟡 | M-10, B-20 | TODO | |
| W-01 | Landing + public pages | 🟡 | B-09, P0-05 | TODO | |
| W-02 | Web dapp | 🟡 | W-01, C-07, B-08 | TODO | |
| W-03 | Web market + mint | 🟡 | W-02, C-09, C-10, B-20 | TODO | |
| Q-01 | E2E suites | 🟡 | M-05…M-16, W-02, W-03 | TODO | |
| Q-02 | Load + DAST | 🟢 | Q-01 | TODO | |
| S-01 | System security review | 🔴 | M3 scope | TODO | |
| L-01 | Testnet launch kit | 🟢 | S-01 | TODO | |
| L-02 | Mainnet go/no-go | 🔴 | season 1 + audit + legal | TODO | |
