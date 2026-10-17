# data/ — 入力と計算データの論理的なルート

## 役割

入力、計算結果、取得済みパッケージを識別する。実際の場所はdata_rootで端末ごとに切り替える。

## 置くもの

inputs/、runs/、fetchが生成する_packages/。

## 置かないもの

解析結果、共通コード、仮想環境、手動で書き換えた生データ。

## ルール

このdata/と各端末のdata_rootの対応を記録する。大量出力や展開コピーはDrive外に置き、正式保存は検証済みDriveパッケージで行う。Gitには説明文書と.gitkeep等の許可済みファイルだけを登録する。

## 配置・利用例

```text
inputs/
runs/<study>/<config_id>/<run_id>/
_packages/<package_id>/     # fetchが生成
```

[全フォルダの案内](../docs/FOLDER_GUIDE.md)を参照する。実際の研究固有ルールはAGENTS.mdと対象studyの仕様に従う。
