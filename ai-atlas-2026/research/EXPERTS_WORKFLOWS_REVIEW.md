# MoE, Kimi, агентная разработка и Карпати

Проверка и интеграция: 21 октября 2026. Сценарий: 25 экранов, 25 мин 50 с текста, около 27 минут с переходами. Каталог: 41 событие, 14 организаций/авторов и экосистем.

## Что вошло

- MoE: условная схема маршрутизации, DeepSeek-V3 (671B / 37B active), Kimi K2 (1T / 32B active). Это параметры на токен, а не независимые агенты. Специализация возникает при обучении.
- Вклад DeepSeek: fine-grained/shared experts, сочетание MoE с MLA, FP8 и инженерными оптимизациями. Предшествующая sparse-MoE работа 2017 года указана отдельно.
- Стоимость V3: 2,788 млн H800 GPU-часов, $5,576 млн при условной цене $2/час. В отчёте исключены предшествующие исследования и абляции. Кластер — 2048 H800. Не представлять как весь бюджет разработки или стоимость R1.
- Kimi K2.5 и Agent Swarm: дата выпуска 27 января подтверждена официальной справкой Kimi; до 100 подагентов / 1500 tool calls — утверждение разработчика о конфигурации. Preview и пределы применения подписаны.
- Skills / MCP / агенты: процедура / интерфейс инструментов / исполнители задач. Пример ролей редакционный; skill не меняет веса.
- SDD: GitHub Spec Kit (02.09.2025); Kiro Design-first/Bugfix (18.02.2026). Пять шагов и пример CSV — иллюстрация, а не единый обязательный стандарт.
- Карпати: Software 2.0, Software 3.0, vibe coding → agentic engineering. Ссылки на эссе и оригинальные видео YC/Sequoia. Тексты — пересказ, не дословные цитаты.
- Autoresearch: программа экспериментов в Markdown, изменение train.py, 5 минут обучения, val_bpb и сохранение/откат. Каталожная дата 08.03.2026 относится к сообщению автора о переносе результатов, не к первому релизу.

## Проверенные первоисточники

- https://arxiv.org/abs/1701.06538
- https://arxiv.org/abs/2401.06066
- https://arxiv.org/html/2412.19437v1 (таблица затрат и исключение prior research)
- https://github.com/MoonshotAI/Kimi-K2
- https://www.kimi.com/en/blog/kimi-k2-5
- https://www.kimi.com/en/help/docs-and-sheets/docs-and-sheets-overview
- https://www.anthropic.com/research/equipping-agents-for-the-real-world-with-agent-skills
- https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/
- https://kiro.dev/blog/specs-bugfix-and-design-first/
- https://karpathy.medium.com/software-2-0-a64152b37c35
- https://www.youtube.com/watch?v=LCEmiRjPEtQ
- https://www.youtube.com/watch?v=96jN2OCOfLs (ссылка также подтверждена страницей Stephanie Zhan на sequoiacap.com)
- https://github.com/karpathy/autoresearch
- https://x.com/karpathy/status/2030777122223173639?lang=en

Первые посты X про vibe coding и agentic engineering вернули 403; embed не дал содержимого. Точные цитаты и даты этих постов не добавлялись. Оригинальные видео и их индексированные описания подтвердили темы; полный видеотранскрипт не использовался. В публичных карточках это не превращено в выдуманную дословную цитату.

## Проверка реализации

`output/playwright/experts/results.json`: 68 успешных проверок; все 25 экранов без переполнения при 1440×900, ошибок JavaScript нет. Проверены источники/модальные окна, клавиатура, главы, fullscreen, возврат к фильтрам, 41 карточка, старые ссылки и работа file://. Новые экраны проверены по изображениям: `output/playwright/experts/new-slides.png`.
