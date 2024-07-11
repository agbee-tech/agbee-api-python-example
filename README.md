## agbee-api-python example
agbeeの外部連携APIにアクセスするpythonのExampleです。APIの利用方法については、こちらの[Agbee APIリファレンス](https://agbee.co.jp/)を参照してください。

## 環境構築
### 現在のpython環境にインストールする場合
```
git clone https://github.com/agbee-tech/agbee-api-python-example
cd agbee-api-python-example
pip3 install .
```

### pyenv + poetryを利用する場合(Ubuntu)
前提環境をインストールをします。
python環境をインストールします。仮想環境は[pyenv](https://github.com/pyenv/pyenv?tab=readme-ov-file#installation)を推奨しています。
```
git clone git://github.com/yyuu/pyenv.git ~/.pyenv
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
```

```
pyenv install 3.12.2
pyenv versions
pyenv global 3.12.2
```

[poetry](https://python-poetry.org/docs/#installing-with-pipx)をインストールします。
```
sudo apt update
sudo apt install pipx
pipx ensurepath
sudo pipx ensurepath --global
```
以下、poetryに紐付けるpythonのpathは使用する環境によって異なります。pyenvを使用する場合、下記の通り実行してください。
```
pipx install poetry==1.3.0
poetry env use /home/$USERNAME/.pyenv/shims/python
```

依存関係をインストールします。
```
git clone https://github.com/agbee-tech/agbee-api-python-example
cd agbee-api-python-example
poetry install
```

## Run
.env.exampleファイルを参考に同じディレクトリ内に.envファイルを作成して、必要な項目を記入します。

```
cd agbee-api-python-example
# poetryの場合
poetry run python agbee_api_python_example/example.py

# pip installの場合
python agbee_api_python_example/example.py
```

