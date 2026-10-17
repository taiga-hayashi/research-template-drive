# data/runs/ — 計算試行の結果

## 役割

サーバーで生成する各計算試行の生データ・設定・再開情報を保存する。

## 置くもの

config.json、metadata.json、raw/、checkpoints/、logs/、status.json。

## 置かないもの

最終的な比較図、共通コードの編集元、異なる条件を混ぜた結果。

## ルール

<study>/<config_id>/<run_id>/。同条件の再試行も別run_idにし、条件hashの仕様を固定する。フォルダは短いconfig_idを使い、完全なconfig_hashとの対応を記録する。継続再開は整合性と二重起動防止を確認する。失敗・部分完了も残し、計算・検証・保存を別管理する。

## 配置・利用例

```text
<study>/<config_id>/<run_id>/
  config.json
  metadata.json
  raw/
  checkpoints/
  logs/
  status.json
```

[全フォルダの案内](../../docs/FOLDER_GUIDE.md)を参照する。実際の研究固有ルールはAGENTS.mdと対象studyの仕様に従う。
