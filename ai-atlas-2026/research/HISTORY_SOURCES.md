# История AI: источники и датировка

Дополнение после [проверки внешнего исследования](deep-research-2026-10-21/EXTERNAL_REVIEW.md): в историю добавлены правила маркировки CAC с датой применения 01.09.2025, передача MCP в AAIF 09.12.2025, EnterpriseOps-Gym и Ropedia W0. Первичные ссылки сохранены в `history.json` и обеих HTML-главах. Пояснения 2026 года включают ограничения оценки агентов и работы с недоверенными данными. Проценты отдельных бенчмарков не выдаются за общий уровень надёжности всех агентов.

После [второй внешней сверки](deep-research-2026-10-21/EXTERNAL_REVIEW_2.md) добавлены scaling laws (23.01.2020), Chinchilla (29.03.2022), CooperBench (первая подача 19.01.2026, прочитана v2 от 26.01) и ссылка на Auto Benchmark Audit v2. Проценты частных экспериментов не используются как общий штраф за делегирование.

Проверено 21 октября 2026 года. История выборочная: шесть ранних этапов и каждый календарный год 2017–2026. Названия этапов и выводы редакционные. Список не претендует на полноту истории AI.

## Границы и проверка

- 1950: статья Тьюринга; 1955: предложение семинара; 1956: сам Дартмутский семинар. Это разные даты.
- Ранние эпохи: обзор Stanford AI100 — исследовательский исторический синтез. Для отдельных технических вех использованы оригинальные публикации и история разработчиков.
- Датировка статьи об обратном распространении ошибки 1986 года подтверждена описанием оригинальной публикации; доступен авторский PDF. Основной URL Nature не открылся через веб-инструмент; указан доступный PDF автора.
- Deep Blue использовал поиск и шахматные эвристики. Его победа не приписывается современному глубокому обучению.
- Нейронные языковые модели появились раньше 2017 года. Transformer отмечен как граница подробной годовой шкалы, а не рождение всего NLP или AI.
- GPT-2: анонс 14 февраля 2019 и публикация полных весов 5 ноября 2019 разделены.
- RAG: первая версия статьи 22 мая 2020; более поздние ревизии не меняют год вехи.
- AlphaFold: результат CASP14 — 2020; код, научная публикация и база структур — 2021. AlphaFold не назван LLM.
- Llama 2: открытые веса и собственная лицензия. Термин «без ограничений» не используется.
- GPT-4o: анонс и начало доступа не приравнены к немедленному доступу ко всем аудиовозможностям. o1 отмечен как preview.
- MCP: исходный анонс 25 ноября 2024. AlphaEvolve: первый анонс 14 мая 2025. Более позднее применение не переносит дату появления.
- 2026: срез на 21 октября, без прогноза за остаток года. Cowork и ГигаЧат Бизнес опираются на проверенную подборку проекта; Gemini Robotics 2 — на публикацию DeepMind от 30 июля 2026.
- Заявления разработчиков о возможностях не являются независимой проверкой всех систем. Оговорки об автономности, стадиях доступа и пересечении подходов сохранены в интерфейсе.

## Ранние этапы

### 1950–1956 · Можно ли описать интеллект?

1956 — условная точка рождения научной области. Идеи вычислений, обучения и нейросетей появились раньше.

- [Тьюринг · Computing Machinery and Intelligence · 1950](https://doi.org/10.1093/mind/LIX.236.433)
- [McCarthy et al. · предложение от 31 августа 1955](https://www-formal.stanford.edu/jmc/history/dartmouth/dartmouth.html)
- [Dartmouth · история семинара 1956](https://ai.dartmouth.edu/our-story)

### 1960–1980-е · Знания записывают в правила

Развитие шло волнами: успехи в узких задачах чередовались с разочарованием и сокращением финансирования.

- [Stanford AI100 · исторический обзор и экспертные системы](https://ai100.stanford.edu/2016-report/appendix-i-short-history-ai)

### 1986–1997 · Обучение и вычисления набирают силу

Deep Blue — пример силы поиска и шахматных эвристик; его победа не была победой LLM или современной глубокой нейросети.

- [Авторы · Learning representations by back-propagating errors · 1986](https://www.cs.toronto.edu/~hinton/absps/naturebp.pdf)
- [IBM · Deep Blue · матч 1997](https://www.ibm.com/history/deep-blue)

### 2003 · Язык становится пространством чисел

Языковые модели существовали до Transformer и до ChatGPT. Это одна из опорных работ, а не дата изобретения всех языковых моделей.

- [Bengio et al. · A Neural Probabilistic Language Model · JMLR 2003](https://jmlr.org/papers/v3/bengio03a.html)

### 2012 · Глубокое обучение показывает масштаб

Это важная веха компьютерного зрения. Глубокие сети и GPU применялись и раньше; 2012-й не является годом рождения нейросетей.

- [Krizhevsky et al. · ImageNet Classification · NeurIPS 2012](https://papers.nips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html)

### 2016 · Система учится выбирать действия

Это специализированная система для го. Обучение с подкреплением и AI-агенты существовали задолго до нынешних LLM-агентов.

- [Google DeepMind · AlphaGo](https://deepmind.google/research/alphago/)

## По годам

### 2017 · Архитектура

Attention существовал раньше. Новизна Transformer — архитектура на основе внимания без рекуррентных и свёрточных слоёв в исходной модели.

- **2017-06-12 · Attention Is All You Need.** [Авторы · оригинальная статья](https://arxiv.org/abs/1706.03762)

### 2018 · Предобучение

Предобучение и перенос знаний появились раньше. GPT и BERT стали опорными примерами этого подхода для Transformer; BERT не был диалоговым генератором.

- **2018-06-11 · GPT: предобучение и дообучение.** [OpenAI · GPT](https://openai.com/index/language-unsupervised/)
- **2018-11-02 · Открытый выпуск BERT.** [Google Research · BERT](https://research.google/blog/open-sourcing-bert-state-of-the-art-pre-training-for-natural-language-processing/)

### 2019 · Генерация

Связный текст не гарантирует достоверности. Полную модель GPT-2 выпустили в ноябре, после поэтапного раскрытия в течение года.

- **2019-02-14 · GPT-2 и поэтапный выпуск.** [OpenAI · анонс GPT-2](https://openai.com/index/better-language-models/)
- **2019-11-05 · Открыта версия 1.5B.** [OpenAI · GPT-2 1.5B release](https://openai.com/index/gpt-2-1-5b-release/)

### 2020 · Промпт и знания

Few-shot работает с разным качеством на разных задачах. RAG — исследовательская веха 2020 года; поиск в генеративных системах и раньше имел предшественников.

- **2020-05-22 · Retrieval-Augmented Generation.** [Авторы · статья о RAG](https://arxiv.org/abs/2005.11401)
- **2020-05-28 · GPT-3: few-shot learning.** [Brown et al. · GPT-3](https://arxiv.org/abs/2005.14165)

### 2021 · Медиа и наука

AlphaFold не является LLM: это параллельная ветвь AI. Его прорыв на CASP14 относится к 2020 году; здесь отмечен выпуск научных ресурсов в 2021-м.

- **2021-01-05 · CLIP и DALL·E.** [OpenAI · CLIP](https://openai.com/index/clip/)
  - [OpenAI · DALL·E](https://openai.com/index/dall-e/)
- **2021-07-22 · AlphaFold и база структур белков.** [Google DeepMind · AlphaFold DB](https://deepmind.google/blog/enabling-high-accuracy-protein-structure-prediction-at-the-proteome-scale/)

### 2022 · Диалог

RLHF не изобретён в 2022-м. Удобный диалог не устраняет выдуманные факты; ChatGPT стартовал как research preview.

- **2022-01-27 · Обучение следовать намерению человека.** [OpenAI · InstructGPT](https://openai.com/index/instruction-following/)
- **2022-11-30 · Запущен ChatGPT.** [OpenAI · Introducing ChatGPT](https://openai.com/index/chatgpt/)

### 2023 · Приложения

Llama 2 распространялась по собственной лицензии с условиями — «открытые веса» не означают отсутствие ограничений. Вызов функции исполняет приложение, а не сама модель.

- **2023-03-14 · GPT-4.** [OpenAI · GPT-4](https://openai.com/index/gpt-4-research/)
- **2023-06-13 · Function calling.** [OpenAI · function calling](https://openai.com/index/function-calling-and-other-api-updates/)
- **2023-07-18 · Llama 2.** [Meta · Llama 2](https://about.fb.com/news/2023/07/llama-2/)

### 2024 · Рассуждение

Новые голосовые возможности GPT-4o открывались поэтапно; o1 стартовал в preview. MCP появился в ноябре 2024-го, хотя его распространение продолжилось позже.

- **2024-05-13 · GPT-4o.** [OpenAI · GPT-4o](https://openai.com/index/hello-gpt-4o/)
- **2024-09-12 · o1: вычисления перед ответом.** [OpenAI · learning to reason](https://openai.com/index/learning-to-reason-with-llms/)
- **2024-11-25 · Model Context Protocol.** [Anthropic · MCP](https://www.anthropic.com/news/model-context-protocol)

### 2025 · Агенты

AI-агенты не появились впервые в 2025 году. Здесь отмечена новая волна LLM-инструментов; автономность зависит от конкретной задачи и условий проверки.

- **2025-01-20 · DeepSeek-R1.** [DeepSeek · выпуск R1](https://api-docs.deepseek.com/news/news250120)
  - [DeepSeek · репозиторий и лицензии](https://github.com/deepseek-ai/DeepSeek-R1)
- **2025-02-24 · Claude Code.** [Anthropic · Claude Code](https://www.anthropic.com/news/claude-3-7-sonnet)
- **2025-05-14 · AlphaEvolve.** [Google DeepMind · AlphaEvolve](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/)

### 2026 · Экосистемы

Промежуточный срез на 21 октября. Это расширение прежних направлений; анонсы и демонстрации роботов не означают массового внедрения или универсальной автономности.

- **2026-01-12 · Cowork: работа с файлами.** [Anthropic · release notes](https://support.claude.com/en/articles/12138966-release-notes)
- **2026-03-03 · ГигаЧат Бизнес.** [СберБизнес Live · ГигаЧат Бизнес](https://sberbusiness.live/news/sber-predostavil-biznesu-dostup-k-korporativnoi-platforme-gigachat-biznes)
- **2026-07-30 · Gemini Robotics 2.** [Google DeepMind · Gemini Robotics 2](https://deepmind.google/blog/gemini-robotics-2-brings-whole-body-intelligence-to-robots/)

## Воспроизводимость

Данные: `history.json`; автономная страница: `dist/history.html`. Сборка: `python3 ai-atlas-2026/research/build_history.py`. Данные в `script#history-data` совпадают с исходным JSON. Исторические вехи не входят в 32 события основной подборки 2026 года.

## Пояснения механизмов · дополнение 21 октября 2026

Для всех десяти лет доступны краткие пояснения механизмов и ограничений. Они открываются по кнопке «Как это работает». В исторической главе 50 уникальных источников.

- [BERT · оригинальная статья](https://arxiv.org/abs/1810.04805): masked language modeling, двунаправленный контекст и fine-tuning. Первая версия 11 октября 2018, открытый выпуск отмечен отдельно 2 ноября.
- [DeepSeek-R1 · технический отчёт](https://arxiv.org/abs/2501.12948): обучение с подкреплением и проверяемые сигналы. Первый preprint 22 января 2025; дата релиза модели 20 января остаётся отдельным событием.
- [Zhang et al. · harness-aware evaluation](https://arxiv.org/abs/2605.23950): position paper от 7 мая 2026. Его тезис и ограниченные эксперименты не обобщаются на любую модель и задачу; универсальное преимущество harness не утверждается.

Остальные технические ссылки повторно используют источники карточек. Архитектура, обучение, инференс и среда исполнения разделены; корректный формат вызова функции не приравнен к корректности действия.
