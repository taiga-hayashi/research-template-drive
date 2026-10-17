# archive/ — Driveへ保存する再現用パッケージ

## 役割

実験・チャンク単位で固定した保存一式を識別する。

## 置くもの

<study>/<package_id>/のREADME、artifacts.zip、SHA256SUMS.txt、package-report.json、必要な閲覧用CSV/PDF。

## 置かないもの

過去archiveを再帰的に含むZIP、作成中のZIP、仮想環境、秘密情報。

## ルール

package_idを毎回一意にする。まずサーバーの収集元とは別のstagingへpackし、検証後にrcloneでDriveへ保存する。既存tarも維持し、保存検証前に原本を削除しない。データ本体はGit管理外。

## 配置・利用例

```text
<study>/<package_id>/README.md
<study>/<package_id>/artifacts.zip
<study>/<package_id>/SHA256SUMS.txt
<study>/<package_id>/package-report.json
```

[全フォルダの案内](../docs/FOLDER_GUIDE.md)を参照する。実際の研究固有ルールはAGENTS.mdと対象studyの仕様に従う。
