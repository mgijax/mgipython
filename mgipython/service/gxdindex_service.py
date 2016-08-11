from mgipython.dao.user_dao import GxdIndexDAO
from mgipython.dao.vocterm_dao import VocTermDAO
from mgipython.model import GxdIndexRecord
from mgipython.error import NotFoundError
from mgipython.modelconfig import cache

class GxdIndexService():
    
    gxdindex_dao = GxdIndexDAO()
    vocterm_dao = VocTermDAO()
    
    def get_by_key(self, _index_key):
        gxdindex_record = self.gxdindex_dao.get_by_key(_index_key)
        if not gxdindex_record:
            raise NotFoundError("No GxdIndexRecord for _index_key=%d" % _index_key)
        return gxdindex_record
    
    
    def search(self, args):
        """
        Search using an argument object
        """
        index_records = self.gxdindex_dao.search(
            _refs_key=args._refs_key,
            _marker_key=args._marker_key,
            _priority_key=args._priority_key,
            _conditionalmutants_key=args._conditionalmutants_key,
            comments=args.comments,
            _createdby_key=args._createdby_key,
            _modifiedby_key=args._modifiedby_key
        )
        return index_records
    
    
        
    def create(self, args, current_user):
        """
        Create user with an argument object
        """
        gxdindex_record = GxdIndexRecord()
        # get the next primary key
        gxdindex_record._index_key = self.gxdindex_dao.get_next_key()
        # set GxdIndexRecord values
        gxdindex_record._refs_key = args._refs_key
        gxdindex_record._marker_key = args._marker_key
        gxdindex_record._priority_key = args._priority_key
        gxdindex_record._conditionalmutants_key = args._conditionalmutants_key
        gxdindex_record.comments = args.comments
        gxdindex_record._createdby_key = current_user._user_key
        gxdindex_record._modifiedby_key = current_user._user_key
        
        self.gxdindex_dao.save(gxdindex_record)
        
        return gxdindex_record
        
        
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
        
    
    @cache.memoize()
    def get_user_status_choices(self):
        """
        Get all possible userstatus choices
        return format is
        { 'choices': [{'term', '_term_key'}] }
        """
        terms = self.vocterm_dao.search(_vocab_key=22)
        json = {
            'choices':[]
        }
        for term in terms:
            json['choices'].append({'term':term.term, '_term_key':term._term_key})
        
        return json
    
    @cache.memoize()
    def get_user_type_choices(self):
        """
        Get all possible usertype choices
        return format is
        { 'choices': [{'term', '_term_key'}] }
        """
        terms = self.vocterm_dao.search(_vocab_key=23)
        json = {
            'choices':[]
        }
        for term in terms:
            json['choices'].append({'term':term.term, '_term_key':term._term_key})
        
        return json
        
        