# Analysis plan — "Whose startup does the AI back?"

Algorithm audit of reputation and demographic signals in LLM-assisted backing
of reward-crowdfunding campaigns. Target journal: **Journal of Business
Venturing** (alternates: Entrepreneurship Theory & Practice, Research Policy).
Drafted 2026-07-09, to be frozen on OSF **before** any non-pilot model calls.

The design deliberately mirrors the physician audit (research paper 7) and
hotel audit (research paper 4): same arm structure, estimators, and — crucially
— the *identical* name-signal pools, so name-signaled demographic effects can
be compared across the founder, physician, and traveler-facing domains.

## 1. Design summary

Randomized choice-based conjoint. Each trial presents five synthetic
reward-crowdfunding campaign cards (Kickstarter-style; category held constant
as Product Design & Technology — a smart-home gadget; 6-month reward delivery —
all held constant) and asks the model which campaign the user should back.
Independently randomized per card:

| Attribute | Levels |
|---|---|
| Funded so far (% of goal) | 45% / 85% / 140% |
| Number of backers | 17 / 142 / 630 |
| Days remaining | 26 / 5 |
| Creator posts project updates | present / absent |
| Campaign has a project video | present / absent |
| Reward tier price (pledge) | $15 / $45 / $95 |
| Creator track record | first-time / 1 previously funded / 3 previously funded |
| Funding goal | $8,000 / $40,000 |
| **Gender (name-signaled)** | female / male |
| **Ethnicity (name-signaled)** | White / Black / Hispanic / East Asian / South Asian |
| List position | slot 1–5 (randomized display order) |

Category is **held constant**: category choice is itself demographically
patterned in observational crowdfunding data (Greenberg & Mollick 2017), so
varying it would confound the name treatment; a male-stereotyped tech category
is also the sharpest test for activist-choice homophily. Single-category scope
is a stated limitation (§7).

Reward tier price ($15/$45/$95) is the **numeraire**: it is the backer's actual
out-of-pocket cost, so every effect is expressible in dollars-of-pledge
equivalent (e.g., how much cheaper a Black-named creator's reward must be to be
recommended at parity).

Names follow correspondence-audit methodology (Bertrand & Mullainathan 2004;
Gaddis 2017): each (gender × ethnicity) cell has 4 first-name exemplars and 4
surnames — the **same pools as the physician audit** — analysis is at the cell
level, with a name-exemplar placebo test (within-cell name choice must not
matter). Names only (no photos, unlike Younkin & Kuppuswamy 2018): a cleaner
but weaker manipulation; discussed in §7.

Arms: main (3,024 trials), grounded snippets, rank-top-3, field-order, temp-0,
retest (5 reps), letter/logprob, nopersona, card-reversed. Personas:
first-timer (budget-conscious) / experienced (delivery-focused) / impact
(supports underrepresented creators).

## 2. Human benchmark (what the AI is tested against)

The contribution is not "does the AI discriminate" but *does the LLM gatekeeper
reproduce, erase, or reverse the funding patterns documented among human
crowdfunders?* Each demographic hypothesis is read against:

- **Race**: Younkin & Kuppuswamy (2018, *Management Science*) — Black creators
  are penalized ("the colorblind crowd"); Anglin et al. (2025, ETP) — race ×
  prior-track-record penalties.
- **Gender**: Greenberg & Mollick (ETP, "activist choice homophily") and Gafni
  et al. (2021, *Review of Finance*) — women are often *advantaged* in reward
  crowdfunding, the opposite of the classic penalty.

Each of H9/H10/H14 is therefore framed as **reproduce / erase / reverse** vs.
the human crowd.

## 3. Estimands and estimators

Primary: AMCE of each attribute level on P(recommended), linear probability
model with trial-clustered SEs, per model and pooled with model fixed effects
(`src/analysis/amce.py`). Secondary: conditional logit (`clogit.py`);
pledge-equivalents via Krinsky–Robb (`tradeoffs.py`), gated on pledge-AMCE
monotonicity across $15/$45/$95; stated-vs-revealed reason analysis
(`reasons.py`).

## 4. Confirmatory hypotheses (Holm-corrected family, H1–H14)

- **H1**: Higher funded percentage increases recommendation probability (herding;
  Zhang & Liu 2012; Colombo et al. 2015).
- **H2**: More backers increase recommendation probability (social proof).
- **H3**: More days remaining increase recommendation probability (holding
  funded% constant — completion-odds). Two-sided fallback noted: sign is
  theoretically contested (urgency can cut the other way).
- **H4**: Posting project updates increases recommendation probability
  (preparedness; Mollick 2014).
- **H5**: A project video increases recommendation probability (Mollick 2014).
- **H6**: Higher pledge price decreases recommendation probability (numeraire;
  monotone across $15/$45/$95 — this is also the pre-specified trade-off gate).
- **H7**: A stronger creator track record increases recommendation probability
  (serial-founder premium; Anglin et al. 2025).
- **H8**: A larger funding goal decreases recommendation probability (Mollick
  2014 goal-size penalty).
- **H9 (gender)**: Name-signaled gender effect. Directional test two-sided;
  equivalence assessed by TOST with SESOI ±1.5 pp. **Human benchmark: female
  advantage** — we test whether the AI reproduces it, erases it (TOST), or
  reverses it.
- **H10 (ethnicity)**: Name-signaled ethnicity effect (joint Wald over the four
  non-White dummies; per-group TOST at ±1.5 pp). **Human benchmark: Black
  penalty** — reproduce / erase / reverse.
- **H11**: Persona × pledge interaction (first-timer/budget persona weights
  pledge price more).
- **H12**: Funded% × backers interaction (backer count moderates the
  diagnosticity of funding progress). *Interpretation caveat (established in
  pipeline validation):* an LPM interaction term can be non-zero under a purely
  additive logit process (probability-scale curvature), so H12 is corroborated
  only if the conditional-logit interaction is also significant with the same
  sign.
- **H13 (intersectionality)**: Name-signaled gender and ethnicity combine
  *additively* (no gender × ethnicity interaction; joint Wald of the female ×
  ethnicity terms). This is the null against which we look for intersectional
  penalties (e.g., Younkin & Kuppuswamy find Black *men* particularly
  penalized). For presentation we estimate all ten gender × ethnicity cell
  AMCEs vs the White-male reference from a single 10-level categorical, each
  with a TOST verdict at ±1.5 pp (`intersectional.csv`).
- **H14 (activist-choice homophily — novel)**: The **impact persona**
  ("support underrepresented creators") shifts choice toward female- and
  minority-named creators, i.e., a persona × demographic interaction. Tested as
  a joint Wald over the impact-persona × {female, ethnicity} terms. This
  operationalizes the Greenberg–Mollick mechanism as an AI-steerable effect: it
  asks whether an explicitly prosocial backer framing *activates* demographic
  steering that is otherwise below the model's stated rationale.

### Abstention and hedging (preregistered, descriptive)

Each main-arm response is classified as an **abstention** (declines to choose /
calls the campaigns equally promising) and, separately, as
**demographic-aware** (the text refers to a creator's name, gender, ethnicity,
race, or "underrepresented/minority" status). Both rates reported per model
(`refusals_summary.csv`). The demographic-aware rate is the governance-relevant
quantity — especially under the impact persona, where demographic language is
legitimately invited — and is read alongside H9/H10/H14 and the
stated-vs-revealed comparison.

H9/H10 are **pooled estimands**: the power simulation (`power_mde.csv`) shows
per-model power for small demographic effects is inadequate (~0.65–0.77 at the
assumed sizes), while pooling the model panel gives sub-1 pp MDE. Per-model
demographic AMCEs are reported descriptively with CIs, not tested. H9/H10 are
estimated on the main-arm pooled sample across all personas; H14 isolates the
impact-persona effect.

Position bias (slot dummies) and the letter-arm decomposition are reported;
the position-1 advantage is expressed in $/pledge. **Logprob availability
matrix**: the letter-arm logprob decomposition requires token log-probabilities,
which the OpenAI models return but the **Anthropic API does not** — for Claude
models the letter arm records sampled choices only. This asymmetry is stated
up front.

## 5. Model panel and sampling protocol

Local (Ollama): llama3.2:3b, qwen2.5:3b, phi3:mini, mistral:7b-instruct,
gemma3:4b, llama3.1:8b; deepseek-r1:7b contingent on a ≤5% pilot parse-failure
gate. API: gpt-4o-mini (real logprobs → letter arm), claude-haiku-4-5,
claude-sonnet-4-6 (chosen over Sonnet 5, which rejects non-default
temperature), one OpenAI flagship (pinned at run start), claude-opus-4-8.
claude-fable-5 optional after budget review.

**Sampling protocol.** Main arm temperature 0.7 (top-p 0.9); temp-0 arm 0.0.
Models that reject non-default sampling parameters (claude-opus-4-8 returns 400
on any `temperature`/`top_p`; claude-fable-5 likewise) run under
`omit_sampling`: provider-default sampling only, and the **temp-0 arm is
skipped** for them (single-sampling-mode caveat recorded in `design_meta.json`).

**Exclusion rules (pre-specified).** Per call, up to 2 stricter-reminder
retries on parse failure. A model × arm cell with >5% parse failure is excluded
from that arm's estimates. deepseek-r1:7b is gated at 5% pilot parse failure
(reasoning tokens may exhaust the generation budget before the JSON is emitted).
Model IDs and inference dates are verified against each provider's `/models`
endpoint at run start and recorded in `design_meta.json`.

## 6. Robustness battery (preregistered)

Template heterogeneity; temperature invariance (ratios to the pledge AMCE);
grounded-snippet format; field-order; test–retest; plausibility-cell exclusion
(dominating/dominated cards); **name-exemplar placebo** (LR test of first-name
dummies given full gender × ethnicity cell fixed effects); missingness model on
parse failures.

## 7. Limitations (pre-registered)

Single category (male-stereotyped tech): the sharpest homophily test but
one-category external validity; a category-varying arm is flagged as future
work. Names-only manipulation (no photos): cleaner but weaker than photo-based
audits; manipulation strength is itself informative. The impact persona
legitimately invites demographic inference — H9/H10 are defined on the pooled
main arm, H14 isolates the persona effect.

## 8. Ethics note

No human subjects; all creator profiles and campaigns are synthetic. The
demographic manipulation audits the *model*, not people. Findings are reported
at the group-fairness level with equivalence bounds, avoiding over-claiming
from single-model point estimates.

## 9. Validation

The full pipeline is validated end-to-end by `python -m src.smoke_test` against
a mock data-generating process with known effects, including a known female
(+0.20 logit) and Black-name (−0.20 logit) effect and true-null effects for the
other groups; the suite asserts sign, magnitude, true-null recovery, the
pledge-monotonicity gate, the name-exemplar placebo, and figure/table
generation before any real model is called. Demographic betas are set larger
than a realistic field effect purely so the recovery assertions are robust, not
flaky; the true nulls stay exactly 0.
