# cache/ — 再生成可能なキャッシュ

## 役割

取得・計算を効率化する、失っても正式保存先から復元できるコピーを置く。

## 置くもの

各端末のcache_rootにあるパッケージキャッシュや再生成可能な中間結果。

## 置かないもの

唯一の実験原本、未保存の再開checkpoint、正式な解析結果。

## ルール

実際の生成先はDrive外のcache_rootにする。このフォルダの存在や.gitignoreはDrive同期除外を意味しない。削除時は再取得可能性と実行中処理への影響を確認する。fetchの再利用時もchecksumを検証する。

## 配置・利用例

```text
cache_root/packages/<sha256の先頭16桁>/artifact.archive
# このREADMEは説明用。実データは端末別cache_rootへ
```

[全フォルダの案内](../docs/FOLDER_GUIDE.md)を参照する。実際の研究固有ルールはAGENTS.mdと対象studyの仕様に従う。
