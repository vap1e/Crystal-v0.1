Crystal v3 は、Windows 上でランサムウェアのような不審挙動を検知することを目的とした、教育・研究用途向けの概念実証（Proof of Concept）ツールです。本ツールは防御機能のアイデア検証を目的としており、実運用環境での利用や完全な保護を保証するものではありません。

【主な機能】
・監視ディレクトリ内のファイル変更イベントの検知（watchdog 使用）
・CANARY ファイルの自動生成と監視
・高エントロピー化ファイルの検知
・高書き込みレートを示すプロセスの検出および kill（設定により実行）
・不審拡張子の生成検知
・大量リネーム（burst rename）挙動の検知
・レジストリ Run キーの監視
・ハニーポート（疑似 SMB 風ポート）へのアクセス検知
・疑わしいファイルを隔離フォルダへコピー（active mode 時）
・ホワイトリスト管理 GUI
・リアルタイムログとリスクスコア表示
・依存ライブラリが無い場合の自動インストールと再起動

【動作モード】
・シミュレーションモード（dry_run=True）
　検知のみで kill・隔離・防御コマンドを実行しません。
・アクティブモード（dry_run=False）
　プロセス終了、隔離、Firewall 一括遮断、ネットワークドライブ切断、VSS スナップショットなどを実際に行います。

【必要環境】
・Windows 10 / 11（64bit）
・Python 3.11 以上
・管理者権限（必須）
・インターネット接続（初回の依存ライブラリ自動インストール時に必要）

【依存関係】（コードより抽出済み）
・watchdog
・psutil
・pywin32（win32api のため）
これらは起動時に自動チェックされ、不足していれば GUI で確認後 pip により自動インストールされ、再起動されます。

【監視対象】
・ユーザーデスクトップ
・ドキュメント
（config_v3.json にて変更可能）

【トリガー条件（抜粋）】
・CANARY ファイルを触られる
・高エントロピーのファイルが連続で生成・更新される
・大量の rename イベント
・不審拡張子（.encrypted / .crypted など）の生成
・レジストリ Run キーが変化
・ハニーポートへのアクセス
・プロセスの高速書き込み（デフォルト 50MB/s 超）

これらをスコア化し、閾値に達した場合に防御アクションを実行（またはシミュレーション）します。

【注意事項】
・本ツールは Windows のシステム API・ファイル監視・プロセス操作・レジストリ操作を行います。
・誤検知により正規のプロセスが kill される可能性があります。
・重要データが存在する環境では絶対に使用しないでください。
・必ず仮想環境・テスト用 PC で使用してください。
・学校・企業・他者所有の PC に無断で導入しないでください。
・攻撃目的での利用は禁止します（攻撃用コードは含まれていません）。

【免責事項（重要・強化版）】
Crystal v3 は「現状のまま (AS IS)」で提供され、いかなる種類の保証も行いません。
開発者は、以下を含むあらゆる損害・不具合について一切の責任を負いません。
・データ消失、破損
・システム障害、OS 動作不全
・プロセス kill による業務停止
・不正検知・誤検知
・誤設定や利用者の操作による影響
・本ツールを使用した結果生じた直接的・間接的な損害
本ツールの使用により生じた結果はすべて利用者自身の責任となります。
本ツールを使用した時点で、利用者はこれらの免責に同意したものとします。

【ライセンス】
MIT License（ソフトウェアの利用責任は全て利用者にあります）

🇺🇸 Crystal v3 — README (Text Only / Strong Disclaimer)

Crystal v3 is a Proof-of-Concept (PoC) tool designed for educational and research purposes to illustrate defensive techniques against ransomware-like behavior on Windows systems. It is not intended for production use, and it does not guarantee any form of full protection.

[Key Features]

File system monitoring using watchdog

Automatic creation and monitoring of CANARY files

High-entropy file detection

Process write-rate monitoring with optional automatic termination

Detection of suspicious extensions

Burst rename detection

Registry monitoring for Run keys

Honeypot TCP ports

Automatic isolation copy for suspicious files (active mode only)

GUI with whitelist management

Real-time log and scoring system

Automatic dependency installation with restart

[Modes]
Simulation mode (dry_run=True): detection only.
Active mode (dry_run=False): process termination, isolation, firewall blocking, disconnecting network drives, and VSS snapshot creation.

[Requirements]

Windows 10 / 11 (64-bit)

Python 3.11+

Administrator privileges (mandatory)

Internet access for first-time dependency installation

[Monitored Targets]

Desktop

Documents
(these can be changed in config_v3.json)

[Trigger Examples]

CANARY file modification

Multiple high-entropy file writes

Burst rename events

Creation of suspicious file extensions

Registry Run key changes

Honeypot port connections

High write-rate processes (default 50MB/s)

Once the internal score exceeds the configured threshold, defensive actions are triggered (or simulated).

[Important Notes]

This tool interacts with low-level Windows APIs, processes, registry keys, and filesystem events.

False positives may kill legitimate processes.

Do NOT use this on machines containing important data.

Only use inside virtual machines or testing PCs.

Do NOT install on computers you do not own.

Offensive or malicious use is prohibited (no attack code is included).

[Disclaimer (Strong)]
Crystal v3 is provided strictly “AS IS,” without any warranties, express or implied.
The developer assumes absolutely no responsibility for any kind of damage or loss, including but not limited to:

data loss or corruption

system instability or failure

termination of legitimate processes

false positives or misdetections

improper configuration or misuse

any direct, indirect, incidental, or consequential damages
All risks and responsibilities related to the use of this tool rest entirely with the user.
By using this software, the user agrees to all responsibility and fully accepts the disclaimer.

[License]
MIT License (All responsibility of use lies solely with the user)
