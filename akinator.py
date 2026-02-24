__version__ = (1, 0, 1)

# ©️ Fixyres, 2026
# 🌐 https://github.com/Fixyres/FModules
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 🔑 http://www.apache.org/licenses/LICENSE-2.0

# forked from: https://raw.githubusercontent.com/pixwet/Astro-modules/refs/heads/main/akinator.py

# meta banner: https://raw.githubusercontent.com/Fixyres/FModules/refs/heads/main/assets/akinator/banner.png
# meta pic: https://raw.githubusercontent.com/Fixyres/FModules/refs/heads/main/assets/akinator/pic.png
# meta developer: @FModules

# requires: akinator deep_translator

import akinator
import deep_translator

from .. import loader, utils
from ..inline.types import InlineCall


@loader.tds
class Akinator(loader.Module):
    """Akinator will guess any character you have in mind, you just need to answer a couple of questions."""

    strings = {
        "name": "Akinator",
        "lang": "en",
        "child_mode": "Child mode. If enabled, it will be easier to guess 18+ heroes",
        "start": "Start",
        "text": "<b>Guess any character you have in mind, and click on the Start button.</b>",
        "yes": "Yes",
        "no": "No",
        "idk": "I don't know",
        "probably": "Probably",
        "probably_not": "Probably not",
        "this_is": "<b>This is <code>{name}</code>\n<code>{description}</code></b>",
        "this_is_no_desc": "<b>This is <code>{name}</code></b>",
        "not_right": "Not right",
        "error": "<b>An error occurred, please try again.</b>",
        "failed": "<b>Failed to guess the character.</b>",
    }

    strings_ru = {
        "lang": "ru",
        "_cls_doc": "Акинатор угадает любого вами загаданного персонажа, стоит лишь ответить на пару вопросов.",
        "child_mode": "Детский режим. Если включен, то будет сложнее отгадать 18+ героев",
        "start": "Начать",
        "text": "<b>Задумайте реального или вымышленного персонажа, и нажмите начать.</b>",
        "yes": "Да",
        "no": "Нет",
        "idk": "Не знаю",
        "probably": "Возможно",
        "probably_not": "Скорее нет",
        "this_is": "<b>Это <code>{name}</code>\n<code>{description}</code></b>",
        "this_is_no_desc": "<b>Это <code>{name}</code></b>",
        "not_right": "Это не он",
        "error": "<b>Произошла ошибка, попробуйте снова.</b>",
        "failed": "<b>Не удалось угадать персонажа.</b>",
    }

    strings_ua = {
        "lang": "uk",
        "_cls_doc": "Акінатор вгадає будь-якого персонажа, якого ви загадали, варто лише відповісти на кілька питань.",
        "child_mode": "Дитячий режим. Якщо увімкнено, то буде складніше відгадати 18+ героїв",
        "start": "Почати",
        "text": "<b>Загадайте реального або вигаданого персонажа, і натисніть почати.</b>",
        "yes": "Так",
        "no": "Ні",
        "idk": "Не знаю",
        "probably": "Можливо",
        "probably_not": "Швидше ні",
        "this_is": "<b>Це <code>{name}</code>\n<code>{description}</code></b>",
        "this_is_no_desc": "<b>Це <code>{name}</code></b>",
        "not_right": "Це не він",
        "error": "<b>Сталася помилка, спробуйте знову.</b>",
        "failed": "<b>Не вдалося вгадати персонажа.</b>",
    }

    strings_de = {
        "lang": "de",
        "_cls_doc": "Akinator errät jeden Charakter, den du dir vorstellst, du musst nur ein paar Fragen beantworten.",
        "child_mode": "Kindermodus. Wenn aktiviert, wird es schwieriger sein, 18+ Helden zu erraten",
        "start": "Start",
        "text": "<b>Denk dir einen realen oder fiktiven Charakter aus und klicke auf Start.</b>",
        "yes": "Ja",
        "no": "Nein",
        "idk": "Ich weiß nicht",
        "probably": "Wahrscheinlich",
        "probably_not": "Wahrscheinlich nicht",
        "this_is": "<b>Das ist <code>{name}</code>\n<code>{description}</code></b>",
        "this_is_no_desc": "<b>Das ist <code>{name}</code></b>",
        "not_right": "Das ist er nicht",
        "error": "<b>Ein Fehler ist aufgetreten, bitte versuchen Sie es erneut.</b>",
        "failed": "<b>Charakter konnte nicht erraten werden.</b>",
    }

    strings_fr = {
        "lang": "fr",
        "_cls_doc": "Akinator devinera n'importe quel personnage auquel vous pensez, il vous suffit de répondre à quelques questions.",
        "child_mode": "Mode enfant. Si activé, il sera plus difficile de deviner les héros 18+",
        "start": "Commencer",
        "text": "<b>Pensez à un personnage réel ou fictif et cliquez sur Commencer.</b>",
        "yes": "Oui",
        "no": "Non",
        "idk": "Je ne sais pas",
        "probably": "Probablement",
        "probably_not": "Probablement pas",
        "this_is": "<b>C'est <code>{name}</code>\n<code>{description}</code></b>",
        "this_is_no_desc": "<b>C'est <code>{name}</code></b>",
        "not_right": "Ce n'est pas lui",
        "error": "<b>Une erreur s'est produite, veuillez réessayer.</b>",
        "failed": "<b>Impossible de deviner le personnage.</b>",
    }

    strings_jp = {
        "lang": "ja",
        "_cls_doc": "アキネーターはあなたが考えているキャラクターを当てます。いくつかの質問に答えるだけです。",
        "child_mode": "子供モード。有効にすると、18+のヒーローを推測するのが難しくなります",
        "start": "開始",
        "text": "<b>実在または架空のキャラクターを思い浮かべて、開始ボタンをクリックしてください。</b>",
        "yes": "はい",
        "no": "いいえ",
        "idk": "わかりません",
        "probably": "おそらく",
        "probably_not": "おそらく違う",
        "this_is": "<b>これは <code>{name}</code>\n<code>{description}</code></b>",
        "this_is_no_desc": "<b>これは <code>{name}</code></b>",
        "not_right": "違います",
        "error": "<b>エラーが発生しました。もう一度お試しください。</b>",
        "failed": "<b>キャラクターを推測できませんでした。</b>",
    }

    strings_uz = {
        "lang": "uz",
        "_cls_doc": "Akinator siz o'ylagan har qanday qahramonni topadi, faqat bir nechta savollarga javob bering.",
        "child_mode": "Bolalar rejimi. Yoqilgan bo'lsa, 18+ qahramonlarni topish qiyinroq bo'ladi",
        "start": "Boshlash",
        "text": "<b>Haqiqiy yoki xayoliy qahramonni o'ylang va Boshlash tugmasini bosing.</b>",
        "yes": "Ha",
        "no": "Yo'q",
        "idk": "Bilmayman",
        "probably": "Ehtimol",
        "probably_not": "Ehtimol yo'q",
        "this_is": "<b>Bu <code>{name}</code>\n<code>{description}</code></b>",
        "this_is_no_desc": "<b>Bu <code>{name}</code></b>",
        "not_right": "Bu u emas",
        "error": "<b>Xatolik yuz berdi, qaytadan urinib ko'ring.</b>",
        "failed": "<b>Qahramonni topib bo'lmadi.</b>",
    }

    strings_kz = {
        "lang": "kk",
        "_cls_doc": "Акинатор сіз ойлаған кез келген кейіпкерді табады, тек бірнеше сұрақтарға жауап беріңіз.",
        "child_mode": "Балалар режимі. Қосылған болса, 18+ кейіпкерлерді табу қиынырақ болады",
        "start": "Бастау",
        "text": "<b>Нақты немесе ойдан шығарылған кейіпкерді ойлаңыз және Бастау түймесін басыңыз.</b>",
        "yes": "Иә",
        "no": "Жоқ",
        "idk": "Білмеймін",
        "probably": "Мүмкін",
        "probably_not": "Мүмкін емес",
        "this_is": "<b>Бұл <code>{name}</code>\n<code>{description}</code></b>",
        "this_is_no_desc": "<b>Бұл <code>{name}</code></b>",
        "not_right": "Бұл ол емес",
        "error": "<b>Қате орын алды, қайталап көріңіз.</b>",
        "failed": "<b>Кейіпкерді таба алмадық.</b>",
    }

    suplang = {
        "en": "english",
        "de": "german",
        "fr": "french",
        "jp": "japanese",
        "ru": "russian"
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "child_mode",
                False,
                lambda: self.strings("child_mode"),
                validator=loader.validators.Boolean()
            )
        )

    async def client_ready(self):
        self.games = {}

    @loader.command(
        ru_doc="- начать игру.",
        ua_doc="- почати гру.",
        de_doc="- Spiel starten.",
        fr_doc="- commencer le jeu.",
        jp_doc="- ゲームを開始します。",
        uz_doc="- o'yinni boshlash.",
        kz_doc="- ойынды бастау.",
    )
    async def akinator(self, message):
        """- start the game."""
        try:
            aki = akinator.AsyncAkinator()
            
            user_lang = self.strings("lang")
            aki_lang = self.suplang.get(user_lang, "english")
            
            await aki.start_game(language=aki_lang, child_mode=self.config["child_mode"])
            
            self.games.update({message.chat_id: {message.id: {"aki": aki, "user_lang": user_lang, "aki_lang": aki_lang}}})

            await self.inline.form(
                message=message,
                photo="https://raw.githubusercontent.com/Fixyres/FModules/refs/heads/main/assets/akinator/banner.png",
                text=self.strings("text"),
                reply_markup={
                    "text": self.strings("start"),
                    "callback": self.doai,
                    "args": (message,),
                }
            )
        except Exception as e:
            await utils.answer(message, f"<code>{str(e)}</code>")

    async def doai(self, call, message):
        chat_id = int(message.chat_id)
        mid = int(message.id)

        if chat_id not in self.games or mid not in self.games[chat_id]:
            await call.edit(
                self.strings("error"), 
                photo="https://raw.githubusercontent.com/Fixyres/FModules/refs/heads/main/assets/akinator/idk.png"
            )
            return

        game_data = self.games[chat_id][mid]
        aki = game_data["aki"]
        user_lang = game_data["user_lang"]
        aki_lang = game_data["aki_lang"]
        
        text = await self._translate(aki.question, user_lang, aki_lang)
        await self._show_question(call, text, message)

    async def _show_question(self, call: InlineCall, text: str, message):
        await call.edit(
            text=f"<b>{text}</b>",
            photo="https://raw.githubusercontent.com/Fixyres/FModules/refs/heads/main/assets/akinator/banner.png",
            reply_markup=[
                [
                    {
                        "text": self.strings("yes"),
                        "callback": self.cont,
                        "args": ("y", message,),
                    },
                    {
                        "text": self.strings("no"),
                        "callback": self.cont,
                        "args": ("n", message,),
                    },
                    {
                        "text": self.strings("idk"),
                        "callback": self.cont,
                        "args": ("i", message,),
                    }
                ],
                [
                    {
                        "text": self.strings("probably"),
                        "callback": self.cont,
                        "args": ("p", message,),
                    },
                    {
                        "text": self.strings("probably_not"),
                        "callback": self.cont,
                        "args": ("pn", message,),
                    }
                ]
            ]
        )

    async def _translate(self, text, user_lang, aki_lang):
        if not text or not isinstance(text, str) or len(text.strip()) == 0:
            return text or ""
        
        if user_lang == aki_lang or aki_lang == self.suplang.get(user_lang):
            return text
        
        try:
            if len(text) > 5000:
                text = text[:5000]
            
            translated = deep_translator.GoogleTranslator(
                source="auto", 
                target=user_lang
            ).translate(text)
            return translated
        except Exception:
            return text

    async def _show_guess(self, call: InlineCall, aki, message):
        chat_id = int(message.chat_id)
        mid = int(message.id)
        
        game_data = self.games[chat_id][mid]
        user_lang = game_data["user_lang"]
        aki_lang = game_data["aki_lang"]
        
        name = getattr(aki, 'name_proposition', None) or "Unknown"
        description = getattr(aki, 'description_proposition', None) or ""
        picture = getattr(aki, 'photo', None) or "https://raw.githubusercontent.com/Fixyres/FModules/refs/heads/main/assets/akinator/banner.png"
        
        if description and description.strip():
            description_translated = await self._translate(description, user_lang, aki_lang)
            text = self.strings("this_is").format(name=name, description=description_translated)
        else:
            text = self.strings("this_is_no_desc").format(name=name)
        
        await call.edit(
            text, 
            photo=picture,
            reply_markup=[
                [
                    {
                        "text": self.strings("yes"),
                        "callback": self.finish_game,
                        "args": (message, True, text, picture),
                    },
                    {
                        "text": self.strings("not_right"),
                        "callback": self.reject_guess,
                        "args": (message,),
                    },
                ]
            ]
        )

    async def finish_game(self, call: InlineCall, message, won: bool, final_text: str, final_photo: str):
        chat_id = message.chat_id
        mid = message.id
        
        if chat_id in self.games and mid in self.games[chat_id]:
            del self.games[chat_id][mid]
            if not self.games[chat_id]:
                del self.games[chat_id]
        
        if won:
            await call.edit(final_text, photo=final_photo, reply_markup=[])
        else:
            await call.edit(
                self.strings("failed"), 
                photo="https://raw.githubusercontent.com/Fixyres/FModules/refs/heads/main/assets/akinator/idk.png", 
                reply_markup=[]
            )

    async def reject_guess(self, call: InlineCall, message):
        try:
            chat_id = message.chat_id
            mid = message.id
            
            if chat_id not in self.games or mid not in self.games[chat_id]:
                await call.edit(
                    self.strings("error"), 
                    photo="https://raw.githubusercontent.com/Fixyres/FModules/refs/heads/main/assets/akinator/idk.png", 
                    reply_markup=[]
                )
                return
            
            game_data = self.games[chat_id][mid]
            aki = game_data["aki"]
            user_lang = game_data["user_lang"]
            aki_lang = game_data["aki_lang"]
            
            try:
                await aki.exclude()
                
                aki.name_proposition = None
                aki.description_proposition = None
                aki.photo = None
            except Exception:
                await self.finish_game(call, message, False, "", "")
                return
            
            text = await self._translate(aki.question, user_lang, aki_lang)
            await self._show_question(call, text, message)
            
        except Exception as e:
            await call.edit(
                text=self.strings("error") + f"\n<code>{str(e)}</code>",
                photo="https://raw.githubusercontent.com/Fixyres/FModules/refs/heads/main/assets/akinator/idk.png",
                reply_markup=[]
            )

    async def cont(
        self, 
        call: InlineCall, 
        args: str, 
        message
    ):
        try:
            chat_id = message.chat_id
            mid = message.id
            
            if chat_id not in self.games or mid not in self.games[chat_id]:
                await call.edit(
                    self.strings("error"), 
                    photo="https://raw.githubusercontent.com/Fixyres/FModules/refs/heads/main/assets/akinator/idk.png", 
                    reply_markup=[]
                )
                return
            
            game_data = self.games[chat_id][mid]
            aki = game_data["aki"]
            user_lang = game_data["user_lang"]
            aki_lang = game_data["aki_lang"]
            
            try:
                await aki.answer(args)
            except akinator.InvalidChoiceError:
                await self._show_guess(call, aki, message)
                return
            except Exception as e:
                await call.edit(
                    text=self.strings("error") + f"\n<code>{str(e)}</code>",
                    photo="https://raw.githubusercontent.com/Fixyres/FModules/refs/heads/main/assets/akinator/idk.png",
                    reply_markup=[]
                )
                return
            
            has_guess = getattr(aki, 'name_proposition', None) and getattr(aki, 'name_proposition', None) != "Unknown"
            
            if aki.finished or has_guess:
                await self._show_guess(call, aki, message)
            else:
                text = await self._translate(aki.question, user_lang, aki_lang)
                await self._show_question(call, text, message)
                
        except akinator.CantGoBackAnyFurther:
            await call.edit(
                text=self.strings("failed"),
                photo="https://raw.githubusercontent.com/Fixyres/FModules/refs/heads/main/assets/akinator/idk.png",
                reply_markup=[]
            )
        except Exception as e:
            await call.edit(
                text=self.strings("error") + f"\n<code>{str(e)}</code>",
                photo="https://raw.githubusercontent.com/Fixyres/FModules/refs/heads/main/assets/akinator/idk.png",
                reply_markup=[]
        )
