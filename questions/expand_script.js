export const meta = {
  name: 'deep-research-bank',
  description: 'Deep-research + expand the NEET PG / INI-CET PYQ bank to ~45 questions per subject',
  phases: [{ title: 'DeepResearch' }],
}

const SUBJECTS = [
  "Anatomy", "Biochemistry", "Physiology", "Pathology", "Pharmacology", "Microbiology",
  "Forensic Medicine", "PSM", "ENT", "Ophthalmology", "Medicine", "Surgery", "OBG",
  "Paediatrics", "Psychiatry", "Anaesthesia", "Radiology", "Orthopaedics", "Dermatology"
]

const QUESTION_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  properties: {
    subject: { type: 'string' },
    questions: {
      type: 'array', minItems: 30, maxItems: 45,
      items: {
        type: 'object', additionalProperties: false,
        properties: {
          q: { type: 'string' },
          o: { type: 'array', items: { type: 'string' }, minItems: 4, maxItems: 4 },
          a: { type: 'integer', minimum: 0, maximum: 3 },
          ex: { type: 'string' },
          e: { type: 'string', enum: ['NEET PG', 'INI-CET'] },
          y: { type: 'string', pattern: '^20(2[1-5])$' }
        },
        required: ['q', 'o', 'a', 'ex', 'e', 'y']
      }
    }
  },
  required: ['subject', 'questions']
}

phase('DeepResearch')
const results = await parallel(SUBJECTS.map((sub, i) => () =>
  agent(
    `You are a senior Indian medical PG entrance examiner and a PYQ archivist. Build an EXPANDED high-yield practice bank for ${sub} for NEET PG / INI-CET (CMD-level, 2021-2025 recall).

PART A — RESEARCH (mandatory, use web_search / fetch):
The authorities do not publish papers, but candidate-memory recall compilations do. Fetch at least these FREE sources for ${sub} and mine them for the genuinely-asked TOPICS and CONCEPTS:
- neetpgai.com previous-year-questions (search for the subject or title-matched)
- Prepladder "last 5 year PYQs in wet icons (medicine etc.)" blog pages
- careers360 subject-wise 2025/2024 PYQ blogs
- Collegedunia / Get-mock / EduRev solved-PDFs (topics only, do not copy wording)
- Any open Telegram-repo recall list for the subject you can find via search
Record the asked-concepts list you found (10-30 distinct). Keep it internal; do not return raw scraped text.

PART 2 — BUILD 30-45 fresh practice questions for ${sub}:
Rules:
1. FACTUAL EXACTNESS FIRST. Reconstruct the classic high-yield facts that genuinely recur. Error on unambiguous textbook answers. No invented statistics, no lies, no cultural-clinical edge trivia.
2. Parallel-phrase, never verbatim. Short stems (encode same concept with fresh wording). No statutory copyrighted lifeline text reuse.
3. EXAM tag mixing: aim ~60/40 NEET PG (135/227 in existing bank) to INI-CET.
4. Year tag across ["2021","2022","2023","2024","2025"] — timeless classics → 2021-2022; newer IMGs → 2023-2025.
5. Exactly 4 options (index 0-3); 'a' = correct index; 'ex' = one-line exam-highlight fact.
6. Echo NEETs' real high-frequency subject specifics — e.g. Anatomy: brachial plexus, circle of Willis, cranial nerve nuclei, fascial spaces; MSK: Caplan syndrome, gout pseudogout, meralgia, etc. — but DO NOT produce the same question twice (this whole run is additive: existing bank has 12 per subject and the NEW set must be DISJOINT / non-overlapping with those 12).

You produce {"subject": "${sub}", "questions": [30-45 per schema]}. Nothing else.`,
    { label: 'gen:' + sub, phase: 'DeepResearch', schema: QUESTION_SCHEMA, model: 'opus' }
  )
))

const ok = results.filter(Boolean)
let total = 0
for (const r of ok) total += r.questions.length
log(`Generated ${ok.length}/${SUBJECTS.length} subjects, ${total} new questions.`)
return { subjects: ok.map(r => r.subject).sort(), total }