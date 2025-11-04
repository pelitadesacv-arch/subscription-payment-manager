# 🌀 Subscription Payment Manager (Algorand dApp)

A decentralized **subscription payment manager** built on **Algorand**, designed to handle recurring payments securely and transparently using smart contracts.

---

## 📜 Project Description

**Subscription Payment Manager** is a lightweight Algorand smart contract that enables users to create, manage, and cancel subscriptions directly on-chain.  
It leverages **Algorand ARC-4 ABI** and **box storage** to keep track of users’ subscription data, payment intervals, and status — all without centralized servers.

This project is perfect for dApps that need **recurring billing** or **subscription tracking**, such as:
- Decentralized SaaS tools  
- NFT or DAO membership payments  
- Content creator subscriptions  

---

## 💡 What It Does

The smart contract provides a complete on-chain system for managing subscriptions:

1. **Create subscriptions** — Users can define the amount and interval (e.g., monthly, weekly).  
2. **Check payment due** — The system automatically detects if the next payment is due based on the current blockchain timestamp.  
3. **Cancel or delete subscriptions** — Users can stop or remove their subscriptions anytime.  
4. **Track total subscriptions** — The contract keeps a counter of all subscriptions ever created.  

---

## ⚙️ Features

| Feature | Description |
|----------|-------------|
| 🏗️ **Create Subscription** | Register a new recurring payment with a set amount and interval. |
| 👀 **View Subscription Info** | View details of your subscription (amount, interval, and status). |
| ⏰ **Check Payment Due** | Automatically determine if it’s time to renew payment. |
| ❌ **Cancel Subscription** | Instantly deactivate your subscription without deleting data. |
| 🧹 **Delete Subscription** | Permanently remove a subscription from box storage. |
| 🔢 **Get Total Subscriptions** | Retrieve how many subscriptions have been created overall. |
| 🧰 **Hello Method** | A simple “Hello, Name” method for easy contract testing. |

---

## 🧾 Deployed Smart Contract

- **Algorand MainNet App ID:** [`749003734`](https://app.dappflow.org/explorer/application/749003734)

---

## 🧠 How It Works

Each user’s subscription is stored in a **box** on the Algorand blockchain.  
The contract packs subscription data into 25 bytes for efficiency:

| Data | Size | Description |
|------|------|-------------|
| `amount` | 8 bytes | Payment amount (microAlgos) |
| `interval_days` | 8 bytes | Subscription interval (in seconds) |
| `last_payment` | 8 bytes | Last payment timestamp |
| `is_active` | 1 byte | Subscription status (`0x01` = active, `0x00` = inactive) |

All operations — create, check, cancel, delete — are **permissionless** and **on-chain**.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- [Algopy](https://github.com/algorandfoundation/algopy) SDK
- An Algorand wallet (e.g., [Pera Wallet](https://perawallet.app/))
- Access to an Algorand node or [DappFlow](https://app.dappflow.org/)

### Clone the Repository
```bash
git clone https://github.com/yourusername/subscription-payment-manager.git
cd subscription-payment-manager
