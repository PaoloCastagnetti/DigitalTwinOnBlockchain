import time
class DTClass:

    def __init__(self):
        self.properties=[]
        self.actions=[]
        self.events=[]
        self.associatedPhisicalObjects=[]
        self.relations=[]

        self.propertyValue=[]
        self.actionName=[]
        self.eventValue=[]

        self.timestamp = time.time()

    # ----------PROPERTIES----------
    def addProperty(self, _property, _value):
        print("Adding property ", _property, "with value ", _value)
        self.properties.append(_property)
        self.propertyValue.append(_value)

    def setPropertyValue(self, _property, _value):
        print("Setting property ", _property, "to ", _value)
        k=0
        for i in self.properties:
            if(i==_property):
                self.propertyValue[k]=_value
                break
            k += 1

    def getPropertyValue(self,_property):
        k=0
        for i in self.properties:
            if(i==_property):
                return self.propertyValue[k]
            k += 1
    
    def getProperties(self):
        return self.properties

    def removeProperty(self, _property):
        print("Removing property ", _property)
        k=0
        for i in self.properties:
            if(i==_property):
                self.properties.pop(k)
                self.propertyValue.pop(k)
                break
            k += 1


    # ----------ACTIONS----------
    def addAction(self, _action, _name):
        print("Adding action ", _action, "with name ", _name)
        self.actions.append(_action)
        self.actionName.append(_name)

    def setActionName(self, _action, _name):
        print("Setting action ", _action, "to ", _name)
        k=0
        for i in self.actions:
            if(i==_action):
                self.actionName[k]=_name
                break
            k += 1

    def getActionName(self, _action):
        k=0
        for i in self.actions:
            if(i==_action):
                return self.actionName[k]
            k += 1
    
    def getActions(self):
        return self.actions

    def removeAction(self, _action):
        print("Removing action ", _action)
        k=0
        for i in self.actions:
            if(i==_action):
                self.actions.pop(k)
                self.actionName.pop(k)
                break
            k += 1

    # ----------EVENTS----------
    def addEvent(self, _event, _value):
        print("Adding event ", _event, "with value ", _value)
        self.events.append(_event)
        self.eventValue.append(_value)

    def setEventValue(self, _event, _value):
        print("Setting event ", _event, "to ", _value)
        k=0
        for i in self.events:
            if(i==_event):
                self.eventValue[k]=_value
                break
            k += 1

    def getEventValue(self,_event):
        k=0
        for i in self.events:
            if(i==_event):
                return self.eventValue[k]
            k += 1
    
    def getEvents(self):
        return self.events

    def removeEvent(self, _event):
        print("Removing event ", _event)
        k=0
        for i in self.events:
            if(i==_event):
                self.events.pop(k)
                self.eventValue.pop(k)
                break
            k += 1

    # ----------ASSOCIATED PHISICAL OBJECT----------
    def addAssociatedPhisicalObject(self, _object):
        print("Adding associated phisical object ", _object)
        self.associatedPhisicalObjects.append(_object)

    def getAssociatedPhisicalObjects(self):
        return self.associatedPhisicalObjects
    
    def removeAssociatedPhisicalObjects(self, _object):
        print("Removing associated phisical object ", _object)
        k=0
        for i in self.associatedPhisicalObjects:
            if(i==_object):
                self.associatedPhisicalObjects.pop(k)
                break
            k += 1

    # ----------RELATIONS----------
    def addRelation(self, _address):
        print("Adding relation ", _address)
        self.relations.append(_address)

    def getRelations(self):
        return self.relations
    
    def removeRelation(self, _address):
        print("Removing relation ", _address)
        k=0
        for i in self.relations:
            if(i==_address):
                self.relations.pop(k)
                break
            k += 1