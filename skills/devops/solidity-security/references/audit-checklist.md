# Security Audit Checklist

Comprehensive smart contract security audit checklist organized by category. Use before deployment, during internal review, or when preparing for a professional audit.

Items marked **[CRITICAL]** must pass before mainnet deployment.

---

## 1. State Management

### Checklist

- [ ] **[CRITICAL]** Checks-Effects-Interactions pattern followed in all functions with external calls
- [ ] **[CRITICAL]** `ReentrancyGuard` applied on functions making external calls
- [ ] **[CRITICAL]** `ReentrancyGuard` applied on all functions sharing state with externally-calling functions
- [ ] State variables properly initialized (no reliance on default zero values for security)
- [ ] No unintended storage slot collisions in proxy patterns
- [ ] Storage layout is append-only in upgradeable contracts
- [ ] State transitions validated with `require` statements before execution
- [ ] Events emitted for every state change

### What to Look For

❌ **Bad: State update after external call**

```solidity
function withdraw(uint256 amount) external {
    require(balances[msg.sender] >= amount);
    (bool success, ) = msg.sender.call{value: amount}("");
    require(success);
    balances[msg.sender] -= amount;  // Updated too late
}
```

✅ **Good: State update before external call**

```solidity
function withdraw(uint256 amount) external nonReentrant {
    require(balances[msg.sender] >= amount);
    balances[msg.sender] -= amount;  // Effect before interaction
    (bool success, ) = msg.sender.call{value: amount}("");
    require(success);
}
```

---

## 2. Access Control

### Checklist

- [ ] **[CRITICAL]** All privileged functions protected with access control modifiers
- [ ] **[CRITICAL]** No `tx.origin` used for authentication
- [ ] **[CRITICAL]** Initializer functions protected with `initializer` modifier
- [ ] Role-based access control used for multi-role systems (prefer `AccessControl` over custom)
- [ ] Ownership transfer uses two-step pattern (`Ownable2Step`)
- [ ] Admin functions behind timelock for DeFi protocols
- [ ] No single point of failure (multisig for critical operations)
- [ ] `_disableInitializers()` called in implementation contract constructors

### What to Look For

Scan for `external` and `public` functions without modifiers:

❌ **Bad: Public function without access control**

```solidity
function setFeeRecipient(address _recipient) external {
    feeRecipient = _recipient;  // Anyone can call
}
```

✅ **Good: Protected with role-based access**

```solidity
function setFeeRecipient(address _recipient) external onlyRole(ADMIN_ROLE) {
    require(_recipient != address(0), "Zero address");
    feeRecipient = _recipient;
    emit FeeRecipientUpdated(_recipient);
}
```

---

## 3. External Calls

### Checklist

- [ ] **[CRITICAL]** Return values of all external calls checked
- [ ] **[CRITICAL]** No `delegatecall` to untrusted or user-provided addresses
- [ ] Low-level `.call{}` preferred over `.transfer()` and `.send()` (2300 gas limit issues)
- [ ] Reentrancy protection on all callback-receiving functions
- [ ] `fallback()` and `receive()` functions are minimal (no complex logic)
- [ ] External call targets validated (not address(0))
- [ ] Failed external calls handled gracefully (no silent failures)

### What to Look For

❌ **Bad: Unchecked external call return value**

```solidity
payable(recipient).send(amount);  // Return value ignored
token.transfer(to, amount);       // Some tokens don't revert on failure
```

✅ **Good: Checked returns with SafeERC20**

```solidity
(bool success, ) = recipient.call{value: amount}("");
require(success, "ETH transfer failed");

// For ERC-20 tokens
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
using SafeERC20 for IERC20;
token.safeTransfer(to, amount);
```

---

## 4. Token Handling

### Checklist

- [ ] **[CRITICAL]** `SafeERC20` wrapper used for all ERC-20 interactions
- [ ] **[CRITICAL]** Fee-on-transfer tokens handled (balance checked before and after transfer)
- [ ] Rebasing token behavior accounted for (balance changes without transfers)
- [ ] No hardcoded assumptions about token decimals (query dynamically)
- [ ] Approval race condition mitigated (approve to 0 first, or use `increaseAllowance`)
- [ ] ERC-777 callback reentrancy considered for arbitrary token support
- [ ] Token return values not assumed (some tokens return void)
- [ ] No assumption that `balanceOf(address(this))` equals internal accounting

### What to Look For

❌ **Bad: Assuming transfer amount equals received amount**

```solidity
function deposit(uint256 amount) external {
    token.transferFrom(msg.sender, address(this), amount);
    balances[msg.sender] += amount;  // Wrong for fee-on-transfer tokens
}
```

✅ **Good: Measuring actual received amount**

```solidity
function deposit(uint256 amount) external {
    uint256 balanceBefore = token.balanceOf(address(this));
    token.safeTransferFrom(msg.sender, address(this), amount);
    uint256 received = token.balanceOf(address(this)) - balanceBefore;
    balances[msg.sender] += received;  // Actual amount received
}
```

---

## 5. Mathematical Operations

### Checklist

- [ ] Solidity version >= 0.8.0 used (built-in overflow/underflow protection)
- [ ] `unchecked` blocks used only where overflow is proven impossible and documented
- [ ] Division-before-multiplication avoided (precision loss)
- [ ] Rounding direction consistent and documented (round down for withdrawals, round up for deposits)
- [ ] No division by zero possible
- [ ] Large multiplications checked for overflow before division

### What to Look For

❌ **Bad: Precision loss from division before multiplication**

```solidity
uint256 share = totalAmount / totalShares * userShares;
// If totalAmount=100, totalShares=3, userShares=2:
// 100/3 = 33 (truncated), 33*2 = 66 (lost 0.66)
```

✅ **Good: Multiplication before division**

```solidity
uint256 share = totalAmount * userShares / totalShares;
// 100*2 = 200, 200/3 = 66 (only 0.33 lost)
```

---

## 6. Oracle and Price Feed Security

### Checklist

- [ ] **[CRITICAL]** No AMM spot price used as oracle (flash-loan manipulable)
- [ ] **[CRITICAL]** Oracle data freshness validated (`updatedAt` check)
- [ ] Oracle round completeness checked (`answeredInRound >= roundId`)
- [ ] Price > 0 validated (negative or zero prices rejected)
- [ ] Price deviation bounds enforced (circuit breaker for extreme moves)
- [ ] Fallback oracle configured for primary oracle failure
- [ ] Oracle decimals handled correctly (different feeds use different decimals)

### What to Look For

❌ **Bad: No validation on oracle data**

```solidity
(, int256 price, , , ) = priceFeed.latestRoundData();
return uint256(price);
```

✅ **Good: Comprehensive oracle validation**

```solidity
(uint80 roundId, int256 price, , uint256 updatedAt, uint80 answeredInRound) =
    priceFeed.latestRoundData();
require(price > 0, "Invalid price");
require(updatedAt > 0, "Round not complete");
require(answeredInRound >= roundId, "Stale round");
require(block.timestamp - updatedAt <= MAX_STALENESS, "Price too old");
return uint256(price);
```

---

## 7. Upgrade Patterns

### Checklist

- [ ] **[CRITICAL]** Storage layout compatibility verified between versions (no slot reordering)
- [ ] **[CRITICAL]** Initializer not callable after upgrade (no re-initialization)
- [ ] **[CRITICAL]** No constructor with state in implementation contracts
- [ ] UUPS: `_authorizeUpgrade` properly restricted to admin
- [ ] Transparent proxy: admin cannot call implementation functions
- [ ] Storage gaps (`uint256[50] __gap`) in base contracts for future variables
- [ ] Implementation contract self-destruct impossible (since Cancun, less relevant)
- [ ] Upgrade tested on fork before mainnet deployment

### What to Look For

❌ **Bad: Missing storage gap in base contract**

```solidity
contract BaseV1 {
    uint256 public value;
    // No gap - adding variables in V2 will collide with child storage
}

contract ChildV1 is BaseV1 {
    uint256 public childValue;  // Slot 1
}
```

✅ **Good: Storage gap for future-proofing**

```solidity
contract BaseV1 {
    uint256 public value;
    uint256[49] private __gap;  // Reserve slots for future variables
}

contract BaseV2 is BaseV1 {
    uint256 public newValue;    // Uses one gap slot
    uint256[48] private __gap;  // Reduced gap
}
```

---

## 8. Gas and DoS Prevention

### Checklist

- [ ] No unbounded loops over storage arrays
- [ ] Pull-over-push payment pattern used for fund distribution
- [ ] Array operations bounded by a maximum iteration count
- [ ] No single user action can permanently block contract functionality
- [ ] Gas-intensive operations paginated
- [ ] `selfdestruct` not relied upon (deprecated post-Dencun for most use cases)

### What to Look For

❌ **Bad: Unbounded loop over growing array**

```solidity
function distributeRewards() external {
    for (uint256 i = 0; i < stakers.length; i++) {
        payable(stakers[i]).transfer(rewards[stakers[i]]);
    }
}
```

✅ **Good: Pull pattern with individual claims**

```solidity
function claimReward() external {
    uint256 reward = pendingRewards[msg.sender];
    require(reward > 0, "No reward");
    pendingRewards[msg.sender] = 0;
    (bool success, ) = msg.sender.call{value: reward}("");
    require(success);
}
```

---

## 9. Documentation and Testing

### Checklist

- [ ] NatSpec comments on all `public` and `external` functions
- [ ] Test coverage > 95% for critical paths (deposits, withdrawals, liquidations)
- [ ] Fuzz testing on arithmetic operations (Foundry `forge test --fuzz-runs 10000`)
- [ ] Invariant testing on state transitions
- [ ] Edge cases tested: zero amounts, max uint256, empty arrays, self-transfers
- [ ] Fork testing against mainnet state for integrations
- [ ] Gas snapshots recorded for regression detection

---

## Pre-Deployment Final Checks

### Checklist

- [ ] All **[CRITICAL]** items above passing
- [ ] All compiler warnings resolved
- [ ] `pragma solidity` pinned to exact version (e.g., `0.8.20`, not `^0.8.20`)
- [ ] All events emitted for state changes (enables off-chain indexing)
- [ ] Constructor / initializer parameters verified on testnet
- [ ] Deployment script tested on testnet and forked mainnet
- [ ] Contract verified on Etherscan / Sourcify
- [ ] Admin keys secured (hardware wallet or multisig)
- [ ] Emergency pause mechanism tested
- [ ] Monitoring and alerting configured for critical events

---

## Quick Reference

| Category | Critical Items | Detection Tool |
|----------|---------------|----------------|
| State Management | CEI pattern, ReentrancyGuard | Slither reentrancy detectors |
| Access Control | Modifier coverage, no tx.origin | Slither access-control checks |
| External Calls | Return value checks, no unsafe delegatecall | Slither unchecked-lowlevel |
| Token Handling | SafeERC20, fee-on-transfer handling | Manual review + Slither |
| Math | Overflow protection, precision ordering | Mythril, Foundry fuzz |
| Oracles | No spot price, freshness validation | Manual review |
| Upgrades | Storage layout, initializer protection | OpenZeppelin Upgrades Plugin |
| Gas / DoS | Bounded loops, pull payments | Gas profiler, manual review |
| Testing | 95%+ coverage, fuzz, invariant | Foundry coverage, Hardhat |
