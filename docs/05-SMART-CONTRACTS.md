# 05 · Smart Contracts (Foundry, OpenZeppelin v5)

> Location: `packages/contracts/`. Solidity is pinned exactly in `foundry.toml`, and `evm_version` comes from P0-01 (default `paris`).
> Style: custom errors, an event for every state change, CEI ordering, `SafeERC20`, `nonReentrant` on every function that moves value, no `tx.origin`, no inline assembly unless the spec asks for it.
> Merkle: off-chain trees use `@openzeppelin/merkle-tree` `StandardMerkleTree` (double-hashed leaves, sorted pairs). On-chain checks use `MerkleProof.verifyCalldata`.

## 1. Contract set
| Contract | Purpose | Tier to build |
|---|---|---|
| `TreatToken` | ERC-20 TREAT | 🟡 |
| `RewardsDistributor` | Daily emission cap, cumulative Merkle claims, bonus pool, veto | 🔴 |
| `GenesisNFT` | The 1,000-cap collection (Pups, Walkers, Relics): rarity caps, leash lock, ERC-4907 rentals, Pup level sync | 🟠 |
| `BadgeSBT` | Soulbound ERC-1155 achievements | 🟢 |
| `WalkBetPool` | Commitment challenges | 🔴 |
| `CheerRouter` | Live tips (TREAT + native DOGE) | 🟡 |
| `TreatSink` | Every TREAT spend (evolve, shop, forge, shields…) with per-purpose burn splits | 🟡 |
| `MuchMarket` | Fixed-price sales (TREAT/DOGE) + NFT↔NFT swaps, 5% fee | 🟠 |
| `RentalHouse` | Paid rentals and free lending through ERC-4907 user rights | 🟠 |
| `TimelockController` (OZ) | Admin of everything | — |
| `VestingWallet` (OZ) | Team allocation | — |

Roles use OZ `AccessControl`. `DEFAULT_ADMIN_ROLE` always belongs to the **Timelock**, and the deployer renounces every role at the end of the deploy script.

---

## 2. Interfaces

### 2.1 TreatToken
```solidity
contract TreatToken is ERC20, ERC20Permit, ERC20Burnable, ERC20Capped, AccessControl {
    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");
    uint256 public constant MAX_SUPPLY = 1_000_000_000e18;
    uint256 public constant GENESIS_SUPPLY = 500_000_000e18; // every bucket except Move-to-Earn

    error GenesisMismatch();
    // recipients/amounts must sum to exactly GENESIS_SUPPLY, else GenesisMismatch
    constructor(address admin, address[] memory recipients, uint256[] memory amounts);
    function mint(address to, uint256 amount) external onlyRole(MINTER_ROLE);
    // _update override required by ERC20Capped (call super)
}
```

### 2.2 RewardsDistributor 🔴
```solidity
// Shared by all contracts: src/interfaces/ITreat.sol
interface ITreat is IERC20 {
    function mint(address,uint256) external; function burn(uint256) external; function burnFrom(address,uint256) external;
}

contract RewardsDistributor is AccessControl, Pausable, ReentrancyGuard {
    bytes32 public constant POSTER_ROLE   = keccak256("POSTER_ROLE");
    bytes32 public constant GUARDIAN_ROLE = keccak256("GUARDIAN_ROLE");
    uint32  public constant YEAR_EPOCHS = 365;
    uint32  public constant MAX_YEARS   = 30;
    uint64  public constant MIN_CLAIM_DELAY = 10 minutes;
    uint64  public constant MAX_CLAIM_DELAY = 7 days;

    ITreat  public immutable treat;
    uint64  public immutable genesisTs;   // UTC midnight
    uint256 public immutable e0;          // 273_972e18

    struct RootInfo {
        bytes32 root; uint64 activeAt; uint32 epochId;
        uint32 prevLastEpoch; bool prevHasPosted;
        uint256 minted; uint256 bonusUsed;
    }
    RootInfo public current;   // claims verify against this
    RootInfo public pending;   // at most one
    uint32  public lastEpoch;  bool public hasPosted;
    uint64  public claimDelay;
    uint256 public bonusBalance;
    uint256 public totalAllocated;   // Σ(minted + bonusUsed) of non-vetoed epochs
    uint256 public totalClaimed;
    mapping(address => uint256) public claimed; // cumulative claimed per account

    event EpochPosted(uint32 indexed epochId, bytes32 root, uint256 minted, uint256 bonusUsed,
                      bytes32 metadataHash, bytes32 nextSeedCommit, uint128 seasonMeters, uint64 activeAt);
    event RootActivated(uint32 indexed epochId, bytes32 root);
    event PendingVetoed(uint32 indexed epochId, bytes32 root, uint256 burned, uint256 bonusRefunded);
    event Claimed(address indexed account, uint256 amount, uint256 cumulative, uint32 epochId);
    event BonusFunded(address indexed from, uint256 amount);
    event ClaimDelaySet(uint64 delay);

    error EpochNotIncreasing(); error EpochNotOver(); error MintAboveCap(uint256 cap);
    error BonusInsufficient(); error ZeroRoot(); error PendingRootExists();
    error NoActiveRoot(); error InvalidProof(); error NothingToClaim();
    error NoPendingRoot(); error PendingAlreadyActive(); error DelayOutOfRange(); error CannotRecoverTreat();

    constructor(ITreat treat, uint64 genesisTs, uint256 e0, uint64 claimDelay, address admin);

    function dailyEmission(uint32 epochId) public view returns (uint256);
    // year = epochId / 365; if year >= MAX_YEARS return 0; b = e0; repeat `year` times: b = b * 4 / 5;

    function postEpoch(uint32 epochId, bytes32 root, uint256 mintAmount, uint256 bonusUsed,
                       bytes32 metadataHash, bytes32 nextSeedCommit, uint128 seasonMeters)
        external onlyRole(POSTER_ROLE) whenNotPaused;
    // Order of checks (exact):
    // 1 root != 0                                   else ZeroRoot
    // 2 !hasPosted || epochId > lastEpoch           else EpochNotIncreasing
    // 3 block.timestamp >= genesisTs + (epochId+1)*86400   else EpochNotOver
    // 4 mintAmount <= dailyEmission(epochId)        else MintAboveCap
    // 5 bonusUsed <= bonusBalance                   else BonusInsufficient
    // 6 _promote(); pending.root == 0               else PendingRootExists
    // effects: bonusBalance -= bonusUsed; totalAllocated += mintAmount + bonusUsed;
    //          pending = RootInfo(root, now+claimDelay, epochId, lastEpoch, hasPosted, mintAmount, bonusUsed);
    //          lastEpoch = epochId; hasPosted = true;
    // interaction: treat.mint(address(this), mintAmount); emit EpochPosted

    function claim(address account, uint256 cumulativeAmount, bytes32[] calldata proof)
        external nonReentrant whenNotPaused;     // permissionless; pays `account`
    struct ClaimArgs { address account; uint256 cumulativeAmount; bytes32[] proof; }
    function claimMany(ClaimArgs[] calldata args) external nonReentrant whenNotPaused;
    // claimMany: entries with cumulativeAmount <= claimed[account] are SKIPPED; an invalid proof REVERTS. Max 100 entries.
    // leaf = keccak256(bytes.concat(keccak256(abi.encode(account, cumulativeAmount))))

    function fundBonus(uint256 amount) external;           // anyone; transferFrom → bonusBalance += amount
    function vetoPending() external onlyRole(GUARDIAN_ROLE);
    // requires pending.root != 0 (NoPendingRoot) and now < pending.activeAt (PendingAlreadyActive)
    // effects: totalAllocated -= minted+bonusUsed; bonusBalance += bonusUsed;
    //          lastEpoch = prevLastEpoch; hasPosted = prevHasPosted; delete pending
    // interaction: treat.burn(minted)
    function promote() external;                              // anyone; calls _promote()
    function pause() external onlyRole(GUARDIAN_ROLE);
    function unpause() external onlyRole(DEFAULT_ADMIN_ROLE);
    function setClaimDelay(uint64 d) external onlyRole(DEFAULT_ADMIN_ROLE); // [MIN, MAX]
    function recoverERC20(IERC20 token, address to, uint256 amount) external onlyRole(DEFAULT_ADMIN_ROLE); // never TREAT

    // _promote(): if pending.root != 0 && now >= pending.activeAt → current = pending; delete pending; emit RootActivated
}
```
**Invariants** (Foundry invariant tests, handler-based):
1. Total TREAT minted by the distributor ≤ Σ `dailyEmission(e)` over all posted, non-vetoed epochs.
2. `totalClaimed ≤ totalAllocated`.
3. `treat.balanceOf(distributor) ≥ totalAllocated − totalClaimed + bonusBalance`. This is equality unless someone transfers tokens in directly.
4. `claimed[a]` never decreases.
5. There is at most one pending root, and `current.epochId < pending.epochId` whenever both exist.
6. Claims only succeed against a root with `activeAt ≤ now`.
7. `postEpoch` for an epoch whose UTC day hasn't ended always reverts.

### 2.3 GenesisNFT 🟠 (replaces the old PupNFT; the only tradable NFT)
```solidity
contract GenesisNFT is ERC721, IERC4906, IERC4907, ERC2981, AccessControl, EIP712, ReentrancyGuard {
    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");   // voucher signer + relayer
    bytes32 public constant SYNCER_ROLE = keccak256("SYNCER_ROLE");   // Pup level/stage sync
    bytes32 public constant RENTAL_ROLE = keccak256("RENTAL_ROLE");   // RentalHouse
    uint16  public constant MAX_SUPPLY = 1_000;
    uint64  public constant MAX_RENT = 30 days;
    enum Kind { Pup, Walker, Relic }
    enum Rarity { Normal, Rare, SuperRare, Legendary, MuchWow }
    // cap[kind][rarity], set in the constructor from 02 §19 and checked to sum to 1,000; no setter exists
    uint16[5][3] public cap;   uint16[5][3] public minted;   uint16 public totalMinted;
    uint8[4] public STAGE_CAP = [9, 24, 49, 50];

    struct Token { Kind kind; Rarity rarity; uint8 channel; uint8 level; uint8 stage; uint64 seed; uint64 lockedUntil; }
    struct UserInfo { address user; uint64 expires; }
    mapping(uint256 => Token) public tokens;
    mapping(uint256 => UserInfo) internal _users;
    mapping(bytes32 => bool) public voucherUsed;
    uint256 public nextId = 1;
    address public treasury; address public shelterFund;

    // EIP-712: Mint(address to,uint8 kind,uint8 rarity,uint8 channel,uint64 seed,uint16 lockDays,uint256 price,bytes32 voucherId,uint256 deadline)
    struct MintVoucher { address to; uint8 kind; uint8 rarity; uint8 channel; uint64 seed; uint16 lockDays; uint256 price; bytes32 voucherId; uint256 deadline; }

    event GenesisMinted(uint256 indexed id, address indexed to, Kind kind, Rarity rarity, uint8 channel, bytes32 voucherId);
    event PupSynced(uint256 indexed id, uint8 level, uint8 stage);
    error SoldOut(); error CellFull(); error VoucherUsed(); error VoucherExpired(); error BadSignature();
    error WrongPrice(); error NotRecipient(); error LeashLocked(); error Rented(); error NotPup();
    error LevelDecrease(); error LevelAboveCap(); error RentTooLong(); error NotAuthorized(); error BatchTooLarge();

    function mintWithVoucher(MintVoucher calldata v, bytes calldata sig) external payable nonReentrant;
    //   Check order: deadline → !voucherUsed → signer has MINTER_ROLE → totalMinted < MAX (SoldOut)
    //   → minted[k][r] < cap[k][r] (CellFull) → caller is v.to, or caller has MINTER_ROLE and v.price == 0 (gasless claim)
    //   → msg.value == v.price (native DOGE; only the mainnet mint sale uses price > 0).
    //   Effects: voucherUsed = true; minted++ / totalMinted++; tokens[id] = …; lockedUntil = lockDays > 0 ? now + lockDays days : 0
    //   Interactions: _mint (not _safeMint); then split proceeds 70% treasury / 30% shelterFund with Address.sendValue
    function syncPups(uint256[] calldata ids, uint8[] calldata levels, uint8[] calldata stages) external onlyRole(SYNCER_ROLE);
    //   ≤ 200 per call; Pup kind only; level and stage never decrease; stage ≤ 3; level ≤ STAGE_CAP[stage]; emits MetadataUpdate

    // ERC-4907 (rentals / lending)
    function setUser(uint256 id, address user, uint64 expires) external;
    //   Allowed when: no active user (_users[id].expires <= now) AND token not leash-locked AND expires <= now + MAX_RENT
    //   AND caller is (owner or approved: free lend to a friend) or RENTAL_ROLE. An active rental can never be overridden.
    function userOf(uint256 id) external view returns (address);       // address(0) once expired
    function userExpires(uint256 id) external view returns (uint256);
    function isTransferable(uint256 id) public view returns (bool);    // !locked && no active user

    // _update override (transfers only, i.e. from != 0 && to != 0):
    //   lockedUntil > now → LeashLocked; active user → Rented; on success delete _users[id] and emit UpdateUser(id, 0, 0)
    // tokenURI = baseURI + id (dynamic metadata API); setBaseURI emits BatchMetadataUpdate
    // ERC2981 default royalty 500 bps → shelterFund. supportsInterface includes IERC4907 (0xad092b5c) and IERC4906 (0x49064906)
}
```
**Invariants:**
1. `totalMinted ≤ 1,000`.
2. `minted[k][r] ≤ cap[k][r]` for every cell. Relic / Much Wow can never be minted.
3. Each voucher is used at most once.
4. A token that is locked or actively rented never changes owner.
5. An active rental can't be overwritten, and no rental lasts longer than 30 days.
6. Pup level and stage never decrease.

### 2.4 BadgeSBT 🟢
```solidity
contract BadgeSBT is ERC1155, AccessControl {
    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");
    mapping(uint256 => bool) public stackable;   // true for 801,802,803
    error Soulbound();
    function airdrop(address[] calldata to, uint256 id) external onlyRole(MINTER_ROLE);       // ≤300; skip holders of non-stackable ids
    function mintBatch(address to, uint256[] calldata ids, uint256[] calldata amts) external onlyRole(MINTER_ROLE); // same skip rule
    function burn(uint256 id, uint256 amount) external;   // holder may hide a badge
    function locked(uint256) external pure returns (bool) { return true; }
    // _update: if (from != 0 && to != 0) revert Soulbound();  setApprovalForAll → revert Soulbound()
    function setURI(string calldata) external onlyRole(DEFAULT_ADMIN_ROLE);  // ".../badges/{id}.json"
}
```

### 2.5 WalkBetPool 🔴
```solidity
contract WalkBetPool is AccessControl, Pausable, ReentrancyGuard {
    bytes32 public constant CURATOR_ROLE  = keccak256("CURATOR_ROLE");
    bytes32 public constant ORACLE_ROLE   = keccak256("ORACLE_ROLE");
    bytes32 public constant GUARDIAN_ROLE = keccak256("GUARDIAN_ROLE");
    uint256 public constant FEE_BPS = 1_000;
    uint64  public constant RESULTS_DELAY = 6 hours;
    uint64  public constant DISPUTE_WINDOW = 24 hours;
    uint64  public constant ORACLE_TIMEOUT = 7 days;   // after end+RESULTS_DELAY, anyone can cancel if no results
    uint128 public constant MIN_STAKE = 10e18;  uint128 public constant MAX_STAKE = 1_000e18;
    uint32  public constant MAX_PARTICIPANTS = 500;

    enum Status { None, Open, Resolved, Cancelled }
    struct Challenge {
        uint128 stake; uint128 payoutPerWinner;
        uint64 startTime; uint64 endTime; uint64 resultsPostedAt;
        uint32 maxParticipants; uint32 participants; uint32 winners; uint32 paidCount;
        Status status; bytes32 rulesHash; bytes32 winnersRoot;
    }
    ITreat public immutable treat; address public shelterFund;
    uint256 public challengeCount;
    mapping(uint256 => Challenge) public challenges;
    mapping(uint256 => mapping(address => uint8)) public state; // 0 none, 1 joined, 2 settled

    event ChallengeCreated(uint256 indexed id, uint128 stake, uint64 start, uint64 end, uint32 maxP, bytes32 rulesHash);
    event Joined(uint256 indexed id, address indexed user);
    event Left(uint256 indexed id, address indexed user);
    event ResultsPosted(uint256 indexed id, bytes32 winnersRoot, uint32 winners);
    event Finalized(uint256 indexed id, uint128 payoutPerWinner, uint256 burned, uint256 toShelter);
    event Cancelled(uint256 indexed id);
    event Paid(uint256 indexed id, address indexed user, uint256 amount, bool refund);

    function createChallenge(uint128 stake, uint32 maxP, uint64 start, uint64 end, bytes32 rulesHash)
        external onlyRole(CURATOR_ROLE) returns (uint256 id);  // stake∈[MIN,MAX]; 2≤maxP≤MAX; start>now; 3d ≤ end-start ≤ 30d
    function join(uint256 id) external nonReentrant whenNotPaused;      // Open, now<start, room, state==0; pull stake
    function joinWithPermit(uint256 id, uint256 deadline, uint8 v, bytes32 r, bytes32 s) external; // try permit {} catch {}; then join logic
    function leave(uint256 id) external nonReentrant;                   // only before start; refund stake; state→0
    function postResults(uint256 id, bytes32 root, uint32 winners) external onlyRole(ORACLE_ROLE);
    //   Open; participants>0; now ≥ end+RESULTS_DELAY; resultsPostedAt==0; winners ≤ participants; root!=0 || winners==0
    function finalize(uint256 id) external nonReentrant;               // anyone; now ≥ resultsPostedAt+DISPUTE_WINDOW; math in 03 §11
    function claim(uint256 id, bytes32[] calldata proof) external;      // = claimFor(id, msg.sender, proof)
    function claimFor(uint256 id, address user, bytes32[] calldata proof) public nonReentrant;
    //   Resolved; state==1; paidCount < winners; leaf = keccak256(bytes.concat(keccak256(abi.encode(id, user))))
    //   state→2; paidCount++; transfer payoutPerWinner to user
    function cancel(uint256 id) external;
    //   GUARDIAN: if Open && (resultsPostedAt==0 || now < resultsPostedAt+DISPUTE_WINDOW)
    //   ANYONE:   if Open && resultsPostedAt==0 && now ≥ end+RESULTS_DELAY+ORACLE_TIMEOUT
    function refund(uint256 id, address user) external nonReentrant;    // Cancelled; state==1 → 2; transfer stake
    function setShelterFund(address) external onlyRole(DEFAULT_ADMIN_ROLE);
}
```
**Invariants:**
1. For every challenge, the total paid out plus burned plus sent to the shelter is ≤ `participants × stake`.
2. Each participant is paid at most once.
3. `paidCount ≤ winners`.
4. The contract's balance ≥ Σ outstanding obligations of all challenges. One challenge can never touch another challenge's funds.
5. Funds can always leave: every challenge eventually becomes Resolved or Cancelled, via the timeout.

### 2.6 CheerRouter 🟡
```solidity
contract CheerRouter is AccessControl, Pausable, ReentrancyGuard {
    uint256 public constant TIP_FEE_BPS = 200;   uint256 public constant MIN_TIP = 1e18;
    IERC20 public immutable treat; address public shelterFund;
    event Cheered(address indexed from, address indexed to, bytes32 indexed sessionId,
                  address token, uint256 amount, uint256 fee, bytes32 messageHash);
    error SelfTip(); error ZeroAddress(); error TipTooSmall();
    function cheer(address to, uint256 amount, bytes32 sessionId, bytes32 messageHash) external nonReentrant whenNotPaused;
    function cheerWithPermit(address to, uint256 amount, bytes32 sessionId, bytes32 messageHash,
                             uint256 deadline, uint8 v, bytes32 r, bytes32 s) external;
    function cheerNative(address payable to, bytes32 sessionId, bytes32 messageHash) external payable nonReentrant whenNotPaused;
    //   native MIN_TIP = 1e18 wei-DOGE too; fee to shelterFund; Address.sendValue for both legs; token = address(0)
}
```
Only `messageHash = keccak256(utf8(message))` goes on-chain. The plaintext goes to the API, which checks it against the hash and moderates it. That way no offensive text is ever permanent on-chain.

### 2.7 TreatSink 🟡 (one door for all TREAT spending)
```solidity
contract TreatSink is AccessControl, Pausable, ReentrancyGuard {
    struct Split { uint16 burnBps; uint16 shelterBps; uint16 treasuryBps; bool active; }  // sums to 10_000
    mapping(bytes32 => Split) public splits;   // keys: keccak256("EVOLVE"|"SHIELD"|"SHOP"|"FORGE"|"PACK"|"COACH"|"RENAME"|"PASS")
    ITreat public immutable treat; address public shelterFund; address public treasury;
    event Spent(address indexed user, uint256 amount, bytes32 indexed purpose, bytes32 indexed ref);
    error UnknownPurpose(); error ZeroAmount(); error BadSplit();
    function spend(uint256 amount, bytes32 purpose, bytes32 ref) external nonReentrant whenNotPaused;
    //   pull amount; burn burnBps share via treat.burn; send shelter/treasury shares; emit Spent
    function spendWithPermit(uint256 amount, bytes32 purpose, bytes32 ref, uint256 deadline, uint8 v, bytes32 r, bytes32 s) external;
    function setSplit(bytes32 purpose, Split calldata sp) external onlyRole(DEFAULT_ADMIN_ROLE);  // through the Timelock
}
```
Prices live off-chain:
1. The API returns a **quote** `{purpose, ref, amount, expiresAt}`.
2. The user pays it through `TreatSink.spend`.
3. The indexer credits the action only if a `Spent` event matches an unexpired quote with `amount ≥ quote`.
4. Underpaying credits nothing and flags the payment for support. The UI always sends the exact amount.

### 2.8 MuchMarket 🟠 (sell + trade; escrow-less)
```solidity
contract MuchMarket is AccessControl, Pausable, ReentrancyGuard {
    uint256 public constant FEE_BPS = 500;  uint64 public constant MAX_LISTING = 90 days;  uint8 public constant MAX_SWAP_IDS = 5;
    IGenesis public immutable genesis; ITreat public immutable treat; address public shelterFund; address public treasury;
    struct Listing { address seller; uint96 price; address payToken; uint64 expiry; }   // payToken: treat, or address(0) = DOGE
    mapping(uint256 => Listing) public listings;
    struct Swap { address maker; address taker; uint256[] makerIds; uint256[] takerIds; uint128 makerTreat; uint128 takerTreat; uint64 expiry; bool open; }
    mapping(uint256 => Swap) internal _swaps;  uint256 public swapCount;

    event Listed(uint256 indexed id, address indexed seller, uint96 price, address payToken, uint64 expiry);
    event ListingCancelled(uint256 indexed id);
    event Sold(uint256 indexed id, address indexed seller, address indexed buyer, uint96 price, address payToken, uint256 fee);
    event SwapProposed(uint256 indexed swapId, address indexed maker, address indexed taker);
    event SwapAccepted(uint256 indexed swapId);  event SwapCancelled(uint256 indexed swapId);
    error NotOwner(); error NotTransferable(); error NotApproved(); error BadToken(); error BadPrice(); error Expired();
    error NoListing(); error PriceChanged(); error WrongValue(); error NotTaker(); error SwapClosed(); error TooManyIds();

    function list(uint256 id, uint96 price, address payToken, uint64 expiry) external whenNotPaused;
    //   caller owns id; genesis.isTransferable(id); market is approved; payToken ∈ {treat, 0}; price > 0; expiry ≤ now + MAX_LISTING
    function cancel(uint256 id) external;            // the seller, or anyone once the seller no longer owns the token (clears a stale listing)
    function buy(uint256 id, uint96 expectedPrice, address expectedToken) external payable nonReentrant whenNotPaused;
    //   listing exists, not expired, seller still owns the token, price/token == expected (front-run guard)
    //   delete listing → collect payment (DOGE: msg.value == price; TREAT: transferFrom buyer)
    //   fee = price × 500 / 10_000 → TREAT: half burned, half to shelterFund · DOGE: half treasury, half shelterFund
    //   seller gets price − fee → genesis.safeTransferFrom(seller, buyer, id)
    function proposeSwap(address taker, uint256[] calldata makerIds, uint256[] calldata takerIds,
                         uint128 makerTreat, uint128 takerTreat, uint64 expiry) external returns (uint256 swapId);
    //   ≤ 5 ids per side; maker owns makerIds and they're transferable; expiry ≤ now + 7 days
    function acceptSwap(uint256 swapId) external nonReentrant whenNotPaused;
    //   caller == taker; open; not expired; re-check ownership + transferability of every id on both sides;
    //   close the swap → move every NFT both ways → move the TREAT legs, applying the 5% fee (same split) to each TREAT leg
    function cancelSwap(uint256 swapId) external;    // the maker
}
```
**Invariants:**
- A buy or swap either completes in full or reverts.
- The market never holds NFTs. It holds TREAT and DOGE only inside a single call.
- A seller always receives `price − fee`.
- A listing whose seller no longer owns the token can't be bought.

### 2.9 RentalHouse 🟠 (lend / rent via ERC-4907)
```solidity
contract RentalHouse is AccessControl, Pausable, ReentrancyGuard {
    uint256 public constant FEE_BPS = 500;  uint16 public constant MAX_DAYS = 30;
    IGenesis public immutable genesis; ITreat public immutable treat; address public shelterFund;
    struct Offer { address owner; uint96 pricePerDay; uint16 minDays; uint16 maxDays; uint64 expiry; address reservedFor; } // reservedFor 0 = anyone
    mapping(uint256 => Offer) public offers;
    event Offered(uint256 indexed id, address indexed owner, uint96 pricePerDay, uint16 minDays, uint16 maxDays, address reservedFor);
    event OfferCancelled(uint256 indexed id);
    event Rented(uint256 indexed id, address indexed owner, address indexed renter, uint16 days_, uint256 paid, uint256 fee, uint64 until);
    error NotOwner(); error NotTransferable(); error BadDays(); error NoOffer(); error Reserved(); error SelfRent(); error PriceChanged();

    function offer(uint256 id, uint96 pricePerDay, uint16 minDays, uint16 maxDays, uint64 expiry, address reservedFor) external;
    //   caller owns id; isTransferable(id); 1 ≤ minDays ≤ maxDays ≤ 30. pricePerDay may be 0 only when reservedFor != 0 (free lend to a friend)
    function cancel(uint256 id) external;            // the owner, or anyone once the owner has changed
    function rent(uint256 id, uint16 days_, uint96 expectedPricePerDay) external nonReentrant whenNotPaused;
    //   offer valid; owner unchanged; no active user; reservedFor rule; caller != owner; days within range; price == expected
    //   cost = pricePerDay × days_; fee 5% (half burned, half shelterFund); owner is paid upfront (no refunds)
    //   genesis.setUser(id, msg.sender, now + days_ × 1 days)   // RENTAL_ROLE; the offer stays live for future rentals
}
```
**Invariants:**
- RentalHouse never takes custody of an NFT.
- A rental can't be shortened, extended past 30 days, or overridden.
- While a rental is active, the owner can't sell or transfer the token (GenesisNFT enforces this).

---

## 3. Deployment (`script/Deploy.s.sol`) 🟡
1. Check the deployer's balance against `MIN_DEPLOY_BALANCE`, and log the balance before and after **every** deployment (see the DogeOS gas issue in 04 §2).
2. Deploy `TimelockController(minDelay = 3600 on testnet / 172800 on mainnet, proposers = [ADMIN_SAFE], executors = [ADMIN_SAFE], admin = address(0))`.
3. Deploy `VestingWallet(teamBeneficiary, start = now + 365 days, duration = 3 * 365 days)`.
4. Deploy `TreatToken(admin = deployer, recipients = [community, ecosystem, liquidity, treasury, vesting], amounts = [100M, 100M, 80M, 100M, 120M])`.
5. Deploy `RewardsDistributor(treat, GENESIS_TS, 273_972e18, claimDelay = 3600, admin = deployer)`, then deploy `GenesisNFT`, `BadgeSBT`, `WalkBetPool`, `CheerRouter`, `TreatSink`, `MuchMarket` and `RentalHouse`.
6. Wire the roles:
   - Treat `MINTER` → Distributor
   - Distributor `POSTER` → poster key; `GUARDIAN` → guardian(s)
   - Genesis `MINTER` → relayer (also the voucher signer); Genesis `SYNCER` → worker; Genesis `RENTAL` → RentalHouse
   - TreatSink splits for every purpose (03 §10)
   - Badge `MINTER` → relayer
   - BetPool `CURATOR` → curator; `ORACLE` → oracle key; `GUARDIAN` → guardian
7. Grant `DEFAULT_ADMIN_ROLE` on every contract to the Timelock, and have the deployer **renounce all its roles**.
8. **Assert the final role state on-chain inside the script.** Fail the script if the deployer still holds any role.
9. Write `addresses/<chainId>.json`, verify the contracts on the explorer (Blockscout verifier), and run `pnpm --filter @muchwalk/contracts export` to generate the TS ABIs.

## 4. Testing requirements (all contracts)
- Unit tests cover every external function's happy path **and every custom error**.
- Fuzz tests cover amounts, timings, Merkle sets (random trees built in Solidity test helpers), and pack sizes.
- Invariant tests are handler-based, use `fail_on_revert = false`, and run ≥ 256 runs × depth 64 in CI and 10k runs nightly.
- Coverage: Distributor, BetPool, GenesisNFT, MuchMarket and RentalHouse **≥ 95% lines and branches**; others ≥ 90%.
- Marketplace and rental tests must include: a malicious ERC-721 receiver, a seller contract that rejects DOGE, front-run price changes, stale listings after a transfer, and rent → transfer attempt → expiry → transfer.
- Static analysis: **Slither** shows no unresolved high/medium findings, and the **Aderyn** report is reviewed in `docs/audits/`.
- Gas snapshot (`forge snapshot`) is committed, and CI fails on a >10% regression.
- A cross-language test checks that a tree built with `StandardMerkleTree` in TS verifies in Solidity (fixtures in `test/fixtures/*.json`).
