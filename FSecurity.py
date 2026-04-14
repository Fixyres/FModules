__version__ = (1, 0, 0)

# meta developer: @FModules

# ©️ Fixyres, 2024-2030
# 🌐 https://github.com/Fixyres/FModules
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 🔑 http://www.apache.org/licenses/LICENSE-2.0

import asyncio
import aiohttp
import html
import sys
import uuid
import copy
from contextlib import suppress
from .. import loader, utils


@loader.tds
class FSecurity(loader.Module):
    """Module for automatic AI-based security checks of installed modules."""

    strings = {
        "name": "FSecurity",
        "lang": "en",
        "unavailable": "AI module check is unavailable{}",
        "suspicious": "AI interrupted installation of a suspicious module{}, reason:",
        "blocked": "AI blocked module installation{}, reason:",
        "continue": "Continue installation?",
        "strict_mode_doc": "Block loading modules by any method (not just dlm/lm) if the AI API is unavailable or the module is suspicious. On restart, this also applies to already installed modules."
    }

    strings_ru = {
        "lang": "ru",
        "_cls_doc": "Модуль для автоматической проверки устанавливаемых модулей через ИИ.",
        "unavailable": "Проверка модуля через ИИ недоступна{}",
        "suspicious": "ИИ прервал установку подозрительного модуля{}, причина:",
        "blocked": "ИИ заблокировал установку модуля{}, причина:",
        "continue": "Продолжить установку?",
        "strict_mode_doc": "Не позволять загружать модули любым методом (не только dlm/lm), если API ИИ недоступен или модуль подозрителен. При перезагрузке работает даже на уже установленные модули."
    }

    strings_ua = {
        "lang": "ua",
        "_cls_doc": "Модуль для автоматичної перевірки встановлюваних модулів через ШІ.",
        "unavailable": "Перевірка модуля через ШІ недоступна{}",
        "suspicious": "ШІ перервав встановлення підозрілого модуля{}, причина:",
        "blocked": "ШІ заблокував встановлення модуля{}, причина:",
        "continue": "Продовжити встановлення?",
        "strict_mode_doc": "Не дозволяти завантажувати модулі будь-яким методом (не лише dlm/lm), якщо API ШІ недоступний або модуль підозрілий. При перезавантаженні працює навіть на вже встановлені модулі."
    }

    strings_de = {
        "lang": "de",
        "_cls_doc": "Modul zur automatischen Prüfung installierter Module mit KI.",
        "unavailable": "Die KI-Modulprüfung ist nicht verfügbar{}",
        "suspicious": "Die KI hat die Installation eines verdächtigen Moduls unterbrochen{}, Grund:",
        "blocked": "Die KI hat die Modulinstallation blockiert{}, Grund:",
        "continue": "Installation fortsetzen?",
        "strict_mode_doc": "Das Laden von Modulen mit jeder Methode (nicht nur dlm/lm) blockieren, wenn die KI-API nicht verfügbar ist oder das Modul verdächtig ist. Beim Neustart gilt dies auch für bereits installierte Module."
    }

    strings_jp = {
        "lang": "jp",
        "_cls_doc": "AIでインストールされるモジュールを自動チェックするモジュール。",
        "unavailable": "AIモジュールのチェックが利用できません{}",
        "suspicious": "AIが疑わしいモジュールのインストールを中断しました{}、理由：",
        "blocked": "AIがモジュールのインストールをブロックしました{}、理由：",
        "continue": "インストールを続行しますか？",
        "strict_mode_doc": "AI APIが利用できない場合や疑わしいモジュールの場合、dlm/lmだけでなくすべての方法でモジュールの読み込みをブロックします。再起動時にはインストール済みモジュールにも適用されます。"
    }

    strings_tr = {
        "lang": "tr",
        "_cls_doc": "Kurulan modülleri yapay zeka ile otomatik kontrol eden modül.",
        "unavailable": "Yapay zeka modül kontrolü kullanılamıyor{}",
        "suspicious": "Yapay zeka şüpheli bir modülün kurulumunu durdurdu{}, sebep:",
        "blocked": "Yapay zeka modül kurulumunu engelledi{}, sebep:",
        "continue": "Kuruluma devam edilsin mi?",
        "strict_mode_doc": "AI API kullanılamıyorsa veya modül şüpheliyse, sadece dlm/lm değil tüm yöntemlerle modül yüklenmesini engelle. Yeniden başlatmada zaten kurulu modüller için de geçerlidir."
    }

    strings_uz = {
        "lang": "uz",
        "_cls_doc": "O'rnatilayotgan modullarni AI orqali avtomatik tekshiruvchi modul.",
        "unavailable": "AI modul tekshiruvi mavjud emas{}",
        "suspicious": "AI shubhali modul o'rnatilishini to'xtatdi{}, sabab:",
        "blocked": "AI modul o'rnatilishini blokladi{}, sabab:",
        "continue": "O'rnatishni davom ettirasizmi?",
        "strict_mode_doc": "AI API mavjud bo'lmasa yoki modul shubhali bo'lsa, faqat dlm/lm emas, barcha usullar bilan modul yuklashni bloklash. Qayta ishga tushirishda allaqachon o'rnatilgan modullarga ham ta'sir qiladi."
    }

    strings_kz = {
        "lang": "kz",
        "_cls_doc": "Орнатылатын модульдерді ЖИ арқылы автоматты тексеретін модуль.",
        "unavailable": "AI модульін тексеру қолжетімсіз{}",
        "suspicious": "AI күдікті модульді орнатуды тоқтатты{}, себебі:",
        "blocked": "AI модульді орнатуды бұғаттады{}, себебі:",
        "continue": "Орнатуды жалғастырасыз ба?",
        "strict_mode_doc": "AI API қолжетімсіз болса немесе модуль күдікті болса, тек dlm/lm ғана емес, барлық әдістермен модуль жүктеуді бұғаттау. Қайта іске қосқанда орнатылған модульдерге де қолданылады."
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "strict_mode",
                False,
                lambda: self.strings("strict_mode_doc"),
                validator=loader.validators.Boolean(),
            )
        )
        self.tasks = {}
        self.oreg = None
        self.oload = None

    async def client_ready(self, client, db):
        self.core = self.lookup("loader")
        self.modules = self.core.allmodules
        self.restore_hooks()
        self.patch()

    async def on_unload(self):
        self.unpatch()

    async def check(self, code):
        try:
            form = aiohttp.FormData()
            form.add_field('file', code.encode('utf-8'), filename='module.py', content_type='text/x-python')
            form.add_field('lang', self.strings("lang") or "en")

            async with aiohttp.ClientSession() as session:
                async with session.post("https://api.fixyres.com/check", data=form, timeout=60) as resp:
                    if resp.status != 200:
                        return False
                    return await resp.json()
        except Exception:
            return False

    def format(self, state, reason="", link=""):
        link_part = f' (<code>{utils.escape_html(link)}</code>)' if link else ""
        if state == "unavailable":
            return f'<b>{self.strings("unavailable").format(link_part)}</b>\n<b>{self.strings("continue")}</b>'
        if state == "suspicious":
            return f'<b>{self.strings("suspicious").format(link_part)}</b>\n<blockquote expandable>{utils.escape_html(reason)}</blockquote>\n<b>{self.strings("continue")}</b>'
        return f'<b>{self.strings("blocked").format(link_part)}</b>\n<blockquote expandable>{utils.escape_html(reason)}</blockquote>'

    def buttons(self, task):
        return [[
            {"text": "✓", "callback": self.confirm, "args": (task, "yes")},
            {"text": "✗", "callback": self.confirm, "args": (task, "no")}
        ]]

    def closure_var(self, func, name):
        raw = getattr(func, "__func__", func)
        code = getattr(raw, "__code__", None)
        closure = getattr(raw, "__closure__", None)
        if not code or not closure or name not in code.co_freevars:
            return None

        with suppress(Exception):
            return closure[code.co_freevars.index(name)].cell_contents

        return None

    def restore_hooks(self):
        with suppress(Exception):
            inst_reg = getattr(self.modules, "register_module")
            owner = getattr(inst_reg, "__self__", None)
            if (
                owner
                and owner is not self
                and owner.__class__.__name__ == self.__class__.__name__
            ):
                original = getattr(owner, "oreg", None)
                if original:
                    if getattr(original, "__self__", None) is None:
                        self.modules.register_module = original.__get__(
                            self.modules,
                            self.modules.__class__,
                        )
                    else:
                        self.modules.register_module = original

        with suppress(Exception):
            inst_load = getattr(self.core, "load_module")
            raw = getattr(inst_load, "__func__", inst_load)
            if "FSecurity.patch.<locals>.load" in getattr(raw, "__qualname__", ""):
                original = self.closure_var(raw, "original")
                if original:
                    if getattr(original, "__self__", None) is None:
                        self.core.load_module = original.__get__(
                            self.core,
                            self.core.__class__,
                        )
                    else:
                        self.core.load_module = original

    def patch(self):
        if not self.oreg:
            self.oreg = getattr(self.modules, "register_module")
        if not self.oload:
            self.oload = self.core.load_module

        original = self.oload

        async def load(_, *args, **kwargs):
            base = utils.answer

            async def answer(message, response, *a, **k):
                if isinstance(response, str) and "😖</tg-emoji>" in response:
                    body = response.split("😖</tg-emoji>", 1)[1].strip()
                    if body in {"", "<b></b>", "<b> </b>"}:
                        with suppress(Exception):
                            if hasattr(message, "delete"):
                                await message.delete()
                        return message

                    if body.startswith("<b>") and body.endswith("</b>"):
                        decoded = html.unescape(body[3:-4])
                        response = response.split("😖</tg-emoji>", 1)[0] + f'😖</tg-emoji> {decoded}' if decoded else response.split("😖</tg-emoji>", 1)[0] + '😖</tg-emoji>'

                try:
                    return await base(message, response, *a, **k)
                except Exception:
                    with suppress(Exception):
                        return await self._client.send_message(
                            utils.get_chat_id(message),
                            response,
                            reply_to=getattr(message, "reply_to_msg_id", None),
                            buttons=k.get("reply_markup"),
                        )

                    return message

            utils.answer = answer
            try:
                if getattr(original, "__self__", None) is None:
                    return await original(_, *args, **kwargs)
                return await original(*args, **kwargs)
            finally:
                if utils.answer is answer:
                    utils.answer = base

        self.core.load_module = load.__get__(self.core, self.core.__class__)
        self.modules.register_module = self.register

    def unpatch(self):
        if self.oreg:
            self.modules.register_module = self.oreg
        if getattr(self, "core", None) and self.oload:
            self.core.load_module = self.oload

    def context(self):
        frame = sys._getframe()
        msg = None
        fmsg = None
        is_dlm_lm = False

        while frame:
            locals = frame.f_locals
            if (
                frame.f_code.co_name == "load_module"
                and locals.get("self") is self.core
                and 'message' in locals
                and hasattr(locals['message'], 'edit')
            ):
                if not msg:
                    msg = locals['message']
                    fmsg = locals.get('msg')

            if frame.f_code.co_name in {"dlmod", "loadmod"}:
                is_dlm_lm = True
                if not msg and 'message' in locals and hasattr(locals['message'], 'edit'):
                    msg = locals['message']

            if frame.f_code.co_name == "download_and_install":
                if not msg and 'message' in locals and hasattr(locals['message'], 'edit'):
                    msg = locals['message']

            frame = frame.f_back

        return msg, fmsg, is_dlm_lm

    def target_chat(self, msg=None, fmsg=None):
        if not msg:
            return None

        if not fmsg:
            return msg

        with suppress(Exception):
            target = copy.copy(msg)
            target.reply_to_msg_id = fmsg.id
            return target

        return None

    async def call_oreg(self, spec, name, origin="<core>", save_fs=False):
        if getattr(self.oreg, "__self__", None) is None:
            return await self.oreg(self.modules, spec, name, origin, save_fs=save_fs)
        return await self.oreg(spec, name, origin, save_fs=save_fs)

    async def register(self, spec, name, origin="<core>", save_fs=False):
        if origin != "<core>":
            code = ""

            if hasattr(spec.loader, "data") and spec.loader.data:
                code = spec.loader.data
                if isinstance(code, bytes):
                    code = code.decode("utf-8", errors="ignore")
            elif origin and origin.endswith(".py"):
                with suppress(Exception):
                    with open(origin, "r", encoding="utf-8") as f:
                        code = f.read()

            if code:
                check = await self.check(code)

                if check is not True:
                    msg, fmsg, is_dlm_lm = self.context()
                    target = self.target_chat(msg, fmsg)

                    if isinstance(check, dict):
                        status = check.get("level", "blocked")
                        reason = check.get("reason", "")
                    else:
                        status = "unavailable"
                        reason = ""

                    link = origin if origin.startswith("http") else ""

                    if status == "blocked":
                        if msg and target:
                            raise loader.LoadError(self.format("blocked", reason, link))
                        raise loader.LoadError("")

                    should_block = is_dlm_lm or self.config["strict_mode"]

                    if should_block and not (msg and target):
                        raise loader.LoadError("")

                    if should_block and msg and target:
                        task = str(uuid.uuid4())
                        event = asyncio.Event()
                        self.tasks[task] = {"event": event, "decision": False}

                        try:
                            form = await self.inline.form(
                                text=self.format(status, reason, link),
                                message=target,
                                reply_markup=self.buttons(task)
                            )

                            if not form:
                                raise loader.LoadError(reason)

                            await asyncio.wait_for(event.wait(), timeout=60.0)

                            if not self.tasks.pop(task)["decision"]:
                                with suppress(Exception):
                                    await form.delete()
                                raise loader.LoadError("")

                        except asyncio.TimeoutError:
                            self.tasks.pop(task, None)
                            with suppress(Exception):
                                await form.delete()
                            raise loader.LoadError("")
                        except loader.LoadError:
                            raise
                        except Exception:
                            raise loader.LoadError("")

        return await self.call_oreg(spec, name, origin, save_fs=save_fs)

    async def confirm(self, call, task, action):
        if task in self.tasks:
            self.tasks[task]["decision"] = (action == "yes")
            self.tasks[task]["event"].set()
        with suppress(Exception):
            await call.delete()
