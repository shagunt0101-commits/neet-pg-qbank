import io, json, re, collections, hashlib

qs = json.loads(io.open('research/_parsed.json', encoding='utf-8').read())

# 1) drop artifacts
qs = [q for q in qs if len(q['q']) >= 8]
# 2) image-based -> reclassify? keep, but tag
for q in qs:
    q['img'] = any(k in q['q'].lower() for k in ('image','shown','figure','diagram','labelled','labeled'))

# 3) Surgery -> Ortho classifier based on content keywords
ORTHO = ['fracture','scaphoid','femur','tibia','wrist','knee','hip','joint','orthopaedic','orthopedic',
         'dislocation','spine','vertebra','ligament','tendon','meniscus','plaster','cast','fragment',
         'union','fixation','screw','plate','nailing','prosthesis','amputat','amputation','foot','ankle',
         'shoulder dislocation','avascular necrosis','knee','fracture dis','epiphys''']
SUBLABELS = {}
for q in qs[:0]: pass

# Heuristic: any 'surgery' subj that also mentions bone/joint heavily
surg_ortho = []
for q in qs:
    if q['subj'] == 'Surgery':
        low = q['q'].lower()
        # ortho-ish?
        score = sum(1 for kw in ['fracture','bone','joint','oste','knee','hip','spine','wrist','ankle',
                                 'dislocation','spondyl','vertebra','plate','screw','arthro','tendo',
                                 'limb','amput','cast','femur','tibia','humerus','radius','scaphoid'] if kw in low)
        if score >= 1:
            q['subj2'] = 'Orthopaedics'
        else:
            q['subj2'] = 'Surgery'
    else:
        q['subj2'] = q['subj']
from collections import Counter
print('subj2 distribution:')
for k,v in Counter(q['subj2'] for q in qs).items():
    print('  ', k, v)
