# analysis/ — 解析結果

## 役割

Macまたはサーバーで生成した集計値・図・解析記録を保存する。

## 置くもの

study/analysis_idごとのREADME、analysis_config.json、CSV、PNG/PDF、図設定snapshot。

## 置かないもの

生データの原本、仮想環境、解析ごとに複製した共通コード。

## ルール

新規フォルダは24文字以内を基本とし、短いIDを使う。条件・日時はREADMEと索引に記録する。

<study>/<analysis_id>/へ保存し、描き直しは新しいanalysis_idにする。入力run/package・checksum・コード版・集計条件を記録する。PNG/PDFを同名にし、必要な各パネルは独立描画する。端末のoutput_rootとDrive保存先を区別する。

## 配置・利用例

```text
<study>/<analysis_id>/README.md
<study>/<analysis_id>/analysis_config.json
<study>/<analysis_id>/{csv,png,pdf}/
compare/
```

[全フォルダの案内](../docs/FOLDER_GUIDE.md)を参照する。実際の研究固有ルールはAGENTS.mdと対象studyの仕様に従う。
