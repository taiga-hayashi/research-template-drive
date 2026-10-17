# フォルダの役割と保存ルール

各フォルダのREADMEに、役割・置くもの・置かないもの・ルール・例を記載する。迷ったときはこの案内から参照する。これらは新規研究の標準であり、PestControl等の既存フォルダを移動・改名する指示ではない。

| フォルダ | 役割 |
|---|---|
| [src/](../src/README.md) | 共通実装 |
| [experiments/](../experiments/README.md) | 実験固有のコードと条件 |
| [config/](../config/README.md) | 端末設定と共通表示設定 |
| [analysis/](../analysis/README.md) | 解析結果 |
| [analysis/compare/](../analysis/compare/README.md) | 複数studyの比較解析 |
| [data/](../data/README.md) | 入力と計算データの論理的なルート |
| [data/inputs/](../data/inputs/README.md) | 実験の入力 |
| [data/runs/](../data/runs/README.md) | 計算試行の結果 |
| [docs/](README.md) | 研究の仕様と運用文書 |
| [notes/](../notes/README.md) | 日付単位の研究ノート |
| [refs/](../refs/README.md) | 参考文献と外部資料 |
| [scripts/](../scripts/README.md) | 操作用のコマンド入口 |
| [tests/](../tests/README.md) | 必要な検証コード |
| [templates/](../templates/README.md) | コピーして使う記録雛形 |
| [archive/](../archive/README.md) | Driveへ保存する再現用パッケージ |
| [cache/](../cache/README.md) | 再生成可能なキャッシュ |
| [tmp/](../tmp/README.md) | 一時作業 |
| [.context/](../.context/README.md) | AIと担当者のための作業文脈 |
| [.context/core/](../.context/core/README.md) | 安定した研究固有情報 |
| [.context/templates/](../.context/templates/README.md) | 作業引継ぎの雛形 |
| [.context/work/](../.context/work/README.md) | 作業の実施状態 |
| [.context/work/active/](../.context/work/active/README.md) | 進行中の作業 |
| [.context/work/completed/](../.context/work/completed/README.md) | 完了作業の記録 |

## どこへ置くか

- 再利用する実装はsrc/、実験ごとの入口と条件はexperiments/、操作コマンドはscripts/。
- 入力はdata/inputs/、計算結果はdata/runs/、解析結果はanalysis/、保存パッケージはarchive/。
- 仕様と判断はdocs/、日付単位の観測・考察はnotes/、作業の引継ぎは.context/work/。
- 端末のパスはconfig/*.local.json、研究全体の図設定はconfig/figures.json、実験条件はexperiments/<study>/へ分ける。
- 仮想環境は各端末のDrive外の既存環境を使う。cache/とtmp/は役割を示す説明用で、実際の生成先はDrive外にする。

## 識別子と新規フォルダ

| 識別子 | 役割 | 命名 |
|---|---|---|
| study | 実験テーマ・保存スキーマ | 短い小文字英数字とハイフン、24文字以内を基本とする |
| config_hash / config_id | 条件の完全hash / フォルダ用の短い別名 | 完全SHA-256を記録し、フォルダはc-＋先頭12桁。対応と衝突を確認 |
| run_id | 計算の各試行 | r-＋ランダム16進12桁を推奨。同条件の再試行も新ID |
| package_id | 保存パッケージ | p-＋ランダム16進12桁を推奨。新規梱包は24文字以内 |
| analysis_id | 解析・作図の各試行 | a-＋ランダム16進12桁を推奨。描き直しも新ID |
| task_id | 作業の引継ぎ | 内容が分かる名前。同じ作業は既存の記録を更新 |

新規フォルダは1要素24文字以内を基本とし、詳しい条件と日時はREADME・設定・索引へ残す。[短い命名ルール](NAMING.md)に従う。

run/package/analysisのIDを自動発行する処理とconfig_hashの生成処理は未実装。latestやfinal2だけで版を判別せず、索引で最新版と前の版の対応を示す。既存のseed=、cfg-等の階層は維持する。

新しく作るstudy・run・analysis・packageのフォルダにもREADMEを置き、目的・入力・出力・条件/版・再現コマンド・完了/検証状態・関連索引を記録する。生成スクリプトがREADMEを自動生成しない場合は雛形から作成する。空の構造保持には.gitkeepを使える。

## 生成時だけ現れるフォルダ

- `data_root/_packages/<package_id>/`: fetchの復元コピー。元の相対パスを保持し、既存runへ上書きしない。
- `cache_root/packages/<sha256の先頭16桁>/`: 再利用可能な取得アーカイブ。cache_rootはDrive外。
- `raw/`・`checkpoints/`・`logs/`: 各runの生データ・再開情報・実行記録。
- `csv/`・`png/`・`pdf/`・各`panels/`: 各解析の集計と図。PNG/PDFの対応を維持する。
- `code_snapshot/`・`records/`: パッケージに固定した実行時ソースと記録。編集用の共通コードと区別する。

## Git・Drive・実行領域の違い

.gitignoreはGitの登録規則でありDrive同期除外にはならない。data/、archive/、cache/、tmp/のREADMEは説明文書としてGitへ含めるが、データ本体の扱いは変更しない。Driveを正式保存先とし、サーバー出力・端末の復元コピー・クラウド保存の検証状態を区別する。非公開ノート・文献・図・個人設定は、Gitの除外規則だけに頼らず公開前に確認する。

詳細は[運用](DRIVE_WORKFLOW.md)、[梱包と取得](PACKAGING_AND_FETCH.md)、[状態管理](STATUS_AND_JOBS.md)、[図](FIGURE_POLICY.md)を参照する。
