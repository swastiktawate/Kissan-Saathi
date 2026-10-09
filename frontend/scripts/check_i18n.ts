import fs from 'fs';
import path from 'path';

const en = JSON.parse(fs.readFileSync(path.join(process.cwd(), 'src/i18n/en.json'), 'utf8'));
const hi = JSON.parse(fs.readFileSync(path.join(process.cwd(), 'src/i18n/hi.json'), 'utf8'));
const mr = JSON.parse(fs.readFileSync(path.join(process.cwd(), 'src/i18n/mr.json'), 'utf8'));

const enKeys = Object.keys(en).sort();
const hiKeys = Object.keys(hi).sort();
const mrKeys = Object.keys(mr).sort();

let failed = false;
if (JSON.stringify(enKeys) !== JSON.stringify(hiKeys)) {
    console.error("Hindi keys do not match English keys");
    failed = true;
}
if (JSON.stringify(enKeys) !== JSON.stringify(mrKeys)) {
    console.error("Marathi keys do not match English keys");
    failed = true;
}

if (failed) process.exit(1);
console.log("i18n check passed");
