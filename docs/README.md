# docs/ — 研究の仕様と運用文書

## 役割

安定した管理方針、入出力仕様、設計判断、実験・解析の索引を置く。

## 置くもの

運用ガイド、experiments-io.md、decisions.md、experiment-index.csv、analysis-index.csv、protocol。

## 置かないもの

巨大ログ、生データ、日々の操作履歴の全文。

## ルール

仕様変更は理由・影響・版をdecisions.mdへ記録する。索引は既存行を保持して更新し、未確認を推測で検証済みにしない。日々の考察はnotes/、作業引継ぎは.context/へ分ける。

## 配置・利用例

```text
FOLDER_GUIDE.md
DRIVE_WORKFLOW.md
PACKAGING_AND_FETCH.md
experiment-index.csv     # 雛形から作成
analysis-index.csv       # 雛形から作成
```

[全フォルダの案内](FOLDER_GUIDE.md)を参照する。実際の研究固有ルールはAGENTS.mdと対象studyの仕様に従う。

- [解析・作図の運用](ANALYSIS_WORKFLOW.md): Notebook/Pythonのセット、図の読み方、固定した出力先と実行記録。
