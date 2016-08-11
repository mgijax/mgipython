from mgipython.dao.vocterm_dao import VocTermDAO
from mgipython.error import NotFoundError
from mgipython.modelconfig import cache
from mgipython.model.query import batchLoadAttribute

class VocTermService():
    
    vocterm_dao = VocTermDAO()
    
    def get_by_key(self, _term_key):
        term = self.vocterm_dao.get_by_key(_term_key)
        if not term:
            raise NotFoundError("No VocTerm for _term_key=%d" % _term_key)
        return term
    
    def get_by_primary_id(self, id):
        term = self.vocterm_dao.get_by_primary_id(id)
        if not term:
            raise NotFoundError("No VocTerm with id=%s" % id)
        return term
    
    
    def search(self, args):
        """
        Search using an argument object
        """
        users = self.user_dao.search(
            login=args.login,
            name=args.name,
            _usertype_key=args._usertype_key,
            _userstatus_key=args._userstatus_key,
            orcid=args.orcid,
            _createdby_key=args._createdby_key,
            _modifiedby_key=args._modifiedby_key
        )
        return users
    
    
    def search_emapa_terms(self,
                         termSearch="",
                         stageSearch="",
                         isobsolete=0,
                         limit=None):
        """
        Search specifically for EMAPA vocterm objects
        """
        terms = self.vocterm_dao.search_emapa_terms(
             termSearch=termSearch,
             stageSearch=stageSearch,
             isobsolete=isobsolete,
             limit=limit
        )
        
        # batch load necessary attributes
        batchLoadAttribute(terms, "emapa_info")
        
        return terms
    
    
        
    def create(self, args):
        """
        Create user with an argument object
        """
        user = MGIUser()
        # get the next primary key
        user._user_key = self.user_dao.get_next_key()
        # set MGIUser values
        user.login = args.login
        user.name = args.name
        user._usertype_key = args._usertype_key
        user._userstatus_key = args._userstatus_key
        
        #user._createdby_key = current_user._user_key
        #user._modifiedby_key = current_user._modifiedby_key
        self.user_dao.save(user)
        
        return user
        
        
    def edit(self, key, args):
        """
        Edit user with and argument object
        """
        user = self.user_dao.get_by_key(key)
        if not user:
            raise NotFoundError("No MGIUser for _user_key=%d" % key)
        user.login = args.login
        user.name = args.name
        user._usertype_key = args._usertype_key
        user._userstatus_key = args._userstatus_key
        #user._modifiedby_key = current_user._modifiedby_key
        
        self.user_dao.save()
        return user
        
        
    def delete(self, _user_key):
        """
        Delete MGIUser object
        """
        user = self.user_dao.get_by_key(_user_key)
        if not user:
            raise NotFoundError("No MGIUser for _user_key=%d" % _user_key)
        self.user_dao.delete(user)
        
    
    
    def get_term_choices_by_vocab_key(self, _vocab_key):
        """
        Get all possible term choices
        for the given _vocab_key
        return format is
        { 'choices': [{'term', '_term_key'}] }
        """
        terms = self.vocterm_dao.search(_vocab_key=_vocab_key)
        json = {
            'choices':[]
        }
        for term in terms:
            json['choices'].append({'term':term.term, '_term_key':term._term_key})
        
        return json
    
        
        