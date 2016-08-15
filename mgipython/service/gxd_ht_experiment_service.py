from mgipython.dao.gxd_ht_experiment_dao import GxdHTExperimentDAO
from mgipython.model import GxdHTExperiment
from mgipython.error import NotFoundError
from mgipython.modelconfig import cache

class GxdHTExperimentService():
    
    gxd_dao = GxdHTExperimentDAO()
    
    def get_by_key(self, _experiment_key):
        experiment = self.gxd_dao.get_by_key(_experiment_key)
        if not experiment:
            raise NotFoundError("No GxdHTExperiment for _experiment_key=%d" % _experiment_key)
        return experiment
    
    def search(self, searchObject):
        experiments = self.gxd_dao.search(searchObject)
        return experiments

#    def edit(self, key, args):
#        user = self.gxd_dao.get_by_key(key)
#        if not user:
#            raise NotFoundError("No MGIUser for _user_key=%d" % key)
#        user.name = args.name
#        user.login = args.login
#        user._usertype_key = args._usertype_key
#        user._userstatus_key = args._userstatus_key
#        #user._modifiedby_key = current_user._modifiedby_key
#        
#        self.gxd_dao.save()
#        return user
#
#
#    def create(self, args):
#
#        experiment = GxdHTExperiment()
#
#        experiment.name = args.name
#        experiment.description = args.description
#        
#        self.gxd_dao.save(experiment)
#        
#        return experiment
#
#    def delete(self, _user_key):
#        """
#        Delete MGIUser object
#        """
#        user = self.gxd_dao.get_by_key(_user_key)
#        if not user:
#            raise NotFoundError("No MGIUser for _user_key=%d" % _user_key)
#        self.gxd_dao.delete(user)
