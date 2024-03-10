# InternetTV
## 1. データベースを構築する
### データベース設計の前に
画面図など，仕様を決めておく


### 論理設計
どんなものを作るか，概念的に作る
#### 1.エンティティの定義
システムを作るにあたって必要な事象を定義する。
どういうデータがシステム上で出てきて，保存する必要があるかを可視化する。
1. 何をデータとして保存するかを書き出す
* システムで使用するもの
```
例
 1.農学部，2.工学部
 1.農学，3.心理学
```

* ユーザーが登録するもの
```
例
　101.小野，230.内田
（小野が心理学を受講，小野が農学部に所属）
```

2. 具体的なデータを抽象化してエンティティ（実体）としてまとめる
```
例
 1.農学部，2.工学部 →　学部ID，学部名
 1.農学，3.心理学 →　科目ID,科目名
 101.小野，230.内田 →　生徒ID，生徒名
```

* インターネットTV
```
エンティティの定義
 * チャンネル:
 　ドラマ1、ドラマ2、アニメ1、アニメ2、スポーツ、ペット
 * 放映時間:

 * 各エピソード情報：
  -シーズン数，
  -エピソード数，
  -タイトル，
  -エピソード詳細，
  -動画時間，
  -公開日，
  -視聴数，
  （単発エピソードの場合は，シーズン数，エピソード数は表示されない）

 * ジャンル名（アニメ、映画、ドラマ、ニュース）:
   各番組は1つ以上のジャンルに属する

* 番組情報として，タイトル、番組詳細、ジャンルが画面上に表示される
* KPIとして、チャンネルの番組枠のエピソードごとに視聴数を記録する。なお、一つのエピソードは複数の異なるチャンネル及び番組枠で放送されることがあるので、属するチャンネルの番組枠ごとに視聴数がどうだったかも追えるようにする
```


3. テーブル名と列名を定義し，データを入れる
>例）
>
>| 生徒名 | 学部ID | 学部名 | 科目ID | 科目名 |
>| ---- | ---- | ---- | ---- | ---- |
>| 小野 | 101 | 農学部 | 3 | 心理学 |

>インターネットTV
>
>| カラム名 | データ型 |	NULL | キー | 初期値 | AUTO INCREMENT | ユニークキー制約 |
>| ------- |------- | ---- | ---- | ---- | ---- | ------- |
>|チャンネルid|bigint(20)||PRIMARY||YES||
>|チャンネル|varchar(100)||INDEX||||
>|放映時間|time||||||
>|シーズン数|INTEGER||||||
>|エピソード数|INTEGER|||||YES|
>|タイトル|varchar(100)||||||
>|エピソード詳細|text|YES|||||
>|動画時間|time||||||
>|公開日|date|YES|||||
>|視聴数|bigint(20)|||0|||
>|ジャンル名|varchar(100)||INDEX||||
>
>　＊外部キー制約（子テーブルにだけ設定）

#### 2.正規化
データの重複（冗長性）をなくし，データの不整合（非一貫性）をなくすようにデータベースを設計する設計手法
* データを一意に特定できるように，PRIMARY（主キー）を設定する
1. 第一正規化
　1つのセルの中には1つの値しか含まない形
　　第一正規系にする際は，データが増えてもカラムの追加なしで対応できるようにする
2. 第二正規化
　部分的関数従属性（主キーの一部のカラムに対して従属するカラムがある）をなくした形
　　方法：テーブル分割することが基本的な手法
3. 第三正規化
　第二正規形推移的関数従属性をなくした形
　　方法：テーブル分割することが基本的な手法
4. ボイスコット正規化
* 第三正規形から，非キーから主キーへの関数従属性をなくした形
  - 方法：テーブル分割することが基本的な手法

> インターネットTV テーブル設計（正規化後）

> * テーブル：channels

>| カラム名 | データ型 |	NULL | キー | 初期値 | AUTO INCREMENT | ユニークキー制約 |
>| ------- |------- | ---- | ---- | ---- | ---- | ------- |
>|channel_id|bigint(20)|NO|PRIMARY||YES||
>|channel|varchar(100)|NO|INDEX||||
>

> * テーブル：titles

>| カラム名 | データ型 |	NULL | キー | 初期値 | AUTO INCREMENT | ユニークキー制約 |
>| ------- |------- | ---- | ---- | ---- | ---- | ------- |
>|channel_id|bigint(20)|NO|||||
>|title|varchar(100)|NO|||||
>|title_id|bigint(20)|NO|PRIMARY||YES||
>  - 外部キー制約：channel_id に対して、channel テーブルの channel_id カラムから設定

> * テーブル：seasons

>| カラム名 | データ型 |	NULL | キー | 初期値 | AUTO INCREMENT | ユニークキー制約 |
>| ------- |------- | ---- | ---- | ---- | ---- | ------- |
>|channel_id|bigint(20)|NO|||||
>|season_number|INTEGER|NO|||||
>|season_id|bigint(20)|NO|PRIMARY||YES||
>  - 外部キー制約：channel_id に対して、channel テーブルの channel_id カラムから設定

> * テーブル：episodes

>| カラム名 | データ型 |	NULL | キー | 初期値 | AUTO INCREMENT | ユニークキー制約 |
>| ------- |------- | ---- | ---- | ---- | ---- | ------- |
>|channel_id|bigint(20)|NO|||||
>|episode_number|INTEGER|NO||||YES|
>|episode_detail|text|YES|||||
>|video_time|time|NO|||||
>|release_date|date|YES|||||
>|watching_number|bigint(20)|NO||0|||
>|episode_id|bigint(20)|NO|PRIMARY||YES||
>  - 外部キー制約：channel_id に対して、channel テーブルの channel_id カラムから設定

> * テーブル：genres

>| カラム名 | データ型 |	NULL | キー | 初期値 | AUTO INCREMENT | ユニークキー制約 |
>| ------- |------- | ---- | ---- | ---- | ---- | ------- |
>|channel_id|bigint(20)|NO|||||
>|genre_name|varchar(100)|NO|INDEX||||
>|genre_id|bigint(20)|NO|PRIMARY||YES||
>  - 外部キー制約：channel_id に対して、channel テーブルの channel_id カラムから設定

> * テーブル：airing_time

>| カラム名 | データ型 |	NULL | キー | 初期値 | AUTO INCREMENT | ユニークキー制約 |
>| ------- |------- | ---- | ---- | ---- | ---- | ------- |
>|channel_id|bigint(20)|NO|||||
>|episode_number|INTEGER|NO||||YES|
>|broadcasting_start_time|time|NO|||||
>|broadcasting_end_time|time|NO|||||
>|airing_time_id|bigint(20)|NO|PRIMARY||YES||
>|airing_date|date|NO|||||
>  - 外部キー制約：channel_id に対して、channel テーブルの channel_id カラムから設定

> インターネットTV テーブル設計（SQL文）


#### 3.リレーションの直行性のチェック
  * DB全体（複数のリレーション間）で同じ値を含まないようにする
    - 方法：カラムの名前を統一する
        - 共通のデータは１箇所にまとめる
        - アプリケーションコードも必要に応じて修正する
        * 全てのデータを直行化しなくても良い（例えばIDのような主キー）

#### 4.ER図の作成
  * 各テーブルの持つデータとデーブル同士の関係を整理するための図
    - テーブル同士の関係は，1対1，1対多，多対多がある
    - 正規化することで，1対多の関係が生まれる
    - 多対多の場合は中間テーブルを作成し，1対多の形にする

### 物理設計
#### 5.テーブル定義
　データベース上でテーブルを作成するために必要なコクモクを定義する。
* テーブル名
 - カラム名
 - データ型：INTEGER，VARCHAR，DATEなど
 - PK（プライマリーキー）：その値を指定すれば，必ず１行のレコードが特定できる列の組み合わせ。主キーともいう。
 - UK(ユニークキー)：重複を許さない列の組み合わせ。例えば，メールアドレスの列。何個でも設定可能
 - NOT NULL制約：NULLを入れてはならないとする制約
 - デフォルト値：データ登録時に該当列が空白だった際に指定のデフォルト値を入れる
 - 外部キー制約：他のテーブルのデータを参照するようにカラムにつける制約。親テーブルに存在しているデータしか子テーブルには保存できなくなる。他のテーブルの列を参照する場合は設定する。外部キーに使用する列は，何らかのコードやID等の表記体系の定まったデータを用いる。
  * 外部キー制約のアクション：RESTRICT／デフォルト，CASCADE／親テーブルのレコードが変更されたら，子テーブルも変更削除される
　
#### 6.インデックス設定
索引を作ることで検索が速くなる

## 2. ステップ1で設計したテーブルを構築します
* テーブルの作成
  - SQL文
---
CREATE TABLE channels (
    channel_id BIGINT(20) NOT NULL AUTO_INCREMENT,
    channel VARCHAR(100) NOT NULL,
    PRIMARY KEY (channel_id)
);

CREATE TABLE titles (
    channel_id BIGINT(20) NOT NULL,
    title VARCHAR(100) NOT NULL,
    title_id BIGINT(20) NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (title_id)
);

CREATE TABLE seasons (
    channel_id BIGINT(20) NOT NULL,
    season_number INTEGER NOT NULL,
    season_id BIGINT(20) NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (season_id)
);

CREATE TABLE episodes (
    channel_id BIGINT(20) NOT NULL,
    episode_number INTEGER NOT NULL,
    episode_detail TEXT,
    video_time TIME NOT NULL,
    release_date DATE,
    watching_number BIGINT(20) NOT NULL DEFAULT 0,
    episode_id BIGINT(20) NOT NULL AUTO_INCREMENT,
    title_id BIGINT(20) NOT NULL,
    PRIMARY KEY (episode_id)
);

CREATE TABLE genres (
    channel_id BIGINT(20) NOT NULL,
    genre_name VARCHAR(100) NOT NULL,
    genre_id BIGINT(20) NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (genre_id)
);

CREATE TABLE airing_time (
    channel_id BIGINT(20) NOT NULL,
    episode_number INTEGER NOT NULL,
    broadcasting_start_time TIME NOT NULL,
    broadcasting_time_id BIGINT(20) NOT NULL AUTO_INCREMENT,
    broadcasting_end_time TIME NOT NULL,
    PRIMARY KEY (airing_time_id)
);

- 各テーブルに外部キー制約を追加する
ALTER TABLE titles
ADD CONSTRAINT fk_titles_channel_id
FOREIGN KEY (channel_id) REFERENCES channels(channel_id);

ALTER TABLE seasons
ADD CONSTRAINT fk_seasons_channel_id
FOREIGN KEY (channel_id) REFERENCES channels(channel_id);

ALTER TABLE episodes
ADD CONSTRAINT fk_episodes_channel_id
FOREIGN KEY (channel_id) REFERENCES channels(channel_id);

ALTER TABLE genres
ADD CONSTRAINT fk_genres_channel_id
FOREIGN KEY (channel_id) REFERENCES channels(channel_id);

ALTER TABLE airing_time
ADD CONSTRAINT fk_airing_time_channel_id
FOREIGN KEY (channel_id) REFERENCES channels(channel_id);

ALTER TABLE episodes
ADD CONSTRAINT fk_episodes_titles_title_id FOREIGN KEY (title_id) REFERENCES titles(title_id);



---
* テーブルの確認
  - SHOW TABLES;
  - SHOW COLUMNS FROM <テーブル名>;


## 3. サンプルデータを入れます。

-- チャンネルを追加
INSERT INTO channels (channel) VALUES
    -> ('ドラマ'),
    -> ('アニメ'),
    -> ('スポーツ'),
    -> ('ペット');

-- タイトルを追加
INSERT INTO titles (channel_id, title) VALUES
    -> (1, '鬼滅の刃'),
    -> (2, '進撃の巨人'),
    -> (3, 'ワールドカップ'),
    -> (4, 'かわいいペットたち');

-- 「鬼滅の刃」のシーズン1〜4を追加
INSERT INTO seasons (channel_id, season_number, season_id) VALUES
(1, 1, 1),
(1, 2, 2),
(1, 3, 3),
(1, 4, 4);

-- 「進撃の巨人」のシーズン1〜4を確認して追加（シーズン1がまだない場合）
-- シーズン1が存在しないと仮定して、全シーズンを追加
INSERT INTO seasons (channel_id, season_number, season_id) VALUES
(2, 1, 5),
(2, 2, 6),
(2, 3, 7),
(2, 4, 8);

* エピソードデータの追加
INSERT INTO episodes (channel_id, episode_number, episode_detail, video_time, release_date, airing_time, watching_number, episode_id) VALUES (1, 1, '鬼滅の刃 第1話 詳細', '00:24:00', '2020-04-06', '20:00:00', 100000, 1);
INSERT INTO episodes (channel_id, episode_number, episode_detail, video_time, release_date, airing_time, watching_number, episode_id) VALUES (1, 2, '鬼滅の刃 第2話 詳細', '00:24:00', '2020-04-06', '20:30:00', 200000, 2);
INSERT INTO episodes (channel_id, episode_number, episode_detail, video_time, release_date, airing_time, watching_number, episode_id) VALUES (1, 3, '鬼滅の刃 第3話 詳細', '00:24:00', '2020-04-06', '21:00:00', 300000, 3);
INSERT INTO episodes (channel_id, episode_number, episode_detail, video_time, release_date, airing_time, watching_number, episode_id) VALUES (1, 4, '鬼滅の刃 第4話 詳細', '00:24:00', '2020-04-06', '21:30:00', 400000, 4);
INSERT INTO episodes (channel_id, episode_number, episode_detail, video_time, release_date, airing_time, watching_number, episode_id) VALUES (1, 5, '鬼滅の刃 第5話 詳細', '00:24:00', '2020-04-06', '22:00:00', 500000, 5);
INSERT INTO episodes (channel_id, episode_number, episode_detail, video_time, release_date, airing_time, watching_number, episode_id) VALUES (1, 6, '鬼滅の刃 第6話 詳細', '00:24:00', '2020-04-06', '22:30:00', 600000, 6);
INSERT INTO episodes (channel_id, episode_number, episode_detail, video_time, release_date, airing_time, watching_number, episode_id) VALUES (1, 7, '鬼滅の刃 第7話 詳細', '00:24:00', '2020-04-06', '23:00:00', 700000, 7);
INSERT INTO episodes (channel_id, episode_number, episode_detail, video_time, release_date, airing_time, watching_number, episode_id) VALUES (1, 8, '鬼滅の刃 第8話 詳細', '00:24:00', '2020-04-06', '23:30:00', 800000, 8);
INSERT INTO episodes (channel_id, episode_number, episode_detail, video_time, release_date, airing_time, watching_number, episode_id) VALUES (1, 9, '鬼滅の刃 第9話 詳細', '00:24:00', '2020-04-06', '00:00:00', 900000, 9);
INSERT INTO episodes (channel_id, episode_number, episode_detail, video_time, release_date, airing_time, watching_number, episode_id) VALUES (1, 10, '鬼滅の刃 第10話 詳細', '00:24:00', '2020-04-06', '00:30:00', 1000000, 10);
INSERT INTO episodes (channel_id, episode_number, episode_detail, video_time, release_date, airing_time, watching_number, episode_id) VALUES (1, 1, '進撃の巨人 第1話 詳細', '00:24:00', '2020-04-07', '20:00:00', 100000, 11);
INSERT INTO episodes (channel_id, episode_number, episode_detail, video_time, release_date, airing_time, watching_number, episode_id) VALUES (1, 2, '進撃の巨人 第2話 詳細', '00:24:00', '2020-04-07', '20:30:00', 200000, 12);
INSERT INTO episodes (channel_id, episode_number, episode_detail, video_time, release_date, airing_time, watching_number, episode_id) VALUES (1, 3, '進撃の巨人 第3話 詳細', '00:24:00', '2020-04-07', '21:00:00', 300000, 13);
INSERT INTO episodes (channel_id, episode_number, episode_detail, video_time, release_date, airing_time, watching_number, episode_id) VALUES (1, 4, '進撃の巨人 第4話 詳細', '00:24:00', '2020-04-07', '21:30:00', 400000, 14);
INSERT INTO episodes (channel_id, episode_number, episode_detail, video_time, release_date, airing_time, watching_number, episode_id) VALUES (1, 5, '進撃の巨人 第5話 詳細', '00:24:00', '2020-04-07', '22:00:00', 500000, 15);
INSERT INTO episodes (channel_id, episode_number, episode_detail, video_time, release_date, airing_time, watching_number, episode_id) VALUES (1, 6, '進撃の巨人 第6話 詳細', '00:24:00', '2020-04-07', '22:30:00', 600000, 16);
INSERT INTO episodes (channel_id, episode_number, episode_detail, video_time, release_date, airing_time, watching_number, episode_id) VALUES (1, 7, '進撃の巨人 第7話 詳細', '00:24:00', '2020-04-07', '23:00:00', 700000, 17);
INSERT INTO episodes (channel_id, episode_number, episode_detail, video_time, release_date, airing_time, watching_number, episode_id) VALUES (1, 8, '進撃の巨人 第8話 詳細', '00:24:00', '2020-04-07', '23:30:00', 800000, 18);
INSERT INTO episodes (channel_id, episode_number, episode_detail, video_time, release_date, airing_time, watching_number, episode_id) VALUES (1, 9, '進撃の巨人 第9話 詳細', '00:24:00', '2020-04-07', '00:00:00', 900000, 19);
INSERT INTO episodes (channel_id, episode_number, episode_detail, video_time, release_date, airing_time, watching_number, episode_id) VALUES (1, 10, '進撃の巨人 第10話 詳細', '00:24:00', '2020-04-07', '00:30:00', 1000000, 20);
INSERT INTO episodes (channel_id, episode_number, episode_detail, video_time, release_date, watching_number, episode_id) VALUES (1, 1, 'ドラマの新シリーズ開始', '00:30:00', '2020-04-06', 50000, 21);
INSERT INTO episodes (channel_id, episode_number, episode_detail, video_time, release_date, watching_number, episode_id) VALUES (1, 2, 'ドラマの感動エピソード', '00:30:00', '2020-04-06', 100000, 22);
INSERT INTO episodes (channel_id, episode_number, episode_detail, video_time, release_date, watching_number, episode_id) VALUES (1, 3, 'ドラマのクリスマス特別編', '00:30:00', '2020-04-06', 150000, 23);
INSERT INTO episodes (channel_id, episode_number, episode_detail, video_time, release_date, watching_number, episode_id) VALUES (1, 4, 'ドラマの新年スペシャル', '00:30:00', '2020-04-06', 200000, 24);
INSERT INTO episodes (channel_id, episode_number, episode_detail, video_time, release_date, watching_number, episode_id) VALUES (1, 5, 'ドラマのバレンタインデー特集', '00:30:00', '2020-04-06', 250000, 25);
INSERT INTO episodes (channel_id, episode_number, episode_detail, video_time, release_date, watching_number, episode_id) VALUES (1, 6, 'ドラマの卒業シーズン', '00:30:00', '2020-04-06', 300000, 26);
INSERT INTO episodes (channel_id, episode_number, episode_detail, video_time, release_date, watching_number, episode_id) VALUES (1, 7, 'ドラマの夏休みスペシャル', '00:30:00', '2020-04-06', 350000, 27);
INSERT INTO episodes (channel_id, episode_number, episode_detail, video_time, release_date, watching_number, episode_id) VALUES (1, 8, 'ドラマの秋の新シーズン', '00:30:00', '2020-04-06', 400000, 28);
INSERT INTO episodes (channel_id, episode_number, episode_detail, video_time, release_date, watching_number, episode_id) VALUES (1, 9, 'ドラマのハロウィン特別編', '00:30:00', '2020-04-06', 450000, 29);
INSERT INTO episodes (channel_id, episode_number, episode_detail, video_time, release_date, watching_number, episode_id) VALUES (1, 10, 'ドラマの感謝祭スペシャル', '00:30:00', '2020-04-06', 500000, 30);
INSERT INTO episodes (channel_id, episode_number, episode_detail, video_time, release_date, watching_number, episode_id) VALUES (3, 1, 'サッカーワールドカップ予選ハイライト', '01:00:00', '2020-04-06', 100000, 31);
INSERT INTO episodes (channel_id, episode_number, episode_detail, video_time, release_date, watching_number, episode_id) VALUES (3, 2, 'オリンピック特集：過去の名シーン', '01:00:00', '2020-04-06', 200000, 32);
INSERT INTO episodes (channel_id, episode_number, episode_detail, video_time, release_date, watching_number, episode_id) VALUES (3, 3, 'マラソン大会2020ハイライト', '01:00:00', '2020-04-06', 300000, 33);
INSERT INTO episodes (channel_id, episode_number, episode_detail, video_time, release_date, watching_number, episode_id) VALUES (3, 4, 'プロ野球：春のセンバツ特集', '01:00:00', '2020-04-06', 400000, 34);
INSERT INTO episodes (channel_id, episode_number, episode_detail, video_time, release_date, watching_number, episode_id) VALUES (3, 5, 'サッカー：国内リーグ戦ハイライト', '01:00:00', '2020-04-06', 500000, 35);
INSERT INTO episodes (channel_id, episode_number, episode_detail, video_time, release_date, watching_number, episode_id) VALUES (3, 6, 'バスケットボール：NBAの歴史', '01:00:00', '2020-04-06', 600000, 36);
INSERT INTO episodes (channel_id, episode_number, episode_detail, video_time, release_date, watching_number, episode_id) VALUES (3, 7, 'テニス：四大大会特集', '01:00:00', '2020-04-06', 700000, 37);
INSERT INTO episodes (channel_id, episode_number, episode_detail, video_time, release_date, watching_number, episode_id) VALUES (3, 8, 'フィギュアスケート：世界選手権ハイライト', '01:00:00', '2020-04-06', 800000, 38);
INSERT INTO episodes (channel_id, episode_number, episode_detail, video_time, release_date, watching_number, episode_id) VALUES (3, 9, 'ラグビーワールドカップ：名試合振り返り', '01:00:00', '2020-04-06', 900000, 39);
INSERT INTO episodes (channel_id, episode_number, episode_detail, video_time, release_date, watching_number, episode_id) VALUES (3, 10, 'ボクシング：世界タイトルマッチ特集', '01:00:00', '2020-04-06', 1000000, 40);
INSERT INTO episodes (channel_id, episode_number, episode_detail, video_time, release_date, watching_number, episode_id) VALUES (4, 1, 'かわいい猫の日常', '00:30:00', '2020-04-06', 20000, 41);
INSERT INTO episodes (channel_id, episode_number, episode_detail, video_time, release_date, watching_number, episode_id) VALUES (4, 2, '犬のしつけ方ガイド', '00:30:00', '2020-04-06', 40000, 42);
INSERT INTO episodes (channel_id, episode_number, episode_detail, video_time, release_date, watching_number, episode_id) VALUES (4, 3, '小動物との暮らし方', '00:30:00', '2020-04-06', 60000, 43);
INSERT INTO episodes (channel_id, episode_number, episode_detail, video_time, release_date, watching_number, episode_id) VALUES (4, 4, 'ペットと旅行する際の注意点', '00:30:00', '2020-04-06', 80000, 44);
INSERT INTO episodes (channel_id, episode_number, episode_detail, video_time, release_date, watching_number, episode_id) VALUES (4, 5, 'ペットの健康管理', '00:30:00', '2020-04-06', 100000, 45);
INSERT INTO episodes (channel_id, episode_number, episode_detail, video_time, release_date, watching_number, episode_id) VALUES (4, 6, 'ペットの手作りごはんレシピ', '00:30:00', '2020-04-06', 120000, 46);
INSERT INTO episodes (channel_id, episode_number, episode_detail, video_time, release_date, watching_number, episode_id) VALUES (4, 7, '動物病院の選び方', '00:30:00', '2020-04-06', 140000, 47);
INSERT INTO episodes (channel_id, episode_number, episode_detail, video_time, release_date, watching_number, episode_id) VALUES (4, 8, 'ペットの保険について', '00:30:00', '2020-04-06', 160000, 48);
INSERT INTO episodes (channel_id, episode_number, episode_detail, video_time, release_date, watching_number, episode_id) VALUES (4, 9, '迷子のペットを探す方法', '00:30:00', '2020-04-06', 180000, 49);
INSERT INTO episodes (channel_id, episode_number, episode_detail, video_time, release_date, watching_number, episode_id) VALUES (4, 10, 'ペットのためのエクササイズ', '00:30:00', '2020-04-06', 200000, 50);


--ジャンルを追加
INSERT INTO genres (channel_id, genre_name) VALUES
    -> (1, 'アニメ'),
    -> (1, 'ドラマ'),
    -> (3, 'スポーツ'),
    -> (4, 'ペット');

--テーブル：airing_timeにデータを追加
INSERT INTO airing_time (channel_id, episode_number, broadcasting_start_time, broadcasting_end_time, airing_time_id, airing_date) VALUES (1, 1, '18:00:00', '18:30:00', 1, '2020-04-13');
INSERT INTO airing_time (channel_id, episode_number, broadcasting_start_time, broadcasting_end_time, airing_time_id, airing_date) VALUES (1, 2, '19:00:00', '19:30:00', 2, '2020-04-14');
INSERT INTO airing_time (channel_id, episode_number, broadcasting_start_time, broadcasting_end_time, airing_time_id, airing_date) VALUES (1, 3, '20:00:00', '20:30:00', 3, '2020-04-15');
INSERT INTO airing_time (channel_id, episode_number, broadcasting_start_time, broadcasting_end_time, airing_time_id, airing_date) VALUES (1, 4, '21:00:00', '21:30:00', 4, '2020-04-16');
INSERT INTO airing_time (channel_id, episode_number, broadcasting_start_time, broadcasting_end_time, airing_time_id, airing_date) VALUES (1, 5, '22:00:00', '22:30:00', 5, '2020-04-17');
INSERT INTO airing_time (channel_id, episode_number, broadcasting_start_time, broadcasting_end_time, airing_time_id, airing_date) VALUES (1, 6, '23:00:00', '23:30:00', 6, '2020-04-18');
INSERT INTO airing_time (channel_id, episode_number, broadcasting_start_time, broadcasting_end_time, airing_time_id, airing_date) VALUES (1, 7, '18:00:00', '18:30:00', 7, '2020-04-19');
INSERT INTO airing_time (channel_id, episode_number, broadcasting_start_time, broadcasting_end_time, airing_time_id, airing_date) VALUES (2, 1, '19:00:00', '19:30:00', 11, '2020-04-13');
INSERT INTO airing_time (channel_id, episode_number, broadcasting_start_time, broadcasting_end_time, airing_time_id, airing_date) VALUES (2, 2, '20:00:00', '20:30:00', 12, '2020-04-14');
INSERT INTO airing_time (channel_id, episode_number, broadcasting_start_time, broadcasting_end_time, airing_time_id, airing_date) VALUES (2, 3, '21:00:00', '21:30:00', 13, '2020-04-15');
INSERT INTO airing_time (channel_id, episode_number, broadcasting_start_time, broadcasting_end_time, airing_time_id, airing_date) VALUES (2, 4, '22:00:00', '22:30:00', 14, '2020-04-16');
INSERT INTO airing_time (channel_id, episode_number, broadcasting_start_time, broadcasting_end_time, airing_time_id, airing_date) VALUES (2, 5, '23:00:00', '23:30:00', 15, '2020-04-17');
INSERT INTO airing_time (channel_id, episode_number, broadcasting_start_time, broadcasting_end_time, airing_time_id, airing_date) VALUES (2, 6, '18:00:00', '18:30:00', 16, '2020-04-18');
INSERT INTO airing_time (channel_id, episode_number, broadcasting_start_time, broadcasting_end_time, airing_time_id, airing_date) VALUES (2, 7, '19:00:00', '19:30:00', 17, '2020-04-19');
INSERT INTO airing_time (channel_id, episode_number, broadcasting_start_time, broadcasting_end_time, airing_time_id, airing_date) VALUES (2, 8, '20:00:00', '20:30:00', 18, '2020-04-13');
INSERT INTO airing_time (channel_id, episode_number, broadcasting_start_time, broadcasting_end_time, airing_time_id, airing_date) VALUES (2, 9, '21:00:00', '21:30:00', 19, '2020-04-14');
INSERT INTO airing_time (channel_id, episode_number, broadcasting_start_time, broadcasting_end_time, airing_time_id, airing_date) VALUES (2, 10, '22:00:00', '22:30:00', 20, '2020-04-15');
INSERT INTO airing_time (channel_id, episode_number, broadcasting_start_time, broadcasting_end_time, airing_time_id, airing_date) VALUES (3, 1, '23:00:00', '23:30:00', 21, '2020-04-16');
INSERT INTO airing_time (channel_id, episode_number, broadcasting_start_time, broadcasting_end_time, airing_time_id, airing_date) VALUES (3, 2, '18:00:00', '18:30:00', 22, '2020-04-17');
INSERT INTO airing_time (channel_id, episode_number, broadcasting_start_time, broadcasting_end_time, airing_time_id, airing_date) VALUES (3, 3, '19:00:00', '19:30:00', 23, '2020-04-18');
INSERT INTO airing_time (channel_id, episode_number, broadcasting_start_time, broadcasting_end_time, airing_time_id, airing_date) VALUES (3, 4, '20:00:00', '20:30:00', 24, '2020-04-19');
INSERT INTO airing_time (channel_id, episode_number, broadcasting_start_time, broadcasting_end_time, airing_time_id, airing_date) VALUES (3, 5, '21:00:00', '21:30:00', 25, '2020-04-13');
INSERT INTO airing_time (channel_id, episode_number, broadcasting_start_time, broadcasting_end_time, airing_time_id, airing_date) VALUES (3, 6, '22:00:00', '22:30:00', 26, '2020-04-14');
INSERT INTO airing_time (channel_id, episode_number, broadcasting_start_time, broadcasting_end_time, airing_time_id, airing_date) VALUES (3, 7, '23:00:00', '23:30:00', 27, '2020-04-15');
INSERT INTO airing_time (channel_id, episode_number, broadcasting_start_time, broadcasting_end_time, airing_time_id, airing_date) VALUES (3, 8, '18:00:00', '18:30:00', 28, '2020-04-16');
INSERT INTO airing_time (channel_id, episode_number, broadcasting_start_time, broadcasting_end_time, airing_time_id, airing_date) VALUES (3, 9, '19:00:00', '19:30:00', 29, '2020-04-17');
INSERT INTO airing_time (channel_id, episode_number, broadcasting_start_time, broadcasting_end_time, airing_time_id, airing_date) VALUES (3, 10, '20:00:00', '20:30:00', 30, '2020-04-18');
INSERT INTO airing_time (channel_id, episode_number, broadcasting_start_time, broadcasting_end_time, airing_time_id, airing_date) VALUES (4, 1, '21:00:00', '21:30:00', 31, '2020-04-19');
INSERT INTO airing_time (channel_id, episode_number, broadcasting_start_time, broadcasting_end_time, airing_time_id, airing_date) VALUES (4, 2, '22:00:00', '22:30:00', 32, '2020-04-13');
INSERT INTO airing_time (channel_id, episode_number, broadcasting_start_time, broadcasting_end_time, airing_time_id, airing_date) VALUES (4, 3, '23:00:00', '23:30:00', 33, '2020-04-14');
INSERT INTO airing_time (channel_id, episode_number, broadcasting_start_time, broadcasting_end_time, airing_time_id, airing_date) VALUES (4, 4, '18:00:00', '18:30:00', 34, '2020-04-15');
INSERT INTO airing_time (channel_id, episode_number, broadcasting_start_time, broadcasting_end_time, airing_time_id, airing_date) VALUES (4, 5, '19:00:00', '19:30:00', 35, '2020-04-16');
INSERT INTO airing_time (channel_id, episode_number, broadcasting_start_time, broadcasting_end_time, airing_time_id, airing_date) VALUES (4, 6, '20:00:00', '20:30:00', 36, '2020-04-17');
INSERT INTO airing_time (channel_id, episode_number, broadcasting_start_time, broadcasting_end_time, airing_time_id, airing_date) VALUES (4, 7, '21:00:00', '21:30:00', 37, '2020-04-18');
INSERT INTO airing_time (channel_id, episode_number, broadcasting_start_time, broadcasting_end_time, airing_time_id, airing_date) VALUES (4, 8, '22:00:00', '22:30:00', 38, '2020-04-19');
INSERT INTO airing_time (channel_id, episode_number, broadcasting_start_time, broadcasting_end_time, airing_time_id, airing_date) VALUES (4, 9, '23:00:00', '23:30:00', 39, '2020-04-13');
INSERT INTO airing_time (channel_id, episode_number, broadcasting_start_time, broadcasting_end_time, airing_time_id, airing_date) VALUES (4, 10, '18:00:00', '18:30:00', 40, '2020-04-14');

--テーブルの追加
CREATE TABLE episode_titles (
    episode_title_id BIGINT(20) AUTO_INCREMENT PRIMARY KEY,
    episode_id BIGINT(20) NOT NULL,
    episode_title VARCHAR(255),
    FOREIGN KEY (episode_id) REFERENCES episodes(episode_id)
);
--データの追加
INSERT INTO episode_titles (episode_id, episode_title)
SELECT
    e.episode_id,
    CONCAT(c.channel, ' 第', e.episode_number, '話') AS episode_title
FROM
    episodes e
JOIN
    channels c ON e.channel_id = c.channel_id;

--カラムの追加
ALTER TABLE episodes
ADD COLUMN season_id BIGINT(20),
ADD CONSTRAINT fk_episodes_seasons_season_id FOREIGN KEY (season_id) REFERENCES seasons(season_id);

--データの追加
-- エピソードID 21から30までをシーズン1に割り当てる例
UPDATE episodes
SET season_id = 1
WHERE episode_id BETWEEN 21 AND 30;

-- 必要に応じて、異なるエピソード範囲に対して異なるシーズンIDを割り当てる
-- 例: エピソードID 31から40をシーズン2に割り当てる
UPDATE episodes
SET season_id = 2
WHERE episode_id BETWEEN 31 AND 40;

サンプルデータはご自身で作成ください（ChatGPTを利用すると比較的簡単に生成できます）

手順のドキュメントは、他の人が見た時にその手順通りに実施すればテーブル作成及びサンプルデータ格納が行えるように記載してください。
