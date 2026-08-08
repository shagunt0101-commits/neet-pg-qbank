import json, re
from collections import Counter
qs = []
def add(e, y, q, o, a, ex):
    qs.append({'q': q, 'o': o, 'a': a, 'ex': ex, 'e': e, 'y': y})

add('NEET PG', '2023', 'While examining the jugular venous pulse, the c wave is produced by bulging of which structure into the atrium during the isovolumetric phase of ventricular contraction?',
    ['Tricuspid valve into the right atrium', 'Mitral valve into the left atrium', 'Aortic valve into the left ventricle', 'Pulmonary valve into the right ventricle'], 0,
    'The c wave of the JVP marks displacement of the tricuspid valve into the right atrium during isovolumetric ventricular contraction.')
add('NEET PG', '2022', 'In sinoatrial nodal pacemaker cells, the slow diastolic (phase 4) depolarization that sets intrinsic heart rate is initiated chiefly by which current?',
    ['The hyperpolarization-activated funny current (If)', 'The IK1 inward-rectifier potassium current', 'The transient outward potassium current (Ito)', 'The L-type calcium plateau current'], 0,
    'The funny current If plus decaying K+ conductance generate SA node diastolic depolarization; IK1 is absent in pacemaker cells.')
add('INI-CET', '2022', 'Blood flow through the left coronary artery is maximal during which phase of the cardiac cycle?',
    ['Ventricular diastole', 'Ventricular systole', 'Isovolumetric ventricular contraction', 'Atrial systole'], 0,
    'Systolic compression of subendocardial vessels limits flow, so left coronary flow peaks during diastole.')
add('NEET PG', '2022', 'When arterial pressure suddenly falls, the baroreceptor reflex acts to return pressure toward baseline. Which type of physiological control is this?',
    ['Negative feedback', 'Positive feedback', 'Feed-forward control', 'Local tissue autoregulation'], 0,
    'The baroreflex opposes any pressure disturbance, the defining feature of negative feedback control.')
add('INI-CET', '2024', 'By Fick principle, oxygen consumption is 250 mL/min while the arterial and mixed venous oxygen contents are 20 and 15 mL/dL respectively. The cardiac output is closest to:',
    ['5 L/min', '2.5 L/min', '10 L/min', '20 L/min'], 0,
    'CO = VO2/(CaO2-CvO2); with an a-v oxygen gap of 5 vol%, cardiac output is about 5 L/min.')
add('NEET PG', '2021', 'For a healthy young adult with a blood pressure of 150/90 mmHg, the approximate mean arterial pressure is:',
    ['110 mmHg', '90 mmHg', '130 mmHg', '125 mmHg'], 0,
    'MAP = DBP + (SBP-DBP)/3; here 90 + 20 = 110 mmHg.')
add('INI-CET', '2022', 'The vascular segment providing the greatest fraction of systemic vascular resistance, hence a main target of blood-pressure control, is:',
    ['Arterioles', 'Large conduit arteries', 'Capillaries', 'Venules and veins'], 0,
    'Arterioles contribute the majority of total systemic resistance.')
add('NEET PG', '2023', 'Functional residual capacity equals the arithmetic sum of which two volumes?',
    ['Expiratory reserve volume + residual volume', 'Inspiratory reserve volume + expiratory reserve volume', 'Tidal volume + inspiratory reserve volume', 'Tidal volume + expiratory reserve volume'], 0,
    'FRC = ERV + RV; it is the lung volume present at the end of a quiet expiration.')
add('INI-CET', '2023', 'Deoxygenated blood carries appreciably more CO2 than oxygenated blood at the same partial pressure. This property of hemoglobin is the:',
    ['Haldane effect', 'Bohr effect', 'Chloride shift', 'Krogh effect'], 0,
    'Reduced hemoglobin binds CO2 and H+ better than oxyhemoglobin, which aids CO2 uptake in the veins.')
add('INI-CET', '2022', 'Which receptors are chiefly stimulated by a fall in arterial PO2 (hypoxemia) and drive the hyperventilation of high altitude?',
    ['Carotid and aortic bodies (peripheral chemoreceptors)', 'Carotid sinus baroreceptors', 'Lung slowly adapting stretch receptors', 'Juxtacapillary J receptors'], 0,
    'Peripheral chemoreceptors, especially the carotid body, are the principal sensors of arterial hypoxemia.')
add('NEET PG', '2025', 'The stimulus sensed by the central chemoreceptors that closely tracks arterial PCO2 changes is:',
    ['Hydrogen ion concentration of the cerebrospinal fluid', 'Arterial hydrogen ion concentration', 'Arterial PO2 directly', 'Plasma oncotic pressure'], 0,
    'CO2 crosses the blood-brain barrier and hydrates to liberate H+; CSF H+ is the real stimulus of central chemoreceptors.')
add('NEET PG', '2021', 'A trekker develops headache, breathlessness and cerebral edema after rapid ascent above 3000 m. Which of the following is NOT part of standard management?',
    ['Intravenous digoxin', 'Immediate descent to lower altitude', 'Inhalation of oxygen', 'Tablet acetazolamide'], 0,
    'Acute mountain sickness is managed with descent, O2, acetazolamide and dexamethasone; digoxin has no role.')
add('NEET PG', '2024', 'Compared with a healthy lung, the static compliance of the lungs in emphysema is characteristically:',
    ['Increased, with reduced elastic recoil', 'Decreased, with stiff lungs', 'Unchanged', 'Raised only when gas trapping occurs'], 0,
    'Emphysema destroys elastic tissue, raising compliance; fibrosis instead lowers it.')
add('NEET PG', '2021', 'At the end of a quiet expiration, the intrapleural pressure in a healthy adult is closest to:',
    ['About 5 mmHg below atmospheric', 'Zero (equal to atmospheric)', 'About 5 mmHg above atmospheric', 'About 25 mmHg below atmospheric'], 0,
    'Resting intrapleural pressure is roughly -5 mmHg, keeping the lung partly distended at FRC.')
add('INI-CET', '2024', 'The counter-current multiplier that concentrates urine operates principally in which nephron segment?',
    ['Loop of Henle, mainly its thick ascending limb', 'Proximal convoluted tubule', 'Distal convoluted tubule', 'Cortical collecting duct'], 0,
    'NaCl transport out of the thick ascending limb builds the medullary osmotic gradient.')
add('INI-CET', '2023', 'Creatinine clearance slightly OVERESTIMATES the true GFR because:',
    ['Creatinine is actively secreted by renal tubules', 'Creatinine is reabsorbed along the nephron', 'Creatinine preferentially binds plasma proteins', 'Creatinine is stored in the renal medulla'], 0,
    'Mild tubular secretion of creatinine makes its clearance exceed the actual GFR.')
add('NEET PG', '2022', 'Renal plasma flow is best approximated by the clearance of which substance?',
    ['Sodium para-aminohippurate (PAH)', 'Inulin', 'Glucose', 'Urea'], 0,
    'PAH is almost completely removed in a single pass through the kidney, so PAH clearance equals renal plasma flow.')
add('NEET PG', '2021', 'Body fluid analysis shows: sodium 12 mEq/L, potassium 140 mEq/L, chloride 4 mmol/L. This represents:',
    ['Intracellular fluid', 'Plasma', 'Interstitial fluid', 'Extracellular fluid'], 0,
    'High potassium with low sodium marks the intracellular composition.')
add('NEET PG', '2022', 'The normal insensible water loss from the skin and respiratory tract each day is closest to:',
    ['About 700 mL', 'About 150 mL', 'About 2500 mL', 'About 3500 mL'], 0,
    'Insensible loss is on the order of 500-700 mL/day and cannot be regulated.')
add('NEET PG', '2021', 'A middle-aged woman leaks small volumes of urine only on coughing or straining. The most likely diagnosis is:',
    ['Stress incontinence', 'Urge incontinence', 'Overflow incontinence', 'Reflex neurogenic bladder'], 0,
    'Sudden intra-abdominal pressure overcomes a weakened sphincter, producing stress incontinence.')
add('INI-CET', '2025', 'ADH promotes water reabsorption in the collecting duct by inserting which channel at the apical membrane?',
    ['Aquaporin-2', 'Aquaporin-1', 'GLUT-2', 'SGLT-1'], 0,
    'Vasopressin moves AQP-2 water channels into the luminal membrane of collecting-duct principal cells.')
add('NEET PG', '2023', 'During intestinal peristalsis, the segment aboral (downstream) to the food bolus relaxes mainly because of which mediator?',
    ['VIP (vasoactive intestinal peptide)', 'Substance P', 'Dopamine released by sympathetic fibers', 'Acetylcholine from myenteric neurons'], 0,
    'VIP relaxes the segment ahead of the bolus during peristalsis.')
add('NEET PG', '2022', 'After a fatty meal, gall bladder contraction is chiefly triggered by which hormone?',
    ['Cholecystokinin (CCK)', 'Gastrin', 'Secretin', 'Gastric inhibitory peptide'], 0,
    'CCK contracts the gall bladder and promotes pancreatic enzyme secretion.')
add('INI-CET', '2024', 'Which sequence best describes the order of motor events during vomiting?',
    ['Reverse peristalsis of small intestine, LES closure, gastric contraction, UES relaxation, then inspiration against closed glottis', 'Pyloric relaxation, reverse peristalsis, inspiration with closed glottis, gastric contraction', 'Gastric contraction, LES relaxation, reverse peristalsis, UES relaxation', 'Inspiration with closed glottis occurs first, then gastric emptying'], 0,
    'Vomiting classically runs: small-intestine reverse peristalsis, LES closure, gastric contraction, UES relaxation, then forced inspiration against the closed glottis at ejection.')
add('NEET PG', '2021', 'The receptor that mediates the metabolic actions of insulin on target cells is best described as:',
    ['A receptor tyrosine kinase', 'A G-protein-coupled receptor', 'An intracellular nuclear receptor', 'A JAK-coupled cytokine receptor'], 0,
    'The insulin receptor is an alpha2-beta2 receptor tyrosine kinase.')
add('INI-CET', '2022', 'Which hormone acts on a receptor located INSIDE the cell?',
    ['Thyroxine', 'Glucagon', 'Epinephrine', 'Parathyroid hormone'], 0,
    'Lipophilic thyroxine diffuses into the cell and binds its nuclear receptor.')
add('INI-CET', '2024', 'For equal glucose loads, the plasma insulin rise is greater when glucose is taken by mouth than given intravenously. The reason is:',
    ['The incretin effect of GIP and GLP-1', 'The liver trapping more glucose after an oral load', 'Lower renal loss of the oral glucose', 'Suppression of glucagon by gastric acidity'], 0,
    'Gut incretins (GIP, GLP-1) potentiate insulin secretion after oral glucose.')
add('NEET PG', '2022', 'Plasma prolactin levels are highest at approximately which time?',
    ['24 hours after delivery', '24 hours after ovulation', '24 hours after a heavy meal', 'At peak physical exertion'], 0,
    'The postpartum prolactin surge (about 24 h) initiates lactation; sleep also raises prolactin.')
add('NEET PG', '2021', 'Secretion of aldosterone occurs from which zone of the adrenal gland?',
    ['Zona glomerulosa', 'Zona fasciculata', 'Zona reticularis', 'Adrenal medulla'], 0,
    'Aldosterone is the product of the outermost zona glomerulosa.')
add('NEET PG', '2022', 'Somatostatin within the pancreatic islets is produced by which cell type?',
    ['Delta (D) cells', 'Beta cells', 'Alpha cells', 'PP cells'], 0,
    'Islet delta cells release somatostatin, which inhibits both insulin and glucagon.')
add('NEET PG', '2022', 'The circadian peak of plasma cortisol in a normal day-night cycle occurs at approximately:',
    ['Early morning', 'Midnight', 'Mid-afternoon', 'Exactly at noon'], 0,
    'Cortisol secretion peaks in the early-morning hours and declines through the day.')
add('NEET PG', '2022', 'The resting membrane potential of an excitable cell is largely set by the resting conductance of which ion?',
    ['K+', 'Na+', 'Cl-', 'Ca2+'], 0,
    'At rest the membrane behaves almost as a potassium electrode, so the RMP sits near the K+ equilibrium potential.')
add('INI-CET', '2023', 'During the ABSOLUTE refractory period a neuron cannot discharge a new action potential mainly because:',
    ['Voltage-gated Na+ channels are in the inactivated state', 'All voltage-gated K+ channels close', 'Chloride channels open maximally', 'The Na-K ATPase pump stops working'], 0,
    'Na+ channel inactivation renders the membrane absolutely inexcitable.')
add('NEET PG', '2023', 'A patient has hyperkalemia with serum potassium 7 mEq/L. The expected effect on resting potential and action-potential generation is:',
    ['Depolarizes the resting potential and makes spikes harder to generate', 'Hyperpolarizes the resting potential and makes spikes easier to generate', 'Leaves the resting potential unchanged', 'Abolishes all Na-K pump activity'], 0,
    'High extracellular K+ partially depolarizes the membrane toward threshold and inactivates some Na+ channels, blunting excitability.')
add('INI-CET', '2023', 'In the actin-myosin cross-bridge cycle, detachment of myosin heads from actin requires:',
    ['The binding of a fresh ATP molecule to the myosin head', 'Rise and fall of sarcoplasmic calcium', 'Conformational change of troponin T', 'Dissociation of ADP and phosphate from the head'], 0,
    'The rigor state persists until a new ATP binds the myosin head and detaches the cross-bridge.')
add('NEET PG', '2021', 'Which nerve fiber conducts impulses at the highest velocity (about 120 m/s) and transmits muscle-spindle afferents?',
    ['Group Ia (A alpha) fiber', 'Group C fiber', 'Group III (A delta) fiber', 'Preganglionic B fiber'], 0,
    'Group Ia fibers are the largest myelinated afferents, conducting near 120 m/s.')
add('NEET PG', '2022', 'After a night of sleeping with an arm under the head, a person wakes with arm weakness but no numbness. The best explanation is:',
    ['Large myelinated A fibers are more susceptible to pressure than unmyelinated C fibers', 'C fibers are more easily compressed than any other fiber', 'B fibers fail even before A fibers under pressure', 'C and A fibers show identical pressure sensitivity'], 0,
    'Compression blocks the large myelinated motor fibers first while pain-carrying C fibers survive, giving paresis without numbness.')
add('NEET PG', '2021', 'In excitation-contraction coupling of skeletal muscle, calcium released from the sarcoplasmic reticulum switches the contraction on by binding directly to:',
    ['Troponin C', 'Tropomyosin', 'The myosin head core', 'Myosin light-chain kinase'], 0,
    'Ca2+ binds troponin C, moving tropomyosin to expose the myosin-binding sites of actin.')
add('NEET PG', '2022', 'A patient develops involuntary violent flinging movements confined to one side after a stroke. The likely lesion is in the:',
    ['Subthalamic nucleus', 'Globus pallidus externus', 'Caudate nucleus', 'Thalamus'], 0,
    'Contralateral hemiballismus localizes to the subthalamic nucleus.')
add('INI-CET', '2022', 'The spinal nucleus of the trigeminal nerve mediates which sensory modality?',
    ['Pain and temperature from the face', 'Vibratory sensation', 'Conscious proprioception', 'Fine touch discrimination'], 0,
    'Pain and temperature fibers of the trigeminal nerve descend to end in its spinal nucleus.')
add('INI-CET', '2025', 'The hippocampus plays its most classically pivotal role in:',
    ['Encoding and consolidating new long-term memories', 'Sensing arterial CO2', 'Generating the circadian rhythm', 'Maintaining muscle tone'], 0,
    'The hippocampus is central to the consolidation of new episodic memories.')
add('NEET PG', '2022', 'Parkinson disease is classically caused by loss of dopamine neurons in which brain region?',
    ['Substantia nigra pars compacta', 'Globus pallidus internus', 'Locus coeruleus', 'Red nucleus'], 0,
    'Loss of the nigro-striatal dopamine pathway is the hallmark of Parkinson disease.')
add('NEET PG', '2021', 'The sympathetic innervation of eccrine sweat glands is unusual because the transmitter acting on the gland is:',
    ['Acetylcholine acting on muscarinic receptors', 'Norepinephrine acting on alpha receptors', 'Epinephrine acting on beta-2 receptors', 'Dopamine acting on D2 receptors'], 0,
    'Eccrine sweat glands receive sympathetic cholinergic fibers acting on muscarinic receptors, the classic exception.')
add('INI-CET', '2023', 'Hemisection of the right half of the cervical cord (Brown-Sequard syndrome) typically produces:',
    ['Ipsilateral loss of touch-vibration-proprioception plus contralateral loss of pain-temperature below the lesion', 'Contralateral paralysis with ipsilateral pain loss', 'Bilateral flaccid paralysis below the lesion', 'Loss of light touch, pain and temperature all on the contralateral side'], 0,
    'Hemisection spares the ipsilateral dorsal columns/pyramidal tract and the opposite spinothalamic tract, hence dissociated crossed sensory loss.')
add('NEET PG', '2022', 'In the dark-adapted eye, night vision and sensitivity to very low light intensities are provided mainly by:',
    ['Rods containing rhodopsin', 'Foveal cones', 'Bipolar cells alone', 'Ganglion cells with melanopsin'], 0,
    'Rods and their visual pigment rhodopsin subserve scotopic dim-light vision.')

# validation
errs = []
if not (30 <= len(qs) <= 45):
    errs.append('COUNT %d' % len(qs))
for i, q in enumerate(qs):
    for k in ['subject']:
        pass
    for k in ['q', 'o', 'a', 'ex', 'e', 'y']:
        if k not in q:
            errs.append('q%d missing %s' % (i, k))
    if len(q['o']) != 4:
        errs.append('q%d o len %d' % (i, len(q['o'])))
    if not (0 <= q['a'] <= 3):
        errs.append('q%d bad a' % i)
    if q['e'] not in ['NEET PG', 'INI-CET']:
        errs.append('q%d bad e %r' % (i, q['e']))
    if not re.match(r'^20(2[1-5])$', str(q['y'])):
        errs.append('q%d bad y %r' % (i, q['y']))
    if len(q['q']) < 10 or len(q['ex']) < 5:
        errs.append('q%d too short' % i)
print('COUNT', len(qs))
print('ERRS:', errs[:20] if errs else 'NONE')
print('e-tags:', dict(Counter(q['e'] for q in qs)))
print('years:', dict(sorted(Counter(q['y'] for q in qs).items())))
stems = [q['q'] for q in qs]
print('dup stems:', len(stems) - len(set(stems)))
with open('_phys_qs_tmp.json', 'w', encoding='utf-8') as fh:
    json.dump(qs, fh, ensure_ascii=False, indent=1)
print('WRITTEN _phys_qs_tmp.json')