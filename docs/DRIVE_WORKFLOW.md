# サーバー計算・Macとサーバーでの解析・Drive保存

## 基本方針

研究室サーバーで計算し、計算結果をサーバーからGoogle Driveへ直接アップロードする。解析はMacでもサーバーでも同じコードと入力指定を使う。Driveを正式保存先とし、各端末の取得・展開先は作業用とする。

MacではDrive同期フォルダでコード・文書・閲覧用成果物を直接扱える。サーバーでは同じ版のコードを作業領域に用意する。変更を往復させる場合は差分を確認し、どの版を実行したか記録する。同じファイルを複数端末で同時に書き換えず、双方向の自動上書き同期を前提にしない。

## 保存先だけを端末ごとに切り替える

`config/paths.example.json`を`config/paths.local.json`へコピーし、macとserverの実際のパスを記入する。個人のパスはGitへ登録しない。

| 設定 | 用途 |
|---|---|
| project_root | その端末のコード・文書のルート |
| data_root | 計算データの生成・取得・展開先。アーカイブの`data/`に対応 |
| output_root | 解析成果物の生成先。`analysis/`に対応 |
| cache_root | 再生成可能なキャッシュ。Drive外に置く |

端末のパス設定と研究条件・解析条件を分離する。保存先だけの違いはconfig_hashに含めない。端末やbackendの違いが数値結果に影響する場合は、その条件も記録して同じ実験と無条件に扱わない。

標準ライブラリのみの`src/research_paths.py`で設定を読み込める。以下はパスを確認するだけで、計算・取得・転送・フォルダ作成は行わない。

```sh
python3 src/research_paths.py --paths config/paths.local.json --profile mac
python3 src/research_paths.py --paths config/paths.local.json --profile server
```

解析スクリプトからは`load_paths(path, profile)`を使い、`paths.data_root / relative_path`で入力を参照する。独自の起動方法に応じてimport経路を設定する。この雛形は既存の解析スクリプトを自動で書き換えない。

`.gitignore`はDrive同期を除外しない。仮想環境・キャッシュ・一時ファイル・秘密情報はDrive外に置く。Macのストリーミング利用時は必要なコード・入力をオフライン利用可能にしてから実行する。

## Python環境は各端末のローカルを使う

MacではDrive外にある既存のローカル仮想環境、研究室サーバーではサーバー側に用意された環境を使う。研究フォルダ内の`.venv`を前提にせず、Drive内に新しく作らない。既存環境を勝手に作り直したり依存関係を更新したりしない。使用環境が不明な場合は実行前に確認する。

- 対象環境をactivateするか、その環境のPython実行ファイルを直接指定する。
- 上記の`python3`コマンド例も、対象の仮想環境を有効にしてから実行する。
- 実行記録にはPython実行ファイルの場所、Pythonとライブラリの版、依存定義ファイルを残す。
- Macとサーバーで`.venv`本体をコピー・同期・共有しない。DriveやGitHubには環境本体を送らず、`pyproject.toml`・lockファイル・`requirements.txt`等の依存定義を保存する。
- 同じコードでも端末ごとのライブラリ版・backend・数値精度に差がある場合は記録する。保存先profileの切替だけで環境まで一致したと判断しない。

## サーバーで計算してDriveへ保存する

1. study・条件・seed・モデル・実行コード版・一意なrun_idを記録して計算する。実行開始時のコード・設定・依存定義を固定し、dirtyなら変更後の全実行時ソースまたは復元可能な差分も保存する。Git commit名とdirty表示だけで版の特定を済ませない。
2. 完了したseed・run・チャンクごと、長時間計算では原則1時間ごとに、整合性のある保存済みcheckpointから保存パッケージを作る。実行中のファイルをそのまま圧縮しない。
3. 新規はZIPを標準とするが、既存の`checkpoints.tar`等も保存できる。形式を変えるためだけに再圧縮・再送しない。結果とcheckpointを分ける場合も、同じ実行との対応を記録する。
4. サーバーでアーカイブ内manifest（相対パス・サイズ・SHA-256、manifest自身を除く）とアーカイブ全体のSHA-256を検証する。必要な生データ・ログ・実行時コード・設定・seed・依存定義・checkpointを保持する。
5. 新しいpackage_idでDriveへ直接アップロードする。アップロード手段は既存のものを利用する。認証・転送ツールをこのテンプレートが自動設定することはない。
6. クラウド上の存在・サイズ・checksumを検証する。SHA-256を照合できなければクラウドから再取得して照合する。ローカルの同名ファイルの確認だけで済ませない。検証前にサーバーの元データを削除しない。
7. `docs/experiment-index.csv`に計算状態と保存検証状態を別々に記録する。結果・checkpointが別の保存先なら両方のpackage_idとリンクを記録する。

DriveでREADME・主要指標CSV・代表図PDFを直接読めるようにし、大量の生データやcheckpointはアーカイブにまとめる。計算時点にまだ存在しない解析図は、後で独立した解析成果として保存する。既存パッケージに追記・上書きしない。

新規標準は`archive/<study>/<package_id>/`。既存プロジェクトでは現在の分類先の下に一意な保存先を設け、元の結果を維持する。ZIP内部は論理的な元の相対パスを保持し、別々の出力先から集めた場合は対応表をREADMEに記載する。依存する入力・コードを別パッケージで参照する場合は版・Driveリンク・checksumを明記する。

## Macでもサーバーでも解析する

1. `docs/experiment-index.csv`から対象run・package・Drive参照を選ぶ。全データを毎回取得せず、必要なものだけ取得する。
2. 取得したアーカイブ全体と内部manifestを検証し、新しい空の展開先で復元する。標準パッケージの`data/`配下をdata_rootへ対応付け、二重に`data/data/`を作らない。旧形式は既存の階層を保持する。
3. `templates/ANALYSIS_CONFIG.json`と`templates/ANALYSIS_README.md`を使い、新しいanalysis_idの解析記録を作る。入力run/package・相対パス・checksum、使用モデル・seed・予算・除外理由・集計条件を確定する。テンプレートの未記入値は実行前に埋める。
4. 同じ解析コード版と設定を用意し、端末に応じたpaths.local.jsonのprofileだけを切り替える。再現コマンド、実際の入出力先、環境・ライブラリ版も記録する。
5. `output_root/<study>/<analysis_id>/`へREADME、analysis_config.json、csv/、png/、pdf/を生成する。解析コードはsrc/またはscripts/等で共有し、解析結果フォルダごとに実装を複製しない。実行時snapshotは再現用に保存できる。
6. PNG/PDFと必要な独立パネル、CSV整合性、図の表示を検証する。完了判定後に計算状態をcompleteにする。
7. MacでDrive内へ直接出力した場合は同期後にクラウド保存を検証する。サーバーで生成した場合はDriveの対応する解析先へアップロードして検証する。大量ファイルは解析単位のアーカイブも使い、閲覧用ファイルは外に置く。
8. `docs/analysis-index.csv`に入力一覧への参照、実行場所、解析状態、Drive保存検証を記録する。再実行には新しいanalysis_idを付け、前の解析への参照を残す。未完了・失敗も残す。

同じstudy・入力・設定の再解析でもMacとサーバーで同じ出力先を使い回さない。analysis_idはUTC日時と一意suffix等で発行する。run_idは計算試行、package_idは保存単位、analysis_idは解析試行であり、互いに代用しない。

## 索引の使い方

`templates/EXPERIMENT_INDEX.csv`を`docs/experiment-index.csv`へ、`templates/ANALYSIS_INDEX.csv`を`docs/analysis-index.csv`へコピーして使う。実験索引はモデル・seedを含む各runを1行とする。既存run名を変える必要はなく、他の条件列と組み合わせて一意に識別する。同じrunに複数チャンクがある場合はpackageごとに行を追加し、保存済み範囲をnotesに記録する。

解析索引はanalysis_idごとに1行とし、複数入力はinput_manifest_pathでanalysis_config.jsonを参照する。CSVのカンマを含むセルは引用符で囲む。実験・解析のcompute_statusはpending/running/partial/failed/complete、保存のstorage_statusはpending/unverified/verified/failedを使う。必要なcheckpointがない場合はcheckpoint_storage_statusをnot_requiredとし、READMEに理由を書く。

## PestControlの既存配置に合わせる場合

| 役割 | 既存分類 |
|---|---|
| 計算結果 | `01_results/<problem>/`以下の既存の符号化・seed・cfg・コード版・モデル・run階層 |
| checkpoint | `01_results/01_checkpoints/<problem>/`以下の対応する階層 |
| 解析結果 | `02_analysis/<category>/<problem>/<analysis_id>/` |
| 解析コード | `03_scripts/`等の既存の共通コード |
| 記録・索引 | `04_docs/`または`.context/`の既存ルールに合う位置 |

この対応は新規データ・解析の案であり、自動移行ではない。既存のpng/pdf/csvやrun、cfg、コード版名は移動・改名しない。複数の問題設定を混ぜず、同じseedだけで同一実験と判断しない。既存のtar、結果とcheckpointの別保存も索引で対応付ける。

## GitHubを併用する場合（任意）

GitHubは雛形配布と必要なコード・管理文書の履歴管理に使う。研究用リポジトリ、DVC、uvは任意。新規研究ではGitHubからZIPを取得して始められる。公開範囲は研究ごとに決める。

コード更新はMacとサーバーの差分を確認して反映する。Gitを使わない場合も実行時コードのsnapshotとchecksumで版を固定する。Gitを使う場合もDrive外の作業コピーを利用できる。GitHubへはstaged diffと対象一覧を確認して送信し、生データ、大容量アーカイブ、秘密情報、非公開ノート・文献・図は送らない。

## 含まれない自動処理

パス設定の読込以外の、サーバー接続、Driveへの認証・転送、ZIP作成・検証、データ取得・展開、条件ハッシュ計算、索引更新、実験・解析実行は未実装。手順と記録雛形を提供し、既存の実行・転送手段と組み合わせて使う。
