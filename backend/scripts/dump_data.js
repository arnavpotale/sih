import fs from 'fs';
import { DETAILED_PROJECTS } from '../../src/data/paimanaData.js';

fs.writeFileSync('detailed_projects.json', JSON.stringify(DETAILED_PROJECTS, null, 2));
console.log('Saved detailed_projects.json');
