#!/usr/bin/python
# -*- coding: utf-8 -*-
# Code by Javik
# Update by @FreeManRepo

import re
import uuid

from plugin import *

from siriObjects.baseObjects import *
from siriObjects.uiObjects import *
from siriObjects.systemObjects import *
from siriObjects.contactObjects import *


res = {
    'command': {
        'de-DE': u'(Wer bin ich.*)|(Wie ist mein Name.*)',
        'en-US': u'(Who am I.*)|(What\'s my name.*)'
    },
    'answer': {
        'de-DE': u'Du bist {0}, das hast du mir jedenfalls gesagt.',
        'en-US': u'You\'re {0}, that\'s what you told me. anyway.'
    }
}

helpPhrases = {
    'en-US': u'Who am I, Whats my name',
    'de-DE': u'Wer bin ich, Wie ist mein Name',
}

class meCard(Plugin):
	
    @register("en-US", res['command']['en-US'])
    @register('de-DE', res['command']['de-DE'])
	def mePerson(self, speech, language):
		
		self.say(res['answer'][language].format(self.user_name()))		
		person_search = PersonSearch(self.refId)
		person_search.scope = PersonSearch.ScopeLocalValue
		person_search.me = "true"        
		person_return = self.getResponseForRequest(person_search)
		person_ = person_return["properties"]["results"]
		mecard = PersonSnippet(persons=person_)
		view = AddViews(self.refId, dialogPhase="Completion")		
		view.views = [mecard]
		self.sendRequestWithoutAnswer(view)
		self.complete_request()