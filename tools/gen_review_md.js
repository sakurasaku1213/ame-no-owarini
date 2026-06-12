// UI/UXレビュー結果JSON → REVIEW.md 変換
// 使い方: node gen_review_md.js <workflow出力ファイル> <出力md>
const fs = require('fs');
const src = process.argv[2];
const dst = process.argv[3] || 'REVIEW.md';
const data = JSON.parse(fs.readFileSync(src, 'utf8'));
const r = data.result;
const sevName = { high: '高', medium: '中', low: '低' };
const verName = { html: 'HTML版', renpy: "Ren'Py版", both: '両版' };
const order = { high: 0, medium: 1, low: 2 };
const items = [...r.confirmed].sort((a, b) => order[a.severity] - order[b.severity]);

let md = `# UI/UXレビュー報告書 『雨の終わりに』

実施日: 2026-06-13 ／ 対象: HTML版 (ame_no_owarini.html) と Ren'Py版 (renpy/AmeNoOwariNi)

## 方法

6観点(HTML操作性・Ren'Py操作性・ビジュアル/レイアウト・ゲームUX・アクセシビリティ・VN慣習)の並列レビューで53件の指摘を収集し、
全件を「指摘を反証せよ」という敵対的検証にかけた。コード行・実測値・Ren'Py SDKソースまで確認した結果、**50件が実在と確定、3件は反証され棄却**。
severityは検証側で再調整済み(誇張された影響は引き下げた)。

## 指摘一覧（優先度順）

| # | 優先度 | 対象 | 指摘 |
|---|--------|------|------|
`;
items.forEach((f, i) => {
  md += `| ${i + 1} | ${sevName[f.severity]} | ${verName[f.version]} | ${f.title} |\n`;
});

md += `\n## 詳細\n`;
let cur = '';
items.forEach((f, i) => {
  if (f.severity !== cur) {
    cur = f.severity;
    md += `\n---\n\n# 優先度【${sevName[cur]}】\n`;
  }
  md += `\n### ${i + 1}. ${f.title}\n\n`;
  md += `- **対象**: ${verName[f.version]} ／ ${f.file}\n`;
  md += `- **根拠**: ${f.evidence}\n`;
  md += `- **影響**: ${f.impact}\n`;
  md += `- **修正案**: ${f.fix}\n`;
});

md += `\n---\n\n## 検証で棄却された指摘（誤検知）\n\n`;
r.rejected.forEach(x => {
  md += `- **${x.title}**\n  - 棄却理由: ${x.why}\n`;
});

md += `\n## 良くできている点\n\n`;
r.strengths.forEach(s => { md += `- ${s}\n`; });

fs.writeFileSync(dst, md);
console.log('written', dst, md.length, 'chars,', items.length, 'findings');
