const vm = require('vm');
try {
  const content = require('fs').readFileSync('test.js', 'utf8');
  new vm.Script(content);
  console.log('test.js syntax is valid');
} catch (e) {
  console.error('test.js syntax error:', e.message);
}

try {
  const html = require('fs').readFileSync('EFLTG.html', 'utf8');
  const scriptContent = html.match(/<script>([\s\S]*?)<\/script>/)[1];
  new vm.Script(scriptContent);
  console.log('EFLTG.html syntax is valid');
} catch (e) {
  console.error('EFLTG.html syntax error:', e.message);
}
