# data/inputs/ — 実験の入力

## 役割

計算に使う外部データや固定入力を管理する。

## 置くもの

入力ファイル、出典・版・checksum・取得日・Drive参照を記したREADME。

## 置かないもの

計算結果、再生成キャッシュ、出典や版の分からない置換データ。

## ルール

データセット名・版で識別する。同名で内容を差し替えず、新しい版として保存する。SSD等の外部入力は場所だけでなく版とchecksumを記録し、Drive未保存なら明記する。

## 配置・利用例

```text
<dataset>/<version>/README.md
<dataset>/<version>/...
```

[全フォルダの案内](../../docs/FOLDER_GUIDE.md)を参照する。実際の研究固有ルールはAGENTS.mdと対象studyの仕様に従う。
