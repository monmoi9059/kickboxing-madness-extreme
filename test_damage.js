const fs = require('fs');

let content = fs.readFileSync('hairstyles_upgrade.html', 'utf8');
let combatLogicStart = content.indexOf('// Calculate Damage');
let combatLogicEnd = content.indexOf('if (dmg < 1) dmg = 1;', combatLogicStart);
console.log(content.substring(combatLogicStart, combatLogicEnd + 21));
