# Spam Words Exclude List for Email Copy

**Last Updated:** 2026-01-27
**Source:** Mailmeteor, industry research, deliverability best practices
**Usage:** Check all email copy against this list before launching campaigns

## Quick Rules

1. **Never use % symbol** → spell out "percent" 
2. **Avoid numeric stats in subject lines** (81%, 100%, 50%)
3. **No ALL CAPS** anywhere
4. **No excessive punctuation** (!!!, ???)
5. **No "Re:" in first email** (fake threading)

---

## 🚨 URGENCY WORDS (High Risk)

These pressure the reader and trigger spam filters:

- Act now
- Act immediately
- Action required
- Apply now
- Before it's too late
- Call now
- Click here
- Click now
- Contact us immediately
- Deal ending soon
- Don't delay
- Don't hesitate
- Don't miss out
- Expire / Expires today
- Final call
- For instant access
- Get it now
- Hurry up
- Immediately
- Limited time
- Now only
- Offer expires
- Once in lifetime
- Order now
- Please read
- Supplies are limited
- Take action now
- This won't last
- Time limited
- Top urgent
- Urgent
- What are you waiting for?
- While supplies last
- ASAP

---

## 🔞 SHADY WORDS (High Risk)

Ethically/legally questionable - major red flags:

- As seen on
- Confidential
- Dear friend
- Dear [generic]
- Financial
- Finance
- Hidden
- Investment
- Multi-level marketing
- MLM
- No catch
- No cost
- No credit check
- No fees
- No gimmick
- No obligation
- No purchase necessary
- No questions asked
- No strings attached
- Not spam
- Obligation
- Off shore
- Per month / Per week / Per year
- Pre-approved
- Private
- Privately owned
- Secret
- This isn't spam
- Undisclosed
- Unsecured
- Why pay more?

---

## 🤩 OVERPROMISE WORDS (Medium-High Risk)

Exaggerated claims that sound too good to be true:

- #1
- 100% (free, guaranteed, satisfied, etc.)
- Amazing
- Bargain
- Be amazed
- Be your own boss
- Best deal
- Best offer
- Best price
- Best rates
- Big bucks
- Bonus
- Can't live without
- Double your [money/income/cash]
- Drastically reduced
- Earn extra cash
- Extra income
- Fantastic
- Fast cash
- Financial freedom
- Free (especially "free money", "free gift")
- Guarantee / Guaranteed
- Incredible
- Instant [earnings/income/savings]
- Join millions
- Lowest price
- Make money
- Million dollars
- Money-back guarantee
- Prize
- Promise
- Pure profit
- Risk-free
- Satisfaction guaranteed
- Save big money
- Special promotion
- The best
- Thousands
- Unbeatable offer
- Unbelievable
- Unlimited
- Will not believe your eyes
- Winner
- Wonderful
- You won't believe

---

## 💰 MONEY WORDS (Medium Risk)

Use sparingly and in context:

- $$$
- €€€
- £££
- 50% off
- Affordable
- Avoid bankruptcy
- Bankruptcy
- Billion / Billionaire
- Cash / Cash bonus / Cash out
- Casino
- Cents on the dollar
- Cheap
- Cost / Costs
- Credit / Credit card
- Debt
- Discount
- Dollars
- Earn $ / Earn cash
- Easy terms
- F r e e (spaced out)
- For free
- For just $
- Free access / trial / membership
- Full refund
- Giveaway
- Income
- Insurance
- Investment
- Loans
- Make $
- Money
- Mortgage
- Offer
- Only $
- Price
- Profits
- Quote
- Refinance
- Revenue
- Save $
- Subject to credit
- US Dollars
- Your income

---

## 💬 UNNATURAL WORDS (Low-Medium Risk)

Words that don't feel natural in conversation:

- Accept credit cards
- Accordance with
- Accordingly
- Billing / Billing address
- Card accepted
- Check or money order
- Click below
- Click me
- Click this link
- Click to get
- Click to remove
- Dear [anything]
- For you
- Here
- Increase your
- Info you requested
- Information you requested
- Instance
- Kindly
- Maintains
- Name:
- Please
- Regarding
- Remove
- Reply
- Request
- Rofl
- See for yourself
- Success
- Terms and conditions
- They're
- Undisclosed recipient
- Valorem
- Web
- Weight
- What are you waiting for?
- While stocks last

---

## 📧 SUBJECT LINE SPECIFIC

### Never use in subject lines:
- % symbol (use "percent")
- Numbers with claims (81% faster → "significantly faster")
- Re: or Fwd: (if not actually a reply/forward)
- ALL CAPS words
- Multiple exclamation marks
- Question marks + exclamation (really?!)
- Brackets with urgency [URGENT] [ACTION REQUIRED]
- Emojis (some filters flag these)

### Safer alternatives:
| Instead of | Use |
|------------|-----|
| 81% faster | significantly faster / much faster |
| 100% guaranteed | fully backed / we stand behind |
| Free trial | try it out / test drive |
| Act now | when you're ready |
| Click here | learn more / see how |
| Limited time | available through [date] |
| Best price | competitive pricing |
| Make money | grow revenue |

---

## ✅ TESTING WORKFLOW

1. **Before sending ANY campaign:**
   - Go to https://mailmeteor.com/spam-checker
   - Paste full email body (subject + body)
   - Fix ALL flagged words
   - Re-test until score is "Good" or better

2. **Compare variants:**
   - If one variant gets 0 replies and another gets replies
   - Test both in spam checker
   - The 0-reply version likely has more spam words

3. **Subject line check:**
   - No % symbols
   - No numeric claims
   - No urgency words
   - Keep it conversational

---

## 🎯 HYGRAPH SPECIFIC FINDINGS

From campaign analysis (2026-01-27):

**Steps with 0 replies (likely spam):**
- Step 4212: "{FIRST_NAME} - 81% faster" ← **% symbol flagged**
- Step 4213: "BioCentury's content approach"
- Step 4201, 4202, 4206, 4209, 4214

**Steps getting replies (passing filters):**
- Step 4203: "Healthcare content at scale"
- Step 4208: "{FIRST_NAME}- compliance question"

**Action:** Pull body copy from failing steps, run through spam checker, identify and replace flagged words.

---

## 📚 REFERENCES

- Mailmeteor Spam Checker: https://mailmeteor.com/spam-checker
- Mailmeteor Spam Words List: https://mailmeteor.com/blog/spam-words
- Gmail Deliverability Guide: https://mailmeteor.com/blog/gmail-deliverability
