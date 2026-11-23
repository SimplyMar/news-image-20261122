import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const PNG_SIG = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const MAX_BYTES = 1048576;
const MAX_DIM = 1024;

const rootDir = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const pngBytes = readFileSync(join(rootDir, 'entry.png'));

if (pngBytes.length > MAX_BYTES || pngBytes.subarray(0, 8).compare(PNG_SIG) !== 0) {
  throw new Error(`Invalid PNG deliverable (${pngBytes.length} bytes)`);
}
if (pngBytes.subarray(12, 16).toString('ascii') !== 'IHDR') {
  throw new Error('Missing PNG IHDR header');
}

const width = pngBytes.readUInt32BE(16);
const height = pngBytes.readUInt32BE(20);
if (width === 0 || height === 0 || width > MAX_DIM || height > MAX_DIM) {
  throw new Error(`PNG dimensions out of range: ${width}x${height}`);
}
if (!pngBytes.subarray(-12).includes(Buffer.from('IEND'))) {
  throw new Error('Missing PNG IEND trailer');
}

mkdirSync(outDir, { recursive: true });
writeFileSync(join(outDir, 'entry.png'), pngBytes);
