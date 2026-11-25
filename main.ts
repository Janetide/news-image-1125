// Entry point for the news-image-20261125 submission.
//
// What this does: hand the finished front page (entry.png) to the grader by
// placing a verified copy at $MAKEFUN_OUTPUT_DIR/entry.png. Nothing is
// drawn here — the picture was already rendered by draw25.py. This script
// only checks the file is what the bounty asks for, then copies it.
//
// Run:  MAKEFUN_OUTPUT_DIR=<dir> node main.ts
// Exit: 0 once the copy lands and matches the original byte for byte.

import { createHash } from "node:crypto";
import {
  existsSync,
  mkdirSync,
  readFileSync,
  statSync,
  writeFileSync,
} from "node:fs";
import { join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

// The eight bytes every PNG file opens with.
const PNG_SIGNATURE = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];
const WANTED_WIDTH = 1024;
const WANTED_HEIGHT = 1024;
const SIZE_CAP = 1024 * 1024; // 1 MiB

function abort(reason: string): never {
  throw new Error(`entry.png check failed: ${reason}`);
}

function fingerprint(data: Buffer): string {
  return createHash("sha256").update(data).digest("hex");
}

// The harness always tells us where the output goes.
const outputDir = process.env.MAKEFUN_OUTPUT_DIR;
if (!outputDir) abort("MAKEFUN_OUTPUT_DIR is not set");

// Resolve the picture relative to this script, not the working directory.
const scriptDir = resolve(fileURLToPath(new URL(".", import.meta.url)));
const picturePath = join(scriptDir, "entry.png");
if (!existsSync(picturePath)) {
  abort(`no entry.png found in ${scriptDir}`);
}

const picture = readFileSync(picturePath);

// First check: the file really is a PNG.
const head = [...picture.subarray(0, 8)];
const badSignature = head.some((byte, index) => byte !== PNG_SIGNATURE[index]);
if (badSignature) abort("first eight bytes are not the PNG signature");

// Second check: the IHDR chunk stores width and height at fixed offsets.
const width = picture.readUInt32BE(16);
const height = picture.readUInt32BE(20);
if (width !== WANTED_WIDTH || height !== WANTED_HEIGHT) {
  abort(`dimensions are ${width}x${height}, need ${WANTED_WIDTH}x${WANTED_HEIGHT}`);
}

// Third check: the bounty caps the file at one mebibyte.
if (picture.length > SIZE_CAP) {
  abort(`file is ${picture.length} bytes, over the ${SIZE_CAP} byte cap`);
}

mkdirSync(outputDir, { recursive: true });
const targetPath = join(outputDir, "entry.png");
writeFileSync(targetPath, picture);

// Prove the copy is exact before declaring success.
const delivered = readFileSync(targetPath);
if (fingerprint(delivered) !== fingerprint(picture)) {
  abort("copied file does not match the original");
}

console.log(
  `entry.png -> ${targetPath} (${statSync(targetPath).size} bytes, ` +
    `sha256 ${fingerprint(delivered)})`,
);
