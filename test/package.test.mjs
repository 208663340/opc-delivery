import test from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { existsSync, mkdtempSync, mkdirSync, readFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');

test('the actual npm tarball installs a working CLI and complete skills without install-time home writes', t => {
  const directory = mkdtempSync(join(tmpdir(), 'opc-package-test-'));
  t.after(() => rmSync(directory, { recursive: true, force: true }));
  // Parent npm commands can inject --dry-run, --prefix or --package settings.
  // Each isolated consumer must run with its own npm configuration.
  const env = Object.fromEntries(Object.entries(process.env).filter(([key]) => !key.toLowerCase().startsWith('npm_config_')));
  env.CODEX_HOME = join(directory, 'codex');
  env.npm_config_cache = join(directory, 'cache');
  function npm(args, cwd) {
    const executable = process.env.npm_execpath;
    const result = spawnSync(executable ? process.execPath : 'npm', executable ? [executable, ...args] : args, {
      cwd, env, encoding: 'utf8', timeout: 60_000,
    });
    assert.equal(result.status, 0, result.stderr || String(result.error));
    return result.stdout;
  }

  const [packed] = JSON.parse(npm(['pack', '--offline', '--ignore-scripts', '--json', '--pack-destination', directory], root));
  const paths = new Set(packed.files.map(file => file.path));
  for (const path of ['bin/opc-delivery.mjs', 'package.json', 'SKILL.md', 'references/skill-recommendations.md', 'scripts/inspect_project.py', 'skills/frontend-design/LICENSE.txt', 'skills/python-testing/references/pytest.md']) {
    assert.ok(paths.has(path), `Missing packed file: ${path}`);
  }
  assert.equal([...paths].some(path => path.startsWith('test/') || path.startsWith('node_modules/') || path.endsWith('.tgz')), false);
  assert.equal([...paths].filter(path => /^skills\/[^/]+\/SKILL.md$/.test(path)).length, 27);

  const project = join(directory, 'consumer project');
  mkdirSync(project);
  npm(['install', '--offline', '--ignore-scripts=false', '--no-audit', '--no-fund', '--no-package-lock', join(directory, packed.filename)], project);
  assert.equal(existsSync(join(directory, 'codex')), false, 'npm install must not run a skill installation lifecycle hook');

  const destination = join(directory, 'consumer skills');
  npm(['exec', '--offline', '--', 'opc-delivery', 'install', '--dir', destination], project);
  const installed = join(destination, 'opc-delivery');
  assert.equal(readFileSync(join(installed, 'SKILL.md'), 'utf8'), readFileSync(join(root, 'SKILL.md'), 'utf8'));
  assert.equal(readFileSync(join(installed, 'skills/manifest.json'), 'utf8'), readFileSync(join(root, 'skills/manifest.json'), 'utf8'));
  assert.equal(readFileSync(join(installed, 'skills/frontend-design/LICENSE.txt'), 'utf8'), readFileSync(join(root, 'skills/frontend-design/LICENSE.txt'), 'utf8'));
  const listed = npm(['exec', '--offline', '--', 'opc-delivery', 'list'], project);
  assert.match(listed, /python-sqlalchemy/);
  assert.match(listed, /deep-agents-memory/);
});
