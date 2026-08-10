import { readFile } from "node:fs/promises";

const file = process.argv[2];

if (!file) {
  console.error("Usage: node web/exp-0007/analyze.mjs <results.json>");
  process.exit(1);
}

let payload;
try {
  payload = JSON.parse(await readFile(file, "utf8"));
} catch (error) {
  console.error(`結果ファイルを読めませんでした: ${error.message}`);
  process.exit(1);
}

if (payload.experiment_id !== "EXP-0007" || !Array.isArray(payload.responses)) {
  console.error("EXP-0007の結果ファイルではありません。");
  process.exit(1);
}

const counts = { fact: 0, memory_selection: 0, unknown: 0 };
for (const response of payload.responses) {
  if (response.selected_condition in counts) {
    counts[response.selected_condition] += 1;
  } else {
    counts.unknown += 1;
  }
}

const total = payload.responses.length;
const rate = total ? (counts.memory_selection / total * 100).toFixed(1) : "0.0";

console.log(`EXP-0007 回答数: ${total}`);
console.log(`事実中心: ${counts.fact}`);
console.log(`Memory Selection: ${counts.memory_selection} (${rate}%)`);
if (counts.unknown) console.log(`不明: ${counts.unknown}`);
console.log(`探索基準（5人中4人以上）: ${counts.memory_selection >= 4 ? "到達" : "未到達"}`);

const reasons = payload.responses
  .map((response, index) => `${index + 1}. [${response.selected_condition}] ${response.reason || "（理由なし）"}`)
  .join("\n");

console.log("\n選択理由");
console.log(reasons || "（回答なし）");

const improvements = payload.responses
  .filter(response => response.improvement)
  .map((response, index) => `${index + 1}. ${response.improvement}`)
  .join("\n");

console.log("\n実験環境の改善点");
console.log(improvements || "（記載なし）");
