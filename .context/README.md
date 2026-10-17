# .context/ — AIと担当者のための作業文脈

## 役割

研究固有の基本情報と、作業の引継ぎ状態を分離して管理する。

## 置くもの

INDEX.md、core/、templates/、work/。

## 置かないもの

巨大ログ、生データ、認証情報、AGENTS.mdへ蓄積する作業履歴。

## ルール

INDEX.mdから必要な文書だけ読む。安定した情報はcore/、変化する作業状態はwork/へ置く。実験結果は索引・原本を参照し、チャットだけに残さない。非公開の作業記録をGitHubへ自動公開しない。

## 配置・利用例

```text
INDEX.md
core/
templates/
work/
```

[全フォルダの案内](../docs/FOLDER_GUIDE.md)を参照する。実際の研究固有ルールはAGENTS.mdと対象studyの仕様に従う。
