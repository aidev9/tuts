### **Use Case: Core Banking System Operations for Legacy Mainframe (Cobol-based)**

---

#### **Use Case Name**: Core Banking System Operations (Interest Rates, Account Creation, Transactions, Fees, etc.)

#### **Actor**:

- Bank Customer (User)
- Bank Teller
- System Administrator
- Bank Back-Office Staff
- Core Banking System (COBOL Mainframe)

#### **Preconditions**:

- The core banking system is a legacy system originally built in the 1980s, written in **COBOL**, and running on **Mainframe computers**.
- The system supports key banking operations such as **interest rate calculation**, **account creation**, **account closure**, **money transfers**, and **transaction processing**.
- System handles both **savings** and **checking** accounts.
- Customer data and account information are stored in flat files or proprietary databases commonly used in mainframe environments.

#### **Description**:

This use case details the various operations performed on a legacy core banking system built in the 1980s using COBOL and running on mainframe infrastructure. It includes business rules for handling critical banking functions such as **interest rate calculations**, **debits**, **credits**, **account transfers**, **account creation**, **account closing**, and **fee management**.

---

### **Main Success Scenario**:

1. **Account Creation**:

   - A bank customer walks into the branch or applies online to open a **new account** (either savings or checking).
   - The **Bank Teller** or **Online System** sends the request to the COBOL-based mainframe system.
   - The system generates a **unique account number** based on predefined algorithms.
   - The account is flagged as either **savings** or **checking**, with different business rules applying based on the account type.
   - The system stores the following details:
     - Customer’s **name**, **address**, **email** (if digital records are supported).
     - **Account type** (checking/savings).
     - **Initial deposit**.
     - **Interest rate** for savings accounts (based on business rules).
     - Flags for **joint accounts** or **special account status** (student accounts, senior citizen accounts, etc.).

   **Business Rules for Account Creation**:

   - **Minimum balance** for opening an account:
     - For savings accounts: Minimum of **$100**.
     - For checking accounts: No minimum balance required but a deposit is recommended.
   - **Interest rate for savings accounts**:
     - Based on **tiered structure**:
       - Balances **up to $1,000**: **0.5%** annual interest.
       - Balances between **$1,001 and $10,000**: **1.0%** annual interest.
       - Balances over **$10,000**: **1.5%** annual interest.
   - **Interest is compounded monthly**.
   - **Checking accounts do not accrue interest**.

2. **Deposit of Funds**:

   - The **Customer** makes a **deposit** into their account either through the teller, ATM, or online banking.
   - The **Bank Teller** or **Automated System** initiates the deposit transaction in the core banking system.
   - The **COBOL program** updates the account’s **current balance** by adding the deposit amount.
   - The system records the transaction in the account's **transaction history** and updates the timestamp for the last transaction.

   **Business Rules for Deposits**:

   - **Deposit limits**: No maximum deposit limit, but deposits above **$10,000** may trigger a **regulatory hold** or require additional documentation.
   - **Funds availability**:
     - **Cash deposits** are available **immediately**.
     - **Check deposits** may be held for **2 business days** before they are available in the account.

3. **Interest Rate Calculation (Savings Accounts)**:

   - The core system runs a **monthly batch job** at the end of each month to calculate interest on all **savings accounts**.
   - The system reads the current balance for each account and applies the corresponding **interest rate** based on the balance tier.
   - **Interest earned** is added to the account balance.
   - The system logs an interest transaction in the **account statement** and updates the **balance**.

   **Business Rules for Interest Calculation**:

   - **Interest formula**:  
     \[
     \text{Interest Earned} = \frac{\text{Current Balance} \times \text{Interest Rate}}{12}
     \]
     where the interest rate is based on the current balance and the tier.
   - Interest is **accrued daily** but **credited monthly**.
   - For accounts with **zero balance**, no interest is calculated.
   - **Compounding interest**: The system compounds interest monthly, adding the interest earned to the balance before the next month's calculation.

4. **Withdrawals and Debit Transactions**:

   - The **Customer** makes a withdrawal either at a branch, ATM, or via **online banking**.
   - The **Bank Teller** or **Automated System** sends a debit request to the core banking system.
   - The system checks the **account balance** and verifies if the withdrawal is allowed (i.e., no overdraft protection for certain accounts).
   - If sufficient funds are available, the system **deducts** the withdrawal amount from the account balance.
   - The system logs the withdrawal in the account’s **transaction history** and updates the balance.

   **Business Rules for Withdrawals**:

   - **Daily ATM withdrawal limit**: $500 per day.
   - **Fee for out-of-network ATM withdrawals**: $3 per transaction.
   - **Overdraft protection**: Enabled only for accounts with linked savings.
     - **Overdraft fee**: $35 per occurrence if overdraft protection is not enabled.
   - **Minimum balance** for savings accounts:
     - If the savings account balance falls below **$100**, a **$10 monthly fee** is applied.
     - No minimum balance for checking accounts, but overdraft fees apply.

5. **Fund Transfers**:

   - The **Customer** requests a transfer of funds between two of their accounts or to another customer’s account.
   - The **Bank Teller** or **Online System** initiates the transfer request.
   - The system verifies the **origin account balance** and checks if the funds are sufficient for the transfer.
   - The system **debits** the origin account and **credits** the destination account.
   - The system logs both the **debit** and **credit** transactions in their respective **account histories**.

   **Business Rules for Fund Transfers**:

   - **Internal transfers** (between the customer’s own accounts) are processed **immediately**.
   - **External transfers** (to another customer) may take up to **24 hours** to process.
   - **Transfer limits**:
     - **Daily limit for internal transfers**: $10,000.
     - **Daily limit for external transfers**: $5,000.

6. **Account Closure**:

   - The **Customer** requests account closure either by visiting the branch or through customer service.
   - The **Bank Teller** or **Back-Office Staff** initiates the account closure process in the core banking system.
   - The system verifies that the account balance is **zero** before allowing closure.
   - If there are any remaining funds, the system processes a **final disbursement** (either by check or wire transfer).
   - The system sets the account’s status to **closed**, and the account is no longer accessible for transactions.

   **Business Rules for Account Closure**:

   - **Balance verification**: The account balance must be **zero** before closure.
   - **Outstanding fees**: Any outstanding fees must be paid before closure.
   - **Final disbursement**: If funds remain in the account, they are disbursed via check or wire transfer.
   - **Account reactivation**: Closed accounts cannot be reactivated; a new account must be opened.

7. **Fees and Charges**:

   - The system processes **monthly account maintenance fees** and **transaction-based fees** (e.g., for out-of-network ATM withdrawals or overdrafts).
   - The system deducts these fees from the account balance and logs the fee deduction in the **transaction history**.

   **Business Rules for Fees**:

   - **Monthly maintenance fee**:
     - **Savings accounts**: $10 per month if the balance falls below $100.
     - **Checking accounts**: No monthly fee if the customer maintains an average daily balance of $500; otherwise, a **$5 monthly fee** applies.
   - **Overdraft fee**: $35 per occurrence.
   - **ATM fees**:
     - **In-network withdrawals**: Free.
     - **Out-of-network withdrawals**: $3 per transaction.

---

### **Alternate Flow 1 (Insufficient Funds)**:

1. If the customer attempts to withdraw or transfer funds but the **available balance is insufficient**, the system rejects the transaction.
2. An error message is displayed (e.g., "Insufficient funds").
3. If the account has **overdraft protection**, the system processes the transaction and applies the **overdraft fee**.
4. The system updates the account balance to reflect the overdraft.

---

### **Exceptions**:

1. **System Outage**:
   - If the mainframe system experiences downtime or failure, all banking transactions must be logged manually and entered into the system once it is back online.
2. **Regulatory Holds**:
   - Large transactions (e.g., deposits over $10,000

### **Alternate Flows**

---

#### **Alternate Flow 2 (Interest Rate Change)**:

1. The bank's management decides to adjust the interest rates for savings accounts.
2. The system administrator updates the interest rate parameters in the COBOL program.
3. When the monthly interest calculation job runs, it applies the new rates to all applicable accounts from the effective date of the change.
4. The system logs the change in interest rates in an audit log for regulatory compliance.

---

#### **Alternate Flow 3 (Account Creation – Invalid Information)**:

1. If the customer provides incomplete or invalid information (e.g., invalid date of birth, missing city or state), the system prompts the teller or customer to correct the data before proceeding.
2. The account creation process is paused until valid information is provided.
3. If the customer cannot provide valid information, the account creation process is cancelled.

---

#### **Alternate Flow 4 (Customer Attempts Withdrawal During Maintenance Window)**:

1. If a customer attempts to make a withdrawal during a **scheduled system maintenance window**, the system rejects the transaction and displays a message: "System is temporarily unavailable, please try again later."
2. The system does not deduct any funds or log any transaction.
3. The customer must attempt the transaction again once the system is back online.

---

#### **Alternate Flow 5 (Joint Account Transfer)**:

1. A customer requests to transfer funds from a joint account.
2. The system prompts the teller or online interface to verify authorization from both account holders.
3. Once both account holders confirm, the system processes the transfer.
4. If one account holder does not authorize the transfer, the system cancels the request.

---

#### **Alternate Flow 6 (Overdraft Protection Activated)**:

1. A customer with overdraft protection tries to withdraw more than their available balance.
2. The system checks if the linked savings account has sufficient funds to cover the overdraft.
3. If so, the system transfers the necessary funds from the savings account, deducts the overdraft fee, and allows the withdrawal.
4. If the savings account has insufficient funds, the system rejects the withdrawal request.

---

#### **Alternate Flow 7 (Transfer to External Bank)**:

1. A customer requests a transfer of funds to an external bank account.
2. The system verifies that the destination bank details are correct and meets the compliance standards for external transfers.
3. If any details are incorrect (e.g., invalid routing number or account number), the system rejects the transfer request and prompts the customer to correct the information.
4. Once the information is verified, the transfer is scheduled and may take up to 3 business days to complete.

---

#### **Alternate Flow 8 (Account Closing with Non-Zero Balance)**:

1. If the customer tries to close an account that still has a non-zero balance, the system does not immediately close the account.
2. The system prompts the customer to either withdraw the remaining funds or transfer them to another account.
3. Once the balance reaches zero, the system completes the closure process.
4. If the customer fails to transfer or withdraw funds within 30 days, the account is flagged for administrative closure with the remaining funds transferred to an escheatment account.

---

#### **Alternate Flow 9 (Fee Waiver Request)**:

1. A customer disputes a fee (e.g., overdraft or out-of-network ATM fees) and requests a waiver.
2. The teller or bank staff sends a waiver request to the system.
3. The system checks the customer’s account history and applies predefined business rules to decide whether the fee can be waived (e.g., first-time offense or long-time customer with no past overdrafts).
4. If the waiver is approved, the system reverses the fee and logs the adjustment in the transaction history.

---

#### **Alternate Flow 10 (Duplicate Transaction Detected)**:

1. A customer mistakenly submits the same transaction twice (e.g., two identical fund transfers).
2. The system detects that the second transaction is identical to a transaction processed within the last 5 minutes (same account, same amount, same destination).
3. The system flags the duplicate transaction and does not process it.
4. An alert is sent to the bank’s fraud detection system, and the customer is notified of the potential duplication.

---

#### **Alternate Flow 11 (Account Reopening Request)**:

1. A customer requests to reopen an account that was closed within the last 30 days.
2. The system verifies that the account balance is zero and that no legal or regulatory holds are preventing reopening.
3. The system reactivates the account, restoring its status and transaction history.
4. If more than 30 days have passed, the customer is required to open a new account instead of reopening the old one.

---

#### **Alternate Flow 12 (Insufficient Data for Interest Calculation)**:

1. During the monthly interest calculation batch job, the system encounters an account with missing or corrupted balance data.
2. The system skips interest calculation for that account and logs an error in the system logs.
3. A system administrator is notified to manually correct the account data.
4. Once the data is corrected, the system recalculates the interest and applies it to the account.

---

---

### **Exceptions**

---

#### **Exception 1 (System Crash)**:

1. The mainframe system crashes during a high-volume transaction processing period.
2. All pending transactions are halted, and customer accounts may show incorrect balances.
3. The system administrator triggers a rollback mechanism to restore the system to its last stable state using the last known backup.
4. Affected customers are notified, and any failed transactions are reprocessed once the system is back online.

---

#### **Exception 2 (Duplicate Account Number)**:

1. During account creation, the system generates a duplicate account number due to a conflict in the account numbering algorithm.
2. The system cancels the account creation process and notifies the bank staff of the issue.
3. The bank staff manually generates a unique account number and re-initiates the account creation process.

---

#### **Exception 3 (Invalid Interest Rate Applied)**:

1. During interest rate recalculations, a COBOL program bug applies a negative interest rate to some savings accounts.
2. The system administrator is alerted, and the system reverses any negative interest charges.
3. A patch is applied to the interest calculation module to prevent further errors.
4. Affected accounts are corrected, and customers are notified.

---

#### **Exception 4 (Lost Transaction Records)**:

1. A power failure during the transaction processing cycle results in the loss of some transaction records.
2. The system flags these accounts for review and reconciliation.
3. Bank staff manually review the transaction logs, and missing transactions are re-entered.
4. Customers are notified if any of their transactions were affected.

---

#### **Exception 5 (Unauthorized Access Detected)**:

1. The system detects an unauthorized login attempt to a customer’s account from an unrecognized IP address.
2. The system locks the account and prevents further access until the customer verifies their identity.
3. An alert is sent to the customer and the bank’s security team for investigation.

---

#### **Exception 6 (Data Corruption in Transaction History)**:

1. A software bug causes corruption in a customer’s transaction history, making it unreadable.
2. The system logs the corruption and automatically attempts to recover the transaction history from backup.
3. If recovery fails, the customer is notified, and a bank representative is assigned to manually investigate and restore the records.

---

#### **Exception 7 (Regulatory Hold on High-Value Transfer)**:

1. A customer initiates a transfer exceeding the legal limit of $10,000.
2. The system automatically places the transaction on hold pending review by the compliance team.
3. The customer is notified of the hold, and the transaction is reviewed within 24 hours before being processed.

---

#### **Exception 8 (Inconsistent Balance After Transfer)**:

1. A bug in the COBOL transfer module results in inconsistent balances between the origin and destination accounts after a transfer.
2. The system automatically flags the accounts for manual reconciliation.
3. The affected accounts are locked from further transactions until the issue is resolved.
4. Customers are notified of the issue and provided with a timeline for resolution.

---

#### **Exception 9 (Transaction Duplication Due to Network Error)**:

1. A network error during an online banking session causes a debit transaction to be duplicated.
2. The system detects the duplicate transaction and reverses the second debit.
3. The customer is notified, and their balance is corrected.
4. The issue is logged for review by the IT team.

---

#### **Exception 10 (Outdated Customer Information)**:

1. The system attempts to process a large wire transfer but finds that the customer’s address on file is incomplete or outdated.
2. The system places a hold on the transaction until the customer updates their information.
3. Once the update is completed, the transaction is reprocessed.
4. If the customer does not update their information within 5 business days, the transaction is cancelled.

---

#### **Exception 11 (Compliance Violation Detected)**:

1. During a routine audit, the system detects a potential compliance violation (e.g., missing KYC documentation for an account).
2. The system flags the account and temporarily suspends all transactions.
3. The compliance team is notified, and the customer is asked to provide the missing documentation before the account can be reactivated.

---

#### **Exception 12 (Insufficient Resources on Mainframe)**:

1. The mainframe’s resources are exhausted due to a spike in transaction volume.
2. The system halts all new transactions until additional resources are allocated.
3. Affected transactions are queued and processed once the system recovers.

---

#### **Exception 13 (Fee Calculation Error)**:

1. The system miscalculates the fee for an international transfer due to incorrect exchange rate data.
2. The incorrect fee is

applied, and the customer is overcharged. 3. The system flags the discrepancy, refunds the excess fee, and notifies the customer. 4. Exchange rate data is updated, and the issue is logged for further review.

---

#### **Exception 14 (Transaction Rolled Back After Failure)**:

1. A transfer between two accounts fails midway due to a system timeout.
2. The system automatically rolls back both the debit and credit portions of the transaction to their original states.
3. The customer is notified, and the transaction can be retried later.

---

#### **Exception 15 (Account Frozen Due to Suspicious Activity)**:

1. The system detects unusual transaction patterns (e.g., multiple high-value transfers in quick succession).
2. The customer’s account is frozen pending further investigation by the bank’s fraud team.
3. The customer is notified and asked to verify the suspicious transactions.

---

#### **Exception 16 (Overdraft Protection Failed to Apply)**:

1. A customer with overdraft protection makes a withdrawal that should trigger a transfer from their linked savings account.
2. Due to a system error, the overdraft protection fails, and the withdrawal is rejected.
3. The customer is notified, and the system corrects the issue, allowing the withdrawal to be processed.
4. The overdraft protection is manually applied to prevent recurrence.

---

#### **Exception 17 (Scheduled Payment Failure)**:

1. A customer’s scheduled payment (e.g., loan repayment) fails due to insufficient funds in their account.
2. The system sends a notification to the customer, and the payment is reattempted the next business day.
3. If the payment fails again, a late fee is applied, and the system logs the failure.

---

#### **Exception 18 (Duplicate Account Closure Request)**:

1. A customer mistakenly submits two account closure requests for the same account.
2. The system detects the duplicate request and only processes the first one.
3. The customer is notified that the account is already in the process of being closed.

---

#### **Exception 19 (Currency Exchange Failure for International Transfer)**:

1. A customer initiates an international transfer, but the system fails to retrieve the current exchange rate from the external exchange rate service.
2. The transaction is put on hold until the exchange rate can be retrieved.
3. The customer is notified of the delay, and the transfer is processed once the issue is resolved.

---

#### **Exception 20 (Legal Hold Prevents Account Closure)**:

1. A customer requests to close their account, but the system detects a **legal hold** on the account (e.g., due to pending litigation or a tax lien).
2. The system prevents the account from being closed and notifies the customer of the legal restriction.
3. The account remains open until the legal hold is lifted.

---

These **alternate flows** and **exceptions** cover a wide variety of operational conditions for a COBOL-based core banking system running on mainframe infrastructure, helping to ensure resilience, accuracy, and regulatory compliance in both standard and edge cases.
