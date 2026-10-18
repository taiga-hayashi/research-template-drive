# analysis/compare/ — 複数studyの比較解析

## 役割

複数の実験・問題設定を横断する比較結果を保存する。

## 置くもの

comparison_id/analysis_idごとの入力一覧、比較条件表、CSV、図、解釈。

## 置かないもの

各studyの生データのコピー、条件が揃っていないものを無説明に混ぜた比較。

## ルール

新規フォルダは24文字以内を基本とし、短いIDを使う。条件・日時はREADMEと索引に記録する。

<comparison_id>/で分け、対象study・モデル・seed・評価予算・相違点を記録する。共通範囲と未測定範囲を示し、比較ごとにplot.ipynbとplot.pyをセットにし、再実行では同じcsv/・png/・pdf/を更新する。analysis_idは設定・索引に記録し、更新前の実行情報はdocs/records/analysis_runs/へ保持する。

## 配置・利用例

```text
<comparison_id>/README.md
<comparison_id>/{csv,png,pdf}/
```

[全フォルダの案内](../../docs/FOLDER_GUIDE.md)を参照する。実際の研究固有ルールはAGENTS.mdと対象studyの仕様に従う。
