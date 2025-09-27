export const SERVICES = [
    {
      id: 'bed_assembly',
      label: 'Assemble a new bed',
      keywords: ['assemble','assembly','new','ikea','wayfair','frame','malm'],
      followups: [
        { id: 'size', q: 'What bed size?', type: 'select', options: ['Twin','Full','Queen','King'] },
        { id: 'brand_model', q: 'Brand/model (if known)?', type: 'short' }
      ],
      skill_tag: 'furniture_assembly',
      estimate_hours: [1.5, 3]
    },
    {
      id: 'bed_repair',
      label: 'Fix wobbly/creaky bed',
      keywords: ['fix','repair','wobbly','creak','slat','support','bolt'],
      followups: [
        { id: 'issue', q: 'What seems wrong?', type: 'select',
          options: ['Loose frame','Broken slat','Squeaks','Missing hardware','Other'] }
      ],
      skill_tag: 'handyman',
      estimate_hours: [0.5, 2]
    },
    {
      id: 'bed_move',
      label: 'Disassemble & move to another room',
      keywords: ['move','disassemble','reassemble','relocate'],
      followups: [
        { id: 'stairs', q: 'Any stairs/elevator?', type: 'select',
          options: ['No stairs','Stairs','Elevator'] }
      ],
      skill_tag: 'moving_help',
      estimate_hours: [1, 2.5]
    },
    {
      id: 'bed_haulaway',
      label: 'Remove old bed',
      keywords: ['remove','haul','dispose','junk'],
      followups: [],
      skill_tag: 'junk_removal',
      estimate_hours: [0.5, 1.5]
    },
    {
      id: 'bed_bugs',
      label: 'Possible bed bugs (inspection/treatment)',
      keywords: ['bug','bedbug','bites','pest'],
      followups: [{ id: 'evidence', q: 'Do you see live bugs or stains?', type: 'select',
        options: ['Live bugs','Stains','Not sure'] }],
      skill_tag: 'pest_control',
      regulated: true,
      estimate_hours: [1, 3]
    },
    { id: 'other', label: 'Something else', keywords: [], followups: [{ id:'describe', q:'Tell us more', type:'long'}], skill_tag:'general', estimate_hours:[0.5,2] }
  ];
  