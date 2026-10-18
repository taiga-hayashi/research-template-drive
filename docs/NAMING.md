# 短いフォルダ名

新規フォルダは1要素24文字以内を基本とする。条件・モデル名・seed・日時・コード版を1つの名前へ連結しない。詳しい意味はREADME、config.json、metadata.json、索引へ記録する。既存プロジェクトや保存済みパッケージは改名しない。

| 名前 | 新規の推奨形式 | 例 |
|---|---|---|
| study | 意味の分かる短い英小文字・数字・ハイフン、24文字以内 | `irm`、`penalty`、`encoding` |
| config_id | `c-`＋条件hashの先頭12桁 | `c-1a2b3c4d5e6f` |
| run_id | `r-`＋ランダムな16進12桁 | `r-a1b2c3d4e5f6` |
| package_id | `p-`＋ランダムな16進12桁 | `p-112233aabbcc` |
| analysis_id | `a-`＋ランダムな16進12桁 | `a-445566ddeeff` |
| task_id / comparison_id | 内容が分かる短い名前、24文字以内 | `check-input`、`model-comp` |

config_idはフォルダ用の短い別名であり、config_hashは従来どおり正規化条件の完全なSHA-256を記録する。索引には両方を残し、先頭12桁だけで同じ条件と判断しない。異なる完全hashが同じconfig_idになったら、先頭16桁等へ延長し24文字以内で識別する。既存の対応を別条件へ使い回さない。

run/package/analysisの短いIDも既存IDとの重複を確認し、同じなら再発行する。ランダム値だけで衝突しないと仮定しない。`python -c "import secrets; print('r-' + secrets.token_hex(6))"`等で候補を作れるが、重複確認は別途必要。Pythonは既存のローカル仮想環境を使う。

日時・seed・モデル・コード版・条件値はmetadataと索引へ保存する。意味が分からない略語を増やすより、短いstudy名と説明READMEを組み合わせる。latest/final2等を唯一の識別子にしない。

```text
data/runs/irm/c-1a2b3c4d5e6f/r-a1b2c3d4e5f6/
analysis/irm/a-445566ddeeff/
archive/irm/p-112233aabbcc/
```

PestControlの既存のseed=、cfg-、code=等は維持する。新しい短い保存先から既存データを参照でき、移動・改名・hash再計算は不要。

## ツールの扱い

packは新規package_idを24文字以内に制限する。fetchは保存済みパッケージとの互換性のため従来の128文字以内のIDも読める。どちらも英数字で始まり、英数字・.・_・-を使う。

新規取得キャッシュはchecksumの先頭16桁をフォルダ名に使う。完全SHA-256は常に照合し、短い名前だけで再利用しない。衝突・破損があれば停止し、別cache_rootで取得する。既存の64桁キャッシュは参照できるが、自動改名しない。

フォルダ作成やrun/analysis/config_idの割当を一括管理する処理は未実装。梱包対象の元の相対パスは維持するため、packが元データの長い階層を自動短縮することもない。

解析のanalysis_idは設定・索引・過去実行記録で使う識別子であり、出力フォルダ名には使わない。出力はanalysis/<study>/<category>/直下のpdf/・png/・csv/へ固定し、v01等の版番号フォルダを作らない。
