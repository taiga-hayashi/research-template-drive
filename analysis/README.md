# analysis/ — 解析結果

## 役割

Macまたはサーバーで生成した集計値・図・解析記録を保存する。

## 置くもの

study/categoryごとのREADME、plot.ipynbとplot.py、analysis_config.json、results.md、CSV、PNG/PDF、図設定snapshot。

## 置かないもの

生データの原本、仮想環境、解析ごとに複製した共通コード。

## ルール

新規フォルダは24文字以内を基本とし、短いIDを使う。条件・日時はREADMEと索引に記録する。

<study>/<category>/へ保存し、描き直しは同じpdf/・png/・csv/を更新する。版番号フォルダは作らない。解析試行のanalysis_idは設定・索引へ記録し、旧実行情報はdocs/records/analysis_runs/へ保持する。入力run/package・checksum・コード版・集計条件を記録する。PNG/PDFを同名にし、必要な各パネルは独立描画する。端末のoutput_rootとDrive保存先を区別する。

## 配置・利用例

```text
<study>/<category>/README.md
<study>/<category>/analysis_config.json
<study>/<category>/{csv,png,pdf}/
compare/
```

[全フォルダの案内](../docs/FOLDER_GUIDE.md)を参照する。実際の研究固有ルールはAGENTS.mdと対象studyの仕様に従う。

Notebookの各図には読み方をMarkdownで説明し、先頭から実行した出力を保存する。詳細は [解析・作図の運用](../docs/ANALYSIS_WORKFLOW.md) を参照する。
