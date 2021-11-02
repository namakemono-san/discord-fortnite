# discord-fortnite

このDiscord Botはフォートナイトコマンドのテンプレートでございます。  
あなたのBotに導入する場合は私の名前（なまけもの）を記入してください。  

現在のバージョン: v1.0.5

# 導入方法

## Pythonの導入

**Pythonの導入がお済みな方は飛ばして構いません。**

[Python](https://python.org/)から**Downloads**にいき、 **Looking for a specific release?** から  
**Python 3.9.6**を[選択](https://www.python.org/downloads/release/python-396/)します。  

### Windows OSの場合

まず最初にPythonをダウンロードします
32bitの場合は [**Windows installer (32-bit)**](https://www.python.org/ftp/python/3.9.6/python-3.9.6.exe)  
64bitの場合は [**Windows installer (64-bit)**](https://www.python.org/ftp/python/3.9.6/python-3.9.6-amd64.exe)  
ダウンロードが完了しましたら起動してください。
起動したら**Add Python 3.9 to PATH**に必ずチェックを入れて**Install Now**をクリックしてください。  
インストールが完了しましたら閉じてください。  
次にコマンドプロンプトを起動して、そこに`python --version`を入力し、**Python 3.9.6**が表示されましたらインストールが完了です。

### Mac OSの場合

#### Homebrewのインストール
**Homebrew**を先にインストールします。（作成者はこれしか知らないので...）  
`/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`  
これをMac OSのターミナルに貼り付けてください。  

#### Pythonのインストール
次にPythonをインストールします。  
`brew install python@3.9` を実行してください。  
実行してインストールが完了したら、インストールができているか確認するため  
ターミナルに`python3 --version`を入力し、**Python 3.9.x**が表示されたらダウンロード完了です。  
※ Python 3.9.x のxは最新バージョンでございます、時間が立つごとに数字が変わるので違くても大丈夫です。

## Discord-Fortniteの設定

まず[この](https://github.com/namakemono-san/discord-fortnite)ページに飛び、**Code**から**Download ZIP**をクリックします。  
ダウンロードができましたら、ファイルを解凍します。  
解凍できましたらまず最初に**install.bat**を起動してください。（ライブラリーのインストール）
**続行するには何かキーを押してください . . .** という表示が出たらインストール完了です。
インストールができましたら次に**config.json**を開きます。**Token**というところに自分のDiscordBotのトークンを入力してください。
※ Discord Botの作成から取得方法を解説しています。
**lang**はAPIの言語設定でございます。（初期設定: ja）
**prefix**はbotのプレフィックスでございます。（初期設定: fn!）
設定が完了しましたら **run.bat** を起動してください。
起動して **Discord Botが起動しました。** と表示されましたらBotの準備が完了です。お疲れさまでした。
※ここでエラーが発生した場合はTwitter(namakemono_san5)にDMでご連絡ください。（確認は遅れます）

# Discord Botの作成

[Discord Developer Portal](https://discord.com/developers/applications)から**New Application**をクリックし  
お好きな名前を入力し**Create**をクリックしてください。  
General InformationからBotのアイコンや名前を変更することが可能です。  
次にBotの左のタブから**Bot**という欄に飛び、**Add Bot**を押します。  
**ADD A BOT TO THIS APP?** というものが出ますが **Yes, do it!** をクリックしてください。  
Botページが開けましたら、**TOKEN**という欄から**Copy**をクリックしてください。  
コピーしたトークンは**discord-fortnite**の**config.json**にある**Token**の欄に貼り付けてください。

# ライセンス

[MITライセンス](LICENCE)

このソフトウェアを無制限で使用することができます  
商用、非商用、改変、再配布なども許可されます  
ただし、著作権表示と英語のライセンス全文を目に留まる場所に配置してください  
このソフトウェアの使用によって発生したいかなる損害にも責任を負いません  