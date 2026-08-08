export const meta = {
  name: 'paper-2026',
  description: 'Author 200-question NEET PG 2026 practice paper',
  phases: [
    { title: 'Author', detail: '19 subject writers, ~11 questions each' },
    { title: 'Verify', detail: 'independent expert check of answers/explanations' },
  ],
}

const SUBJECTS = [
  ['Anatomy', 11], ['Biochemistry', 11], ['Physiology', 11],
  ['Pathology', 13], ['Pharmacology', 13], ['Microbiology', 12],
  ['Forensic Medicine', 6], ['PSM', 12], ['ENT', 8], ['Ophthalmology', 8],
  ['Medicine', 17], ['Surgery', 14], ['OBG', 13], ['Paediatrics', 13],
  ['Psychiatry', 7], ['Anaesthesia', 7], ['Radiology', 8], ['Orthopaedics', 8],
  ['Dermatology', 8],
]

const Q_SCHEMA = {
  type: 'object',
  properties: {
    questions: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          q: { type: 'string' },
          o: { type: 'array', items: { type: 'string' }, minItems: 4, maxItems: 4 },
          a: { type: 'integer' },
          ex: { type: 'string' },
          tp: { type: 'string' },
        },
        required: ['q', 'o', 'a', 'ex', 'tp'],
      },
      minItems: 1,
    },
  },
  required: ['questions'],
}

const AUTHOR_PROMPT = (subject, n) => `You are a senior NEET PG examiner and medical educator. Write ${n} original exam-grade single-best-answer MCQs in ${subject} for a NEET PG 2026 practice paper.

CONTEXT — NEET PG 2026 blueprint (NBEMS official pattern):
- 200 questions, 180 minutes. Questions are of moderate length with an increasing number of image-based and clinical-vignette items.
- Recent exams emphasise: clinical problem solving, investigations, management guidelines (e.g. current AHA/ACC, ACOG, RCOG, IDSA, GINA, KDOQI, latest NMC/NBE circulars), pharmacovigilance, ethics, medicolegal updates, and recent guideline changes (2024-2026). Two-step questions (identify condition, then choose management) are common.
- Difficulty distribution: ~45% easy (recall of high-yield facts), ~35% moderate (clinical reasoning), ~20% hard (rare presentations, guideline minutiae). Prefer moderate-hard clinical vignettes — that is the current trend.

RULES:
1. Each question: realistic clinical vignette (age, sex, key findings, lab values, imaging or investigation result where apt). Avoid trivia-only recall when a vignette fits.
2. Four single-answer options (A-D). Exactly ONE correct. Distractors plausible but clearly wrong; no absurd options, no 'all of the above'.
3. Tracked NEWEST guidelines where they changed (e.g. hypertension ≥130/80 per ACC/AHA 2017 — but note Indian JNC-style thresholds; diabetic management; newer anticoagulants; monoclonal antibodies in cancer/asthma/migraine; SGLT2i/GLP-1RA in HF & CKD; 2024-2025 NICE/NBEMS exam-relevant updates). When a guideline point is contested, phrase the stem to make the intended standard unambiguous.
4. Explanation: 2-5 sentences. State the correct option explicitly and why each distractor fails. Include high-yield memory hooks.
5. Topic (tp): one short topic name, e.g. "Thyroid disorders".
6. Every question must be NEW — no duplicates of classic PYQ stems.

OUTPUT: JSON only, schema: {"questions":[{"q":"stem (include age/sex where relevant)","o":["A text","B text","C text","D text"],"a":<index of correct, 0-3>,"ex":"explanation","tp":"topic"}]}. Exactly ${n} items. No markdown fences, no commentary.`

const VERIFY_SCHEMA = {
  type: 'object',
  properties: {
    ok: { type: 'boolean' },
    fixes: { type: 'array', items: { type: 'string' } },
  },
  required: ['ok', 'fixes'],
}

phase('Author')
const authorResults = await parallel(SUBJECTS.map(([subject, n]) => () => agent(
  AUTHOR_PROMPT(subject, n),
  { label: `author:${subject}`, phase: 'Author', schema: Q_SCHEMA, effort: 'xhigh' }
)))

const all = authorResults.filter(Boolean).flatMap((r, i) =>
  (r.questions || []).map(q => ({ ...q, s: SUBJECTS[i][0] }))
)
log(`authored: ${all.length} questions`)

phase('Verify')
const V_SCHEMA = {
  type: 'object',
  properties: {
    fixes: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          idx: { type: 'integer' },
          what: { type: 'string' },
        },
        required: ['idx', 'what'],
      },
    },
  },
  required: ['fixes'],
}
const CHUNK = 25
const verifyResults = await parallel(
  Array.from({ length: Math.ceil(all.length / CHUNK) }, (_, c) => () => agent(
    `You are a second, independent NEET PG examiner verifying a practice paper. Below are ${Math.min(CHUNK, all.length - c * CHUNK)} questions (JSON, array index = question index). For EACH: (1) is the keyed answer correct? (2) is the explanation consistent with the answer? (3) are distractors valid? (4) is the medical content current (2024-2026 guidelines)? Flag ONLY real errors with the exact correction.

QUESTIONS:
${JSON.stringify(all.slice(c * CHUNK, c * CHUNK + CHUNK).map(q => ({ ...q, o: q.o.map((t, k) => String.fromCharCode(65 + k) + '. ' + t), a: String.fromCharCode(65 + q.a) })))}

Return ONLY JSON: {"fixes":[{"idx":<absolute question index>,"what":"<exact correction, e.g. 'answer should be C (option index 2), explanation mentions X; option B text is wrong because...'"}]}. Empty array if all correct. No markdown.`,
    { label: `verify:${c}`, phase: 'Verify', schema: V_SCHEMA, effort: 'xhigh' }
  ))
)

const fixes = verifyResults.filter(Boolean).flatMap(r => r.fixes || [])
log(`verifier fixes: ${fixes.length}`)
return { questions: all, fixes }
