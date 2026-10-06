# 12 · Launch Checklists

## 1. Public testnet beta (Chikyū)
**Chain and contracts**
- [ ] P0-02 chain facts verified. Contracts deployed with `Deploy.s.sol`, and the role assertions passed
- [ ] Contracts verified on the explorer, and `addresses/6281971.json` committed
- [ ] Deployer holds no roles. Timelock is admin. Guardian keys tested (a pause/unpause drill on testnet)
- [ ] Relayer, poster, oracle and syncer keys are funded and have low-balance alerts
- [ ] The first 3 epochs were posted and claimed end-to-end, and `blocks/verify.ts` reproduces the draws

**Backend and apps**
- [ ] Staging k6 and ZAP pass (Q-02), and S-01 has no open high findings
- [ ] Sentry, logs, uptime and the chain monitor are alerting to the team channel
- [ ] TestFlight external group and Play closed testing published, with the Health permission declarations filled in
- [ ] Coach spend cap is set and the evals pass
- [ ] Backups: Postgres PITR on, plus a restore drill done

**Users and community**
- [ ] In-app: "Testnet: treats have no value" banner on Claim, Bets and Tips
- [ ] Privacy policy and terms (drafts reviewed by counsel), and age gate
- [ ] Support inbox + FAQ (faucet, wallets, "Under review")
- [ ] Launch posts: the DogeOS community, a Moon Mission season 1 announcement, and the Pioneer badge rules (recognition only)
- [ ] Incident runbook rehearsed (09 §10)

## 2. Mainnet go/no-go (L-02)
Each item needs evidence linked in `docs/launch/mainnet-readiness.md`.
- [ ] DogeOS mainnet is live and stable. Its security model, finality and fee behaviour are documented, and the testnet gas-accounting issue is resolved
- [ ] An external audit of every contract, with all findings resolved. A public contest is complete. A bug bounty is live
- [ ] Mainnet keys are in KMS, with Safe 2-of-3 + 48h Timelock and a separate guardian Safe. A key-rotation drill is done
- [ ] Testnet season 1 metrics: cheat-flag rate < 3%, zero contract incidents, a burn/mint trend toward the 40% target
- [ ] Tokenomics re-simulated with real testnet data (T-01 re-run). Sink prices finalised by governance
- [ ] **Legal sign-off**: token, Walk Bets, Walk Blocks prize draw, tipping, health data, and the geo-fencing list
- [ ] App Store and Play policy review of the crypto features (NFT display/sale rules, crypto transfers). If needed, gated features move to the web dapp
- [ ] Liquidity plan and treasury policy published. No promises of price or returns in any marketing
- [ ] Genesis mainnet supply matrix and season schedule verified against the deployed `cap` table. Mint-sale price set. Shelter Pup auction partner confirmed
- [ ] Store builds use the feature-flag defaults from 09 §11, and the loot odds page is live
- [ ] Fresh mainnet deployment (testnet balances do **not** carry over). Communications plan for testers
