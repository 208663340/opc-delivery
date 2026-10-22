import test from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { existsSync, mkdtempSync, mkdirSync, readFileSync, readdirSync, rmSync, symlinkSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const cli = join(root, 'bin/opc-delivery.mjs');

function sandbox(t) {
  const directory = mkdtempSync(join(tmpdir(), 'opc-cli-test-'));
  t.after(() => rmSync(directory, { recursive: true, force: true }));
  return directory;
}

function run(args, directory, extraEnv = {}) {
  return spawnSync(process.execPath, [cli, ...args], {
    cwd: directory, encoding: 'utf8',
    env: { ...process.env, CODEX_HOME: join(directory, 'codex'), ...extraEnv },
  });
}

test('installs the complete bundle into a destination containing spaces', t => {
  const directory = sandbox(t);
  const destination = join(directory, 'my skills');
  const result = run(['install', '--dir', destination], directory);
  assert.equal(result.status, 0, result.stderr);
  const installed = join(destination, 'opc-delivery');
  for (const file of ['SKILL.md', 'references/skill-recommendations.md', 'scripts/inspect_project.py', 'skills/frontend-design/LICENSE.txt', 'skills/python-testing/references/pytest.md']) {
    assert.equal(readFileSync(join(installed, file), 'utf8'), readFileSync(join(root, file), 'utf8'));
  }
  assert.equal(readdirSync(join(installed, 'skills')).filter(name => existsSync(join(installed, 'skills', name, 'SKILL.md'))).length, 27);
  assert.equal(existsSync(join(installed, 'test')), false);
  assert.equal(existsSync(join(installed, 'node_modules')), false);
});

test('uses CODEX_HOME for the default install location', t => {
  const directory = sandbox(t);
  const result = run(['install'], directory);
  assert.equal(result.status, 0, result.stderr);
  assert.equal(existsSync(join(directory, 'codex/skills/opc-delivery/SKILL.md')), true);
});

test('dry-run reports the destination without creating it', t => {
  const directory = sandbox(t);
  const destination = join(directory, 'new skills');
  const result = run(['install', '--dir', destination, '--dry-run'], directory);
  assert.equal(result.status, 0, result.stderr);
  assert.ok(result.stdout.includes(join(destination, 'opc-delivery')));
  assert.equal(existsSync(destination), false);
});

test('refuses an existing installation without changing user files', t => {
  const directory = sandbox(t);
  const destination = join(directory, 'skills');
  const installed = join(destination, 'opc-delivery');
  mkdirSync(installed, { recursive: true });
  writeFileSync(join(installed, 'notes.md'), 'my local changes');
  const result = run(['install', '--dir', destination], directory);
  assert.notEqual(result.status, 0);
  assert.equal(readFileSync(join(installed, 'notes.md'), 'utf8'), 'my local changes');
  assert.equal(existsSync(join(installed, 'SKILL.md')), false);
  assert.deepEqual(readdirSync(destination), ['opc-delivery']);
});

test('force keeps the entire old installation in a backup', t => {
  const directory = sandbox(t);
  const destination = join(directory, 'skills');
  const installed = join(destination, 'opc-delivery');
  mkdirSync(installed, { recursive: true });
  writeFileSync(join(installed, 'notes.md'), 'keep this');
  const result = run(['install', '--dir', destination, '--force'], directory);
  assert.equal(result.status, 0, result.stderr);
  const backups = readdirSync(destination).filter(name => name.startsWith('.opc-delivery-backup-'));
  assert.equal(backups.length, 1);
  assert.equal(readFileSync(join(destination, backups[0], 'notes.md'), 'utf8'), 'keep this');
  assert.equal(existsSync(join(installed, 'SKILL.md')), true);
  assert.equal(existsSync(join(installed, 'notes.md')), false);
  assert.ok(result.stdout.includes(backups[0]));
});

test('dry-run with force preserves the existing install and creates no backup', t => {
  const directory = sandbox(t);
  const installed = join(directory, 'skills/opc-delivery');
  mkdirSync(installed, { recursive: true });
  writeFileSync(join(installed, 'notes.md'), 'keep this');
  const result = run(['install', '--dir', join(directory, 'skills'), '--force', '--dry-run'], directory);
  assert.equal(result.status, 0, result.stderr);
  assert.deepEqual(readdirSync(dirname(installed)), ['opc-delivery']);
  assert.equal(readFileSync(join(installed, 'notes.md'), 'utf8'), 'keep this');
});

test('list, help and version do not install anything', t => {
  const directory = sandbox(t);
  const listed = run(['list'], directory);
  assert.equal(listed.status, 0, listed.stderr);
  assert.match(listed.stdout, /frontend-design/);
  assert.match(listed.stdout, /langgraph-persistence/);
  for (const args of [[], ['--help'], ['--version']]) {
    const result = run(args, directory);
    assert.equal(result.status, 0, result.stderr);
    assert.ok(result.stdout.trim());
  }
  assert.deepEqual(readdirSync(directory), []);
});

test('invalid arguments fail without writing a destination', t => {
  const directory = sandbox(t);
  for (const args of [['install', '--dir'], ['install', '--dir', ''], ['install', '--wat'], ['delete'], ['list', '--force'], ['install', '--dir', '--force']]) {
    const result = run(args, directory);
    assert.notEqual(result.status, 0, args.join(' '));
  }
  assert.deepEqual(readdirSync(directory), []);
});

test('does not replace a symlinked install even with force', t => {
  const directory = sandbox(t);
  const original = join(directory, 'my-original');
  const destination = join(directory, 'skills');
  mkdirSync(original);
  mkdirSync(destination);
  writeFileSync(join(original, 'notes.md'), 'original');
  symlinkSync(original, join(destination, 'opc-delivery'), 'junction');
  const result = run(['install', '--dir', destination, '--force'], directory);
  assert.notEqual(result.status, 0);
  assert.equal(readFileSync(join(original, 'notes.md'), 'utf8'), 'original');
  assert.deepEqual(readdirSync(destination), ['opc-delivery']);
});

test('refuses installs inside the source package or over an ancestor of it', t => {
  const directory = sandbox(t);
  for (const destination of [join(root, 'skills'), root]) {
    const result = run(['install', '--dir', destination, '--force', '--dry-run'], directory);
    assert.notEqual(result.status, 0, destination);
  }
});
