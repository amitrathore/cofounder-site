# Dev Note: Add Tally Forms for Cofounder Student Founders

The site is wired for Tally, but the live Tally forms still need to be created. Create the forms in Tally, then replace the placeholder form URLs in `assets/forms.js`.

Tally MCP docs: <https://developers.tally.so/api-reference/mcp>

## Product Context

Cofounder is introducing a paid Student Founders program while preserving the existing free community signup.

Important distinction:

- Global `Join` is the free community signup and must keep pointing to `/1b.html#join`.
- Student Founders `Enroll` and `Apply` are paid-program actions and must use separate Tally forms.

The program pages speak to parents. The form copy should feel parent-facing, serious, and confidence-building. Avoid teen/community language like "join the crew" or generic startup hype. The parent should feel: this is structured, selective where appropriate, respectful of their student's ambition, and thoughtful about time commitment.

## Site Wiring

The site expects three Tally form URLs in `assets/forms.js`:

```js
window.CofounderForms = {
  founderEnroll: "https://tally.so/r/REPLACE_FOUNDER_ENROLL",
  ventureApply: "https://tally.so/r/REPLACE_VENTURE_APPLY",
  interest: "https://tally.so/r/REPLACE_COMING_SOON_INTEREST"
};
```

Replace only the `REPLACE_*` URLs after the forms exist.

The site already passes query parameters into links and embeds:

- `source`
- `track`
- `payment_plan`

Set these up as hidden fields in Tally so submissions can be segmented.

## Form 1: Founder Track Enrollment

Config key: `founderEnroll`

Use for:

- `/build/student-founders/founder-track/`
- `/build/student-founders/compare/`

Audience: parent or guardian ready to enroll a student in the lower-time-commitment track.

Tone: direct, warm, structured. This is enrollment, not a competitive application, but still signal seriousness.

Suggested title:

`Enroll in the Founder Track`

Suggested description:

`A 12-week path for students who can commit about five hours a week to building a serious venture-shaped project with group mentorship and weekly milestones.`

Recommended sections:

1. Parent/guardian contact
2. Student profile
3. Readiness and fit
4. Payment preference
5. Final confirmation

Recommended fields:

- Parent/guardian full name
- Parent/guardian email
- Parent/guardian phone number
- Student full name
- Student age
- Student grade/year
- Student school
- What is your student interested in building, exploring, or solving?
- Has your student already built, launched, sold, published, organized, or experimented with anything? Give examples.
- What would make this program a successful experience for your student?
- Can your student commit about five hours per week for 12 weeks?
- Preferred payment option
- Anything we should know about schedule, learning style, or support needs?

Suggested multiple-choice values for payment:

- Pay in full
- Payment plan
- Not sure yet

Hidden/query fields:

- `source`
- `track`
- `payment_plan`

Expected values:

- `track=founder`
- `source=founder-track` from the Founder Track page
- `source=compare` from Compare Tracks
- `payment_plan=pay-in-full`
- `payment_plan=payment-plan`

Suggested confirmation message:

`Thank you. We received your Founder Track enrollment details and will follow up with next steps for the founding cohort.`

## Form 2: Venture Track Application

Config key: `ventureApply`

Use for:

- `/build/student-founders/venture-track/`
- `/build/student-founders/compare/`

Audience: parent or guardian applying on behalf of a student who may be ready for the deeper, application-only track.

Tone: selective, respectful, ambitious. Make the application feel like a thoughtful fit check, not a bureaucratic intake form.

Suggested title:

`Apply for the Venture Track`

Suggested description:

`For students ready to commit about ten hours a week to a deeper company build with 1:1 mentor attention. We use this application to understand fit, readiness, and the kind of venture support the student needs.`

Recommended sections:

1. Parent/guardian contact
2. Student profile
3. Venture readiness
4. Time commitment and mentor fit
5. Payment preference if accepted

Recommended fields:

- Parent/guardian full name
- Parent/guardian email
- Parent/guardian phone number
- Student full name
- Student age
- Student grade/year
- Student school
- What venture, problem, audience, or domain is the student most interested in?
- What has the student already done to explore this idea?
- Share links to anything relevant: prototype, website, GitHub, writing, video, social, store, deck, or project page.
- What makes the student ready for a more intensive track?
- Can the student commit about ten hours per week for 12 weeks?
- What kind of mentor support would be most useful?
- Why Venture Track instead of Founder Track?
- Preferred payment option if accepted
- Anything else we should know while reviewing fit?

Suggested multiple-choice values for payment:

- Pay in full if accepted
- Payment plan if accepted
- Not sure yet

Hidden/query fields:

- `source`
- `track`
- `payment_plan`

Expected values:

- `track=venture`
- `source=venture-track` from the Venture Track page
- `source=compare` from Compare Tracks
- `payment_plan=pay-in-full`
- `payment_plan=payment-plan`

Suggested confirmation message:

`Thank you. We received the Venture Track application and will review it for fit with the founding cohort.`

## Form 3: Coming Soon Interest

Config key: `interest`

Use for:

- `/build/first-time-founders/`
- `/build/repeat-founders/`
- `/build/exchange/`

Audience: three different future buyer/user groups. Use one shared form, but let the hidden `source` field segment intent.

Tone: light but still premium. These are placeholders, so the form should be short and easy to finish.

Suggested title:

`Request early access`

Suggested description:

`Tell us what you are building toward. We will use this to prioritize early access as new Cofounder tracks and the Exchange open up.`

Recommended fields:

- Name
- Email
- Which best describes you?
- What are you hoping to build, learn, or access?
- Optional: website, LinkedIn, project, or company URL

Suggested multiple-choice values for "Which best describes you?":

- First-time founder
- Repeat founder
- Interested in the Exchange
- Parent of a student founder
- Other

Hidden/query fields:

- `source`

Expected values:

- `source=first-time`
- `source=repeat`
- `source=exchange`

Suggested dynamic copy by source, if easy in Tally:

- First-time: `Get notified when the self-directed founder journey opens.`
- Repeat: `Request access to the repeat founder track and early Exchange opportunities.`
- Exchange: `Request early access to the marketplace of tools, agents, templates, and services.`

Suggested confirmation message:

`Thanks. We received your request and will use this to prioritize early access.`

## Founding Cohort Context

The Compare Tracks page frames pricing as a founding-member offer, not a generic sale.

Current site copy is configured in `assets/program-config.js`:

```js
window.CofounderProgram = {
  foundingCohortCap: 20,
  enrollmentDeadline: "August 31, 2026",
  giveBackTerms: "Founding members commit to a testimonial, a case-study writeup of their venture, and program feedback."
};
```

Do not present the offer inside Tally as a discount code or "50% off" sale. Use founding cohort language:

- Founding cohort
- Founding-member price
- First 20 students
- Includes give-back commitment
- Enrollment deadline

## Tally Implementation Notes

For each form:

- Add hidden fields matching the query parameter names exactly.
- Preserve query parameters on embedded and linked forms.
- Keep required fields reasonable; high-friction questions should be optional unless needed for fit.
- Use one question per screen when it improves completion, especially for Venture Track.
- Use conditional logic if available for payment preference and source-specific copy.
- Avoid asking for payment details directly in Tally unless payment processing is intentionally configured there.

After creating forms:

1. Replace the three placeholders in `assets/forms.js`.
2. Test these URLs:
   - `/build/student-founders/compare/`
   - `/build/student-founders/founder-track/`
   - `/build/student-founders/venture-track/`
   - `/build/first-time-founders/`
   - `/build/repeat-founders/`
   - `/build/exchange/`
3. Confirm Tally submissions include the expected hidden fields.
4. Confirm global `Join` still goes to `/1b.html#join`, not a paid-program form.
