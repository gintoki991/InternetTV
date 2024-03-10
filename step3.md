# Step3

* 以下のデータを抽出するクエリを書いてください。

1. よく見られているエピソードを知りたいです。エピソード視聴数トップ3のエピソードタイトルと視聴数を取得してください
SELECT
    et.episode_title AS "エピソードタイトル",
    SUM(e.watching_number) AS "合計視聴数"
FROM
    episodes e
JOIN
    episode_titles et ON e.episode_id = et.episode_id
GROUP BY
    et.episode_title
ORDER BY
    SUM(e.watching_number) DESC
LIMIT 3;

2. よく見られているエピソードの番組情報やシーズン情報も合わせて知りたいです。エピソード視聴数トップ3の番組タイトル、シーズン数、エピソード数、エピソードタイトル、視聴数を取得してください
SELECT
    t.title AS "番組タイトル",
    e.episode_number AS "エピソード数",
    et.episode_title AS "エピソードタイトル",
    e.watching_number AS "視聴数"
FROM
    episodes e
JOIN
    episode_titles et ON e.episode_id = et.episode_id
JOIN
    titles t ON e.title_id = t.title_id
ORDER BY
    e.watching_number DESC
LIMIT 3;

3. 本日の番組表を表示するために、本日、どのチャンネルの、何時から、何の番組が放送されるのかを知りたいです。本日放送される全ての番組に対して、チャンネル名、放送開始時刻(日付+時間)、放送終了時刻、シーズン数、エピソード数、エピソードタイトル、エピソード詳細を取得してください。なお、番組の開始時刻が本日のものを本日方法される番組とみなすものとします
SELECT
    c.channel AS "チャンネル名",
    CONCAT(at.airing_date, ' ', at.broadcasting_start_time) AS "放送開始時刻",
    CONCAT(at.airing_date, ' ', at.broadcasting_end_time) AS "放送終了時刻",
    s.season_number AS "シーズン数",
    e.episode_number AS "エピソード数",
    et.episode_title AS "エピソードタイトル",
    e.episode_detail AS "エピソード詳細"
FROM
    airing_time at
JOIN
    episodes e ON at.channel_id = e.channel_id AND at.episode_number = e.episode_number
JOIN
    episode_titles et ON e.episode_id = et.episode_id
JOIN
    channels c ON e.channel_id = c.channel_id
JOIN
    seasons s ON e.season_id = s.season_id
WHERE
    at.airing_date = '2020-04-16';

4. ドラマというチャンネルがあったとして、ドラマのチャンネルの番組表を表示するために、本日から一週間分、何日の何時から何の番組が放送されるのかを知りたいです。ドラマのチャンネルに対して、放送開始時刻、放送終了時刻、シーズン数、エピソード数、エピソードタイトル、エピソード詳細を本日から一週間分取得してください
SELECT
    c.channel AS "チャンネル名",
    CONCAT(at.airing_date, ' ', at.broadcasting_start_time) AS "放送開始時刻",
    CONCAT(at.airing_date, ' ', at.broadcasting_end_time) AS "放送終了時刻",
    s.season_number AS "シーズン数",
    e.episode_number AS "エピソード数",
    et.episode_title AS "エピソードタイトル",
    e.episode_detail AS "エピソード詳細"
FROM
    airing_time at
JOIN
    episodes e ON at.channel_id = e.channel_id AND at.episode_number = e.episode_number
JOIN
    episode_titles et ON e.episode_id = et.episode_id
JOIN
    channels c ON e.channel_id = c.channel_id
JOIN
    seasons s ON e.season_id = s.season_id
WHERE
    c.channel = 'ドラマ'
    AND at.airing_date BETWEEN '2020-04-13' AND '2020-04-13' + INTERVAL 7 DAY
ORDER BY
    at.airing_date, at.broadcasting_start_time;

5. (advanced) 直近一週間で最も見られた番組が知りたいです。直近一週間に放送された番組の中で、エピソード視聴数合計トップ2の番組に対して、番組タイトル、視聴数を取得してください
6. (advanced) ジャンルごとの番組の視聴数ランキングを知りたいです。番組の視聴数ランキングはエピソードの平均視聴数ランキングとします。ジャンルごとに視聴数トップの番組に対して、ジャンル名、番組タイトル、エピソード平均視聴数を取得してください。
