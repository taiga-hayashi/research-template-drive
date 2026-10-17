# config/ — 端末設定と共通表示設定

## 役割

端末ごとの保存先と、研究全体で共有する図の設定を管理する。

## 置くもの

paths.example.json、figures.example.json、研究のfigures.json。端末固有の*.local.jsonはローカルで使う。

## 置かないもの

仮想環境本体、認証情報、実験結果。実験の科学的条件はexperiments/へ置く。

## ルール

paths.example.jsonからpaths.local.jsonを作り、mac/serverの絶対パスを記入する。*.local.jsonはGit管理外。認証情報はここに書かない。保存先だけの違いは条件hashに含めない。

## 配置・利用例

```text
paths.example.json
paths.local.json       # 各端末のみ
figures.json           # 実際に使う研究の図設定
```

[全フォルダの案内](../docs/FOLDER_GUIDE.md)を参照する。実際の研究固有ルールはAGENTS.mdと対象studyの仕様に従う。
