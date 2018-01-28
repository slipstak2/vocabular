#!/usr/bin/env python
# -*- coding: utf-8 -*-


from translate import Translator
translator= Translator(to_lang="ru")
print translator.translate("exciting")
print translator.translate("retrieval")


toEng = Translator(from_lang="ru", to_lang="en")
print toEng.translate(u"захватывающий")



