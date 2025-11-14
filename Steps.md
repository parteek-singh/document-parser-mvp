Absolutely — here is **the most complete, practical, ASX-ready announcement taxonomy** you can use for your parser and data marketplace.
This covers **all announcement types** that matter for investors, funds, traders, analytics systems, and news engines.

I have grouped everything into **15 major categories** and **60+ sub-types** exactly the way a real ASX data product or “event classifier” should be designed.

Use this list as the **master schema** for your “Announcement Type Classification Engine”.

---

# ✅ **MASTER LIST OF ASX ANNOUNCEMENT TYPES**

### (Organised into 15 Categories + Sub-Types)

---

# **1. Dividend / Distribution Notices**

### **Type Code: DIVIDEND**

* Interim Dividend (APP 3A.1)
* Final Dividend
* Special Dividend
* Distribution (Trusts)
* DRP Update
* Dividend Currency Election Notice
* Dividend Timetable Change

---

# **2. Capital Raising**

### **Type Code: CAPITAL_RAISING**

#### **A. Equity Raising**

* Placement / Institutional Placement
* Accelerated Non-Renounceable Entitlement Offer (ANREO)
* Rights Issue / Entitlement Offer
* Share Purchase Plan (SPP)
* Prospectus / Offer Document
* Bookbuild Completion
* Capital Raising Results
* Pricing Announcement (Offer Price / Take-up %)

#### **B. Debt Raising**

* Bond Issue (USD / EUR / AUD)
* Syndicated Loan Announcement
* Credit Facility Update
* Debt Refinancing
* Convertible Note Issue

---

# **3. Earnings / Results**

### **Type Code: RESULTS**

* Appendix 4E – Preliminary Final Report
* Appendix 4D – Half-Year Results
* Full-Year Results
* Quarterly Update (non-cashflow)
* Production & Sales Update (for miners)
* Operational Metrics Update
* Key Metrics Update (ARR, Churn, LTV:CAC — for SaaS)

---

# **4. Guidance / Trading Update**

### **Type Code: GUIDANCE**

* Earnings Guidance Update (Upgrade / Downgrade)
* Profit Warning
* Trading Conditions Update
* Revenue/EBITDA Guidance Revision
* Cost Guidance Revision
* Operational Forecast Update
* Production Guidance Update (Resources)

---

# **5. Mergers & Acquisitions**

### **Type Code: MNA**

* Acquisition Announcement
* Divestment / Asset Sale
* Scheme of Arrangement
* Takeover Bid / Offer
* Indicative Proposal
* Binding Agreement
* Due Diligence Update
* Completion Announcement
* Termination of Deal

---

# **6. Appendix 3B / 2A / Equity Securities**

### **Type Code: SECURITIES**

* Appendix 3B – Proposed Issue of Securities
* Appendix 2A – Actual Issue of Securities
* Appendix 3G – Notification of Change in Equity
* Cleansing Notice
* Restricted Securities
* Issue Price Information

---

# **7. Corporate Actions (Non-Raising)**

### **Type Code: CORPORATE_ACTION**

* Share Consolidation / Split
* Change of Company Name
* Change of Ticker Code
* Buyback – On-market
* Buyback – Off-market
* Capital Reduction
* New Constitution
* Change in Purpose / Strategic Shift

---

# **8. Director / Key Executive Changes**

### **Type Code: MANAGEMENT**

* Appendix 3X – Initial Director Interest
* Appendix 3Y – Change in Director Interest
* Appendix 3Z – Final Director Interest
* Director Appointment
* Director Resignation
* CEO/CFO/COO Appointment
* CEO/CFO Departure
* Key Management Personnel Update
* Executive Remuneration Update

---

# **9. Cashflow Reports**

### **Type Code: CASHFLOW**

* Appendix 4C – Quarterly Cashflow (SaaS / small caps)
* Appendix 5B – Mining Exploration Quarterly
* Quarterly Activities Report (combined with cashflow)
* Estimated Cash Burn
* Liquidity Position

---

# **10. Operational Announcements**

### **Type Code: OPERATIONS**

#### **Resources**

* Exploration Results (JORC)
* Drilling Update
* Production Report
* Site Incident / Fatality
* Mine Shutdown / Restart
* Resource/Reserve Upgrade

#### **Technology / Retail / Other**

* Customer Acquisition Update
* New Product Launch
* Infrastructure Upgrade
* Supply Chain Disruption
* Operational Issue / Outage

---

# **11. Trading Halts & Suspensions**

### **Type Code: TRADING_STATUS**

* Trading Halt
* Voluntary Suspension
* ASX-imposed Suspension
* Lift of Suspension
* Resume Trading Notice
* Pause / Pending Announcement

---

# **12. Notices of Meeting / Corporate Governance**

### **Type Code: GOVERNANCE**

* Notice of AGM
* Notice of EGM
* Meeting Materials
* Chair’s Address
* CEO Address
* Proxy Votes
* Results of Meeting
* Constitution Amendments

---

# **13. Regulatory / Compliance**

### **Type Code: REGULATORY**

* ASIC Notice
* ASX Query Response
* ASX Price & Volume Query
* Compliance Update
* Change in Listing Rules Compliance
* Court Orders (Schemes, Approvals)
* Approval for Listing / Admission

---

# **14. Strategic Announcements**

### **Type Code: STRATEGIC**

* Major Contract Win
* Major Contract Loss
* Strategic Partnership
* Joint Venture (JV)
* Memorandum of Understanding (MOU)
* Market Expansion / New Region
* Operational Restructuring
* Major Customer Signed
* Government Grant / Funding

---

# **15. Miscellaneous / Other**

### **Type Code: OTHER**

* Investor Presentation
* Market Update
* Media Release
* Sustainability / ESG Update
* Corporate Overview
* Non-price-sensitive announcements
* Internal Reorganisation

---

# 🎯 What You Should Build in Your Parser

For each announcement you should classify into:

```json
{
  "category": "CAPITAL_RAISING",
  "type": "PLACEMENT"
}
```

or another example:

```json
{
  "category": "DIVIDEND",
  "type": "INTERIM_DIVIDEND"
}
```

### This helps you:

* Route documents to the correct **extractor module**
* Extract KPIs correctly
* Build structured JSON for your ASX Data Marketplace
* Trigger analytics / signals
* Build your "Smart Announcement Feed"

---

# ⭐ If You Want

I can generate:

### ✔ **The full JSON taxonomy (complete hierarchy)**

Perfect for your database.

### ✔ **Mapping rules: Which keywords → which announcement types**

### ✔ **All extractor templates (dividend, placement, SPP, guidance, M&A, 4C cashflow, production updates, trading halts...)**

### ✔ **A classifier model prompt (LLM-based)**

that predicts category + type with 95%+ accuracy.

Just tell me what you want next.
