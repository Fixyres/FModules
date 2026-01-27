__version__ = (1, 0, 0)

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
        "not_right": "Das ist er nicht",
        "error": "<b>Ein Fehler ist aufgetreten, bitte versuchen Sie es erneut.</b>",
        "failed": "<b>Charakter konnte nicht erraten werden.</b>",
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
    )
    async def akinator(self, message):
        """- start the game."""

        try:
            aki = akinator.AsyncAkinator()
            
            lang = self.strings("lang")
            
            await aki.start_game(language=lang, child_mode=self.config["child_mode"])
            
            self.games.update({message.chat_id: {message.id: aki}})

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

        aki = self.games[chat_id][mid]
        
        text = await self._translate(aki.question)
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

    async def _translate(self, text):
        if not text or not isinstance(text, str) or len(text.strip()) == 0:
            return text or ""
        
        try:
            target_lang = self.strings("lang")
            
            if len(text) > 5000:
                text = text[:5000]
            
            translated = deep_translator.GoogleTranslator(
                source="auto", 
                target=target_lang
            ).translate(text)
            return translated
        except Exception:
            return text

    async def _show_guess(self, call: InlineCall, aki, message):
        name = getattr(aki, 'name_proposition', None) or "Unknown"
        description = getattr(aki, 'description_proposition', None) or ""
        picture = getattr(aki, 'photo', None) or "https://raw.githubusercontent.com/Fixyres/FModules/refs/heads/main/assets/akinator/banner.png"
        
        description_translated = await self._translate(description) if description else ""
        
        text = self.strings("this_is").format(name=name, description=description_translated)
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
            
            aki = self.games[chat_id][mid]
            
            try:
                await aki.exclude()
                
                aki.name_proposition = None
                aki.description_proposition = None
                aki.photo = None
            except Exception:
                await self.finish_game(call, message, False, "", "")
                return
            
            text = await self._translate(aki.question)
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
            
            aki = self.games[chat_id][mid]
            
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
                text = await self._translate(aki.question)
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