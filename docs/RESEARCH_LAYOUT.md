# Google Drive研究フォルダ標準 v1.3
作成日: 2026-10-17
更新日: 2026-10-17（サーバー計算・Mac/サーバー解析・Drive直接保存に対応）

## 参照と統合方針
参照: https://github.com/shunta0213/research-template
確認した版: 93189445cbc9bf2b4c18c5d999086b99da80bf5d
README.md、AGENTS.md、docs/development.md、scripts/README.mdを参照して作成した独自の統合ガイド。参照元のコードを同梱したものではない。

採用: 共通コード・実験・解析の分離、条件ハッシュ、追記型の判断ログ、日付ノート、圧縮アーカイブ。
維持: Driveを正式保存先にする運用、実験ごとのZIP、閲覧用要約、図のPNG/PDFと個別パネル、再現性、公平な比較、SSDの大規模入力。
任意: DVC、uv、pueue、cjob。利用環境が整ったプロジェクトだけで導入する。
変更: output.npzの存在だけでは完了とせず、各実験の検証基準と完了記録を必要とする。
適用範囲: 新規研究フォルダ。既存プロジェクトの移動・改名・既存ハッシュの変更は行わない。

## 作業領域の標準構成

各フォルダの具体的な役割・配置・命名・READMEのルールは[FOLDER_GUIDE.md](FOLDER_GUIDE.md)を参照する。

計算は研究室サーバー、解析はMacまたはサーバーで行う。正式保存先はDrive。端末別保存先、直接アップロード、解析入力の取得・展開、索引は[DRIVE_WORKFLOW.md](DRIVE_WORKFLOW.md)に従う。GitHubへの研究用リポジトリ作成は任意。

```text
<project>/
  README.md
  AGENTS.md
  src/                       # 共通実装を一元管理
  experiments/<study>/       # 実験固有の計算本体・設定・実行入口
  config/paths.example.json  # 端末別の保存先設定例
  analysis/<study>/<category>/ # 解析結果と記録
    README.md
    analysis_config.json
    png/panels/
    pdf/panels/
    csv/
    md/
  analysis/compare/          # 複数実験比較
  data/inputs/               # 外部入力（出典・版・checksum）
  data/runs/<study>/<config_id>/<run_id>/
    config.json
    metadata.json
    raw/                     # JSON/CSV/NPZなど既存の形式を使用
    checkpoints/
    logs/
    status.json
  docs/                      # 入出力仕様・設計判断・手順
  notes/                     # YYYY-MM-DD.md
  refs/                      # 文献と書誌情報
  scripts/                   # 保存・復元・検証などの補助
  tests/                     # 必要な単体・通し検証
  archive/                   # 確定した保存パッケージ
  cache/                     # 再生成可能。転送しない
  tmp/                       # 一時作業。転送しない
```

空フォルダは必要になった時点で作成する。共通コードはsrc/を参照し、実験ごとに複製しない。
experiments/にはコード・設定、data/runs/には計算出力、analysis/には解析ごとの成果物を置き、解析コードはsrc/やscripts/で共有する。
実験ID（study）で3か所を対応させ、READMEからリンクする。PNG/PDFの相対名を一致させる。
必要なSVGも保持する。個別パネルは独立して描画し、切り抜きで代替しない。

## Drive上の構成
```text
<project>/
  README.md                  # 目的・索引・実験一覧・正式保存先
  AGENTS.md                  # エージェント向け必須ルール
  src/、experiments/          # 日常編集するコード・設定
  analysis/                  # 図・主要指標・解析コード
  data/                      # 少量の入力・結果。大量出力は下記の方式で保存
  docs/                      # 人間が直接読む共通仕様
  notes/                     # 日付ノート
  refs/                      # 必要な文献
  archive/<study>/<package_id>/
    README.md
    summary.csv              # 該当する場合
    overview.pdf             # 該当する場合
    artifacts.zip
```

Macではコード・文書・閲覧用成果物をDrive内で直接扱える。サーバーでは同じ版のコードと設定を用意する。実行時のsnapshotを保存パッケージに固定する。
大量の生データや高頻度のcheckpointはDrive外の作業先で生成し、アーカイブでまとめてサーバーから直接保存する。
少量の結果はDrive内に直接生成してもよい。ZIP化しても元ファイルの自動同期は止まらない。
Pythonは各端末のDrive外にある既存のローカル仮想環境で実行する。Macとサーバーで環境本体を共有せず、Drive内に.venvを作らない。環境の場所・Pythonとライブラリ版・依存定義を実行記録に残す。
.gitignoreはDrive同期を制御しない。仮想環境・キャッシュ・一時ファイル・秘密情報の生成先はDrive外に設定する。
artifacts.zip内部では上記の論理的な相対パスを保持し、実際の生成先はmetadataに記録する。
ZIPには対象実験のデータ・解析・コード・設定と、それらが依存する共通src/や環境定義も含める。
検証済みの別コードパッケージを参照する場合はDriveリンク・版・checksumを明記する。
ローカルにarchive/を同時に保持していても、ZIP内部に過去のarchive/やZIP自体を再帰的に含めない。
DriveのREADMEにはstudy、条件hash、run ID、package ID、状態、保存先リンクを一覧化する。
ノートは日単位でまとめ、細かな操作ごとに新規ファイルを送信しない。

## 実験の識別と完了判定
- study: 問題・方法・保存スキーマのまとまり。破壊的な変更はstudy-v2を作り、docs/decisions.mdに残す。
- config_hash: 結果に影響する条件を正規化したJSONのSHA-256。キー順・型・単位・スキーマ版を仕様化する。
  問題・入力データのchecksum、encoding、手法、seed、評価予算、学習条件、探索条件、backend、数値精度、
  結果に影響するコード版を含める。日時や保存先だけの変更で条件hashを変えない。
  同じ条件の再試行も別のrun_idで保存し、成功・失敗を上書きしない。
- config_id: フォルダ用の短い条件ID。完全なconfig_hashとの対応を索引に記録する。
- run_id / package_id / analysis_id: 短いIDを使い、日時や条件を名前に連結しない。[NAMING.md](NAMING.md)に従い、重複を確認する。
- metadata.json: 実行コマンド、開始終了日時、環境・依存版、Git commitとdirty状態
  （Gitがない場合はコードsnapshotのchecksum）、入力参照、実行状態を記録する。dirtyの場合も実行時ソースまたは復元可能な差分を保存する。
- analysis_id: 解析試行ごとの一意ID。入力run/package・checksum、選択・除外・集計条件、解析コード版、再現コマンドをanalysis_config.jsonとREADMEに記録する。出力先はanalysis/<study>/<category>/直下のpdf/・png/・csv/とし、再実行は同じ生成ファイルを更新する。新しいanalysis_idは設定・索引に記録し、更新前の実行情報・ソース・checksumをdocs/records/analysis_runs/の記録ファイルに保持する。Notebook/Pythonのセットと図の説明は[ANALYSIS_WORKFLOW.md](ANALYSIS_WORKFLOW.md)に従う。
- status.json: [RUN_STATUS.json](../templates/RUN_STATUS.json)を使い、計算・結果検証・パッケージ検証・Drive保存・解析・全体の状態を別々に記録する。
  raw結果の整合性・必要seed/件数・軌跡長・必須再現用ファイルを検証し、必要な保存と解析も確認してからoverall_status=completeを記録する。
  結果は一時ファイルからの確定書き込みを使い、図の更新やoutputファイルの存在だけで完了扱いにしない。
- 失敗・未完了runも記録して比較対象の範囲を明示する。未測定値を補完・捏造しない。

## 圧縮・転送・復元
1. 実験単位または完了チャンク単位で、変更分だけ保存パッケージをDrive外で作り、検証後にサーバーからDriveへ直接アップロードする。
2. 長時間計算は原則1時間ごと、またはチャンク完了時に、整合性のある途中snapshotを保存する。
3. 新規アーカイブはZIPを標準とする。既存tar等も維持し、再圧縮のためだけに再送しない。アーカイブ内にmanifest.json（相対パス・サイズ・SHA-256）を含める。manifest自体は自己hash対象にしない。
4. READMEにZIPのSHA-256、条件、含むrun、partial/complete、入力参照、再現・復元手順を記載する。
5. .venv、.git、__pycache__、cache、tmp、秘密情報、過去archiveを除外。
   失敗ログ・生データ・必要なcheckpoint・環境定義は保持する。
6. 直接アップロードまたはDrive同期の完了を待ち、クラウド上の存在・サイズ・取得可能checksumを確認し、SHA-256比較ができなければクラウドから再取得して照合する。
   同期フォルダ内のローカルファイルを読み返すだけでクラウド保存を検証済みにしない。
   元データを検証前に削除しない。検証不能なら未検証と報告する。
7. 復元は新しい空の作業先へ行い、ZIPと内部manifestを検証する。既存runに上書き展開しない。
8. 大きすぎる場合はstudy・条件・run群など意味のある単位に分割し、依存関係をREADMEに記載する。
   再圧縮だけを理由に変更のない入力や結果を再送しない。

SSD上の入力はパスだけでなくchecksum・版・取得元を記録する。SSDだけにあるファイルを
Drive保存済みと表現しない。全結果のDrive保存を求められている場合は分割パッケージで保存する。

## DVCを導入するとき
保存は新規ZIPを標準とし、既存tar等も許容する。転送はサーバーで利用している既存手段を使い、特定のDrive connectorを前提にしない。DVCの認証は未設定であり、この雛形はDVC実行環境を含まない。
導入時は閲覧用archive/とDVC専用remoteを分け、圧縮済みパッケージを追跡する。
同じ大容量データを両方式で二重保存しない。DVC pointer・Git版・Drive参照の対応を索引に残す。
GitHubへのpushや公開、認証設定は別の明示的な依頼に従う。

## 既存プロジェクトとの対応
| 新規標準 | PestControl | Intern_Fujitsu |
|---|---|---|
| src/, experiments/ | 03_scripts/、関連コードリポジトリ | src/、experimet/、code/など既存配置 |
| data/runs/ | 01_results/、01_results/01_checkpoints/ | 各実験のjson/、results/ |
| analysis/ | 02_analysis/内の既存分類 | 各実験のpng/pdf/svg/md/ |
| docs/, notes/ | 04_docs/、.context/work/ | report/、md/、既存研究記録 |
| archive/ | 既存分類先内の一意な実行ID | 既存実験保存先内の一意な実行ID |

既存のexperimet/を改名せず、intern/の配布snapshot同期要件も維持する。
PestControlの.context/INDEX.mdと既存の問題別分類・fairness基準を優先する。
新規標準を使うために既存の実験定義・seed・予算・数値条件を変更しない。


## 作業・比較・図の詳細

[状態とジョブ](STATUS_AND_JOBS.md)、[比較と確認実験](RESEARCH_PROTOCOL.md)、[図の設定](FIGURE_POLICY.md)、[引継ぎ](../.context/INDEX.md)を必要な作業だけ参照する。研究固有の予算・seed数・検定をテンプレートから一律に課さない。
