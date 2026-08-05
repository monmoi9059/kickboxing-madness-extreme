const vm = require('vm');
try {
  const content = require('fs').readFileSync('test.js', 'utf8');
  new vm.Script(content);
  console.log('test.js syntax is valid');
} catch (e) {
  console.error('test.js syntax error:', e.message);
}

try {
  const html = require('fs').readFileSync('hairstyles_upgrade.html', 'utf8');
  const scriptContent = html.match(/<script>([\s\S]*?)<\/script>/)[1];
  new vm.Script(scriptContent);
  console.log('hairstyles_upgrade.html syntax is valid');
} catch (e) {
  console.error('hairstyles_upgrade.html syntax error:', e.message);
}
