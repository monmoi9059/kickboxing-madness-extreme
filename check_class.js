const html = require('fs').readFileSync('hairstyles_upgrade.html', 'utf8');
const scriptContent = html.match(/<script>([\s\S]*?)<\/script>/)[1];

try {
  new (require('vm').Script)(scriptContent);
} catch (e) {
  console.log(e.stack);
}
