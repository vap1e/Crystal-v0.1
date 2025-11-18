# Crystal-v0.1
Real-time ransomware defense tool made by a first-year university student.

==========================================================
 Crystal v3.1 
==========================================================

最終更新日: 2025年11月

----------------------------------------------------------
 ■ 概要
----------------------------------------------------------
Crystal v3.1 は、ランサムウェア対策の概念実証(PoC)ツールです。

【主な特徴】
 1.  監視: 書き込み速度、高エントロピー、カナリアファイルなど多角的に検知。
 2.  自動インストール: Python環境に必要なライブラリを自動でインストール＆再起動します。
 3.  GUI管理: ホワイトリスト機能により、安全なプロセスを簡単に登録・除外できます。

----------------------------------------------------------
 ■ 起動方法
----------------------------------------------------------
* 本アプリは、配布された「DIST」フォルダ内にある「.exe」ファイルを使用して起動してください。
* 起動時にWindowsのUAC（ユーザーアカウント制御）により、管理者権限が要求されます。
  （防御機能はシステムの深い部分にアクセスするため必須です。）

----------------------------------------------------------
 ■ ⚠️ 免責事項（重要）
----------------------------------------------------------
本アプリは、学習および概念実証（PoC）のために開発されたものであり、開発段階にあります。

1. 【保証の否認】本アプリは、全てのランサムウェア攻撃を防ぐことを保証するものではありません。
2. 【責任の制限】本アプリの使用、または使用できなかったことにより生じた、直接的または間接的ないかなる損害（データの損失、システム障害などを含む）についても、開発者は一切の責任を負いません。
3. 【自己責任】ユーザーは、本アプリを自己の責任において利用するものとします。

★ 公的に、開発者はいかなる損害に対する責任も負わないことをここに表明します。

==========================================================


In English

==========================================================
Crystal v3.1

Last Updated: November 2025

■ Overview

Crystal v3.1 is a Proof-of-Concept (PoC) tool designed for ransomware countermeasures.

Key Features

Monitoring: Detects suspicious behavior through multiple indicators such as write speed, high entropy, and canary files.

Auto Installation: Automatically installs required Python libraries and restarts the environment.

GUI Management: Includes a whitelist feature that allows easy registration and exclusion of trusted processes.

■ How to Launch

Start the application by running the .exe file located in the distributed DIST folder.

When launching, Windows UAC (User Account Control) will request administrator privileges.
(This is required because the protection features access deep system layers.)

■ ⚠️ Disclaimer (Important)

This application is developed for educational use and as a proof-of-concept (PoC), and is still in the development stage.

No Warranty: This application does not guarantee prevention of all ransomware attacks.

Limitation of Liability: The developer assumes no responsibility for any direct or indirect damages arising from the use or inability to use this application, including but not limited to data loss or system failures.

Use at Your Own Risk: Users agree to operate this application at their own responsibility.

★ The developer hereby formally states that no liability of any kind shall be borne for any damages.

==========================================================

