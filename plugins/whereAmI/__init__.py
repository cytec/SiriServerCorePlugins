#!/usr/bin/python
# -*- coding: utf-8 -*-

#need help? ask john-dev
#updated version to work with SiriServerCore by cytec
 
import re
import urllib2, urllib
import json
 
from plugin import *
 
from siriObjects.systemObjects import GetRequestOrigin, Location
from siriObjects.uiObjects import AddViews, AssistantUtteranceView
from siriObjects.localsearchObjects import MapItem, MapItemSnippet

res = {
    'command': {
        'en-US': u'(Where am I.*)|(What is my location.*)',
        'de-DE': u'Wo bin ich.*',
        'fr-FR': u'(Où suis-je.*)'
    },
    'answer': {
        'en-US': u'Your location',
        'de-DE': u'Dein Standort',
        'fr-FR': u'Votre position'
    }
}

helpPhrases = {
    'en-US': u'Where am I, What is my location',
    'de-DE': u'Wo bin ich',
    'fr-FR': u'Où suis-je'
}


class whereAmI(Plugin):
    
    @register("de-DE", res['command']['de-DE'])
    @register("fr-FR", res['command']['fr-FR'])    
    @register("en-US", res['command']['en-US'])
    def whereAmI(self, speech, language):
        location = self.getCurrentLocation(force_reload=True,accuracy=GetRequestOrigin.desiredAccuracyBest)
        url = "http://maps.googleapis.com/maps/api/geocode/json?latlng={0},{1}&sensor=false&language={2}".format(str(location.latitude),str(location.longitude), language)
        try:
            jsonString = urllib2.urlopen(url, timeout=3).read()
        except:
            pass
        if jsonString != None:
            response = json.loads(jsonString)
            if response['status'] == 'OK':
                components = response['results'][0]['address_components']              
                street = filter(lambda x: True if "route" in x['types'] else False, components)[0]['long_name']
                stateLong= filter(lambda x: True if "administrative_area_level_1" in x['types'] or "country" in x['types'] else False, components)[0]['long_name']
                try:
                    postalCode= filter(lambda x: True if "postal_code" in x['types'] else False, components)[0]['long_name']
                except:
                    postalCode=""
                try:
                    city = filter(lambda x: True if "locality" in x['types'] or "administrative_area_level_1" in x['types'] else False, components)[0]['long_name']
                except:
                    city=""
                countryCode = filter(lambda x: True if "country" in x['types'] else False, components)[0]['short_name']
                view = AddViews(self.refId, dialogPhase="Completion")
                the_header = res['answer'][language]
        view = AddViews(self.refId, dialogPhase="Completion")
        mapsnippet = MapItemSnippet(items=[MapItem(label=postalCode+" "+city, street=street, city=city, postalCode=postalCode, latitude=location.latitude, longitude=location.longitude, detailType="CURRENT_LOCATION")])
        view.views = [AssistantUtteranceView(speakableText=the_header, dialogIdentifier="Map#whereAmI"), mapsnippet]
        self.sendRequestWithoutAnswer(view)
        self.complete_request()