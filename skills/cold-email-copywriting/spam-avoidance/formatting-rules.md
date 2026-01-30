# Email Formatting Rules

Formatting affects deliverability as much as word choice. Follow these rules.

---

## Structure Rules

### 1. Plain Text Over HTML
- Most cold email tools send plain text or minimal HTML
- Avoid rich formatting (colors, fonts, backgrounds)
- No embedded images in cold emails
- Links should be minimal (1 max, or none)

### 2. Short Paragraphs
```
❌ Long block of text that goes on and on for multiple sentences without any breaks making it hard to read and easy to skip over entirely.

✅ Short paragraphs.

One idea each.

Easy to scan.
```

### 3. Line Length
- Keep lines under 60 characters when possible
- Avoid long unbroken sentences
- Natural breaks at phrase boundaries

### 4. No Excessive Punctuation
```
❌ This is amazing!!!
❌ What do you think???
❌ Check this out...

✅ This is solid.
✅ What do you think?
✅ Check this out.
```

---

## Subject Line Rules

### Length
- **Ideal:** 4-7 words
- **Max:** 50 characters
- **Avoid:** Truncation on mobile

### Capitalization
```
❌ FREE CONSULTATION INSIDE
❌ You Won't BELIEVE This
❌ URGENT: Read This Now

✅ site navigation question
✅ quick question about your website
✅ your enrollment journey
```

**Style:** Sentence case or lowercase. Never title case for cold email.

### No Triggers
```
❌ Re: (fake threading)
❌ Fwd: (fake forwarding)
❌ [URGENT]
❌ [ACTION REQUIRED]
❌ 🔥 (emojis)

✅ {topic} at {COMPANY}
✅ quick question about {topic}
```

---

## Body Rules

### Opening Line
- First word: `{FIRST_NAME}` or reference to prospect
- No greetings (Hi, Hey, Hello, Dear)
- Immediately relevant to recipient

```
❌ Hi {FIRST_NAME}, I hope this finds you well.
❌ Hello! My name is John and I work at...
❌ Dear Sir/Madam,

✅ {FIRST_NAME}, can prospects at {COMPANY} actually find...
✅ {FIRST_NAME}, what if students at {COMPANY} could...
```

### Links
- **Ideal:** Zero links in cold email
- **Max:** One link if necessary
- **Format:** Full URL, not hyperlinked text
- **Never:** "Click here" or similar

```
❌ Click here to learn more
❌ [Learn More](https://...)

✅ More here if useful: example.com/case-study
✅ [No link at all - save for reply conversation]
```

### Signature
- Use `{SENDER_EMAIL_SIGNATURE}` variable
- Keep signature minimal
- No images, banners, or social icons in cold email

---

## Variables

### Required Format
```
{FIRST_NAME}
{COMPANY}
{SENDER_EMAIL_SIGNATURE}
```

### Fallback Handling
If your email tool requires fallbacks:
```
{FIRST_NAME|there}
{COMPANY|your company}
```

But better: **Don't send without valid data.** Empty personalization kills response rates.

### Never Use
```
{{double braces}}
[SQUARE BRACKETS]
<ANGLE BRACKETS>
%PERCENT_SIGNS%
```

---

## Length Guidelines

| Element | Ideal | Max |
|---------|-------|-----|
| Subject line | 4-7 words | 50 chars |
| Body | 50-80 words | 100 words |
| Sentences | 8-12 words | 20 words |
| Paragraphs | 1-2 sentences | 3 sentences |
| P.S. | 1 sentence | 2 sentences |

---

## Mobile Optimization

Over 60% of emails opened on mobile. Test for:
- Subject line truncation (first 30 chars matter most)
- Preview text (first line of body shows in preview)
- Readability without zooming
- Tap targets if any links

---

## Pre-Send Formatting Checklist

```
[ ] Subject line under 50 characters
[ ] Subject line in sentence case (not Title Case or ALL CAPS)
[ ] No fake RE:/FW: prefixes
[ ] Opens with {FIRST_NAME}, (no greeting)
[ ] Body under 100 words
[ ] Paragraphs are 1-2 sentences max
[ ] No excessive punctuation (!! or ???)
[ ] Zero or one link maximum
[ ] No "click here" language
[ ] Signature uses {SENDER_EMAIL_SIGNATURE} variable
[ ] P.S. line is one sentence with proof point
```
