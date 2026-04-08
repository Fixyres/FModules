__version__ = (9, 3, 8)

# meta developer: @FModules
# meta pic: https://raw.githubusercontent.com/Fixyres/FModules/refs/heads/main/assets/FHeta/logo.png
# meta banner: https://raw.githubusercontent.com/Fixyres/FModules/refs/heads/main/assets/FHeta/logo.png
# scope: hikka_min 1.7.2

# ©️ Fixyres, 2024-2030
# 🌐 https://github.com/Fixyres/FModules
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 🔑 http://www.apache.org/licenses/LICENSE-2.0

import asyncio
import aiohttp
import ast
import re
import sys
import uuid
from typing import Optional, Dict, List
from urllib.parse import unquote
from importlib.machinery import ModuleSpec

from .. import loader, utils
from ..types import CoreOverwriteError
from herokutl.tl.functions.contacts import UnblockRequest
from herokutl.errors.common import ScamDetectionError
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent, LinkPreviewOptions


@loader.tds
class FHeta(loader.Module):
    '''Module for searching modules! Watch all FHeta news in @FHeta_Updates!'''

    strings = {
        "name": "FHeta",
        "searching": "{emoji} <b>Searching for <code>{query}</code>...</b>",
        "no_query": "{emoji} <b>You didn't enter a search query, example: <code>{prefix}fheta your query</code></b>",
        "no_results": "{emoji} <b>Nothing found for query <code>{query}</code>.</b>",
        "query_too_big": "{emoji} <b>Your query is too big, please try reducing it to 168 characters.</b>",
        "module_info": "{emoji} <code>{name}</code> <b>by</b> <code>{author}</code>",
        "module_info_version": "{emoji} <code>{name}</code> <b>by</b> <code>{author}</code> (<code>v{version}</code>)",
        "desc": "\n\n{emoji} <b>Description:</b>\n<blockquote expandable>{desc}</blockquote>",
        "cmds": "\n\n{emoji} <b>Commands:</b>\n<blockquote expandable>{cmds}</blockquote>",
        "placeholders": "\n\n{emoji} <b>Placeholders:</b>\n<blockquote expandable>{placeholders}</blockquote>",
        "more_cmds": "<i>...and {remaining} more commands.</i>",
        "more_phs": "<i>...and {remaining} more placeholders.</i>",
        "lang": "en",
        "rating_added": "✔ Rating submitted!",
        "rating_changed": "✔ Rating has been changed!",
        "rating_removed": "✔ Rating deleted!",
        "inline_no_query": "Enter a query to search.",
        "inline_desc": "Name, command, description, author.",
        "inline_no_results": "Try another query.",
        "inline_query_too_big": "Your query is too big, please try reducing it to 168 characters.",
        "query_label": "Query",
        "install_btn": "Install",
        "results_count": "{idx}/{total}",
        "join_channel": "{emoji} This is the channel with all updates in FHeta!",
        "modules_list": "{emoji} <b>All found modules:</b>",
        "success": "✔ Module successfully installed!",
        "error": "✘ Error, perhaps the module is broken!",
        "overwrite": "✘ Error, module tried to overwrite built-in module!",
        "requirements": "✘ Dependencies installation error!",
        "requirements_deps": "✘ Dependencies installation error ({deps})!",
        "code": "Code",
        "_cfg_doc_only_official_developers": "Use only modules from official Heroku developers when searching?",
        "_cfg_doc_theme": "Theme for emojis."
    }
    
    strings_ru = {
        "_cls_doc": "Модуль для поиска модулей! Следите за всеми новостями FHeta в @FHeta_Updates!",
        "searching": "{emoji} <b>Поиск по запросу <code>{query}</code>...</b>",
        "no_query": "{emoji} <b>Вы не ввели запрос для поиска, пример: <code>{prefix}fheta ваш запрос</code></b>",
        "no_results": "{emoji} <b>Ничего не найдено по запросу <code>{query}</code>.</b>",
        "query_too_big": "{emoji} <b>Ваш запрос слишком большой, пожалуйста, сократите его до 168 символов.</b>",
        "module_info": "{emoji} <code>{name}</code> <b>от</b> <code>{author}</code>",
        "module_info_version": "{emoji} <code>{name}</code> <b>от</b> <code>{author}</code> (<code>v{version}</code>)",
        "desc": "\n\n{emoji} <b>Описание:</b>\n<blockquote expandable>{desc}</blockquote>",
        "cmds": "\n\n{emoji} <b>Команды:</b>\n<blockquote expandable>{cmds}</blockquote>",
        "placeholders": "\n\n{emoji} <b>Плейсхолдеры:</b>\n<blockquote expandable>{placeholders}</blockquote>",
        "more_cmds": "<i>...и еще {remaining} команд.</i>",
        "more_phs": "<i>...и еще {remaining} плейсхолдеров.</i>",
        "lang": "ru",
        "rating_added": "✔ Оценка добавлена!",
        "rating_changed": "✔ Оценка изменена!",
        "rating_removed": "✔ Оценка удалена!",
        "inline_no_query": "Введите запрос для поиска.",
        "inline_desc": "Название, команда, описание, автор.",
        "inline_no_results": "Попробуйте другой запрос.",
        "inline_query_too_big": "Ваш запрос слишком большой, пожалуйста, сократите его до 168 символов.",
        "query_label": "Запрос",
        "install_btn": "Установить",
        "join_channel": "{emoji} Это канал со всеми обновлениями FHeta!",
        "modules_list": "{emoji} <b>Все найденные модули:</b>",
        "success": "✔ Модуль успешно установлен!",
        "error": "✘ Ошибка, возможно, модуль поломан!",
        "overwrite": "✘ Ошибка, модуль пытался перезаписать встроенный модуль!",
        "requirements": "✘ Ошибка установки зависимостей!",
        "requirements_deps": "✘ Ошибка установки зависимостей ({deps})!",
        "code": "Код",
        "_cfg_doc_only_official_developers": "Использовать только модули от официальных разработчиков Heroku при поиске?",
        "_cfg_doc_theme": "Тема для эмодзи."
    }
    
    strings_ua = {
        "_cls_doc": "Модуль для пошуку модулів! Слідкуйте за всіма новинами FHeta в @FHeta_Updates!",
        "searching": "{emoji} <b>Пошук за запитом <code>{query}</code>...</b>",
        "no_query": "{emoji} <b>Ви не ввели запит для пошуку, приклад: <code>{prefix}fheta ваш запит</code></b>",
        "no_results": "{emoji} <b>Нічого не знайдено за запитом <code>{query}</code>.</b>",
        "query_too_big": "{emoji} <b>Ваш запит занадто великий, будь ласка, скоротіть його до 168 символів.</b>",
        "module_info": "{emoji} <code>{name}</code> <b>від</b> <code>{author}</code>",
        "module_info_version": "{emoji} <code>{name}</code> <b>від</b> <code>{author}</code> (<code>v{version}</code>)",
        "desc": "\n\n{emoji} <b>Опис:</b>\n<blockquote expandable>{desc}</blockquote>",
        "cmds": "\n\n{emoji} <b>Команди:</b>\n<blockquote expandable>{cmds}</blockquote>",
        "placeholders": "\n\n{emoji} <b>Плейсхолдери:</b>\n<blockquote expandable>{placeholders}</blockquote>",
        "more_cmds": "<i>...і ще {remaining} команд.</i>",
        "more_phs": "<i>...і ще {remaining} плейсхолдерів.</i>",
        "lang": "ua",
        "rating_added": "✔ Оцінку додано!",
        "rating_changed": "✔ Оцінку змінено!",
        "rating_removed": "✔ Оцінку видалено!",
        "inline_no_query": "Введіть запит для пошуку.",
        "inline_desc": "Назва, команда, опис, автор.",
        "inline_no_results": "Спробуйте інший запит.",
        "inline_query_too_big": "Ваш запит занадто великий, будь ласка, скоротіть його до 168 символів.",
        "query_label": "Запит",
        "install_btn": "Встановити",
        "join_channel": "{emoji} Це канал з усіма оновленнями FHeta!",
        "modules_list": "{emoji} <b>Всі знайдені модулі:</b>",
        "success": "✔ Модуль успішно встановлено!",
        "error": "✘ Помилка, можливо, модуль поламаний!",
        "overwrite": "✘ Помилка, модуль намагався перезаписати вбудований модуль!",
        "requirements": "✘ Помилка встановлення залежностей!",
        "requirements_deps": "✘ Помилка встановлення залежностей ({deps})!",
        "code": "Код",
        "_cfg_doc_only_official_developers": "Використовувати тільки модулі від офіційних розробників Heroku при пошуку?",
        "_cfg_doc_theme": "Тема для емодзі."
    }
    
    strings_kz = {
        "_cls_doc": "Модульдерді іздеу модулі! FHeta барлық жаңалықтарын @FHeta_Updates арнасында қадағалаңыз!",
        "searching": "{emoji} <b><code>{query}</code> сұрауы бойынша іздеу...</b>",
        "no_query": "{emoji} <b>Сіз іздеу сұрауын енгізбедіңіз, мысал: <code>{prefix}fheta сіздің сұрауыңыз</code></b>",
        "no_results": "{emoji} <b><code>{query}</code> сұрауы бойынша ештеңе табылмады.</b>",
        "query_too_big": "{emoji} <b>Сіздің сұрауыңыз тым үлкен, оны 168 таңбаға дейін қысқартыңыз.</b>",
        "module_info": "{emoji} <code>{name}</code> <b>авторы</b> <code>{author}</code>",
        "module_info_version": "{emoji} <code>{name}</code> <b>авторы</b> <code>{author}</code> (<code>v{version}</code>)",
        "desc": "\n\n{emoji} <b>Сипаттама:</b>\n<blockquote expandable>{desc}</blockquote>",
        "cmds": "\n\n{emoji} <b>Командалар:</b>\n<blockquote expandable>{cmds}</blockquote>",
        "placeholders": "\n\n{emoji} <b>Плейсхолдерлер:</b>\n<blockquote expandable>{placeholders}</blockquote>",
        "more_cmds": "<i>...және тағы {remaining} команда.</i>",
        "more_phs": "<i>...және тағы {remaining} плейсхолдер.</i>",
        "lang": "kz",
        "rating_added": "✔ Бағалау қосылды!",
        "rating_changed": "✔ Бағалау өзгертілді!",
        "rating_removed": "✔ Бағалау жойылды!",
        "inline_no_query": "Іздеу үшін сұрау енгізіңіз.",
        "inline_desc": "Атауы, команда, сипаттама, автор.",
        "inline_no_results": "Басқа сұрауды қолданып көріңіз.",
        "inline_query_too_big": "Сіздің сұрауыңыз тым үлкен, оны 168 таңбаға дейін қысқартыңыз.",
        "query_label": "Сұрау",
        "install_btn": "Орнату",
        "join_channel": "{emoji} Бұл FHeta барлық жаңартулары бар арна!",
        "modules_list": "{emoji} <b>Барлық табылған модульдер:</b>",
        "success": "✔ Модуль сәтті орнатылды!",
        "error": "✘ Қате, мүмкін модуль бұзылған!",
        "overwrite": "✘ Қате, модуль кіріктірілген модульді қайта жазуға тырысты!",
        "requirements": "✘ Тәуелділіктерді орнату қатесі!",
        "requirements_deps": "✘ Тәуелділіктерді орнату қатесі ({deps})!",
        "code": "Код",
        "_cfg_doc_only_official_developers": "Іздеу кезінде тек ресми Heroku әзірлеушілерінің модульдерін пайдалану керек пе?",
        "_cfg_doc_theme": "Эмодзилер үшін тақырып."
    }
    
    strings_uz = {
        "_cls_doc": "Modullarni qidirish moduli! FHeta barcha yangilanishlarini @FHeta_Updates kanalida kuzatib boring!",
        "searching": "{emoji} <b><code>{query}</code> so'rovi bo'yicha qidiruv...</b>",
        "no_query": "{emoji} <b>Siz qidiruv so'rovini kiritmadingiz, misol: <code>{prefix}fheta sizning sorovingiz</code></b>",
        "no_results": "{emoji} <b><code>{query}</code> so'rovi bo'yicha hech narsa topilmadi.</b>",
        "query_too_big": "{emoji} <b>Sizning so'rovingiz juda katta, iltimos uni 168 belgigacha qisqartiring.</b>",
        "module_info": "{emoji} <code>{name}</code> <b>muallif</b> <code>{author}</code>",
        "module_info_version": "{emoji} <code>{name}</code> <b>muallif</b> <code>{author}</code> (<code>v{version}</code>)",
        "desc": "\n\n{emoji} <b>Tavsif:</b>\n<blockquote expandable>{desc}</blockquote>",
        "cmds": "\n\n{emoji} <b>Buyruqlar:</b>\n<blockquote expandable>{cmds}</blockquote>",
        "placeholders": "\n\n{emoji} <b>Pleysholderlar:</b>\n<blockquote expandable>{placeholders}</blockquote>",
        "more_cmds": "<i>...va yana {remaining} ta buyruq.</i>",
        "more_phs": "<i>...va yana {remaining} ta pleysholder.</i>",
        "lang": "uz",
        "rating_added": "✔ Reyting qo'shildi!",
        "rating_changed": "✔ Reyting o'zgartirildi!",
        "rating_removed": "✔ Reyting o'chirildi!",
        "inline_no_query": "Qidirish uchun so'rov kiriting.",
        "inline_desc": "Nomi, buyruq, tavsif, muallif.",
        "inline_no_results": "Boshqa so'rovni sinab ko'ring.",
        "inline_query_too_big": "Sizning so'rovingiz juda katta, iltimos uni 168 belgigacha qisqartiring.",
        "query_label": "So'rov",
        "install_btn": "O'rnatish",
        "join_channel": "{emoji} Bu FHeta barcha yangilanishlari bo'lgan kanal!",
        "modules_list": "{emoji} <b>Barcha topilgan modullar:</b>",
        "success": "✔ Modul muvaffaqiyatli o'rnatildi!",
        "error": "✘ Xatolik, ehtimol modul buzilgan!",
        "overwrite": "✘ Xatolik, modul o'rnatilgan modulni qayta yozishga harakat qildi!",
        "requirements": "✘ Bog'liqliklarni o'rnatish xatosi!",
        "requirements_deps": "✘ Bog'liqliklarni o'rnatish xatosi ({deps})!",
        "code": "Kod",
        "_cfg_doc_only_official_developers": "Qidiruv paytida faqat rasmiy Heroku ishlab chiquvchilarining modullaridan foydalanish kerakmi?",
        "_cfg_doc_theme": "Emojilar uchun mavzu."
    }
    
    strings_fr = {
        "_cls_doc": "Module de recherche de modules! Suivez toutes les actualités FHeta sur @FHeta_Updates!",
        "searching": "{emoji} <b>Recherche pour <code>{query}</code>...</b>",
        "no_query": "{emoji} <b>Vous n'avez pas entré de requête de recherche, exemple: <code>{prefix}fheta votre requête</code></b>",
        "no_results": "{emoji} <b>Rien trouvé pour la requête <code>{query}</code>.</b>",
        "query_too_big": "{emoji} <b>Votre requête est trop longue, veuillez la réduire à 168 caractères.</b>",
        "module_info": "{emoji} <code>{name}</code> <b>par</b> <code>{author}</code>",
        "module_info_version": "{emoji} <code>{name}</code> <b>par</b> <code>{author}</code> (<code>v{version}</code>)",
        "desc": "\n\n{emoji} <b>Description:</b>\n<blockquote expandable>{desc}</blockquote>",
        "cmds": "\n\n{emoji} <b>Commandes:</b>\n<blockquote expandable>{cmds}</blockquote>",
        "placeholders": "\n\n{emoji} <b>Espaces réservés:</b>\n<blockquote expandable>{placeholders}</blockquote>",
        "more_cmds": "<i>...et {remaining} commandes supplémentaires.</i>",
        "more_phs": "<i>...et {remaining} espaces réservés supplémentaires.</i>",
        "lang": "fr",
        "rating_added": "✔ Note ajoutée!",
        "rating_changed": "✔ Note modifiée!",
        "rating_removed": "✔ Note supprimée!",
        "inline_no_query": "Entrez une requête pour rechercher.",
        "inline_desc": "Nom, commande, description, auteur.",
        "inline_no_results": "Essayez une autre requête.",
        "inline_query_too_big": "Votre requête est trop longue, veuillez la réduire à 168 caractères.",
        "query_label": "Requête",
        "install_btn": "Installer",
        "join_channel": "{emoji} C'est le canal avec toutes les mises à jour de FHeta!",
        "modules_list": "{emoji} <b>Tous les modules trouvés:</b>",
        "success": "✔ Module installé avec succès!",
        "error": "✘ Erreur, le module est peut-être cassé!",
        "overwrite": "✘ Erreur, le module a tenté d'écraser le module intégré!",
        "requirements": "✘ Erreur d'installation des dépendances!",
        "requirements_deps": "✘ Erreur d'installation des dépendances ({deps})!",
        "code": "Code",
        "_cfg_doc_only_official_developers": "Utiliser uniquement les modules des développeurs Heroku officiels lors de la recherche?",
        "_cfg_doc_theme": "Thème pour les emojis."
    }
    
    strings_de = {
        "_cls_doc": "Modul zur Suche nach Modulen! Verfolgen Sie alle FHeta-Neuigkeiten auf @FHeta_Updates!",
        "searching": "{emoji} <b>Suche nach <code>{query}</code>...</b>",
        "no_query": "{emoji} <b>Sie haben keine Suchanfrage eingegeben, Beispiel: <code>{prefix}fheta ihre anfrage</code></b>",
        "no_results": "{emoji} <b>Nichts gefunden für Anfrage <code>{query}</code>.</b>",
        "query_too_big": "{emoji} <b>Ihre Anfrage ist zu groß, bitte reduzieren Sie sie auf 168 Zeichen.</b>",
        "module_info": "{emoji} <code>{name}</code> <b>von</b> <code>{author}</code>",
        "module_info_version": "{emoji} <code>{name}</code> <b>von</b> <code>{author}</code> (<code>v{version}</code>)",
        "desc": "\n\n{emoji} <b>Beschreibung:</b>\n<blockquote expandable>{desc}</blockquote>",
        "cmds": "\n\n{emoji} <b>Befehle:</b>\n<blockquote expandable>{cmds}</blockquote>",
        "placeholders": "\n\n{emoji} <b>Platzhalter:</b>\n<blockquote expandable>{placeholders}</blockquote>",
        "more_cmds": "<i>...und {remaining} weitere Befehle.</i>",
        "more_phs": "<i>...und {remaining} weitere Platzhalter.</i>",
        "lang": "de",
        "rating_added": "✔ Bewertung hinzugefügt!",
        "rating_changed": "✔ Bewertung geändert!",
        "rating_removed": "✔ Bewertung gelöscht!",
        "inline_no_query": "Geben Sie eine Suchanfrage ein.",
        "inline_desc": "Name, Befehl, Beschreibung, Autor.",
        "inline_no_results": "Versuchen Sie eine andere Anfrage.",
        "inline_query_too_big": "Ihre Anfrage ist zu groß, bitte reduzieren Sie sie auf 168 Zeichen.",
        "query_label": "Anfrage",
        "install_btn": "Installieren",
        "join_channel": "{emoji} Dies ist der Kanal mit allen FHeta-Updates!",
        "modules_list": "{emoji} <b>Alle gefundenen Module:</b>",
        "success": "✔ Modul erfolgreich installiert!",
        "error": "✘ Fehler, vielleicht ist das Modul kaputt!",
        "overwrite": "✘ Fehler, Modul hat versucht, das integrierte Modul zu überschreiben!",
        "requirements": "✘ Fehler bei der Installation von Abhängigkeiten!",
        "requirements_deps": "✘ Fehler bei der Installation von Abhängigkeiten ({deps})!",
        "code": "Code",
        "_cfg_doc_only_official_developers": "Nur Module von offiziellen Heroku-Entwicklern bei der Suche verwenden?",
        "_cfg_doc_theme": "Thema für Emojis."
    }
    
    strings_jp = {
        "_cls_doc": "モジュール検索用モジュール！@FHeta_UpdatesでFHetaのすべてのニュースをフォローしてください！",
        "searching": "{emoji} <b><code>{query}</code>を検索中...</b>",
        "no_query": "{emoji} <b>検索クエリを入力していません、例: <code>{prefix}fheta あなたのクエリ</code></b>",
        "no_results": "{emoji} <b>クエリ<code>{query}</code>で何も見つかりませんでした。</b>",
        "query_too_big": "{emoji} <b>クエリが大きすぎます。168文字に短縮してください。</b>",
        "module_info": "{emoji} <code>{name}</code> <b>作成者</b> <code>{author}</code>",
        "module_info_version": "{emoji} <code>{name}</code> <b>作成者</b> <code>{author}</code> (<code>v{version}</code>)",
        "desc": "\n\n{emoji} <b>説明:</b>\n<blockquote expandable>{desc}</blockquote>",
        "cmds": "\n\n{emoji} <b>コマンド:</b>\n<blockquote expandable>{cmds}</blockquote>",
        "placeholders": "\n\n{emoji} <b>プレースホルダー:</b>\n<blockquote expandable>{placeholders}</blockquote>",
        "more_cmds": "<i>...さらに {remaining} 個のコマンド。</i>",
        "more_phs": "<i>...さらに {remaining} 個のプレースホルダー。</i>",
        "lang": "jp",
        "rating_added": "✔ 評価が追加されました！",
        "rating_changed": "✔ 評価が変更されました！",
        "rating_removed": "✔ 評価が削除されました！",
        "inline_no_query": "検索するクエリを入力してください。",
        "inline_desc": "名前、コマンド、説明、作成者。",
        "inline_no_results": "別のクエリを試してください。",
        "inline_query_too_big": "クエリが大きすぎます。168文字に短縮してください。",
        "query_label": "クエリ",
        "install_btn": "インストール",
        "join_channel": "{emoji} これはFHetaのすべての更新があるチャンネルです！",
        "modules_list": "{emoji} <b>見つかったすべてのモジュール:</b>",
        "success": "✔ モジュールが正常にインストールされました!",
        "error": "✘ エラー、モジュールが壊れている可能性があります!",
        "overwrite": "✘ エラー、モジュールが組み込みモジュールを上書きしようとしました!",
        "requirements": "✘ 依存関係のインストールエラー!",
        "requirements_deps": "✘ 依存関係のインストールエラー ({deps})!",
        "code": "コード",
        "_cfg_doc_only_official_developers": "検索時に公式Heroku開発者のモジュールのみを使用しますか？",
        "_cfg_doc_theme": "絵文字のテーマ。"
    }
    
    THEMES = {
        "default": {
            "search": '<tg-emoji emoji-id="5188217332748527444">🔍</tg-emoji>',
            "error": '<tg-emoji emoji-id="5465665476971471368">❌</tg-emoji>',
            "warn": '<tg-emoji emoji-id="5447644880824181073">⚠️</tg-emoji>',
            "description": '<tg-emoji emoji-id="5334882760735598374">📝</tg-emoji>',
            "command": '<tg-emoji emoji-id="5341715473882955310">⚙️</tg-emoji>',
            "placeholder": '<tg-emoji emoji-id="5359785904535774578">🗒️</tg-emoji>',
            "module": '<tg-emoji emoji-id="5454112830989025752">📦</tg-emoji>',
            "channel": '<tg-emoji emoji-id="5278256077954105203">📢</tg-emoji>',
            "modules_list": '<tg-emoji emoji-id="5197269100878907942">📋</tg-emoji>'
        },
        "winter": {
            "search": '<tg-emoji emoji-id="5431895003821513760">❄️</tg-emoji>',
            "error": '<tg-emoji emoji-id="5404728536810398694">🧊</tg-emoji>',
            "warn": '<tg-emoji emoji-id="5447644880824181073">🌨️</tg-emoji>',
            "description": '<tg-emoji emoji-id="5255850496291259327">📜</tg-emoji>',
            "command": '<tg-emoji emoji-id="5199503707938505333">🎅</tg-emoji>',
            "placeholder": '<tg-emoji emoji-id="5204046675236109418">🗒️</tg-emoji>',
            "module": '<tg-emoji emoji-id="5197708768091061888">🎁</tg-emoji>',
            "channel": '<tg-emoji emoji-id="5278256077954105203">📢</tg-emoji>',
            "modules_list": '<tg-emoji emoji-id="5345935030143196497">🎄</tg-emoji>'
        },
        "summer": {
            "search": '<tg-emoji emoji-id="5188217332748527444">🔍</tg-emoji>',
            "error": '<tg-emoji emoji-id="5470049770997292425">🌡️</tg-emoji>',
            "warn": '<tg-emoji emoji-id="5447644880824181073">⚠️</tg-emoji>',
            "description": '<tg-emoji emoji-id="5361684086807076580">🍹</tg-emoji>',
            "command": '<tg-emoji emoji-id="5442644589703866634">🏄</tg-emoji>',
            "placeholder": '<tg-emoji emoji-id="5434121252874756456">🗒️</tg-emoji>',
            "module": '<tg-emoji emoji-id="5433645645376264953">🏖️</tg-emoji>',
            "channel": '<tg-emoji emoji-id="5278256077954105203">📢</tg-emoji>',
            "modules_list": '<tg-emoji emoji-id="5472178859300363509">🏖️</tg-emoji>'
        },
        "spring": {
            "search": '<tg-emoji emoji-id="5449885771420934013">🌱</tg-emoji>',
            "error": '<tg-emoji emoji-id="5208923808169222461">🥀</tg-emoji>',
            "warn": '<tg-emoji emoji-id="5447644880824181073">⚠️</tg-emoji>',
            "description": '<tg-emoji emoji-id="5251524493561569780">🍃</tg-emoji>',
            "command": '<tg-emoji emoji-id="5449850741667668411">🦋</tg-emoji>',
            "placeholder": '<tg-emoji emoji-id="5434121252874756456">🗒️</tg-emoji>',
            "module": '<tg-emoji emoji-id="5440911110838425969">🌿</tg-emoji>',
            "channel": '<tg-emoji emoji-id="5278256077954105203">📢</tg-emoji>',
            "modules_list": '<tg-emoji emoji-id="5440748683765227563">🌺</tg-emoji>'
        },
        "autumn": {
            "search": '<tg-emoji emoji-id="5253944419870062295">🍂</tg-emoji>',
            "error": '<tg-emoji emoji-id="5281026503658728615">🍁</tg-emoji>',
            "warn": '<tg-emoji emoji-id="5447644880824181073">⚠️</tg-emoji>',
            "description": '<tg-emoji emoji-id="5406631276042002796">📜</tg-emoji>',
            "command": '<tg-emoji emoji-id="5212963577098417551">🍂</tg-emoji>',
            "placeholder": '<tg-emoji emoji-id="5363965354391388799">🗒️</tg-emoji>',
            "module": '<tg-emoji emoji-id="5249157915041865558">🍄</tg-emoji>',
            "channel": '<tg-emoji emoji-id="5278256077954105203">📢</tg-emoji>',
            "modules_list": '<tg-emoji emoji-id="5305495722618010655">🍂</tg-emoji>'
        }
    }
    
    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "only_official_developers",
                False,
                lambda: self.strings("_cfg_doc_only_official_developers"),
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "theme",
                "default",
                lambda: self.strings("_cfg_doc_theme"),
                validator=loader.validators.Choice(["default", "winter", "summer", "spring", "autumn"])
            )
        )
    
    async def client_ready(self, client, db):
        try:
            await client(UnblockRequest("@FHeta_robot"))
            await utils.dnd(client, "@FHeta_robot", archive=True)
        except:
            pass
        
        self.uid = (await client.get_me()).id
        self.token = db.get("FHeta", "token")
        self._asession = aiohttp.ClientSession()
        
        if self.token:
            result = await self._api_get("validatetkn", user_id=str(self.uid))
            if result == False:
                self.token = None
        
        if not self.token:
            try:
                async with client.conversation("@FHeta_robot") as conv:
                    await conv.send_message('/token')
                    resp = await conv.get_response(timeout=5)
                    self.token = resp.text.strip()
                    db.set("FHeta", "token", self.token)
            except:
                pass
        
        asyncio.create_task(self._sync_loop())
        
    async def _sync_loop(self):
        ll = None
        while True:
            try:
                cl = self.strings["lang"]
                if cl != ll:
                    await self._api_post("dataset", params={"user_id": self.uid, "lang": cl})
                    ll = cl
            except Exception:
                pass
            await asyncio.sleep(1)

    async def _api_get(self, endpoint: str, **params):
        try:
            async with self._asession.get(
                f"https://api.fixyres.com/{endpoint}",
                params=params,
                headers={"Authorization": self.token},
                timeout=aiohttp.ClientTimeout(total=180)
            ) as response:
                if response.status == 200:
                    return await response.json()
                return {}
        except Exception:
            return {}

    async def _api_post(self, endpoint: str, json: Dict = None, **params):
        try:
            async with self._asession.post(
                f"https://api.fixyres.com/{endpoint}",
                json=json,
                params=params,
                headers={"Authorization": self.token},
                timeout=aiohttp.ClientTimeout(total=180)
            ) as response:
                if response.status == 200:
                    return await response.json()
                return {}
        except Exception:
            return {}

    def _get_emoji(self, key: str) -> str:
        return self.THEMES[self.config["theme"]][key]

    def _fmt_mod(self, mod: Dict, query: str = "", idx: int = 1, total: int = 1, inline: bool = False) -> str:
        version = mod.get("version", "?.?.?")
        limit = 3700
        
        if version and version != "?.?.?":
            info = self.strings["module_info_version"].format(
                emoji=self._get_emoji("module"),
                name=utils.escape_html(mod.get("name", "")),
                author=utils.escape_html(mod.get("author", "???")),
                version=utils.escape_html(version)
            )
        else:
            info = self.strings["module_info"].format(
                emoji=self._get_emoji("module"),
                name=utils.escape_html(mod.get("name", "")),
                author=utils.escape_html(mod.get("author", "???"))
            )

        desc = mod.get("description")
        if desc:
            if isinstance(desc, dict):
                text = desc.get(self.strings["lang"]) or desc.get("doc") or next(iter(desc.values()), "")
            else:
                text = desc
            
            text = str(text)
            
            info += self.strings["desc"].format(desc=utils.escape_html(text), emoji=self._get_emoji("description"))

        info_clean_len = len(re.sub(r'<[^>]+>', '', info))
        cmds_text = self._fmt_cmds(mod.get("commands",[]), limit=limit - info_clean_len)
        info += cmds_text
        
        info_clean_len = len(re.sub(r'<[^>]+>', '', info))
        phs_text = self._fmt_phs(mod.get("placeholders",[]), limit=limit - info_clean_len)
        info += phs_text

        return info

    def _fmt_cmds(self, cmds: List[Dict], limit: int) -> str:
        if not cmds:
            return ""
        cmd_lines =[]
        lang = self.strings["lang"]
        
        for i, cmd in enumerate(cmds):
            desc_dict = cmd.get("description", {})
            desc_text = desc_dict.get(lang) or desc_dict.get("doc") or ""
            
            if isinstance(desc_text, dict):
                desc_text = desc_text.get("doc", "")
            
            cmd_name = utils.escape_html(cmd.get("name", ""))
            cmd_desc = utils.escape_html(desc_text) if desc_text else ""

            if cmd_desc:
                cmd_desc = cmd_desc.split('\n')[0]

            if cmd.get("inline"):
                line = f"<code>@{self.inline.bot_username} {cmd_name}</code> {cmd_desc}"
            else:
                line = f"<code>{self.get_prefix()}{cmd_name}</code> {cmd_desc}"
            
            current_text = "\n".join(cmd_lines)
            test_text = current_text + ("\n" if current_text else "") + line
            
            more_str = self.strings["more_cmds"].format(remaining=len(cmds) - i)
            test_text_with_more = test_text + "\n" + more_str
            
            if len(re.sub(r'<[^>]+>', '', test_text_with_more)) > limit and i > 0:
                cmd_lines.append(more_str)
                break
            
            cmd_lines.append(line)

        if cmd_lines:
            return self.strings["cmds"].format(cmds="\n".join(cmd_lines), emoji=self._get_emoji("command"))
            
        return ""

    def _fmt_phs(self, phs: List[Dict], limit: int) -> str:
        if not phs:
            return ""
        ph_lines =[]
        
        for i, ph in enumerate(phs):
            ph_name = utils.escape_html(ph.get("name", ""))
            ph_desc = utils.escape_html(ph.get("description", ""))
            
            if ph_desc:
                line = f"<code>{{{ph_name}}}</code> {ph_desc}"
            else:
                line = f"<code>{{{ph_name}}}</code>"
            
            current_text = "\n".join(ph_lines)
            test_text = current_text + ("\n" if current_text else "") + line
            
            more_str = self.strings["more_phs"].format(remaining=len(phs) - i)
            test_text_with_more = test_text + "\n" + more_str
            
            if len(re.sub(r'<[^>]+>', '', test_text_with_more)) > limit and i > 0:
                ph_lines.append(more_str)
                break
            
            ph_lines.append(line)

        if ph_lines:
            return self.strings["placeholders"].format(placeholders="\n".join(ph_lines), emoji=self._get_emoji("placeholder"))
            
        return ""

    def _mk_btns(self, install: str, stats: Dict, idx: int, mods: Optional[List] = None, query: str = "") -> List[List[Dict]]:
        buttons =[]
        
        decoded_install = unquote(install.replace('%20', '___SPACE___')).replace('___SPACE___', '%20')
        install_url = decoded_install[4:] if decoded_install.startswith('dlm ') else decoded_install
        
        if query:
            buttons.append([
                {"text": self.strings["query_label"], "copy": query},
                {"text": self.strings["install_btn"], "callback": self._install_cb, "args": (install_url, idx, mods, query)},
                {"text": self.strings["code"], "url": install_url}
            ])
        
        buttons.append([
            {"text": f"↑ {stats.get('likes', 0)}", "callback": self._rate_cb, "args": (install, "like", idx, mods, query)},
            {"text": f"↓ {stats.get('dislikes', 0)}", "callback": self._rate_cb, "args": (install, "dislike", idx, mods, query)}
        ])
        
        if mods and len(mods) > 1:
            buttons[-1].insert(1, {"text": self.strings["results_count"].format(idx=idx+1, total=len(mods)), "callback": self._show_list_cb, "args": (idx, mods, query)})

        if mods and len(mods) > 1:
            nav_buttons =[]
            if idx > 0:
                nav_buttons.append({"text": "←", "callback": self._nav_cb, "args": (idx - 1, mods, query)})
            if idx < len(mods) - 1:
                nav_buttons.append({"text": "→", "callback": self._nav_cb, "args": (idx + 1, mods, query)})
            if nav_buttons:
                buttons.append(nav_buttons)

        return buttons

    def _mk_list_btns(self, mods: List, query: str, page: int = 0, current_idx: int = 0) -> List[List[Dict]]:
        buttons =[]
        items_per_page = 8
        total_pages = (len(mods) + items_per_page - 1) // items_per_page
        
        start_idx = page * items_per_page
        end_idx = min(start_idx + items_per_page, len(mods))
        
        for i in range(start_idx, end_idx):
            mod = mods[i]
            name = mod.get("name", "Unknown")
            author = mod.get("author", "???")
            button_text = f"{i + 1}. {name} by {author}"
            buttons.append([
                {"text": button_text, "callback": self._select_from_list_cb, "args": (i, mods, query)}
            ])
        
        nav_buttons =[]
        if page > 0:
            nav_buttons.append({"text": "←", "callback": self._list_page_cb, "args": (page - 1, mods, query, current_idx)})
        if page < total_pages - 1:
            nav_buttons.append({"text": "→", "callback": self._list_page_cb, "args": (page + 1, mods, query, current_idx)})
        
        if nav_buttons:
            buttons.append(nav_buttons)
        
        buttons.append([
            {"text": "✘", "callback": self._close_list_cb, "args": (current_idx, mods, query)}
        ])
        
        return buttons

    async def _edit_with_preview(self, call_or_msg_id, text: str, reply_markup: list, banner_url: str = None):
        if banner_url:
            lo = LinkPreviewOptions(url=banner_url, show_above_text=True, prefer_large_media=True)
        else:
            lo = LinkPreviewOptions(is_disabled=True)
            
        markup = self.inline.generate_markup(reply_markup)
        
        try:
            if isinstance(call_or_msg_id, str):
                await self.inline.bot.edit_message_text(
                    inline_message_id=call_or_msg_id,
                    text=text,
                    reply_markup=markup,
                    link_preview_options=lo,
                    parse_mode="HTML"
                )
            else:
                inline_msg_id = getattr(call_or_msg_id, "inline_message_id", None)
                if inline_msg_id:
                    await self.inline.bot.edit_message_text(
                        inline_message_id=inline_msg_id,
                        text=text,
                        reply_markup=markup,
                        link_preview_options=lo,
                        parse_mode="HTML"
                    )
                elif getattr(call_or_msg_id, "message", None):
                    await self.inline.bot.edit_message_text(
                        chat_id=call_or_msg_id.message.chat.id,
                        message_id=call_or_msg_id.message.message_id,
                        text=text,
                        reply_markup=markup,
                        link_preview_options=lo,
                        parse_mode="HTML"
                    )
        except Exception:
            pass

    async def _show_list_cb(self, call, idx: int, mods: List, query: str):
        try:
            await call.answer()
        except:
            pass
        
        await self._edit_with_preview(
            call,
            text=self.strings["modules_list"].format(emoji=self._get_emoji("modules_list")),
            reply_markup=self._mk_list_btns(mods, query, 0, idx),
            banner_url=None
        )

    async def _list_page_cb(self, call, page: int, mods: List, query: str, current_idx: int):
        try:
            await call.answer()
        except:
            pass
            
        await self._edit_with_preview(
            call,
            text=self.strings["modules_list"].format(emoji=self._get_emoji("modules_list")),
            reply_markup=self._mk_list_btns(mods, query, page, current_idx),
            banner_url=None
        )

    async def _select_from_list_cb(self, call, idx: int, mods: List, query: str):
        try:
            await call.answer()
        except:
            pass
        
        if not (0 <= idx < len(mods)):
            return
        
        mod = mods[idx]
        install = mod.get('install', '')
        stats = mod if all(k in mod for k in['likes', 'dislikes']) else {"likes": 0, "dislikes": 0}
        
        await self._edit_with_preview(
            call,
            text=self._fmt_mod(mod, query, idx + 1, len(mods)),
            reply_markup=self._mk_btns(install, stats, idx, mods, query),
            banner_url=mod.get("banner")
        )

    async def _close_list_cb(self, call, idx: int, mods: List, query: str):
        try:
            await call.answer()
        except:
            pass
        
        if not (0 <= idx < len(mods)):
            return
        
        mod = mods[idx]
        install = mod.get('install', '')
        stats = mod if all(k in mod for k in['likes', 'dislikes']) else {"likes": 0, "dislikes": 0}
        
        await self._edit_with_preview(
            call,
            text=self._fmt_mod(mod, query, idx + 1, len(mods)),
            reply_markup=self._mk_btns(install, stats, idx, mods, query),
            banner_url=mod.get("banner")
        )

    async def _rate_cb(self, call, install: str, action: str, idx: int, mods: Optional[List], query: str = ""):
        result = await self._api_post(f"rate/{self.uid}/{install}/{action}")
        
        decoded_install = unquote(install)
        
        if mods and idx < len(mods):
            mod = mods[idx]
            stats_response = await self._api_post("get", json=[decoded_install])
            stats = stats_response.get(decoded_install, {"likes": 0, "dislikes": 0})
            
            mod["likes"] = stats.get("likes", 0)
            mod["dislikes"] = stats.get("dislikes", 0)
        else:
            stats_response = await self._api_post("get", json=[decoded_install])
            stats = stats_response.get(decoded_install, {"likes": 0, "dislikes": 0})
        
        try:
            await call.edit(reply_markup=self._mk_btns(install, stats, idx, mods, query))
        except:
            pass

        if result and result.get("status"):
            result_status = result.get("status", "")
            try:
                if result_status == "added":
                    await call.answer(self.strings["rating_added"], show_alert=True)
                elif result_status == "changed":
                    await call.answer(self.strings["rating_changed"], show_alert=True)
                elif result_status == "removed":
                    await call.answer(self.strings["rating_removed"], show_alert=True)
            except:
                pass

    async def _install_cb(self, call, install_url: str, idx: int, mods: Optional[List], query: str = ""):
        lm = self.lookup("loader")
        
        try:
            r = await lm._storage.fetch(install_url, auth=lm.config.get("basic_auth"))
        except (aiohttp.ClientError, aiohttp.ClientResponseError) as e:
            try:
                await call.answer(
                    self.strings["error"],
                    show_alert=True
                )
            except:
                pass
            return
        
        doc = r
        origin = install_url
        
        max_attempts = 5
        for attempt in range(max_attempts):
            try:
                result = await self._load_module(lm, doc, origin, attempt)
                
                if result == "success":
                    if lm.fully_loaded:
                        lm.update_modules_in_db()
                    
                    try:
                        await call.answer(
                            self.strings["success"],
                            show_alert=True
                        )
                    except:
                        pass
                    return
                
                elif result == "retry":
                    if attempt < max_attempts - 1:
                        await asyncio.sleep(0.33)
                        continue
                    else:
                        try:
                            await call.answer(
                                self.strings["requirements"],
                                show_alert=True
                            )
                        except Exception:
                            pass
                        return
                
                elif isinstance(result, dict) and result.get("type") == "requirements_error":
                    deps = result.get("deps",[])
                    if deps:
                        deps_text = ", ".join(deps[:5])
                        try:
                            await call.answer(
                                self.strings["requirements_deps"].format(deps=deps_text),
                                show_alert=True
                            )
                        except:
                            pass
                    else:
                        try:
                            await call.answer(
                                self.strings["requirements"],
                                show_alert=True
                            )
                        except:
                            pass
                    return
                
                elif result == "overwrite":
                    try:
                        await call.answer(
                            self.strings["overwrite"],
                            show_alert=True
                        )
                    except:
                        pass
                    return
                
                else:
                    try:
                        await call.answer(
                            self.strings["error"],
                            show_alert=True
                        )
                    except:
                        pass
                    return
                    
            except:
                try:
                    await call.answer(
                        self.strings["error"],
                        show_alert=True
                    )
                except:
                    pass
                return
        
        try:
            await call.answer(
                self.strings["requirements"],
                show_alert=True
            )
        except:
            pass

    async def _nav_cb(self, call, idx: int, mods: List, query: str = ""):
        try:
            await call.answer()
        except:
            pass
            
        if not (0 <= idx < len(mods)):
            return
        
        mod = mods[idx]
        install = mod.get('install', '')
        stats = mod if all(k in mod for k in['likes', 'dislikes']) else {"likes": 0, "dislikes": 0}
        
        await self._edit_with_preview(
            call,
            text=self._fmt_mod(mod, query, idx + 1, len(mods)),
            reply_markup=self._mk_btns(install, stats, idx, mods, query),
            banner_url=mod.get("banner")
        )

    @loader.inline_handler(
        ru_doc="(запрос) - поиск модулей.",
        ua_doc="(запит) - пошук модулів.",
        kz_doc="(сұрау) - модульдерді іздеу.",
        uz_doc="(so'rov) - modullarni qidirish.",
        fr_doc="(requête) - rechercher des modules.",
        de_doc="(anfrage) - module suchen.",
        jp_doc="(クエリ) - モジュールを検索します。"
    )
    async def fheta(self, query):
        '''(query) - search modules.'''
        actual_query = query.args
        is_cmd = False

        if actual_query.startswith("__cmd__ "):
            is_cmd = True
            actual_query = actual_query[8:]

        if not actual_query:
            return {
                "title": self.strings["inline_no_query"],
                "description": self.strings["inline_desc"],
                "message": self.strings["inline_no_query"].format(emoji=self._get_emoji("error")),
                "thumb": "https://raw.githubusercontent.com/Fixyres/FModules/refs/heads/main/assets/FHeta/magnifying_glass.png",
            }

        if len(actual_query) > 168:
            return {
                "title": self.strings["inline_query_too_big"],
                "description": self.strings["inline_no_results"],
                "message": self.strings["query_too_big"].format(emoji=self._get_emoji("warn")),
                "thumb": "https://raw.githubusercontent.com/Fixyres/FModules/refs/heads/main/assets/FHeta/try_other_query.png",
            }

        mods = await self._api_get("search", query=actual_query, inline="true", token=self.token, user_id=self.uid, ood=str(self.config["only_official_developers"]).lower())
        
        if not mods or not isinstance(mods, list):
            return {
                "title": self.strings["inline_no_results"],
                "description": self.strings["inline_desc"],
                "message": self.strings["inline_no_results"],
                "thumb": "https://raw.githubusercontent.com/Fixyres/FModules/refs/heads/main/assets/FHeta/try_other_query.png",
            }

        results = []
        
        for i, mod in enumerate(mods[:50]):
            stats = {
                "likes": mod.get('likes', 0),
                "dislikes": mod.get('dislikes', 0)
            }
            
            desc = mod.get("description", "")
            if isinstance(desc, dict):
                desc = desc.get(self.strings["lang"]) or desc.get("doc") or next(iter(desc.values()), "")
            
            desc_str = str(desc)
            inline_desc = desc_str[:250] + "..." if len(desc_str) > 250 else desc_str
            
            msg_text = self._fmt_mod(mod, actual_query, i + 1 if is_cmd else 1, len(mods) if is_cmd else 1, inline=True)
            banner = mod.get("banner")
            
            if banner:
                lo = LinkPreviewOptions(url=banner, show_above_text=True, prefer_large_media=True)
            else:
                lo = LinkPreviewOptions(is_disabled=True)

            pic = mod.get("pic")
            if not pic:
                pic = "https://raw.githubusercontent.com/Fixyres/FModules/refs/heads/main/assets/FHeta/empty_pic.png"

            results.append(
                InlineQueryResultArticle(
                    id=utils.rand(20),
                    title=utils.escape_html(mod.get("name", "")),
                    description=utils.escape_html(inline_desc),
                    thumbnail_url=pic,
                    input_message_content=InputTextMessageContent(
                        message_text=msg_text,
                        parse_mode="HTML",
                        link_preview_options=lo
                    ),
                    reply_markup=self.inline.generate_markup(
                        self._mk_btns(mod.get("install", ""), stats, i if is_cmd else 0, mods if is_cmd else None, actual_query)
                    )
                )
            )

        await query.inline_query.answer(results, cache_time=0)
        return None

    @loader.command(
        ru_doc="(запрос) - поиск модулей.",
        ua_doc="(запит) - пошук модулів.",
        kz_doc="(сұрау) - модульдерді іздеу.",
        uz_doc="(so'rov) - modullarni qidirish.",
        fr_doc="(requête) - rechercher des modules.",
        de_doc="(anfrage) - module suchen.",
        jp_doc="(クエリ) - モジュールを検索します。"
    )
    async def fhetacmd(self, message):
        '''(query) - search modules.'''
        query = utils.get_args_raw(message)
        
        if not query:
            await utils.answer(message, self.strings["no_query"].format(emoji=self._get_emoji("error"), prefix=self.get_prefix()))
            return

        if len(query) > 168:
            await utils.answer(message, self.strings["query_too_big"].format(emoji=self._get_emoji("warn")))
            return

        message = await utils.answer(message, self.strings["searching"].format(emoji=self._get_emoji("search"), query=utils.escape_html(query)))
        
        mods = await self._api_get("search", query=query, inline="false", token=self.token, user_id=self.uid, ood=str(self.config["only_official_developers"]).lower())
        
        if not mods or not isinstance(mods, list):
            await utils.answer(message, self.strings["no_results"].format(emoji=self._get_emoji("error"), query=utils.escape_html(query)))
            return

        mod = mods[0]
        text = self._fmt_mod(mod, query, 1, len(mods))
        stats = {"likes": mod.get("likes", 0), "dislikes": mod.get("dislikes", 0)}
        install = mod.get("install", "")
        buttons = self._mk_btns(install, stats, 0, mods, query)
        
        form = await self.inline.form("🪐", message, silent=True)
        
        await self._edit_with_preview(
            form,
            text=text,
            reply_markup=buttons,
            banner_url=mod.get("banner"),
        )
        
    @loader.watcher(chat_id=7575472403)
    async def _install_via_fheta(self, message):
        link = message.raw_text.strip()
        
        if not link.startswith("https://api.fixyres.com/module/"):
            return
        
        try:
            lm = self.lookup("loader")
            
            try:
                r = await lm._storage.fetch(link, auth=lm.config.get("basic_auth"))
            except (aiohttp.ClientError, aiohttp.ClientResponseError):
                status_msg = await message.respond("❌")
                await asyncio.sleep(0.67)
                await status_msg.delete()
                await message.delete()
                return
            
            doc = r
            origin = link
            
            max_attempts = 5
            for attempt in range(max_attempts):
                try:
                    result = await self._load_module(
                        lm,
                        doc,
                        origin,
                        attempt
                    )
                    
                    if result == "success":
                        if lm.fully_loaded:
                            lm.update_modules_in_db()
                        
                        status_msg = await message.respond("✅")
                        await asyncio.sleep(0.5)
                        await status_msg.delete()
                        await message.delete()
                        return
                    
                    elif result == "retry":
                        if attempt < max_attempts - 1:
                            await asyncio.sleep(0.33)
                            continue
                        else:
                            status_msg = await message.respond("📋")
                            await asyncio.sleep(1)
                            await status_msg.delete()
                            await message.delete()
                            return
                    
                    elif isinstance(result, dict) and result.get("type") == "requirements_error":
                        deps = result.get("deps",[])
                        if deps:
                            deps_text = ",".join(deps[:5])
                            status_msg = await message.respond(f"📋{deps_text}")
                        else:
                            status_msg = await message.respond("📋")
                        await asyncio.sleep(1)
                        await status_msg.delete()
                        await message.delete()
                        return
                    
                    elif result == "overwrite":
                        status_msg = await message.respond("😨")
                        await asyncio.sleep(1)
                        await status_msg.delete()
                        await message.delete()
                        return
                    
                    else:
                        status_msg = await message.respond("❌")
                        await asyncio.sleep(0.67)
                        await status_msg.delete()
                        await message.delete()
                        return
                        
                except Exception:
                    status_msg = await message.respond("❌")
                    await asyncio.sleep(0.67)
                    await status_msg.delete()
                    await message.delete()
                    return
            
            status_msg = await message.respond("📋")
            await asyncio.sleep(1)
            await status_msg.delete()
            await message.delete()
            
        except Exception:
            status_msg = await message.respond("❌")
            await asyncio.sleep(0.67)
            await status_msg.delete()
            await message.delete()

    async def _load_module(self, lm, doc, origin, attempt):
        if attempt == 0:
            requirements = []
            try:
                requirements = list(
                    filter(
                        lambda x: not x.startswith(("-", "_", ".")),
                        map(
                            lambda s: s.strip().rstrip(','),
                            loader.VALID_PIP_PACKAGES.search(doc)[1].split(),
                        ),
                    )
                )
            except (TypeError, AttributeError):
                pass
            
            if requirements:
                is_venv = hasattr(sys, 'real_prefix') or sys.prefix != getattr(sys, 'base_prefix', sys.prefix)
                need_user_flag = loader.USER_INSTALL and not is_venv
                
                pip = await asyncio.create_subprocess_exec(
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    "--upgrade",
                    "-q",
                    "--disable-pip-version-check",
                    "--no-warn-script-location",
                    *["--user"] if need_user_flag else [],
                    *requirements,
                )
                
                rc = await pip.wait()
                
                if rc != 0:
                    return {"type": "requirements_error", "deps": requirements}
                
                __import__('importlib').invalidate_caches()
                return "retry"
            
            packages = []
            try:
                packages = list(
                    filter(
                        lambda x: not x.startswith(("-", "_", ".")),
                        map(
                            lambda s: s.strip().rstrip(','),
                            loader.VALID_APT_PACKAGES.search(doc)[1].split(),
                        ),
                    )
                )
            except (TypeError, AttributeError):
                pass
            
            if packages:
                result = await lm.install_packages(packages)
                if not result:
                    return {"type": "requirements_error", "deps": packages}
                __import__('importlib').invalidate_caches()
                return "retry"
        
        try:
            node = ast.parse(doc)
            uid = next(
                n.name
                for n in node.body
                if isinstance(n, ast.ClassDef)
                and any(
                    isinstance(base, ast.Attribute)
                    and base.value.id == "Module"
                    or isinstance(base, ast.Name)
                    and base.id == "Module"
                    for base in n.bases
                )
            )
        except Exception:
            uid = "__extmod_" + str(uuid.uuid4())
        
        module_name = f"heroku.modules.{uid}"
        
        try:
            spec = ModuleSpec(
                module_name,
                loader.StringLoader(doc, f"<external {module_name}>"),
                origin=f"<external {module_name}>",
            )
            instance = await lm.allmodules.register_module(
                spec,
                module_name,
                origin,
                save_fs=False,
            )
        except ImportError as e:
            requirements = [
                {
                    "sklearn": "scikit-learn",
                    "pil": "Pillow",
                    "herokutl": "Heroku-TL-New",
                }.get(e.name.lower(), e.name)
            ]
            
            if not requirements:
                return "error"
            
            is_venv = hasattr(sys, 'real_prefix') or sys.prefix != getattr(sys, 'base_prefix', sys.prefix)
            need_user_flag = loader.USER_INSTALL and not is_venv
            
            pip = await asyncio.create_subprocess_exec(
                sys.executable,
                "-m",
                "pip",
                "install",
                "--upgrade",
                "-q",
                "--disable-pip-version-check",
                "--no-warn-script-location",
                *["--user"] if need_user_flag else [],
                *requirements,
            )
            
            rc = await pip.wait()
            
            if rc != 0:
                return {"type": "requirements_error", "deps": requirements}
            
            __import__('importlib').invalidate_caches()
            return "retry"
            
        except CoreOverwriteError:
            with __import__('contextlib').suppress(Exception):
                await lm.allmodules.unload_module(instance.__class__.__name__)
            with __import__('contextlib').suppress(Exception):
                lm.allmodules.modules.remove(instance)
            return "overwrite"
        except (loader.LoadError, ScamDetectionError):
            with __import__('contextlib').suppress(Exception):
                await lm.allmodules.unload_module(instance.__class__.__name__)
            with __import__('contextlib').suppress(Exception):
                lm.allmodules.modules.remove(instance)
            return "error"
        except Exception:
            return "error"
        
        try:
            lm.allmodules.send_config_one(instance)
            
            await lm.allmodules.send_ready_one(
                instance,
                no_self_unload=True,
                from_dlmod=False,
            )
        except CoreOverwriteError:
            with __import__('contextlib').suppress(Exception):
                await lm.allmodules.unload_module(instance.__class__.__name__)
            with __import__('contextlib').suppress(Exception):
                lm.allmodules.modules.remove(instance)
            return "overwrite"
        except (loader.LoadError, ScamDetectionError, loader.SelfUnload, loader.SelfSuspend):
            with __import__('contextlib').suppress(Exception):
                await lm.allmodules.unload_module(instance.__class__.__name__)
            with __import__('contextlib').suppress(Exception):
                lm.allmodules.modules.remove(instance)
            return "error"
        except Exception:
            return "error"
        
        return "success"
