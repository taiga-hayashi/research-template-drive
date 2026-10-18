# templates/ — コピーして使う記録雛形

## 役割

各run・解析・保存・ジョブ・比較の記録を揃える。

## 置くもの

RUN_STATUS.json、JOB_RECORD.json、PACKAGE_SPEC.json、DOWNLOAD_REQUEST.json、各種README・索引・protocol。

## 置かないもの

実際のrun結果、個人設定、認証情報。

## ルール

元の雛形へ実データを埋めず、用途に応じた保存先へコピーする。REPLACE_*・null等を実データに合わせて記入し、未確認は推測で埋めない。schema_versionとCSVの列を確認し、古い記録を上書きしない。

## 配置・利用例

```text
PACKAGE_SPEC.json → config/package.local.json
DOWNLOAD_REQUEST.json → config/downloads.local.json
EXPERIMENT_INDEX.csv → docs/experiment-index.csv
ANALYSIS_CONFIG.json → analysis/<study>/<category>/analysis_config.json
```

[全フォルダの案内](../docs/FOLDER_GUIDE.md)を参照する。実際の研究固有ルールはAGENTS.mdと対象studyの仕様に従う。
