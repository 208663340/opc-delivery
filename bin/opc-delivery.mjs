#!/usr/bin/env node
import { cpSync, existsSync, lstatSync, mkdirSync, mkdtempSync, readFileSync, realpathSync, renameSync, rmSync } from 'node:fs';
import { homedir } from 'node:os';
import { dirname, isAbsolute, join, relative, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';
import { parseArgs } from 'node:util';

const packageRoot = realpathSync(resolve(dirname(fileURLToPath(import.meta.url)), '..'));
const metadata = JSON.parse(readFileSync(join(packageRoot, 'package.json'), 'utf8'));
const companionSkills = JSON.parse(readFileSync(join(packageRoot, 'skills/manifest.json'), 'utf8')).skills;
const payload = ['SKILL.md', 'README.md', 'CONTRIBUTING.md', 'agents', 'assets', 'references', 'skills', 'scripts', 'docs'];
const help = `OPC Delivery ${metadata.version}

Usage:
  opc-delivery install [--dir <skills-root>] [--dry-run] [--force]
  opc-delivery list
  opc-delivery --help
  opc-delivery --version

Default destination: CODEX_HOME/skills/opc-delivery, or ~/.codex/skills/opc-delivery
--dir       Install opc-delivery inside this skills root.
--dry-run   Show the destination without writing files.
--force     Back up an existing installation before replacing it.

The bundle includes ${companionSkills.length} companion skills. Installation is explicit;
npm install only installs this CLI. Python tools require Python 3.
`;

function stat(path) {
  try {
    return lstatSync(path);
  } catch (error) {
    if (error.code === 'ENOENT') return null;
    throw error;
  }
}

function canonical(path) {
  if (stat(path)) return realpathSync(path);
  return join(canonical(dirname(path)), relative(dirname(path), path));
}

function within(path, parent) {
  const rest = relative(parent, path);
  return !rest || (rest !== '..' && !rest.startsWith(`..${sep}`) && !isAbsolute(rest));
}

function install(values) {
  if (values.dir !== undefined && !values.dir.trim()) throw new Error('--dir must be a non-empty path.');
  const skillsRoot = resolve(values.dir ?? join(process.env.CODEX_HOME || join(homedir(), '.codex'), 'skills'));
  const destination = join(skillsRoot, 'opc-delivery');
  const existing = stat(destination);
  if (existing?.isSymbolicLink()) throw new Error(`Refusing to replace a symbolic link: ${destination}`);
  if (existing && !existing.isDirectory()) throw new Error(`Destination is not a directory: ${destination}`);
  const resolvedDestination = canonical(destination);
  if (within(resolvedDestination, packageRoot) || within(packageRoot, resolvedDestination)) {
    throw new Error('The destination must not overlap the source package.');
  }
  if (existing && !values.force) throw new Error(`Already exists: ${destination}\nUse --force to keep a backup and replace it.`);
  for (const name of payload) {
    if (!existsSync(join(packageRoot, name))) throw new Error(`The package is incomplete: missing ${name}`);
  }
  if (values['dry-run']) {
    console.log(`Would install OPC Delivery ${metadata.version} with ${companionSkills.length} companion skills to ${destination}`);
    if (existing) console.log('The existing directory would be preserved in a backup.');
    return;
  }

  mkdirSync(skillsRoot, { recursive: true });
  const staging = mkdtempSync(join(skillsRoot, '.opc-delivery-stage-'));
  let backup;
  try {
    for (const name of payload) cpSync(join(packageRoot, name), join(staging, name), { recursive: true });
    // Recheck after copying so a concurrently created installation is not overwritten.
    const current = stat(destination);
    if (current) {
      if (!values.force || current.isSymbolicLink() || !current.isDirectory()) {
        throw new Error(`Destination changed during installation: ${destination}`);
      }
      backup = mkdtempSync(join(skillsRoot, '.opc-delivery-backup-'));
      rmSync(backup, { recursive: true });
      renameSync(destination, backup);
    }
    renameSync(staging, destination);
  } catch (error) {
    if (backup && !stat(destination)) renameSync(backup, destination);
    throw error;
  } finally {
    rmSync(staging, { recursive: true, force: true });
  }
  console.log(`Installed OPC Delivery ${metadata.version} with ${companionSkills.length} companion skills to ${destination}`);
  if (backup) console.log(`Previous installation preserved at ${backup}`);
  console.log('The skill is available to your agent on its next skill refresh or session.');
}

try {
  const { values, positionals } = parseArgs({
    options: {
      dir: { type: 'string' },
      'dry-run': { type: 'boolean' },
      force: { type: 'boolean' },
      help: { type: 'boolean', short: 'h' },
      version: { type: 'boolean', short: 'v' },
    },
    allowPositionals: true,
  });
  if (values.help) console.log(help);
  else if (values.version) console.log(metadata.version);
  else if (positionals.length === 0 && Object.keys(values).length === 0) console.log(help);
  else if (positionals.length === 1 && positionals[0] === 'install') install(values);
  else if (positionals.length === 1 && positionals[0] === 'list' && Object.keys(values).length === 0) {
    for (const skill of companionSkills) console.log(`${skill.name}\t${skill.category}\t${skill.role}`);
  } else throw new Error('Unknown command or options. Run opc-delivery --help.');
} catch (error) {
  console.error(`opc-delivery: ${error.message}`);
  process.exitCode = 1;
}
