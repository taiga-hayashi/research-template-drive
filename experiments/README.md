# experiments/ — 実験固有のコードと条件

## 役割

共通実装を組み合わせ、何をどの条件で計算するかを定義する。

## 置くもの

studyごとの実行入口、条件JSON、パラメータ指定、protocolへの参照。

## 置かないもの

生データ、checkpoint、解析図、複製した共通実装。

## ルール

<study>/で分ける。studyは内容が分かる短い小文字英数字とハイフンを使い、新規は24文字以内を基本とする。既存studyの意味を変えず、破壊的変更は別studyにする。出力先・seed・予算・コード版を記録し、サーバーの保存先設定を使う。

## 配置・利用例

```text
<study>/run.py
<study>/config.json
```

[全フォルダの案内](../docs/FOLDER_GUIDE.md)を参照する。実際の研究固有ルールはAGENTS.mdと対象studyの仕様に従う。
