const vm = require('vm');
try {
  const html = require('fs').readFileSync('EFLTG.html', 'utf8');
  const scriptMatch = html.match(/<script>([\s\S]*?)<\/script>/);
  if (scriptMatch) {
      new vm.Script(scriptMatch[1]);
      console.log('EFLTG.html syntax is valid');
  } else {
      console.log('No script found in EFLTG.html');
  }
} catch (e) {
  console.error('EFLTG.html syntax error:', e.message);
}
