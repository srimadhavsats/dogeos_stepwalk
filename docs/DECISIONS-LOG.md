# Decisions Log

Record every spec gap filled during the build and every verified fact, newest first. Keep each entry to one line.
Format: `YYYY-MM-DD · TASK-ID · decision · why`

- 2026-10-14 · PLAN · Economy v2 proposal used for build v6: Points First, revenue-linked Treat Bowl, DOGE-priced items with 50% buyback, instant claims burn 50% or vest 21 days, leash energy, sponsored walks, launch gate; in Phase 1 anything tradable is priced in DOGE (pending team review, OPEN-QUESTIONS #12) · outside money must fund rewards, and points must never leak value
- 2026-10-06 · PLAN · Only 1,000 NFTs ever (GenesisNFT: 500 Pups, 350 Walkers, 150 Relics; Normal → Much Wow). Starter Pups, Walkers and items are off-chain · scarcity plus free-to-play
- 2026-10-06 · PLAN · Lending = ERC-4907 rentals (and free lending to a friend), no collateral loans · no custody, no default risk
- 2026-10-06 · PLAN · Loot boxes are earned only, never sold; odds published; rolls verifiable; Genesis NFTs come from a nightly draw with a fixed per-season count · fairness + legal safety
- 2026-10-06 · PLAN · All TREAT spending goes through TreatSink with per-purpose splits · one auditable sink, simple indexing
- 2026-10-06 · PLAN · Mini-games are Phaser web games with a deterministic engine re-simulated server-side; tickets come only from walking · same build on web and mobile, verifiable scores
- 2026-10-06 · PLAN · Tab bar becomes Home · Ranks · Walk · Play · Den · room for games and collection
- 2026-10-05 · PLAN · Brand "MuchWalk", token "$TREAT", coach "Coach Bark" (working names; change with a single find-replace) · fun and on-brand for Doge
- 2026-10-05 · PLAN · `evm_version = paris` until P0-02 proves newer opcodes on Chikyū · a zk-rollup EVM may not support PUSH0/TSTORE/MCOPY
