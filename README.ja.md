# CCmite bot
[ウェブサイト](http://ccmite.com/)

# Installation
- [Git](https://git-scm.com/book/ja/v2/%E4%BD%BF%E3%81%84%E5%A7%8B%E3%82%81%E3%82%8B-Git%E3%81%AE%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB)
- [Python](https://www.python.org/downloads/)
- [Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#id13)

# Requirements
- Ubuntuのサーバを用意してください。Vagrantでローカルに用意してもクラウサービスでインスタンスを用意しても構いません。sshで接続できれば大丈夫です。

# Usage
- プロジェクトをクローンします
    ```bash
    git clone git@github.com:okamos/ccmite-discord-bot.git
    ```
- Google Driveの共有ディレクトリにdiscord_bot_vault_passwordというファイルがあるので.vaultというファイル名で保存して使ってください
- ansible.cfgファイルのプライベートキーは適宜サーバへのsshの鍵へのパスを設定してください
- hostsファイルにはサーバーのIPを記載します
- 以下のコマンドでサーバへのデプロイを始めます。終了後にDiscordにボットがオンラインになっていることを確認してください
  ```bash
  ansible-playbook -i hosts server.yml
  ```
