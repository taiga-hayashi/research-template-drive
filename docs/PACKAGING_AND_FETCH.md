# サーバーでまとめ、必要なデータだけ取得する

この手順はPython 3.10以上の標準ライブラリと、認証済みの既存rcloneを使う。Pythonは各端末の既存のローカル仮想環境を有効にして使う。環境の新規作成・依存更新・rclone認証の設定は行わない。転送設定やトークンを雛形へ書き込まない。

## サーバー側で何をまとめるか

保存単位は、検証可能な実験・完了run・seed群・計算チャンクとする。原則1時間ごと、またはチャンク完了時に保存する。実行中のディレクトリをそのまま渡さず、計算が確定したrunか、一貫性のある保存済みcheckpointと対応ファイルを凍結したsnapshotを使う。

| 必要な対象 | 梱包先の例 | 確認すること |
|---|---|---|
| 生データ・history・samples・ログ | `data/runs/<study>/<config_hash>/<run_id>/` | 完了範囲・seed・モデル・評価回数 |
| 再開に必要なcheckpoint | 同じrunの下、または既存の対応階層 | checksum・cycle・結果との対応 |
| 実行時ソース・描画コード | `code_snapshot/` | 現在の最新版ではなく実行した版。dirty変更も含む |
| 設定・seed・依存定義・入力参照 | 元のrun内、または`records/` | 大規模入力を省略する場合はDrive参照・版・checksum |
| 実行と再現方法の説明 | `records/run-record.md`等 | 実行コマンド・環境・検証結果・再開方法 |
| その時点の全図・独立パネル | 元の相対パス | 解析前なら後の解析パッケージで保存 |

別保存のcheckpointを同じZIPにまとめる場合はsourcesへ追加する。別パッケージで保存する場合は双方のpackage_idとchecksumを索引・run-recordへ記載する。既存の`checkpoints.tar`を中へ含めることも可能だが、ZIPは中のtarを自動展開しない。元の階層を変える必要はない。

`.venv`、`.git`、cache、tmp、過去archive、`.secrets`、`.env`（`.env.example`を除く）、`.pem`、`.key`、credentials.json、*.local.json等は収集から除外する。シンボリックリンクは拒否する。ファイル名の除外は秘密情報の内容検査ではないため、対象コード・文書・ログに秘密が混入していないことも確認する。プロジェクト全体を無条件に指定せず、必要なsnapshotだけを明示する。

## 1. 梱包仕様を記入する

[PACKAGE_SPEC.json](../templates/PACKAGE_SPEC.json)を`config/package.local.json`へコピーする。sourceにはそのサーバーでの絶対パス、targetにはZIP内の相対パスを書く。複数のsourceを対応する論理パスへ集められる。required_pathsに必須ファイルまたはフォルダを列挙する。

- package_idは毎回一意にし、同じ保存先を使い回さない。
- study・run_ids・code_version・compute_statusを実データに合わせる。
- snapshot_confirmedは保存範囲が凍結されていることを確認してからtrueにする。
- 必須のコード・設定・ログ・checkpointを指定したか、人が仕様と対象一覧を確認する。ツールは実験固有の必要ファイルや計算の正しさを自動判定しない。
- sources/required_pathsは例を研究の既存階層へ変更してよい。PestControlでは`01_results/<problem>/...`と`01_results/01_checkpoints/<problem>/...`をtargetにして元の相対パスを保持できる。

```sh
python3 scripts/artifacts.py pack --spec config/package.local.json --dry-run
```

対象ファイル一覧とサイズを表示するだけで、ZIP作成やアップロードはしない。除外されたファイルが必要なものではないか確認する。フォルダが空の場合は収録されない。隠しファイルも、除外対象以外は収集する。

## 2. 作成して検証する

```sh
python3 scripts/artifacts.py pack --spec config/package.local.json \
  --output /absolute/path/to/staging/unique-package-id
```

出力先は収集元の外にある新規フォルダにする。既存の保存先には上書きしない。作成中にファイルのサイズ・更新時刻等が変われば失敗させるが、凍結snapshotの代わりにはならない。

```text
unique-package-id/
  README.md
  artifacts.zip          # ZIP64、内部manifest.json付き
  SHA256SUMS.txt
  package-report.json
```

内部manifestは各ファイルのパス・サイズ・SHA-256とrun情報を含む。元のサーバー絶対パスはmanifestへ保存しない。既に圧縮済みのファイルは不要な再圧縮を避ける。梱包後にZIP全体と内部manifestを読み戻して検証する。

閲覧用summary.csv・overview.pdfがある場合はパッケージの外にも置く。ツールはそれらを生成せず、必要なら同じ保存先へコピーする。READMEは最低限を自動生成するので、研究固有の結果・検証・復元方法を[RUN_README.md](../templates/RUN_README.md)に沿って補足する。

再検証する場合は、保存記録のSHA-256を明示する。

```sh
python3 scripts/artifacts.py verify \
  --archive /absolute/path/to/staging/unique-package-id/artifacts.zip \
  --sha256 REPLACE_WITH_64_HEX_DIGITS
```

## 3. 既存rcloneでDriveへ保存する

以下は例。認証済みremoteと新規保存先へ置き換えて実行する。ツールのpackは自動アップロードしない。

```sh
rclone copy /absolute/path/to/staging/unique-package-id \
  drive:ResearchProject/archive/study/unique-package-id --immutable
```

新規package_idを使用し、転送完了後にクラウド上の存在・サイズを確認する。アーカイブのクラウド内容を検証するには、次のfetchをサーバー上でrcloneの保存先から実行できる。ローカルの同名ファイルや同じ端末のキャッシュを読むだけでは転送確認にならないため、クラウドからの再取得検証は新しい空のcache_rootを使う。README等の閲覧用ファイルの転送も別途確認する。

package-report.jsonのstorage_statusはpack時点でpending。取得成功が計算結果の妥当性や必要件数まで保証するわけではない。検証根拠を索引へ記録し、保存検証前に元データを削除しない。

## 4. Mac／サーバーで必要なパッケージだけ取得する

[DOWNLOAD_REQUEST.json](../templates/DOWNLOAD_REQUEST.json)を`config/downloads.local.json`へコピーする。packagesには今回解析に必要なものだけを列挙し、package_id、信頼できる保存記録のSHA-256、rclone上のファイルパスを記入する。DriveのブラウザーURLは参照用のdrive_urlへ書き、source.pathにはrcloneのremote:pathを書く。

```sh
python3 scripts/artifacts.py fetch --request config/downloads.local.json \
  --paths config/paths.local.json --profile mac

# サーバーで解析する場合はprofileを切り替える
python3 scripts/artifacts.py fetch --request config/downloads.local.json \
  --paths config/paths.local.json --profile server
```

処理は次の順に進む。

1. rclone lsjson --statで単一ファイルと確認し、指定ファイルだけをrclone copytoで一時領域へ取得する。フォルダ全体は取得しない。
2. ZIP全体のSHA-256を指定値と照合する。
3. 内部manifestと全ファイルのサイズ・SHA-256を照合する。
4. パス逸脱・リンク・重複等を拒否し、新しい展開先へ復元する。
5. 取得・検証結果と実際の保存先をJSONで標準出力へ報告する。必要ならローカルの作業記録へ保存する。

```text
cache_root/packages/<sha256>/artifact.archive

data_root/_packages/<package_id>/
  manifest.json
  data/...                  # 標準のtargetを使った場合
  code_snapshot/...
  records/...
```

復元は専用の新規フォルダへ行い、既存のdata/runsやPestControlの階層には書き戻さない。analysis_config.jsonのrelative_pathには`_packages/<package_id>/data/runs/...`を指定する。既存階層のパッケージなら`_packages/<package_id>/01_results/...`となる。fetch結果のpayload_data_rootは標準のdata/配下の便宜的な場所であり、旧階層にdata/がない場合は存在を仮定しない。

同じchecksumのキャッシュは毎回SHA-256を再検証して利用する。既存の展開先がある場合は上書きせず停止する。やり直す場合は、元の展開データを確認したうえで別のdata_rootを指定する。複数packageは順番に処理し、途中で失敗した場合も先に正常復元したpackageは保持し、completed_packagesとして報告する。再試行時は成功済みのpackageを取得指定から外す。索引・状態の更新や原本削除は自動では行わない。

rclone以外で既にダウンロード済みの場合はsource.kindをlocal、source.pathをローカル絶対パスにすれば、同じ検証・展開を行える。localによる取得はクラウドからの再取得検証ではない。

## 旧tarや別形式のZIP

このツールの自動展開は、ここで作成したschema_version=1の内部manifestを持つZIPを対象にする。旧tar等は次で指定したSHA-256を照合して取得するだけにできる。

```sh
python3 scripts/artifacts.py fetch --request config/downloads.local.json \
  --paths config/paths.local.json --profile mac --archive-only
```

archive-onlyでは内部manifest検証・展開は行わず、internal_manifest_verified=falseを報告する。旧形式の復元はその実験の既存手順を使い、自動展開済み・内部検証済みと扱わない。形式を変えるためだけに元のtarを再圧縮しない。

## 対応範囲と参考

対象は通常ファイルと相対パス、内部manifestは16MiBまで。大きすぎる保存単位はrunやチャンクで分割する。成果物の取得・検証・復元は行うが、実験や解析コードを実行せず、科学的妥当性の検証は行わない。

- [rclone lsjson](https://rclone.org/commands/rclone_lsjson/)
- [rclone copyto](https://rclone.org/commands/rclone_copyto/)
- [rclone copy](https://rclone.org/commands/rclone_copy/)
- [Python zipfile](https://docs.python.org/3.11/library/zipfile.html)
