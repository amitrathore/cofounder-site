# Developer Note — Cofounder Navigation & Student Founder Program

**Project:** cofounder.community
**Scope:** New top-level navigation, Student Founder Program section (fully built), two "Coming Soon" audience sections, shared Examples page, and pricing on a Compare Tracks page.
**Status:** Information architecture is final. This note is the implementation spec.

---

## 1. Context (read first)

The current site has a flat nav: `Book · 1B · Ventures · Join`. We're introducing a **paid program for student founders**, with a second buyer (parents) that didn't exist before. The architecture below adds slots for all three audience types from the homepage ("three kinds of builders") while only fully building the Student track now. The other two and the Exchange are honest placeholders that capture interest.

**Two audiences, two voices.** The community pages (1B, Join) speak teen-to-builder. The Program pages speak to **parents**. Keep these voices separate — do not let the existing peer voice bleed into Program copy.

---

## 2. Navigation structure

Replace the current nav with:

```
Book · 1B · Build ▾ · Examples · Join
```

- `Book` — existing, unchanged. Links to `/read/`.
- `1B` — existing, unchanged. Links to `/1b.html`. (This is the thesis + founder page; do NOT relabel or fold it.)
- `Build ▾` — NEW dropdown (see §3).
- `Examples` — NEW top-level (formerly "Ventures"; see §5).
- `Join` — existing CTA button. Links to `/1b.html#join`. This is the FREE community signup. Keep it visually distinct as the primary button.

**Important:** `Join` ≠ program enrollment. Program enrollment uses its own "Apply / Enroll" buttons inside the Student Founders pages. Do not wire the two together or reuse the label.

---

## 3. The `Build ▾` dropdown

Four items. Each shows a status tag. Render the tag visually (small pill/label), not just text.

| Label | Status | Links to | Build now? |
|---|---|---|---|
| Student Founders | Live | `/build/student-founders/` | YES — full build |
| First-Time Founders | Coming Soon | `/build/first-time-founders/` | Placeholder only |
| Repeat Founders | Coming Soon | `/build/repeat-founders/` | Placeholder only |
| The Exchange | Coming Soon | `/build/exchange/` | Placeholder only |

- "Coming Soon" items are clickable and lead to a real placeholder page (§6) — they are NOT disabled/greyed dead links. They capture email interest.
- Optional one-line descriptor under each dropdown item for clarity, e.g. *"Student Founders — the 12-week path to building your own company."* Recommended but not required.

---

## 4. Student Founders section (FULL BUILD)

Base path: `/build/student-founders/`

Page hierarchy:

| Page | Path | Purpose |
|---|---|---|
| Overview | `/build/student-founders/` | Parent-facing pitch. **No pricing on this page.** |
| Founder Track | `/build/student-founders/founder-track/` | Detail page for the ~5 hr/week tier |
| Venture Track | `/build/student-founders/venture-track/` | Detail page for the ~10 hr/week tier |
| Compare Tracks | `/build/student-founders/compare/` | Side-by-side + ALL pricing lives here |
| (Examples is top-level — see §5, do not duplicate here) |

**Page flow / intended funnel:** Overview (desire) → Compare Tracks (price in context) → Apply/Enroll. Primary CTA on Overview and the track pages points to Compare Tracks or Apply, NOT directly to a checkout that shows a bare price.

**Critical rule: pricing appears ONLY on Compare Tracks.** Do not surface prices on Overview, the track detail pages, or the nav. This is deliberate (aspirational-before-price sequencing) — do not "helpfully" add prices elsewhere.

### 4a. Apply / Enroll CTA
- Each Student Founders page has its own "Apply" (Venture) / "Enroll" (Founder) button.
- These are separate from the global `Join` button. Different action, different label, different destination.

---

## 5. Examples page (top-level)

Path: `/examples/` (migrate existing `/ventures/` content here; set up a 301 redirect from `/ventures/` → `/examples/`).

- This is shared proof for ALL three audiences — that's why it's top-level, not nested under Student Founders.
- Structure the page so it can be **filtered or grouped by audience type** (e.g. sections or tags: "Built by students / first-timers / repeat founders"). Not all groups have content yet; build the grouping mechanism so student-built examples are findable without scrolling past large-scale ventures.
- Rationale: a teenager who only sees billion-dollar solopreneur ventures feels "that's not me." Peer examples convert. Make student examples easy to surface.

---

## 6. Placeholder pages (First-Time Founders, Repeat Founders, The Exchange)

Each is a SINGLE page with: a short audience-promise headline + one line of copy + an email capture form ("Notify me" / "Request access"). No other content.

- `/build/first-time-founders/` — promise: self-directed version of the founder journey, build for yourself, your own pace.
- `/build/repeat-founders/` — promise: peers at your level, the new AI-native playbook, early access to the Exchange. Consider "Request access" framing rather than "Notify me."
- `/build/exchange/` — promise: marketplace of tools, agents, templates, services members trade.

Wire each form to the same email-capture backend with a `source` field tagging which page (`first-time`, `repeat`, `exchange`) so interest can be segmented.

---

## 7. Homepage wiring

The homepage already has a "three kinds of builders" section with three cards. Wire each card to its on-ramp:

- First-time builder card → `/build/first-time-founders/`
- Repeat founder card → `/build/repeat-founders/`
- Student card → `/build/student-founders/`

The "Four pillars" homepage section stays as-is. No changes needed there.

---

## 8. Pricing & launch offer (Compare Tracks page only)

Display BOTH tiers side by side. Each tier shows: list price (anchor), founding-cohort price beneath it, the give-back terms, and the cap/deadline.

| Tier | List price | Founding price | Notes |
|---|---|---|---|
| Founder Track | $1,997 | **$1,297** | ~5 hr/week, group mentorship |
| Venture Track | $4,997 | **$3,297** | ~10 hr/week, 1:1 mentor, application-only |

**Founding offer is NOT a generic discount.** Render it as a founding-member deal with conditions:

- List price shown struck-through / as the anchor.
- Founding price shown as the active price.
- **Give-back terms displayed as part of the offer**, e.g.: *"Founding members commit to a testimonial, a case-study writeup of their venture, and program feedback."*
- **Scarcity displayed:** cap + deadline, e.g. *"Founding Cohort — first 20 students · enrollment closes [DATE]."* Make the cap count and deadline editable (config/CMS field, not hardcoded).

**Do not render the founding price as a sitewide sale banner or "50% OFF" style promo.** The discount is earned and time-boxed; presenting it as a blowout sale undercuts the premium positioning. Keep it on Compare Tracks, framed as founding membership.

**Offer payment plans** for both tiers (especially Venture at $3,297) — significantly raises conversion at this price point. Implement as an option on the enrollment flow.

---

## 9. Implementation checklist

- [ ] New nav: `Book · 1B · Build ▾ · Examples · Join`
- [ ] `Build ▾` dropdown with 4 items + status pills (1 Live, 3 Coming Soon)
- [ ] Student Founders: Overview, Founder Track, Venture Track, Compare Tracks pages
- [ ] Pricing rendered ONLY on Compare Tracks
- [ ] Founding offer block: anchor price + founding price + give-back terms + cap/deadline (CMS-editable)
- [ ] Payment-plan option in enrollment flow
- [ ] Apply/Enroll CTAs distinct from global Join
- [ ] `/examples/` page with audience grouping/filtering + 301 from `/ventures/`
- [ ] 3 placeholder pages with email capture + `source` tagging
- [ ] Homepage "three builders" cards wired to on-ramps
- [ ] Confirm `Join` still points to free community signup (`/1b.html#join`)

---

## 10. Things NOT to change / NOT to "optimize"

These are deliberate; flag with product before altering:

1. **No pricing outside Compare Tracks.** Sequencing is intentional.
2. **Don't merge `Join` and program enrollment.** Two different actions/audiences.
3. **Don't fold `1B` into anything** — it's the thesis + founder page and stays top-level.
4. **Don't disable the Coming Soon links** — they capture interest.
5. **Don't render the founding offer as a generic % - off sale** — it's a conditional founding-member deal.
6. **Keep parent voice and teen/community voice separate** across Program vs 1B/Join pages.
