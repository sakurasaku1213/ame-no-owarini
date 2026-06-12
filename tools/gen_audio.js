// 『雨の終わりに』Ren'Py版 音声アセット生成スクリプト
// HTML版のWebAudioシーケンサと同じ譜面・パラメータからWAVを合成する。
// 使い方: node gen_audio.js <出力先ディレクトリ>
const fs = require('fs');
const path = require('path');
const SR = 44100;
const OUT = process.argv[2] || path.join(__dirname, '..', 'renpy', 'AmeNoOwariNi', 'game', 'audio');

function writeWav(name, samples) {
  const n = samples.length;
  const buf = Buffer.alloc(44 + n * 2);
  buf.write('RIFF', 0); buf.writeUInt32LE(36 + n * 2, 4); buf.write('WAVE', 8);
  buf.write('fmt ', 12); buf.writeUInt32LE(16, 16); buf.writeUInt16LE(1, 20); buf.writeUInt16LE(1, 22);
  buf.writeUInt32LE(SR, 24); buf.writeUInt32LE(SR * 2, 28); buf.writeUInt16LE(2, 32); buf.writeUInt16LE(16, 34);
  buf.write('data', 36); buf.writeUInt32LE(n * 2, 40);
  for (let i = 0; i < n; i++) {
    const v = Math.max(-1, Math.min(1, samples[i]));
    buf.writeInt16LE(Math.round(v * 32767), 44 + i * 2);
  }
  fs.mkdirSync(OUT, { recursive: true });
  fs.writeFileSync(path.join(OUT, name), buf);
  console.log(name, (buf.length / 1024 | 0) + 'KB', (n / SR).toFixed(2) + 's');
}
function wave(type, ph) {
  const x = ph - Math.floor(ph);
  if (type === 'sine') return Math.sin(2 * Math.PI * x);
  if (type === 'square') return x < .5 ? 1 : -1;
  if (type === 'triangle') return 4 * Math.abs(x - .5) - 1;
  return 2 * x - 1; // sawtooth
}
function normalize(out, peak) {
  let mx = 0;
  for (const v of out) mx = Math.max(mx, Math.abs(v));
  const sc = mx > 0 ? peak / mx : 1;
  return Float32Array.from(out, v => v * sc);
}
// ---- BGMループ（16ステップ、音の余韻はループ先頭に折り返して継ぎ目なし） ----
const PAT = {
  bgm_calm: { bpm: 84, notes: [
    [0,110,2,'triangle',.6],[4,98,2,'triangle',.6],[8,87.3,2,'triangle',.6],[12,82.4,2,'triangle',.6],
    [2,220,1,'sine',.35],[6,261.6,.8,'sine',.3],[7,246.9,.8,'sine',.3],[10,196,1,'sine',.3],[14,164.8,1.5,'sine',.35]]},
  bgm_tense: { bpm: 126, notes: [
    [0,110,.8,'square',.45],[2,110,.8,'square',.45],[4,110,.8,'square',.45],[6,116.5,.8,'square',.5],
    [8,110,.8,'square',.45],[10,110,.8,'square',.45],[12,103.8,.8,'square',.5],[14,116.5,.8,'square',.5],
    [3,466.2,.5,'sine',.25],[11,415.3,.5,'sine',.25]]},
  bgm_sad: { bpm: 66, notes: [
    [0,110,.9,'sine',.5],[1,130.8,.9,'sine',.45],[2,164.8,.9,'sine',.45],[3,220,.9,'sine',.5],
    [4,87.3,.9,'sine',.5],[5,110,.9,'sine',.45],[6,130.8,.9,'sine',.45],[7,174.6,.9,'sine',.5],
    [8,98,.9,'sine',.5],[9,123.5,.9,'sine',.45],[10,146.8,.9,'sine',.45],[11,196,.9,'sine',.5],
    [12,82.4,.9,'sine',.5],[13,103.8,.9,'sine',.45],[14,123.5,.9,'sine',.45],[15,164.8,.9,'sine',.5]]}
};
for (const [name, pat] of Object.entries(PAT)) {
  const spb = 60 / pat.bpm / 2, L = Math.round(spb * 16 * SR);
  const out = new Float32Array(L);
  for (const [st, f, d, type, vol] of pat.notes) {
    const t0 = Math.round(st * spb * SR), dur = Math.round(d * spb * .95 * SR);
    const k = Math.log(.0001 / vol) / dur;
    for (let i = 0; i < dur; i++) out[(t0 + i) % L] += wave(type, f * i / SR) * vol * Math.exp(k * i);
  }
  writeWav(name + '.wav', normalize(out, .5));
}
// ---- 単発トーン（周波数スイープ対応） ----
function toneInto(out, t0, f0, d, type, vol, f1) {
  const s0 = Math.round(t0 * SR), n = Math.round(d * SR), k = Math.log(.0001 / vol) / n;
  let ph = 0;
  for (let i = 0; i < n && s0 + i < out.length; i++) {
    const fr = f1 ? f0 * Math.pow(f1 / f0, i / n) : f0;
    ph += fr / SR;
    out[s0 + i] += wave(type, ph) * vol * Math.exp(k * i);
  }
}
let b;
b = new Float32Array(Math.round(.12 * SR)); toneInto(b, 0, 660, .06, 'square', .5);
writeWav('select.wav', normalize(b, .4));
b = new Float32Array(Math.round(.35 * SR)); toneInto(b, 0, 880, .12, 'sine', .5); toneInto(b, .07, 1318.5, .18, 'sine', .35);
writeWav('ding.wav', normalize(b, .45));
b = new Float32Array(Math.round(.4 * SR)); toneInto(b, 0, 110, .28, 'sawtooth', .5); toneInto(b, 0, 104, .3, 'sawtooth', .4);
writeWav('buzz.wav', normalize(b, .5));
b = new Float32Array(Math.round(.45 * SR)); toneInto(b, 0, 220, .32, 'sawtooth', .6, 50);
for (let i = 0; i < .2 * SR; i++) b[i] += (Math.random() * 2 - 1) * .5 * (1 - i / (.2 * SR));
writeWav('slam.wav', normalize(b, .55));
// ---- 雨ループ（ホワイトノイズ→ローパス2段、端0.5秒クロスフェード） ----
{
  const L = 8 * SR, raw = new Float32Array(L + SR);
  const a = 1 - Math.exp(-2 * Math.PI * 900 / SR);
  let y1 = 0, y2 = 0;
  for (let i = 0; i < raw.length; i++) {
    y1 += a * ((Math.random() * 2 - 1) - y1);
    y2 += a * (y1 - y2);
    raw[i] = y2;
  }
  const F = Math.round(.5 * SR), out = new Float32Array(L);
  for (let i = 0; i < L; i++) out[i] = raw[i + SR];
  for (let i = 0; i < F; i++) {
    const k = i / F;
    out[L - F + i] = out[L - F + i] * (1 - k) + raw[SR - F + i] * k;
  }
  writeWav('rain.wav', normalize(out, .3));
}
// ---- 雷鳴（ノイズ＋ローパス周波数スイープ170→55Hz） ----
{
  const L = 3 * SR, out = new Float32Array(L);
  let y1 = 0, y2 = 0;
  for (let i = 0; i < L; i++) {
    const t = i / SR;
    const fc = 170 * Math.pow(55 / 170, Math.min(1, t / 2.6));
    const a = 1 - Math.exp(-2 * Math.PI * fc / SR);
    y1 += a * ((Math.random() * 2 - 1) - y1);
    y2 += a * (y1 - y2);
    let g;
    if (t < .18) g = Math.pow(t / .18, 2);
    else g = Math.exp(Math.log(.0002) * (t - .18) / (2.9 - .18));
    out[i] = y2 * g;
  }
  writeWav('thunder.wav', normalize(out, .55));
}
console.log('done ->', OUT);
