# scripts/ — 操作用のコマンド入口

## 役割

保存・復元・集計・作図など、利用者が実行する入口を置く。

## 置くもの

artifacts.pyや研究固有の作図・診断のコマンド入口。

## 置かないもの

生データ、図、仮想環境、共通関数の重複実装。

## ルール

機能が分かるsnake_case.pyを使い、再利用する処理はsrc/へ分離する。引数・出力・前提を--helpや文書に残す。既存のローカル仮想環境を使い、既存runへ黙って上書きしない。

## 配置・利用例

```text
artifacts.py pack --spec ... --dry-run
artifacts.py pack --spec ... --output ...
artifacts.py verify --archive ... --sha256 ...
artifacts.py fetch --request ... --paths ... --profile mac
```

[全フォルダの案内](../docs/FOLDER_GUIDE.md)を参照する。実際の研究固有ルールはAGENTS.mdと対象studyの仕様に従う。
