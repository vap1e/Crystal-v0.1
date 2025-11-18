Crystal v0.1 は、ランサムウェアの挙動を早期に検知することを目的とした教育・研究用途向けの概念実証（PoC）ツールです。商用アンチランサムウェア製品のような完全な保護を保証するものではありません。

【主な機能】
・ファイルの異常な変更（高速書き込み、高エントロピー化など）の監視
・カナリアファイルの監視
・不審プロセスの検知および強制停止
・ホワイトリストおよびブラックリストの管理
・簡易 GUI による設定
・プロセス制御のための管理者権限の要求
・設定の保存（永続化）

【動作環境】
・Windows 10 / 11（64bit）
・Python 3.11 以上
・管理者権限が必要

【インストール方法】

requirements.txt を使用して必要なライブラリをインストールします。

main.py を実行します。
初回起動時に依存ライブラリが自動インストールされる場合があります。一部の機能は再起動後に有効になります。

【安全上の注意】
・本ツールを本番環境や業務端末に導入しないでください。
・学校や会社の PC など、自分の所有物でない環境に無断でインストールしないでください。
・誤検知により正常なプロセスが終了する可能性があります。
・必ず仮想環境やテスト用 PC で使用してください。
・このツールを攻撃目的で使用することは禁止されています。

【禁止事項】
・本ツールを攻撃行為や不正行為の補助目的で使用すること
・第三者の PC やネットワークに無断で導入・使用すること
・法律や組織の規則に反する用途で使用すること
※Crystal には攻撃用コードやマルウェアは含まれていません。

【想定される用途】
・ランサムウェアの挙動研究
・セキュリティ教育・学習
・研究室内での検証
・PoC 手法の確認やデモ

【免責事項】
Crystal v0.1 は現状のまま（AS IS）提供されます。
開発者は以下に対して責任を負いません。
・データ損失
・システム障害
・誤検知や機能の不具合による影響
・その他の直接的または間接的な損害
利用者自身の責任において使用してください。

【ライセンス】
本プロジェクトは MIT License の下で公開されています。

🇺🇸 English README (Text Only)

Crystal v0.1 is a Proof-of-Concept (PoC) tool designed to demonstrate early detection techniques for ransomware behavior. It is intended solely for educational and research purposes and does not provide the full protection of a commercial anti-ransomware product.

[Features]

Monitoring abnormal file modifications such as high write rates and high entropy

Canary file integrity monitoring

Detection and termination of suspicious processes

Whitelist and blacklist management

Simple graphical user interface

Requires administrator privileges for process control

Persistent configuration storage

[System Requirements]

Windows 10 / 11 (64-bit)

Python 3.11 or higher

Administrator privileges

[Installation]

Install required libraries using requirements.txt

Run main.py
On first launch, some dependencies may be installed automatically. Certain features may require a system reboot.

[Safety Notes]

Do not install this tool on production systems or work machines.

Do not install it on systems you do not own, such as school or company PCs, without permission.

False positives may terminate legitimate processes.

Always use this tool in a virtual machine or isolated test environment.

Offensive or malicious use of this tool is strictly prohibited.

[Prohibited Use]

Using this tool to assist attacks or illegal activities

Deploying or using it on third-party systems without authorization

Any use that violates laws or organizational policies
Note: Crystal does not include ransomware, malicious code, or attack tools.

[Intended Use Cases]

Ransomware behavior analysis

Cybersecurity education and training

Research laboratory testing

Demonstration of PoC defensive techniques

[Disclaimer]
Crystal v0.1 is provided “AS IS” without warranty of any kind.
The developer is not responsible for:

Data loss

System damage

Effects resulting from false detections or malfunction

Any direct or indirect damages
Use this tool at your own risk.

[License]
This project is released under the MIT License.
